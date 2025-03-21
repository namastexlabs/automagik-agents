import importlib
import logging
from pathlib import Path
from typing import Dict, Type, List, Tuple
import uuid

from src.agents.models.base_agent import BaseAgent
from src.agents.models.agent_db import (
    register_agent,
    get_agent_by_name,
)

logger = logging.getLogger(__name__)


class AgentFactory:
    """Factory class for creating and managing agents."""

    _agents: Dict[
        str, Tuple[Type[BaseAgent], str]
    ] = {}  # Maps agent_name -> (agent_class, agent_type)
    _initialized_agents: Dict[str, BaseAgent] = {}
    _agent_db_ids: Dict[str, str] = {}  # Maps agent_name -> database_id

    @classmethod
    def discover_agents(cls) -> None:
        """Discover all available agents using standardized create_agent functions."""
        agents_dir = Path(__file__).parent.parent
        logger.info(f"Scanning for agents in directory: {agents_dir}")

        # Clear existing agents
        cls._agents.clear()
        cls._initialized_agents.clear()
        cls._agent_db_ids.clear()

        # Scan for agent type directories
        for type_dir in agents_dir.iterdir():
            if type_dir.is_dir() and type_dir.name not in ["models", "__pycache__"]:
                agent_type = type_dir.name
                
                # Check if the directory has an __init__.py file
                init_file = type_dir / "__init__.py"
                if init_file.exists():
                    logger.info(f"Found agent type directory with __init__.py: {type_dir}")
                    
                    # For each agent subdirectory, register it as an agent
                    for agent_dir in type_dir.iterdir():
                        if agent_dir.is_dir() and agent_dir.name != "__pycache__":
                            agent_name = agent_dir.name
                            full_agent_name = agent_name if agent_name.endswith("_agent") else f"{agent_name}_agent"
                            
                            logger.info(f"Registering agent: {full_agent_name} [Type: {agent_type}]")
                            
                            # Store the agent name and type for later initialization
                            # We'll use GenericAgent as a placeholder until actual initialization
                            class GenericAgent(BaseAgent):
                                def __init__(self, config=None):
                                    super().__init__(config or {}, f"Generic {full_agent_name}")
                                def register_tools(self):
                                    pass
                                def run(self, *args, **kwargs):
                                    pass
                                    
                            cls._agents[full_agent_name] = (GenericAgent, agent_type)

        # Report discovered agents
        if cls._agents:
            logger.info(f"Discovered {len(cls._agents)} agents: {', '.join(cls._agents.keys())}")
        else:
            logger.warning("No agents discovered!")

    @classmethod
    def get_agent(cls, agent_name: str) -> BaseAgent:
        """Get an initialized agent instance by name."""
        # Add _agent suffix if not present
        original_name = agent_name
        if not agent_name.endswith("_agent"):
            agent_name = f"{agent_name}_agent"

        # Refresh the agent instance to ensure run_id is always up to date
        if agent_name in cls._initialized_agents:
            # Force recreation of agent to refresh run_id
            del cls._initialized_agents[agent_name]
            logger.info(f"Forcing recreation of {agent_name} to refresh run_id")

        if agent_name not in cls._initialized_agents:
            if agent_name not in cls._agents:
                cls.discover_agents()
                if agent_name not in cls._agents:
                    available_agents = cls.list_available_agents()
                    raise ValueError(
                        f"Agent {agent_name} not found. Available agents: {', '.join(available_agents)}"
                    )

            # Get the agent type
            _, agent_type = cls._agents[agent_name]
            
            try:
                # Import the agent type module (e.g., src.agents.simple)
                type_module_path = f"src.agents.{agent_type}"
                type_module = importlib.import_module(type_module_path)
                
                # Get the base name without _agent suffix if needed
                base_name = agent_name.replace("_agent", "") if agent_name.endswith("_agent") else agent_name
                
                # Create the agent using the standardized function
                if hasattr(type_module, "create_agent") and callable(type_module.create_agent):
                    logger.info(f"Using create_agent from {type_module_path}")
                    agent = type_module.create_agent(base_name)
                else:
                    # Try to import the specific agent module as a fallback
                    agent_module_path = f"src.agents.{agent_type}.{base_name}"
                    try:
                        agent_module = importlib.import_module(agent_module_path)
                        if hasattr(agent_module, "create_agent"):
                            logger.info(f"Using create_agent from {agent_module_path}")
                            agent = agent_module.create_agent()
                        else:
                            raise AttributeError(f"Could not find create_agent function in {agent_module_path}")
                    except ImportError:
                        # Try with _agent suffix in the module path if base_name doesn't have it
                        if not base_name.endswith("_agent"):
                            agent_module_path = f"src.agents.{agent_type}.{base_name}_agent"
                            agent_module = importlib.import_module(agent_module_path)
                            if hasattr(agent_module, "create_agent"):
                                logger.info(f"Using create_agent from {agent_module_path}")
                                agent = agent_module.create_agent()
                            else:
                                raise AttributeError(f"Could not find create_agent function in {agent_module_path}")
                        else:
                            raise
                
                # Extract agent metadata for database registration
                agent_class = type(agent)
                config_dict = {}
                
                if hasattr(agent, "config"):
                    config = getattr(agent, "config")
                    # Ensure config is a dictionary
                    if isinstance(config, dict):
                        config_dict = config
                    else:
                        # Try to convert to dict if it has __dict__ attribute
                        if hasattr(config, "__dict__"):
                            config_dict = config.__dict__
                        else:
                            config_dict = {"value": str(config)}
                
                description = (
                    getattr(agent, "description", "") 
                    or getattr(agent_class, "__doc__", "") 
                    or f"{agent_name} agent"
                )
                model = config_dict.get("model", "")
                
                # Update the agent class in the registry
                cls._agents[agent_name] = (agent_class, agent_type)
                
                # Register in database if not already registered
                if agent_name not in cls._agent_db_ids:
                    try:
                        db_id = register_agent(
                            name=agent_name,
                            agent_type=agent_type,
                            model=model,
                            description=description,
                            config=config_dict,
                        )
                        cls._agent_db_ids[agent_name] = db_id
                        agent.db_id = db_id
                    except Exception as e:
                        logger.error(f"Failed to register agent {agent_name} in database: {str(e)}")
                else:
                    agent.db_id = cls._agent_db_ids[agent_name]
                
                # Store the initialized agent
                cls._initialized_agents[agent_name] = agent
                logger.info(f"Successfully initialized agent: {agent_name}")
                
            except Exception as e:
                logger.error(f"Failed to initialize agent {agent_name}: {str(e)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise ValueError(f"Failed to initialize agent {agent_name}: {str(e)}")

        return cls._initialized_agents[agent_name]

    @classmethod
    def list_available_agents(cls) -> List[str]:
        """List all available agent names."""
        if not cls._agents:
            cls.discover_agents()
        return list(cls._agents.keys())

    @classmethod
    def get_agent_type(cls, agent_name: str) -> str:
        """Get the type of an agent by name."""
        if not cls._agents:
            cls.discover_agents()

        if not agent_name.endswith("_agent"):
            agent_name = f"{agent_name}_agent"

        if agent_name not in cls._agents:
            available_agents = cls.list_available_agents()
            raise ValueError(
                f"Agent {agent_name} not found. Available agents: {', '.join(available_agents)}"
            )

        return cls._agents[agent_name][1]

    @classmethod
    def link_agent_to_session(cls, agent_name: str, session_id_or_name: str) -> bool:
        """Link an agent to a session in the database.
        
        Args:
            agent_name: The name of the agent to link
            session_id_or_name: Either a session ID or name
            
        Returns:
            True if the link was successful, False otherwise
        """
        # Check if the input is potentially a session name rather than a UUID
        session_id = session_id_or_name
        try:
            # Try to parse as UUID
            uuid.UUID(session_id_or_name)
        except ValueError:
            # Not a UUID, try to look up by name
            logger.info(f"Session ID is not a UUID, treating as session name: {session_id_or_name}")
            
            # Use the appropriate database function to get session by name
            from src.db import get_session_by_name
            
            session = get_session_by_name(session_id_or_name)
            if not session:
                logger.error(f"Session with name '{session_id_or_name}' not found")
                return False
                
            session_id = str(session.id)
            logger.info(f"Found session ID {session_id} for name {session_id_or_name}")

        # Now that we have a valid session ID, proceed with linking
        try:
            # Get the database ID for the agent name
            agent = None
            for name, (a_class, _) in cls._agents.items():
                if name == agent_name or f"{name}_agent" == agent_name:
                    a_instance = cls.get_agent(name)
                    agent_id = getattr(a_instance, "db_id", None)
                    if agent_id:
                        from src.db import link_session_to_agent
                        return link_session_to_agent(uuid.UUID(session_id), agent_id)

            # Try direct lookup by name in case the agent was registered directly in the database
            from src.db import get_agent_by_name, link_session_to_agent

            agent = get_agent_by_name(agent_name)
            if agent:
                return link_session_to_agent(uuid.UUID(session_id), agent.id)

            # Try with _agent suffix if needed
            agent_full_name = f"{agent_name}_agent" if not agent_name.endswith("_agent") else agent_name
            agent = get_agent_by_name(agent_full_name)
            if agent:
                return link_session_to_agent(uuid.UUID(session_id), agent.id)
                
            logger.error(f"Could not find agent with name '{agent_name}' to link to session")
            return False
        except Exception as e:
            logger.error(f"Error linking agent {agent_name} to session {session_id}: {str(e)}")
            return False
