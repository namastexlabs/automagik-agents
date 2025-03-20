"""Evolution tool schemas.

This module defines the Pydantic models for Evolution tool input and output.
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List

class Message(BaseModel):
    """Model for Evolution message data."""
    id: str = Field(..., description="Message ID")
    from_field: str = Field(..., description="Sender of the message", alias="from")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="Timestamp of the message")
    type: str = Field(..., description="Type of message (incoming/outgoing)")
    
    class Config:
        allow_population_by_field_name = True

class SendMessageResponse(BaseModel):
    """Response model for send_message."""
    success: bool = Field(..., description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if the operation failed")
    message_id: Optional[str] = Field(None, description="ID of the sent message")
    timestamp: Optional[str] = Field(None, description="Timestamp of the sent message")

class GetChatHistoryResponse(BaseModel):
    """Response model for get_chat_history."""
    success: bool = Field(..., description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if the operation failed")
    messages: List[Message] = Field(default_factory=list, description="List of messages in the chat history") 