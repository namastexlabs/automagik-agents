from typing import Dict, Optional
from src.agents.discord_agent.agent import DiscordAgent
from src.agents.models import initialize_agent
from src.config import settings
import logging

logger = logging.getLogger(__name__)

def create_discord_agent(config: Optional[Dict[str, str]] = None) -> Optional[DiscordAgent]:
    """Create and initialize a DiscordAgent instance.
    
    Args:
        config: Optional configuration override
        
    Returns:
        Initialized DiscordAgent instance
        
    Raises:
        ValueError: If Discord bot token is not provided in config or settings
    """
    default_config = {
        "model": settings.OPENAI_MODEL,
        "retries": 3
    }
    
    # Add Discord bot token from settings if available
    if settings.DISCORD_BOT_TOKEN:
        default_config["discord_bot_token"] = settings.DISCORD_BOT_TOKEN
        logger.info("Discord bot token found in settings.")
    else:
        logger.warning("Discord bot token not found in settings.")
        return None
    
    if config:
        default_config.update(config)
    
    try:
        agent = initialize_agent(DiscordAgent, default_config)
        logger.info("Discord agent created successfully.")
        return agent
    except Exception as e:
        logger.exception(f"Error creating Discord agent: {str(e)}")
        return None

# Default instance (only created if Discord bot token is available)
default_agent = create_discord_agent() if settings.DISCORD_BOT_TOKEN else None

# Export the functions and default agent for use in other modules
__all__ = ['create_discord_agent', 'default_agent']
