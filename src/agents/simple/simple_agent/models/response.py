from pydantic import BaseModel
from typing import Optional, List, Any

class SimpleAgentResponse(BaseModel):
    message: str
    tool_calls: Optional[List[Any]] = None
    tool_outputs: Optional[List[Any]] = None
