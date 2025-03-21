import logging
import re
from typing import Dict, Optional, Union, List, Any, Set, Type, TypeVar, Generic
from pydantic import BaseModel
from pydantic_ai import Agent as PydanticAgent
from pydantic_ai.usage import UsageLimits
from pydantic_ai.settings import ModelSettings
from src.agents.models.agent import AgentBaseResponse_v2
from src.memory.message_history import MessageHistory
from src.agents.models.dependencies import BaseDependencies
import time
from abc import ABC, abstractmethod
import json
import uuid
from pydantic_ai.messages import SystemPromptPart

logger = logging.getLogger(__name__)

# Define a generic type variable for dependencies
T = TypeVar('T', bound=BaseDependencies)

class AgentConfig:
    """Configuration for an agent.

    Attributes:
        model: The LLM model to use.
        temperature: The temperature to use for LLM calls.
        retries: The number of retries to perform for LLM calls.
    """

    def __init__(self, config: Dict[str, str] = None):
        """Initialize the agent configuration.

        Args:
            config: A dictionary of configuration options.
        """
        self.config = config or {}
        self.model = self.config.get("model", "openai:gpt-3.5-turbo")
        self.temperature = float(self.config.get("temperature", "0.7"))
        self.retries = int(self.config.get("retries", "1"))
        
    def get(self, key: str, default=None):
        """Get a configuration value.
        
        Args:
            key: The configuration key to get
            default: Default value if key is not found
            
        Returns:
            The configuration value or default
        """
        return self.config.get(key, default)
        
    def __getattr__(self, name):
        """Get configuration attribute.
        
        Args:
            name: Attribute name to get
            
        Returns:
            The attribute value or None
            
        Raises:
            AttributeError: If configuration attribute doesn't exist
        """
        if name in self.config:
            return self.config[name]
        return None


