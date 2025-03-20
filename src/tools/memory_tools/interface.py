from typing import Dict, Any, Optional, Callable
import logging
import re
from functools import wraps

logger = logging.getLogger(__name__)

def invalidate_memory_cache(func: Callable) -> Callable:
    """Decorator that invalidates the memory cache after the function is called.
    
    This ensures that any memory updates are immediately reflected in
    subsequent system prompt generation.
    
    Args:
        func: The function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Call the original function
        result = await func(*args, **kwargs)
        
        # Get the memory provider
        from src.tools.memory_tools.provider import get_memory_provider_for_agent
        
        # Try to extract agent_id from args/kwargs
        agent_id = None
        
        # Check if first argument might be a context with dependencies
        if args and hasattr(args[0], 'deps'):
            deps = args[0].deps
            if hasattr(deps, '_agent_id_numeric'):
                agent_id = deps._agent_id_numeric
        
        # Check if agent_id is in kwargs
        if 'agent_id' in kwargs:
            agent_id = kwargs['agent_id']
        
        # If we found an agent_id, invalidate its cache
        if agent_id:
            provider = get_memory_provider_for_agent(agent_id)
            if provider:
                provider.invalidate_cache()
                logger.debug(f"Invalidated memory cache for agent {agent_id}")
            else:
                logger.warning(f"No memory provider found for agent {agent_id}")
        else:
            logger.warning(f"Could not determine agent_id for cache invalidation in {func.__name__}")
        
        return result
    
    return wrapper

def validate_memory_name(name: str) -> bool:
    """Validate that a memory name contains only allowed characters.
    
    Args:
        name: Memory name to validate
        
    Returns:
        True if valid, False otherwise
    """
    return bool(re.match(r'^[a-zA-Z0-9_]+$', name))

def format_memory_content(content: Any) -> str:
    """Format memory content for storage.
    
    Args:
        content: Memory content to format
        
    Returns:
        Formatted string representation
    """
    if isinstance(content, str):
        return content
    
    # For other types, convert to string representation
    try:
        import json
        return json.dumps(content)
    except:
        return str(content) 