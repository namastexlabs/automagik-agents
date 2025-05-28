"""Common evolution-related functionality.

Originally defined for simple agents, so that every agent can import it from a
central location instead of defining it in each agent class.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class EvolutionMessagePayload(BaseModel):
    """Payload model for Evolution (WhatsApp) webhook messages."""
    
    instance: Optional[str] = None
    phoneNumber: Optional[str] = None
    remoteJid: Optional[str] = None
    
    def get_user_number(self) -> Optional[str]:
        """Get the user's phone number from the payload."""
        return self.phoneNumber or self.remoteJid

__all__ = [
    "EvolutionMessagePayload",
] 