"""PostgreSQL implementation of MessageStore."""

import json
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
import math

from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    UserPromptPart,
    TextPart
)

from src.memory.message_store import MessageStore
from src.db import execute_query, execute_batch
from src.memory.message_history import TextPart, ToolCall, ToolOutput, ToolCallPart, ToolOutputPart

# Configure logger
logger = logging.getLogger(__name__)

class PostgresMessageStore(MessageStore):
    """PostgreSQL implementation of MessageStore."""
    
    def __init__(self):
        """Initialize the store."""
        logger.info("🔍 Initializing PostgresMessageStore")
        # Test database connection immediately
        try:
            from src.db import get_connection_pool
            pool = get_connection_pool()
            with pool.getconn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version()")
                    version = cur.fetchone()[0]
                    logger.info(f"✅ PostgresMessageStore successfully connected to database: {version}")
                    
                    # Check if run_finished_at column exists in sessions table, add it if not
                    cur.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_name = 'sessions' AND column_name = 'run_finished_at'
                        ) as exists
                    """)
                    column_exists = cur.fetchone()[0]
                    
                    if not column_exists:
                        logger.info("Adding run_finished_at column to sessions table...")
                        try:
                            cur.execute("""
                                ALTER TABLE sessions
                                ADD COLUMN run_finished_at TIMESTAMP WITH TIME ZONE
                            """)
                            conn.commit()
                            logger.info("✅ Added run_finished_at column to sessions table")
                        except Exception as e:
                            logger.error(f"❌ Error adding run_finished_at column: {str(e)}")
                            conn.rollback()
                    
                pool.putconn(conn)
        except Exception as e:
            logger.error(f"❌ PostgresMessageStore failed to connect to database during initialization: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
    
    def get_messages(self, session_id: str) -> List[ModelMessage]:
        """Get all messages for a session.
        
        Args:
            session_id: The session ID to get messages for.
            
        Returns:
            List of ModelMessage objects.
        """
        try:
            # Import necessary functions
            from src.db import list_messages
            
            try:
                # Try to parse the session_id
                session_id_uuid = uuid.UUID(session_id) if session_id else None
            except ValueError:
                logger.error(f"Invalid session ID format: {session_id}")
                return []
            
            # Retrieve messages from the database
            messages = list_messages(session_id_uuid)
            
            # Convert database messages to ModelMessage objects
            result = []
            for msg in messages:
                # Convert from Model to Dict for processing
                message_dict = msg.dict()
                model_message = self._db_to_model_message(message_dict)
                if model_message:
                    result.append(model_message)
            
            logger.debug(f"Retrieved {len(result)} messages for session {session_id}")
            return result
        except Exception as e:
            logger.error(f"Error getting messages for session {session_id}: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
            return []
    
    def add_message(self, session_id: str, message: ModelMessage) -> None:
        """Add a message to a session.
        
        Args:
            session_id: The unique session identifier.
            message: The message to add.
        """
        # Get user_id from message if available, otherwise default to 1
        user_id = getattr(message, "user_id", 1)
        
        try:
            # Make sure the session exists
            session_id = self._ensure_session_exists(session_id, user_id)
            
            # Determine message role
            role = self._determine_message_role(message)
            
            # First, check if the message has direct content attribute (higher priority)
            text_content = ""
            if hasattr(message, "content") and message.content:
                text_content = message.content
                logger.debug(f"Extracted content directly from message: {text_content[:50]}...")
            elif hasattr(message, "message_input") and message.message_input:
                text_content = message.message_input
                logger.debug(f"Extracted content from message_input: {text_content[:50]}...")
            
            assistant_name = None
            agent_id = getattr(message, "agent_id", None)
            
            # Extract context from user messages
            context = getattr(message, "context", None)
            
            # Extract system_prompt from assistant messages
            system_prompt = getattr(message, "system_prompt", None)
            
            # Extract tool calls and outputs
            tool_calls = []
            tool_outputs = []
            
            # If no direct content was found, try to extract from message parts based on role
            if not text_content:
                logger.debug(f"No direct content found, trying to extract from message parts for role: {role}")
                # Handle different message types based on role
                if role == "user":
                    # For user messages, extract content from UserPromptPart
                    for part in message.parts:
                        if hasattr(part, "part_kind") and part.part_kind == "user":
                            if hasattr(part, "content") and part.content:
                                text_content = part.content
                                logger.debug(f"Extracted user content from part: {text_content[:50]}...")
                                break
                elif role == "system":
                    # For system messages, extract content
                    for part in message.parts:
                        if hasattr(part, "part_kind") and part.part_kind == "system":
                            if hasattr(part, "content") and part.content:
                                text_content = part.content
                                logger.debug(f"Extracted system content from part: {text_content[:50]}...")
                                break
                    
                    # Instead of storing system message, update session metadata
                    try:
                        from src.db import get_session, update_session
                        
                        session = get_session(uuid.UUID(session_id))
                        if session:
                            # Get existing metadata or create new dictionary
                            metadata = session.metadata or {}
                            if isinstance(metadata, str):
                                try:
                                    metadata = json.loads(metadata)
                                except json.JSONDecodeError:
                                    metadata = {}
                            
                            # Store system prompt in metadata
                            metadata["system_prompt"] = text_content
                            session.metadata = metadata
                            
                            # Update session
                            update_session(session)
                            logger.debug(f"Stored system prompt in session metadata: {text_content[:50]}...")
                            
                            # Return early - we don't need to create a separate system message
                            return
                        else:
                            logger.error(f"Failed to find session {session_id} to store system prompt")
                    except Exception as e:
                        logger.error(f"Error storing system prompt in metadata: {e}")
                        # Continue to create a system message as fallback
                else:
                    # For assistant messages, extract content from TextPart
                    for part in message.parts:
                        if hasattr(part, "part_kind") and part.part_kind == "text":
                            if hasattr(part, "content") and part.content:
                                text_content = part.content
                                logger.debug(f"Extracted assistant content from part: {text_content[:50]}...")
                                if hasattr(part, "assistant_name") and part.assistant_name:
                                    assistant_name = part.assistant_name
                                break
            
            # Process all parts to collect tool calls and outputs
            for part in message.parts:
                if hasattr(part, "part_kind"):
                    if part.part_kind == "tool-call" and hasattr(part, "tool_call"):
                        tool_calls.append({
                            "tool_name": part.tool_call.tool_name,
                            "args": part.tool_call.args,
                            "tool_call_id": part.tool_call.tool_call_id
                        })
                    elif part.part_kind == "tool-output" and hasattr(part, "tool_output"):
                        tool_outputs.append({
                            "tool_name": part.tool_output.tool_name,
                            "tool_call_id": part.tool_output.tool_call_id,
                            "content": part.tool_output.content
                        })
            
            # Prepare message payload
            message_payload = {
                "role": role,
                "content": text_content,
                "assistant_name": assistant_name,
                "agent_id": agent_id,
                "tool_calls": tool_calls,
                "tool_outputs": tool_outputs
            }
            
            # Ensure text_content is never empty
            if not text_content:
                logger.warning(f"No content found for {role} message in session {session_id}. Using placeholder.")
                text_content = "[No content available]"
                message_payload["content"] = text_content
            
            # Add context to payload for user messages
            if context and role == "user":
                message_payload["channel_payload"] = context
                
            # Generate message ID
            message_id = str(uuid.uuid4())
            
            # For assistant messages, get system prompt from session metadata if not provided
            if role == "assistant" and not system_prompt:
                from src.db import get_system_prompt
                try:
                    system_prompt = get_system_prompt(uuid.UUID(session_id))
                    if system_prompt:
                        logger.debug(f"Found system prompt for assistant message: {system_prompt[:50]}...")
                        message_payload["system_prompt"] = system_prompt
                except Exception as e:
                    logger.error(f"Error retrieving system prompt: {str(e)}")
            
            # Create Message object using repository function
            from src.db import create_message, Message, get_session, update_session
            
            # Ensure tool_calls and tool_outputs are stored as dictionaries, not lists
            tool_calls_dict = {}
            for i, tc in enumerate(tool_calls):
                tool_calls_dict[str(i)] = tc
                
            tool_outputs_dict = {}
            for i, to in enumerate(tool_outputs):
                tool_outputs_dict[str(i)] = to
            
            # Log the final message content being stored
            logger.debug(f"Storing {role} message with content: {text_content[:100]}...")
            if system_prompt:
                logger.debug(f"Including system_prompt in message: {system_prompt[:50]}...")
                # Update the message_payload to include system_prompt
                message_payload["system_prompt"] = system_prompt
            
            message_obj = Message(
                id=uuid.UUID(message_id),
                session_id=uuid.UUID(session_id) if session_id else None,
                user_id=user_id,
                agent_id=agent_id,
                role=role,
                text_content=text_content,
                message_type="text",
                raw_payload=message_payload,
                tool_calls=tool_calls_dict,
                tool_outputs=tool_outputs_dict,
                context=context,
                system_prompt=system_prompt
            )
            
            create_message(message_obj)
            logger.debug(f"Created message with ID {message_id} in session {session_id}")
            
            # If this is an assistant message (response), update run_finished_at in the session
            if role == "assistant":
                session = get_session(uuid.UUID(session_id))
                if session:
                    session.run_finished_at = datetime.utcnow()
                    update_session(session)
                    logger.debug(f"Updated session {session_id} run_finished_at")
            
        except Exception as e:
            logger.error(f"❌ Error adding message to session {session_id}: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
    
    def update_system_prompt(self, session_id: str, system_prompt: str, agent_id: Optional = None, user_id: int = 1) -> None:
        """Update the system prompt for a session.
        
        Args:
            session_id: The unique session identifier.
            system_prompt: The new system prompt text.
            agent_id: Optional agent ID to associate with the message.
            user_id: Optional user ID to associate with the message.
        """
        try:
            # Ensure session exists
            session_id = self._ensure_session_exists(session_id, user_id)
            
            # Store the system prompt in the session metadata instead of creating a message
            try:
                from src.db import get_session, update_session
                
                session = get_session(uuid.UUID(session_id))
                if session:
                    # Get existing metadata or create new dictionary
                    metadata = session.metadata or {}
                    if isinstance(metadata, str):
                        try:
                            metadata = json.loads(metadata)
                        except json.JSONDecodeError:
                            metadata = {}
                    
                    # Store system prompt in metadata
                    metadata["system_prompt"] = system_prompt
                    session.metadata = metadata
                    
                    # Update session
                    update_session(session)
                    logger.debug(f"Stored system prompt in session metadata: {system_prompt[:50]}...")
                else:
                    logger.error(f"Failed to find session {session_id} to update system prompt")
            except Exception as e:
                logger.error(f"Error updating session metadata: {str(e)}")
                import traceback
                logger.error(f"Detailed error: {traceback.format_exc()}")
                
        except Exception as e:
            logger.error(f"Error updating system prompt for session {session_id}: {str(e)}")
            # Log traceback for debugging but don't crash
            import traceback
            logger.debug(f"Traceback: {traceback.format_exc()}")
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists.
        
        Args:
            session_id: The session ID to check
            
        Returns:
            True if the session exists, False otherwise
        """
        try:
            from src.db import get_session
            
            # Try to parse the session_id
            try:
                session_id_uuid = uuid.UUID(session_id) if session_id else None
            except ValueError:
                return False
            
            # Check if the session exists
            session = get_session(session_id_uuid)
            return session is not None
        except Exception as e:
            logger.error(f"Error checking session existence: {str(e)}")
            return False
    
    def _ensure_session_exists(self, session_id: str, user_id: int = 1, agent_id: Optional[int] = None, session_name: Optional[str] = None, session_origin: Optional[str] = None) -> str:
        """Ensure a session exists, creating it if necessary.
        
        Args:
            session_id: The session ID to check/create
            user_id: User ID associated with the session
            agent_id: Optional agent ID associated with the session
            session_name: Optional name for the session
            session_origin: Optional origin platform for the session
            
        Returns:
            The session ID (could be different if original was invalid)
        """
        from src.db import get_session, create_session, Session, get_agent, get_agent_by_name
        
        # If agent_id is a string name, try to look up the actual agent ID
        if agent_id is not None and not isinstance(agent_id, int) and not str(agent_id).isdigit():
            # This might be an agent name, try to find the ID
            agent_name = str(agent_id)
            agent = get_agent_by_name(agent_name)
            if agent:
                logger.debug(f"Resolved agent name '{agent_name}' to ID {agent.id}")
                agent_id = agent.id
            else:
                logger.warning(f"Could not find agent with name '{agent_name}', using as-is")
        
        # Try to get the session first
        try:
            session_id_uuid = uuid.UUID(session_id) if session_id else None
            session = get_session(session_id_uuid)
        except ValueError:
            # Invalid UUID format, we'll need to create a new session
            session = None
            logger.warning(f"Provided session ID '{session_id}' is not a valid UUID, creating a new session")
            new_session_id = create_session(Session(
                user_id=user_id,
                agent_id=agent_id,
                name=session_name,
                platform=session_origin or 'web',
                metadata={"session_origin": session_origin} if session_origin else {}
            ))
            return str(new_session_id)
        
        if not session:
            # Valid UUID but doesn't exist, create it with the specified ID
            try:
                # Prepare metadata with session_origin if provided
                metadata = {"session_origin": session_origin} if session_origin else {}
                
                # Create a new session object
                new_session = Session(
                    id=uuid.UUID(session_id),
                    user_id=user_id,
                    agent_id=agent_id,
                    name=session_name,
                    platform=session_origin or 'web',
                    metadata=metadata,
                )
                
                create_session(new_session)
                logger.info(f"Created new session with provided ID {session_id} for user {user_id}")
                return session_id
            except Exception as e:
                logger.error(f"Error creating session: {str(e)}")
                # Try to create with a new ID if there was an error
                new_session_id = create_session(Session(
                    user_id=user_id,
                    agent_id=agent_id,
                    name=session_name,
                    platform=session_origin or 'web',
                    metadata={"session_origin": session_origin} if session_origin else {}
                ))
                return str(new_session_id)
        else:
            # Session exists, check if agent_id matches (if provided)
            if agent_id is not None and session.agent_id is not None:
                # FIX: If a session already exists with an agent_id, we prefer to keep that agent_id
                # This solves the issue where CLI might first use numeric ID and then string ID
                logger.debug(f"Session already exists with agent_id {session.agent_id}, keeping it instead of {agent_id}")
                return session_id
                
                # The following code is kept commented out as reference of what we're replacing
                # Try to make sure we're comparing the same types
                # try:
                #     session_agent_id = int(session.agent_id) if str(session.agent_id).isdigit() else str(session.agent_id)
                #     new_agent_id = int(agent_id) if str(agent_id).isdigit() else str(agent_id)
                #     
                #     if session_agent_id != new_agent_id:
                #         error_msg = f"Session {session_id} is already associated with agent ID {session.agent_id}, cannot reassign to agent ID {agent_id}"
                #         logger.error(error_msg)
                #         raise ValueError(error_msg)
                # except (ValueError, TypeError):
                #     # If we can't convert to the same types, do a string comparison
                #     if str(session.agent_id) != str(agent_id):
                #         error_msg = f"Session {session_id} is already associated with agent ID {session.agent_id}, cannot reassign to agent ID {agent_id}"
                #         logger.error(error_msg)
                #         raise ValueError(error_msg)
            
            # If agent_id is provided and session doesn't have one, update it
            if agent_id is not None and session.agent_id is None:
                session.agent_id = agent_id
                session.updated_at = datetime.utcnow()
                
                # Update session
                from src.db import update_session
                update_session(session)
                logger.debug(f"Updated session {session_id} with agent ID {agent_id}")
            
            return session_id
    
    def _determine_message_role(self, message: ModelMessage) -> str:
        """Determine the role of a message.
        
        Args:
            message: The message to determine the role for.
            
        Returns:
            The role of the message (system, user, or assistant).
        """
        if any(isinstance(p, SystemPromptPart) or (hasattr(p, "part_kind") and p.part_kind == "system") for p in message.parts):
            return "system"
        elif any(isinstance(p, UserPromptPart) or (hasattr(p, "part_kind") and p.part_kind == "user") for p in message.parts):
            return "user"
        # Tool calls and outputs are now stored in dedicated columns,
        # so all assistant messages (including those with tool calls) should be "assistant"
        return "assistant"
    
    def clear_session(self, session_id: str) -> None:
        """Clear all messages from a session.
        
        Args:
            session_id: The session ID to clear messages from
        """
        try:
            from src.db import execute_query
            
            # Try to parse the session_id
            try:
                session_id_uuid = uuid.UUID(session_id) if session_id else None
            except ValueError:
                logger.error(f"Invalid session ID format: {session_id}")
                return
            
            # Delete all messages for the session
            execute_query(
                "DELETE FROM messages WHERE session_id = %s",
                (str(session_id_uuid),),
                fetch=False
            )
            logger.info(f"Cleared all messages for session {session_id}")
        except Exception as e:
            logger.error(f"Error clearing session: {str(e)}")
    
    def get_session_by_name(self, session_name: str, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Get a session ID by name.
        
        Args:
            session_name: The name of the session to retrieve
            user_id: Optional user ID to filter by
            
        Returns:
            Dictionary with id and agent_id if found, None otherwise
        """
        try:
            from src.db import get_session_by_name
            
            # Get the session from the database
            session = get_session_by_name(session_name)
            
            # If a user_id is provided, check if it matches
            if session and user_id is not None and session.user_id != user_id:
                logger.warning(f"Session with name '{session_name}' found but belongs to a different user")
                return None
            
            if session:
                # Return a dictionary with the expected format
                return {
                    "id": str(session.id),
                    "agent_id": session.agent_id
                }
            
            return None
        except Exception as e:
            logger.error(f"Error getting session by name '{session_name}': {str(e)}")
            import traceback
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return None
    
    def _db_to_model_message(self, db_message: Dict[str, Any]) -> ModelMessage:
        """Convert a database message to a ModelMessage.
        
        Args:
            db_message: The database message to convert.
            
        Returns:
            The converted ModelMessage.
        """
        try:
            # Check if db_message is None
            if db_message is None:
                logger.error("Received None db_message in _db_to_model_message")
                return ModelResponse(parts=[TextPart(content="Error: Missing message data")])
                
            role = db_message.get("role", "")
            content = db_message.get("text_content", "")
            
            # Safely parse raw_payload
            raw_payload = {}
            if db_message.get("raw_payload"):
                if isinstance(db_message["raw_payload"], str):
                    try:
                        # Handle potential Unicode issues by using utf-8 encoding/decoding
                        payload_str = db_message["raw_payload"].encode('utf-8').decode('utf-8')
                        raw_payload = json.loads(payload_str)
                    except json.JSONDecodeError as e:
                        logger.error(f"Error parsing raw_payload JSON: {db_message['raw_payload']} - Error: {str(e)}")
                        raw_payload = {}
                elif isinstance(db_message["raw_payload"], dict):
                    # It's already a dict, no need to parse
                    raw_payload = db_message["raw_payload"]
                else:
                    logger.error(f"Unexpected raw_payload type: {type(db_message['raw_payload'])}")
                    raw_payload = {}
            
            # Parse tool_calls from dedicated column if available
            tool_calls = []
            if db_message.get("tool_calls"):
                if isinstance(db_message["tool_calls"], str):
                    try:
                        # Handle potential Unicode issues by using utf-8 encoding/decoding
                        tool_calls_str = db_message["tool_calls"].encode('utf-8').decode('utf-8')
                        tool_calls_dict = json.loads(tool_calls_str)
                        # Convert from dict to list if needed
                        if isinstance(tool_calls_dict, dict):
                            tool_calls = list(tool_calls_dict.values())
                        else:
                            tool_calls = tool_calls_dict
                    except json.JSONDecodeError as e:
                        logger.error(f"Error parsing tool_calls JSON: {db_message['tool_calls']} - Error: {str(e)}")
                elif isinstance(db_message["tool_calls"], dict):
                    # Convert from dict to list
                    tool_calls = list(db_message["tool_calls"].values())
                else:
                    tool_calls = db_message["tool_calls"]
            
            # Parse tool_outputs from dedicated column if available
            tool_outputs = []
            if db_message.get("tool_outputs"):
                if isinstance(db_message["tool_outputs"], str):
                    try:
                        # Handle potential Unicode issues by using utf-8 encoding/decoding
                        tool_outputs_str = db_message["tool_outputs"].encode('utf-8').decode('utf-8')
                        tool_outputs_dict = json.loads(tool_outputs_str)
                        # Convert from dict to list if needed
                        if isinstance(tool_outputs_dict, dict):
                            tool_outputs = list(tool_outputs_dict.values())
                        else:
                            tool_outputs = tool_outputs_dict
                    except json.JSONDecodeError as e:
                        logger.error(f"Error parsing tool_outputs JSON: {db_message['tool_outputs']} - Error: {str(e)}")
                elif isinstance(db_message["tool_outputs"], dict):
                    # Convert from dict to list
                    tool_outputs = list(db_message["tool_outputs"].values())
                else:
                    tool_outputs = db_message["tool_outputs"]
            
            # Use tool data from dedicated columns if available, otherwise try to get from raw_payload
            if not tool_calls and "tool_calls" in raw_payload and raw_payload["tool_calls"]:
                tool_calls = raw_payload["tool_calls"]
            
            if not tool_outputs and "tool_outputs" in raw_payload and raw_payload["tool_outputs"]:
                tool_outputs = raw_payload["tool_outputs"]
            
            # Create appropriate message type based on role
            if role == "user":
                message = ModelRequest(parts=[
                    UserPromptPart(content=content)
                ])
            elif role == "system":
                message = ModelRequest(parts=[
                    SystemPromptPart(content=content)
                ])
            else:  # Assistant message
                # Create a text part for the main content
                parts = [TextPart(content=content)]
                
                # Create tool call parts
                for tc in tool_calls:
                    try:
                        if isinstance(tc, dict) and "tool_name" in tc:
                            tool_call = ToolCall(
                                tool_name=tc.get("tool_name", ""),
                                args=tc.get("args", {}),
                                tool_call_id=tc.get("tool_call_id", "")
                            )
                            parts.append(ToolCallPart(tool_call=tool_call))
                    except Exception as e:
                        logger.error(f"Error creating tool call part: {str(e)}")
                
                # Create tool output parts
                for to in tool_outputs:
                    try:
                        if isinstance(to, dict) and "tool_name" in to:
                            tool_output = ToolOutput(
                                tool_name=to.get("tool_name", ""),
                                tool_call_id=to.get("tool_call_id", ""),
                                content=to.get("content", "")
                            )
                            parts.append(ToolOutputPart(tool_output=tool_output))
                    except Exception as e:
                        logger.error(f"Error creating tool output part: {str(e)}")
                
                # Create the response message with all parts
                message = ModelResponse(parts=parts)
                
                # Add system_prompt from the database if available
                if db_message.get("system_prompt"):
                    message.system_prompt = db_message["system_prompt"]
            
            # Add agent_id and user_id if available
            if db_message.get("agent_id") is not None:
                message.agent_id = db_message["agent_id"]
                
            if db_message.get("user_id") is not None:
                message.user_id = db_message["user_id"]
            
            return message
        except Exception as e:
            logger.error(f"Error converting database message to ModelMessage: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
            # Fallback to a simple error message
            return ModelResponse(parts=[TextPart(content=f"Error processing message: {str(e)}")])