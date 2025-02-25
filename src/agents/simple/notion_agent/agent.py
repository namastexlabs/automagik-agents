from typing import Dict, List, Optional
import logging
from pydantic_ai import Agent

from src.agents.models.base_agent import BaseAgent
from src.agents.simple.notion_agent.prompts import NOTION_AGENT_PROMPT
from src.tools.notion_tools import NotionTools

logger = logging.getLogger(__name__)

class NotionAgent(BaseAgent):
    """Notion agent implementation for interacting with Notion API."""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the notion agent with configuration."""
        # Validate Notion token
        if "notion_token" not in config:
            raise ValueError("Notion token is required for NotionAgent")
            
        # Store the token for later use by tools
        self.notion_token = config["notion_token"]
        
        super().__init__(config, NOTION_AGENT_PROMPT)

    def initialize_agent(self) -> Agent:
        """Initialize the notion agent with configuration."""
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register Notion-specific tools with the agent."""
        # Initialize the NotionTools class
        notion_tools = NotionTools()
        
        # Register all Notion tools
        for tool in notion_tools.tools:
            self.agent.tool(tool)
