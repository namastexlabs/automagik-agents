"""Read memory tool implementation.

Provides functionality to read memories from the database with various filtering options.
"""

from typing import Dict, Any, Optional, List, Union
import logging
import json
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from pydantic_ai import RunContext
from src.db import (
    Memory, 
    get_memory, 
    get_memory_by_name,
    list_memories as repo_list_memories
)
from src.tools.memory_tools.common import clean_memory_object, map_agent_id

logger = logging.getLogger(__name__)


class MemoryReadResult(BaseModel):
    """Result model for a memory read operation."""
    id: str
    name: str
    description: Optional[str] = None
    content: str
    created_at: datetime
    updated_at: datetime
    read_mode: Optional[str] = None
    access: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def get_read_memory_description() -> str:
    """Basic description for the read_memory tool.
    
    This is a fallback description used when dynamic generation fails.
    
    Returns:
        A basic description for the read_memory tool.
    """
    return "Read memories from the database by name or ID, or list all available memories."


def read_memory(ctx: RunContext[Dict], memory_id: Optional[str] = None, name: Optional[str] = None, 
               read_mode: Optional[str] = None, list_all: Optional[bool] = False,
               session_specific: bool = False) -> Dict[str, Any]:
    """Read a memory or list of memories with optional filters.
    
    This tool allows an agent to retrieve memories stored in the database.
    It can return a single memory or a list of memories matching the specified criteria.
    If no specific memory is requested and list_all is True, it will return a list
    of all available memories with their descriptions to serve as a guide for their usage.
    
    Args:
        ctx: The run context with agent, user, and session information.
        memory_id: Optional ID of the specific memory to retrieve.
        name: Optional memory name (or partial name) to search for.
        read_mode: Optional filter for memory read mode ("system_prompt" or "tool_calling").
        list_all: If True and no specific memory is requested, returns all available memories.
        session_specific: If True, only memories associated with the current session will be considered.
        
    Returns:
        Dictionary containing either a single memory or a list of memories with metadata.
    """
    try:
        # Extract context information
        # Handle case where ctx.deps might be None
        agent_id_raw = None
        if hasattr(ctx, 'deps') and ctx.deps is not None and ctx.deps:
            # Get agent_id from context
            agent_id_raw = ctx.deps.get("agent_id")
            
            # If agent_id is not in context, log a warning and use a default
            if not agent_id_raw:
                logger.warning("No agent_id found in context, using default value")
                agent_id_raw = "sofia_agent"
            
            # Get the numeric agent ID from the agent name
            if isinstance(agent_id_raw, int):
                agent_id = agent_id_raw
            elif agent_id_raw.isdigit():
                agent_id = int(agent_id_raw)
            else:
                # Get agent ID via the map_agent_id helper
                agent_id = map_agent_id(agent_id_raw)
            
            user_id = ctx.deps.get("user_id", 1)  # Default to user ID 1 if not provided
            session_id = ctx.deps.get("session_id")
        else:
            # Fallback when deps is not available - use default values
            logger.warning("Context deps not available for read_memory, using default values")
            agent_id = 3  # Default to sofia_agent ID 3 as fallback
            agent_id_raw = "sofia_agent"
            user_id = 1  # Default to user ID 1 if not provided
            session_id = None

        # Validate and normalize read_mode if provided
        original_read_mode = None
        if read_mode is not None:
            original_read_mode = read_mode  # Store original value for display
            # Map "tool_calling" to "tool" for compatibility with the database
            if read_mode.lower() == "tool_calling":
                read_mode = "tool"
                logger.info(f"Mapped read_mode 'tool_calling' to 'tool' for database query")
            elif read_mode.lower() != "system_prompt":
                return {"success": False, "message": f"Invalid read_mode: {read_mode}. Must be 'system_prompt' or 'tool_calling'"}
            
            logger.info(f"Using read_mode={read_mode} for filtering memories (original value: {original_read_mode})")
        
        # Get session ID based on session_specific flag
        if session_specific:
            # Use the session ID from context if available
            if hasattr(ctx, 'deps') and ctx.deps is not None and ctx.deps:
                session_id = ctx.deps.get("session_id")
            # Otherwise, session_id remains as set above (None for fallback case)
        else:
            # If not session_specific, set session_id to None to ignore session filtering
            session_id = None
            
        logger.info(f"Reading memory with filters: memory_id={memory_id}, name={name}, read_mode={read_mode}, list_all={list_all}, session_specific={session_specific}")
        logger.info(f"Context: agent_id={agent_id} (original: {agent_id_raw if 'agent_id_raw' in locals() else 'unknown'}), user_id={user_id}, session_id={session_id}")
        
        # Single memory lookup by ID
        if memory_id:
            try:
                # Validate UUID format
                memory_uuid = UUID(memory_id)
            except ValueError:
                return {"success": False, "message": f"Invalid memory ID format: {memory_id}"}
                
            # Use the repository pattern to get memory by ID
            memory_obj = get_memory(memory_uuid)
            
            if not memory_obj:
                if read_mode:
                    # Use the original read_mode for user-friendly messages
                    display_read_mode = original_read_mode or read_mode
                    return {"success": False, "message": f"Memory with ID {memory_id} and read_mode {display_read_mode} not found"}
                else:
                    return {"success": False, "message": f"Memory with ID {memory_id} not found"}
            
            # Check if read_mode matches (if specified)
            if read_mode and memory_obj.read_mode != read_mode:
                display_read_mode = original_read_mode or read_mode
                return {"success": False, "message": f"Memory with ID {memory_id} exists but does not have read_mode {display_read_mode}"}
                
            # Verify that the agent has permission to access this memory
            memory_agent_id = memory_obj.agent_id
            memory_user_id = memory_obj.user_id
            
            # Conditions for memory access (in order of hierarchy):
            # 1. Agent+User+Session memories - personalized to the current session
            # 2. Agent+User memories - personalized for a specific user with a specific agent
            # 3. Agent-specific memories (global) - accessible to all users of a specific agent (user_id is NULL)
            # Note: Records where both agent_id and user_id are NULL are considered invalid
            
            memory_session_id = memory_obj.session_id
            can_access = False
            
            # Check if this is an Agent+User+Session memory
            if (memory_agent_id is not None and agent_id is not None and str(memory_agent_id) == str(agent_id) and
                memory_user_id is not None and user_id is not None and str(memory_user_id) == str(user_id) and
                memory_session_id is not None and session_id is not None and str(memory_session_id) == str(session_id)):
                can_access = True
                logger.info(f"Access granted: memory {memory_id} belongs to session {session_id} with agent {agent_id} and user {user_id}")
                
            # Check if this is an Agent+User memory
            elif (memory_agent_id is not None and agent_id is not None and str(memory_agent_id) == str(agent_id) and
                  memory_user_id is not None and user_id is not None and str(memory_user_id) == str(user_id) and
                  memory_session_id is None):
                can_access = True
                logger.info(f"Access granted: memory {memory_id} belongs to both agent {agent_id} and user {user_id}")
                
            # Check if this is an Agent-specific global memory (accessible to all users of this agent)
            elif (memory_agent_id is not None and agent_id is not None and str(memory_agent_id) == str(agent_id) and
                  memory_user_id is None):
                can_access = True
                logger.info(f"Access granted: memory {memory_id} is a global memory for agent {agent_id}")
            
            if not can_access:
                return {"success": False, "message": f"Memory with ID {memory_id} is not accessible to this agent/user"}
            
            # Normalize read_mode in the response for consistency
            memory_obj_dict = memory_obj.model_dump()
            if memory_obj_dict.get("read_mode") == "tool":
                memory_obj_dict["read_mode"] = "tool_calling"
            
            # Clean and format the memory object for return
            cleaned_memory = clean_memory_object(memory_obj_dict, include_content=True)
            
            return {
                "success": True,
                "memory": cleaned_memory
            }

        # If name is provided, look up by name or partial match
        elif name:
            # Implement name lookup using the repository pattern
            memories = repo_list_memories(
                agent_id=agent_id,
                user_id=user_id,
                session_id=session_id,
                read_mode=read_mode,
                name_pattern=name
            )
            
            if not memories:
                return {
                    "success": True,
                    "memories": [],
                    "count": 0,
                    "message": f"No memories found matching name '{name}'"
                }
                
            # Convert memories to dictionary format
            memory_list = []
            for memory_obj in memories:
                memory_dict = memory_obj.model_dump()
                # Normalize read_mode for consistency
                if memory_dict.get("read_mode") == "tool":
                    memory_dict["read_mode"] = "tool_calling"
                    
                # Clean and format the memory
                cleaned_memory = clean_memory_object(memory_dict, include_content=True)
                memory_list.append(cleaned_memory)
                
            return {
                "success": True,
                "memories": memory_list,
                "count": len(memory_list),
                "message": f"Found {len(memory_list)} memories matching name '{name}'"
            }
            
        # If list_all is True, return all available memories for this agent/user
        elif list_all:
            # Use consistent agent_id for sofia_agent
            if agent_id_raw == "sofia_agent":
                agent_id = 3  # Use consistent ID 3 for sofia_agent
                logger.info(f"Using consistent agent_id={agent_id} for sofia_agent")
            
            # Construct a query with proper access controls
            query = """
                SELECT id, name, description, created_at, updated_at, 
                       read_mode, access, session_id, user_id, agent_id, metadata
                FROM memories 
                WHERE (
                      -- Agent-specific global memories (accessible to all users of this agent)
                      (agent_id = %s AND user_id IS NULL)
                      
                      -- Agent + User memories (personalized agent)
                      OR (agent_id = %s AND user_id = %s AND session_id IS NULL)
                      
                      -- Agent + User + Session memories (personalized session)
                      OR (agent_id = %s AND user_id = %s AND session_id = %s)
                )
            """
            
            # Add read_mode filter if provided
            params = [agent_id, agent_id, user_id, agent_id, user_id, session_id]
            if read_mode is not None:
                # Ensure the read_mode filter is explicitly part of the WHERE clause
                query += " AND read_mode = %s"
                params.append(read_mode)
                
            query += " ORDER BY name ASC"
            
            # Execute the query with parameters
            logger.info(f"Executing list_all query with params: {params}")
            logger.info(f"SQL Query: {query}")
            
            result = execute_query(query, params)
            
            # Log detailed information about the query result to debug filtering
            if isinstance(result, list):
                logger.info(f"Query returned {len(result)} results as a list")
                if read_mode:
                    # Count how many items actually have the expected read_mode
                    matching_count = sum(1 for r in result if r.get("read_mode") == read_mode)
                    logger.info(f"Of these, {matching_count} actually have read_mode={read_mode}")
            else:
                rows = result.get('rows', [])
                logger.info(f"Query returned {len(rows)} results as dict.rows")
                if read_mode and rows:
                    # Count how many items actually have the expected read_mode
                    matching_count = sum(1 for r in rows if r.get("read_mode") == read_mode)
                    logger.info(f"Of these, {matching_count} actually have read_mode={read_mode}")
            
            # Handle case where result is a list (DB rows) or dict with 'rows' key
            if isinstance(result, list):
                rows = result
            else:
                rows = result.get('rows', [])
                
            # If no memories found, return empty list with success
            if not rows:
                if read_mode:
                    # Display user-friendly read_mode value in messages
                    display_read_mode = original_read_mode or read_mode
                    logger.warning(f"No memories found for agent_id={agent_id}, user_id={user_id}, session_id={session_id}, read_mode={display_read_mode}")
                    return {
                        "success": True,
                        "message": f"No memories with read_mode={display_read_mode} available for this agent/user",
                        "count": 0,
                        "memories": []
                    }
                else:
                    logger.warning(f"No memories found for agent_id={agent_id}, user_id={user_id}, session_id={session_id}")
                    return {
                        "success": True,
                        "message": "No memories available for this agent/user",
                        "count": 0,
                        "memories": []
                    }
            
            # Additional validation for read_mode filter
            if read_mode and rows:
                # Double-check that all rows match the expected read_mode
                for row in rows:
                    if row.get("read_mode") != read_mode:
                        logger.warning(f"Found memory with mismatched read_mode: expected {read_mode}, got {row.get('read_mode')} for memory {row.get('name')}")
            
            # Normalize read_mode in all results for consistency
            for memory in rows:
                if memory.get("read_mode") == "tool":
                    memory["read_mode"] = "tool_calling"
                
            # Return list of memories without content
            memories = []
            for memory in rows:
                cleaned_memory = clean_memory_object(memory, include_content=False)
                memories.append(cleaned_memory)
            
            if read_mode:
                # Display user-friendly read_mode value in messages
                display_read_mode = original_read_mode or read_mode
                return {
                    "success": True,
                    "message": f"Found {len(memories)} memories with read_mode={display_read_mode} available to this agent/user",
                    "count": len(memories),
                    "memories": memories
                }
            else:
                return {
                    "success": True,
                    "message": f"Found {len(memories)} memories available to this agent/user",
                    "count": len(memories),
                    "memories": memories
                }
            
        # If no specific lookup criteria provided
        else:
            return {
                "success": False,
                "message": "Must provide memory_id, name, or set list_all=True to retrieve memories"
            }
            
    except Exception as e:
        logger.error(f"Error reading memory: {str(e)}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def map_agent_id(agent_name):
    """Map agent name to numeric ID.
    
    Args:
        agent_name: Agent name
        
    Returns:
        Numeric agent ID
    """
    # Try to convert to int if it's a string number
    if isinstance(agent_name, int):
        return agent_name
    
    try:
        return int(agent_name)
    except (ValueError, TypeError):
        # Query the database to get the ID
        query = "SELECT id FROM agents WHERE name = %s"
        result = execute_query(query, [agent_name])
        
        if result and isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            return result['rows'][0].get('id')
        elif isinstance(result, list) and len(result) > 0:
            return result[0].get('id')
        else:
            logger.warning(f"Agent ID not found for name: {agent_name}, using default ID 3")
            return 3  # Default to sofia_agent ID 3 as fallback
