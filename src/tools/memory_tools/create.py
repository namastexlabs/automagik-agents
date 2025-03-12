"""Create memory tool implementation.

Provides functionality to create new memories in the database.
"""

from typing import Dict, Any, Optional, Union
import json
import logging
import os
import requests
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from pydantic_ai import RunContext
from src.tools.memory_tools.common import map_agent_id

logger = logging.getLogger(__name__)


def get_agent_id_from_db(agent_name):
    """Get the agent ID from the database by name.
    
    Args:
        agent_name: The name of the agent.
        
    Returns:
        The agent ID if found, None otherwise.
    """
    try:
        query = "SELECT id FROM agents WHERE name = %s"
        result = execute_query(query, [agent_name])
        
        # Handle case where result is a list (DB rows) or dict with 'rows' key
        if isinstance(result, list):
            rows = result
        else:
            rows = result.get('rows', [])
            
        if not rows:
            logger.warning(f"Agent '{agent_name}' not found in database")
            return None
            
        agent_id = rows[0].get('id')
        if not agent_id:
            logger.warning(f"Agent '{agent_name}' has no ID")
            return None
            
        logger.info(f"Found agent ID {agent_id} for agent '{agent_name}'")
        return agent_id
    except Exception as e:
        logger.error(f"Error getting agent ID from database: {str(e)}")
        return None


class MemoryCreateResponse(BaseModel):
    """Response model for a memory creation operation."""
    id: str
    name: str
    success: bool
    message: str


def get_create_memory_description() -> str:
    """Basic description for the create_memory tool.
    
    This is a fallback description used when dynamic generation fails.
    
    Returns:
        A basic description for the create_memory tool.
    """
    return "Create a new memory in the database with the specified name, content, and metadata."


