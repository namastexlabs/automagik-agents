"""CLI Agent for interacting with Notion databases."""
import asyncio
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime, timezone
from agent_models import AgentResponse
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelRequest, ModelResponse, TextPart, UserPromptPart
import logfire
from notion_tools import NotionTools
from notion_models import (
    DatabaseListItem, DatabaseSchema, PeopleFilter,
    QueryFilter, DatabaseQuery, PageProperties, PageResponse
)
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich import print as rprint
from config import OPENAI_API_KEY, LOGFIRE_TOKEN
from memory import memory
import os

# Configure Logfire
logfire.configure()

# Also set up standard logging for console output
console_logger = logging.getLogger(__name__)
console_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_logger.addHandler(console_handler)

# Set OpenAI API key for the environment
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

@dataclass
class NotionDeps:
    notion_tools: NotionTools

# Create the agent
notion_agent = Agent(
    'openai:gpt-4o-mini',
    result_type=AgentResponse,
    system_prompt="""You are Sofia, a friendly AI assistant who helps manage Notion databases. You have a warm, conversational style and genuinely enjoy helping users organize their work.

You will receive a conversation history in the format:
[
    {"role": "user", "content": "user message"},
    {"role": "ai", "content": "your response"}
]

Use this history to maintain context and remember important information like the user's name.

You must ALWAYS return responses in the following JSON format:
{
    "reasoning": "Your internal thought process about how to handle the request (optional)",
    "message": "The actual response message to show to the user (required)"
}
    
    Your personality:
    - You are Sofia, a friendly and helpful AI assistant
    - You have a warm and engaging personality
    - You remember users' names and preferences
    - You speak in the same language as the user (e.g., Portuguese if they speak Portuguese)
    - You're knowledgeable about Notion and databases
    - Friendly and approachable - use casual language and emojis occasionally
    - Proactive - anticipate user needs and make helpful suggestions
    - Clear and organized - present information in a clean, readable format
    
    When interacting:
    - Greet users warmly and acknowledge their requests
    - Explain what you're doing in simple terms
    - After showing information, suggest relevant next steps
    - Keep responses concise but friendly
    
    Example response style:
    'Hi! Of course I can help you with that! Let me check your databases... Here's what I found:
    [info in clean markdown format]
    Would you like to see what's inside any of these? Or I can help you create something new!'
    """,
    deps_type=NotionDeps,
    retries=2,
)

@notion_agent.tool
async def list_databases(ctx: RunContext[NotionDeps]) -> List[Dict[str, Any]]:
    """List all available Notion databases."""
    databases = await ctx.deps.notion_tools.list_databases()
    return [db.model_dump() for db in databases]

@notion_agent.tool
async def get_database_schema(ctx: RunContext[NotionDeps], database_id: str) -> Dict[str, Any]:
    """Get the schema for a specific database."""
    schema = await ctx.deps.notion_tools.get_database_schema(database_id)
    return schema.model_dump()

@notion_agent.tool
async def query_database(ctx: RunContext[NotionDeps], database_id: str, filter_type: str = None, filter_value: str = None, property_name: str = None) -> List[Dict[str, Any]]:
    """Query items from a database with optional filters.
    
    Args:
        database_id: The ID of the database to query
        filter_type: Type of filter (e.g., 'person', 'text', 'select', 'status')
        filter_value: Value to filter by
        property_name: Name of the property to filter on
    
    Example:
        To find tasks assigned to Cezar:
        query_database(database_id="...", filter_type="person", filter_value="Cezar", property_name="Assignee")
    """
    if filter_type and filter_value:
        filter_by = {
            "text": filter_type,
            "value": filter_value,
            "property": property_name
        }
    else:
        filter_by = None
        
    return await ctx.deps.notion_tools.query_database(
        database_id=database_id,
        filter_by=filter_by
    )

@notion_agent.tool
async def create_page(ctx: RunContext[NotionDeps], page: PageProperties) -> Dict[str, Any]:
    """Create a new page in a database."""
    response = await ctx.deps.notion_tools.create_page(
        database_id=page.database_id,
        properties=page.properties
    )
    return response.model_dump()

