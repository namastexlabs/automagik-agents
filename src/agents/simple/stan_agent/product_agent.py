from typing import Dict, List, Optional
import logging
from pydantic_ai import Agent

from src.agents.models.base_agent import BaseAgent
from src.agents.models.agent import AgentBaseResponse
from src.memory.message_history import MessageHistory
from src.tools.chroma_tools import ChromaTools
from src.tools.google_drive_tools import GoogleDriveTools
from src.tools.evolution_tools import EvolutionTools

logger = logging.getLogger(__name__)

# Product agent system prompt
PRODUCT_PROMPT = (
    "You are the Product agent for Solid, responsible for providing accurate information "
    "about products to approved clients.\n\n"
    
    "Your primary responsibilities are:\n"
    "1. Searching for products in our database\n"
    "2. Providing detailed product information\n"
    "3. Sending product images when available\n"
    "4. Answering product-related questions\n\n"
    
    "Important guidelines:\n"
    "- Only provide product information to approved users\n"
    "- Be accurate and comprehensive in your product descriptions\n"
    "- Always include product images when available\n"
    "- Compare user requests with available product families and brands to avoid hallucinations\n"
    "- If a product is not found, clearly state that it's not available\n\n"
    
    "When responding, focus on providing factual product information in a helpful manner."
)

class ProductAgent(BaseAgent):
    """Product agent implementation for product information retrieval."""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the product agent with configuration."""
        # Validate required tokens
        if "google_drive_token" not in config:
            raise ValueError("Google Drive token is required for ProductAgent")
            
        if "evolution_token" not in config:
            raise ValueError("Evolution token is required for ProductAgent")
            
        # Store the tokens for later use by tools
        self.google_drive_token = config["google_drive_token"]
        self.evolution_token = config["evolution_token"]
        
        super().__init__(config, PRODUCT_PROMPT)

    def initialize_agent(self) -> Agent:
        """Initialize the product agent with configuration."""
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register Product-specific tools with the agent."""
        # Initialize the tools
        chroma_tools = ChromaTools()
        google_drive_tools = GoogleDriveTools(self.google_drive_token)
        evolution_tools = EvolutionTools(self.evolution_token)
        
        # Register Chroma tools
        for tool in chroma_tools.get_tools():
            self.agent.tool(tool)
            
        # Register Google Drive tools
        for tool in google_drive_tools.get_tools():
            self.agent.tool(tool)
            
        # Register Evolution tools
        for tool in evolution_tools.get_tools():
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
            error_msg = f"Error running ProductAgent: {str(e)}"
            logger.error(error_msg)
            return AgentBaseResponse.from_agent_response(
                message="An error occurred while processing your request.",
                history=message_history,
                error=error_msg,
                session_id=message_history.session_id
            ) 