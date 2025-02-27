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
import logging
import uuid

logger = logging.getLogger(__name__)

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
    
    def __init__(self, session_id: str, system_prompt: Optional[str] = None, user_id: int = 1):
        """Initialize a new message history for a session.
        
        Args:
            session_id: The unique session identifier.
            system_prompt: Optional system prompt to set at initialization.
            user_id: The user identifier to associate with this session (defaults to 1).
        """
        self.session_id = session_id
        self.user_id = user_id  # Store as integer
        
        # Add system prompt if provided
        if system_prompt:
            self.add_system_prompt(system_prompt)
    
    def add_system_prompt(self, content: str, agent_id: Optional[Union[int, str]] = None) -> ModelMessage:
        """Add or update the system prompt for this conversation.
        
        Args:
            content: The system prompt content.
            agent_id: Optional agent ID associated with the message.
            
        Returns:
            The created system prompt message.
        """
        message = ModelRequest(parts=[SystemPromptPart(content=content)])
        
        # Add agent ID if provided
        if agent_id:
            message.agent_id = agent_id
        
        # Add user_id to the message
        message.user_id = self.user_id
        
        # Don't try to create a session if it doesn't exist - the API should handle this
        if not self.session_id:
            logger.warning("Empty session_id provided to add_system_prompt, this may cause issues")
        
        # Store the user_id and agent_id attributes in the pg_message_store implementation directly
        # This is a workaround to avoid modifying the MessageStore interface
        from src.memory.pg_message_store import PostgresMessageStore
        if isinstance(self._store, PostgresMessageStore):
            # PostgresMessageStore implementation accepts user_id
            self._store.update_system_prompt(self.session_id, content, agent_id, self.user_id)
        else:
            # For other implementations that follow the base interface
            self._store.update_system_prompt(self.session_id, content, agent_id)
        return message
    
    def add(self, content: str, agent_id: Optional[Union[int, str]] = None, context: Optional[Dict] = None) -> ModelMessage:
        """Add a user message to the history.
        
        Args:
            content: The message content.
            agent_id: Optional agent ID associated with the message.
            context: Optional context data (like channel_payload) to include with the message.
            
        Returns:
            The created user message.
        """
        message = ModelRequest(parts=[UserPromptPart(content=content)])
        
        # Add agent ID if provided
        if agent_id:
            message.agent_id = agent_id
            
        # Add user_id to the message
        message.user_id = self.user_id
        
        # Add context if provided
        if context:
            message.context = context
        
        # Don't try to create a session if it doesn't exist - the API should handle this
        if not self.session_id:
            logger.warning("Empty session_id provided to add, this may cause issues")
            
        # Pass only the required parameters to match the interface
        self._store.add_message(self.session_id, message)
        
        return message
    
    def add_response(
        self, 
        content: str, 
        assistant_name: Optional[str] = None, 
        tool_calls: List[Dict] = None, 
        tool_outputs: List[Dict] = None,
        agent_id: Optional[Union[int, str]] = None,
        system_prompt: Optional[str] = None
    ) -> ModelMessage:
        """Add an assistant response to the history.
        
        Args:
            content: The response content.
            assistant_name: Optional name of the assistant.
            tool_calls: Optional list of tool calls made during processing.
            tool_outputs: Optional list of outputs from tool calls.
            agent_id: Optional agent ID associated with the message.
            system_prompt: Optional system prompt to include with the response.
            
        Returns:
            The created assistant response message.
        """
        # Create a text part with the assistant name
        text_part = TextPart(content=content, assistant_name=assistant_name)
        
        # Start with the text part
        parts = [text_part]
        
        # Add tool call parts if any
        if tool_calls:
            for tc in tool_calls:
                if tc and isinstance(tc, dict) and tc.get("tool_name"):
                    try:
                        tool_call = ToolCall(
                            tool_name=tc.get("tool_name"),
                            args=tc.get("args", {}),
                            tool_call_id=tc.get("tool_call_id", "")
                        )
                        parts.append(ToolCallPart(tool_call=tool_call))
                    except Exception as e:
                        logger.error(f"Error creating ToolCallPart: {str(e)}")
        
        # Add tool output parts if any
        if tool_outputs:
            for to in tool_outputs:
                if to and isinstance(to, dict) and to.get("tool_name"):
                    try:
                        tool_output = ToolOutput(
                            tool_name=to.get("tool_name"),
                            tool_call_id=to.get("tool_call_id", ""),
                            content=to.get("content", "")
                        )
                        parts.append(ToolOutputPart(tool_output=tool_output))
                    except Exception as e:
                        logger.error(f"Error creating ToolOutputPart: {str(e)}")
        
        # Create the response message
        message = ModelResponse(parts=parts)
        
        # Add agent ID if provided
        if agent_id:
            message.agent_id = agent_id
            
        # Add system prompt if provided
        if system_prompt:
            message.system_prompt = system_prompt
        
        # Add the message to the store
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

    def to_dict(self) -> Dict[str, List[Dict[str, Any]]]:
        """Convert the message history to a dictionary.
        
        Returns:
            Dictionary representation of the message history.
        """
        try:
            result = {"messages": []}
            
            for message in self.messages:
                if not message or not hasattr(message, "parts") or not message.parts:
                    logger.warning("Skipping invalid message in to_dict")
                    continue
                    
                # Determine role based on message parts
                role = "assistant"  # default role
                
                if any(isinstance(p, SystemPromptPart) for p in message.parts):
                    role = "system"
                elif any(isinstance(p, UserPromptPart) for p in message.parts):
                    role = "user"
                
                # Extract content from message parts, handling TextPart specially
                content = ""
                for part in message.parts:
                    if isinstance(part, TextPart):
                        content = part.content
                        break
                
                # Create the message dictionary with basic properties
                message_dict = {
                    "role": role,
                    "content": content
                }
                
                # If it's an assistant message, add assistant_name if available
                if role == "assistant":
                    for part in message.parts:
                        if isinstance(part, TextPart) and hasattr(part, "assistant_name") and part.assistant_name:
                            message_dict["assistant_name"] = part.assistant_name
                            break
                
                # Add tool calls if any
                tool_calls = []
                for part in message.parts:
                    if isinstance(part, ToolCallPart):
                        try:
                            tool_calls.append({
                                "tool_name": part.tool_call.tool_name,
                                "args": part.tool_call.args,
                                "tool_call_id": part.tool_call.tool_call_id
                            })
                        except Exception as e:
                            logger.error(f"Error serializing tool call: {str(e)}")
                
                if tool_calls:
                    message_dict["tool_calls"] = tool_calls
                
                # Add tool outputs if any
                tool_outputs = []
                for part in message.parts:
                    if isinstance(part, ToolOutputPart):
                        try:
                            tool_outputs.append({
                                "tool_name": part.tool_output.tool_name,
                                "tool_call_id": part.tool_output.tool_call_id,
                                "content": part.tool_output.content
                            })
                        except Exception as e:
                            logger.error(f"Error serializing tool output: {str(e)}")
                
                if tool_outputs:
                    message_dict["tool_outputs"] = tool_outputs
                
                # Remove any None or empty list values
                message_dict = {k: v for k, v in message_dict.items() if v is not None and v != []}
                
                result["messages"].append(message_dict)
            
            return result
        except Exception as e:
            logger.error(f"Error in to_dict: {str(e)}")
            return {"messages": [{"role": "system", "content": "Error converting message history"}]}

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

    def format_message_for_api(self, message: ModelMessage, hide_tools: bool = False) -> Dict[str, Any]:
        """Format a message for API responses.
        
        Args:
            message: The message to format.
            hide_tools: Whether to hide tool calls and outputs in the formatted message.
            
        Returns:
            Formatted message dictionary for API response.
        """
        try:
            if not message or not hasattr(message, "parts") or not message.parts:
                logger.warning("Missing or invalid message in format_message_for_api")
                return {"role": "system", "content": "Error: Missing message data"}
            
            # Determine role based on message parts
            role = "assistant"  # default role
            
            if any(isinstance(p, SystemPromptPart) for p in message.parts):
                role = "system"
            elif any(isinstance(p, UserPromptPart) for p in message.parts):
                role = "user"
            
            # Extract content from message parts, handling TextPart specially
            content = ""
            for part in message.parts:
                if isinstance(part, TextPart):
                    content = part.content
                    break
            
            # Initialize with basic properties
            message_data = {
                "role": role,
                "content": content
            }
            
            # If it's an assistant message, add assistant_name if available
            if role == "assistant":
                for part in message.parts:
                    if isinstance(part, TextPart) and hasattr(part, "assistant_name") and part.assistant_name:
                        message_data["assistant_name"] = part.assistant_name
                        break
            
            # Add tool calls if any and not hidden
            if not hide_tools:
                tool_calls = []
                for part in message.parts:
                    if isinstance(part, ToolCallPart):
                        try:
                            tool_calls.append({
                                "tool_name": part.tool_call.tool_name,
                                "args": part.tool_call.args,
                                "tool_call_id": part.tool_call.tool_call_id
                            })
                        except Exception as e:
                            logger.error(f"Error processing tool call in format_message_for_api: {str(e)}")
                
                if tool_calls:
                    message_data["tool_calls"] = tool_calls
                
                # Add tool outputs if any
                tool_outputs = []
                for part in message.parts:
                    if isinstance(part, ToolOutputPart):
                        try:
                            tool_outputs.append({
                                "tool_name": part.tool_output.tool_name,
                                "tool_call_id": part.tool_output.tool_call_id,
                                "content": part.tool_output.content
                            })
                        except Exception as e:
                            logger.error(f"Error processing tool output in format_message_for_api: {str(e)}")
                
                if tool_outputs:
                    message_data["tool_outputs"] = tool_outputs
            
            # Remove any None or empty list values
            return {k: v for k, v in message_data.items() if v is not None and v != []}
        except Exception as e:
            logger.error(f"Error in format_message_for_api: {str(e)}")
            return {"role": "system", "content": "Error formatting message"}
