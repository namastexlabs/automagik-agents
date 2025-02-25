from typing import Dict, Optional
from src.agents.simple.simple_agent.agent import SimpleAgent
from src.agents.models import initialize_agent
from src.config import settings

def create_simple_agent(config: Optional[Dict[str, str]] = None) -> SimpleAgent:
    """Create and initialize a SimpleAgent instance.
    
    Args:
        config: Optional configuration override
        
    Returns:
        Initialized SimpleAgent instance
    """
    default_config = {
        "model": "openai:gpt-4o-mini",  # Specific model for SimpleAgent
        "retries": 3
    }
    
    if config:
        default_config.update(config)
    
    return initialize_agent(SimpleAgent, default_config)

# Default instance
default_agent = create_simple_agent()
