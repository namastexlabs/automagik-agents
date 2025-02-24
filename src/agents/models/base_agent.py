import logging
from typing import Dict, Optional
from pydantic import BaseModel
from pydantic_ai import Agent
from src.agents.models.agent import AgentBaseResponse
from src.memory.message_history import MessageHistory
import time

class AgentConfig(BaseModel):
    """Configuration for agents."""
    model: str
    retries: Optional[int] = None

class BaseAgent:
    """Base agent class with common functionality."""
    
    def __init__(self, config: Dict[str, str], system_prompt: str):
        """Initialize base agent functionality."""
        self.config = AgentConfig(model=config.get("model", "openai:gpt-4o-mini"))
        self.system_prompt = system_prompt
        self.agent = self.initialize_agent()
        self.post_init()

    def initialize_agent(self) -> Agent:
        """Initialize the agent. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement initialize_agent method")

    def register_tools(self):
        """Register tools with the agent. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement register_tools method")

    def post_init(self):
        """Post-initialization tasks. Can be overridden by subclasses."""
        self.register_tools()

    async def process_message(self, user_message: str, session_id: Optional[str] = None) -> AgentBaseResponse:
        """Process a user message and return a response."""
        if session_id is None:
            session_id = f"session_{int(time.time())}"
            logging.info(f"Generated new session ID: {session_id}")
        else:
            logging.info(f"Using existing session ID: {session_id}")
            
        message_history = MessageHistory(session_id)
        message_history.add_system_prompt(self.system_prompt)
        message_history.add(user_message)
        
        logging.info(f"Processing user message in session {session_id}: {user_message}")

        try:
            result = await self.agent.run(
                user_message,
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
                session_id=session_id
            )
        
        response_text = result.data
        logging.info(f"Response text: {response_text[:100]}...")

        # Extract tool calls and outputs from the current run only
        tool_calls = []
        tool_outputs = []
        for message in result.all_messages():
            if hasattr(message, 'parts'):
                for part in message.parts:
                    if hasattr(part, 'part_kind'):
                        if part.part_kind == 'tool-call':
                            tool_calls.append({
                                'tool_name': getattr(part, 'tool_name', ''),
                                'args': getattr(part, 'args', {}),
                                'tool_call_id': getattr(part, 'tool_call_id', '')
                            })
                        elif part.part_kind == 'tool-return':
                            tool_outputs.append({
                                'tool_name': getattr(part, 'tool_name', ''),
                                'tool_call_id': getattr(part, 'tool_call_id', ''),
                                'content': getattr(part, 'content', '')
                            })

        logging.info(f"Captured {len(tool_calls)} tool calls and {len(tool_outputs)} tool outputs")
        
        message_history.add_response(
            content=response_text,
            assistant_name=self.__class__.__name__,
            tool_calls=tool_calls,
            tool_outputs=tool_outputs
        )
        
        response = AgentBaseResponse.from_agent_response(
            message=response_text,
            history=message_history,
            error=None,
            session_id=session_id
        )
        
        logging.info(f"Returning AgentBaseResponse for session {session_id}")
        
        return response 