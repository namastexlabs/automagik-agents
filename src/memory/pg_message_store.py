"""PostgreSQL implementation of MessageStore."""

import json
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    UserPromptPart,
    TextPart
)

from src.memory.message_store import MessageStore
from src.utils.db import execute_query, execute_batch
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
            from src.utils.db import get_connection_pool
            pool = get_connection_pool()
            with pool.getconn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version()")
                    version = cur.fetchone()[0]
                    logger.info(f"✅ PostgresMessageStore successfully connected to database: {version}")
                pool.putconn(conn)
        except Exception as e:
            logger.error(f"❌ PostgresMessageStore failed to connect to database during initialization: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
    
    def get_messages(self, session_id: str) -> List[ModelMessage]:
        """Retrieve all messages for a session from PostgreSQL.
        
        Args:
            session_id: The unique session identifier.
            
        Returns:
            List of messages in the session.
        """
        try:
            # Check if session exists
            if not self.session_exists(session_id):
                logger.debug(f"Session {session_id} does not exist, returning empty list")
                return []
            
            # Get messages from database
            logger.info(f"🔍 Retrieving messages for session {session_id}")
            messages = execute_query(
                """
                SELECT 
                    id, role, text_content, raw_payload, 
                    message_timestamp, agent_id
                FROM 
                    chat_messages 
                WHERE 
                    session_id = %s
                ORDER BY 
                    message_timestamp
                """,
                (session_id,)
            )
            
            # Log the result
            if messages:
                logger.info(f"✅ Retrieved {len(messages)} messages for session {session_id}")
            else:
                logger.warning(f"⚠️ No messages found for session {session_id}")
            
            # Ensure messages is not None
            if messages is None:
                logger.warning(f"Retrieved None instead of messages list for session {session_id}")
                return []
            
            # Convert to ModelMessage objects
            try:
                return [self._db_to_model_message(msg) for msg in messages]
            except Exception as e:
                logger.error(f"Error converting messages for session {session_id}: {str(e)}")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving messages for session {session_id}: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
            return []
    
    def add_message(self, session_id: str, message: ModelMessage) -> None:
        """Add a message to a session in PostgreSQL.
        
        Args:
            session_id: The unique session identifier.
            message: The message to add.
        """
        # Default to user_id="1" to match our database schema
        user_id = "1"  # Default user ID
        
        try:
            logger.info(f"🔍 Adding message for session {session_id} and user {user_id}")
            
            # Make sure the session exists
            logger.info(f"▶️ Ensuring session {session_id} exists before adding message")
            session_id = self._ensure_session_exists(session_id, user_id)
            logger.info(f"✅ Session {session_id} confirmed for message insertion")
            
            # Extract message data
            role = self._determine_message_role(message)
            text_content = message.parts[0].content if message.parts else ""
            
            # Log the message being added
            logger.info(f"🔍 Adding {role} message to session {session_id}: {text_content[:50]}...")
            
            # Extract assistant name if present
            assistant_name = None
            if role == "assistant" and isinstance(message.parts[0], TextPart) and hasattr(message.parts[0], "assistant_name"):
                assistant_name = message.parts[0].assistant_name
            
            # Extract agent ID if present
            agent_id = getattr(message, "agent_id", None)
            
            # Extract tool calls and outputs
            tool_calls = []
            tool_outputs = []
            
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
            
            # Prepare JSON payload with UTF-8 handling
            message_payload = {
                "role": role,
                "content": text_content,
                "assistant_name": assistant_name,
                "agent_id": agent_id,
                "tool_calls": tool_calls,
                "tool_outputs": tool_outputs
            }
            
            # Handle JSON serialization
            try:
                message_payload_json = json.dumps(message_payload, ensure_ascii=False)
                message_payload_json = message_payload_json.encode('utf-8').decode('utf-8')
            except Exception as e:
                logger.error(f"Error serializing message payload: {str(e)}")
                message_payload_json = json.dumps({"content": text_content, "role": role})
            
            # Generate a unique message ID
            message_id = f"m_{uuid.uuid4()}"
            
            # Insert the message
            logger.info(f"▶️ Inserting message {message_id} into database for session {session_id}")
            try:
                execute_query(
                    """
                    INSERT INTO chat_messages (
                        id, session_id, role, text_content, raw_payload, 
                        message_timestamp, message_type, user_id, agent_id,
                        tool_calls, tool_outputs
                    ) VALUES (
                        %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s,
                        %s, %s
                    )
                    """,
                    (
                        message_id,
                        session_id,
                        role,
                        text_content,
                        message_payload_json,
                        datetime.utcnow(),
                        "text",
                        user_id,
                        agent_id,
                        json.dumps(tool_calls) if tool_calls else None,
                        json.dumps(tool_outputs) if tool_outputs else None
                    ),
                    fetch=False
                )
                logger.info(f"✅ Successfully added {role} message to session {session_id}")
                
                # Now verify the message was actually inserted
                verification = execute_query(
                    "SELECT COUNT(*) as count FROM chat_messages WHERE id = %s",
                    (message_id,)
                )
                if verification and verification[0]["count"] > 0:
                    logger.info(f"✅ Verified message {message_id} exists in database")
                else:
                    logger.warning(f"⚠️ Message {message_id} not found in database after insertion")
                
            except Exception as db_error:
                logger.error(f"❌ Database error adding message: {str(db_error)}")
                import traceback
                logger.error(f"Detailed error: {traceback.format_exc()}")
                
        except Exception as e:
            logger.error(f"❌ Error adding message to session {session_id}: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
    
    def update_system_prompt(self, session_id: str, system_prompt: str) -> None:
        """Update the system prompt for a session in PostgreSQL.
        
        Args:
            session_id: The unique session identifier.
            system_prompt: The system prompt content.
        """
        # Default values
        user_id = "1"  # Default user ID
        agent_id = None  # Default agent ID
        
        try:
            # Make sure the session exists
            session_id = self._ensure_session_exists(session_id, user_id)
            
            # Prepare system payload with UTF-8 handling
            system_payload = {"content": system_prompt, "role": "system"}
            system_payload_json = json.dumps(system_payload, ensure_ascii=False)
            system_payload_json = system_payload_json.encode('utf-8').decode('utf-8')
            
            # First check if system prompt exists
            existing = execute_query(
                """
                SELECT id FROM chat_messages 
                WHERE session_id = %s AND role = 'system'
                LIMIT 1
                """,
                (session_id,)
            )
            
            if existing:
                # Update existing system prompt
                execute_query(
                    """
                    UPDATE chat_messages 
                    SET text_content = %s, raw_payload = %s, updated_at = %s, agent_id = %s
                    WHERE id = %s
                    """,
                    (
                        system_prompt, 
                        system_payload_json,
                        datetime.utcnow(),
                        agent_id,
                        existing[0]["id"]
                    ),
                    fetch=False
                )
                logger.debug(f"Updated system prompt for session {session_id} with agent_id {agent_id}")
            else:
                # Add new system prompt with NULL id to trigger auto-generation
                result = execute_query(
                    """
                    INSERT INTO chat_messages (
                        session_id, role, text_content, raw_payload, 
                        message_timestamp, message_type, user_id, agent_id
                    ) VALUES (
                        %s, %s, %s, %s, 
                        %s, %s, %s, %s
                    )
                    RETURNING id
                    """,
                    (
                        session_id, 
                        "system", 
                        system_prompt, 
                        system_payload_json,
                        datetime.utcnow(),
                        "text",
                        user_id,
                        agent_id
                    )
                )
                
                # Get the auto-generated message ID
                message_id = result[0]["id"] if result else None
                logger.debug(f"Added system prompt {message_id} to session {session_id} for user {user_id} with agent_id {agent_id}")
        except Exception as e:
            logger.error(f"Error updating system prompt for session {session_id}: {str(e)}")
            # Log traceback for debugging but don't crash
            import traceback
            logger.debug(f"Traceback: {traceback.format_exc()}")
            # Don't re-raise the exception to allow the application to continue
    
    def clear_session(self, session_id: str) -> None:
        """Clear all messages in a session from PostgreSQL.
        
        Args:
            session_id: The unique session identifier.
        """
        try:
            # Delete all messages for the session
            execute_query(
                "DELETE FROM chat_messages WHERE session_id = %s",
                (session_id,),
                fetch=False
            )
            logger.debug(f"Cleared messages for session {session_id}")
        except Exception as e:
            logger.error(f"Error clearing session {session_id}: {str(e)}")
            # Log traceback for debugging but don't crash
            import traceback
            logger.debug(f"Traceback: {traceback.format_exc()}")
            # Don't re-raise the exception to allow the application to continue
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists in the database.
        
        Args:
            session_id: The session ID to check.
            
        Returns:
            bool: True if the session exists, False otherwise.
        """
        try:
            if not session_id:
                return False
                
            result = execute_query(
                "SELECT COUNT(*) as count FROM sessions WHERE id = %s",
                (session_id,)
            )
            return result[0]["count"] > 0
        except Exception as e:
            logger.error(f"Error checking session {session_id}: {str(e)}")
            return False
    
    def _ensure_session_exists(self, session_id: str, user_id: str) -> str:
        """
        Ensures a session exists, creating it if necessary.
        Also ensures the user exists, creating it if necessary.
        
        Args:
            session_id: The ID of the session
            user_id: The ID of the user associated with the session
            
        Returns:
            str: The session ID (which may be auto-generated if not provided)
        """
        try:
            # First ensure user exists
            logger.info(f"▶️ Ensuring user {user_id} exists before checking session")
            self._ensure_user_exists(user_id)
            
            # Then check if session already exists
            if session_id and self.session_exists(session_id):
                logger.info(f"✅ Session {session_id} already exists")
                return session_id
            
            # Log session creation
            if session_id:
                logger.info(f"▶️ Creating new session with ID: {session_id}")
            else:
                logger.info(f"▶️ Creating new session with auto-generated ID")
                
            # If session_id is empty, generate a new one
            if not session_id:
                # Generate a new session using the database default
                try:
                    logger.info("▶️ Executing INSERT INTO sessions with auto-generated ID")
                    result = execute_query(
                        """
                        INSERT INTO sessions (user_id, platform, created_at, updated_at) 
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """,
                        (user_id, "web", datetime.utcnow(), datetime.utcnow())
                    )
                    
                    if result and len(result) > 0:
                        new_session_id = result[0]["id"]
                        logger.info(f"✅ Created new session with auto-generated ID {new_session_id}")
                        return new_session_id
                    else:
                        logger.error(f"❌ Failed to get ID for newly created session")
                        return str(uuid.uuid4())  # Fallback to UUID
                except Exception as e:
                    logger.error(f"❌ Error creating session: {str(e)}")
                    import traceback
                    logger.error(f"Detailed error: {traceback.format_exc()}")
                    # Return a UUID as fallback
                    fallback_id = str(uuid.uuid4())
                    logger.warning(f"⚠️ Using fallback session ID: {fallback_id}")
                    return fallback_id
            else:
                # Use the provided session ID as-is without any validation or transformation
                try:
                    logger.info(f"▶️ Executing INSERT INTO sessions with provided ID: {session_id}")
                    execute_query(
                        """
                        INSERT INTO sessions (id, user_id, platform, created_at, updated_at) 
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (session_id, user_id, "web", datetime.utcnow(), datetime.utcnow()),
                        fetch=False
                    )
                    logger.info(f"✅ Created new session {session_id} for user {user_id}")
                except Exception as e:
                    # If we get an error (like a duplicate key), check if it's because the session already exists
                    if "duplicate key" in str(e):
                        logger.debug(f"⚠️ Session {session_id} already exists (caught duplicate key)")
                        return session_id
                    # Otherwise log the error but return the session_id anyway
                    logger.error(f"❌ Error creating session with ID {session_id}: {str(e)}")
                    import traceback
                    logger.error(f"Detailed error: {traceback.format_exc()}")
            
            # Verify the session was created
            logger.info(f"▶️ Verifying session {session_id} was created")
            session_exists = self.session_exists(session_id)
            if session_exists:
                logger.info(f"✅ Verified session {session_id} exists in database")
            else:
                logger.warning(f"⚠️ Session {session_id} not found in database after creation")
            
            return session_id
        except Exception as e:
            logger.error(f"❌ Error ensuring session {session_id}: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
            # Return the session_id even if there was an error
            return session_id or str(uuid.uuid4())
    
    def _ensure_user_exists(self, user_id: str) -> None:
        """
        Ensures a user exists in the database, creating it if necessary.
        
        Args:
            user_id: The ID of the user to check/create
            
        Returns:
            None
        """
        try:
            # Convert string user_id to integer for database compatibility
            numeric_user_id = 1  # Default user ID
            
            # Convert user_id to integer if possible
            try:
                numeric_user_id = int(user_id)
            except ValueError:
                logger.warning(f"⚠️ Non-numeric user_id '{user_id}' provided, using default ID 1 instead")
            
            # Check if user exists
            logger.info(f"▶️ Checking if user {numeric_user_id} exists in database")
            user_exists = execute_query(
                "SELECT COUNT(*) as count FROM users WHERE id = %s",
                (numeric_user_id,)
            )
            
            # If user exists, return
            if user_exists and user_exists[0]["count"] > 0:
                logger.info(f"✅ User {numeric_user_id} already exists in database")
                return
            
            # Log that we're creating a new user
            logger.info(f"▶️ User {numeric_user_id} not found in database, creating now")
            
            # Create user if not exists
            try:
                execute_query(
                    """
                    INSERT INTO users (id, email, created_at, updated_at, user_data) 
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        numeric_user_id,
                        f"user{numeric_user_id}@example.com",  # Default email based on user_id
                        datetime.utcnow(), 
                        datetime.utcnow(),
                        json.dumps({"name": f"User {numeric_user_id}"})
                    ),
                    fetch=False
                )
                logger.info(f"✅ Created user {numeric_user_id} successfully")
            except Exception as inner_e:
                logger.error(f"❌ Failed to create user {numeric_user_id}: {str(inner_e)}")
                import traceback
                logger.error(f"Detailed error: {traceback.format_exc()}")
                # If it's a duplicate key error, the user must have been created in a parallel request
                if "duplicate key" in str(inner_e):
                    logger.debug(f"⚠️ User {numeric_user_id} already exists (caught duplicate key)")
                    return
                # For other errors, re-raise to be handled by the outer try-except
                raise
        except Exception as e:
            logger.error(f"❌ Error ensuring user {user_id} exists: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
            # Don't re-raise the exception to allow session creation to still proceed
    
    def _determine_message_role(self, message: ModelMessage) -> str:
        """Determine the role of a message.
        
        Args:
            message: The message to determine the role for.
            
        Returns:
            The role of the message (system, user, or assistant).
        """
        if any(isinstance(p, SystemPromptPart) for p in message.parts):
            return "system"
        elif any(isinstance(p, UserPromptPart) for p in message.parts):
            return "user"
        # Tool calls and outputs are now stored in dedicated columns,
        # so all assistant messages (including those with tool calls) should be "assistant"
        return "assistant"
    
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
                        tool_calls = json.loads(tool_calls_str)
                    except json.JSONDecodeError as e:
                        logger.error(f"Error parsing tool_calls JSON: {db_message['tool_calls']} - Error: {str(e)}")
                else:
                    tool_calls = db_message["tool_calls"]
            
            # Parse tool_outputs from dedicated column if available
            tool_outputs = []
            if db_message.get("tool_outputs"):
                if isinstance(db_message["tool_outputs"], str):
                    try:
                        # Handle potential Unicode issues by using utf-8 encoding/decoding
                        tool_outputs_str = db_message["tool_outputs"].encode('utf-8').decode('utf-8')
                        tool_outputs = json.loads(tool_outputs_str)
                    except json.JSONDecodeError as e:
                        logger.error(f"Error parsing tool_outputs JSON: {db_message['tool_outputs']} - Error: {str(e)}")
                else:
                    tool_outputs = db_message["tool_outputs"]
            
            # Use tool data from dedicated columns if available, otherwise try to get from raw_payload
            if not tool_calls and "tool_calls" in raw_payload and raw_payload["tool_calls"]:
                tool_calls = raw_payload["tool_calls"]
            
            if not tool_outputs and "tool_outputs" in raw_payload and raw_payload["tool_outputs"]:
                tool_outputs = raw_payload["tool_outputs"]
            
            # Ensure all collections are valid before accessing
            if tool_calls is None:
                tool_calls = []
            if tool_outputs is None:
                tool_outputs = []
            
            if role == "system":
                return ModelRequest(parts=[SystemPromptPart(content=content)])
            elif role == "user":
                return ModelRequest(parts=[UserPromptPart(content=content)])
            else:  # assistant
                # Create text part
                text_part = TextPart(content=content)
                
                # Get assistant name if available
                assistant_name = raw_payload.get("assistant_name")
                if assistant_name:
                    text_part.assistant_name = assistant_name
                
                parts = [text_part]
                
                # Add tool calls if available
                for tc in tool_calls:
                    if tc and isinstance(tc, dict) and tc.get("tool_name"):
                        try:
                            tool_call = ToolCall(
                                tool_name=tc.get("tool_name"),
                                args=tc.get("args", {}),
                                tool_call_id=tc.get("tool_call_id", "")
                            )
                            parts.append(ToolCallPart(tool_call=tool_call))
                        except Exception as e:
                            logger.error(f"Error creating ToolCallPart: {str(e)}")
                
                # Add tool outputs if available
                for to in tool_outputs:
                    if to and isinstance(to, dict) and to.get("tool_name"):
                        try:
                            tool_output = ToolOutput(
                                tool_name=to.get("tool_name"),
                                content=to.get("content", ""),
                                tool_call_id=to.get("tool_call_id", "")
                            )
                            parts.append(ToolOutputPart(tool_output=tool_output))
                        except Exception as e:
                            logger.error(f"Error creating ToolOutputPart: {str(e)}")
                
                # Create message with all parts
                message = ModelResponse(parts=parts)
                
                # Add agent ID if available
                if db_message.get("agent_id"):
                    message.agent_id = db_message["agent_id"]
                
                return message
        except Exception as e:
            logger.error(f"Error converting database message to ModelMessage: {str(e)}")
            # Return a simple text message as fallback
            return ModelResponse(parts=[TextPart(content="Error retrieving message")])
    
    def get_all_sessions(self, page: int = 1, page_size: int = 50, sort_desc: bool = True):
        """Get all sessions from the database with pagination.
        
        Args:
            page: Page number (1-based)
            page_size: Number of sessions per page
            sort_desc: Sort by most recent first if True
            
        Returns:
            Dictionary with sessions, total count, and pagination info
        """
        try:
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Order by clause
            order_by = "created_at DESC" if sort_desc else "created_at ASC"
            
            # Get total count
            total_count_result = execute_query(
                """
                SELECT COUNT(*) as count FROM sessions
                """,
                ()
            )
            total_count = total_count_result[0]['count'] if total_count_result else 0
            
            # Calculate total pages
            total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 1
            
            # Get sessions with pagination
            sessions_query = execute_query(
                f"""
                SELECT 
                    s.id as session_id, 
                    s.user_id, 
                    s.created_at,
                    s.platform,
                    (SELECT COUNT(*) FROM chat_messages cm WHERE cm.session_id = s.id) as message_count,
                    (SELECT MAX(message_timestamp) FROM chat_messages cm WHERE cm.session_id = s.id) as last_updated,
                    (SELECT a.name FROM agents a 
                     JOIN chat_messages cm ON a.id = cm.agent_id 
                     WHERE cm.session_id = s.id 
                     LIMIT 1) as agent_name
                FROM 
                    sessions s
                ORDER BY 
                    {order_by}
                LIMIT 
                    %s OFFSET %s
                """,
                (page_size, offset)
            )
            
            # Format sessions
            sessions = []
            for session in sessions_query:
                # Execute_query returns each row as a dict with column names as keys
                session_info = {
                    "session_id": session['session_id'],
                    "user_id": session['user_id'],
                    "created_at": session['created_at'],
                    "last_updated": session['last_updated'],
                    "message_count": int(session['message_count']) if session['message_count'] is not None else 0,
                    "agent_name": session['agent_name']
                }
                sessions.append(session_info)
            
            logger.info(f"✅ Retrieved {len(sessions)} sessions (page {page}/{total_pages})")
            
            return {
                "sessions": sessions,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
        except Exception as e:
            logger.error(f"Error retrieving all sessions: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
            return {
                "sessions": [],
                "total_count": 0,
                "page": page,
                "page_size": page_size,
                "total_pages": 0
            } 