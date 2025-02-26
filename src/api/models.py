from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, ConfigDict

class BaseResponseModel(BaseModel):
    """Base model for all response models with common configuration."""
    model_config = ConfigDict(
        exclude_none=True,  # Exclude None values from response
        validate_assignment=True,  # Validate values on assignment
        extra='ignore'  # Ignore extra fields
    )

class AgentRunRequest(BaseResponseModel):
    """Request model for running an agent."""
    message_content: str
    message_type: Optional[str] = None
    mediaUrl: Optional[str] = None
    mime_type: Optional[str] = None
    channel_payload: Optional[Dict[str, Any]] = None
    context: dict = {}
    session_id: Optional[str] = None
    user_id: Optional[str] = "default_user"  # Default user ID if none provided
    message_limit: Optional[int] = 10  # Default to last 10 messages

class AgentInfo(BaseResponseModel):
    """Information about an available agent."""
    name: str
    type: str

class HealthResponse(BaseResponseModel):
    """Response model for health check endpoint."""
    status: str
    timestamp: datetime
    version: str
    environment: str = "development"  # Default to development if not specified

class DeleteSessionResponse(BaseResponseModel):
    """Response model for session deletion."""
    status: str
    session_id: str
    message: str

class ToolCallModel(BaseResponseModel):
    """Model for a tool call."""
    tool_name: str
    args: Dict
    tool_call_id: str

class ToolOutputModel(BaseResponseModel):
    """Model for a tool output."""
    tool_name: str
    tool_call_id: str
    content: Any

class MessageModel(BaseResponseModel):
    """Model for a single message in the conversation."""
    role: str
    content: str
    assistant_name: Optional[str] = None
    tool_calls: Optional[List[ToolCallModel]] = None
    tool_outputs: Optional[List[ToolOutputModel]] = None

    model_config = ConfigDict(
        exclude_none=True,
        json_schema_extra={"examples": [{"role": "assistant", "content": "Hello!"}]}
    )

class PaginationParams(BaseResponseModel):
    """Pagination parameters."""
    page: int = 1
    page_size: int = 50
    sort_desc: bool = True  # True for most recent first

class SessionResponse(BaseResponseModel):
    """Response model for session retrieval."""
    session_id: str
    messages: List[MessageModel]
    exists: bool
    total_messages: int
    current_page: int
    total_pages: int

class SessionInfo(BaseResponseModel):
    """Information about a session."""
    session_id: str
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    message_count: Optional[int] = None
    agent_name: Optional[str] = None

class SessionListResponse(BaseResponseModel):
    """Response model for listing all sessions."""
    sessions: List[SessionInfo]
    total_count: int
    page: int = 1
    page_size: int = 50
    total_pages: int = 1 