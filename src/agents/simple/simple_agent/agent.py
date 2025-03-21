"""SimpleAgent implementation.

This module provides the SimpleAgent implementation, which is a basic
agent that follows PydanticAI conventions for multimodal support.
"""
import logging
import asyncio
import traceback
import re
from typing import Dict, List, Any, Optional, Callable, Union, TypeVar, Tuple, Set
from functools import partial
import json
import os
import uuid
from datetime import datetime

from pydantic_ai import Agent

from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import UsageLimits

# Tool-related imports
from pydantic_ai.tools import Tool as PydanticTool, RunContext

# Import constants
from src.constants import (
    DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS, DEFAULT_RETRIES
)

# Import dependencies
from src.agents.models.base_agent import BaseAgent
from src.agents.models.dependencies import SimpleAgentDependencies
from src.agents.models.response import AgentResponse
from src.memory.message_history import MessageHistory

from src.tools.datetime import get_current_date_tool, get_current_time_tool, format_date_tool

# Import memory tools but delay actual import until needed to avoid circular imports
memory_tools_imported = False
get_memory_tool = None
store_memory_tool = None
read_memory = None
create_memory = None
update_memory = None

def _import_memory_tools():
    global memory_tools_imported, get_memory_tool, store_memory_tool, read_memory, create_memory, update_memory
    if not memory_tools_imported:
        from src.tools.memory.tool import get_memory_tool as _get_memory_tool
        from src.tools.memory.tool import store_memory_tool as _store_memory_tool
        from src.tools.memory.tool import read_memory as _read_memory
        from src.tools.memory.tool import create_memory as _create_memory
        from src.tools.memory.tool import update_memory as _update_memory
        
        get_memory_tool = _get_memory_tool
        store_memory_tool = _store_memory_tool
        read_memory = _read_memory
        create_memory = _create_memory
        update_memory = _update_memory
        
        memory_tools_imported = True

# Setup logging
logger = logging.getLogger(__name__)
T = TypeVar('T')  # Generic type for callable return values

