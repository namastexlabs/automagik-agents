from typing import Dict
from pydantic_ai import Agent

from src.agents.models.base_agent import BaseAgent
from src.agents.notion_agent.prompts import NOTION_AGENT_PROMPT
from src.tools.notion_tools import NotionTools

class NotionAgent(BaseAgent):
    """Notion-specific agent implementation."""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the Notion agent with configuration."""
        super().__init__(config, NOTION_AGENT_PROMPT)
        
        # Ensure Notion token is provided
        if 'notion_token' not in config:
            raise ValueError("Notion token is required for NotionAgent")

    def initialize_agent(self) -> Agent:
        """Initialize the Notion agent with configuration."""
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register tools with the agent."""
        # Register Notion tools
        notion_tools = NotionTools()
        for tool_func in notion_tools.tools:
            self.agent.tool(tool_func)
