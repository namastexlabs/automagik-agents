"""Message repository functions for database operations."""

import uuid
import json
import logging
from typing import List, Optional, Dict, Any, Tuple, Union
from datetime import datetime
from pydantic import BaseModel

from src.db.connection import execute_query
from src.db.models import Message
from src.db.repository.session import get_session

# Configure logger
logger = logging.getLogger(__name__)


def get_message(message_id: Union[uuid.UUID, str]) -> Optional[Message]:
    """Get a message by ID.
    
    Args:
        message_id: The UUID of the message to retrieve
        
    Returns:
        Message object if found, None otherwise
    """
    try:
        # Convert string UUID to UUID object if needed
        if isinstance(message_id, str):
            message_id = uuid.UUID(message_id)
            
        query = """
            SELECT * FROM messages WHERE id = %s
        """
        result = execute_query(query, [message_id])
        
        if isinstance(result, list) and len(result) > 0:
            # Convert result dictionary to Message model
            return Message(**result[0])
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            return Message(**result['rows'][0])
            
        return None
    except Exception as e:
        logger.error(f"Error retrieving message {message_id}: {str(e)}")
        return None


def list_messages(session_id: uuid.UUID, page: int = 1, page_size: int = 100, 
                 sort_desc: bool = True) -> List[Message]:
    """List messages for a session with pagination.
    
    Args:
        session_id: The UUID of the session to get messages for
        page: The page number to return (1-indexed)
        page_size: The number of messages per page
        sort_desc: Whether to sort by created_at in descending order (newest first)
        
    Returns:
        List of Message objects
    """
    try:
        order_dir = "DESC" if sort_desc else "ASC"
        offset = (page - 1) * page_size
        
        query = f"""
            SELECT * FROM messages 
            WHERE session_id = %s
            ORDER BY created_at {order_dir}
            LIMIT %s OFFSET %s
        """
        
        result = execute_query(query, [session_id, page_size, offset])
        
        messages = []
        if isinstance(result, list):
            for row in result:
                messages.append(Message(**row))
        elif isinstance(result, dict) and 'rows' in result:
            for row in result['rows']:
                messages.append(Message(**row))
                
        return messages
    except Exception as e:
        logger.error(f"Error listing messages for session {session_id}: {str(e)}")
        return []


def count_messages(session_id: uuid.UUID) -> int:
    """Count the total number of messages in a session.
    
    Args:
        session_id: The UUID of the session
        
    Returns:
        Total message count
    """
    try:
        query = "SELECT COUNT(*) as count FROM messages WHERE session_id = %s"
        result = execute_query(query, [session_id])
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('count', 0)
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            return result['rows'][0].get('count', 0)
            
        return 0
    except Exception as e:
        logger.error(f"Error counting messages for session {session_id}: {str(e)}")
        return 0


