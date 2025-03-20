"""Create memory tool implementation.

Provides functionality to create new memories in the database.
"""

from typing import Dict, Any, Optional, Union
import json
import logging
import os
import requests
import uuid
from uuid import UUID
from datetime import datetime
import re
from pydantic import BaseModel
from pydantic_ai import RunContext
from src.db import get_agent_by_name, create_memory as create_memory_in_db
from src.db import execute_query
from src.tools.memory_tools.common import map_agent_id
from src.tools.memory_tools.interface import invalidate_memory_cache
from src.agents.models.agent_factory import AgentFactory

logger = logging.getLogger(__name__)


def get_agent_id_from_db(agent_name):
    """Get the agent ID from the database by name.
    
    Args:
        agent_name: The name of the agent.
        
    Returns:
        The agent ID if found, None otherwise.
    """
    try:
        # Use repository function instead of direct SQL query
        agent = get_agent_by_name(agent_name)
        
        if not agent:
            logger.warning(f"Agent '{agent_name}' not found in database")
            return None
            
        agent_id = agent.id if hasattr(agent, "id") else None
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


@invalidate_memory_cache
async def create_memory(ctx: RunContext[Dict], name: str, content: Union[str, Dict[str, Any]], 
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
            # Try to get the agent ID using repository functions
            try:
                # Try to get any available agent
                available_agents = AgentFactory.list_available_agents()
                if available_agents:
                    agent = get_agent_by_name(available_agents[0])
                    agent_id = agent.id if agent and hasattr(agent, "id") else None
                    agent_id_raw = available_agents[0]
                else:
                    agent_id = None
                    agent_id_raw = None
                
                logger.info(f"Using first available agent ID: {agent_id}")
            except Exception as e:
                logger.warning(f"Could not determine default agent ID: {str(e)}")
                agent_id = None
                agent_id_raw = None
                
            user_id = 1  # Default to user ID 1 if not provided
            session_id = None
            
            logger.info(f"Using default values: agent_id={agent_id}, user_id={user_id}, session_id={session_id}")
            
            # Use the helper function for the creation
            return _perform_create(agent_id, user_id, session_id if session_specific else None, 
                                  name, content, description, scope, read_mode, metadata)
        
        # Extract context information
        agent_id_raw = ctx.deps.get("agent_id")
        
        # If agent_id is not in context, try to get any available agent
        if not agent_id_raw:
            logger.warning("No agent_id found in context, looking for available agents")
            try:
                available_agents = AgentFactory.list_available_agents()
                if available_agents:
                    agent_id_raw = available_agents[0]
                    logger.info(f"Using first available agent: {agent_id_raw}")
                else:
                    logger.warning("No available agents found")
                    return {"success": False, "message": "No available agents found"}
            except Exception as e:
                logger.error(f"Failed to find available agents: {str(e)}")
                return {"success": False, "message": f"No agent ID available and failed to find alternative agents: {str(e)}"}
        
        # Get the agent object using the repository function
        agent = get_agent_by_name(agent_id_raw)
        if not agent:
            return {"success": False, "message": f"Agent '{agent_id_raw}' not found"}
            
        agent_id = agent.id if hasattr(agent, "id") else None
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