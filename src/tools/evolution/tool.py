"""Evolution tool implementation.

This module provides the core functionality for Evolution tools.
"""
import logging
from typing import Dict, List, Any, Optional
from pydantic_ai import RunContext

from .schema import Message, SendMessageResponse, GetChatHistoryResponse

logger = logging.getLogger(__name__)

def get_send_message_description() -> str:
    """Get description for the send_message function."""
    return "Send a message to a phone number via Evolution API."

def get_chat_history_description() -> str:
    """Get description for the get_chat_history function."""
    return "Get chat history for a phone number from Evolution API."

async def send_message(ctx: RunContext[Dict], token: str, phone: str, message: str) -> Dict[str, Any]:
    """Send a message to a phone number.

    Args:
        ctx: The run context
        token: Evolution API token
        phone: The phone number to send the message to
        message: The message content

    Returns:
        Dict with the response data
    """
    try:
        logger.info(f"Sending message to {phone}: {message}")
        
        # Mock implementation - in a real implementation, this would use the Evolution API
        # Return mock data
        response = SendMessageResponse(
            success=True,
            message_id="mock-message-id-12345",
            timestamp="2023-06-01T12:00:00.000Z"
        )
        return response.dict()
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        response = SendMessageResponse(
            success=False,
            error=f"Error: {str(e)}"
        )
        return response.dict()

async def get_chat_history(ctx: RunContext[Dict], token: str, phone: str, limit: int = 50) -> Dict[str, Any]:
    """Get chat history for a phone number.

    Args:
        ctx: The run context
        token: Evolution API token
        phone: The phone number to get history for
        limit: Maximum number of messages to return

    Returns:
        Dict with the chat history
    """
    try:
        logger.info(f"Getting chat history for {phone}, limit: {limit}")
        
        # Mock implementation - in a real implementation, this would use the Evolution API
        # Return mock data
        mock_messages = [
            {
                "id": "msg1",
                "from": phone,
                "content": "Hello, I need information about your products",
                "timestamp": "2023-06-01T11:50:00.000Z",
                "type": "incoming",
            },
            {
                "id": "msg2",
                "from": "system",
                "content": "Hi there! I'd be happy to help with information about our products. What specific products are you interested in?",
                "timestamp": "2023-06-01T11:51:00.000Z",
                "type": "outgoing",
            },
        ][:limit]
        
        response = GetChatHistoryResponse(
            success=True,
            messages=mock_messages
        )
        return response.dict()
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        response = GetChatHistoryResponse(
            success=False,
            error=f"Error: {str(e)}"
        )
        return response.dict() 