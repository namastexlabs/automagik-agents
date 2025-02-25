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
        # Store the original config dictionary
        self.raw_config = config
        # Create AgentConfig object using the model from config or default
        model = config["model"] if "model" in config else "openai:gpt-4o-mini"
        self.config = AgentConfig(model=model)
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

    async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[str] = None, user_id: str = "default_user") -> AgentBaseResponse:
        """Process a user message and return a response.
        
        Args:
            user_message: The message from the user
            session_id: Optional session ID for message history
            agent_id: Optional agent ID for database tracking
            user_id: User ID for database association, defaults to "default_user"
            
        Returns:
            AgentBaseResponse containing the response and metadata
        """
        if not session_id:
            # Using empty string is no longer allowed - we need a valid session ID
            logging.error("Empty session_id provided, session must be created before calling process_message")
            return AgentBaseResponse.from_agent_response(
                message="Error: No valid session ID provided. A session must be created before processing messages.",
                history=MessageHistory(""),
                error="No valid session ID provided",
                session_id=""
            )
            
        logging.info(f"Using existing session ID: {session_id}")
            
        message_history = MessageHistory(session_id, user_id=user_id)
        message_history.add_system_prompt(self.system_prompt, agent_id=agent_id)
        
        # Add agent_id to the user message metadata
        user_message_obj = message_history.add(user_message, agent_id=agent_id)
        
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
        
        # Add the response with assistant info and agent_id
        message_history.add_response(
            content=response_text,
            assistant_name=self.__class__.__name__,
            tool_calls=tool_calls,
            tool_outputs=tool_outputs,
            agent_id=agent_id
        )
        
        # Use the potentially updated session_id from message_history
        session_id = message_history.session_id
        
        response = AgentBaseResponse.from_agent_response(
            message=response_text,
            history=message_history,
            error=None,
            session_id=session_id
        )
        
        logging.info(f"Returning AgentBaseResponse for session {session_id}")
        
        return response 