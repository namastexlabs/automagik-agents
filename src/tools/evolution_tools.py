"""Mock implementation of Evolution API tools."""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class EvolutionTools:
    """Tools for interacting with Evolution API."""
    
    def __init__(self, token: str):
        """Initialize with API token."""
        self.token = token
        logger.info("Initialized EvolutionTools with token")
        
    def get_tools(self) -> List[Any]:
        """Get tools for the agent."""
        logger.info("Returning empty list of tools")
        return []
        
    async def send_message(self, phone: str, message: str) -> Dict[str, Any]:
        """Send a message to a phone number.
        
        Args:
            phone: The phone number to send the message to
            message: The message content
            
        Returns:
            Response data from the API
        """
        logger.info(f"Mock sending message to {phone}: {message}")
        # Return mock data
        return {
            "success": True,
            "message_id": "mock-message-id-12345",
            "timestamp": "2023-06-01T12:00:00.000Z"
        }
        
    async def get_chat_history(self, phone: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat history for a phone number.
        
        Args:
            phone: The phone number to get history for
            limit: Maximum number of messages to return
            
        Returns:
            List of message objects
        """
        logger.info(f"Mock getting chat history for {phone}, limit: {limit}")
        # Return mock data
        return [
            {
                "id": "msg1",
                "from": phone,
                "content": "Hello, I need information about your products",
                "timestamp": "2023-06-01T11:50:00.000Z",
                "type": "incoming"
            },
            {
                "id": "msg2",
                "from": "system",
                "content": "Hi there! I'd be happy to help with information about our products. What specific products are you interested in?",
                "timestamp": "2023-06-01T11:51:00.000Z",
                "type": "outgoing"
            }
        ][:limit] 