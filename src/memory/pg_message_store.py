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
from src.db import (
    get_session, get_session_by_name, create_session, update_session, 
    Session, create_message, get_message, list_messages, Message,
    delete_session_messages
)

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
    
    def get_messages(self, session_id: str, sort_desc: bool = True) -> List[Dict[str, Any]]:
        """Get all messages for a session.
        
        Args:
            session_id: The session ID to get messages for
            sort_desc: Sort by created_at in descending order if True
            
        Returns:
            List of message dictionaries
        """
        try:
            # Convert session_id to UUID if it's a string
            if isinstance(session_id, str):
                session_id_uuid = uuid.UUID(session_id)
            else:
                session_id_uuid = session_id
                
            # Use repository function to list messages
            messages = list_messages(session_id_uuid, sort_desc=sort_desc)
            
            # Convert each message to a dictionary
            message_dicts = []
            for message in messages:
                message_id = str(message.id)
                # Use the get_message method to format the message
                message_dict = self.get_message(message_id)
                if message_dict:
                    message_dicts.append(message_dict)
            
            return message_dicts
        except Exception as e:
            logger.error(f"Error retrieving messages for session {session_id}: {str(e)}")
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
            # Convert session_id to UUID if it's a string
            if isinstance(session_id, str):
                session_id_uuid = uuid.UUID(session_id)
            else:
                session_id_uuid = session_id
                
            # Use repository function to get the session
            session = get_session(session_id_uuid)
            
            return session is not None
        except Exception as e:
            logger.error(f"Error checking if session {session_id} exists: {str(e)}")
            return False
    
    def _ensure_session_exists(self, session_id: str, user_id: Optional[int] = None, agent_id: Optional[int] = None,
                              session_name: Optional[str] = None, session_origin: Optional[str] = None) -> bool:
        """Ensure a session exists with the given ID, creating it if necessary.
        
        If the session exists and has an agent_id, but a different one is provided, raises ValueError.
        
        Args:
            session_id: The session ID to check/create
            user_id: The user ID to associate with the session
            agent_id: The agent ID to associate with the session
            session_name: Optional session name
            session_origin: Optional session origin platform
            
        Returns:
            True if the session exists or was created, False on error
            
        Raises:
            ValueError: If the session exists but with a different agent_id
        """
        try:
            # Convert session_id to UUID if it's a string
            if isinstance(session_id, str):
                session_id_uuid = uuid.UUID(session_id)
            else:
                session_id_uuid = session_id
                
            # Check if session exists
            existing_session = get_session(session_id_uuid)
            
            if existing_session:
                # Session exists
                logger.debug(f"Session {session_id} already exists")
                
                # Check if agent_id matches if both are provided
                if agent_id is not None and existing_session.agent_id is not None and existing_session.agent_id != agent_id:
                    # Different agent - this is usually not allowed
                    logger.error(f"Session {session_id} is already associated with agent ID {existing_session.agent_id}, "
                               f"cannot use with agent ID {agent_id}")
                    raise ValueError(f"Session {session_id} is already associated with agent ID {existing_session.agent_id}")
                
                # Update the session with new data if provided
                should_update = False
                if agent_id is not None and existing_session.agent_id is None:
                    existing_session.agent_id = agent_id
                    should_update = True
                    
                if user_id is not None and existing_session.user_id is None:
                    existing_session.user_id = user_id
                    should_update = True
                    
                if session_name is not None and not existing_session.name:
                    existing_session.name = session_name
                    should_update = True
                
                if session_origin is not None:
                    # Handle metadata for origin
                    metadata = existing_session.metadata or {}
                    if isinstance(metadata, str):
                        try:
                            metadata = json.loads(metadata)
                        except:
                            metadata = {}
                    
                    # Set the session_origin
                    metadata['session_origin'] = session_origin
                    existing_session.metadata = metadata
                    should_update = True
                
                # Update the session if needed
                if should_update:
                    logger.debug(f"Updating session {session_id} with new data")
                    update_session(existing_session)
                
                return True
            else:
                # Session doesn't exist, create it
                logger.debug(f"Creating new session with ID {session_id}")
                
                # Prepare metadata
                metadata = {}
                if session_origin:
                    metadata['session_origin'] = session_origin
                
                # Create a new Session object
                new_session = Session(
                    id=session_id_uuid,
                    user_id=user_id,
                    agent_id=agent_id,
                    name=session_name,
                    platform=session_origin or 'api',
                    metadata=metadata,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                # Create the session using repository function
                created_id = create_session(new_session)
                
                if created_id:
                    logger.info(f"Created new session with ID {session_id}")
                    return True
                else:
                    logger.error(f"Failed to create session {session_id}")
                    return False
        except Exception as e:
            logger.error(f"Error ensuring session exists: {str(e)}")
            return False
    
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
        """Clear all messages for a session.
        
        Args:
            session_id: The session ID to clear messages for
        """
        try:
            # Convert session_id to UUID if it's a string
            try:
                session_id_uuid = uuid.UUID(session_id) if session_id else None
            except ValueError:
                logger.error(f"Invalid session ID format: {session_id}")
                return
            
            # Delete all messages for the session using repository function
            delete_session_messages(session_id_uuid)
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
                
            # Return a dictionary with the session information
            if session:
                return {
                    "id": str(session.id),
                    "agent_id": session.agent_id,
                    "user_id": session.user_id,
                    "name": session.name,
                    "platform": session.platform,
                    "created_at": session.created_at,
                    "updated_at": session.updated_at
                }
                
            return None
        except Exception as e:
            logger.error(f"Error retrieving session by name '{session_name}': {str(e)}")
            return None
    
    def get_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific message by ID.
        
        Args:
            message_id: The message ID to retrieve
            
        Returns:
            Message data if found, None otherwise
        """
        try:
            # Convert to UUID if needed
            if isinstance(message_id, str):
                message_id_uuid = uuid.UUID(message_id)
            else:
                message_id_uuid = message_id
                
            # Use repository function to get the message
            message = get_message(message_id_uuid)
            
            if not message:
                return None
                
            # Convert the message to a dictionary
            if hasattr(message, 'model_dump'):
                # Pydantic v2
                db_message = message.model_dump()
            elif hasattr(message, 'dict'):
                # Pydantic v1
                db_message = message.dict()
            else:
                # Handle other types of objects
                db_message = {attr: getattr(message, attr) for attr in dir(message) 
                             if not attr.startswith('_') and not callable(getattr(message, attr))}
            
            # Ensure ID is a string
            db_message["id"] = str(db_message["id"])
            if db_message.get("session_id"):
                db_message["session_id"] = str(db_message["session_id"])
            
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
                    
            # Get the raw_payload data
            raw_payload = db_message.get("raw_payload", {})
            if isinstance(raw_payload, str):
                try:
                    raw_payload = json.loads(raw_payload)
                except json.JSONDecodeError:
                    raw_payload = {}
            
            # Get context data
            context = db_message.get("context", {})
            if isinstance(context, str):
                try:
                    context = json.loads(context)
                except json.JSONDecodeError:
                    context = {}
            
            # Get system_prompt if available
            system_prompt = db_message.get("system_prompt")
            if not system_prompt and raw_payload and isinstance(raw_payload, dict):
                system_prompt = raw_payload.get("system_prompt")
            
            # Build the message dictionary with all the data
            message_dict = {
                "id": db_message["id"],
                "session_id": db_message.get("session_id"),
                "role": db_message.get("role"),
                "content": db_message.get("text_content"),
                "tool_calls": tool_calls,
                "tool_outputs": tool_outputs,
                "created_at": db_message.get("created_at"),
                "user_id": db_message.get("user_id"),
                "agent_id": db_message.get("agent_id"),
                "raw_payload": raw_payload,
                "context": context,
                "system_prompt": system_prompt
            }
            
            return message_dict
        except Exception as e:
            logger.error(f"Error retrieving message {message_id}: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None