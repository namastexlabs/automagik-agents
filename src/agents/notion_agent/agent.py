import logging
from dataclasses import dataclass
from typing import Dict, List, Any, Tuple, Optional

from pydantic_ai import Agent
from pydantic_ai.result import RunResult
from src.agents.models.agent import AgentBaseResponse
from src.agents.notion_agent.prompts import NOTION_AGENT_PROMPT
from src.memory.message_history import MessageHistory
from src.tools.notion_tools import NotionTools

class NotionAgentError(Exception):
    """Custom exception for NotionAgent errors."""
    pass

@dataclass
class Deps:
    # Add any dependencies your agent might need
    pass

@dataclass
class ToolCall:
    tool_name: str
    args: str
    tool_call_id: str

@dataclass
class ToolOutput:
    tool_name: str
    tool_call_id: str
    content: Any

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

    @staticmethod
    def format_tool_info(info: Dict[str, Any]) -> str:
        """Format tool call or output information for logging."""
        return ", ".join(f"{k}: {v}" for k, v in info.items())

    def extract_tool_calls_and_outputs(self, result: RunResult) -> Tuple[List[ToolCall], List[ToolOutput]]:
        tool_calls: List[ToolCall] = []
        tool_outputs: List[ToolOutput] = []
        current_tool_call: Optional[ToolCall] = None

        for message in result._all_messages:
            if hasattr(message, 'parts'):
                for part in message.parts:
                    if hasattr(part, 'part_kind'):
                        if part.part_kind == 'tool-call':
                            current_tool_call = ToolCall(
                                tool_name=part.tool_name,
                                args=part.args,
                                tool_call_id=part.tool_call_id
                            )
                            tool_calls.append(current_tool_call)
                            logging.info(f"Tool call: {current_tool_call}")
                        elif part.part_kind == 'tool-return':
                            if current_tool_call:
                                tool_output = ToolOutput(
                                    tool_name=current_tool_call.tool_name,
                                    tool_call_id=current_tool_call.tool_call_id,
                                    content=part.content
                                )
                                tool_outputs.append(tool_output)
                                logging.info(f"Tool output: {tool_output}")
                                current_tool_call = None
                            else:
                                logging.warning("Received tool-return without a preceding tool-call")

        if current_tool_call:
            logging.warning(f"Unmatched tool call: {current_tool_call}")

        return tool_calls, tool_outputs

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
