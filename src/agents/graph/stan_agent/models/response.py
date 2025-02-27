"""Response models for the Stan agent."""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class StanAgentResponse(BaseModel):
    """Response model for the Stan agent."""
    message: str
    user_state: str = "NOT_REGISTERED"  # NOT_REGISTERED, REJECTED, APPROVED, VERIFYING
    client_info: Optional[Dict[str, Any]] = None
    cnpj_data: Optional[Dict[str, Any]] = None
    backoffice_consulted: bool = False
    product_consulted: bool = False
    actions_taken: List[str] = Field(default_factory=list)
    
    class Config:
        """Pydantic model configuration."""
        arbitrary_types_allowed = True 