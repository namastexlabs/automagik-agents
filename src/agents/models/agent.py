from pydantic import BaseModel
from typing import Optional, List, Any

from src.memory.message_history import MessageHistory

class AgentBaseResponse(BaseModel):
    message: str
    history: MessageHistory
    error: Optional[str] = None
    tool_calls: Optional[List[Any]] = None
    tool_outputs: Optional[List[Any]] = None