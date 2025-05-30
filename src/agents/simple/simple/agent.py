"""SimpleAgent implementation with PydanticAI.

This module provides a SimpleAgent class that uses PydanticAI for LLM integration
and inherits common functionality from AutomagikAgent.
"""
import logging
import traceback
from typing import Dict, Optional, List, Any
import asyncio

from pydantic_ai import Agent
from pydantic_ai.tools import RunContext
from src.config import settings
from src.agents.models.automagik_agent import AutomagikAgent
from src.agents.models.dependencies import AutomagikAgentsDependencies
from src.agents.models.response import AgentResponse
from src.memory.message_history import MessageHistory
from src.agents.common.evolution import EvolutionMessagePayload

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

class SimpleAgent(AutomagikAgent):
    """SimpleAgent implementation using PydanticAI.
    
    This agent provides a basic implementation that follows the PydanticAI
    conventions for multimodal support and tool calling.
    """
    
    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize the SimpleAgent.
        
        Args:
            config: Dictionary with configuration options
        """
        # First initialize the base agent without a system prompt
        super().__init__(config)
        
        # Load and register the code-defined prompt
        from src.agents.simple.simple.prompts.prompt import AGENT_PROMPT
        
        # Register the code-defined prompt for this agent
        # This call is asynchronous but we're in a synchronous __init__,
        # so we'll register the prompt later during the first run
        self._prompt_registered = False
        self._code_prompt_text = AGENT_PROMPT
        
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
        
        # Register Evolution tools with context-aware wrappers
        self.tool_registry.register_tool(self._create_send_reaction_wrapper())
        self.tool_registry.register_tool(self._create_send_text_wrapper())
        
        # MCP Servers - Will be loaded fresh on each run to ensure latest configurations
        # Don't cache MCP servers or client manager to avoid synchronization issues
        
        logger.info("SimpleAgent initialized successfully")
    
    def _convert_image_payload_to_pydantic(self, image_item_payload: Dict[str, Any]) -> Any:
        """Convert image payload to PydanticAI format.
        
        Args:
            image_item_payload: Image payload dict with 'data' and 'mime_type' keys
            
        Returns:
            ImageUrl object for PydanticAI or original payload if conversion fails
        """
        try:
            from pydantic_ai import ImageUrl, BinaryContent
        except ImportError:
            ImageUrl = None
            BinaryContent = None

        if not ImageUrl:  # PydanticAI types not available
            return image_item_payload

        # image_item_payload is expected to be like {'data': 'url_or_base64', 'mime_type': 'image/jpeg'}
        data_content = image_item_payload.get("data")
        mime_type = image_item_payload.get("mime_type", "")

        if isinstance(data_content, str) and mime_type.startswith("image/"):
            if data_content.lower().startswith("http"):
                # Remote image (HTTP/S) → wrap as ImageUrl
                logger.debug(f"Converting image URL to ImageUrl object: {data_content[:100]}…")
                return ImageUrl(url=data_content)
        
        logger.debug(f"Image payload not converted to ImageUrl/BinaryContent: {str(image_item_payload)[:100]}…")
        return image_item_payload  # Return original if not a convertible image URL

    async def _load_mcp_servers(self) -> List:
        """Load RUNNING MCP servers assigned to this agent from the MCP client manager.
        
        PydanticAI expects servers to already be running (is_running=True) when passed
        to the Agent constructor. This method gets running server instances from our
        MCP server manager instead of creating fresh ones.
        
        Returns:
            List of running MCP server instances for PydanticAI
        """
        try:
            # Import MCP refresh function
            from src.mcp.client import refresh_mcp_client_manager
            
            # Force refresh to ensure we get the latest server configurations
            mcp_client_manager = await refresh_mcp_client_manager()
            
            # Get servers assigned to this agent (use 'simple' name for MCP server assignment)
            agent_name = 'simple'  # Use 'simple' for MCP servers
            servers = mcp_client_manager.get_servers_for_agent(agent_name)
            
            # Get RUNNING server instances from our MCP server manager
            mcp_servers = []
            for server_manager in servers:
                try:
                    # Check if the server is running in our manager
                    if server_manager.is_running and server_manager._server:
                        # Get the server instance from our manager
                        # Note: The server instance exists but may not be in running state
                        # We need to start it for PydanticAI
                        server_instance = server_manager._server
                        
                        # Start the server if it's not already running
                        if not server_instance.is_running:
                            try:
                                # Enter the server context to make it running
                                server_manager._server_context = await server_instance.__aenter__()
                                logger.debug(f"Started MCP server context for PydanticAI: {server_manager.name}")
                            except Exception as e:
                                logger.warning(f"Failed to start server context for {server_manager.name}: {str(e)}")
                                continue
                        
                        if server_instance.is_running:
                            mcp_servers.append(server_instance)
                            logger.debug(f"Added running MCP server for PydanticAI: {server_manager.name}")
                        else:
                            logger.warning(f"MCP server {server_manager.name} could not be started")
                    else:
                        logger.info(f"MCP server {server_manager.name} is not running, skipping for agent")
                        
                except Exception as e:
                    logger.warning(f"Failed to get running MCP server instance for {server_manager.name}: {str(e)}")
                    continue
            
            logger.info(f"Loaded {len(mcp_servers)} running MCP server instances for PydanticAI")
            return mcp_servers
            
        except Exception as e:
            logger.warning(f"Failed to load MCP servers: {str(e)}. Continuing without MCP servers.")
            return []

    async def _initialize_pydantic_agent(self) -> None:
        """Initialize the underlying PydanticAI agent.
        
        Always reloads MCP servers to ensure fresh configurations
        even if the agent instance is cached.
        """
        # Always load fresh MCP servers to ensure synchronization with API updates
        mcp_servers = await self._load_mcp_servers()
        
        # If agent exists but MCP servers changed, recreate it
        if self._agent_instance is not None:
            # Check if MCP servers have changed by comparing count
            current_mcp_count = len(getattr(self._agent_instance, 'mcp_servers', []))
            new_mcp_count = len(mcp_servers)
            
            if current_mcp_count == new_mcp_count:
                # Same count, assume no changes needed
                logger.debug(f"Agent already initialized with {current_mcp_count} MCP servers")
                return
            else:
                # MCP servers changed, need to recreate agent
                logger.info(f"MCP servers changed ({current_mcp_count} -> {new_mcp_count}), recreating agent")
                self._agent_instance = None
            
        # Get model configuration
        model_name = self.dependencies.model_name
        model_settings = create_model_settings(self.dependencies.model_settings)
        
        # Convert tools to PydanticAI format
        tools = self.tool_registry.convert_to_pydantic_tools()
        logger.info(f"Prepared {len(tools)} tools for PydanticAI agent")
                    
        try:
            # Create agent instance with fresh MCP servers
            self._agent_instance = Agent(
                model=model_name,
                tools=tools,
                model_settings=model_settings,
                deps_type=AutomagikAgentsDependencies,
                mcp_servers=mcp_servers  # Fresh servers loaded each time
            )
            
            logger.info(f"Initialized Simple agent with model: {model_name}, {len(tools)} tools, and {len(mcp_servers)} MCP servers")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}")
            raise
        
    async def run(self, input_text: str, *, multimodal_content=None, system_message=None, message_history_obj: Optional[MessageHistory] = None,
                 channel_payload: Optional[Dict] = None,
                 message_limit: Optional[int] = 20) -> AgentResponse:
        """Run the agent with the given input.
        
        Args:
            input_text: Text input for the agent
            multimodal_content: Optional multimodal content
            system_message: Optional system message for this run (ignored in favor of template)
            message_history_obj: Optional MessageHistory instance for DB storage
            channel_payload: Optional Evolution payload dictionary
            
        Returns:
            AgentResponse object with result and metadata
        """
        
        # -------------------------------------------------------------
        # Evolution (WhatsApp) channel payload handling
        # -------------------------------------------------------------
        evolution_payload = None  # type: Optional[EvolutionMessagePayload]
        if channel_payload:
            try:
                # Convert raw dict coming from webhook into the Pydantic model
                evolution_payload = EvolutionMessagePayload(**channel_payload)
                logger.debug(
                    "Successfully converted channel_payload to EvolutionMessagePayload"
                )
            except Exception as e:
                logger.error(
                    f"Failed to convert channel_payload to EvolutionMessagePayload: {str(e)}"
                )

        if evolution_payload is not None:
            # Make it available in context/dependencies
            self.context["evolution_payload"] = evolution_payload

            if hasattr(self.dependencies, 'set_context'):
                combined_ctx = {**getattr(self.dependencies, 'context', {}), "evolution_payload": evolution_payload}
                self.dependencies.set_context(combined_ctx)

            # Extract basic user info from the payload
            user_number: Optional[str] = None
            user_name: Optional[str] = None

            try:
                user_number = evolution_payload.get_user_number()
                user_name = evolution_payload.get_user_name()
                logger.debug(
                    f"Extracted user info from evolution_payload: number={user_number}, name={user_name}"
                )
                
                # Set user_phone_number and user_name in context for test compatibility
                if user_number:
                    self.context["user_phone_number"] = user_number
                if user_name:
                    self.context["user_name"] = user_name
                    
            except Exception as e:
                logger.error(f"Error extracting user info from evolution_payload: {str(e)}")

            
            # Detect if we are in a group chat
            if evolution_payload.is_group_chat():
                self.context["is_group_chat"] = True
                self.context["group_jid"] = evolution_payload.get_group_jid()
            else:
                self.context.pop("is_group_chat", None)
                self.context.pop("group_jid", None)
                
            # Persist user information into memory so it can be injected into the
            # system prompt via the {{user_information}} template variable (same
            # pattern used by StanAgent).
            if self.db_id and (user_number or user_name):
                try:
                    from src.db.models import Memory
                    from src.db.repository import create_memory

                    # Build info dict without None values
                    info_dict: Dict[str, Any] = {
                        k: v for k, v in {
                            "user_name": user_name,
                            "user_number": user_number,
                        }.items() if v is not None
                    }

                    if info_dict:
                        memory_to_create = Memory(
                            name="user_information",
                            content=str(info_dict),
                            user_id=self.context.get("user_id"),
                            agent_id=self.db_id,
                            read_mode="system_prompt",
                            access="read_write",
                        )

                        create_memory(memory=memory_to_create)
                        logger.info("Created/Updated user_information memory for SimpleAgent run")
                except Exception as e:
                    logger.error(f"Failed to create user_information memory: {str(e)}")

        # Register the code-defined prompt if not already done
        await self._check_and_register_prompt()
        
        # Load the active prompt template for this agent
        await self.load_active_prompt_template(status_key="default")
        
        # Ensure memory variables are initialized
        if self.db_id:
            await self.initialize_memory_variables(getattr(self.dependencies, 'user_id', None))
        
        # Get message history in PydanticAI format
        pydantic_message_history = []
        if message_history_obj:
            pydantic_message_history = message_history_obj.get_formatted_pydantic_messages(limit=message_limit)
        
        # Prepare user input (handle multimodal content)
        user_input = input_text if input_text else "empty message" # Default to text-only or empty message

        if multimodal_content:
            # This call is a placeholder in dependencies, but good to keep for intent
            if hasattr(self.dependencies, 'configure_for_multimodal'):
                self.dependencies.configure_for_multimodal(True)
            
            # Attempt to import the rich multimodal types from *pydantic_ai*.
            # We fall back gracefully if running with an older/stripped version
            # of the library.
            try:
                from pydantic_ai import ImageUrl, BinaryContent  # type: ignore
            except ImportError:
                ImageUrl = None  # type: ignore
                BinaryContent = None  # type: ignore

            pydantic_ai_input_list: list[Any] = [input_text] # Start with the text prompt
            successfully_converted_at_least_one = False

            # Process the 'images' list from the multimodal_content dictionary
            if isinstance(multimodal_content, dict) and "images" in multimodal_content:
                image_list = multimodal_content.get("images", [])
                if isinstance(image_list, list):
                    for item_payload in image_list:
                        if isinstance(item_payload, dict): # Ensure item in list is a dict
                            converted_obj = self._convert_image_payload_to_pydantic(item_payload)
                            if converted_obj != item_payload:  # Successfully converted
                                successfully_converted_at_least_one = True
                            pydantic_ai_input_list.append(converted_obj)
                        else:
                            pydantic_ai_input_list.append(item_payload) # Append as-is if not a dict
            # TODO: Add elif clauses here to handle other direct multimodal_content structures if necessary,
            # e.g., if multimodal_content could be a list of URLs or a single URL string directly.
            # For now, focusing on the {'images': [...]} structure from the API controller.
            
            if successfully_converted_at_least_one:
                user_input = pydantic_ai_input_list
                logger.debug(f"Using PydanticAI list format for user_input: {str(user_input)[:200]}")
            else:
                # Fallback if no items were successfully converted to PydanticAI objects
                user_input = {"text": input_text, "multimodal_content": multimodal_content}
                logger.debug(f"Using legacy dict format for user_input: {str(user_input)[:200]}")
        
        try:
            # Initialize the agent
            await self._initialize_pydantic_agent()
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
        
            # Run the agent with concurrency limit and retry logic
            # MCP servers are now properly managed by our MCPServerManager
            from src.agents.models.automagik_agent import get_llm_semaphore
            semaphore = get_llm_semaphore()
            retries = settings.LLM_RETRY_ATTEMPTS
            last_exc: Optional[Exception] = None
            
            async with semaphore:
                for attempt in range(1, retries + 1):
                    try:
                        result = await self._agent_instance.run(
                            user_input,
                            message_history=pydantic_message_history,
                            usage_limits=getattr(self.dependencies, "usage_limits", None),
                            deps=self.dependencies
                        )
                        break  # success
                    except Exception as e:
                        last_exc = e
                        logger.warning(f"LLM call attempt {attempt}/{retries} failed: {e}")
                        if attempt < retries:
                            await asyncio.sleep(2 ** (attempt - 1))
                        else:
                            raise
            
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

    # ------------------------------------------------------------------
    # Evolution tool wrappers
    # ------------------------------------------------------------------

    def _create_send_reaction_wrapper(self):
        """Wrap send_reaction to auto-fill JIDs from evolution payload."""
        from src.tools.evolution.tool import send_reaction as evo_send_reaction

        async def send_reaction_wrapper(
            ctx: RunContext[AutomagikAgentsDependencies],
            reaction: str,
        ) -> Dict[str, Any]:
            # Try multiple locations to mirror product.py logic
            evo_payload = None
            if hasattr(ctx, "evolution_payload"):
                evo_payload = ctx.evolution_payload
            if not evo_payload and hasattr(ctx, "deps") and hasattr(ctx.deps, "evolution_payload"):
                evo_payload = ctx.deps.evolution_payload
            if not evo_payload and hasattr(ctx, "deps") and hasattr(ctx.deps, "context") and ctx.deps.context:
                evo_payload = ctx.deps.context.get("evolution_payload")
            if not evo_payload and hasattr(ctx, "parent_context") and isinstance(ctx.parent_context, dict):
                evo_payload = ctx.parent_context.get("evolution_payload")

            if not evo_payload:
                return {"success": False, "error": "evolution_payload not found in context"}

            try:
                # -----------------------------
                # 1. Locate message key safely
                # -----------------------------
                key_obj = None
                if hasattr(evo_payload, "data") and hasattr(evo_payload.data, "key"):
                    key_obj = evo_payload.data.key  # new structure
                elif hasattr(evo_payload, "output") and hasattr(evo_payload.output, "key"):
                    key_obj = evo_payload.output.key  # legacy structure

                if not key_obj:
                    return {"success": False, "error": "Message key not found in payload"}

                remote_jid = getattr(key_obj, "remoteJid", None)
                message_id = getattr(key_obj, "id", None)
                if not remote_jid or not message_id:
                    return {"success": False, "error": "Missing remote_jid or message_id"}

                # -----------------------------
                # 2. Credentials / config
                # -----------------------------
                instance_name = getattr(evo_payload, "instance", None) or getattr(settings, "EVOLUTION_INSTANCE", "default")
                api_url       = getattr(evo_payload, "server_url", None) or getattr(settings, "EVOLUTION_API_URL", None)
                api_key       = getattr(evo_payload, "apikey", None)      or getattr(settings, "EVOLUTION_API_KEY", None)

                # -----------------------------
                # 3. Call evolution tool
                # -----------------------------
                return await evo_send_reaction(
                    ctx,
                    remote_jid,
                    message_id,
                    reaction,
                    instance=instance_name,
                    api_url=api_url,
                    api_key=api_key,
                )
            except Exception as e:
                logger.error(f"send_reaction_wrapper error: {e}")
                return {"success": False, "error": str(e)}

        # Add metadata for tool registration
        send_reaction_wrapper.__name__ = "send_reaction"
        send_reaction_wrapper.__doc__ = "Send a reaction (emoji) to the last user message via Evolution. Auto-detects JID and message ID from context."
        return send_reaction_wrapper

    def _create_send_text_wrapper(self):
        """Wrap send_message tool to auto-fill phone number and instance."""
        from src.tools.evolution.tool import send_message as evo_send_text

        async def send_text_wrapper(
            ctx: RunContext[AutomagikAgentsDependencies],
            text: str,
        ) -> Dict[str, Any]:
            # Get evolution payload
            evo_payload = None
            if hasattr(ctx, "evolution_payload"):
                evo_payload = ctx.evolution_payload
            if not evo_payload and hasattr(ctx, "deps") and hasattr(ctx.deps, "evolution_payload"):
                evo_payload = ctx.deps.evolution_payload
            if not evo_payload and hasattr(ctx, "deps") and hasattr(ctx.deps, "context") and ctx.deps.context:
                evo_payload = ctx.deps.context.get("evolution_payload")
            if not evo_payload and hasattr(ctx, "parent_context") and isinstance(ctx.parent_context, dict):
                evo_payload = ctx.parent_context.get("evolution_payload")

            if not evo_payload:
                return {"success": False, "error": "evolution_payload not found"}

            try:
                phone_number = evo_payload.get_user_number()
                if not phone_number:
                    return {"success": False, "error": "Could not determine user number"}

                # Prefer credentials from payload, else config
                instance_name = getattr(evo_payload, "instance", None) or getattr(settings, "EVOLUTION_INSTANCE", "default")
                api_url       = getattr(evo_payload, "server_url", None) or getattr(settings, "EVOLUTION_API_URL", None)
                api_key       = getattr(evo_payload, "apikey", None)      or getattr(settings, "EVOLUTION_API_KEY", None)

                return await evo_send_text(
                    ctx,
                    phone=phone_number,
                    message=text,
                    instance=instance_name,
                    api_url=api_url,
                    token=api_key,
                )
            except Exception as e:
                logger.error(f"send_text_wrapper error: {e}")
                return {"success": False, "error": str(e)}

        send_text_wrapper.__name__ = "send_text_to_user"
        send_text_wrapper.__doc__ = "Send plain text to the current user via Evolution API. Auto-fills phone number."
        return send_text_wrapper

    # ------------------------------------------------------------------
    # Backwards-compatibility shim
    # ------------------------------------------------------------------
    async def _initialize_agent(self) -> None:  # noqa: D401
        """Alias maintained for legacy tests – delegates to `_initialize_pydantic_agent`."""
        await self._initialize_pydantic_agent() 