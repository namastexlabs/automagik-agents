from typing import Dict, List, Optional, Any, Union
import logging
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from src.agents.models.base_agent import BaseAgent, AgentConfig
from src.agents.models.agent import AgentBaseResponse
from src.memory.message_history import MessageHistory
from .prompts.prompt import STAN_HOST_PROMPT
from .backoffice_agent import BackofficeAgent
from .product_agent import ProductAgent
from .models.response import StanAgentResponse
from pydantic_ai.usage import Usage

# Import tools - adjust these imports based on your actual project structure
try:
    from src.tools.blackpearl_tools import BlackPearlTools
    from src.tools.omie_tools import OmieTools
except ImportError:
    # Mock classes for development/testing
    class BlackPearlTools:
        def __init__(self, token): self.token = token
        def get_host_tools(self): return []
        async def search_contacts(self, user_id): return {"results": []}
        async def verify_cnpj(self, cnpj): return {}
        
    class OmieTools:
        def __init__(self, token): self.token = token
        def get_host_tools(self): return []

logger = logging.getLogger(__name__)

class UserContext(BaseModel):
    """User context information fetched from BlackPearl API."""
    user_id: str
    status: str = "NOT_REGISTERED"  # NOT_REGISTERED, REJECTED, APPROVED, VERIFYING
    name: Optional[str] = None
    phone: Optional[str] = None
    cnpj: Optional[str] = None
    company_name: Optional[str] = None
    company_data: Optional[Dict] = None
    
    @classmethod
    def from_blackpearl_response(cls, response_data: Dict) -> "UserContext":
        """Create a UserContext from BlackPearl API response."""
        if not response_data or "results" not in response_data or len(response_data["results"]) == 0:
            return cls(user_id="unknown", status="NOT_REGISTERED")
            
        user_data = response_data["results"][0]
        return cls(
            user_id=user_data.get("wpp_session_id", "unknown"),
            status=user_data.get("status_aprovacao", "NOT_REGISTERED"),
            name=user_data.get("nome"),
            phone=user_data.get("telefone")
        )

class StanAgentState(BaseModel):
    """State for the Stan Agent workflow."""
    prompt: str  # User input
    user_context: UserContext  # User context information
    history: MessageHistory  # Message history
    stage: str = "initial"  # Current stage: initial, collecting_info, verifying, approved
    action_needed: Optional[str] = None  # collect_cnpj, verify_info, etc.
    collected_data: Dict = Field(default_factory=dict)  # Data collected from user
    backoffice_response: Optional[Dict] = None  # Response from backoffice agent
    product_response: Optional[Dict] = None  # Response from product agent
    response: Optional[str] = None  # Final response to user
    usage: Usage = Field(default_factory=Usage)  # Usage metrics
    
    model_config = {
        "arbitrary_types_allowed": True
    }

