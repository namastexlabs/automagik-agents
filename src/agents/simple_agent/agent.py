from typing import Dict
from pydantic_ai import Agent

from src.agents.models.base_agent import BaseAgent
from src.agents.simple_agent.prompts import SIMPLE_AGENT_PROMPT

class SimpleAgent(BaseAgent):
    """Simple agent implementation for basic chat functionality."""
    
    def __init__(self, config: Dict[str, str]):
        super().__init__(config, SIMPLE_AGENT_PROMPT)

    def initialize_agent(self) -> Agent:
        """Initialize the simple agent with default configuration."""
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register tools with the agent."""
        from src.tools.datetime_tools import get_current_date, get_current_time
        self.agent.tool(get_current_date)
        self.agent.tool(get_current_time)
