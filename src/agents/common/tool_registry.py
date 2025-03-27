"""Tool registry for agent implementations.

This module handles tool registration and management for all agent implementations.
"""
import logging
from typing import Dict, Any, Optional, Callable, List

from pydantic_ai.tools import Tool as PydanticTool

# Setup logging
logger = logging.getLogger(__name__)

# Import memory tools but delay actual import until needed to avoid circular imports
memory_tools_imported = False
get_memory_tool = None
store_memory_tool = None
read_memory = None
create_memory = None
update_memory = None
list_memories_tool = None

def _import_memory_tools():
    """Import memory tools to avoid circular imports."""
    global memory_tools_imported, get_memory_tool, store_memory_tool, read_memory, create_memory, update_memory, list_memories_tool
    if not memory_tools_imported:
        from src.tools.memory.tool import get_memory_tool as _get_memory_tool
        from src.tools.memory.tool import store_memory_tool as _store_memory_tool
        from src.tools.memory.tool import read_memory as _read_memory
        from src.tools.memory.tool import create_memory as _create_memory
        from src.tools.memory.tool import update_memory as _update_memory
        from src.tools.memory.tool import list_memories_tool as _list_memories_tool
        
        get_memory_tool = _get_memory_tool
        store_memory_tool = _store_memory_tool
        read_memory = _read_memory
        create_memory = _create_memory
        update_memory = _update_memory
        list_memories_tool = _list_memories_tool
        
        memory_tools_imported = True