class StanAgentWorkflow:
    """Graph-based workflow for Stan Agent."""
    
    class FetchUserContext(BaseNode[StanAgentState]):
        """Fetch user context from BlackPearl API."""
        
        def __init__(self, blackpearl_token: str):
            self.blackpearl_tools = BlackPearlTools(blackpearl_token)
            
        async def run(self, ctx: GraphRunContext[StanAgentState]) -> 'StanAgentWorkflow.DetermineAction':
            user_id = ctx.state.user_context.user_id
            
            try:
                # Fetch user data from BlackPearl
                user_data = await self.blackpearl_tools.search_contacts(user_id)
                
                # Update user context
                if user_data and "results" in user_data and len(user_data["results"]) > 0:
                    result = user_data["results"][0]
                    ctx.state.user_context = UserContext(
                        user_id=user_id,
                        status=result.get("status_aprovacao", "NOT_REGISTERED"),
                        name=result.get("nome"),
                        phone=result.get("telefone")
                    )
                    logger.info(f"User context updated: {ctx.state.user_context}")
                else:
                    logger.info(f"No user data found for user_id: {user_id}")
            except Exception as e:
                logger.error(f"Error fetching user context: {str(e)}")
            
            return StanAgentWorkflow.DetermineAction()
    
    class DetermineAction(BaseNode[StanAgentState]):
        """Determine next action based on user context and prompt."""
        
        def __init__(self, model_name: str = None):
            self.model_name = model_name
            self.agent = None
            
        def initialize_agent(self, model_name: str):
            if not self.agent:
                self.agent = Agent(
                    model=model_name,
                    system_prompt=STAN_HOST_PROMPT,
                    result_type=str
                )
            
        async def run(self, ctx: GraphRunContext[StanAgentState]) -> Union[
            'StanAgentWorkflow.CollectUserInfo',
            'StanAgentWorkflow.VerifyCNPJ',
            'StanAgentWorkflow.BackofficeProcess',
            'StanAgentWorkflow.ProductInfo',
            'StanAgentWorkflow.GenerateResponse']:
            
            self.initialize_agent(self.model_name)
            
            # Check user registration status
            status = ctx.state.user_context.status
            logger.info(f"Determining action for user with status: {status}")
            
            if status == "NOT_REGISTERED":
                # Check if CNPJ is already collected
                if not ctx.state.user_context.cnpj:
                    ctx.state.action_needed = "collect_cnpj"
                    ctx.state.stage = "collecting_info"
                    return StanAgentWorkflow.CollectUserInfo()
                else:
                    return StanAgentWorkflow.VerifyCNPJ()
                    
            elif status == "VERIFYING" or status == "APPROVED":
                # Determine if this is a product query
                # Use LLM to classify the query
                result = await self.agent.run(
                    ctx.state.prompt,
                    message_history=ctx.state.history.messages,
                    usage=ctx.state.usage
                )
                
                if "product" in result.data.lower():
                    return StanAgentWorkflow.ProductInfo()
                else:
                    return StanAgentWorkflow.BackofficeProcess()
            
            else:  # REJECTED or other
                # Handle rejected users
                ctx.state.response = "I'm sorry, your registration was not approved. Please contact our support team."
                return StanAgentWorkflow.GenerateResponse()
    
    class CollectUserInfo(BaseNode[StanAgentState]):
        """Collect required user information."""
        
        def __init__(self, model_name: str = None):
            self.model_name = model_name
            self.agent = None
            
        def initialize_agent(self, model_name: str):
            if not self.agent:
                self.agent = Agent(
                    model=model_name,
                    system_prompt="""
                    You are Stan, an assistant for Solid. Your task is to collect information from users.
                    If the user hasn't provided their CNPJ, ask for it politely.
                    If they have provided a CNPJ, confirm it and ask for any additional information needed.
                    Be professional and helpful.
                    """,
                    result_type=str
                )
            
        async def run(self, ctx: GraphRunContext[StanAgentState]) -> Union[
            'StanAgentWorkflow.VerifyCNPJ',
            'StanAgentWorkflow.GenerateResponse']:
            
            self.initialize_agent(self.model_name)
            
            # Check if CNPJ is in the prompt
            if "cnpj" in ctx.state.prompt.lower() or any(char.isdigit() for char in ctx.state.prompt):
                # Extract CNPJ-like pattern from the prompt
                import re
                cnpj_pattern = re.compile(r'\d{2}[\.\s]?\d{3}[\.\s]?\d{3}[\/\.\s]?\d{4}[\-\.\s]?\d{2}')
                match = cnpj_pattern.search(ctx.state.prompt)
                
                if match:
                    cnpj = match.group(0)
                    # Clean up the CNPJ
                    cnpj = ''.join(c for c in cnpj if c.isdigit())
                    ctx.state.user_context.cnpj = cnpj
                    ctx.state.collected_data["cnpj"] = cnpj
                    logger.info(f"CNPJ collected: {cnpj}")
                    return StanAgentWorkflow.VerifyCNPJ()
            
            # If no CNPJ found, generate a response asking for it
            result = await self.agent.run(
                "Please ask the user for their CNPJ number in a professional manner.",
                message_history=ctx.state.history.messages,
                usage=ctx.state.usage
            )
            
            ctx.state.response = result.data
            return StanAgentWorkflow.GenerateResponse()
    
    class VerifyCNPJ(BaseNode[StanAgentState]):
        """Verify CNPJ using BlackPearl API."""
        
        def __init__(self, blackpearl_token: str = None):
            self.blackpearl_token = blackpearl_token
            self.blackpearl_tools = None
            
        def initialize_tools(self, blackpearl_token: str):
            if not self.blackpearl_tools:
                self.blackpearl_tools = BlackPearlTools(blackpearl_token)
            
        async def run(self, ctx: GraphRunContext[StanAgentState]) -> Union[
            'StanAgentWorkflow.BackofficeProcess',
            'StanAgentWorkflow.GenerateResponse']:
            
            self.initialize_tools(self.blackpearl_token)
            
            try:
                # Verify CNPJ
                cnpj = ctx.state.user_context.cnpj
                logger.info(f"Verifying CNPJ: {cnpj}")
                
                cnpj_data = await self.blackpearl_tools.verify_cnpj(cnpj)
                
                if cnpj_data and "company" in cnpj_data:
                    # Store company data
                    ctx.state.user_context.company_data = cnpj_data
                    ctx.state.user_context.company_name = cnpj_data.get("company", {}).get("name")
                    ctx.state.collected_data["company_data"] = cnpj_data
                    ctx.state.stage = "verifying"
                    
                    logger.info(f"CNPJ verified successfully: {ctx.state.user_context.company_name}")
                    return StanAgentWorkflow.BackofficeProcess()
                else:
                    # Invalid CNPJ
                    ctx.state.response = "I couldn't verify this CNPJ. Please check the number and try again."
                    return StanAgentWorkflow.GenerateResponse()
                    
            except Exception as e:
                logger.error(f"Error verifying CNPJ: {str(e)}")
                ctx.state.response = "There was an error verifying your CNPJ. Please try again later."
                return StanAgentWorkflow.GenerateResponse()
    
    class BackofficeProcess(BaseNode[StanAgentState]):
        """Process user registration via Backoffice agent."""
        
        def __init__(self, backoffice_agent: BackofficeAgent = None):
            self.backoffice_agent = backoffice_agent
            
        async def run(self, ctx: GraphRunContext[StanAgentState]) -> 'StanAgentWorkflow.GenerateResponse':
            if not self.backoffice_agent:
                logger.error("Backoffice agent not initialized")
                ctx.state.response = "I'm having trouble processing your request. Please try again later."
                return StanAgentWorkflow.GenerateResponse()
                
            try:
                # Prepare the query for the backoffice agent
                if ctx.state.stage == "verifying":
                    # New registration
                    company_data = ctx.state.user_context.company_data
                    query = (
                        f"Process new user registration with CNPJ {ctx.state.user_context.cnpj}. "
                        f"Company name: {ctx.state.user_context.company_name}. "
                        f"User name: {ctx.state.user_context.name or 'Unknown'}. "
                        f"Phone: {ctx.state.user_context.phone or 'Unknown'}. "
                        f"Please register this user in our system."
                    )
                else:
                    # General query
                    query = f"Process user request: {ctx.state.prompt}"
                
                # Clone history and remove system prompts
                message_history = MessageHistory.from_model_messages(ctx.state.history.messages)
                message_history.remove_part_kind("system-prompt")
                
                # Run the backoffice agent
                result = await self.backoffice_agent.run(query, message_history)
                
                # Store the response
                ctx.state.backoffice_response = {
                    "message": result.message,
                    "action_taken": getattr(result, "action_taken", "none")
                }
                
                ctx.state.response = result.message
                return StanAgentWorkflow.GenerateResponse()
                
            except Exception as e:
                logger.error(f"Error in backoffice process: {str(e)}")
                ctx.state.response = "I'm having trouble processing your request with our backoffice. Please try again later."
                return StanAgentWorkflow.GenerateResponse()
    
    class ProductInfo(BaseNode[StanAgentState]):
        """Handle product information requests via Product agent."""
        
        def __init__(self, product_agent: ProductAgent = None):
            self.product_agent = product_agent
            
        async def run(self, ctx: GraphRunContext[StanAgentState]) -> 'StanAgentWorkflow.GenerateResponse':
            if not self.product_agent:
                logger.error("Product agent not initialized")
                ctx.state.response = "I'm having trouble retrieving product information. Please try again later."
                return StanAgentWorkflow.GenerateResponse()
                
            try:
                # Prepare the query for the product agent
                query = f"Provide product information for: {ctx.state.prompt}"
                
                # Clone history and remove system prompts
                message_history = MessageHistory.from_model_messages(ctx.state.history.messages)
                message_history.remove_part_kind("system-prompt")
                
                # Run the product agent
                result = await self.product_agent.run(query, message_history)
                
                # Store the response
                ctx.state.product_response = {
                    "message": result.message,
                    "product_found": getattr(result, "product_found", False)
                }
                
                ctx.state.response = result.message
                return StanAgentWorkflow.GenerateResponse()
                
            except Exception as e:
                logger.error(f"Error in product info process: {str(e)}")
                ctx.state.response = "I'm having trouble retrieving product information. Please try again later."
                return StanAgentWorkflow.GenerateResponse()
    
    class GenerateResponse(BaseNode[StanAgentState]):
        """Generate final response to user."""
        
        async def run(self, ctx: GraphRunContext[StanAgentState]) -> End[StanAgentResponse]:
            # Create a structured response
            response = StanAgentResponse(
                message=ctx.state.response or "I'm sorry, I couldn't process your request properly. Please try again.",
                user_state=ctx.state.user_context.status,
                client_info={
                    "name": ctx.state.user_context.name,
                    "phone": ctx.state.user_context.phone,
                    "cnpj": ctx.state.user_context.cnpj,
                    "company_name": ctx.state.user_context.company_name
                } if ctx.state.user_context.name else None,
                cnpj_data=ctx.state.user_context.company_data,
                backoffice_consulted=ctx.state.backoffice_response is not None,
                product_consulted=ctx.state.product_response is not None,
                actions_taken=[f"Stage: {ctx.state.stage}"] if ctx.state.stage != "initial" else []
            )
            
            # Update history with the response
            if not ctx.state.response:
                ctx.state.response = response.message
                
            ctx.state.history.add_message("assistant", response.message)
            return End(response)

