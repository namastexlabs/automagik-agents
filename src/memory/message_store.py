"""Message storage implementations for Sofia."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    SystemPromptPart
)

class MessageStore(ABC):
    """Abstract interface for message storage."""
    
    @abstractmethod
    def get_messages(self, session_id: str) -> List[ModelMessage]:
        """Retrieve all messages for a session.
        
        Args:
            session_id: The unique session identifier.
            
        Returns:
            List of messages in the session.
        """
        pass
    
    @abstractmethod
    def add_message(self, session_id: str, message: ModelMessage) -> None:
        """Add a message to a session.
        
        Args:
            session_id: The unique session identifier.
            message: The message to add.
        """
        pass
    
    @abstractmethod
    def update_system_prompt(self, session_id: str, system_prompt: str, agent_id: Optional = None) -> None:
        """Update or add the system prompt for a session.
        
        Args:
            session_id: The unique session identifier.
            system_prompt: The new system prompt content.
            agent_id: Optional agent ID associated with the message.
        """
        pass
    
    @abstractmethod
    def clear_session(self, session_id: str) -> None:
        """Clear all messages in a session.
        
        Args:
            session_id: The unique session identifier.
        """
        pass

    @abstractmethod
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists.
        
        Args:
            session_id: The unique session identifier.
            
        Returns:
            True if the session exists, False otherwise.
        """
        pass

class CacheMessageStore(MessageStore):
    """In-memory cache implementation of MessageStore."""
    
    def __init__(self):
        """Initialize the cache store."""
        self._sessions: Dict[str, List[ModelMessage]] = {}
    
    def get_messages(self, session_id: str) -> List[ModelMessage]:
        """Get all messages for a session from cache."""
        return self._sessions.get(session_id, [])
    
    def add_message(self, session_id: str, message: ModelMessage) -> None:
        """Add a message to a session in cache."""
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append(message)
    
    def update_system_prompt(self, session_id: str, system_prompt: str, agent_id: Optional = None) -> None:
        """Update the system prompt for a session in cache."""
        messages = self._sessions.get(session_id, [])
        
        # Remove existing system prompt if present
        messages = [msg for msg in messages if not any(
            isinstance(part, SystemPromptPart) for part in msg.parts
        )]
        
        # Add new system prompt at the beginning
        system_message = ModelRequest(parts=[SystemPromptPart(content=system_prompt)])
        
        # Add agent ID if provided
        if agent_id:
            system_message.agent_id = agent_id
            
        messages.insert(0, system_message)
        
        self._sessions[session_id] = messages
    
    def clear_session(self, session_id: str) -> None:
        """Clear a session from cache."""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists in cache."""
        return session_id in self._sessions 