"""Message history management for Sofia."""

from typing import List, Optional, Dict, Any, Union
import json
from pydantic import BaseModel, field_validator
from pydantic_ai.messages import (
    ModelMessage, 
    UserPromptPart, 
    TextPart as BaseTextPart, 
    ModelRequest, 
    ModelResponse,
    SystemPromptPart
)
from src.memory.message_store import MessageStore, CacheMessageStore
from datetime import datetime

class TextPart(BaseTextPart):
    """Custom TextPart that includes assistant name."""
    def __init__(self, content: str, assistant_name: Optional[str] = None):
        super().__init__(content)
        self.assistant_name = assistant_name
        self.part_kind = "text"

class ToolCall(BaseModel):
    """Model for a tool call."""
    tool_name: str
    args: Union[str, Dict]
    tool_call_id: str

    @field_validator('args')
    @classmethod
    def parse_args(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {}
        return v

class ToolOutput(BaseModel):
    """Model for a tool output."""
    tool_name: str
    tool_call_id: str
    content: Any

class ToolCallPart(BaseTextPart):
    """Part representing a tool call in a message."""
    def __init__(self, tool_call: ToolCall):
        super().__init__(content=tool_call.tool_name)
        self.tool_call = tool_call
        self.part_kind = "tool-call"

class ToolOutputPart(BaseTextPart):
    """Part representing a tool output in a message."""
    def __init__(self, tool_output: ToolOutput):
        super().__init__(content=str(tool_output.content))
        self.tool_output = tool_output
        self.part_kind = "tool-output"

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

    def add_response(self, content: str, assistant_name: str = None, tool_calls: List[Dict] = None, tool_outputs: List[Dict] = None) -> ModelMessage:
        """Add an assistant response.
        
        Args:
            content: The response content from the assistant.
            assistant_name: The name of the assistant providing the response.
            tool_calls: Optional list of tool calls made during processing.
            tool_outputs: Optional list of outputs from tool calls.
            
        Returns:
            The created message object.
        """
        # Create base text part with content and assistant name if provided
        text_part = TextPart(content=content)
        if assistant_name:
            text_part.assistant_name = assistant_name
        parts = [text_part]
        
        # Add only non-empty tool calls
        if tool_calls:
            for tool_call in tool_calls:
                if tool_call.get('tool_name'):  # Only add if tool_name is present and non-empty
                    parts.append(ToolCallPart(tool_call=ToolCall(**tool_call)))
        
        # Add only non-empty tool outputs
        if tool_outputs:
            for tool_output in tool_outputs:
                if tool_output.get('content'):  # Only add if content is present and non-empty
                    parts.append(ToolOutputPart(tool_output=ToolOutput(**tool_output)))
        
        message = ModelResponse(parts=parts)
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

    def update_messages(self, messages: List[ModelMessage]) -> None:
        """Update all messages in the store.
        
        Args:
            messages: New list of messages to store
        """
        self._store.clear_session(self.session_id)
        for message in messages:
            self._store.add_message(self.session_id, message)

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
                {k: v for k, v in {
                    "role": "system" if any(isinstance(p, SystemPromptPart) for p in msg.parts)
                    else "user" if any(isinstance(p, UserPromptPart) for p in msg.parts)
                    else "assistant",
                    "content": msg.parts[0].content if msg.parts else "",
                    **({"assistant_name": getattr(msg.parts[0], "assistant_name", None)}
                        if any(isinstance(p, TextPart) for p in msg.parts) 
                        and not any(isinstance(p, (SystemPromptPart, UserPromptPart)) for p in msg.parts)
                        and getattr(msg.parts[0], "assistant_name", None) is not None
                        else {}),
                    **({"tool_calls": [
                        {k: v for k, v in p.tool_call.dict().items() if v is not None}
                        for p in msg.parts if isinstance(p, ToolCallPart)
                    ]} if any(isinstance(p, ToolCallPart) for p in msg.parts) else {}),
                    **({"tool_outputs": [
                        {k: v for k, v in p.tool_output.dict().items() if v is not None}
                        for p in msg.parts if isinstance(p, ToolOutputPart)
                    ]} if any(isinstance(p, ToolOutputPart) for p in msg.parts) else {})
                }.items() if v is not None and (not isinstance(v, list) or v)}
                for msg in self.messages
            ]
        }

    def get_filtered_messages(self, message_limit: Optional[int] = None, sort_desc: bool = True) -> List[ModelMessage]:
        """Get filtered messages with optional limit and sorting.
        
        Args:
            message_limit: Optional limit on number of non-system messages to return
            sort_desc: Whether to sort by most recent first
            
        Returns:
            List of messages, optionally filtered and sorted
        """
        messages = self.messages
        system_prompt = next((msg for msg in messages if any(isinstance(p, SystemPromptPart) for p in msg.parts)), None)
        non_system_messages = [msg for msg in messages if not any(isinstance(p, SystemPromptPart) for p in msg.parts)]
        
        # Sort messages by recency
        sorted_messages = sorted(
            non_system_messages,
            key=lambda x: getattr(x, 'timestamp', datetime.min).timestamp() if isinstance(getattr(x, 'timestamp', None), datetime) else float(getattr(x, 'timestamp', 0)),
            reverse=sort_desc  # Sort based on sort_desc parameter
        )
        
        # Apply limit if specified
        if message_limit is not None:
            if sort_desc:
                sorted_messages = sorted_messages[:message_limit]
            else:
                sorted_messages = sorted_messages[-message_limit:]
        
        # Always put system prompt at the start for context
        return ([system_prompt] if system_prompt else []) + (sorted_messages if not sort_desc else list(reversed(sorted_messages)))

    def get_paginated_messages(
        self,
        page: int = 1,
        page_size: int = 50,
        sort_desc: bool = True
    ) -> tuple[List[ModelMessage], int, int, int]:
        """Get paginated messages with sorting.
        
        Args:
            page: Page number (1-based)
            page_size: Number of messages per page
            sort_desc: Sort by most recent first if True
            
        Returns:
            Tuple of (paginated messages, total messages, current page, total pages)
        """
        messages = self.messages
        system_prompt = next((msg for msg in messages if any(isinstance(p, SystemPromptPart) for p in msg.parts)), None)
        non_system_messages = [msg for msg in messages if not any(isinstance(p, SystemPromptPart) for p in msg.parts)]
        
        # Sort messages by timestamp
        sorted_messages = sorted(
            non_system_messages,
            key=lambda x: getattr(x, 'timestamp', datetime.min).timestamp() if isinstance(getattr(x, 'timestamp', None), datetime) else float(getattr(x, 'timestamp', 0)),
            reverse=sort_desc  # Sort based on sort_desc parameter
        )
        
        # Calculate pagination
        total_messages = len(sorted_messages)
        total_pages = (total_messages + page_size - 1) // page_size
        current_page = max(1, min(page, total_pages))
        start_idx = (current_page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Get paginated messages
        paginated = sorted_messages[start_idx:end_idx]
        
        # Always put system prompt at the start for context
        final_messages = ([system_prompt] if system_prompt else []) + (paginated if not sort_desc else list(reversed(paginated)))
        
        return final_messages, total_messages, current_page, total_pages

    def format_message_for_api(self, msg: ModelMessage, hide_tools: bool = False) -> Optional[Dict]:
        """Format a single message for API response.
        
        Args:
            msg: The message to format
            hide_tools: Whether to exclude tool calls and outputs
            
        Returns:
            Formatted message dictionary or None if message should be skipped
        """
        if not msg.parts:
            return None

        # Determine message role
        role = "system" if any(isinstance(p, SystemPromptPart) for p in msg.parts) else \
               "user" if any(isinstance(p, UserPromptPart) for p in msg.parts) else \
               "assistant"

        # Start with minimal message data
        message_data = {
            "role": role,
            "content": msg.parts[0].content
        }

        # Only add assistant-specific fields for assistant messages
        if role == "assistant":
            assistant_name = getattr(msg.parts[0], "assistant_name", None)
            if assistant_name:
                message_data["assistant_name"] = assistant_name

            if not hide_tools:
                # Add non-empty tool calls
                tool_calls = [
                    {k: v for k, v in {
                        "tool_name": part.tool_call.tool_name,
                        "args": part.tool_call.args,
                        "tool_call_id": part.tool_call.tool_call_id
                    }.items() if v is not None}
                    for part in msg.parts 
                    if isinstance(part, ToolCallPart) and part.tool_call.tool_name
                ]
                if tool_calls:
                    message_data["tool_calls"] = tool_calls

                # Add non-empty tool outputs
                tool_outputs = [
                    {k: v for k, v in {
                        "tool_name": part.tool_output.tool_name,
                        "tool_call_id": part.tool_output.tool_call_id,
                        "content": part.tool_output.content
                    }.items() if v is not None}
                    for part in msg.parts 
                    if isinstance(part, ToolOutputPart) and part.tool_output.content
                ]
                if tool_outputs:
                    message_data["tool_outputs"] = tool_outputs

        return {k: v for k, v in message_data.items() if v is not None}