class SimpleAgent(BaseAgent):
    """SimpleAgent implementation using PydanticAI.
    
    This agent provides a basic implementation that follows the PydanticAI
    conventions for multimodal support and tool calling.
    """
    
    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize the SimpleAgent.
        
        Args:
            config: Dictionary with configuration options
        """
        # Import prompt template from prompt.py
        from src.agents.simple.simple_agent.prompts.prompt import SIMPLE_AGENT_PROMPT
        self.prompt_template = SIMPLE_AGENT_PROMPT
        
        # Store agent_id if provided
        self.db_id = config.get("agent_id")
        if self.db_id and isinstance(self.db_id, str) and self.db_id.isdigit():
            self.db_id = int(self.db_id)
            logger.info(f"Initialized SimpleAgent with database ID: {self.db_id}")
        else:
            # Don't log a warning here, as this is expected during discovery
            # The actual agent_id will be set later in the API routes
            self.db_id = None
        
        # Extract template variables from the prompt
        self.template_vars = self._extract_template_variables(self.prompt_template)
        if self.template_vars:
            logger.info(f"Detected template variables: {', '.join(self.template_vars)}")
            
            # Initialize memory variables if agent ID is available
            if self.db_id:
                try:
                    self._initialize_memory_variables_sync()
                    logger.info(f"Memory variables initialized for agent ID {self.db_id}")
                except Exception as e:
                    logger.error(f"Error initializing memory variables: {str(e)}")
        
        # Create initial system prompt - dynamic parts will be added via decorators
        base_system_prompt = self._create_base_system_prompt()
        
        # Initialize the BaseAgent with proper arguments
        super().__init__(config, base_system_prompt)
        
        # Initialize variables
        self._agent_instance: Optional[Agent] = None
        self._registered_tools: Dict[str, Callable] = {}
        
        # Create dependencies
        self.dependencies = SimpleAgentDependencies(
            model_name=config.get("model", DEFAULT_MODEL),
            model_settings=self._parse_model_settings(config)
        )
        
        # Set agent ID in dependencies
        if self.db_id:
            self.dependencies.set_agent_id(self.db_id)
        
        # Set usage limits if specified
        if "response_tokens_limit" in config or "request_limit" in config or "total_tokens_limit" in config:
            self._set_usage_limits(config)
        
        # Register default tools
        self._register_default_tools()
        
        # Set up message history with a valid session ID but don't auto-create in database during init
        session_id = config.get("session_id", str(uuid.uuid4()))
        self.message_history = MessageHistory(session_id=session_id, no_auto_create=True)
               
        logger.info("SimpleAgent initialized successfully")
    
    def _extract_template_variables(self, template: str) -> List[str]:
        """Extract all template variables from a string.
        
        Args:
            template: Template string with {{variable}} placeholders
            
        Returns:
            List of variable names without braces
        """
        pattern = r'\{\{([a-zA-Z_]+)\}\}'
        matches = re.findall(pattern, template)
        return list(set(matches))  # Remove duplicates
    
    def _initialize_memory_variables_sync(self, user_id: Optional[int] = None) -> None:
        """Initialize memory variables in the database.
        
        This ensures all template variables exist in memory with default values.
        Uses direct repository calls to avoid async/await issues.
        
        Args:
            user_id: Optional user ID to associate with the memory variables
        """
        if not self.db_id:
            logger.warning("Cannot initialize memory variables: No agent ID available")
            return
            
        try:
            # Import the repository functions for direct database access
            from src.db.repository.memory import get_memory_by_name, create_memory
            from src.db.models import Memory
            
            # Extract all variables except run_id which is handled separately
            memory_vars = [var for var in self.template_vars if var != "run_id"]
            
            # Log the user_id we're using (if any)
            if user_id:
                logger.info(f"Initializing memory variables for user_id={user_id}")
            else:
                logger.warning("No user_id provided, memories will be created with NULL user_id")
            
            for var_name in memory_vars:
                try:
                    # Check if memory already exists with direct repository call for this user
                    existing_memory = get_memory_by_name(var_name, agent_id=self.db_id, user_id=user_id)
                    
                    # If not found, create it with default value
                    if not existing_memory:
                        logger.info(f"Creating missing memory variable: {var_name} for user: {user_id}")
                        
                        # Prepare a proper description based on the variable name
                        description = f"Auto-created template variable for SimpleAgent"
                        if var_name == "personal_attributes":
                            description = "Personal attributes and preferences for the agent"
                            content = "None stored yet. You can update this by asking the agent to remember personal details."
                        elif var_name == "technical_knowledge":
                            description = "Technical knowledge and capabilities for the agent"
                            content = "None stored yet. You can update this by asking the agent to remember technical information."
                        elif var_name == "user_preferences":
                            description = "User preferences and settings for the agent"
                            content = "None stored yet. You can update this by asking the agent to remember your preferences."
                        else:
                            content = "None stored yet"
                        
                        # Create the memory directly using repository function
                        memory = Memory(
                            name=var_name,
                            content=content,
                            description=description,
                            agent_id=self.db_id,
                            user_id=user_id,  # Include the user_id here
                            read_mode="system_prompt",
                            access="read_write"  # Ensure it can be written to
                        )
                        
                        memory_id = create_memory(memory)
                        if memory_id:
                            logger.info(f"Created memory variable: {var_name} with ID: {memory_id} for user: {user_id}")
                        else:
                            logger.error(f"Failed to create memory variable: {var_name}")
                    else:
                        logger.info(f"Memory variable already exists: {var_name}")
                        
                except Exception as e:
                    logger.error(f"Error initializing memory variable {var_name}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error in _initialize_memory_variables_sync: {str(e)}")
    
    def _create_base_system_prompt(self) -> str:
        """Create the base system prompt.
        
        Returns an empty base prompt since we'll completely fill it
        in the dynamic system prompt handler.
        
        Returns:
            Empty string as base prompt
        """
        # Instead of returning an empty string, we'll use the template directly
        # This ensures the prompt is available even without template replacement
        return self.prompt_template

    def _parse_model_settings(self, config: Dict[str, str]) -> Dict[str, Any]:
        """Parse model settings from config.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dictionary with model settings
        """
        settings = {}
        
        # Extract model settings from config
        for key, value in config.items():
            if key.startswith("model_settings."):
                setting_key = key.replace("model_settings.", "")
                settings[setting_key] = value
        
        # Add default settings if not specified
        if "temperature" not in settings and "model_settings.temperature" not in config:
            settings["temperature"] = DEFAULT_TEMPERATURE
        if "max_tokens" not in settings and "model_settings.max_tokens" not in config:
            settings["max_tokens"] = DEFAULT_MAX_TOKENS
            
        return settings
    
    def _set_usage_limits(self, config: Dict[str, str]) -> None:
        """Set usage limits from config.
        
        Args:
            config: Configuration dictionary
        """
            
        # Parse limits from config
        response_tokens_limit = config.get("response_tokens_limit")
        request_limit = config.get("request_limit")
        total_tokens_limit = config.get("total_tokens_limit")
        
        # Convert string values to integers
        if response_tokens_limit:
            response_tokens_limit = int(response_tokens_limit)
        if request_limit:
            request_limit = int(request_limit)
        if total_tokens_limit:
            total_tokens_limit = int(total_tokens_limit)
            
        # Create UsageLimits object
        self.dependencies.set_usage_limits(
            response_tokens_limit=response_tokens_limit,
            request_limit=request_limit,
            total_tokens_limit=total_tokens_limit
        )
    
    async def __aenter__(self):
        """Async context manager entry method."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit method."""
        await self.cleanup()
    
    def _register_default_tools(self) -> None:
        """Register the default set of tools for this agent."""
        # Date/time tools
        self.register_tool(get_current_date_tool)
        self.register_tool(get_current_time_tool)
        self.register_tool(format_date_tool)
        
        # Memory tools
        _import_memory_tools()
        self.register_tool(store_memory_tool)
        self.register_tool(get_memory_tool)
        
        logger.info("Default tools registered for SimpleAgent")
    
    def register_tool(self, tool_func: Callable) -> None:
        """Register a tool with the agent.
        
        Args:
            tool_func: The tool function to register
        """
        name = getattr(tool_func, "__name__", str(tool_func))
        self._registered_tools[name] = tool_func
    
    async def _initialize_agent(self) -> None:
        """Initialize the underlying PydanticAI agent with dynamic system prompts."""
        if self._agent_instance is not None:
            return
            
        # Get model settings
        model_name = self.dependencies.model_name
        model_settings = self._get_model_settings()
        
        # Ensure system_prompt is set properly from the template
        self.system_prompt = self.prompt_template
        logger.info(f"Initializing agent with system prompt template (first 50 chars): {self.system_prompt[:50]}...")
        
        # Get available tools
        tools = []
        for name, func in self._registered_tools.items():
            try:
                if hasattr(func, "get_pydantic_tool"):
                    # Use the PydanticAI tool definition if available
                    tool = func.get_pydantic_tool()
                    tools.append(tool)
                    logger.info(f"Registered PydanticAI tool: {name}")
                elif isinstance(func, PydanticTool):
                    # If it's already a PydanticTool instance, use it directly
                    tools.append(func)
                    logger.info(f"Added existing PydanticTool: {name}")
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
                    logger.info(f"Created PydanticTool for function: {name}")
                else:
                    logger.warning(f"Could not register tool {name}: not a function or missing documentation")
            except Exception as e:
                logger.error(f"Error creating tool {name}: {str(e)}")
        
        logger.info(f"Prepared {len(tools)} tools for PydanticAI agent")
                    
        # Create the agent
        try:
            self._agent_instance = Agent(
                model=model_name,
                system_prompt=self.system_prompt,
                tools=tools,
                model_settings=model_settings,
                deps_type=SimpleAgentDependencies
            )
            
            # Log that we created the agent with the system prompt
            logger.info(f"Created Agent with system prompt: {self.system_prompt[:50]}...")
            
            # Register dynamic system prompts
            self._register_system_prompts()
            
            logger.info(f"Initialized agent with model: {model_name} and {len(tools)} tools")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}")
            raise
    
    def _register_system_prompts(self) -> None:
        """Register dynamic system prompts for template variables."""
        if not self._agent_instance:
            logger.error("Cannot register system prompts: Agent not initialized")
            return
            
        # Register a dynamic prompt handler that will replace all template variables in the prompt
        @self._agent_instance.system_prompt
        async def replace_template_variables(ctx: RunContext[SimpleAgentDependencies]) -> str:
            """Replace all template variables in the system prompt with their values."""
            template_values = {}
            variables_with_errors = []
            
            # Get user_id from dependencies if available
            user_id = None
            if ctx and hasattr(ctx, 'deps'):
                user_id = getattr(ctx.deps, 'user_id', None)
                if user_id:
                    logger.info(f"Using user_id={user_id} for memory variables")
            
            # Get run_id value
            if self.db_id:
                try:
                    from src.db.repository import increment_agent_run_id, get_agent
                    # First increment
                    increment_success = increment_agent_run_id(self.db_id)
                    if not increment_success:
                        logger.warning(f"Failed to increment run_id for agent {self.db_id}")
                    
                    # Then get updated value
                    agent = get_agent(self.db_id)
                    if agent and hasattr(agent, 'run_id'):
                        template_values["run_id"] = str(agent.run_id)
                        logger.info(f"Using run_id={agent.run_id} for prompt")
                    else:
                        template_values["run_id"] = "1"
                except Exception as e:
                    logger.error(f"Error getting run_id: {str(e)}")
                    template_values["run_id"] = "1"
                    variables_with_errors.append("run_id")
            else:
                template_values["run_id"] = "1"
                logger.warning("No agent ID available - using default run_id=1")
            
            # Get memory variables
            _import_memory_tools()
            memory_vars = [var for var in self.template_vars if var != "run_id"]
            for var_name in memory_vars:
                try:
                    # Pass user_id to get_memory_tool if available
                    if user_id:
                        memory_content = await get_memory_tool(self.context, var_name, user_id=user_id)
                    else:
                        memory_content = await get_memory_tool(self.context, var_name)
                    
                    if memory_content and not memory_content.startswith("Memory with key"):
                        template_values[var_name] = memory_content
                    else:
                        # Try to create memory if it doesn't exist and we have an agent ID
                        if self.db_id:
                            try:
                                from src.db.repository.memory import get_memory_by_name, create_memory
                                from src.db.models import Memory
                                
                                # Create memory with default value
                                memory = Memory(
                                    name=var_name,
                                    content="None stored yet",
                                    description=f"Auto-created template variable for SimpleAgent during runtime",
                                    agent_id=self.db_id,
                                    user_id=user_id,  # Add user_id to runtime-created memories
                                    read_mode="system_prompt"
                                )
                                
                                memory_id = create_memory(memory)
                                if memory_id:
                                    logger.info(f"Created memory variable during runtime: {var_name} with ID: {memory_id} for user: {user_id}")
                                    template_values[var_name] = "None stored yet"
                                else:
                                    logger.error(f"Failed to create memory variable: {var_name}")
                                    template_values[var_name] = "None stored yet"
                                    variables_with_errors.append(var_name)
                            except Exception as e:
                                logger.error(f"Error creating memory during runtime for {var_name}: {str(e)}")
                                template_values[var_name] = "None stored yet"
                                variables_with_errors.append(var_name)
                        else:
                            template_values[var_name] = "None stored yet"
                            variables_with_errors.append(var_name)
                except Exception as e:
                    logger.error(f"Error getting memory for {var_name}: {str(e)}")
                    template_values[var_name] = "None stored yet"
                    variables_with_errors.append(var_name)
            
            # Log the values we're using
            for name, value in template_values.items():
                display_value = value[:30] + "..." if len(value) > 30 else value
                logger.info(f"Template variable {name} = {display_value}")
            
            if variables_with_errors:
                logger.warning(f"Issues with template variables: {', '.join(variables_with_errors)}")
            
            # Now generate a filled template by replacing each variable
            try:
                prompt_template = self.prompt_template
                for var_name, value in template_values.items():
                    placeholder = f"{{{{{var_name}}}}}"
                    prompt_template = prompt_template.replace(placeholder, value)
                
                # Log the first 100 characters of the final prompt for debugging
                preview = prompt_template[:100] + "..." if len(prompt_template) > 100 else prompt_template
                logger.info(f"Final system prompt (preview): {preview}")
                
                # Return the filled template as the system prompt
                return prompt_template
            except Exception as e:
                logger.error(f"Error filling template: {str(e)}")
                # Return the original template as a fallback
                return self.prompt_template
    
    def _get_model_settings(self) -> Optional[ModelSettings]:
        """Get model settings for the PydanticAI agent.
        
        Returns:
            ModelSettings object with model configuration
        """
   
        settings = self.dependencies.model_settings.copy()
        
        # Apply defaults if not specified
        if "temperature" not in settings:
            settings["temperature"] = DEFAULT_TEMPERATURE
        if "max_tokens" not in settings:
            settings["max_tokens"] = DEFAULT_MAX_TOKENS
        
        return ModelSettings(**settings)
    
    async def cleanup(self) -> None:
        """Clean up resources used by the agent."""
        if self.dependencies.http_client:
            await self.dependencies.close_http_client()
    
    def _check_and_ensure_memory_variables(self, user_id: Optional[int] = None) -> bool:
        """Check if memory variables are properly initialized and initialize if needed.
        
        Args:
            user_id: Optional user ID to associate with the memory variables
            
        Returns:
            True if all memory variables are properly initialized, False otherwise
        """
        if not self.db_id:
            logger.warning("Cannot check memory variables: No agent ID available")
            return False
            
        try:
            from src.db.repository.memory import get_memory_by_name
            
            # Extract all variables except run_id which is handled separately
            memory_vars = [var for var in self.template_vars if var != "run_id"]
            missing_vars = []
            
            for var_name in memory_vars:
                # Check if memory exists for this user
                existing_memory = get_memory_by_name(var_name, agent_id=self.db_id, user_id=user_id)
                
                if not existing_memory:
                    missing_vars.append(var_name)
            
            # If we found missing variables, try to initialize them
            if missing_vars:
                logger.warning(f"Found {len(missing_vars)} uninitialized memory variables: {', '.join(missing_vars)}")
                self._initialize_memory_variables_sync(user_id)
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error checking memory variables: {str(e)}")
            return False
            
    async def run(self, input_text: str, *, multimodal_content=None, system_message=None, message_history_obj=None) -> AgentResponse:
        """Run the agent with the given input.
        
        Args:
            input_text: Text input for the agent
            multimodal_content: Optional multimodal content
            system_message: Optional system message for this run
            message_history_obj: Optional MessageHistory instance for DB storage
            
        Returns:
            AgentResponse object with result and metadata
        """
        # Check and ensure memory variables are initialized if we have an agent ID
        if self.db_id:
            # Get user_id from dependencies if available
            user_id = getattr(self.dependencies, 'user_id', None)
            self._check_and_ensure_memory_variables(user_id)
            if user_id:
                logger.info(f"Checked memory variables for user_id={user_id}")
            else:
                logger.warning("No user_id available in dependencies for memory initialization")
        
        # Initialize agent if not done already
        await self._initialize_agent()
        
        # Log the current system prompt for debugging
        if hasattr(self, "system_prompt") and self.system_prompt:
            preview = self.system_prompt[:100] + "..." if len(self.system_prompt) > 100 else self.system_prompt
            logger.info(f"Using system prompt (preview): {preview}")
        
        # Get or create message history from dependencies
        pydantic_message_history = self.dependencies.get_message_history()
        
        # If we have no message history yet, ensure we'll use the proper system prompt
        if not pydantic_message_history:
            logger.info("No existing message history found, will ensure system prompt is used")
            
            # Force rebuild the agent with current system prompt if needed
            if self._agent_instance and not system_message:
                logger.info("Rebuilding agent to ensure fresh system prompt application")
                self._agent_instance = None
                await self._initialize_agent()
        else:
            # If we have existing message history, ensure it includes the system prompt
            self.dependencies_to_message_history()
        
        # Check if we need multimodal support
        agent_input = input_text
        if multimodal_content:
            agent_input = self._configure_for_multimodal(input_text, multimodal_content)
        
        # If a system message is provided for this run and we don't have message history,
        # we need to reinitialize the agent with the new system prompt
        if system_message and not pydantic_message_history:
            temp_system_prompt = self.system_prompt
            self.system_prompt = system_message
            self._agent_instance = None  # Force reinitialization
            await self._initialize_agent()
            self.system_prompt = temp_system_prompt  # Restore original
            
            # Also store system prompt in database if we have MessageHistory
            if message_history_obj and system_message:
                message_history_obj.add_system_prompt(system_message, agent_id=getattr(self, "db_id", None))
                logger.info(f"Added custom system message to MessageHistory")
        
        # If we have a MessageHistory object but no messages in dependencies,
        # check if we should add a system prompt to the database
        if message_history_obj and not pydantic_message_history and hasattr(self, "system_prompt") and self.system_prompt:
            message_history_obj.add_system_prompt(self.system_prompt, agent_id=getattr(self, "db_id", None))
            logger.info(f"Added system prompt from agent to MessageHistory: {self.system_prompt[:50]}...")
        
        # Run the agent
        try:
            # Include usage_limits if available
            usage_limits = self.dependencies.usage_limits if hasattr(self.dependencies, "usage_limits") else None
            
            result = await self._agent_instance.run(
                agent_input,
                message_history=pydantic_message_history,
                usage_limits=usage_limits,
                deps=self.dependencies
            )
            
            # Extract tool calls and outputs from message parts
            tool_calls = []
            tool_outputs = []
            
            try:
                all_messages = result.all_messages()
                logger.info(f"Retrieved {len(all_messages)} messages from result")
                
                for msg in all_messages:
                    # Handle direct message attributes containing tool calls/returns
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tc in msg.tool_calls:
                            tool_call = {
                                'tool_name': getattr(tc, 'name', getattr(tc, 'tool_name', '')),
                                'args': getattr(tc, 'args', getattr(tc, 'arguments', {})),
                                'tool_call_id': getattr(tc, 'id', getattr(tc, 'tool_call_id', ''))
                            }
                            tool_calls.append(tool_call)
                            logger.info(f"Found direct tool call: {tool_call['tool_name']}")
                            
                    if hasattr(msg, 'tool_outputs') and msg.tool_outputs:
                        for to in msg.tool_outputs:
                            tool_output = {
                                'tool_name': getattr(to, 'name', getattr(to, 'tool_name', '')),
                                'content': getattr(to, 'content', ''),
                                'tool_call_id': getattr(to, 'id', getattr(to, 'tool_call_id', ''))
                            }
                            tool_outputs.append(tool_output)
                            logger.info(f"Found direct tool output: {tool_output['tool_name']}")
                    
                    # Process message parts if available
                    if hasattr(msg, 'parts'):
                        for part in msg.parts:
                            # Check if this part is a tool call by looking for multiple indicators
                            if (hasattr(part, 'part_kind') and part.part_kind == 'tool-call') or \
                               type(part).__name__ == 'ToolCallPart' or \
                               hasattr(part, 'tool_name') and hasattr(part, 'args'):
                                
                                tool_call = {
                                    'tool_name': getattr(part, 'tool_name', ''),
                                    'args': getattr(part, 'args', {}),
                                    'tool_call_id': getattr(part, 'tool_call_id', getattr(part, 'id', ''))
                                }
                                tool_calls.append(tool_call)
                                logger.info(f"Found part tool call: {tool_call['tool_name']}")
                            
                            # Check if this part is a tool return by looking for multiple indicators
                            if (hasattr(part, 'part_kind') and part.part_kind == 'tool-return') or \
                               type(part).__name__ == 'ToolReturnPart' or \
                               (hasattr(part, 'tool_name') and hasattr(part, 'content')):
                                
                                # Extract content, handling both string and object formats
                                content = getattr(part, 'content', None)
                                
                                tool_output = {
                                    'tool_name': getattr(part, 'tool_name', ''),
                                    'content': content,
                                    'tool_call_id': getattr(part, 'tool_call_id', getattr(part, 'id', ''))
                                }
                                tool_outputs.append(tool_output)
                                
                                # Safely log a preview of the content
                                try:
                                    if content is None:
                                        content_preview = "None"
                                    elif isinstance(content, str):
                                        content_preview = content[:50]
                                    elif isinstance(content, dict):
                                        content_preview = f"Dict with keys: {', '.join(content.keys())[:50]}"
                                    else:
                                        content_preview = f"{type(content).__name__}[...]"
                                    
                                    logger.info(f"Found part tool output for {tool_output['tool_name']} with content: {content_preview}")
                                except Exception as e:
                                    logger.warning(f"Error creating content preview: {str(e)}")
                    
                    # Also check for any direct attributes on the message that might contain tool info
                    for attr_name in dir(msg):
                        # Skip private attributes and already processed ones
                        if attr_name.startswith('_') or attr_name in ('parts', 'tool_calls', 'tool_outputs'):
                            continue
                        
                        try:
                            attr_value = getattr(msg, attr_name)
                            # Check if this attribute looks like a tool call or return object
                            if hasattr(attr_value, 'tool_name') and (hasattr(attr_value, 'args') or hasattr(attr_value, 'content')):
                                if hasattr(attr_value, 'args'):
                                    # It's likely a tool call
                                    tool_call = {
                                        'tool_name': getattr(attr_value, 'tool_name', ''),
                                        'args': getattr(attr_value, 'args', {}),
                                        'tool_call_id': getattr(attr_value, 'tool_call_id', getattr(attr_value, 'id', ''))
                                    }
                                    tool_calls.append(tool_call)
                                    logger.info(f"Found attribute tool call: {tool_call['tool_name']}")
                                else:
                                    # It's likely a tool return
                                    content = getattr(attr_value, 'content', None)
                                    tool_output = {
                                        'tool_name': getattr(attr_value, 'tool_name', ''),
                                        'content': content,
                                        'tool_call_id': getattr(attr_value, 'tool_call_id', getattr(attr_value, 'id', ''))
                                    }
                                    tool_outputs.append(tool_output)
                                    logger.info(f"Found attribute tool output: {tool_output['tool_name']}")
                        except Exception:
                            # Skip any attributes that can't be accessed
                            pass
                            
            except Exception as e:
                logger.error(f"Error extracting tool calls and outputs: {str(e)}")
                logger.error(traceback.format_exc())
            
            # Log the extracted tool calls and outputs
            if tool_calls:
                logger.info(f"Found {len(tool_calls)} tool calls in the result")
                for i, tc in enumerate(tool_calls):
                    args_preview = str(tc.get('args', {}))[:50] + ('...' if len(str(tc.get('args', {}))) > 50 else '')
                    logger.info(f"Tool call {i+1}: {tc.get('tool_name', 'unknown')} with args: {args_preview}")
            else:
                logger.info("No tool calls found in the result")
                
            if tool_outputs:
                logger.info(f"Found {len(tool_outputs)} tool outputs in the result")
                for i, to in enumerate(tool_outputs):
                    content = to.get('content', '')
                    try:
                        if content is None:
                            content_preview = "None"
                        elif isinstance(content, str):
                            content_preview = f"string[{len(content)} chars]"
                        elif isinstance(content, dict):
                            content_preview = f"dict[{len(content)} keys]"
                        else:
                            content_preview = f"{type(content).__name__}"
                        logger.info(f"Tool output {i+1}: {to.get('tool_name', 'unknown')} with content: {content_preview}")
                    except Exception as e:
                        logger.warning(f"Error logging tool output: {str(e)}")
            else:
                logger.info("No tool outputs found in the result")
            
            # Store assistant response in database if we have a MessageHistory object
            if message_history_obj:
                logger.info(f"Adding assistant response to MessageHistory in the database")
                
                # Extract the response content
                response_content = result.data
                
                # Make sure tool_calls and tool_outputs are in the right format for storage
                formatted_tool_calls = []
                formatted_tool_outputs = []
                
                # Format tool calls for storage
                if tool_calls:
                    for tc in tool_calls:
                        formatted_tc = {
                            'tool_name': tc.get('tool_name', ''),
                            'args': tc.get('args', {}),
                            'tool_call_id': tc.get('tool_call_id', '')
                        }
                        formatted_tool_calls.append(formatted_tc)
                
                # Format tool outputs for storage, ensuring content is properly serializable
                if tool_outputs:
                    for to in tool_outputs:
                        content = to.get('content', '')
                        # Ensure content is JSON serializable
                        if not isinstance(content, (str, dict, list, int, float, bool, type(None))):
                            try:
                                # Try to convert to a string representation
                                content = str(content)
                            except Exception as e:
                                logger.warning(f"Could not convert tool output content to string: {str(e)}")
                                content = f"[Unserializable content of type {type(content).__name__}]"
                        
                        formatted_to = {
                            'tool_name': to.get('tool_name', ''),
                            'content': content,
                            'tool_call_id': to.get('tool_call_id', '')
                        }
                        formatted_tool_outputs.append(formatted_to)
                
                # Store in database with properly formatted tool calls/outputs
                message_history_obj.add_response(
                    content=response_content,
                    tool_calls=formatted_tool_calls if formatted_tool_calls else None,
                    tool_outputs=formatted_tool_outputs if formatted_tool_outputs else None,
                    agent_id=getattr(self, "db_id", None),
                    system_prompt=self._get_current_system_prompt()
                )
            
            # Create response with the tool calls and outputs
            return AgentResponse(
                text=result.data,
                success=True,
                tool_calls=tool_calls,
                tool_outputs=tool_outputs,
                raw_message=result.all_messages() if hasattr(result, "all_messages") else None
            )
        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            logger.error(traceback.format_exc())
            return AgentResponse(
                text="An error occurred while processing your request.",
                success=False,
                error_message=str(e)
            )
    
    def _configure_for_multimodal(self, input_text: str, multimodal_content: Dict[str, Any]) -> List[Any]:
        """Configure the agent input for multimodal content.
        
        Args:
            input_text: The text input from the user
            multimodal_content: Dictionary of multimodal content
            
        Returns:
            List containing text and multimodal content objects
        """
            
        result = [input_text]
        
        # Process different content types
        for content_type, content in multimodal_content.items():
            if content_type == "image":
                if isinstance(content, str) and (content.startswith("http://") or content.startswith("https://")):
                    result.append(ImageUrl(url=content))
                else:
                    result.append(BinaryContent(data=content, media_type="image/jpeg"))
            elif content_type == "audio":
                if isinstance(content, str) and (content.startswith("http://") or content.startswith("https://")):
                    result.append(AudioUrl(url=content))
                else:
                    result.append(BinaryContent(data=content, media_type="audio/mp3"))
            elif content_type == "document":
                if isinstance(content, str) and (content.startswith("http://") or content.startswith("https://")):
                    result.append(DocumentUrl(url=content))
                else:
                    result.append(BinaryContent(data=content, media_type="application/pdf"))
            else:
                logger.warning(f"Unsupported content type: {content_type}")
                
        return result
    
    async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[Union[int, str]] = None, user_id: int = 1, context: Optional[Dict] = None, message_history: Optional['MessageHistory'] = None) -> AgentResponse:
        """Process a user message with this agent.
        
        Args:
            user_message: User message to process
            session_id: Optional session ID
            agent_id: Optional agent ID for database tracking
            user_id: User ID
            context: Optional additional context
            message_history: Optional MessageHistory object
            
        Returns:
            Agent response
        """
        # Set session and user info in dependencies
        if session_id:
            self.dependencies.session_id = session_id
        self.dependencies.user_id = user_id
        logger.info(f"Processing message from user {user_id} with session {session_id}")
        
        # If agent_id is provided and different from the current db_id, update it
        agent_id_updated = False
        if agent_id and str(agent_id) != str(getattr(self, "db_id", None)):
            self.db_id = int(agent_id) if isinstance(agent_id, (str, int)) and str(agent_id).isdigit() else agent_id
            self.dependencies.set_agent_id(self.db_id)
            logger.info(f"Updated agent ID to {self.db_id}")
            agent_id_updated = True
            
            # Initialize memory variables if they haven't been initialized yet
            if agent_id_updated and self.template_vars:
                try:
                    # Pass user_id to memory initialization
                    self._initialize_memory_variables_sync(user_id)
                    logger.info(f"Memory variables initialized for agent ID {self.db_id} and user ID {user_id}")
                except Exception as e:
                    logger.error(f"Error initializing memory variables: {str(e)}")
        
        # Check and ensure memory variables for this user explicitly
        if self.db_id and self.template_vars:
            try:
                self._check_and_ensure_memory_variables(user_id)
                logger.info(f"Checked and ensured memory variables for user {user_id}")
            except Exception as e:
                logger.error(f"Error checking memory variables: {str(e)}")
        
        # Extract multimodal content from context
        multimodal_content = None
        if context and "multimodal_content" in context:
            multimodal_content = context["multimodal_content"]
        
        # If message_history is provided:
        # 1. Store user message in database
        # 2. Extract messages for PydanticAI
        if message_history:
            logger.info(f"Using provided MessageHistory for session {session_id}")
            # Add user message to database
            message_history.add(user_message, agent_id=self.db_id, context=context)
            # Get messages to pass to PydanticAI
            self.dependencies.set_message_history(message_history.all_messages())
        else:
            logger.info(f"No MessageHistory provided, will not store messages in database")
        
        # Reinitialize the agent if needed to use updated config
        if agent_id_updated:
            # Force agent to reinitialize with new ID
            self._agent_instance = None
            logger.info(f"Agent will be reinitialized with updated ID {self.db_id}")
        
        logger.info(f"Processing message for agent {self.db_id} with dynamic system prompts")
        
        # Run the agent with the MessageHistory object for database storage
        return await self.run(
            user_message, 
            multimodal_content=multimodal_content,
            message_history_obj=message_history
        )

    async def _handle_memory_variables(self, template: str) -> str:
        """Replace memory variable references with actual memory contents.
        
        Args:
            template: String containing memory variable references
            
        Returns:
            Template with variables replaced with their values
        """
        memory_var_pattern = r'\$memory\.([a-zA-Z0-9_]+)'
        memory_vars = re.findall(memory_var_pattern, template)
        
        if not memory_vars:
            return template
            
        # Create a copy of the template to modify
        result = template
        template_values = {}
        
        _import_memory_tools()
        for var_name in memory_vars:
            try:
                # Use get_memory_tool to get memory content
                response = await get_memory_tool(self.context, var_name)
                
                if isinstance(response, dict):
                    if 'success' in response and response['success'] and 'content' in response:
                        memory_content = response['content']
                    elif 'error' in response:
                        memory_content = f"[Memory Error: {response['error']}]"
                    else:
                        memory_content = str(response)
                else:
                    memory_content = str(response)
                
                template_values[var_name] = memory_content
            except Exception as e:
                logger.error(f"Error retrieving memory '{var_name}': {str(e)}")
                template_values[var_name] = f"[Memory Error: {str(e)}]"
        
        # Replace all memory references with their values
        for var_name, value in template_values.items():
            result = result.replace(f"$memory.{var_name}", value)
            
        return result 

    def _get_current_system_prompt(self) -> str:
        """Retrieve the current system prompt with template variables replaced.
        
        Returns:
            The current system prompt with all template variables filled
        """
        try:
            # If we've initialized the agent, get the most up-to-date system prompt with all replacements
            if self._agent_instance and hasattr(self._agent_instance, 'get_full_system_prompt'):
                try:
                    # Get the system prompt with all template variables replaced
                    return self._agent_instance.get_full_system_prompt()
                except Exception as e:
                    logger.error(f"Error getting full system prompt: {str(e)}")
            
            # Fallback to the original system prompt if we can't get the filled version
            return self.system_prompt
        except Exception as e:
            logger.error(f"Error in _get_current_system_prompt: {str(e)}")
            return self.system_prompt 

    def dependencies_to_message_history(self) -> None:
        """Ensure dependencies message history includes the system prompt.
        
        This method ensures that when we use existing dependencies for message history,
        the system prompt is properly included.
        """
        # Check if we have dependencies with a message history manager
        if not hasattr(self.dependencies, "message_history_manager"):
            logger.warning("No message_history_manager in dependencies")
            return
            
        # If there are no messages yet, add the system prompt
        messages = self.dependencies.message_history_manager.messages
        if not messages or len(messages) == 0:
            logger.info("Adding system prompt to empty message history manager")
            if hasattr(self, "system_prompt") and self.system_prompt:
                try:
                    # Add system prompt to the beginning of the messages
                    # Implementation depends on the specific structure of message_history_manager
                    # This is a basic approach that might need adaptation
                    if hasattr(self.dependencies.message_history_manager, "add_system_message"):
                        self.dependencies.message_history_manager.add_system_message(self.system_prompt)
                        logger.info("Added system prompt to message history manager")
                    else:
                        logger.warning("message_history_manager lacks add_system_message method")
                except Exception as e:
                    logger.error(f"Failed to add system prompt to message history: {str(e)}") 