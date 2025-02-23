from typing import Dict, Type, Optional
from src.agents.models.base_agent import BaseAgent

def initialize_agent(agent_class: Type[BaseAgent], config: Optional[Dict[str, str]] = None) -> BaseAgent:
    """Initialize an agent with configuration.
    
    Args:
        agent_class: The agent class to initialize
        config: Optional configuration override
        
    Returns:
        Initialized agent instance
    """
    if config is None:
        config = {}
    return agent_class(config) 