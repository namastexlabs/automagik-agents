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
    
    def get_messages(self, session_id: str, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Retrieve messages for a session with pagination.
        
        Args:
            session_id: The unique session identifier.
            limit: Maximum number of messages to retrieve (default: 100).
            offset: Number of messages to skip (default: 0).
            
        Returns:
            A list of message dictionaries.
        """
        try:
            # Try to use the session_messages view if it exists
            try:
                result = execute_query(
                    """
                    SELECT *
                    FROM session_messages 
                    WHERE session_id = %s::uuid 
                    LIMIT %s OFFSET %s
                    """,
                    (session_id, limit, offset)
                )
            except Exception as view_error:
                # Fall back to direct query if view doesn't exist
                logger.debug(f"Could not use session_messages view, falling back to direct query: {str(view_error)}")
                result = execute_query(
                    """
                    SELECT 
                        id, 
                        session_id, 
                        role, 
                        text_content, 
                        tool_calls, 
                        tool_outputs, 
                        raw_payload, 
                        created_at,
                        updated_at, 
                        message_type,
                        user_id,
                        agent_id,
                        context,
                        system_prompt
                    FROM messages 
                    WHERE session_id = %s::uuid 
                    ORDER BY created_at ASC, updated_at ASC
                    LIMIT %s OFFSET %s
                    """,
                    (session_id, limit, offset)
                )
            
            if not result:
                logger.debug(f"No messages found for session {session_id}")
                return []
            
            # Convert the database results to ModelMessage objects
            messages = []
            for db_msg in result:
                # Convert database message to ModelMessage
                model_message = self._db_to_model_message(db_msg)
                messages.append(model_message)
            
            logger.debug(f"Retrieved {len(messages)} messages for session {session_id}")
            return messages
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
        # Get user_id from message if available, otherwise default to 1
        user_id = getattr(message, "user_id", 1)
        
        try:
            # Make sure the session exists
            session_id = self._ensure_session_exists(session_id, user_id)
            
            # Determine message role
            role = self._determine_message_role(message)
            
            # Extract text content from message parts
            text_content = ""
            assistant_name = None
            agent_id = getattr(message, "agent_id", None)
            
            # Extract context from user messages
            context = getattr(message, "context", None)
            
            # Extract system_prompt from assistant messages
            system_prompt = getattr(message, "system_prompt", None)
            
            # Extract tool calls and outputs
            tool_calls = []
            tool_outputs = []
            
            # Extract text content and other data from message parts
            for part in message.parts:
                if hasattr(part, "content"):
                    text_content = part.content
                    if hasattr(part, "assistant_name") and part.assistant_name:
                        assistant_name = part.assistant_name
                
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
            
            # Add context to payload for user messages
            if context and role == "user":
                message_payload["channel_payload"] = context
                
            # Add system_prompt to payload for assistant messages
            if system_prompt and role == "assistant":
                message_payload["system_prompt"] = system_prompt
            
            # Handle JSON serialization
            try:
                message_payload_json = json.dumps(message_payload, ensure_ascii=False)
                message_payload_json = message_payload_json.encode('utf-8').decode('utf-8')
            except Exception as e:
                logger.error(f"Error serializing message payload: {str(e)}")
                message_payload_json = json.dumps({"content": text_content, "role": role})
            
            # Generate a unique UUID for the message
            message_id = str(uuid.uuid4())
            
            # Serialize tool calls and outputs for dedicated columns
            tool_calls_json = None
            if tool_calls:
                try:
                    tool_calls_json = json.dumps(tool_calls, ensure_ascii=False)
                except Exception as e:
                    logger.error(f"Error serializing tool calls: {str(e)}")
            
            tool_outputs_json = None
            if tool_outputs:
                try:
                    tool_outputs_json = json.dumps(tool_outputs, ensure_ascii=False)
                except Exception as e:
                    logger.error(f"Error serializing tool outputs: {str(e)}")
            
            # Prepare context column data
            context_json = None
            if context and role == "user":
                try:
                    context_json = json.dumps(context, ensure_ascii=False)
                except Exception as e:
                    logger.error(f"Error serializing channel_payload: {str(e)}")
            
            # Set a precise timestamp for this message
            current_time = datetime.utcnow()
            
            # Insert the message into the database - use RETURNING to get the inserted record
            result = execute_query(
                """
                INSERT INTO messages (
                    id, session_id, role, text_content, raw_payload, 
                    message_type, user_id, agent_id,
                    tool_calls, tool_outputs, context, system_prompt,
                    created_at, updated_at
                ) VALUES (
                    %s, %s::uuid, %s, %s, %s, 
                    %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s
                )
                RETURNING id
                """,
                (
                    message_id, 
                    session_id, 
                    role, 
                    text_content, 
                    message_payload_json,
                    "text",
                    user_id,
                    agent_id,
                    tool_calls_json,
                    tool_outputs_json,
                    context_json,
                    system_prompt,
                    current_time,  # created_at
                    current_time   # updated_at
                )
            )
            
            inserted_id = result[0]["id"] if result else None
            logger.debug(f"Added message {inserted_id} to session {session_id} with role {role}")
            
            # If this is an assistant message (response), update run_finished_at in the session
            if role == "assistant":
                execute_query(
                    """
                    UPDATE sessions 
                    SET updated_at = %s, run_finished_at = %s
                    WHERE id = %s::uuid
                    """,
                    (current_time, current_time, session_id),
                    fetch=False
                )
                logger.debug(f"Updated session {session_id} run_finished_at to {current_time}")
            
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
            
            # Check if there's an existing system prompt
            existing_system = execute_query(
                """
                SELECT id 
                FROM messages 
                WHERE session_id = %s::uuid AND role = 'system'
                ORDER BY updated_at DESC 
                LIMIT 1
                """,
                (session_id,)
            )
            
            if existing_system:
                # Update existing system prompt
                execute_query(
                    """
                    UPDATE messages 
                    SET text_content = %s, raw_payload = %s, updated_at = %s, agent_id = %s, user_id = %s
                    WHERE id = %s
                    """,
                    (
                        system_prompt, 
                        json.dumps({"content": system_prompt, "role": "system"}),
                        datetime.utcnow(),
                        agent_id,
                        user_id,
                        existing_system[0]["id"]
                    ),
                    fetch=False
                )
                logger.debug(f"Updated system prompt for session {session_id} with agent_id {agent_id} and user_id {user_id}")
            else:
                # Generate a new UUID for the message
                message_id = str(uuid.uuid4())
                
                # Add new system prompt
                execute_query(
                    """
                    INSERT INTO messages (
                        id, session_id, role, text_content, raw_payload, 
                        message_type, user_id, agent_id
                    ) VALUES (
                        %s, %s::uuid, %s, %s, %s, 
                        %s, %s, %s
                    )
                    """,
                    (
                        message_id,
                        session_id, 
                        "system", 
                        system_prompt, 
                        json.dumps({"content": system_prompt, "role": "system"}),
                        "text",
                        user_id,
                        agent_id
                    ),
                    fetch=False
                )
                logger.debug(f"Added system prompt {message_id} to session {session_id} for user {user_id} with agent_id {agent_id}")
        except Exception as e:
            logger.error(f"Error updating system prompt for session {session_id}: {str(e)}")
            # Log traceback for debugging but don't crash
            import traceback
            logger.debug(f"Traceback: {traceback.format_exc()}")
            # Don't re-raise the exception to allow the application to continue
    
    def clear_session(self, session_id: str) -> None:
        """Clear all messages for a session.
        
        Args:
            session_id: The unique session identifier.
        """
        try:
            # Delete all messages for the session
            execute_query(
                "DELETE FROM messages WHERE session_id = %s::uuid",
                (session_id,),
                fetch=False
            )
            logger.debug(f"Cleared messages for session {session_id}")
        except Exception as e:
            logger.error(f"Error clearing session {session_id}: {str(e)}")
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists in the database.
        
        Args:
            session_id: The unique session identifier to check.
            
        Returns:
            True if the session exists, False otherwise.
        """
        try:
            result = execute_query(
                "SELECT 1 FROM sessions WHERE id = %s::uuid",
                (session_id,)
            )
            
            exists = bool(result and len(result) > 0)
            logger.debug(f"Session {session_id} exists: {exists}")
            return exists
        except Exception as e:
            logger.error(f"Error checking if session {session_id} exists: {str(e)}")
            return False
    
    def _ensure_session_exists(self, session_id: str, user_id: int = 1, session_origin: str = None, session_name: str = None) -> str:
        """Ensure a session exists, creating it if necessary.
        
        Args:
            session_id: The session ID to check or create.
            user_id: The user ID to associate with a new session.
            session_origin: Optional origin information for the session.
            session_name: Optional friendly name for the session.
            
        Returns:
            The validated session ID (same as input if valid, or a new ID if created).
        """
        # If session ID is not provided, create a new one
        if not session_id:
            return self.create_session(user_id=user_id, session_origin=session_origin, session_name=session_name)
            
        # Check if the session exists
        if not self.session_exists(session_id):
            # Check if the session_id is a valid UUID
            try:
                # Validate but don't modify the original session_id
                uuid_obj = uuid.UUID(session_id)
                # If valid UUID but doesn't exist, create it with the specified ID
                # Prepare metadata with session_origin if provided
                metadata = {}
                if session_origin:
                    metadata['session_origin'] = session_origin
                
                execute_query(
                    """
                    INSERT INTO sessions (id, user_id, platform, name, metadata, created_at, updated_at) 
                    VALUES (%s::uuid, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        session_id, 
                        user_id, 
                        session_origin or 'web',  # Use session_origin as platform or default to 'web'
                        session_name,
                        json.dumps(metadata),
                        datetime.utcnow(), 
                        datetime.utcnow()
                    ),
                    fetch=False
                )
                logger.info(f"Created new session with provided ID {session_id} for user {user_id}")
                return session_id
            except ValueError:
                # Not a valid UUID, create a new session with a valid UUID
                logger.warning(f"Provided session ID '{session_id}' is not a valid UUID, creating a new session")
                return self.create_session(user_id=user_id, session_origin=session_origin, session_name=session_name)
        else:
            # Session exists, update name if provided
            if session_name:
                execute_query(
                    """
                    UPDATE sessions 
                    SET name = %s, updated_at = %s
                    WHERE id = %s::uuid
                    """,
                    (
                        session_name,
                        datetime.utcnow(),
                        session_id
                    ),
                    fetch=False
                )
                logger.info(f"Updated session name to '{session_name}' for session {session_id}")
            return session_id
    
    def _ensure_user_exists(self, user_id: int) -> None:
        """
        Ensures a user exists in the database, creating it if necessary.
        
        Args:
            user_id: The ID of the user to check/create (as integer)
            
        Returns:
            None
        """
        try:
            # Use user_id directly as integer
            numeric_user_id = user_id if user_id is not None else 1
            
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
            
            # Create appropriate ModelMessage based on role
            message = None
            if role == "system":
                message = ModelRequest(parts=[SystemPromptPart(content=content)])
            elif role == "user":
                message = ModelRequest(parts=[UserPromptPart(content=content)])
            else:  # assistant role
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
            
            # Add metadata to any type of message
            if message:
                # Add message ID
                if db_message.get("id"):
                    message.id = db_message["id"]
                
                # Add session ID
                if db_message.get("session_id"):
                    message.session_id = db_message["session_id"]
                
                # Add user ID if available
                if db_message.get("user_id"):
                    message.user_id = db_message["user_id"]
                
                # Add agent ID if available
                if db_message.get("agent_id"):
                    message.agent_id = db_message["agent_id"]
                
                # Add system_prompt if available (for assistant messages)
                if role == "assistant":
                    # First check the dedicated column
                    if db_message.get("system_prompt"):
                        message.system_prompt = db_message["system_prompt"]
                    # If not in the column, check if it's in the raw_payload
                    elif raw_payload.get("system_prompt"):
                        message.system_prompt = raw_payload["system_prompt"]
                
                # Add context if available (for user messages)
                if role == "user" and db_message.get("context"):
                    if isinstance(db_message["context"], str):
                        try:
                            context_json = json.loads(db_message["context"])
                            message.context = context_json
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse context JSON for message {db_message.get('id')}")
                    elif isinstance(db_message["context"], dict):
                        message.context = db_message["context"]
                
                # Use updated_at as the timestamp
                if db_message.get("updated_at"):
                    message.timestamp = db_message["updated_at"]
                elif db_message.get("created_at"):
                    message.timestamp = db_message["created_at"]
                
                # Store created_at if available
                if hasattr(message, "created_at") and db_message.get("created_at"):
                    message.created_at = db_message["created_at"]
                
                # Store updated_at if available
                if hasattr(message, "updated_at") and db_message.get("updated_at"):
                    message.updated_at = db_message["updated_at"]
                
                return message
            else:
                # Fallback for unexpected message types
                return ModelResponse(parts=[TextPart(content=content or "Empty message")])
                
        except Exception as e:
            logger.error(f"Error converting database message to ModelMessage: {str(e)}")
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
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
                    (SELECT COUNT(*) FROM messages cm WHERE cm.session_id = s.id) as message_count,
                    (SELECT MAX(updated_at) FROM messages cm WHERE cm.session_id = s.id) as last_updated,
                    (SELECT a.name FROM agents a 
                     JOIN messages cm ON a.id = cm.agent_id 
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
                    "agent_name": session['agent_name'],
                    "session_origin": session['platform']  # Map platform to session_origin for API compatibility
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
    
    def create_session(self, user_id: int = 1, agent_id: Optional[int] = None, session_origin: str = None, session_name: str = None) -> str:
        """Create a new session for a user and agent.
        
        Args:
            user_id: The user ID to associate with the session.
            agent_id: Optional agent ID to associate with the session.
            session_origin: Optional origin information for the session.
            session_name: Optional friendly name for the session.
            
        Returns:
            The new session ID.
        """
        try:
            # Generate a UUID for the session
            session_id = str(uuid.uuid4())
            
            logger.info(f"Creating new session for user {user_id} with agent {agent_id} origin {session_origin}")
            
            # Prepare metadata with session_origin if provided
            metadata = {}
            if session_origin:
                metadata['session_origin'] = session_origin
            
            # Insert the session
            execute_query(
                """
                INSERT INTO sessions (id, user_id, platform, name, metadata, created_at, updated_at) 
                VALUES (%s::uuid, %s, %s, %s, %s, %s, %s)
                """,
                (
                    session_id, 
                    user_id, 
                    session_origin or 'web',  # Use session_origin as platform or default to 'web'
                    session_name,
                    json.dumps(metadata),
                    datetime.utcnow(), 
                    datetime.utcnow()
                ),
                fetch=False
            )
            
            logger.info(f"Created new session {session_id} for user {user_id} with agent {agent_id}")
            return session_id
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            raise e
    
    def get_session_metadata(self, session_id: str) -> Dict:
        """Get metadata for a specific session.
        
        Args:
            session_id: The unique session identifier.
            
        Returns:
            A dictionary containing session metadata or an empty dict if not found.
        """
        try:
            # First check if session exists
            if not self.session_exists(session_id):
                logger.warning(f"No session found with ID {session_id}")
                return {}
                
            # Get session details including metadata
            session_details = execute_query(
                """
                SELECT 
                    s.user_id, 
                    s.agent_id, 
                    s.created_at, 
                    s.updated_at,
                    s.terminated_at,
                    s.metadata,
                    s.platform,
                    u.email as user_email,
                    u.name as user_name
                FROM 
                    sessions s
                LEFT JOIN 
                    users u ON s.user_id = u.id
                WHERE 
                    s.id = %s::uuid
                """,
                (session_id,)
            )
            
            metadata = {}
            if session_details:
                session_data = session_details[0]
                
                # Get metadata from JSONB field
                stored_metadata = session_data.get("metadata")
                if stored_metadata:
                    # If it's already a dict, use it; otherwise parse it
                    if isinstance(stored_metadata, dict):
                        metadata = stored_metadata
                    else:
                        try:
                            metadata = json.loads(stored_metadata)
                        except (json.JSONDecodeError, TypeError):
                            metadata = {}
                            
                # Add standard session details to metadata
                metadata["user_id"] = session_data.get("user_id")
                metadata["agent_id"] = session_data.get("agent_id")
                metadata["platform"] = session_data.get("platform")
                metadata["created_at"] = session_data.get("created_at").isoformat() if session_data.get("created_at") else None
                metadata["updated_at"] = session_data.get("updated_at").isoformat() if session_data.get("updated_at") else None
                metadata["terminated_at"] = session_data.get("terminated_at").isoformat() if session_data.get("terminated_at") else None
                metadata["user_email"] = session_data.get("user_email")
                metadata["user_name"] = session_data.get("user_name")
            
            return metadata
        except Exception as e:
            logger.error(f"Error retrieving metadata for session {session_id}: {str(e)}")
            return {}
    
    def list_sessions(self, user_id: Optional[int] = None, page: int = 1, page_size: int = 10) -> Dict:
        """List chat sessions with pagination.
        
        Args:
            user_id: Optional user ID to filter sessions.
            page: Page number (1-indexed).
            page_size: Number of items per page.
            
        Returns:
            Dictionary containing sessions list and pagination details.
        """
        try:
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Build the query based on filters
            base_query = """
                SELECT 
                    s.id, 
                    s.user_id, 
                    s.agent_id, 
                    s.name,
                    s.platform,
                    s.created_at, 
                    s.updated_at,
                    s.terminated_at,
                    u.email as user_email,
                    u.name as user_name,
                    a.name as agent_name,
                    COUNT(m.id) as message_count
                FROM 
                    sessions s
                LEFT JOIN 
                    users u ON s.user_id = u.id
                LEFT JOIN 
                    agents a ON s.agent_id = a.id
                LEFT JOIN 
                    messages m ON s.id = m.session_id
            """
            
            count_query = "SELECT COUNT(*) FROM sessions s"
            
            # Add filters if user_id is provided
            where_clause = ""
            params = []
            
            if user_id:
                where_clause = "WHERE s.user_id = %s"
                params.append(user_id)
                count_query += " WHERE s.user_id = %s"
            
            # Complete the query with grouping, ordering and pagination
            query = f"""
                {base_query}
                {where_clause}
                GROUP BY s.id, u.email, u.name, a.name
                ORDER BY s.updated_at DESC
                LIMIT %s OFFSET %s
            """
            
            # Add pagination parameters
            params.extend([page_size, offset])
            
            # Execute the query
            sessions_result = execute_query(query, params)
            
            # Get total count
            count_result = execute_query(count_query, [user_id] if user_id else [])
            total_count = count_result[0]['count'] if count_result else 0
            
            # Calculate total pages
            total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0
            
            # Format the results
            sessions = []
            for session in sessions_result:
                # Format the session data
                formatted_session = {
                    "id": str(session["id"]),  # Ensure UUID is returned as string
                    "user_id": session["user_id"],
                    "agent_id": session["agent_id"],
                    "session_name": session["name"],
                    "platform": session["platform"],
                    "user_email": session["user_email"],
                    "user_name": session["user_name"],
                    "agent_name": session["agent_name"],
                    "message_count": session["message_count"],
                    "created_at": session["created_at"].isoformat() if session["created_at"] else None,
                    "updated_at": session["updated_at"].isoformat() if session["updated_at"] else None,
                    "terminated_at": session["terminated_at"].isoformat() if session["terminated_at"] else None
                }
                
                # Get the most recent message for the session
                last_message = execute_query(
                    """
                    SELECT 
                        text_content, 
                        role, 
                        updated_at
                    FROM 
                        messages 
                    WHERE 
                        session_id = %s::uuid
                    ORDER BY 
                        updated_at DESC 
                    LIMIT 1
                    """,
                    (session["id"],)
                )
                
                if last_message:
                    formatted_session["last_message"] = {
                        "content": last_message[0]["text_content"],
                        "role": last_message[0]["role"],
                        "timestamp": last_message[0]["updated_at"].isoformat() if last_message[0]["updated_at"] else None
                    }
                
                sessions.append(formatted_session)
            
            return {
                "sessions": sessions,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
        except Exception as e:
            logger.error(f"Error listing sessions: {str(e)}")
            return {
                "sessions": [],
                "total_count": 0,
                "page": page,
                "page_size": page_size,
                "total_pages": 0
            }
    
    def update_session_metadata(self, session_id: str, metadata: Dict) -> bool:
        """Update metadata for a session.
        
        Args:
            session_id: The unique session identifier.
            metadata: Dictionary of key-value pairs to update.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Ensure session exists
            if not self.session_exists(session_id):
                logger.warning(f"Cannot update metadata for non-existent session {session_id}")
                return False
                
            # Get current metadata to merge with new values
            current_metadata = execute_query(
                """
                SELECT metadata FROM sessions WHERE id = %s::uuid
                """,
                (session_id,)
            )
            
            merged_metadata = {}
            
            # Parse existing metadata if it exists
            if current_metadata and current_metadata[0].get("metadata"):
                existing = current_metadata[0].get("metadata")
                if isinstance(existing, dict):
                    merged_metadata = existing
                else:
                    try:
                        merged_metadata = json.loads(existing)
                    except (json.JSONDecodeError, TypeError):
                        merged_metadata = {}
            
            # Merge with new metadata values
            for key, value in metadata.items():
                # Skip any None values
                if value is None:
                    continue
                    
                # Add/update the key-value pair
                merged_metadata[key] = value
            
            # Update the session with merged metadata
            execute_query(
                """
                UPDATE sessions
                SET metadata = %s, updated_at = %s
                WHERE id = %s::uuid
                """,
                (json.dumps(merged_metadata), datetime.utcnow(), session_id),
                fetch=False
            )
            
            logger.debug(f"Updated metadata for session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating metadata for session {session_id}: {str(e)}")
            return False 