def create_message(message: Message) -> Optional[uuid.UUID]:
    """Create a new message in the database.
    
    Args:
        message: The Message object to create
        
    Returns:
        UUID of the created message if successful, None otherwise
    """
    try:
        # Log message parameters for debugging
        logger.debug(f"Creating message with parameters: session_id={message.session_id}, role={message.role}, "
                    f"user_id={message.user_id}, agent_id={message.agent_id}, "
                    f"message_type={message.message_type}, text_length={len(message.text_content or '') if message.text_content else 0}")
        
        # Prepare raw_payload, tool_calls, and tool_outputs for storage
        raw_payload = message.raw_payload
        if raw_payload is not None and not isinstance(raw_payload, str):
            raw_payload = json.dumps(raw_payload)
            
        tool_calls = message.tool_calls
        if tool_calls is not None and not isinstance(tool_calls, str):
            tool_calls = json.dumps(tool_calls)
            
        tool_outputs = message.tool_outputs
        if tool_outputs is not None and not isinstance(tool_outputs, str):
            tool_outputs = json.dumps(tool_outputs)
            
        # Handle context and system_prompt
        context = message.context
        if context is not None and not isinstance(context, str):
            context = json.dumps(context)
            
        system_prompt = message.system_prompt
        
        # Use current time if not provided
        created_at = message.created_at or datetime.now()
        updated_at = message.updated_at or datetime.now()
        
        query = """
            INSERT INTO messages (
                id, session_id, user_id, agent_id, role, text_content, 
                message_type, raw_payload, tool_calls, tool_outputs,
                context, system_prompt, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING id
        """
        
        params = [
            message.id, message.session_id, message.user_id, message.agent_id,
            message.role, message.text_content, message.message_type,
            raw_payload, tool_calls, tool_outputs,
            context, system_prompt, created_at, updated_at
        ]
        
        # Log the SQL query and parameters for debugging
        logger.debug(f"Executing message creation query: {query}")
        logger.debug(f"Query parameters: id={message.id}, session_id={message.session_id}, "
                    f"user_id={message.user_id}, agent_id={message.agent_id}")
        
        result = execute_query(query, params)
        
        if isinstance(result, list) and len(result) > 0:
            message_id = result[0].get('id')
            logger.info(f"Successfully created message {message_id} for session {message.session_id}")
            return message_id
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            message_id = result['rows'][0].get('id')
            logger.info(f"Successfully created message {message_id} for session {message.session_id}")
            return message_id
            
        logger.error(f"Error creating message: Unexpected result format: {result}")
        return None
    except Exception as e:
        logger.error(f"Error creating message: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        logger.error(f"Message details: session_id={message.session_id}, role={message.role}, "
                     f"id={message.id}, text_length={len(message.text_content or '') if message.text_content else 0}")
        return None


def update_message(message: Message) -> Optional[uuid.UUID]:
    """Update an existing message in the database.
    
    Args:
        message: The Message object to update
        
    Returns:
        UUID of the updated message if successful, None otherwise
    """
    try:
        # Prepare raw_payload, tool_calls, and tool_outputs for storage
        raw_payload = message.raw_payload
        if raw_payload is not None and not isinstance(raw_payload, str):
            raw_payload = json.dumps(raw_payload)
            
        tool_calls = message.tool_calls
        if tool_calls is not None and not isinstance(tool_calls, str):
            tool_calls = json.dumps(tool_calls)
            
        tool_outputs = message.tool_outputs
        if tool_outputs is not None and not isinstance(tool_outputs, str):
            tool_outputs = json.dumps(tool_outputs)
            
        # Handle context and system_prompt
        context = message.context
        if context is not None and not isinstance(context, str):
            context = json.dumps(context)
            
        system_prompt = message.system_prompt
        
        # Use current time for updated_at
        updated_at = datetime.now()
        
        query = """
            UPDATE messages
            SET session_id = %s,
                user_id = %s,
                agent_id = %s,
                role = %s,
                text_content = %s,
                message_type = %s,
                raw_payload = %s,
                tool_calls = %s,
                tool_outputs = %s,
                context = %s,
                system_prompt = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING id
        """
        
        params = [
            message.session_id, message.user_id, message.agent_id,
            message.role, message.text_content, message.message_type,
            raw_payload, tool_calls, tool_outputs,
            context, system_prompt, updated_at, message.id
        ]
        
        result = execute_query(query, params)
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('id')
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            return result['rows'][0].get('id')
            
        return None
    except Exception as e:
        logger.error(f"Error updating message {message.id}: {str(e)}")
        return None


