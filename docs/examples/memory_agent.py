"""Example of PydanticAI with memory tools which allow an agent to read and write memories.

This agent demonstrates how to use memory tools to store and retrieve information.
The agent can remember facts about users, recall previously stored information,
and update existing memories based on new information.

Run with:

    uv run -m docs.examples.memory_agent
"""

from __future__ import annotations as _annotations

import asyncio
import os
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

import logfire
from devtools import debug

from pydantic_ai import Agent, RunContext
from src.tools.memory_tools import read_memory, write_memory
from src.db import get_db_connection

# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')


@dataclass
class Deps:
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    session_id: Optional[str] = None


memory_agent = Agent(
    'openai:gpt-4o',
    system_prompt=(
        'You are a helpful assistant that can remember information about users and recall it later. '
        'Use the `write_memory` tool to store new information, and the `read_memory` tool to retrieve '
        'previously stored information. Be conversational and friendly in your responses.'
    ),
    deps_type=Deps,
    retries=1,
    instrument=True,
)


@memory_agent.tool
async def remember(ctx: RunContext[Deps], topic: str, information: str) -> Dict[str, Any]:
    """Store information in memory.
    
    Args:
        ctx: The context with user, agent, and session information.
        topic: A brief name/topic for this memory.
        information: The content/information to remember.
        
    Returns:
        Dictionary indicating success or failure of the memory storage.
    """
    # Create a description from the topic
    description = f"Memory about {topic}"
    
    # Use our write_memory tool to store the information
    result = write_memory(
        ctx=ctx,
        name=topic,
        content=information,
        description=description,
        read_mode="user_memory",
        access="write"
    )
    
    return result


@memory_agent.tool
async def recall(ctx: RunContext[Deps], topic: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve information from memory.
    
    Args:
        ctx: The context with user, agent, and session information.
        topic: Optional topic to filter memories (can be partial match).
        
    Returns:
        Dictionary containing retrieved memories.
    """
    # Use our read_memory tool to retrieve information
    result = read_memory(ctx=ctx, name=topic, read_mode="user_memory")
    
    return result


@memory_agent.tool
async def update_memory(
    ctx: RunContext[Deps], memory_id: str, new_information: str
) -> Dict[str, Any]:
    """Update an existing memory with new information.
    
    Args:
        ctx: The context with user, agent, and session information.
        memory_id: The ID of the memory to update.
        new_information: The new content to store in the memory.
        
    Returns:
        Dictionary indicating success or failure of the memory update.
    """
    # First read the memory to get its name and other details
    memory_data = read_memory(ctx=ctx, memory_id=memory_id)
    
    if "error" in memory_data or not memory_data.get("found", False):
        return {"success": False, "message": f"Memory with ID {memory_id} not found"}
    
    memory = memory_data.get("memory", {})
    
    # Use our write_memory tool to update the information
    result = write_memory(
        ctx=ctx,
        memory_id=memory_id,
        name=memory.get("name"),
        content=new_information,
    )
    
    return result


async def main():
    # Create a session ID for this conversation
    session_id = str(uuid.uuid4())
    
    # Set up dependencies
    deps = Deps(
        user_id="example_user",
        agent_id="memory_agent",
        session_id=session_id
    )
    
    # Initialize the database connection
    get_db_connection()
    
    # Test the memory tools with a simple conversation
    print("\n=== Memory Tools Example ===\n")
    
    # First interaction - store information
    result = await memory_agent.run(
        "Remember that my favorite color is blue and I like hiking on weekends.", 
        deps=deps
    )
    print("User: Remember that my favorite color is blue and I like hiking on weekends.")
    print(f"Agent: {result.data}")
    
    # Second interaction - retrieve information
    result = await memory_agent.run(
        "What do you remember about me?", 
        deps=deps
    )
    print("\nUser: What do you remember about me?")
    print(f"Agent: {result.data}")
    
    # Third interaction - update information
    result = await memory_agent.run(
        "Actually, my favorite color is green now.", 
        deps=deps
    )
    print("\nUser: Actually, my favorite color is green now.")
    print(f"Agent: {result.data}")


if __name__ == '__main__':
    asyncio.run(main())
