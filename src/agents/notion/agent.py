'''Refactored Notion Agent module following the specialist pattern.

This module defines a NotionAgent class that encapsulates the functionality of the Notion AI Assistant.
'''

import os
import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import logfire
from pydantic_ai import Agent
from src.models.notion import NotionResponse
from src.tools.notion_tools import NotionTools
from config import OPENAI_API_KEY, LOGFIRE_TOKEN
from memory import memory

# Configure Logfire and logging
logfire.configure()

# Set environment variable for OpenAI API key
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

@dataclass
class NotionDeps:
    notion_tools: NotionTools

class NotionAgent:
    """Class for interacting with Notion databases using a natural language interface."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.notion_tools = NotionTools()
        
        # Initialize the Pydantic AI Agent with a system prompt defining Sofia's personality and role
        self.agent = Agent(
            'openai:gpt-4o-mini',
            result_type=NotionResponse,
            system_prompt=(
                "You are Sofia, a friendly AI assistant who helps manage Notion databases. "
                "You have a warm, conversational style and genuinely enjoy helping users organize their work. "
                "You will receive commands in natural language and you should provide helpful responses along with a reasoning."
            )
        )
        
    async def run(self, prompt: str) -> Any:
        """Run the agent asynchronously with the given prompt."""
        self.logger.debug(f"Running NotionAgent with prompt: {prompt}")
        result = await self.agent.run(prompt)
        return result

    def run_sync(self, prompt: str) -> Any:
        """Run the agent synchronously with the given prompt."""
        return asyncio.run(self.run(prompt))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("Enter command: ")
    agent = NotionAgent()
    result = agent.run_sync(prompt)
    print(result) 