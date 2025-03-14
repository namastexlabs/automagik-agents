from typing import Dict, Optional
from src.agents.simple.flashinho_agent.agent import FlashinhoAgent
from src.agents.models import initialize_agent
from src.config import settings

def create_flashinho_agent(config: Optional[Dict[str, str]] = None) -> FlashinhoAgent:
    """Create and initialize a FlashinhoAgent instance.
    
    Args:
        config: Optional configuration override
        
    Returns:
        Initialized FlashinhoAgent instance
    """
    default_config = {
        "model": "openai:gpt-4o-mini",  # Specific model for FlashinhoAgent
        "retries": 3
    }
    
    if config:
        default_config.update(config)
    
    return initialize_agent(FlashinhoAgent, default_config)

# Default instance
default_agent = create_flashinho_agent()
