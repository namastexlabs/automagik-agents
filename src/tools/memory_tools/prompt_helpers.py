from typing import Dict, Any, List, Callable, Optional
import logging
from datetime import datetime
from pydantic_ai import Agent

logger = logging.getLogger(__name__)

def register_memory_prompts(agent: Agent, agent_id: int, memory_names: List[str], 
                           prefix: Optional[str] = None, 
                           templates: Optional[Dict[str, str]] = None) -> None:
    """Register memory-based system prompt functions with an agent.
    
    This function creates and registers system prompt functions for each
    specified memory name, allowing dynamic memory injection at runtime.
    
    Args:
        agent: The pydantic-ai Agent instance
        agent_id: The numeric ID of the agent
        memory_names: List of memory names to create prompt functions for
        prefix: Optional prefix to add to all memories (e.g., "user_")
        templates: Optional dictionary mapping memory names to custom templates
    """
    from src.tools.memory_tools.provider import MemoryProvider
    
    # Create a memory provider
    provider = MemoryProvider(agent_id)
    
    # Default template just returns the value
    default_template = "{value}"
    
    # Templates dictionary (use provided or empty dict)
    templates = templates or {}
    
    for name in memory_names:
        # Get the appropriate template
        template = templates.get(name, default_template)
        
        # Create the actual name to use for lookup (with optional prefix)
        lookup_name = f"{prefix}{name}" if prefix else name
        
        # Create the prompt function
        prompt_fn = provider.create_system_prompt_function(lookup_name, template)
        
        # Register with the agent
        agent.system_prompt(prompt_fn)
        
        logger.debug(f"Registered memory prompt for '{lookup_name}' with template: {template}")
    
    logger.info(f"Registered {len(memory_names)} memory-based system prompt functions")

def register_standard_prompts(agent: Agent, agent_id: int) -> None:
    """Register standard system prompt functions for common metadata.
    
    This adds functions for date/time, run ID, and other common information.
    
    Args:
        agent: The pydantic-ai Agent instance
        agent_id: The numeric ID of the agent
    """
    # Add function for current date/time
    @agent.system_prompt
    def add_current_datetime() -> str:
        """Add the current date and time to the system prompt."""
        now = datetime.now()
        return f"The current date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}."
    
    # Add function for run ID
    @agent.system_prompt
    def add_run_id() -> str:
        """Add the agent's run ID to the system prompt."""
        from src.db import get_agent
        
        try:
            agent_record = get_agent(agent_id)
            run_id = getattr(agent_record, 'run_id', 1) or 1
            return f"This is run #{run_id} for this agent."
        except Exception as e:
            logger.error(f"Error getting run ID: {str(e)}")
            return "This is a new conversation with this agent."
    
    logger.info("Registered standard system prompt functions") 