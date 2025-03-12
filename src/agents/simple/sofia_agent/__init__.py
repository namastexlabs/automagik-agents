from typing import Dict, Optional
from src.agents.simple.sofia_agent.agent import SofiaAgent
from src.agents.models import initialize_agent
from src.config import settings

def create_sofia_agent(config: Optional[Dict[str, str]] = None) -> SofiaAgent:
    """Create and initialize a SofiaAgent instance.
    
    Args:
        config: Optional configuration override
        
    Returns:
        Initialized SofiaAgent instance
    """
    default_config = {
        "model": "openai:gpt-4o-mini",  # Specific model for SofiaAgent
        "retries": 3
    }
    
    if config:
        default_config.update(config)
    
    return initialize_agent(SofiaAgent, default_config)

# Default instance
default_agent = create_sofia_agent()
