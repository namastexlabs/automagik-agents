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
from src.memory.message_store import MessageStore, CacheMessageStore

class MessageHistory:
    """Maintains a history of messages between the user and the agent.
    
    This class integrates with pydantic-ai's message system to maintain context
    across multiple agent runs. It handles system prompts, user messages, and
    assistant responses in a format compatible with pydantic-ai.
    """
    
    # Class-level message store instance
    _store: MessageStore = CacheMessageStore()
    
    @classmethod
    def set_message_store(cls, store: MessageStore) -> None:
        """Set a custom message store implementation.
        
        Args:
            store: The message store implementation to use.
        """
        cls._store = store
    
    def __init__(self, session_id: str, system_prompt: Optional[str] = None):
        """Initialize message history.
        
        Args:
            session_id: Unique identifier for the conversation session.
            system_prompt: Optional system prompt to initialize history with.
        """
        self.session_id = session_id
        if system_prompt:
            self.add_system_prompt(system_prompt)

    def add_system_prompt(self, content: str) -> ModelMessage:
        """Add or update system prompt in history.
        
        Args:
            content: The system prompt content.
            
        Returns:
            The created message object.
        """
        message = ModelRequest(parts=[SystemPromptPart(content=content)])
        self._store.update_system_prompt(self.session_id, content)
        return message

    def add(self, content: str) -> ModelMessage:
        """Add a user message to history.
        
        Args:
            content: The message content from the user.
            
        Returns:
            The created message object.
        """
        message = ModelRequest(parts=[UserPromptPart(content=content)])
        self._store.add_message(self.session_id, message)
        return message

    def add_response(self, content: str) -> ModelMessage:
        """Add an assistant response.
        
        Args:
            content: The response content from the assistant.
            
        Returns:
            The created message object.
        """
        message = ModelResponse(parts=[TextPart(content=content)])
        self._store.add_message(self.session_id, message)
        return message

    def clear(self) -> None:
        """Clear all messages in the current session."""
        self._store.clear_session(self.session_id)

    @property
    def messages(self) -> List[ModelMessage]:
        """Get the messages for the API.
        
        Returns:
            List of messages in pydantic-ai format, including system prompt if present.
        """
        return self._store.get_messages(self.session_id)

    def __len__(self) -> int:
        return len(self.messages)

    def __getitem__(self, index: int) -> ModelMessage:
        return self.messages[index]

    def to_dict(self) -> dict:
        """Convert message history to a dictionary format.
        
        Returns:
            Dictionary containing messages in a format suitable for JSON serialization.
        """
        return {
            "messages": [
                {
                    "role": "system" if any(isinstance(p, SystemPromptPart) for p in msg.parts)
                    else "user" if any(isinstance(p, UserPromptPart) for p in msg.parts)
                    else "assistant",
                    "content": msg.parts[0].content if msg.parts else ""
                }
                for msg in self.messages
            ]
        }
