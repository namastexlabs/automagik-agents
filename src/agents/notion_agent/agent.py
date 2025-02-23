import logging
from typing import Dict, List, Any, Tuple, Optional

from src.agents.models.base_agent import BaseAgent, Deps, ToolCall, ToolOutput
from src.agents.notion_agent.prompts import NOTION_AGENT_PROMPT
from src.tools.notion_tools import NotionTools
from src.agents.models.agent import AgentBaseResponse
from pydantic_ai.result import RunResult

class NotionAgentError(Exception):
    """Custom exception for NotionAgent errors."""
    pass

class NotionAgent(BaseAgent):
    def __init__(self, config: Dict[str, str]):
        super().__init__(config, NOTION_AGENT_PROMPT)

    def get_assistant_name(self) -> str:
        return "Notion Agent"

    def get_deps_type(self):
        return Deps

    def register_tools(self):
        """Register tools with the agent."""
        # Register datetime tools
        from src.tools.datetime_tools import get_current_date, get_current_time
        self.agent.tool(get_current_date)
        self.agent.tool(get_current_time)
        
        # Register Notion tools
        notion_tools = NotionTools()
        for tool_func in notion_tools.tools:
            self.agent.tool(tool_func)

    @staticmethod
    def format_tool_info(info: Dict[str, Any]) -> str:
        """Format tool call or output information for logging."""
        return ", ".join(f"{k}: {v}" for k, v in info.items())
