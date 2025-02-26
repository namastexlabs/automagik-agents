from typing import Dict, List, Optional
import logging
from pydantic_ai import Agent

from src.agents.models.base_agent import BaseAgent
from src.agents.models.agent import AgentBaseResponse
from src.memory.message_history import MessageHistory
from src.agents.simple.notion_agent.prompts import NOTION_AGENT_PROMPT
from src.tools.notion_tools import NotionTools

logger = logging.getLogger(__name__)

class NotionAgent(BaseAgent):
    """Notion agent implementation for interacting with Notion API."""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the notion agent with configuration."""
        # Validate Notion token
        if "notion_token" not in config:
            raise ValueError("Notion token is required for NotionAgent")
            
        # Store the token for later use by tools
        self.notion_token = config["notion_token"]
        
        super().__init__(config, NOTION_AGENT_PROMPT)

    def initialize_agent(self) -> Agent:
        """Initialize the notion agent with configuration."""
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register Notion-specific tools with the agent."""
        # Initialize the NotionTools class
        notion_tools = NotionTools()
        
        # Register all Notion tools
        for tool in notion_tools.tools:
            self.agent.tool(tool)
            
    async def run(self, user_message: str, message_history: MessageHistory) -> AgentBaseResponse:
        """Run the agent with the given message and message history.
        
        Args:
            user_message: User message (already in message_history)
            message_history: Message history for this session
            
        Returns:
            Agent response
        """
        try:
            # Run the agent with the user message and message history
            result = await self.agent.run(
                user_message,
                message_history=message_history.messages
            )
            
            # Extract the response text
            response_text = result.data
            
            # Create and return the agent response
            return AgentBaseResponse.from_agent_response(
                message=response_text,
                history=message_history,
                error=None,
                session_id=message_history.session_id
            )
        except Exception as e:
            error_msg = f"Error running NotionAgent: {str(e)}"
            logger.error(error_msg)
            return AgentBaseResponse.from_agent_response(
                message="An error occurred while processing your Notion request.",
                history=message_history,
                error=error_msg,
                session_id=message_history.session_id
            )
