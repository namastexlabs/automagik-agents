from typing import Dict
from pydantic_ai import Agent

from src.agents.models.base_agent import BaseAgent
from src.agents.discord_agent.prompts import DISCORD_AGENT_PROMPT
from src.tools.discord_tools import DiscordTools

class DiscordAgent(BaseAgent):
    """Discord-specific agent implementation."""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the Discord agent with configuration."""
        # Ensure Discord bot token is provided
        if 'discord_bot_token' not in config:
            raise ValueError("Discord bot token is required for DiscordAgent")
        # Set the discord bot token before calling the base __init__
        self._discord_bot_token = config['discord_bot_token']

        super().__init__(config, DISCORD_AGENT_PROMPT)

    def initialize_agent(self) -> Agent:
        """Initialize the Discord agent with configuration."""
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register tools with the agent."""
        # Register Discord tools
        discord_tools = DiscordTools(self.discord_bot_token)
        for tool_func in discord_tools.tools:
            self.agent.tool(tool_func)

    def post_init(self):
        """Post-initialization tasks."""
        super().post_init()

    @property
    def discord_bot_token(self):
        return self._discord_bot_token

    @discord_bot_token.setter
    def discord_bot_token(self, value):
        self._discord_bot_token = value
