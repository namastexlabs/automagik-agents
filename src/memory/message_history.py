"""Message history management for Sofia."""

from typing import List, Optional
from pydantic_ai.messages import (
    ModelMessage, 
    UserPromptPart, 
    TextPart, 
    ModelRequest, 
    ModelResponse,
    SystemPromptPart
)

class MessageHistory:
    """Maintains a history of messages between the user and the agent.
    
    This class integrates with pydantic-ai's message system to maintain context
    across multiple agent runs. It handles system prompts, user messages, and
    assistant responses in a format compatible with pydantic-ai.
    """
    
    def __init__(self, system_prompt: Optional[str] = None):
        """Initialize message history.
        
        Args:
            system_prompt: Optional system prompt to initialize history with.
        """
        self._messages: List[ModelMessage] = []
        if system_prompt:
            self.add_system_prompt(system_prompt)

    def add_system_prompt(self, content: str) -> ModelMessage:
        """Add a system prompt to history.
        
        Args:
            content: The system prompt content.
            
        Returns:
            The created message object.
        """
        message = ModelRequest(parts=[SystemPromptPart(content=content)])
        self._messages.append(message)
        return message

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
        """Get the messages for the API.
        
        Returns:
            List of messages in pydantic-ai format, including system prompt if present.
        """
        return self._messages

    def __len__(self) -> int:
        return len(self._messages)

    def __getitem__(self, index: int) -> ModelMessage:
        return self._messages[index]
