from typing import Dict, Optional
from src.agents.simple.stan_agent.agent import StanAgent
from src.agents.models import initialize_agent
from src.config import settings

# Only initialize if required tokens are available
def create_stan_agent(config: Optional[Dict[str, str]] = None) -> Optional[StanAgent]:
    """Create and initialize a StanAgent instance if tokens are available.
    
    Args:
        config: Optional configuration override
        
    Returns:
        Initialized StanAgent instance or None if tokens not available
    """
    # Check if we have required tokens available
    if not settings.BLACKPEARL_TOKEN or not settings.OMIE_TOKEN or not settings.GOOGLE_DRIVE_TOKEN or not settings.EVOLUTION_TOKEN:
        return None
        
    default_config = {
        "model": "openai:gpt-4o-mini",  # Specific model for StanAgent (more capable model)
        "retries": 3,
        "blackpearl_token": settings.BLACKPEARL_TOKEN,
        "omie_token": settings.OMIE_TOKEN,
        "google_drive_token": settings.GOOGLE_DRIVE_TOKEN,
        "evolution_token": settings.EVOLUTION_TOKEN
    }
    
    if config:
        default_config.update(config)
    
    return initialize_agent(StanAgent, default_config)

# Default instance
default_agent = create_stan_agent()
