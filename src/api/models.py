from datetime import datetime
from typing import Dict, List, Optional, Any
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
    environment: str = "development"  # Default to development if not specified

class DeleteSessionResponse(BaseModel):
    """Response model for session deletion."""
    status: str
    session_id: str
    message: str

class ToolCallModel(BaseModel):
    """Model for a tool call."""
    tool_name: str
    args: Dict
    tool_call_id: str

class ToolOutputModel(BaseModel):
    """Model for a tool output."""
    tool_name: str
    tool_call_id: str
    content: Any

class MessageModel(BaseModel):
    """Model for a single message in the conversation."""
    role: str
    content: str
    assistant_name: Optional[str] = None
    tool_calls: Optional[List[ToolCallModel]] = None
    tool_outputs: Optional[List[ToolOutputModel]] = None

    class Config:
        json_schema_extra = {"examples": [{"role": "assistant", "content": "Hello!"}]}
        exclude_none = True  # Exclude None values from response

class SessionResponse(BaseModel):
    """Response model for session retrieval."""
    session_id: str
    messages: List[MessageModel]
    exists: bool 