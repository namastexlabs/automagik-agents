"""Update memory tool implementation.

Provides functionality to update existing memories in the database.
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
from src.db import execute_query
from src.db import get_agent_by_name, get_memory, create_memory, update_memory as update_memory_in_db
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
        # Use repository function instead of direct SQL query
        agent = get_agent_by_name(agent_name)
        
        if not agent:
            logger.warning(f"Agent '{agent_name}' not found in database")
            return None
            
        agent_id = agent.id
        if not agent_id:
            logger.warning(f"Agent '{agent_name}' has no ID")
            return None
            
        logger.info(f"Found agent ID {agent_id} for agent '{agent_name}'")
        return agent_id
    except Exception as e:
        logger.error(f"Error getting agent ID from database: {str(e)}")
        return None


class MemoryUpdateResponse(BaseModel):
    """Response model for a memory update operation."""
    id: str
    name: str
    success: bool
    message: str


def get_update_memory_description() -> str:
    """Basic description for the update_memory tool.
    
    This is a fallback description used when dynamic generation fails.
    
    Returns:
        A basic description for the update_memory tool.
    """
    return "Update an existing memory in the database with new content."


def _perform_update(agent_id, user_id, session_id, content, memory_id=None, name=None, description=None, metadata=None, read_mode=None):
    """Helper function to perform the actual memory update.
    
    This function contains the core logic for updating a memory, extracted to avoid code duplication.
    
    Args:
        agent_id: The agent ID (numeric).
        user_id: The user ID.
        session_id: The session ID.
        content: The new content to store.
        memory_id: Optional ID of the memory to update.
        name: Optional name of the memory to update.
        description: Optional new description for the memory.
        metadata: Optional new metadata for the memory.
        read_mode: Optional new read_mode for the memory (system_prompt or tool_calling).
        
    Returns:
        Dictionary with the result of the operation.
    """
    try:
        logger.info(f"Updating memory: memory_id={memory_id}, name={name}")
        logger.info(f"Context: agent_id={agent_id}, user_id={user_id}, session_id={session_id}")
        logger.info(f"Additional fields: description={description is not None}, metadata={metadata is not None}, read_mode={read_mode}")
        
        # If a name was provided but no memory_id, we need to find the memory 
        # with proper access control to ensure only appropriate memories are updated
        if name and not memory_id:
            # Use the get_memory function to find the memory by name with filtering
            from src.db import get_memory_by_name
            memory = get_memory_by_name(name)
            
            if not memory:
                return {"success": False, "message": f"No memory found with name '{name}'"}
            
            # Check access control based on agent_id, user_id, and session_id
            memory_agent_id = memory.agent_id
            memory_user_id = memory.user_id
            memory_session_id = memory.session_id
            
            # Check if this agent has access to this memory
            has_access = False
            
            # Case 1: Agent-specific global memories (accessible to all users of this agent)
            if memory_agent_id == agent_id and memory_user_id is None:
                has_access = True
                
            # Case 2: Agent + User memories (personalized agent)
            elif memory_agent_id == agent_id and memory_user_id == user_id and memory_session_id is None:
                has_access = True
                
            # Case 3: Agent + User + Session memories (personalized session)
            elif memory_agent_id == agent_id and memory_user_id == user_id and memory_session_id == session_id:
                has_access = True
                
            if not has_access:
                return {"success": False, "message": f"Memory '{name}' is not accessible to this agent/user"}
            
            # Use the found memory ID
            memory_id = memory.id
            if not memory_id:
                return {"success": False, "message": "Found memory has no ID"}
                
            logger.info(f"Found memory ID {memory_id} for name '{name}'")
            
        # Process content based on its type
        processed_content = content
        
        # If content is a dictionary, convert it to a JSON string
        if isinstance(content, dict):
            logger.info(f"Converting dictionary content to JSON string for memory update")
            processed_content = json.dumps(content)
        
        # Prepare the memory data - start with content
        memory_data = {"content": processed_content}
        
        # Add optional fields if provided
        if description is not None:
            memory_data["description"] = description
            
        if metadata is not None:
            # Convert metadata to JSON string if it's a dictionary
            if isinstance(metadata, dict):
                memory_data["metadata"] = json.dumps(metadata)
            else:
                memory_data["metadata"] = metadata
                
        if read_mode is not None:
            # Validate read_mode
            if read_mode not in ["system_prompt", "tool", "tool_calling"]:
                return {"success": False, "message": f"Invalid read_mode: {read_mode}. Must be 'system_prompt', 'tool', or 'tool_calling'"}
            
            # Map tool_calling to tool for consistency
            if read_mode == "tool_calling":
                read_mode = "tool"
                
            memory_data["read_mode"] = read_mode
        
        # Convert memory_id to UUID if needed
        if isinstance(memory_id, str):
            try:
                memory_id = UUID(memory_id)
            except ValueError:
                return {"success": False, "message": f"Invalid memory ID format: {memory_id}"}
        
        # Use repository function to update the memory
        result = update_memory_in_db(memory_id, memory_data)
        
        if result:
            # Get the updated memory to return complete information
            updated_memory = get_memory(memory_id)
            if updated_memory:
                return {
                    "success": True,
                    "message": f"Memory updated successfully",
                    "id": str(updated_memory.id),
                    "name": updated_memory.name
                }
            else:
                return {
                    "success": True,
                    "message": f"Memory updated successfully but could not retrieve details",
                    "id": str(memory_id),
                    "name": name or "Unknown"
                }
        else:
            return {"success": False, "message": "Failed to update memory"}
            
    except Exception as e:
        logger.error(f"Error updating memory: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {"success": False, "message": f"Error updating memory: {str(e)}"}


def update_memory(ctx: RunContext[Dict], content: Union[str, Dict[str, Any]], memory_id: Optional[str] = None, 
                 name: Optional[str] = None, description: Optional[str] = None, 
                 read_mode: Optional[str] = None, session_specific: bool = False,
                 metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Update a memory in the database.
    
    Args:
        ctx: The context of the current run
        content: The new content to store
        memory_id: Optional ID of the memory to update
        name: Optional name of the memory to update
        description: Optional new description for the memory
        read_mode: Optional new read_mode for the memory (system_prompt or tool_calling)
        session_specific: Whether to include the session_id in the memory
        metadata: Optional new metadata for the memory
        
    Returns:
        Dictionary with the result of the operation
    """
    try:
        # Validate required parameters
        if not content:
            return {"success": False, "message": "Content is required"}
            
        if not memory_id and not name:
            return {"success": False, "message": "Either memory_id or name must be provided"}
        
        # Validate read_mode if provided
        if read_mode is not None and read_mode not in ["system_prompt", "tool", "tool_calling"]:
            return {"success": False, "message": f"Invalid read_mode: {read_mode}. Must be 'system_prompt', 'tool', or 'tool_calling'"}
        
        # Log context for debugging
        logger.info(f"Update memory context: {ctx}")
        if hasattr(ctx, 'deps'):
            logger.info(f"Context deps: {ctx.deps}")
        else:
            logger.info("Context has no deps attribute")
        
        # Special case for when ctx is None or empty
        if ctx is None or (not hasattr(ctx, 'deps') or ctx.deps is None or not ctx.deps):
            logger.warning("Context is None or empty, using default values")
            # Try to get the agent ID from the database
            agent = get_agent_by_name("sofia_agent")
            if agent is None:
                agent_id = 3  # Default to sofia_agent ID 3 as fallback
                logger.warning(f"⚠️ Agent ID not found for name: sofia_agent, using default ID {agent_id}")
            else:
                agent_id = agent.id
                
            agent_id_raw = "sofia_agent"
            user_id = 1  # Default to user ID 1 if not provided
            session_id = None if not session_specific else None  # No session ID available in this case
            
            logger.info(f"Using default values: agent_id={agent_id}, user_id={user_id}, session_id={session_id}")
            
            # Use the helper function for the update
            return _perform_update(agent_id, user_id, session_id, content, memory_id, name, description, metadata, read_mode)
        
        # Extract context information
        agent_id_raw = ctx.deps.get("agent_id")
        
        # If agent_id is not in context, log a warning and use a default
        if not agent_id_raw:
            logger.warning("No agent_id found in context, using default value")
            agent_id_raw = "sofia_agent"
        
        # Get the numeric agent ID from the agent name using repository function
        agent = get_agent_by_name(agent_id_raw)
        
        if not agent:
            return {"success": False, "message": f"Agent '{agent_id_raw}' not found"}
            
        agent_id = agent.id
        if not agent_id:
            return {"success": False, "message": f"Agent '{agent_id_raw}' has no ID"}
            
        # Get user ID and session ID from context
        user_id = ctx.deps.get("user_id", 1)  # Default to user ID 1 if not provided
        session_id = ctx.deps.get("session_id") if session_specific else None
        
        # Use the helper function for the update
        return _perform_update(agent_id, user_id, session_id, content, memory_id, name, description, metadata, read_mode)
        
    except Exception as e:
        logger.error(f"Error in update_memory: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}
