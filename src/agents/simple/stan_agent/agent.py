"""StanAgentAgent implementation with PydanticAI.

This module provides a StanAgentAgent class that uses PydanticAI for LLM integration
and inherits common functionality from AutomagikAgent.
"""
import logging
import traceback
from typing import Dict, Any, Optional, Union, Tuple

from pydantic_ai import Agent
from src.agents.models.automagik_agent import AutomagikAgent
from src.agents.models.dependencies import AutomagikAgentsDependencies
from src.agents.models.response import AgentResponse
from src.agents.simple.stan_agent.models import EvolutionMessagePayload
from src.agents.simple.stan_agent.specialized.backoffice import backoffice_agent
from src.agents.simple.stan_agent.specialized.onboarding import onboarding_agent
from src.agents.simple.stan_agent.specialized.product import product_agent
from src.memory.message_history import MessageHistory
from src.agents.simple.stan_agent.utils import get_or_create_contact

# Import only necessary utilities
from src.agents.common.message_parser import (
    extract_tool_calls, 
    extract_tool_outputs,
    extract_all_messages
)
from src.agents.common.dependencies_helper import (
    parse_model_settings,
    create_model_settings,
    create_usage_limits,
    get_model_name,
    add_system_message_to_history
)
from src.tools import blackpearl

logger = logging.getLogger(__name__)

class StanAgentAgent(AutomagikAgent):
    """StanAgentAgent implementation using PydanticAI.
    
    This agent provides a basic implementation that follows the PydanticAI
    conventions for multimodal support and tool calling.
    """
    
    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize the StanAgentAgent.
        
        Args:
            config: Dictionary with configuration options
        """
        from src.agents.simple.stan_agent.prompts.prompt import AGENT_PROMPT
        
        # Initialize the base agent
        super().__init__(config, AGENT_PROMPT)
        
        # PydanticAI-specific agent instance
        self._agent_instance: Optional[Agent] = None
        
        # Configure dependencies
        self.dependencies = AutomagikAgentsDependencies(
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
        
        # Register default tools
        self.tool_registry.register_default_tools(self.context)
        
        # Register specialized agents         
        self.tool_registry.register_tool(backoffice_agent)
        self.tool_registry.register_tool(product_agent)
        self.tool_registry.register_tool(onboarding_agent)
        
        logger.info("StanAgentAgent initialized successfully")
    
    async def _initialize_pydantic_agent(self) -> None:
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
                system_prompt=self.system_prompt,
                tools=tools,
                model_settings=model_settings,
                deps_type=AutomagikAgentsDependencies
            )
            
            logger.info(f"Initialized agent with model: {model_name} and {len(tools)} tools")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}")
            raise
        
    async def run(self, input_text: str, *, multimodal_content=None, system_message=None, message_history_obj: Optional[MessageHistory] = None,
                 channel_payload: Optional[dict] = None,
                 message_limit: Optional[int] = 20) -> AgentResponse:
                
        # Convert channel_payload to EvolutionMessagePayload if provided
        evolution_payload = None
        if channel_payload:
            try:
                # Convert the dictionary to EvolutionMessagePayload model
                evolution_payload = EvolutionMessagePayload(**channel_payload)
                logger.debug("Successfully converted channel_payload to EvolutionMessagePayload")
            except Exception as e:
                logger.error(f"Failed to convert channel_payload to EvolutionMessagePayload: {str(e)}")
        
        # Extract user information
        user_number, user_name = None, None
        if evolution_payload:
            user_number = evolution_payload.get_user_number()
            user_name = evolution_payload.get_user_name()
            logger.debug(f"Extracted user info: number={user_number}, name={user_name}")
        
        # Get or create contact in BlackPearl
        contato_blackpearl = None
        if user_number:
            user_id = getattr(self.dependencies, 'user_id', 'unknown')
            contato_blackpearl = await get_or_create_contact(
                self.context, 
                user_number, 
                user_name,
                user_id,
                self.db_id
            )
            5
            if contato_blackpearl:
                user_name = contato_blackpearl.get("nome", user_name)
                # Store contact_id in context for future use if needed
                self.context["blackpearl_contact_id"] = contato_blackpearl.get("id")
                
                # Set user information in dependencies if available
                if hasattr(self.dependencies, 'set_user_info'):
                    self.dependencies.set_user_info({
                        "name": user_name,
                        "phone": user_number,
                        "blackpearl_contact_id": contato_blackpearl.get("id")
                    })
            logger.info(f"🔮 BlackPearl Contact ID: {contato_blackpearl.get('id')} and Name: {user_name}")
        
        # Ensure memory variables are initialized
        if self.db_id:
            await self.initialize_memory_variables(getattr(self.dependencies, 'user_id', None))
            
        # Initialize the agent
        await self._initialize_pydantic_agent()
        
        
        # Get message history in PydanticAI format
        pydantic_message_history = []
        if message_history_obj:
            pydantic_message_history = message_history_obj.get_formatted_pydantic_messages(limit=message_limit)
        
        user_input = input_text
        try:
            # Get filled system prompt
            filled_system_prompt = await self.get_filled_system_prompt(
                user_id=getattr(self.dependencies, 'user_id', None)
            )
            
            # Add system prompt to message history
            if filled_system_prompt:
                pydantic_message_history = add_system_message_to_history(
                    pydantic_message_history, 
                    filled_system_prompt
                )
            
            # Update dependencies with context
            if hasattr(self.dependencies, 'set_context'):
                self.dependencies.set_context(self.context)
        
            # Run the agent
            result = await self._agent_instance.run(
                user_input,
                message_history=pydantic_message_history,
                usage_limits=getattr(self.dependencies, "usage_limits", None),
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
            
            # Create response
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