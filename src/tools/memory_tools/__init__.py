"""Memory tools for Automagik Agents.

Provides tools for reading and writing memories for agents, implementing the pydantic-ai tool interface.
These tools allow agents to store and retrieve information across conversations and sessions.

This package has been split into separate modules for better organization:
- read.py: Tools for reading memories from the database
- create.py: Tools for creating new memories
- update.py: Tools for updating existing memories
- common.py: Shared utilities and helper functions
"""

# Import all the tools for easier access
from src.tools.memory_tools.read import (
    read_memory,
    get_read_memory_description,
    MemoryReadResult
)

from src.tools.memory_tools.create import (
    create_memory,
    get_create_memory_description,
    MemoryCreateResponse
)

from src.tools.memory_tools.update import (
    update_memory,
    get_update_memory_description,
    MemoryUpdateResponse
)

from src.tools.memory_tools.common import (
    clean_memory_object,
    map_agent_id
)

# For backwards compatibility (to be removed in future versions)
def write_memory(*args, **kwargs):
    """Deprecated: Use create_memory or update_memory instead.
    
    This function is maintained for backward compatibility only.
    It will decide whether to create or update a memory based on the presence of memory_id.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("write_memory is deprecated - use create_memory or update_memory instead")
    
    # Check if memory_id exists in kwargs
    if 'memory_id' in kwargs and kwargs['memory_id'] is not None:
        # Update existing memory
        # Re-map parameters to match update_memory's signature
        # update_memory expects: content, memory_id, name
        if len(args) >= 3:
            return update_memory(args[0], args[2], memory_id=kwargs.get('memory_id'))
        else:
            return update_memory(kwargs.get('ctx'), kwargs.get('content', ''), 
                              memory_id=kwargs.get('memory_id'))
    else:
        # Create new memory
        # create_memory expects: ctx, name, content, description, read_mode, access, metadata
        return create_memory(*args, **kwargs)

# Expose only these functions at the package level
__all__ = [
    'read_memory',
    'create_memory',
    'update_memory',
    'write_memory',  # For backwards compatibility
    'get_read_memory_description',
    'get_create_memory_description',
    'get_update_memory_description',
    'MemoryReadResult',
    'MemoryCreateResponse',
    'MemoryUpdateResponse',
    'clean_memory_object',
    'map_agent_id'
]
