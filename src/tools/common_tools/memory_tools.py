"""Memory tools connector module.

This module provides a bridge to the main memory_tools package
for the SimpleAgent to use.
"""
import logging
from typing import Dict, Any, List, Optional
import uuid

# Import from the main memory_tools package
from src.tools.memory_tools import read_memory, create_memory, update_memory
from pydantic_ai.tools import RunContext

logger = logging.getLogger(__name__)

# Re-export implementations with the expected API for SimpleAgent
async def get_memory_tool(key: str) -> str:
    """Retrieve a memory by key.
    
    Args:
        key: The memory key to retrieve
        
    Returns:
        The memory content as a string, or an error message if not found
    """
    logger.info(f"Getting memory with key: {key}")
    try:
        # Create a simple context with empty deps
        ctx = RunContext({})
        
        # Try to get memory by name
        result = await read_memory(ctx, name=key)
        if "content" in result:
            if isinstance(result["content"], dict):
                return str(result["content"])
            return result["content"]
        return f"Memory with key '{key}' not found"
    except Exception as e:
        logger.error(f"Error getting memory: {str(e)}")
        return f"Error getting memory with key '{key}': {str(e)}"

async def store_memory_tool(key: str, content: str) -> str:
    """Store a memory with the given key.
    
    Args:
        key: The key to store the memory under
        content: The memory content to store
        
    Returns:
        Confirmation message
    """
    logger.info(f"Storing memory with key: {key}")
    try:
        # Create a simple context with empty deps
        ctx = RunContext({})
        
        # Store the memory
        await create_memory(
            ctx, 
            name=key, 
            content=content,
            description=f"Memory created by SimpleAgent"
        )
        return f"Memory stored with key '{key}'"
    except Exception as e:
        logger.error(f"Error storing memory: {str(e)}")
        return f"Error storing memory with key '{key}': {str(e)}"

async def list_memories_tool(prefix: Optional[str] = None) -> str:
    """List available memories, optionally filtered by prefix.
    
    Args:
        prefix: Optional prefix to filter memory keys
        
    Returns:
        List of memory keys as a string
    """
    try:
        # Create a simple context with empty deps
        ctx = RunContext({})
        
        # Use read_memory with list_all flag
        result = await read_memory(ctx, list_all=True)
        
        # Filter by prefix if needed
        memories = []
        if "memories" in result and isinstance(result["memories"], list):
            for memory in result["memories"]:
                if "name" in memory:
                    name = memory["name"]
                    if not prefix or name.startswith(prefix):
                        memories.append(name)
        
        if not memories:
            return "No memories found"
        
        return "\n".join(memories)
    except Exception as e:
        logger.error(f"Error listing memories: {str(e)}")
        return f"Error listing memories: {str(e)}" 