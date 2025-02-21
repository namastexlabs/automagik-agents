from pydantic import BaseModel


class NotionResponse(BaseModel):
    """Response model for the NotionAgent containing reasoning and a final message."""
    reasoning: str
    message: str 