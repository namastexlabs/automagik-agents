from typing import Dict, Optional
from src.agents.simple.notion_agent.agent import NotionAgent
from src.agents.models import initialize_agent
from src.config import settings

# Only initialize if Notion token is available
def create_notion_agent(config: Optional[Dict[str, str]] = None) -> Optional[NotionAgent]:
    """Create and initialize a NotionAgent instance if token is available.
    
    Args:
        config: Optional configuration override
        
    Returns:
        Initialized NotionAgent instance or None if token not available
    """
    # Check if we have Notion token available
    if not settings.NOTION_TOKEN:
        return None
        
    default_config = {
        "model": "openai:gpt-4o-mini",  # Specific model for NotionAgent (more capable model)
        "retries": 3,
        "notion_token": settings.NOTION_TOKEN
    }
    
    if config:
        default_config.update(config)
    
    return initialize_agent(NotionAgent, default_config)

# Default instance
default_agent = create_notion_agent()