def delete_message(message_id: Union[uuid.UUID, str]) -> bool:
    """Delete a message from the database.
    
    Args:
        message_id: The UUID of the message to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert string UUID to UUID object if needed
        if isinstance(message_id, str):
            message_id = uuid.UUID(message_id)
            
        query = "DELETE FROM messages WHERE id = %s RETURNING id"
        result = execute_query(query, [message_id])
        
        # If we got a result, the delete was successful
        return (isinstance(result, list) and len(result) > 0) or \
               (isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0)
    except Exception as e:
        logger.error(f"Error deleting message {message_id}: {str(e)}")
        return False


def delete_session_messages(session_id: Union[uuid.UUID, str]) -> bool:
    """Delete all messages for a session.
    
    Args:
        session_id: The UUID of the session
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert string UUID to UUID object if needed
        if isinstance(session_id, str):
            session_id = uuid.UUID(session_id)
            
        query = "DELETE FROM messages WHERE session_id = %s"
        execute_query(query, [session_id])
        
        # We don't return any rows, so just return True
        return True
    except Exception as e:
        logger.error(f"Error deleting messages for session {session_id}: {str(e)}")
        return False


def get_system_prompt(session_id: Union[uuid.UUID, str]) -> Optional[str]:
    """Get the system prompt for a session from metadata or messages.
    
    Args:
        session_id: The UUID of the session
        
    Returns:
        System prompt string if found, None otherwise
    """
    try:
        # Convert string UUID to UUID object if needed
        if isinstance(session_id, str):
            session_id = uuid.UUID(session_id)
            
        # First try to get system prompt from session metadata
        query = "SELECT metadata FROM sessions WHERE id = %s"
        result = execute_query(query, [session_id])
        
        metadata = None
        if isinstance(result, list) and len(result) > 0 and result[0].get('metadata'):
            metadata = result[0].get('metadata')
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0 and result['rows'][0].get('metadata'):
            metadata = result['rows'][0].get('metadata')
        
        if metadata:
            # Parse metadata if it's a string
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except json.JSONDecodeError:
                    pass
                
            # Check if metadata is a dict with system_prompt
            if isinstance(metadata, dict) and 'system_prompt' in metadata:
                return metadata['system_prompt']
        
        # If no system prompt in metadata, look for system messages
        query = """
            SELECT text_content FROM messages 
            WHERE session_id = %s AND role = 'system'
            ORDER BY created_at DESC
            LIMIT 1
        """
        
        result = execute_query(query, [session_id])
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('text_content')
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            return result['rows'][0].get('text_content')
            
        return None
    except Exception as e:
        logger.error(f"Error retrieving system prompt for session {session_id}: {str(e)}")
        return None


def list_session_messages(session_id: uuid.UUID, page: int = 1, page_size: int = 100, sort_desc: bool = False) -> Tuple[List[Dict[str, Any]], int]:
    """List messages for a specific session with pagination.
    
    Args:
        session_id: The session ID
        page: Page number (1-indexed)
        page_size: Number of messages per page
        sort_desc: Sort by most recent first if True
        
    Returns:
        Tuple of (list of messages, total count)
    """
    try:
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Get total count
        count_query = "SELECT COUNT(*) as count FROM messages WHERE session_id = %s"
        count_result = execute_query(count_query, (str(session_id),))
        total_count = count_result[0]["count"] if count_result else 0
        
        # Set up sort order
        sort_direction = "DESC" if sort_desc else "ASC"
        
        # Get paginated results
        query = f"""
            SELECT * FROM messages 
            WHERE session_id = %s 
            ORDER BY created_at {sort_direction}
            LIMIT %s OFFSET %s
        """
        
        result = execute_query(query, (str(session_id), page_size, offset))
        
        # Convert rows to dictionaries
        messages = []
        for row in result:
            message_dict = dict(row)
            
            # Parse JSON fields if present
            for json_field in ["content", "metadata", "tool_calls", "tool_outputs"]:
                if json_field in message_dict and message_dict[json_field]:
                    try:
                        if isinstance(message_dict[json_field], str):
                            message_dict[json_field] = json.loads(message_dict[json_field])
                    except json.JSONDecodeError:
                        # Keep as string if not valid JSON
                        pass
            
            messages.append(message_dict)
        
        return messages, total_count
    except Exception as e:
        logger.error(f"Error listing session messages: {str(e)}")
        return [], 0
