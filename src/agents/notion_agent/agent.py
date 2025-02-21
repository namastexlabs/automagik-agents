import logging
from dataclasses import dataclass
from typing import Dict

from pydantic_ai import Agent
from src.agents.notion_agent.prompts.prompt import NOTION_AGENT_PROMPT
from src.agents.notion_agent.models.response import AgentResponse
from src.memory.message_history import MessageHistory

@dataclass
class Deps:
    # Add any dependencies your agent might need
    pass

class NotionAgent:
    def __init__(self, config: Dict[str, str]):
        self.agent = Agent(
            'openai:gpt-4o-mini',
            system_prompt=NOTION_AGENT_PROMPT,
            deps_type=Deps
        )
        self.deps = Deps()
        self.message_history = MessageHistory(system_prompt=NOTION_AGENT_PROMPT)
        self.register_tools()

    def register_tools(self):
        """Register tools with the agent."""
        from src.tools.datetime_tools import get_current_date, get_current_time
        self.agent.tool(get_current_date)
        self.agent.tool(get_current_time)

    async def process_message(self, user_message: str) -> AgentResponse:
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
            
            return AgentResponse(
                message=response_text,
                error=None
            )
        