def _perform_create(agent_id, user_id, session_id, name, content, description=None, scope=None, read_mode="tool_calling", metadata=None):
    """Helper function to perform the actual memory creation.
    
    This function contains the core logic for creating a memory, extracted to avoid code duplication.
    
    Args:
        agent_id: The agent ID (numeric).
        user_id: The user ID.
        session_id: The session ID.
        name: The name of the memory to create.
        content: The content to store.
        description: Optional description of the memory.
        scope: Optional scope of the memory (global, user, or session).
        read_mode: How this memory should be used (system_prompt or tool_calling).
        metadata: Optional metadata to store with the memory.
        
    Returns:
        Dictionary with the result of the operation.
    """
    try:
        logger.info(f"Creating memory: name={name}, scope={scope}, read_mode={read_mode}")
        logger.info(f"Context: agent_id={agent_id}, user_id={user_id}, session_id={session_id}")
        
        # Validate read_mode
        if read_mode not in ["system_prompt", "tool_calling"]:
            return {"success": False, "message": f"Invalid read_mode: {read_mode}. Must be 'system_prompt' or 'tool_calling'"}
        
        # Process content based on its type
        processed_content = content
        
        # If content is a dictionary, convert it to a JSON string
        if isinstance(content, dict):
            logger.info(f"Converting dictionary content to JSON string for memory creation")
            processed_content = json.dumps(content)
        
        # Determine the scope of the memory
        if scope == "global":
            # Global memories are accessible to all users of this agent
            memory_user_id = None
            memory_session_id = None
        elif scope == "user":
            # User memories are accessible to a specific user across all sessions
            memory_user_id = user_id
            memory_session_id = None
        elif scope == "session":
            # Session memories are accessible only in the current session
            memory_user_id = user_id
            memory_session_id = session_id
        else:
            # Default to user scope if not specified
            memory_user_id = user_id
            memory_session_id = None
            
        # Prepare the memory data
        memory_data = {
            "name": name,
            "content": processed_content,
            "agent_id": agent_id,
            "read_mode": read_mode
        }
        
        # Add optional fields if provided
        if description:
            memory_data["description"] = description
            
        if memory_user_id is not None:
            memory_data["user_id"] = memory_user_id
            
        if memory_session_id is not None:
            memory_data["session_id"] = memory_session_id
            
        # Add metadata if provided
        if metadata is not None:
            # Convert metadata to JSON string if it's a dictionary
            if isinstance(metadata, dict):
                memory_data["metadata"] = json.dumps(metadata)
            else:
                memory_data["metadata"] = metadata
        
        # Set up API request basics
        host = os.environ.get("AM_HOST", "127.0.0.1")
        port = os.environ.get("AM_PORT", "8881")
        base_url = f"http://{host}:{port}"
        api_key = os.environ.get("AM_API_KEY", "namastex-888")  # Default to test key if not set
        
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": api_key
        }
        
        try:
            # Call the create API endpoint
            api_url = f"{base_url}/api/v1/memories"
            
            response = requests.post(api_url, headers=headers, json=memory_data)
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            # Process successful response
            created_memory = response.json()
            
            return {
                "success": True,
                "message": "Memory created successfully",
                "id": created_memory["id"],
                "name": created_memory["name"]
            }
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error when accessing memory API: {str(e)}")
            return {"success": False, "message": f"API error: {str(e)}"}
            
        except Exception as e:
            logger.error(f"Error creating memory: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    except Exception as e:
        logger.error(f"Error in _perform_create: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


def create_memory(ctx: RunContext[Dict], name: str, content: Union[str, Dict[str, Any]], 
                 description: Optional[str] = None, read_mode: str = "tool_calling", 
                 scope: Optional[str] = None, session_specific: bool = False,
                 metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a new memory in the database.
    
    Args:
        ctx: The run context.
        name: The name of the memory to create.
        content: The content to store in the memory.
        description: Optional description of the memory.
        read_mode: How this memory should be used (system_prompt or tool_calling).
        scope: Optional scope of the memory (global, user, or session).
        session_specific: If True, the memory will be associated with the current session.
        metadata: Optional metadata to store with the memory.
        
    Returns:
        Dictionary with the result of the operation.
    """
    try:
        # Log context for debugging
        logger.info(f"Create memory context: {ctx}")
        if hasattr(ctx, 'deps'):
            logger.info(f"Context deps: {ctx.deps}")
        else:
            logger.info("Context has no deps attribute")
        
        # Validate read_mode
        if read_mode not in ["system_prompt", "tool_calling"]:
            return {"success": False, "message": f"Invalid read_mode: {read_mode}. Must be 'system_prompt' or 'tool_calling'"}
        
        # Special case for when ctx is None or empty
        if ctx is None or (not hasattr(ctx, 'deps') or ctx.deps is None or not ctx.deps):
            logger.warning("Context is None or empty, using default values")
            # Try to get the agent ID from the database
            agent_id = get_agent_id_from_db("sofia_agent")
            if agent_id is None:
                agent_id = 3  # Default to sofia_agent ID 3 as fallback
                logger.warning(f"⚠️ Agent ID not found for name: sofia_agent, using default ID {agent_id}")
            agent_id_raw = "sofia_agent"
            user_id = 1  # Default to user ID 1 if not provided
            session_id = None
            
            logger.info(f"Using default values: agent_id={agent_id}, user_id={user_id}, session_id={session_id}")
            
            # Use the helper function for the creation
            return _perform_create(agent_id, user_id, session_id if session_specific else None, 
                                  name, content, description, scope, read_mode, metadata)
        
        # Extract context information
        agent_id_raw = ctx.deps.get("agent_id")
        
        # If agent_id is not in context, log a warning and use a default
        if not agent_id_raw:
            logger.warning("No agent_id found in context, using default value")
            agent_id_raw = "sofia_agent"
        
        # Get the numeric agent ID from the agent name
        query = "SELECT id FROM agents WHERE name = %s"
        result = execute_query(query, [agent_id_raw])
        
        # Handle case where result is a list (DB rows) or dict with 'rows' key
        if isinstance(result, list):
            rows = result
        else:
            rows = result.get('rows', [])
            
        if not rows:
            return {"success": False, "message": f"Agent '{agent_id_raw}' not found"}
            
        agent_id = rows[0].get('id')
        if not agent_id:
            return {"success": False, "message": f"Agent '{agent_id_raw}' has no ID"}
            
        # Get user ID and session ID from context
        user_id = ctx.deps.get("user_id", 1)  # Default to user ID 1 if not provided
        session_id = ctx.deps.get("session_id") if session_specific else None
        
        # Use the helper function for the creation
        return _perform_create(agent_id, user_id, session_id, name, content, 
                              description, scope, read_mode, metadata)
        
    except Exception as e:
        logger.error(f"Error in create_memory: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}