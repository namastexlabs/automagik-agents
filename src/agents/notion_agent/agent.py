import logging
from dataclasses import dataclass
from typing import Dict

from pydantic_ai import Agent
from src.agents.models.agent import AgentBaseResponse
from src.agents.notion_agent.prompts import NOTION_AGENT_PROMPT
from src.memory.message_history import MessageHistory
from src.tools.notion_tools import NotionTools

@dataclass
class Deps:
    # Add any dependencies your agent might need
    pass

class NotionAgent:
    def __init__(self, config: Dict[str, str]):
        self.agent = Agent(
            'openai:gpt-4o-mini',
            system_prompt=NOTION_AGENT_PROMPT,
            deps_type=Deps
        )
        self.deps = Deps()
        self.message_history = MessageHistory(system_prompt=NOTION_AGENT_PROMPT)
        self.register_tools()

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

    async def process_message(self, user_message: str) -> AgentBaseResponse:
        self.message_history.add(user_message)
        
        result = await self.agent.run(
            user_message,
            deps=self.deps,
            message_history=self.message_history.messages
        )
        
        # Get the final response text
        response_text = result.data
        
        # Get tool calls and outputs from the result
        tool_calls = []
        tool_outputs = []

        logging.info(result)
        # Extract tool information from all nodes in the result
        if hasattr(result, 'nodes'):
            for node in result.nodes:
                if hasattr(node, 'tool_calls'):
                    tool_calls.extend(node.tool_calls)
                if hasattr(node, 'tool_outputs'):
                    tool_outputs.extend(node.tool_outputs)
                # Also check model responses within nodes
                if hasattr(node, 'model_response'):
                    if hasattr(node.model_response, 'tool_calls'):
                        tool_calls.extend(node.model_response.tool_calls)
                    if hasattr(node.model_response, 'tool_outputs'):
                        tool_outputs.extend(node.model_response.tool_outputs)
        
        self.message_history.add_response(response_text)
        
        return AgentBaseResponse.from_agent_response(
            message=response_text,
            history=self.message_history,
            error=None,
            tool_calls=tool_calls,
            tool_outputs=tool_outputs
        )
