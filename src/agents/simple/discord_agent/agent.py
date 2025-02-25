from typing import Dict, List, Optional
import logging
from pydantic_ai import Agent

from src.agents.models.base_agent import BaseAgent
from src.agents.simple.discord_agent.prompts import DISCORD_AGENT_PROMPT
from src.tools.discord_tools import DiscordTools

logger = logging.getLogger(__name__)

class DiscordAgent(BaseAgent):
    """Discord agent implementation for interacting with Discord API."""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the discord agent with configuration."""
        # Validate Discord token
        if "discord_bot_token" not in config:
            raise ValueError("Discord bot token is required for DiscordAgent")
            
        # Store the token for later use by tools
        self.discord_bot_token = config["discord_bot_token"]
        
        super().__init__(config, DISCORD_AGENT_PROMPT)

    def initialize_agent(self) -> Agent:
        """Initialize the discord agent with configuration."""
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register Discord-specific tools with the agent."""
        # Initialize Discord tools with the token
        discord_tools = DiscordTools(self.discord_bot_token)
        
        # Register all Discord tools
        for tool in discord_tools.tools:
            self.agent.tool(tool)

    def post_init(self):
        """Post-initialization tasks."""
        super().post_init()

    @property
    def discord_bot_token(self):
        return self._discord_bot_token

    @discord_bot_token.setter
    def discord_bot_token(self, value):
        self._discord_bot_token = value
