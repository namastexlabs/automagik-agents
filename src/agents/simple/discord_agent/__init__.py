from typing import Dict, Optional
from src.agents.simple.discord_agent.agent import DiscordAgent
from src.agents.models import initialize_agent
from src.config import settings
import logging

logger = logging.getLogger(__name__)

def create_discord_agent(config: Optional[Dict[str, str]] = None) -> Optional[DiscordAgent]:
    """Create and initialize a DiscordAgent instance if token is available.
    
    Args:
        config: Optional configuration override
        
    Returns:
        Initialized DiscordAgent instance or None if token not available
    """
    # Check if Discord token is available
    if not settings.DISCORD_BOT_TOKEN:
        return None
    
    default_config = {
        "model": "openai:gpt-4o-mini",  # Specific model for DiscordAgent (more capable model)
        "retries": 3,
        "discord_bot_token": settings.DISCORD_BOT_TOKEN
    }
    
    if config:
        default_config.update(config)
    
    return initialize_agent(DiscordAgent, default_config)

# Default instance
default_agent = create_discord_agent()

# Export the functions and default agent for use in other modules
__all__ = ['create_discord_agent', 'default_agent']
