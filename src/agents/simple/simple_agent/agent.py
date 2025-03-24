"""SimpleAgent implementation with PydanticAI.

This module provides a SimpleAgent class that uses PydanticAI for LLM integration
and leverages common utilities for message parsing, session management, and more.
"""
import logging
import asyncio
import traceback
from typing import Dict, List, Any, Optional, Union, TypeVar

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from src.constants import DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS
from src.agents.models.base_agent import BaseAgent
from src.agents.models.dependencies import SimpleAgentDependencies
from src.agents.models.response import AgentResponse
from src.memory.message_history import MessageHistory

# Import common utilities
from src.agents.common.prompt_builder import PromptBuilder
from src.agents.common.memory_handler import MemoryHandler
from src.agents.common.tool_registry import ToolRegistry
from src.agents.common.message_parser import (
    extract_tool_calls, 
    extract_tool_outputs,
    extract_all_messages,
    format_message_for_db,
    parse_user_message
)
from src.agents.common.session_manager import (
    create_context,
    validate_agent_id,
    validate_user_id,
    extract_multimodal_content
)
from src.agents.common.dependencies_helper import (
    parse_model_settings,
    create_model_settings,
    create_usage_limits,
    get_model_name,
    close_http_client,
    message_history_to_pydantic_format,
    add_system_message_to_history
)