class BaseAgent(ABC, Generic[T]):
    """Base class for all agents.

    This class defines the interface that all agents must implement and
    provides common functionality for agent initialization and management.
    """

    def __init__(self, config: Union[Dict[str, str], AgentConfig], system_prompt: str):
        """Initialize the agent.

        Args:
            config: Dictionary or AgentConfig object with configuration options.
            system_prompt: The system prompt to use for this agent.
        """
        self.agent_id = None
        self.db_id = None
        
        # Convert config dict to AgentConfig if needed
        if isinstance(config, dict):
            self.config = AgentConfig(config)
        else:
            self.config = config
            
        self.system_prompt = system_prompt
        
        # Initialize the agent
        self.agent = self.initialize_agent()
        
        # Register tools with the agent
        if self.agent:
            self.register_tools()

    def initialize_agent(self) -> PydanticAgent:
        """Initialize the pydantic-ai agent.
        
        This implementation creates a basic agent with Dict dependencies.
        Override this method to use specific dependency types.

        Returns:
            The initialized pydantic-ai Agent instance
        """
        return self.initialize_agent_with_deps(BaseDependencies)

    def initialize_agent_with_deps(self, deps_type: Type[T] = BaseDependencies) -> PydanticAgent:
        """Initialize the pydantic-ai agent with type-safe dependencies.
        
        Args:
            deps_type: The type of dependencies to use
            
        Returns:
            The initialized pydantic-ai Agent instance
        """
        model_settings = {}
        
        # Extract model settings from config
        for key, value in self.config.config.items():
            if key.startswith("model_settings."):
                setting_key = key.replace("model_settings.", "")
                try:
                    # Try to convert numbers appropriately
                    if value.isdigit():
                        model_settings[setting_key] = int(value)
                    elif re.match(r'^-?\d+(\.\d+)?$', value):
                        model_settings[setting_key] = float(value)
                    else:
                        model_settings[setting_key] = value
                except (ValueError, AttributeError):
                    model_settings[setting_key] = value
        
        # Create the agent
        agent = PydanticAgent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries,
            deps_type=deps_type,  # Use the specified dependency type
            result_type=str,      # Default to string result type
            instrument=True,      # Enable instrumentation
            model_settings=model_settings or None
        )
        
        return agent

    @abstractmethod
    def register_tools(self):
        """Register tools with the agent.
        
        This method should be implemented by subclasses to register
        all tools that the agent will use.
        """
        pass

    @abstractmethod
    async def process_message(self, user_message: str, session_id: str = None, user_id: int = None) -> AgentBaseResponse_v2:
        """Process a user message and return a response.
        
        This is the main method that clients should call to interact with the agent.
        
        Args:
            user_message: The message to process
            session_id: Optional session ID for message context
            user_id: Optional user ID
            
        Returns:
            The agent's response
        """
        pass
    
    async def _create_dependencies(self, session_id: Optional[str] = None, user_id: Optional[int] = None) -> T:
        """Create dependencies for this agent.
        
        Override this method in subclasses to create agent-specific dependencies.
        
        Args:
            session_id: Optional session ID
            user_id: Optional user ID
            
        Returns:
            Instance of the agent's dependencies
        """
        deps = BaseDependencies(
            user_id=user_id,
            session_id=session_id
        )
        
        # Set agent ID if available
        if hasattr(self, '_get_agent_id_numeric'):
            agent_id = self._get_agent_id_numeric()
            if agent_id:
                deps.set_agent_id(agent_id)
        
        return deps
    
    def _get_usage_limits(self) -> Optional[UsageLimits]:
        """Get usage limits from configuration.
        
        Returns:
            UsageLimits instance or None if not configured
        """
        response_tokens_limit = self.config.get("response_tokens_limit")
        request_limit = self.config.get("request_limit")
        total_tokens_limit = self.config.get("total_tokens_limit")
        
        if not any([response_tokens_limit, request_limit, total_tokens_limit]):
            return None
            
        limits = {}
        
        if response_tokens_limit:
            limits["response_tokens_limit"] = int(response_tokens_limit)
            
        if request_limit:
            limits["request_limit"] = int(request_limit)
            
        if total_tokens_limit:
            limits["total_tokens_limit"] = int(total_tokens_limit)
            
        return UsageLimits(**limits) if limits else None

    def post_init(self):
        """Post-initialization tasks. Can be overridden by subclasses."""
        self.register_tools()

    @abstractmethod
    async def run(self, user_message: str, message_history: MessageHistory) -> AgentBaseResponse_v2:
        """Run the agent with the given message and message history.
        
        Args:
            user_message: User message (already in message_history)
            message_history: Message history for this session
            
        Returns:
            Agent response
        """
        pass
    
    async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[Union[int, str]] = None, user_id: int = 1, context: Optional[Dict] = None, message_history: Optional['MessageHistory'] = None) -> AgentBaseResponse_v2:
        """Process a user message with this agent.
        
        Args:
            user_message: User message to process
            session_id: Optional session ID
            agent_id: Optional agent ID for database tracking (integer or string for backwards compatibility)
            user_id: User ID (integer)
            context: Optional additional context that will be logged but not passed to the agent due to API limitations
            message_history: Optional existing MessageHistory object
            
        Returns:
            Agent response
        """
        if not session_id:
            # Using empty string is no longer allowed - we need a valid session ID
            logging.error("Empty session_id provided, session must be created before calling process_message")
            return AgentBaseResponse_v2.from_agent_response(
                message="Error: No valid session ID provided. A session must be created before processing messages.",
                history=MessageHistory(""),
                error="No valid session ID provided",
                session_id=""
            )
        
        # Set default context if None is provided
        context = context or {}
            
        logging.info(f"Using existing session ID: {session_id}")
        
        # Update self.db_id from agent_id parameter if provided
        if agent_id:
            self.db_id = int(agent_id) if isinstance(agent_id, (str, int)) and str(agent_id).isdigit() else agent_id
            logging.info(f"Updated agent ID to {self.db_id}")
        
        # Log any additional context provided
        if context:
            logging.info(f"Additional message context: {context}")
            
        # Use provided message history or initialize a new one
        if not message_history:
            logging.info(f"Creating new MessageHistory for session {session_id}")
            message_history = MessageHistory(session_id, user_id=user_id)
        else:
            logging.info(f"Using existing MessageHistory for session {session_id}")
        
        # CRITICAL: Add the system prompt explicitly BEFORE adding the user message
        # This ensures it will be the first message in the sequence sent to OpenAI
        if hasattr(self, "system_prompt") and self.system_prompt:
            logging.info("Adding system prompt to message history before user message")
            message_history.add_system_prompt(self.system_prompt, agent_id=self.db_id)
        
        # Add the user message AFTER the system prompt
        user_message_obj = message_history.add(user_message, agent_id=self.db_id, context=context)
        
        logging.info(f"Processing user message in session {session_id}: {user_message}")

        try:
            # Now when we pass message_history.messages to the agent.run method, 
            # the system prompt should be the first message in the sequence
            messages_for_api = message_history.all_messages()
            
            # Logging message count and sequence for debugging
            logging.info(f"Sending {len(messages_for_api)} messages to OpenAI API")
            if len(messages_for_api) > 0:
                first_msg = messages_for_api[0]
                if hasattr(first_msg, 'parts') and first_msg.parts:
                    first_part_type = type(first_msg.parts[0]).__name__
                    logging.info(f"First message type: {type(first_msg).__name__}, first part type: {first_part_type}")
            
            result = await self.agent.run(
                user_message,
                message_history=messages_for_api
            )
            logging.info(f"Agent run completed. Result type: {type(result)}")
        except Exception as e:
            error_msg = f"Error running agent: {str(e)}"
            logging.error(error_msg)
            logging.error(f"Stack trace: {logging._srcfile}")
            import traceback
            logging.error(traceback.format_exc())
            return AgentBaseResponse_v2.from_agent_response(
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
        
        # Safely extract the messages from the result
        try:
            all_messages = result.all_messages()
        except Exception as e:
            logging.warning(f"Error getting all messages from result: {str(e)}")
            all_messages = []
            
        for message in all_messages:
            # Handle dictionary messages from database
            if isinstance(message, dict):
                # Extract tool calls from dict if present
                if 'tool_calls' in message and isinstance(message['tool_calls'], list):
                    for tc in message['tool_calls']:
                        if isinstance(tc, dict) and 'tool_name' in tc:
                            tool_calls.append({
                                'tool_name': tc.get('tool_name', ''),
                                'args': tc.get('args', {}),
                                'tool_call_id': tc.get('tool_call_id', '')
                            })
                
                # Extract tool outputs from dict if present
                if 'tool_outputs' in message and isinstance(message['tool_outputs'], list):
                    for to in message['tool_outputs']:
                        if isinstance(to, dict) and 'tool_name' in to:
                            tool_outputs.append({
                                'tool_name': to.get('tool_name', ''),
                                'tool_call_id': to.get('tool_call_id', ''),
                                'content': to.get('content', '')
                            })
            # Handle ModelMessage objects with parts
            elif hasattr(message, 'parts'):
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
        
        # Ensure system prompt is obtained from the agent
        system_prompt = getattr(self, "system_prompt", None)
        
        # Logging system prompt handling
        if system_prompt:
            logging.debug(f"Using system prompt from agent: {system_prompt[:50]}...")
        else:
            logging.debug("No system prompt found in agent, will check session metadata")
        
        # Add the response with assistant info, agent_id, and explicit content and system_prompt
        assistant_message = message_history.add_response(
            content=response_text,
            assistant_name=self.__class__.__name__,
            tool_calls=tool_calls,
            tool_outputs=tool_outputs,
            agent_id=self.db_id,
            system_prompt=system_prompt
        )
        
        # Ensure assistant message has content set
        if hasattr(assistant_message, "content"):
            logging.debug(f"Assistant message content set: {assistant_message.content[:50]}...")
        else:
            logging.warning("Assistant message doesn't have content attribute")
        
        # Use the potentially updated session_id from message_history
        session_id = message_history.session_id
        
        response = AgentBaseResponse_v2.from_agent_response(
            message=response_text,
            history=message_history,
            error=None,
            session_id=session_id
        )
        
        logging.info(f"Returning AgentBaseResponse for session {session_id}")
        
        return response 