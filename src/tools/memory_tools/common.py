"""Common utilities for memory tools.

Contains shared functionality for memory tools including helper functions and utilities.
"""

from typing import Dict, Any, Optional
import uuid
import json
import logging
from datetime import datetime
from uuid import UUID

logger = logging.getLogger(__name__)

def clean_memory_object(memory, include_content=False):
    """Helper function to clean memory objects for agent consumption.
    
    Removes technical fields and ensures consistent output format.
    
    Args:
        memory: The memory object to clean
        include_content: Whether to include the content field (for single memory vs list)
        
    Returns:
        A cleaned memory object with only the desired fields
    """
    if not memory or not isinstance(memory, dict):
        return {}
        
    # Create a clean memory with only the fields we want to expose
    clean_memory = {}
    
    # Add standard fields
    if memory.get("id") is not None:
        clean_memory["id"] = memory.get("id")
    if memory.get("name") is not None:
        clean_memory["name"] = memory.get("name")
    if memory.get("description") is not None:
        clean_memory["description"] = memory.get("description")
    
    # Add content only for single memory retrieval
    if include_content and memory.get("content") is not None:
        content = memory.get("content")
        
        # Try to parse content as JSON if it looks like a dictionary
        if isinstance(content, str) and content.strip().startswith('{') and content.strip().endswith('}'):
            try:
                parsed_content = json.loads(content)
                # If successfully parsed as a dictionary, use the parsed version
                if isinstance(parsed_content, dict):
                    clean_memory["content"] = parsed_content
                    # Add a flag to indicate this was originally stored as JSON
                    clean_memory["content_type"] = "json"
                else:
                    clean_memory["content"] = content
            except json.JSONDecodeError:
                # If parsing fails, use the original string content
                clean_memory["content"] = content
        else:
            clean_memory["content"] = content
        
    # Remove any None values to keep output clean
    return {k: v for k, v in clean_memory.items() if v is not None}

def map_agent_id(agent_id):
    """Map agent ID from name to numeric ID if needed.
    
    Args:
        agent_id: The agent ID, which could be a name or numeric ID.
        
    Returns:
        The numeric agent ID if possible, otherwise the original value.
    """
    # If agent_id is already an integer or a string that can be converted to an integer, return it
    if isinstance(agent_id, int) or (isinstance(agent_id, str) and agent_id.isdigit()):
        return int(agent_id) if isinstance(agent_id, str) else agent_id
        
    # Map known agent names to their numeric IDs
    agent_map = {
        "simple_agent": 2,
        "sofia_agent": 3,
    }
    
    # If the agent_id is in our map, return the numeric ID
    if agent_id in agent_map:
        return agent_map[agent_id]
        
    # Otherwise, return the original value
    return agent_id
