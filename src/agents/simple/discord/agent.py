"""DiscordAgent implementation with PydanticAI.

This module provides a DiscordAgent class that uses PydanticAI for LLM integration
and inherits common functionality from AutomagikAgent.
"""
import logging
import traceback
import os
from typing import Dict, Any, Optional

from pydantic_ai import Agent, RunContext
from src.agents.models.automagik_agent import AutomagikAgent
from src.agents.models.dependencies import AutomagikAgentsDependencies
from src.agents.models.response import AgentResponse
from src.memory.message_history import MessageHistory

# Import Discord tools
from src.tools.discord.tool import (
    list_guilds_and_channels,
    get_guild_info,
    fetch_messages,
    send_message
)

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

logger = logging.getLogger(__name__)

class DiscordAgent(AutomagikAgent):
    """DiscordAgent implementation using PydanticAI.
    
    This agent provides Discord functionality that follows the PydanticAI
    conventions for tool calling.
    """
    
    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize the DiscordAgent.
        
        Args:
            config: Dictionary with configuration options
        """
        from src.agents.simple.discord.prompts.prompt import AGENT_PROMPT
        
        # Initialize the base agent
        super().__init__(config)
        
        # Register the code-defined prompt for this agent
        # This call is asynchronous but we're in a synchronous __init__,
        # so we'll register the prompt later during the first run
        self._prompt_registered = False
        self._code_prompt_text = AGENT_PROMPT
        
        # PydanticAI-specific agent instance
        self._agent_instance: Optional[Agent] = None
        
        # Get Discord bot token from config or environment variable
        self.discord_bot_token = config.get("DISCORD_BOT_TOKEN") or os.environ.get("DISCORD_BOT_TOKEN")
        if not self.discord_bot_token:
            logger.warning("DISCORD_BOT_TOKEN not provided in config or environment variables")
        
        # Configure dependencies
        self.dependencies = AutomagikAgentsDependencies(
            model_name=get_model_name(config=config),
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
        
        logger.info("DiscordAgent initialized successfully")
    
    async def _initialize_pydantic_agent(self) -> None:
        """Initialize the underlying PydanticAI agent."""
        if self._agent_instance is not None:
            return
            
        # Get model configuration
        model_name = self.dependencies.model_name
        model_settings = create_model_settings(self.dependencies.model_settings, model_name)
        
        # Convert tools to PydanticAI format
        tools = self.tool_registry.convert_to_pydantic_tools()
        
        # Add Discord tools via wrappers
        tools.append(self._create_list_guilds_wrapper())
        tools.append(self._create_guild_info_wrapper())
        tools.append(self._create_fetch_messages_wrapper())
        tools.append(self._create_send_message_wrapper())

        logger.info(f"Prepared {len(tools)} tools for PydanticAI agent")
                    
        try:
            # Create agent instance
            self._agent_instance = Agent(
                model='openai:gpt-4.1',
                tools=tools,
                model_settings=model_settings,
                deps_type=AutomagikAgentsDependencies
            )
            
            logger.info(f"Initialized agent with model: {model_name} and {len(tools)} tools")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}")
            raise
    
    def _create_list_guilds_wrapper(self):
        """Create a wrapper for the list_guilds_and_channels function.
        
        Returns:
            A wrapped version of the list_guilds_and_channels function.
        """
        # Capture references to required variables
        bot_token = self.discord_bot_token
        
        async def list_guilds_wrapper(ctx: RunContext[AutomagikAgentsDependencies]) -> Dict[str, Any]:
            """Lists all guilds and channels the bot has access to.
            
            Args:
                ctx: The run context with dependencies
                
            Returns:
                Dict with the guild and channel information
            """
            return await list_guilds_and_channels(ctx, bot_token)
            
        return list_guilds_wrapper

    def _create_guild_info_wrapper(self):
        """Create a wrapper for the get_guild_info function.
        
        Returns:
            A wrapped version of the get_guild_info function.
        """
        # Capture references to required variables
        bot_token = self.discord_bot_token
        
        async def guild_info_wrapper(ctx: RunContext[AutomagikAgentsDependencies], guild_id: str) -> Dict[str, Any]:
            """Retrieves information about a specific guild.
            
            Args:
                ctx: The run context with dependencies
                guild_id: ID of the guild to retrieve information for
                
            Returns:
                Dict with the guild information
            """
            return await get_guild_info(ctx, bot_token, guild_id)
            
        return guild_info_wrapper

    def _create_fetch_messages_wrapper(self):
        """Create a wrapper for the fetch_messages function.
        
        Returns:
            A wrapped version of the fetch_messages function.
        """
        # Capture references to required variables
        bot_token = self.discord_bot_token
        
        async def fetch_messages_wrapper(ctx: RunContext[AutomagikAgentsDependencies], channel_id: str, limit: int = 100) -> Dict[str, Any]:
            """Fetches messages from a specific channel.
            
            Args:
                ctx: The run context with dependencies
                channel_id: ID of the channel to fetch messages from
                limit: Maximum number of messages to retrieve
                
            Returns:
                Dict with the fetched messages
            """
            return await fetch_messages(ctx, bot_token, channel_id, limit)
            
        return fetch_messages_wrapper

    def _create_send_message_wrapper(self):
        """Create a wrapper for the send_message function.
        
        Returns:
            A wrapped version of the send_message function.
        """
        # Capture references to required variables
        bot_token = self.discord_bot_token
        
        async def send_message_wrapper(ctx: RunContext[AutomagikAgentsDependencies], channel_id: str, content: str) -> Dict[str, Any]:
            """Sends a message to a specific channel.
            
            Args:
                ctx: The run context with dependencies
                channel_id: ID of the channel to send the message to
                content: Content of the message to send
                
            Returns:
                Dict with information about the sent message
            """
            return await send_message(ctx, bot_token, channel_id, content)
            
        return send_message_wrapper
        
    async def run(self, input_text: str, *, multimodal_content=None, system_message=None, message_history_obj: Optional[MessageHistory] = None,
                 channel_payload: Optional[Dict] = None,
                 message_limit: Optional[int] = 20) -> AgentResponse:
        """Run the agent with the given input.
        
        Args:
            input_text: Text input for the agent
            multimodal_content: Optional multimodal content
            system_message: Optional system message for this run (ignored in favor of template)
            message_history_obj: Optional MessageHistory instance for DB storage
            channel_payload: Optional channel payload, which might contain config
            
        Returns:
            AgentResponse object with result and metadata
        """
        # Check for token in channel_payload (API calls will send it here)
        if channel_payload and isinstance(channel_payload, dict):
            config = channel_payload.get("config", {})
            if isinstance(config, dict) and "DISCORD_BOT_TOKEN" in config:
                token = config.get("DISCORD_BOT_TOKEN")
                if token and isinstance(token, str):
                    logger.info("Using Discord token from channel_payload")
                    self.discord_bot_token = token
        
        # Validate token
        if not self.discord_bot_token:
            return AgentResponse(
                text="Error: Discord bot token is required but was not provided",
                success=False,
                error_message="DISCORD_BOT_TOKEN is required"
            )

        # Register the code-defined prompt if not already done
        await self._check_and_register_prompt()
        
        # Load the active prompt template for this agent
        await self.load_active_prompt_template(status_key="default")
        
        # Ensure memory variables are initialized
        if self.db_id:
            await self.initialize_memory_variables(getattr(self.dependencies, 'user_id', None))
                
        # Initialize the agent
        await self._initialize_pydantic_agent()
        
        # Get message history in PydanticAI format
        pydantic_message_history = []
        if message_history_obj:
            pydantic_message_history = message_history_obj.get_formatted_pydantic_messages(limit=message_limit)
        
        # Prepare user input (handle multimodal content)
        user_input = input_text
        
        if multimodal_content:
            if hasattr(self.dependencies, 'configure_for_multimodal'):
                self.dependencies.configure_for_multimodal(True)
            user_input = {"text": input_text, "multimodal_content": multimodal_content}
        
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
                text=result.output,
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