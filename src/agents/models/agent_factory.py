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
        """Discover all available agents in the agents directory."""
        agents_dir = Path(__file__).parent.parent
        logger.info(f"Scanning for agents in directory: {agents_dir}")

        # Clear existing agents
        cls._agents.clear()
        cls._initialized_agents.clear()
        cls._agent_db_ids.clear()

        # List of agent directories to scan (will include subdirectories of type directories)
        agent_dirs_to_scan = []
        
        # First, identify type directories and direct agent directories
        type_dirs = []
        for item in agents_dir.iterdir():
            if item.is_dir() and item.name not in ["models", "__pycache__"]:
                logger.info(f"Found potential agent directory: {item}")
                if (item / "__init__.py").exists():
                    logger.info(f"Detected directory with __init__.py: {item}")
                    # For top-level directories with __init__.py, try to load directly
                    if cls._try_load_agent_from_dir(item, item.name):
                        logger.info(f"Successfully loaded agent from {item}")
                    
                    # Always check if it's also a type directory (like 'simple')
                    type_dirs.append(item)
                else:
                    # It's a type directory without an __init__.py
                    type_dirs.append(item)
                    logger.info(f"Added {item} to type directories list")
        
        # Then, scan all type directories for agents
        for type_dir in type_dirs:
            agent_type = type_dir.name
            logger.info(f"Scanning type directory: {type_dir} (agent_type: {agent_type})")
            
            for agent_dir in type_dir.iterdir():
                if agent_dir.is_dir() and agent_dir.name not in ["__pycache__"]:
                    if (agent_dir / "__init__.py").exists():
                        logger.info(f"Found agent directory: {agent_dir}")
                        if cls._try_load_agent_from_dir(agent_dir, agent_type):
                            logger.info(f"Successfully loaded agent from {agent_dir} as type {agent_type}")
                    else:
                        logger.info(f"Skipping directory without __init__.py: {agent_dir}")
        
        # Report discovered agents
        if cls._agents:
            logger.info(f"Discovered {len(cls._agents)} agents: {', '.join(cls._agents.keys())}")
        else:
            logger.warning("No agents discovered!")

    @classmethod
    def _try_load_agent_from_dir(cls, agent_dir: Path, agent_type: str = None) -> bool:
        """Try to load an agent from a specific directory.

        Args:
            agent_dir: Directory to try loading agent from
            agent_type: Optional agent type (if None, uses the parent directory name)

        Returns:
            bool: True if agent was successfully loaded, False otherwise
        """
        try:
            # Generate module path directly from directory structure
            # Instead of using relative_to which can cause issues with absolute paths
            agent_dir_str = str(agent_dir)
            src_index = agent_dir_str.find("src/agents")
            if src_index == -1:
                logger.error(f"Failed to find src/agents in path: {agent_dir_str}")
                return False
            
            # Extract path relative to the src directory
            rel_path = agent_dir_str[src_index:]
            module_path = rel_path.replace("/", ".")
            logger.info(f"Attempting to load agent from module path: {module_path}")

            # Try to import the agent module
            module = importlib.import_module(module_path)

            # Check for default_agent in the module
            if hasattr(module, "default_agent"):
                # Use the folder name as the agent name
                agent_name = agent_dir.name
                agent_instance = getattr(module, "default_agent")

                if (
                    agent_instance is not None
                ):  # Some agents might be conditionally initialized
                    cls._initialized_agents[agent_name] = agent_instance
                    agent_class = type(agent_instance)
                    cls._agents[agent_name] = (agent_class, agent_type or "generic")

                    # Get the model from the agent instance if available
                    model = getattr(agent_instance, "model", None)
                    if not model and hasattr(agent_instance, "config"):
                        # Check if config is a dictionary with get method or an object
                        if isinstance(agent_instance.config, dict):
                            model = agent_instance.config.get("model")
                        elif hasattr(agent_instance.config, "model"):
                            model = agent_instance.config.model
                    if not model:
                        model = "unknown"

                    # Get description from the agent class docstring
                    description = agent_class.__doc__ or f"{agent_class.__name__} agent"

                    # Get config from the agent instance if available
                    config = getattr(agent_instance, "config", {})

                    # Convert config to a dictionary if it's a Pydantic model
                    if hasattr(config, "model_dump"):
                        config_dict = config.model_dump()
                    elif hasattr(config, "dict"):
                        config_dict = config.dict()
                    else:
                        config_dict = config

                    # Register in database - use agent_type from directory, not class name
                    try:
                        db_id = register_agent(
                            name=agent_name,
                            agent_type=agent_type
                            or "generic",  # Use directory type, not class name
                            model=model,
                            description=description,
                            config=config_dict,
                        )
                        cls._agent_db_ids[agent_name] = db_id
                    except Exception as e:
                        logger.error(
                            f"Failed to register agent {agent_name} in database: {str(e)}"
                        )

                    logger.info(
                        f"Discovered agent: {agent_name} ({agent_class.__name__}) [Type: {agent_type or 'generic'}]"
                    )
                    return True

            return False
        except ImportError as e:
            logger.error(f"Import error loading agent from {agent_dir.name}: {str(e)}")
            logger.error(
                f"Make sure the agent class and imports are correctly defined in {module_path}"
            )
        except Exception as e:
            logger.error(f"Error loading agent from {agent_dir.name}: {str(e)}")

        return False

    @classmethod
    def get_agent(cls, agent_name: str) -> BaseAgent:
        """Get an initialized agent instance by name."""
        # Add _agent suffix if not present
        if not agent_name.endswith("_agent"):
            agent_name = f"{agent_name}_agent"

        # Special case for sofia_agent to ensure run_id is always up to date
        if agent_name == "sofia_agent" and agent_name in cls._initialized_agents:
            # Force recreation of sofia_agent to refresh run_id
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

            # First, try to get from simple type
            try:
                agent_class, agent_type = cls._agents[agent_name]
                module_path = (
                    f"src.agents.{agent_type}.{agent_name}"
                    if agent_type != "generic"
                    else f"src.agents.{agent_name}"
                )

                module = importlib.import_module(module_path)
                create_func = getattr(
                    module, f"create_{agent_name.replace('_agent', '')}_agent"
                )

                # Create the agent
                agent = create_func()

                # Store the database ID with the agent instance
                if agent_name in cls._agent_db_ids:
                    agent.db_id = cls._agent_db_ids[agent_name]
                else:
                    # Try to get the agent ID from the database
                    db_agent = get_agent_by_name(agent_name)
                    if db_agent:
                        agent.db_id = db_agent["id"]
                        cls._agent_db_ids[agent_name] = db_agent["id"]

                cls._initialized_agents[agent_name] = agent
            except ImportError as e:
                raise ValueError(
                    f"Failed to import agent module {agent_name}: {str(e)}"
                )
            except AttributeError as e:
                raise ValueError(
                    f"Failed to find create function for agent {agent_name}: {str(e)}"
                )
            except Exception as e:
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
