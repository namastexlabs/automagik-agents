"""Gmail tool schemas.

This module defines the Pydantic models for Gmail tool input and output.
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class SendEmailInput(BaseModel):
    """Input model for sending email."""
    to: str = Field(..., description="Email address of the recipient")
    cc: Optional[List[str]] = Field(None, description="List of email addresses to CC")
    subject: str = Field(..., description="Subject of the email")
    message: str = Field(..., description="Content of the email")
    content_type: Optional[str] = Field("text/plain", description="Content type of the email: text/plain or text/html")
    plain_text_alternative: Optional[str] = Field(None, description="Plain text alternative for HTML emails")
    extra_content: Optional[str] = Field(None, description="Additional content to append to the email message")

class SendEmailResult(BaseModel):
    """Result model for sending email."""
    success: bool = Field(..., description="Whether the email was sent successfully")
    message_id: Optional[str] = Field(None, description="ID of the sent message if successful")
    error: Optional[str] = Field(None, description="Error message if sending failed") 