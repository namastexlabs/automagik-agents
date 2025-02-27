from pydantic import BaseModel
from typing import Optional, List, Any, Dict

class StanAgentResponse(BaseModel):
    message: str
    user_state: Optional[str] = None  # NOT_REGISTERED, PENDING, or APPROVED
    client_info: Optional[Dict[str, Any]] = None
    tool_calls: Optional[List[Any]] = None
    tool_outputs: Optional[List[Any]] = None
