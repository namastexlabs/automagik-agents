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

    async def process_message(self, user_message: str) -> AgentBaseResponse:
        self.message_history.add(user_message)
        
        logging.info(f"Processing user message: {user_message}")

        try:
            result = await self.agent.run(
                user_message,
                deps=self.deps,
                message_history=self.message_history.messages
            )
            logging.info(f"Agent run completed. Result type: {type(result)}")
        except Exception as e:
            error_msg = f"Error running agent: {str(e)}"
            logging.error(error_msg)
            return AgentBaseResponse.from_agent_response(
                message="An error occurred while processing your request.",
                history=self.message_history,
                error=error_msg,
                tool_calls=[],
                tool_outputs=[]
            )
        
        # Get the final response text
        response_text = result.data
        logging.info(f"Response text: {response_text[:100]}...")  # Log first 100 characters

        # Extract tool calls and outputs from the result
        tool_calls, tool_outputs = self.extract_tool_calls_and_outputs(result)

        logging.info(f"Captured {len(tool_calls)} tool calls and {len(tool_outputs)} tool outputs")
        
        self.message_history.add_response(response_text)
        
        response = AgentBaseResponse.from_agent_response(
            message=response_text,
            history=self.message_history,
            error=None,
            tool_calls=[tc.__dict__ for tc in tool_calls],
            tool_outputs=[to.__dict__ for to in tool_outputs]
        )
        
        logging.info(f"Returning AgentBaseResponse with {len(response.tool_calls)} tool calls and {len(response.tool_outputs)} tool outputs")
        
        return response