@notion_agent.tool
async def update_page(ctx: RunContext[NotionDeps], page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing page in a database."""
    response = await ctx.deps.notion_tools.update_page(page_id, properties)
    return response.model_dump()

@notion_agent.tool
async def delete_page(ctx: RunContext[NotionDeps], page_id: str) -> Dict[str, Any]:
    """Archive/delete a page from a database."""
    response = await ctx.deps.notion_tools.delete_page(page_id)
    return response.model_dump()

class NotionAgent:
    def __init__(self):
        self.console = Console()
        self.notion_tools = NotionTools()
        
        # Cache for database info
        self._databases: Dict[str, Dict[str, Any]] = {}

    async def refresh_database_cache(self):
        """Refresh the cache of database information."""
        databases = await self.notion_tools.list_databases()
        self._databases = {db.title: db.model_dump() for db in databases}
        
    def format_data(self, data: Any) -> str:
        """Format data for display."""
        if isinstance(data, (dict, list)):
            return json.dumps(data, indent=2)
        return str(data)

    async def handle_command(self, command: str):
        """Handle a user command."""
        logfire.debug("Command received", command=command, component="NotionAgent", action="handle_command")
        
        # Add message to memory and get conversation history
        memory.add_message('user', command)
        conversation = memory.get_messages()
        logfire.debug("Added user message to memory", command=command, conversation=conversation)
        
        cmd_lower = command.lower()

        # Prepare message
        message = command
        
        logfire.debug(
            "Prepared message for agent", 
            message=message,
            component="NotionAgent",
            action="prepare_message"
        )
        
        try:
            # Create dependencies
            deps = NotionDeps(notion_tools=self.notion_tools)
            
            # Get conversation history and convert to ModelMessages
            history = []
            for msg in memory.get_messages():
                timestamp = datetime.now(tz=timezone.utc)
                if msg['role'] == 'user':
                    history.append(ModelRequest(parts=[UserPromptPart(content=msg['content'], timestamp=timestamp)]))
                else:
                    history.append(ModelResponse(parts=[TextPart(msg['content'])], timestamp=timestamp))
            
            # Get response from agent
            logfire.debug("Calling agent", component="NotionAgent", action="run_agent", conversation=history)
            result = await notion_agent.run(user_prompt=message, deps=deps, message_history=history)
            
            # Extract response data
            response_data = result.data if hasattr(result, 'data') else str(result)
            
            # Try to parse as JSON if it's a string
            if isinstance(response_data, str):
                try:
                    import json
                    response_data = json.loads(response_data)
                except json.JSONDecodeError:
                    # If not JSON, wrap in message field
                    response_data = {"message": response_data}
            
            # Parse and validate response
            response = AgentResponse.model_validate(response_data)
            logfire.debug(
                "Agent response received",
                response_type=type(response).__name__,
                has_reasoning=bool(response.reasoning),
                component="NotionAgent",
                action="process_response"
            )
            
            # Store AI response in memory
            memory.add_message('ai', response.message)
            
            # Display the response
            if response.reasoning:
                logfire.debug("Agent reasoning", reasoning=response.reasoning)
            self.console.print(Markdown(response.message))
        except Exception as e:
            logfire.error(
                "Error handling command",
                error=str(e),
                error_type=type(e).__name__,
                component="NotionAgent",
                action="handle_error",
                exc_info=True
            )
            self.console.print(f"[red]Error:[/] {str(e)}")

    async def interactive_session(self):
        """Start an interactive session with the user."""
        self.console.print(Markdown("# 🤖 Notion Assistant\n"))
        self.console.print("""I can help you manage your Notion databases. Try commands like:
- List all databases
- Show items in [database name]
- Create a new item in [database name]
- Update item [id] in [database name]
- What properties does [database name] have?

Type 'exit' or 'quit' to end the session.
""")
        
        while True:
            try:
                command = Prompt.ask("\n[bold blue]Input:[/]")
                
                if command.lower() in ('exit', 'quit'):
                    self.console.print("\nGoodbye! 👋")
                    break
                
                self.console.print("\n")
                await self.handle_command(command)
                
            except KeyboardInterrupt:
                self.console.print("\nGoodbye! 👋")
                break
            except Exception as e:
                self.console.print(f"[red]Error:[/] {str(e)}")

def main():
    """Main entry point."""
    agent = NotionAgent()
    asyncio.run(agent.interactive_session())

if __name__ == "__main__":
    main()
