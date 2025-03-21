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
        
        # Convert config to AgentConfig if it's a dictionary
        if isinstance(config, dict):
            self.config = AgentConfig(config)
        else:
            self.config = config
            
        # Store the system prompt
        self.system_prompt = system_prompt
        
        # Initialize agent ID (will be set later if available)
        self.db_id = None
        
        # Initialize message history (will be set in process_message)
        self.message_history = None
        
        return self
   