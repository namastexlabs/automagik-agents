import json
import logging
import os
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

# Suppress logfire warning
os.environ['LOGFIRE_IGNORE_NO_CONFIG'] = '1'

from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage, UserPromptPart, TextPart, ModelRequest, ModelResponse
from src.agents.simple_agent.models.response import SimpleAgentResponse

# Configure prettier logging
class PrettyFormatter(logging.Formatter):
    def format(self, record):
        # Add color based on level
        colors = {
            logging.INFO: '\033[92m',  # Green
            logging.ERROR: '\033[91m',  # Red
            logging.WARNING: '\033[93m',  # Yellow
            logging.DEBUG: '\033[94m'  # Blue
        }
        reset = '\033[0m'
        color = colors.get(record.levelno, '')
        
        # Format the message
        if isinstance(record.msg, (dict, list)):
            record.msg = json.dumps(record.msg, indent=2)
        
        # Simplified format: just emoji + message
        emoji = '🤖' if 'Agent' in record.name else '📝'
        return f"{color}{emoji} {record.msg}{reset}"

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(PrettyFormatter())
logger.handlers = [handler]  # Replace any existing handlers

# Disable httpx logging
logging.getLogger('httpx').setLevel(logging.WARNING)

class MessageHistory:
    def __init__(self):
        self._messages: List[ModelMessage] = []

    def add(self, content: str) -> ModelMessage:
        """Add a user message to history."""
        message = ModelRequest(parts=[UserPromptPart(content=content)])
        self._messages.append(message)
        return message

    def add_response(self, content: str) -> ModelMessage:
        """Add an assistant response."""
        message = ModelResponse(parts=[TextPart(content=content)])
        self._messages.append(message)
        return message

    def remove(self, index: int) -> Optional[ModelMessage]:
        """Remove a message at the given index."""
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

@dataclass
class Deps:
    # Add any dependencies your agent might need
    pass

class SimpleAgent:
    def __init__(self, config: Dict[str, str]):
        self.agent = Agent(
            'openai:gpt-4o-mini',
            system_prompt=(
                "You are a helpful assistant that can provide information about dates and remember user information. "
                "Use the provided tool to get the current date when asked. "
                "Remember and use the user's name if they provide it."
            ),
            deps_type=Deps
        )
        self.deps = Deps()
        self.message_history = MessageHistory()

    @staticmethod
    async def get_current_date(ctx: RunContext[Deps]) -> str:
        """Get the current date in ISO format (YYYY-MM-DD)."""
        return datetime.now().date().isoformat()

    async def process_message(self, user_message: str) -> SimpleAgentResponse:
        # Add the user message
        self.message_history.add(user_message)
        
        # Run the agent and stream response
        async with self.agent.run_stream(
            user_message, 
            deps=self.deps, 
            message_history=self.message_history.messages
        ) as result:
            # Get the last streamed response
            response_text = ""
            last_text = ""
            async for text in result.stream():
                # Only add new text that hasn't been seen
                if text not in last_text:
                    response_text = text
                last_text = text
            
            # Add the assistant response
            self.message_history.add_response(response_text)
            
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug({
                    'history': [
                        {
                            'type': msg.kind,
                            'content': [p.content for p in msg.parts]
                        } for msg in self.message_history.messages
                    ]
                })
            
            return SimpleAgentResponse(
                message=response_text,
                error=None
            )
        
        return SimpleAgentResponse(
            message=result.data,
            tool_calls=getattr(result, 'tool_calls', None),
            tool_outputs=getattr(result, 'tool_outputs', None)
        )

    def get_all_messages(self) -> List[Dict[str, str]]:
        # Return the message history parsed from string content
        messages = []
        for msg in self.message_history:
            if msg.startswith("User:"):
                messages.append({"role": "user", "content": msg[len("User:"):].strip()})
            elif msg.startswith("Assistant:"):
                messages.append({"role": "assistant", "content": msg[len("Assistant:"):].strip()})
            else:
                messages.append({"role": "unknown", "content": msg})
        return messages
