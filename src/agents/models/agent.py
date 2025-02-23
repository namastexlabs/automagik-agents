from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any, Dict

from src.memory.message_history import MessageHistory
from pydantic_ai.messages import SystemPromptPart, UserPromptPart, ModelResponse, ModelRequest

class MessageModel(BaseModel):
    role: str
    content: str

class HistoryModel(BaseModel):
    messages: List[MessageModel]

    @classmethod
    def from_message_history(cls, history: MessageHistory):
        messages = []
        for msg in history._messages:
            if isinstance(msg, SystemPromptPart):
                messages.append(MessageModel(role="system", content=msg.system_prompt))
            elif isinstance(msg, UserPromptPart):
                messages.append(MessageModel(role="user", content=msg.prompt))
            elif isinstance(msg, ModelResponse):
                # Extract just the text content from ModelResponse
                content = ""
                for part in msg.parts:
                    if hasattr(part, "content"):
                        content += part.content
                messages.append(MessageModel(role="assistant", content=content))
            elif isinstance(msg, ModelRequest):
                # Process each part of the ModelRequest separately
                for part in msg.parts:
                    if isinstance(part, SystemPromptPart):
                        messages.append(MessageModel(role="system", content=part.content))
                    elif isinstance(part, UserPromptPart):
                        messages.append(MessageModel(role="user", content=part.content))
            else:
                # For any other type, try to get content or convert to string
                content = getattr(msg, "content", str(msg))
                role = getattr(msg, "role", "unknown")
                messages.append(MessageModel(role=role, content=content))
        
        return cls(messages=messages)

class AgentBaseResponse(BaseModel):
    message: str
    history: HistoryModel
    error: Optional[str] = None
    tool_calls: Optional[List[Any]] = None
    tool_outputs: Optional[List[Any]] = None

    @classmethod
    def from_agent_response(cls, message: str, history: MessageHistory, error: Optional[str] = None, 
                          tool_calls: Optional[List[Any]] = None, tool_outputs: Optional[List[Any]] = None):
        history_model = HistoryModel.from_message_history(history)
        return cls(
            message=message,
            history=history_model,
            error=error,
            tool_calls=tool_calls,
            tool_outputs=tool_outputs
        )