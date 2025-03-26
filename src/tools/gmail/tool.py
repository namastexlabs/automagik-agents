"""Gmail API tool implementation.

This module provides the core functionality for Gmail API tools.
"""
import logging
from typing import Dict, Any, Optional
from pydantic_ai import RunContext

from .schema import SendEmailInput, SendEmailResult
from .provider import GmailProvider

logger = logging.getLogger(__name__)

def get_send_email_description() -> str:
    """Get description for the send_email function."""
    return "Send an email via Gmail API."

async def send_email(ctx: RunContext[Dict], credentials_path: str, input: SendEmailInput) -> Dict[str, Any]:
    """Send an email via Gmail API.
    
    Args:
        ctx: The run context
        credentials_path: Path to OAuth credentials JSON file
        input: Email parameters
        
    Returns:
        Dict with the result of the operation
    """
    logger.info(f"Sending email to: {input.to}")
    
    try:
        # Create provider instance
        provider = GmailProvider(credentials_path=credentials_path)
        
        # Use provider to send email
        result = await provider.send_email(input)
        
        # Return the result as a dictionary
        return result.dict()
    except Exception as e:
        error_msg = f"Error sending email: {str(e)}"
        logger.error(error_msg)
        
        response = SendEmailResult(
            success=False,
            error=error_msg
        )
        return response.dict() 