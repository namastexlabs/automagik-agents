import logging
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from pydantic_ai import Agent
from pydantic_ai.result import RunResult
from src.agents.models.agent import AgentBaseResponse
from src.memory.message_history import MessageHistory
import time

@dataclass
class Deps:
    # Add any common dependencies your agents might need
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

class BaseAgent:
    def __init__(self, config: Dict[str, str], system_prompt: str):
        self.agent = Agent(
            'openai:gpt-4o-mini',
            system_prompt=system_prompt,
            deps_type=self.get_deps_type()
        )
        self.deps = self.get_deps_type()()
        self.system_prompt = system_prompt
        self.assistant_name = self.get_assistant_name()
        self.register_tools()

    def get_deps_type(self):
        return Deps

    def get_assistant_name(self) -> str:
        """Get the name of the assistant. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_assistant_name method")

    def register_tools(self):
        raise NotImplementedError("Subclasses must implement register_tools method")

    @staticmethod
    def format_tool_info(info: Dict[str, Any]) -> str:
        """Format tool call or output information for logging."""
        return ", ".join(f"{k}: {v}" for k, v in info.items())

    def extract_tool_calls_and_outputs(self, result: RunResult) -> Tuple[List[ToolCall], List[ToolOutput]]:
        tool_calls: Dict[str, ToolCall] = {}
        tool_outputs: Dict[str, ToolOutput] = {}
        
        for message in result._all_messages:
            if hasattr(message, 'parts'):
                for part in message.parts:
                    if hasattr(part, 'part_kind'):
                        if part.part_kind == 'tool-call':
                            tool_call = ToolCall(
                                tool_name=part.tool_name,
                                args=part.args,
                                tool_call_id=part.tool_call_id
                            )
                            tool_calls[part.tool_call_id] = tool_call
                            logging.info(f"Tool call: {tool_call}")
                        elif part.part_kind == 'tool-return':
                            tool_output = ToolOutput(
                                tool_name=part.tool_name,
                                tool_call_id=part.tool_call_id,
                                content=part.content
                            )
                            tool_outputs[part.tool_call_id] = tool_output
                            logging.info(f"Tool output: {tool_output}")

        # Match tool calls with their outputs and log any mismatches
        matched_calls = []
        matched_outputs = []
        for call_id, call in tool_calls.items():
            if call_id in tool_outputs:
                matched_calls.append(call)
                matched_outputs.append(tool_outputs[call_id])
            else:
                logging.warning(f"Missing tool output for tool call: {call}")

        for output_id, output in tool_outputs.items():
            if output_id not in tool_calls:
                logging.warning(f"Received tool output without a matching call: {output}")

        logging.info(f"Matched {len(matched_calls)} tool calls with their outputs")
        return matched_calls, matched_outputs

    async def process_message(self, user_message: str, session_id: Optional[str] = None) -> AgentBaseResponse:
        """Process a user message and return a response.
        
        Args:
            user_message: The message from the user to process.
            session_id: Optional session identifier. If not provided, a new session will be created.
            
        Returns:
            The agent's response including tool calls and outputs.
        """
        # Generate a session ID if none provided
        if session_id is None:
            session_id = f"session_{int(time.time())}"
            logging.info(f"Generated new session ID: {session_id}")
        else:
            logging.info(f"Using existing session ID: {session_id}")
            
        # Initialize message history with session ID
        message_history = MessageHistory(session_id)
        
        # Add or update system prompt
        message_history.add_system_prompt(self.system_prompt)
        
        # Add user message
        message_history.add(user_message)
        
        logging.info(f"Processing user message in session {session_id}: {user_message}")

        try:
            result = await self.agent.run(
                user_message,
                deps=self.deps,
                message_history=message_history.messages
            )
            logging.info(f"Agent run completed. Result type: {type(result)}")
        except Exception as e:
            error_msg = f"Error running agent: {str(e)}"
            logging.error(error_msg)
            return AgentBaseResponse.from_agent_response(
                message="An error occurred while processing your request.",
                history=message_history,
                error=error_msg,
                tool_calls=[],
                tool_outputs=[],
                session_id=session_id
            )
        
        response_text = result.data
        logging.info(f"Response text: {response_text[:100]}...")

        tool_calls, tool_outputs = self.extract_tool_calls_and_outputs(result)
        tool_calls_dict = [tc.__dict__ for tc in tool_calls]
        tool_outputs_dict = [to.__dict__ for to in tool_outputs]

        logging.info(f"Captured {len(tool_calls)} tool calls and {len(tool_outputs)} tool outputs")
        
        # Add response with tool information
        message_history.add_response(
            content=response_text,
            assistant_name=self.assistant_name,
            tool_calls=tool_calls_dict,
            tool_outputs=tool_outputs_dict
        )
        
        response = AgentBaseResponse.from_agent_response(
            message=response_text,
            history=message_history,
            error=None,
            session_id=session_id
        )
        
        logging.info(f"Returning AgentBaseResponse for session {session_id}")
        
        return response 