logger = logging.getLogger(__name__)
T = TypeVar('T')

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
        from src.agents.simple.simple_agent.prompts.prompt import SIMPLE_AGENT_PROMPT
        self.prompt_template = SIMPLE_AGENT_PROMPT
        
        # Process agent_id from config
        self.db_id = validate_agent_id(config.get("agent_id"))
        if self.db_id:
            logger.info(f"Initialized SimpleAgent with database ID: {self.db_id}")
        
        # Extract template variables for memory handling
        self.template_vars = PromptBuilder.extract_template_variables(self.prompt_template)
        if self.template_vars:
            logger.info(f"Detected template variables: {', '.join(self.template_vars)}")
            
            # Initialize memory variables if we have an agent_id
            if self.db_id:
                try:
                    MemoryHandler.initialize_memory_variables_sync(
                        template_vars=self.template_vars,
                        agent_id=self.db_id,
                        user_id=None
                    )
                    logger.info(f"Memory variables initialized for agent ID {self.db_id}")
                except Exception as e:
                    logger.error(f"Error initializing memory variables: {str(e)}")
        
        # Create base system prompt
        base_system_prompt = PromptBuilder.create_base_system_prompt(self.prompt_template)
        
        # Initialize the base agent
        super().__init__(config, base_system_prompt)
        
        self._agent_instance: Optional[Agent] = None
        
        # Configure dependencies
        self.dependencies = SimpleAgentDependencies(
            model_name=get_model_name(config),
            model_settings=parse_model_settings(config)
        )
        
        # Set agent_id if available
        if self.db_id:
            self.dependencies.set_agent_id(self.db_id)
        
        # Set usage limits if specified in config
        usage_limits = create_usage_limits(config)
        if usage_limits:
            self.dependencies.set_usage_limits(usage_limits)
        
        # Initialize context
        self.context = {"agent_id": self.db_id}
        
        # Create tool registry and register default tools
        self.tool_registry = ToolRegistry()
        self.tool_registry.register_default_tools(self.context)
        
        logger.info("SimpleAgent initialized successfully")
    
    async def __aenter__(self):
        """Async context manager entry method."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit method."""
        await self.cleanup()
    
    def register_tool(self, tool_func) -> None:
        """Register a tool with the agent.
        
        Args:
            tool_func: The tool function to register
        """
        self.tool_registry.register_tool(tool_func)
    
    async def _initialize_agent(self) -> None:
        """Initialize the underlying PydanticAI agent."""
        if self._agent_instance is not None:
            return
            
        # Get model configuration
        model_name = self.dependencies.model_name
        model_settings = create_model_settings(self.dependencies.model_settings)
        
        # Convert tools to PydanticAI format
        tools = self.tool_registry.convert_to_pydantic_tools()
        logger.info(f"Prepared {len(tools)} tools for PydanticAI agent")
                    
        try:
            # Create agent instance
            self._agent_instance = Agent(
                model=model_name,
                system_prompt=self.prompt_template,
                tools=tools,
                model_settings=model_settings,
                deps_type=SimpleAgentDependencies
            )
            
            logger.info(f"Initialized agent with model: {model_name} and {len(tools)} tools")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}")
            raise
    
    async def cleanup(self) -> None:
        """Clean up resources used by the agent."""
        if self.dependencies.http_client:
            await close_http_client(self.dependencies.http_client)
    
    async def _get_filled_system_prompt(self) -> str:
        """Get the system prompt filled with memory variables.
        
        Returns:
            Filled system prompt
        """
        user_id = getattr(self.dependencies, 'user_id', None)
        
        if self.db_id:
            # Check and ensure memory variables exist
            MemoryHandler.check_and_ensure_memory_variables(
                template_vars=self.template_vars,
                agent_id=self.db_id,
                user_id=user_id
            )
            
            # Fetch memory variables
            memory_vars = await MemoryHandler.fetch_memory_vars(
                template_vars=self.template_vars,
                agent_id=self.db_id,
                user_id=user_id
            )
            
            # Get run ID from session manager
            run_id = f"run-{self.context.get('run_id', '')}"
            
            # Fill system prompt with variables
            return await PromptBuilder.get_filled_system_prompt(
                prompt_template=self.prompt_template,
                memory_vars=memory_vars,
                run_id=run_id,
                agent_id=self.db_id,
                user_id=user_id
            )
        else:
            logger.warning("No agent ID available for memory fetching, using template as is")
            return self.prompt_template
            
    async def process_message(self, user_message: Union[str, Dict[str, Any]], 
                              session_id: Optional[str] = None, 
                              agent_id: Optional[Union[int, str]] = None, 
                              user_id: int = 1, 
                              context: Optional[Dict] = None, 
                              message_history: Optional['MessageHistory'] = None) -> AgentResponse:
        """Process a user message.
        
        Args:
            user_message: User message text or dictionary with message details
            session_id: Optional session ID to use
            agent_id: Optional agent ID to use
            user_id: User ID to associate with the message (default 1)
            context: Optional context dictionary with additional parameters
            message_history: Optional MessageHistory instance for DB storage
            
        Returns:
            AgentResponse object with the agent's response
        """
        # Parse the user message
        content, metadata = parse_user_message(user_message)
        logger.info(f"Processing message from user {user_id}")
            
        # Update agent ID if provided
        if agent_id is not None and str(agent_id) != str(getattr(self, "db_id", None)):
            self.db_id = validate_agent_id(agent_id)
            self.dependencies.set_agent_id(self.db_id)
            logger.info(f"Updated agent ID to {self.db_id}")
        
        # Update user ID
        user_id = validate_user_id(user_id)
        self.dependencies.user_id = user_id
        
        # Update context
        self.context = create_context(
            agent_id=self.db_id, 
            user_id=user_id,
            session_id=session_id,
            additional_context=context
        )
        
        # Update tool registry with new context
        self.tool_registry.update_context(self.context)
        
        # Extract multimodal content if present
        multimodal_content = extract_multimodal_content(context)
        
        # Load message history if provided
        if message_history:
            try:
                db_messages = message_history.all_messages()
                if db_messages:
                    logger.info(f"Loaded {len(db_messages)} messages from message_history")
                    self.dependencies.set_message_history(db_messages)
            except Exception as e:
                logger.error(f"Error loading message history: {str(e)}")
        
        # Run the agent
        response = await self.run(
            content, 
            multimodal_content=multimodal_content,
            message_history_obj=message_history
        )
        
        # Save messages to database if message_history is provided
        if message_history:
            try:
                # Save user message
                user_db_message = format_message_for_db(
                    role="user",
                    content=content
                )
                await message_history.add_message(user_db_message)
                
                # Save agent response
                agent_db_message = format_message_for_db(
                    role="assistant",
                    content=response.text,
                    tool_calls=response.tool_calls,
                    tool_outputs=response.tool_outputs,
                    system_prompt=getattr(response, "system_prompt", None)
                )
                await message_history.add_message(agent_db_message)
                
                logger.info("Saved user message and agent response to the database")
            except Exception as e:
                logger.error(f"Error saving messages to database: {str(e)}")
                
        return response
        
    async def run(self, input_text: str, *, multimodal_content=None, system_message=None, message_history_obj: Optional[MessageHistory] = None) -> AgentResponse:
        """Run the agent with the given input.
        
        Args:
            input_text: Text input for the agent
            multimodal_content: Optional multimodal content
            system_message: Optional system message for this run (ignored in favor of template)
            message_history_obj: Optional MessageHistory instance for DB storage
            
        Returns:
            AgentResponse object with result and metadata
        """
        # Ensure memory variables are initialized if we have an agent ID
        if self.db_id:
            user_id = getattr(self.dependencies, 'user_id', None)
            
            try:
                MemoryHandler.check_and_ensure_memory_variables(
                    template_vars=self.template_vars,
                    agent_id=self.db_id,
                    user_id=user_id
                )
                logger.info(f"Memory variables checked and initialized for user_id: {user_id}")
            except Exception as e:
                logger.error(f"Error checking memory variables: {str(e)}")
                
        # Initialize the agent
        await self._initialize_agent()
        
        # Get message history in PydanticAI format
        pydantic_message_history = []
        if message_history_obj:
            pydantic_message_history = message_history_obj.get_formatted_pydantic_messages(limit=20)
        else:
            logger.info("No message history object provided, starting with empty history")
        
        # Prepare user input (handle multimodal content)
        user_input = input_text
        if multimodal_content:
            if hasattr(self.dependencies, 'configure_for_multimodal'):
                self.dependencies.configure_for_multimodal(True)
            user_input = {"text": input_text, "multimodal_content": multimodal_content}
        
        # We will ignore any provided system_message and always use our template with memory variables
        if system_message:
            logger.warning("Ignoring provided system_message in favor of template with dynamic variables")
        
        try:
            # Get usage limits
            usage_limits = getattr(self.dependencies, "usage_limits", None)
            
            # Get filled system prompt with memory variables
            filled_system_prompt = await self._get_filled_system_prompt()
            
            # Add system prompt to message history
            if filled_system_prompt:
                pydantic_message_history = add_system_message_to_history(
                    pydantic_message_history, 
                    filled_system_prompt
                )
            
            # Update dependencies with context
            if hasattr(self.dependencies, 'set_context') and self.context:
                self.dependencies.set_context(self.context)
                logger.info(f"Updated dependencies with context data: {self.context}")
        
            # Run the agent
            result = await self._agent_instance.run(
                user_input,
                message_history=pydantic_message_history,
                usage_limits=usage_limits,
                deps=self.dependencies
            )
            
            # Extract tool calls and outputs
            all_messages = extract_all_messages(result)
            tool_calls = []
            tool_outputs = []
            
            # Process each message to extract tool calls and outputs
            for msg in all_messages:
                tool_calls.extend(extract_tool_calls(msg))
                tool_outputs.extend(extract_tool_outputs(msg))
            
            # Create response with the tool calls and outputs
            return AgentResponse(
                text=result.data,
                success=True,
                tool_calls=tool_calls,
                tool_outputs=tool_outputs,
                raw_message=all_messages,
                system_prompt=filled_system_prompt,
            )
        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            logger.error(traceback.format_exc())
            return AgentResponse(
                text=f"Error: {str(e)}",
                success=False,
                error_message=str(e),
                raw_message=pydantic_message_history if 'pydantic_message_history' in locals() else None
            ) 