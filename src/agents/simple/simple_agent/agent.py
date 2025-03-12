from typing import Dict
from pydantic_ai import Agent

from src.agents.models.base_agent import BaseAgent
from src.agents.models.agent import AgentBaseResponse
from src.memory.message_history import MessageHistory
from src.agents.simple.simple_agent.prompts import SIMPLE_AGENT_PROMPT

class SimpleAgent(BaseAgent):
    """Simple agent implementation for basic chat functionality with memory tools."""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the simple agent with configuration."""
        super().__init__(config, SIMPLE_AGENT_PROMPT)
        # Set a default agent_id for use with memory tools
        self.agent_id = config.get("agent_id", "simple_memory_agent")

    def initialize_agent(self) -> Agent:
        """Initialize the simple agent with configuration."""
        return Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries
        )

    def register_tools(self):
        """Register tools with the agent.
        
        Note on memory tools: This method contains special handling for memory tools to provide
        dynamic descriptions that include the currently available memories. The descriptions
        are limited to stay within OpenAI API's 1024 character limit for tool descriptions.
        """
        from src.tools.memory_tools import read_memory, create_memory, update_memory
        from src.utils.db import execute_query
        import logging
        import json
        
        logger = logging.getLogger(__name__)
        
        # Direct database approach - fetch memories directly from DB
        try:
            logger.info("Directly fetching memories from database for tool descriptions")
            
            # Query to get all available memories
            query = "SELECT id, name, description FROM memories ORDER BY name ASC"
            result = execute_query(query)
            # Handle case where result is a list (DB rows) or dict with 'rows' key
            if isinstance(result, list):
                memories = result
            else:
                memories = result.get('rows', [])
            memory_count = len(memories)
            
            logger.info(f"Found {memory_count} memories directly from database")
            
            # Create read_memory description with available memory names for this agent/user
            read_desc = "This tool allows retrieving memories stored in the database.\n\n"
            read_desc += "Memory Access Hierarchy (in order of priority):\n"
            read_desc += "- **Agent-specific**: Memories belonging to this agent globally (accessible to all users)\n"
            read_desc += "- **Agent+User**: Memories personalized for this specific user with this specific agent\n"
            read_desc += "- **Agent+User+Session**: Memories valid only in the current session\n\n"
            
            read_desc += "Available parameters:\n"
            read_desc += "- **memory_id**: Optional ID of the specific memory to retrieve\n"
            read_desc += "- **name**: Optional memory name (or partial name) to search for\n"
            read_desc += "- **list_all**: If True, returns all memories available to this agent/user\n\n"
            
            # Filter memories for the current agent access context
            # For this example, we'll list all memories since we don't have the real-time filter context
            # A real implementation would filter based on agent_id, user_id, and permissions
            if memory_count > 0:
                read_desc += "Memories available to this agent/user:\n"
                
                max_desc_length = 950  # Limit to stay within API constraints
                memories_added = 0
                memory_names_str = ""
                
                for memory in memories:
                    mem_name = memory.get('name', 'Unknown')
                    memory_entry = f"- {mem_name}\n"
                    
                    # Check if adding this would exceed our limit
                    if len(read_desc) + len(memory_entry) + 30 > max_desc_length:
                        remaining = memory_count - memories_added
                        if remaining > 0:
                            memory_names_str += f"...and {remaining} more."
                        break
                    
                    memory_names_str += memory_entry
                    memories_added += 1
                
                read_desc += memory_names_str
            else:
                read_desc += "No memories are currently available to this agent/user."
            
            logger.info(f"Created parameter-focused read_memory description ({len(read_desc)} chars)")
            
            # Log the first few memories for debugging purposes only
            if memory_count > 0:
                memory_names = [m.get('name', 'Unknown') for m in memories[:3]]
                logger.debug(f"First few available memories (not shown in description): {', '.join(memory_names)}")

                
            # Create separate descriptions for create_memory and update_memory
            # Create_memory description
            create_desc = "This tool allows creating a new memory in the database.\n\n"
            create_desc += "Memory Access Hierarchy:\n"
            create_desc += "- **Agent-specific**: Accessible globally to all users of this specific agent\n"
            create_desc += "- **Agent+User**: Accessible only to this specific user with this specific agent\n"
            create_desc += "- **Agent+User+Session**: Accessible only in the current session\n\n"
            
            create_desc += "Required parameters:\n"
            create_desc += "- **name**: The name of the new memory to create\n"
            create_desc += "- **content**: The content to store (string or dictionary format)\n"
            create_desc += "- **description**: A description of what this memory contains or is used for\n"
            create_desc += "- **read_mode**: Controls how this memory is used (e.g., tool_call, system_prompt)\n"
            create_desc += "- **access**: Access permissions for this memory (e.g., read, write)\n"
            
            # Update_memory description
            update_desc = "This tool allows updating an existing memory in the database.\n\n"
            update_desc += "Memory Access Hierarchy:\n"
            update_desc += "- **Agent-specific**: Can update memories belonging to this agent (accessible globally)\n"
            update_desc += "- **Agent+User**: Can update memories specific to this user and agent\n"
            update_desc += "- **Agent+User+Session**: Can update memories from the current session\n\n"
            
            update_desc += "Required parameters:\n"
            update_desc += "- **content**: The new content to store (required)\n"
            update_desc += "- **memory_id** OR **name**: ID or name of the existing memory to update\n\n"
            
            # Filter memories that can be updated (same approach as read_memory)
            if memory_count > 0:
                update_desc += "Memories available for updating (that belong to this agent/user):\n"
                
                max_desc_length = 900  # Limit to stay within API constraints
                memories_added = 0
                memory_names_str = ""
                
                for memory in memories:
                    mem_name = memory.get('name', 'Unknown')
                    memory_entry = f"- {mem_name}\n"
                    
                    # Check if adding this would exceed our limit
                    if len(update_desc) + len(memory_entry) + 30 > max_desc_length:
                        remaining = memory_count - memories_added
                        if remaining > 0:
                            memory_names_str += f"...and {remaining} more."
                        break
                    
                    memory_names_str += memory_entry
                    memories_added += 1
                
                update_desc += memory_names_str
            else:
                update_desc += "No existing memories are available for updating."
            
            logger.info(f"Created parameter-focused create_memory description ({len(create_desc)} chars)")
            logger.info(f"Created parameter-focused update_memory description ({len(update_desc)} chars)")
            
            # Log the first few memories for debugging purposes only
            if memory_count > 0:
                memory_names = [m.get('name', 'Unknown') for m in memories[:3]]
                logger.debug(f"First few updatable memories (not shown in description): {', '.join(memory_names)}")

                
            logger.info(f"Read description length: {len(read_desc)}")
            logger.info(f"Create description length: {len(create_desc)}")
            logger.info(f"Update description length: {len(update_desc)}")
            
        except Exception as e:
            logger.warning(f"Error generating dynamic tool descriptions from DB: {e}")
            # Fallback to simple descriptions
            read_desc = "Read memories from the database by name or ID, or list all available memories."
            create_desc = "Create new memories in the database with customizable content and metadata."
            update_desc = "Update existing memories in the database with new content."
        
        # Create wrapper functions with the SAME ORIGINAL NAMES to avoid confusion
        # Properly maintain the original function signatures
        def read_memory(ctx, memory_id=None, name=None, read_mode=None, list_all=False):
            # This wrapper has the same name as the original function
            from src.tools.memory_tools import read_memory as original_read_memory
            return original_read_memory(ctx, memory_id, name, read_mode, list_all)
            
        def create_memory(ctx, name, content, description, read_mode="tool_call", 
                          access="write", metadata=None):
            # This wrapper has the same name as the original function
            from src.tools.memory_tools import create_memory as original_create_memory
            return original_create_memory(ctx, name, content, description, 
                                         read_mode, access, metadata)
                                         
        def update_memory(ctx, content, memory_id=None, name=None):
            # This wrapper has the same name as the original function
            from src.tools.memory_tools import update_memory as original_update_memory
            return original_update_memory(ctx, content, memory_id, name)
            
        # Set the custom docstrings
        read_memory.__doc__ = read_desc
        create_memory.__doc__ = create_desc
        update_memory.__doc__ = update_desc
        
        # Register our wrapper functions that have the same names as the originals
        # Store references to tools to make them accessible for inspection
        self.read_memory_tool = read_memory
        self.create_memory_tool = create_memory
        self.update_memory_tool = update_memory
        
        # Register with the agent
        self.agent.tool(self.read_memory_tool)
        self.agent.tool(self.create_memory_tool)
        self.agent.tool(self.update_memory_tool)
        
        # Store a list of registered tools for easy access by scripts/tests
        self.registered_tools = {
            'read_memory': self.read_memory_tool,
            'create_memory': self.create_memory_tool,
            'update_memory': self.update_memory_tool
        }

        # Log information about the memories for reference
        if memory_count > 0:
            memory_names = [m.get('name', 'Unknown') for m in memories[:5]]  # Show first 5 for brevity
            if len(memories) > 5:
                memory_names_str = ", ".join(memory_names) + f" and {len(memories) - 5} more"
            else:
                memory_names_str = ", ".join(memory_names)
            logger.info(f"Memory information added to docstrings for: {memory_names_str}")
        else:
            logger.info("No memories found to add to tool descriptions")

        
    async def run(self, user_message: str, message_history: MessageHistory) -> AgentBaseResponse:
        """Run the agent with the given message and message history.
        
        Args:
            user_message: User message (already in message_history)
            message_history: Message history for this session
            
        Returns:
            Agent response
        """
        try:
            # Prepare dependency context for memory tools
            deps = {
                "agent_id": self.agent_id,
                "user_id": message_history.user_id,
                "session_id": message_history.session_id
            }
            
            # Run the agent with the user message, message history, and dependencies
            result = await self.agent.run(
                user_message,
                message_history=message_history.messages,
                deps=deps
            )
            
            # Extract the response text
            response_text = result.data
            
            # Create and return the agent response
            return AgentBaseResponse.from_agent_response(
                message=response_text,
                history=message_history,
                error=None,
                session_id=message_history.session_id
            )
        except Exception as e:
            error_msg = f"Error running SimpleAgent: {str(e)}"
            return AgentBaseResponse.from_agent_response(
                message="An error occurred while processing your request.",
                history=message_history,
                error=error_msg,
                session_id=message_history.session_id
            )
