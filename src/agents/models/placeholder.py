"""Placeholder agent implementation.

This module provides a PlaceholderAgent that can be used as a fallback
when a real agent initialization fails. This ensures the system doesn't 
completely break when an agent can't be properly initialized.
"""
import logging
from typing import Dict, Optional, List, Any, Union

from src.agents.models.base_agent import BaseAgent
from src.agents.models.response import AgentResponse
from src.memory.message_history import MessageHistory

logger = logging.getLogger(__name__)

class PlaceholderAgent(BaseAgent):
    """Placeholder agent implementation for fallback when initialization fails.
    
    This agent provides minimal functionality and will return error messages
    when attempts are made to use it. It allows the system to continue running
    even when a real agent fails to initialize.
    """
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the placeholder agent.
        
        Args:
            config: Configuration dictionary
        """
        # Create a useful name for logging
        self.name = config.get("name", "placeholder_agent")
        self.agent_type = config.get("type", "placeholder")
        
        # Set a descriptive system prompt
        system_prompt = "This is a placeholder agent that cannot process requests. Please check logs for initialization errors."
        
        # Initialize the base agent
        super().__init__(config, system_prompt)
        logger.info(f"Created PlaceholderAgent with name: {self.name}")
    
    def register_tools(self):
        """Register tools with the agent.
        
        This is required by BaseAgent but does nothing in the placeholder.
        """
        logger.debug(f"PlaceholderAgent.register_tools called for {self.name}")
        pass
    
    async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[Union[int, str]] = None, user_id: int = 1, context: Optional[Dict] = None) -> AgentResponse:
        """Process a user message and return an error response.
        
        Args:
            user_message: The message to process
            session_id: Optional session ID for message context
            agent_id: Optional agent ID
            user_id: Optional user ID
            context: Optional additional context
            
        Returns:
            Error response indicating this is a placeholder agent
        """
        logger.warning(f"Attempt to use PlaceholderAgent {self.name} to process message")
        
        # Return an error response
        return AgentResponse(
            text=f"This agent ({self.name}) failed to initialize properly. Please check logs for more information.",
            success=False,
            error_message="Agent initialization failed"
        )
    
    async def run(self, *args, **kwargs) -> AgentResponse:
        """Placeholder run method that returns an error.
        
        Returns:
            Error response indicating this is a placeholder agent
        """
        logger.warning(f"Attempt to use PlaceholderAgent {self.name} to run")
        
        return AgentResponse(
            text=f"This agent ({self.name}) failed to initialize properly. Please check logs for more information.",
            success=False,
            error_message="Agent initialization failed"
        ) 