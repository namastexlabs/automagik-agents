from pydantic import BaseModel
from typing import Optional, List, Any

class SofiaAgentResponse(BaseModel):
    message: str
    tool_calls: Optional[List[Any]] = None
    tool_outputs: Optional[List[Any]] = None
