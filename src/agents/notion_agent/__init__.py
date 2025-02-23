from typing import Dict, Optional
from src.agents.notion_agent.agent import NotionAgent
from src.agents.models import initialize_agent
from src.config import settings

def create_notion_agent(config: Optional[Dict[str, str]] = None) -> NotionAgent:
    """Create and initialize a NotionAgent instance.
    
    Args:
        config: Optional configuration override
        
    Returns:
        Initialized NotionAgent instance
        
    Raises:
        ValueError: If Notion token is not provided in config or settings
    """
    default_config = {
        "model": settings.OPENAI_MODEL,
        "retries": 3
    }
    
    # Add Notion token from settings if available
    if settings.NOTION_TOKEN:
        default_config["notion_token"] = settings.NOTION_TOKEN
    
    if config:
        default_config.update(config)
    
    return initialize_agent(NotionAgent, default_config)

# Default instance (only created if Notion token is available)
default_agent = create_notion_agent() if settings.NOTION_TOKEN else None
