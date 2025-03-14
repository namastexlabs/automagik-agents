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

        # Clear existing agents
        cls._agents.clear()
        cls._initialized_agents.clear()
        cls._agent_db_ids.clear()

        # Track directories containing agents
        type_dirs = []
        for item in agents_dir.iterdir():
            if item.is_dir() and item.name not in ["models", "__pycache__"]:
                if (item / "__init__.py").exists():
                    cls._try_load_agent_from_dir(item)
                else:
                    type_dirs.append(item)

        for type_dir in type_dirs:
            agent_type = type_dir.name
            for agent_dir in type_dir.iterdir():
                if agent_dir.is_dir() and agent_dir.name not in ["__pycache__"]:
                    cls._try_load_agent_from_dir(agent_dir, agent_type)

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
            # Generate relative module path
            rel_path = agent_dir.relative_to(Path(__file__).parent.parent.parent)
            module_path = f"src.{rel_path.as_posix().replace('/', '.')}"

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
            agent_name: The name of the agent.
            session_id_or_name: The session ID or name to link.

        Returns:
            True on success, False on failure.
        """
        # Try to determine if session_id_or_name is a session name or ID
        try:
            # First try to validate as UUID
            uuid_obj = uuid.UUID(session_id_or_name)
            session_id = session_id_or_name
        except ValueError:
            # Not a UUID, could be a session name
            try:
                # Import inside the method to avoid circular imports
                from src.memory.pg_message_store import PostgresMessageStore

                store = PostgresMessageStore()
                resolved_id = store.get_session_by_name(session_id_or_name)

                if not resolved_id:
                    logger.warning(f"No session found with name '{session_id_or_name}'")
                    return False

                session_id = resolved_id
                logger.info(
                    f"Resolved session name '{session_id_or_name}' to ID {session_id}"
                )
            except Exception as e:
                logger.error(
                    f"Error resolving session name '{session_id_or_name}': {str(e)}"
                )
                return False

        # Now that we have a valid session ID, proceed with linking
        try:
            # Get the database ID for the agent name
            agent = None
            for name, (a_class, _) in cls._agents.items():
                if name == agent_name or f"{name}_agent" == agent_name:
                    a_instance = cls.get_agent(name)
                    agent_id = getattr(a_instance, "db_id", None)
                    if agent_id:
                        from src.agents.models.agent_db import link_session_to_agent

                        return link_session_to_agent(session_id, agent_id)

            # Try direct lookup by name in case the agent was registered directly in the database
            from src.agents.models.agent_db import (
                get_agent_by_name,
                link_session_to_agent,
            )

            agent_rec = get_agent_by_name(agent_name)
            if agent_rec and "id" in agent_rec:
                return link_session_to_agent(session_id, agent_rec["id"])

            agent_rec = get_agent_by_name(
                f"{agent_name}_agent"
                if not agent_name.endswith("_agent")
                else agent_name
            )
            if agent_rec and "id" in agent_rec:
                return link_session_to_agent(session_id, agent_rec["id"])

            logger.warning(f"Could not find agent ID for agent {agent_name}")
            return False
        except Exception as e:
            logger.error(
                f"Error linking agent {agent_name} to session {session_id_or_name}: {e}"
            )
            return False
