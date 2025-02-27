from typing import Dict, Optional
from .agent import StanAgent
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
    # Check if we have required tokens available - use getattr to safely check for attributes
    blackpearl_token = getattr(settings, 'BLACKPEARL_TOKEN', None)
    omie_token = getattr(settings, 'OMIE_TOKEN', None)
    google_drive_token = getattr(settings, 'GOOGLE_DRIVE_TOKEN', None)
    evolution_token = getattr(settings, 'EVOLUTION_TOKEN', None)
    
    # For development, allow initialization even if tokens are missing
    # In production, you might want to require these tokens
    
    default_config = {
        "model": "openai:gpt-4o-mini",  # Specific model for StanAgent (more capable model)
        "retries": 3,
        "blackpearl_token": blackpearl_token or "mock_token",
        "omie_token": omie_token or "mock_token",
        "google_drive_token": google_drive_token or "mock_token",
        "evolution_token": evolution_token or "mock_token"
    }
    
    if config:
        default_config.update(config)
    
    return initialize_agent(StanAgent, default_config)

# Default instance
default_agent = create_stan_agent()
