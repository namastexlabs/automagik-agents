"""Message history management for Sofia."""

from typing import List, Optional
from pydantic_ai.messages import ModelMessage, UserPromptPart, TextPart, ModelRequest, ModelResponse

class MessageHistory:
    """Maintains a history of messages between the user and the agent."""
    
    def __init__(self):
        self._messages: List[ModelMessage] = []

    def add(self, content: str) -> ModelMessage:
        """Add a user message to history.
        
        Args:
            content: The message content from the user.
            
        Returns:
            The created message object.
        """
        message = ModelRequest(parts=[UserPromptPart(content=content)])
        self._messages.append(message)
        return message

    def add_response(self, content: str) -> ModelMessage:
        """Add an assistant response.
        
        Args:
            content: The response content from the assistant.
            
        Returns:
            The created message object.
        """
        message = ModelResponse(parts=[TextPart(content=content)])
        self._messages.append(message)
        return message

    def remove(self, index: int) -> Optional[ModelMessage]:
        """Remove a message at the given index.
        
        Args:
            index: The index of the message to remove.
            
        Returns:
            The removed message if found, None otherwise.
        """
        if 0 <= index < len(self._messages):
            return self._messages.pop(index)
        return None

    def clear(self) -> None:
        """Clear all messages."""
        self._messages.clear()

    @property
    def messages(self) -> List[ModelMessage]:
        """Get the messages for the API."""
        return self._messages

    def __len__(self) -> int:
        return len(self._messages)

    def __getitem__(self, index: int) -> ModelMessage:
        return self._messages[index]