class StanAgent(BaseAgent):
    """Stan agent implementation for client onboarding and product information using graph-based workflow."""
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the Stan agent with configuration."""
        # Flag to track if tools have been registered
        self._tools_registered = False
        
        # Validate required tokens
        required_tokens = ["blackpearl_token", "omie_token", "google_drive_token", "evolution_token"]
        for token in required_tokens:
            if token not in config:
                raise ValueError(f"{token} is required for StanAgent")
                
        # Store tokens
        self.tokens = {token: config[token] for token in required_tokens}
        
        # Initialize specialized agents
        self.backoffice_agent = BackofficeAgent(config)
        
        # Create config for product agent
        product_config = {
            "model": config.get("model", "openai:gpt-4o-mini"),
            "retries": config.get("retries", 3),
            "google_drive_token": self.tokens["google_drive_token"],
            "evolution_token": self.tokens["evolution_token"]
        }
        self.product_agent = ProductAgent(product_config)
        
        # Initialize graph nodes
        self.fetch_user_context = StanAgentWorkflow.FetchUserContext(self.tokens["blackpearl_token"])
        self.determine_action = StanAgentWorkflow.DetermineAction(config.get("model", "openai:gpt-4o-mini"))
        self.collect_user_info = StanAgentWorkflow.CollectUserInfo(config.get("model", "openai:gpt-4o-mini"))
        self.verify_cnpj = StanAgentWorkflow.VerifyCNPJ(self.tokens["blackpearl_token"])
        self.backoffice_process = StanAgentWorkflow.BackofficeProcess(self.backoffice_agent)
        self.product_info = StanAgentWorkflow.ProductInfo(self.product_agent)
        self.generate_response = StanAgentWorkflow.GenerateResponse()
        
        # Initialize graph
        self.graph = Graph(nodes=[
            StanAgentWorkflow.FetchUserContext,
            StanAgentWorkflow.DetermineAction,
            StanAgentWorkflow.CollectUserInfo,
            StanAgentWorkflow.VerifyCNPJ,
            StanAgentWorkflow.BackofficeProcess, 
            StanAgentWorkflow.ProductInfo,
            StanAgentWorkflow.GenerateResponse
        ])
        
        # Create AgentConfig object using the model from config or default
        model = config.get("model", "openai:gpt-4o-mini")
        self.config = AgentConfig(model=model)
        if "retries" in config:
            self.config.retries = config["retries"]
        
        # Store the system prompt
        self.system_prompt = STAN_HOST_PROMPT
        
        # Initialize the agent
        self.agent = self.initialize_agent()
        
        # Mark post-initialization as complete
        self._tools_registered = True

    def initialize_agent(self) -> Agent:
        """Initialize the Stan host agent with configuration."""
        agent = Agent(
            model=self.config.model,
            system_prompt=self.system_prompt,
            retries=self.config.retries,
            result_type=str
        )
        
        # Store the agent reference first to avoid circular dependency
        self.agent = agent
        
        # Register tools after setting self.agent
        self.register_tools(agent)
        
        return agent

    def register_tools(self, agent=None):
        """Register Stan-specific tools with the agent."""
        if agent is None:
            agent = getattr(self, 'agent', None)
            if agent is None:
                logger.warning("No agent available for tool registration")
                return
            
        # If tools have already been registered for this agent instance, skip
        if self._tools_registered and hasattr(self, 'agent') and agent == self.agent:
            logger.info("Tools already registered for this StanAgent instance, skipping registration")
            return
            
        # Initialize the tools
        blackpearl_tools = BlackPearlTools(self.tokens["blackpearl_token"])
        omie_tools = OmieTools(self.tokens["omie_token"])
        
        # Register BlackPearl tools
        for tool in blackpearl_tools.get_host_tools():
            agent.tool(tool)
            
        # Register Omie tools
        for tool in omie_tools.get_host_tools():
            agent.tool(tool)
            
        # Check if specialist tools are already registered to avoid conflicts
        tool_names = [t.name for t in getattr(agent, '_tools', [])]
        
        # Register specialist agent tools if not already registered
        if 'consult_backoffice_specialist' not in tool_names:
            @agent.tool
            async def consult_backoffice_specialist(ctx: RunContext[None], query: str) -> str:
                """Consult the backoffice specialist for client registration and management.
                
                Args:
                    query: The specific query about client registration, verification, or management
                    
                Returns:
                    Expert response about client status, registration, or account management
                """
                logger.info(f"Consulting backoffice specialist: {query}")
                
                # Extract message history from context
                message_history = MessageHistory.from_model_messages(ctx.messages)
                
                # Remove system prompt from history to avoid conflicts
                message_history.remove_part_kind("system-prompt")
                
                # Run the backoffice agent
                result = await self.backoffice_agent.run(query, message_history)
                
                return result.message
        
        if 'consult_product_specialist' not in tool_names:
            @agent.tool
            async def consult_product_specialist(ctx: RunContext[None], query: str) -> str:
                """Consult the product specialist for product information and details.
                
                Args:
                    query: The specific query about products, features, or availability
                    
                Returns:
                    Expert response about product specifications, features, or availability
                """
                logger.info(f"Consulting product specialist: {query}")
                
                # Extract message history from context
                message_history = MessageHistory.from_model_messages(ctx.messages)
                
                # Remove system prompt from history to avoid conflicts
                message_history.remove_part_kind("system-prompt")
                
                # Run the product agent
                result = await self.product_agent.run(query, message_history)
                
                return result.message
                
        # Mark tools as registered for this agent instance
        if hasattr(self, 'agent') and agent == self.agent:
            self._tools_registered = True

    async def run(self, user_message: str, message_history: MessageHistory) -> AgentBaseResponse:
        """Run the Stan agent with the given message and message history.
        
        Args:
            user_message: User message (already in message_history)
            message_history: Message history for this session
            
        Returns:
            Agent response
        """
        try:
            # Extract user ID from message history
            user_id = message_history.session_id
            
            # Initialize state
            state = StanAgentState(
                prompt=user_message,
                user_context=UserContext(user_id=user_id),
                history=message_history
            )
            
            # Add user message to history if not already there
            if not message_history.messages or message_history.messages[-1].get("role") != "user":
                message_history.add_message("user", user_message)
                state.history = message_history
            
            # Run the graph
            result = await self.graph.run(self.fetch_user_context, state=state)
            
            # Create and return the agent response
            return AgentBaseResponse.from_agent_response(
                message=result.message,
                history=message_history,
                error=None,
                session_id=message_history.session_id
            )
        except Exception as e:
            error_msg = f"Error running StanAgent: {str(e)}"
            logger.error(error_msg)
            return AgentBaseResponse.from_agent_response(
                message="An error occurred while processing your request.",
                history=message_history,
                error=error_msg,
                session_id=message_history.session_id
            )
