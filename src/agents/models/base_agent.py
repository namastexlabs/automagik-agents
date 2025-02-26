import logging
from typing import Dict, Optional, Union
from pydantic import BaseModel
from pydantic_ai import Agent
from src.agents.models.agent import AgentBaseResponse
from src.memory.message_history import MessageHistory
import time
from abc import ABC, abstractmethod

class AgentConfig(BaseModel):
    """Configuration for agents."""
    model: str
    retries: Optional[int] = None

class BaseAgent(ABC):
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

    @abstractmethod
    async def run(self, user_message: str, message_history: MessageHistory) -> AgentBaseResponse:
        """Run the agent with the given message and message history.
        
        Args:
            user_message: User message (already in message_history)
            message_history: Message history for this session
            
        Returns:
            Agent response
        """
        pass
    
    async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[Union[int, str]] = None, user_id: int = 1, context: Optional[Dict] = None) -> AgentBaseResponse:
        """Process a user message with this agent.
        
        Args:
            user_message: User message to process
            session_id: Optional session ID
            agent_id: Optional agent ID for database tracking (integer or string for backwards compatibility)
            user_id: User ID (integer)
            context: Optional additional context that will be logged but not passed to the agent due to API limitations
            
        Returns:
            Agent response
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
        
        # Set default context if None is provided
        context = context or {}
            
        logging.info(f"Using existing session ID: {session_id}")
        
        # Log any additional context provided
        if context:
            logging.info(f"Additional message context: {context}")
            
        message_history = MessageHistory(session_id, user_id=user_id)
        message_history.add_system_prompt(self.system_prompt, agent_id=agent_id)
        
        # Add agent_id to the user message metadata
        user_message_obj = message_history.add(user_message, agent_id=agent_id)
        
        logging.info(f"Processing user message in session {session_id}: {user_message}")

        try:
            # The agent.run() method doesn't accept extra_context parameter
            # Just pass the required parameters
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