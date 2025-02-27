from typing import Dict, List, Optional
import logging
from pydantic_ai import Agent

from src.agents.models.base_agent import BaseAgent
from src.agents.models.agent import AgentBaseResponse
from src.memory.message_history import MessageHistory
from src.agents.simple.stan_agent.prompts import STAN_HOST_PROMPT
from src.agents.simple.stan_agent.backoffice_agent import BackofficeAgent
from src.agents.simple.stan_agent.product_agent import ProductAgent
from src.tools.blackpearl_tools import BlackPearlTools
from src.tools.omie_tools import OmieTools

logger = logging.getLogger(__name__)

class StanAgent(BaseAgent):
    """Stan agent implementation for client onboarding and product information."""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the Stan agent with configuration."""
        # Validate required tokens
        if "blackpearl_token" not in config:
            raise ValueError("BlackPearl token is required for StanAgent")
            
        if "omie_token" not in config:
            raise ValueError("Omie token is required for StanAgent")
            
        if "google_drive_token" not in config:
            raise ValueError("Google Drive token is required for StanAgent")
            
        if "evolution_token" not in config:
            raise ValueError("Evolution token is required for StanAgent")
            
        # Store the tokens for later use by tools
        self.blackpearl_token = config["blackpearl_token"]
        self.omie_token = config["omie_token"]
        self.google_drive_token = config["google_drive_token"]
        self.evolution_token = config["evolution_token"]
        
        # Initialize specialized agents
        self.backoffice_agent = BackofficeAgent(config)
        
        # Create config for product agent
        product_config = {
            "model": config.get("model", "openai:gpt-4o-mini"),
            "retries": config.get("retries", 3),
            "google_drive_token": self.google_drive_token,
            "evolution_token": self.evolution_token
        }
        self.product_agent = ProductAgent(product_config)
        
        super().__init__(config, STAN_HOST_PROMPT)

    def initialize_agent(self) -> Agent:
        """Initialize the Stan host agent with configuration."""
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register Stan-specific tools with the agent."""
        # Initialize the tools
        blackpearl_tools = BlackPearlTools(self.blackpearl_token)
        omie_tools = OmieTools(self.omie_token)
        
        # Register BlackPearl tools
        for tool in blackpearl_tools.get_host_tools():
            self.agent.tool(tool)
            
        # Register Omie tools
        for tool in omie_tools.get_host_tools():
            self.agent.tool(tool)
            
        # Register state router tool
        self.agent.tool(self.route_to_agent)
            
    async def route_to_agent(self, agent_type: str, user_message: str, message_history: MessageHistory) -> str:
        """Route the conversation to the appropriate specialized agent.
        
        Args:
            agent_type: The type of agent to route to ('backoffice' or 'product')
            user_message: The user message to send to the agent
            message_history: The current message history
            
        Returns:
            The response from the specialized agent
        """
        if agent_type.lower() == "backoffice":
            result = await self.backoffice_agent.run(user_message, message_history)
            return result.message
        elif agent_type.lower() == "product":
            result = await self.product_agent.run(user_message, message_history)
            return result.message
        else:
            return f"Unknown agent type: {agent_type}. Please use 'backoffice' or 'product'."
            
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
            error_msg = f"Error running StanAgent: {str(e)}"
            logger.error(error_msg)
            return AgentBaseResponse.from_agent_response(
                message="An error occurred while processing your request.",
                history=message_history,
                error=error_msg,
                session_id=message_history.session_id
            )
