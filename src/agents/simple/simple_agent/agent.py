"""SimpleAgent implementation with PydanticAI.

This module provides a SimpleAgent class that uses PydanticAI for LLM integration.
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
from pydantic_ai.tools import Tool as PydanticTool, RunContext

from src.constants import (
    DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS, DEFAULT_RETRIES
)

from src.agents.models.base_agent import BaseAgent
from src.agents.models.dependencies import SimpleAgentDependencies
from src.agents.models.response import AgentResponse
from src.memory.message_history import MessageHistory

from src.agents.simple.simple_agent.prompt_builder import PromptBuilder
from src.agents.simple.simple_agent.memory_handler import MemoryHandler
from src.agents.simple.simple_agent.tool_registry import ToolRegistry, _import_memory_tools

from src.tools.datetime import get_current_date_tool, get_current_time_tool, format_date_tool

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
        
        self.db_id = config.get("agent_id")
        if self.db_id and isinstance(self.db_id, str) and self.db_id.isdigit():
            self.db_id = int(self.db_id)
            logger.info(f"Initialized SimpleAgent with database ID: {self.db_id}")
        else:
            self.db_id = None
        
        self.template_vars = PromptBuilder.extract_template_variables(self.prompt_template)
        if self.template_vars:
            logger.info(f"Detected template variables: {', '.join(self.template_vars)}")
            
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
        
        base_system_prompt = PromptBuilder.create_base_system_prompt(self.prompt_template)
        
        super().__init__(config, base_system_prompt)
        
        self._agent_instance: Optional[Agent] = None
        
        self.dependencies = SimpleAgentDependencies(
            model_name=config.get("model", DEFAULT_MODEL),
            model_settings=self._parse_model_settings(config)
        )
        
        if self.db_id:
            self.dependencies.set_agent_id(self.db_id)
        
        if "response_tokens_limit" in config or "request_limit" in config or "total_tokens_limit" in config:
            self._set_usage_limits(config)
        
        self.context = {"agent_id": self.db_id}
        
        self.tool_registry = ToolRegistry()
        self.tool_registry.register_default_tools(self.context)
        
        logger.info("SimpleAgent initialized successfully")
    
    def _parse_model_settings(self, config: Dict[str, str]) -> Dict[str, Any]:
        """Parse model settings from config.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dictionary with model settings
        """
        settings = {}
        
        for key, value in config.items():
            if key.startswith("model_settings."):
                setting_key = key.replace("model_settings.", "")
                settings[setting_key] = value
        
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
        response_tokens_limit = config.get("response_tokens_limit")
        request_limit = config.get("request_limit")
        total_tokens_limit = config.get("total_tokens_limit")
        
        if response_tokens_limit:
            response_tokens_limit = int(response_tokens_limit)
        if request_limit:
            request_limit = int(request_limit)
        if total_tokens_limit:
            total_tokens_limit = int(total_tokens_limit)
            
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
    
    def register_tool(self, tool_func: Callable) -> None:
        """Register a tool with the agent.
        
        Args:
            tool_func: The tool function to register
        """
        self.tool_registry.register_tool(tool_func)
    
    async def _initialize_agent(self) -> None:
        """Initialize the underlying PydanticAI agent with dynamic system prompts."""
        if self._agent_instance is not None:
            return
            
        model_name = self.dependencies.model_name
        model_settings = self._get_model_settings()
        
        tools = self.tool_registry.convert_to_pydantic_tools()
        logger.info(f"Prepared {len(tools)} tools for PydanticAI agent")
                    
        try:
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
    
    def _get_model_settings(self) -> Optional[ModelSettings]:
        """Get model settings for the PydanticAI agent.
        
        Returns:
            ModelSettings object with model configuration
        """
        settings = self.dependencies.model_settings.copy()
        
        if "temperature" not in settings:
            settings["temperature"] = DEFAULT_TEMPERATURE
        if "max_tokens" not in settings:
            settings["max_tokens"] = DEFAULT_MAX_TOKENS
        
        return ModelSettings(**settings)
    
    async def cleanup(self) -> None:
        """Clean up resources used by the agent."""
        if self.dependencies.http_client:
            await self.dependencies.close_http_client()
    
    async def _get_filled_system_prompt(self) -> str:
        """Get the system prompt filled with memory variables.
        
        Returns:
            Filled system prompt
        """
        run_id = f"run-{uuid.uuid4()}"
        user_id = getattr(self.dependencies, 'user_id', None)
        
        if self.db_id:
            MemoryHandler.check_and_ensure_memory_variables(
                template_vars=self.template_vars,
                agent_id=self.db_id,
                user_id=user_id
            )
            
            memory_vars = await MemoryHandler.fetch_memory_vars(
                template_vars=self.template_vars,
                agent_id=self.db_id,
                user_id=user_id
            )
            
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
        
        This method handles storing the user message to the database and running the agent.
        Maintains compatibility with the original API signature.
        
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
        logger.info(f"Processing message from user {user_id} with type: {type(user_message)}")
        
        if isinstance(user_message, dict):
            content = user_message.get("content", "")
        else:
            content = user_message
            
        if agent_id is not None and str(agent_id) != str(getattr(self, "db_id", None)):
            self.db_id = int(agent_id) if isinstance(agent_id, (str, int)) and str(agent_id).isdigit() else agent_id
            self.dependencies.set_agent_id(self.db_id)
            logger.info(f"Updated agent ID to {self.db_id}")
        
        self.dependencies.user_id = user_id
        self.context = {"agent_id": self.db_id, "user_id": user_id}
        
        multimodal_content = None
        if context and "multimodal_content" in context:
            multimodal_content = context["multimodal_content"]
        
        if message_history:
            try:
                db_messages = message_history.all_messages()
                if db_messages:
                    logger.info(f"Loaded {len(db_messages)} messages from message_history")
                    self.dependencies.set_message_history(db_messages)
                    logger.info(f"Updated dependencies with {len(db_messages)} messages from message_history")
            except Exception as e:
                logger.error(f"Error loading message history: {str(e)}")
                logger.error(traceback.format_exc())
        
        response = await self.run(
            content, 
            multimodal_content=multimodal_content,
            message_history_obj=message_history
        )
        
        if message_history:
            try:
                db_user_message = {
                    "role": "user",
                    "content": content
                }
                await message_history.add_message(db_user_message)
                
                db_agent_message = {
                    "role": "assistant",
                    "content": response.text,
                    "tool_calls": response.tool_calls,
                    "tool_outputs": response.tool_outputs,
                    "system_prompt": getattr(response, "system_prompt", None)
                }
                await message_history.add_message(db_agent_message)
                
                logger.info("Saved user message and agent response to the database")
            except Exception as e:
                logger.error(f"Error saving messages to database: {str(e)}")
                logger.error(traceback.format_exc())
                
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
                
        await self._initialize_agent()
        
        # Get message history in PydanticAI format
        pydantic_message_history = []
        if message_history_obj:
            pydantic_message_history = message_history_obj.get_formatted_pydantic_messages(limit=20)
        else:
            logger.info("No message history object provided, starting with empty history")
        
        user_input = input_text
        if multimodal_content:
            if hasattr(self.dependencies, 'configure_for_multimodal'):
                self.dependencies.configure_for_multimodal(True)
            user_input = {"text": input_text, "multimodal_content": multimodal_content}
        
        if system_message:
            logger.warning("Ignoring provided system_message in favor of template with dynamic variables")
        
        logger.info("Running agent with dynamic system prompt from template.py (reevaluated each run)")
        
        try:
            usage_limits = self.dependencies.usage_limits if hasattr(self.dependencies, "usage_limits") else None
            
            if hasattr(self, "system_prompt") and self.system_prompt:
                filled_system_prompt = await self._get_filled_system_prompt()
                
                from pydantic_ai.messages import ModelRequest, SystemPromptPart
                
                system_message = ModelRequest(
                    parts=[SystemPromptPart(content=filled_system_prompt)]
                )
                pydantic_message_history = [system_message] + (pydantic_message_history or [])
                logger.info(f"Added system prompt to message history")
                
            if hasattr(self.dependencies, 'set_context') and self.context:
                self.dependencies.set_context(self.context)
                logger.info(f"Updated dependencies with context data: {self.context}")
        
            result = await self._agent_instance.run(
                user_input,
                message_history=pydantic_message_history,
                usage_limits=usage_limits,
                deps=self.dependencies
            )
            
            tool_calls = []
            tool_outputs = []
            
            try:
                all_messages = result.all_messages()
                logger.info(f"Retrieved {len(all_messages)} messages from result")
                
                for msg in all_messages:
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
                    
                    if hasattr(msg, 'parts'):
                        for part in msg.parts:
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
                            
                            if (hasattr(part, 'part_kind') and part.part_kind == 'tool-return') or \
                               type(part).__name__ == 'ToolReturnPart' or \
                               (hasattr(part, 'tool_name') and hasattr(part, 'content')):
                                
                                content = getattr(part, 'content', None)
                                
                                tool_output = {
                                    'tool_name': getattr(part, 'tool_name', ''),
                                    'content': content,
                                    'tool_call_id': getattr(part, 'tool_call_id', getattr(part, 'id', ''))
                                }
                                tool_outputs.append(tool_output)
                                
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
            
            except Exception as e:
                logger.error(f"Error processing tool outputs: {str(e)}")
            
            return AgentResponse(
                text=result.data,
                success=True,
                tool_calls=tool_calls,
                tool_outputs=tool_outputs,
                raw_message=result.all_messages() if hasattr(result, "all_messages") else None,
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