class ToolRegistry:
    """Class for registering and managing tools for agent implementations."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self._registered_tools: Dict[str, Callable] = {}
    
    def register_tool(self, tool_func: Callable) -> None:
        """Register a tool with the registry.
        
        Args:
            tool_func: The tool function to register
        """
        name = getattr(tool_func, "__name__", str(tool_func))
        self._registered_tools[name] = tool_func
        logger.info(f"Registered tool: {name}")
    
    def register_default_tools(self, context: Dict[str, Any]) -> None:
        """Register the default set of tools for the agent.
        
        Args:
            context: Context dictionary for tool execution
        """
        # Import date/time tools
        from src.tools.datetime import get_current_date_tool, get_current_time_tool, format_date_tool
        
        # Register date/time tools
        self.register_tool(get_current_date_tool)
        self.register_tool(get_current_time_tool)
        self.register_tool(format_date_tool)
        
        # Import and register memory tools
        _import_memory_tools()
        
        if context:
            # Create and register wrapper for store_memory_tool that includes the context
            async def store_memory_wrapper(key: str, content: str) -> str:
                """Store a memory with the given key.
                
                Args:
                    key: The key to store the memory under
                    content: The memory content to store
                    
                Returns:
                    Confirmation message
                """
                return await store_memory_tool(key, content, ctx=context)
            
            # Create and register wrapper for get_memory_tool that includes the context
            async def get_memory_wrapper(key: str) -> Any:
                """Retrieve a memory with the given key.
                
                Args:
                    key: The key to retrieve the memory with
                    
                Returns:
                    The memory content if found, else an error message
                """
                return await get_memory_tool(context, key)
            
            # Create and register wrapper for list_memories_tool
            async def list_memories_wrapper(prefix: Optional[str] = None) -> str:
                """List all available memories, optionally filtered by prefix.
                
                Args:
                    prefix: Optional prefix to filter memory keys
                    
                Returns:
                    List of memory keys as a string
                """
                # Extract the agent_id from the context to filter memories by agent
                agent_id = context.get("agent_id") if context else None
                user_id = context.get("user_id") if context else None
                
                try:
                    logger.info(f"Listing memories with agent_id={agent_id}, user_id={user_id}, prefix={prefix}")
                    
                    # Use the imported list_memories_tool directly
                    return await list_memories_tool(prefix)
                except Exception as e:
                    error_msg = f"Error listing memories: {str(e)}"
                    logger.error(error_msg)
                    return error_msg
            
            # Register the wrappers instead of the originals
            self.register_tool(store_memory_wrapper)
            self.register_tool(get_memory_wrapper)
            self.register_tool(list_memories_wrapper)
        else:
            # If no context provided, register the original tools
            self.register_tool(store_memory_tool)
            self.register_tool(get_memory_tool)
            self.register_tool(list_memories_tool)
            
        logger.info("Default tools registered")
    
    def get_registered_tools(self) -> Dict[str, Callable]:
        """Get all registered tools.
        
        Returns:
            Dictionary of registered tools
        """
        return self._registered_tools
        
    def convert_to_pydantic_tools(self) -> List[PydanticTool]:
        """Convert registered tools to PydanticAI tools.
        
        Returns:
            List of PydanticAI tools
        """
        tools = []
        for name, func in self._registered_tools.items():
            try:
                if hasattr(func, "get_pydantic_tool"):
                    # Use the PydanticAI tool definition if available
                    tool = func.get_pydantic_tool()
                    tools.append(tool)
                    logger.debug(f"Converted to PydanticAI tool: {name}")
                elif isinstance(func, PydanticTool):
                    # If it's already a PydanticTool instance, use it directly
                    tools.append(func)
                    logger.debug(f"Added existing PydanticTool: {name}")
                elif hasattr(func, "__doc__") and callable(func):
                    # Create a basic wrapper for regular functions
                    doc = func.__doc__ or f"Tool for {name}"
                    # Create a simple PydanticTool
                    tool = PydanticTool(
                        name=name,
                        description=doc,
                        function=func
                    )
                    tools.append(tool)
                    logger.debug(f"Created PydanticTool for function: {name}")
                else:
                    logger.warning(f"Could not convert tool {name}: not a function or missing documentation")
            except Exception as e:
                logger.error(f"Error converting tool {name}: {str(e)}")
                
        logger.debug(msg=f"Converted {len(tools)} tools to PydanticAI tools")
        return tools

    def update_context(self, new_context: Dict[str, Any]) -> None:
        """Update the context used by tools.
        
        This method updates the context for tools that need it, particularly
        memory tools which require agent_id and user_id for proper operation.
        
        Args:
            new_context: Dictionary with context key-value pairs
        """
        if not new_context:
            logger.warning("Empty context provided to update_context")
            return
            
        # Re-register the memory tools with the updated context
        # This is needed because memory tools need the context for operation
        
        # First make sure memory tools are imported
        _import_memory_tools()
        
        # Re-register wrappers for memory tools with the updated context
        if store_memory_tool and get_memory_tool and list_memories_tool:
            # Create wrapper for store_memory_tool
            async def store_memory_wrapper(key: str, content: str) -> str:
                """Store a memory with the given key.
                
                Args:
                    key: The key to store the memory under
                    content: The memory content to store
                    
                Returns:
                    Confirmation message
                """
                return await store_memory_tool(key, content, ctx=new_context)
                
            # Create wrapper for get_memory_tool  
            async def get_memory_wrapper(key: str) -> Any:
                """Retrieve a memory with the given key.
                
                Args:
                    key: The key to retrieve the memory with
                    
                Returns:
                    The memory content if found, else an error message
                """
                return await get_memory_tool(new_context, key)
            
            # Create wrapper for list_memories_tool
            async def list_memories_wrapper(prefix: Optional[str] = None) -> str:
                """List all available memories, optionally filtered by prefix.
                
                Args:
                    prefix: Optional prefix to filter memory keys
                    
                Returns:
                    List of memory keys as a string
                """
                # Extract the agent_id from the context to filter memories by agent
                agent_id = new_context.get("agent_id") if new_context else None
                user_id = new_context.get("user_id") if new_context else None
                
                try:
                    logger.info(f"Listing memories with agent_id={agent_id}, user_id={user_id}, prefix={prefix}")
                    
                    # Use the imported list_memories_tool directly
                    return await list_memories_tool(prefix)
                except Exception as e:
                    error_msg = f"Error listing memories: {str(e)}"
                    logger.error(error_msg)
                    return error_msg
            
            # Re-register all memory tool wrappers
            self.register_tool(store_memory_wrapper)
            self.register_tool(get_memory_wrapper)
            self.register_tool(list_memories_wrapper)
            logger.info(f"Updated memory tools with new context: {new_context}")
        else:
            logger.warning("Could not update memory tools: not imported")
        
        logger.info("Tool context updated") 