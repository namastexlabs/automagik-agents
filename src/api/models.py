from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel

class AgentRunRequest(BaseModel):
    """Request model for running an agent."""
    message_input: str
    context: dict = {}
    session_id: Optional[str] = None

class AgentInfo(BaseModel):
    """Information about an available agent."""
    name: str
    type: str

class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    timestamp: datetime
    version: str
    environment: str

class DeleteSessionResponse(BaseModel):
    """Response model for session deletion."""
    status: str
    session_id: str
    message: str

class MessageModel(BaseModel):
    """Model for a single message in the conversation."""
    role: str
    content: str
    assistant_name: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_outputs: Optional[List[Dict]] = None

class SessionResponse(BaseModel):
    """Response model for session retrieval."""
    session_id: str
    messages: List[MessageModel]
    exists: bool 