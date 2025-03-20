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
        """Try to load an agent from a specific directory."""

        try:
            # Identify the module path based on directory structure
            module_path = f"src.agents.{agent_dir.name}"
            if agent_type is not None and agent_type != agent_dir.name:
                module_path = f"src.agents.{agent_type}.{agent_dir.name}"

            logger.info(f"Attempting to import module: {module_path}")

            # Import the module
            module = importlib.import_module(module_path)
            
            # Look for agent classes in the module and submodules
            agent_found = False
            
            # Check if this is a module with a default_agent
            if hasattr(module, "default_agent"):
                logger.info(f"Found default_agent in module {module_path}")
                default_agent = getattr(module, "default_agent")
                
                # Check if default_agent is None
                if default_agent is None:
                    logger.error(f"Found default_agent in {module_path} but it's None - check initialization errors")
                    
                    # Check if create_* function exists - we can still register the agent type
                    create_func_name = f"create_{agent_dir.name.replace('_agent', '')}_agent"
                    if hasattr(module, create_func_name) and callable(getattr(module, create_func_name)):
                        logger.info(f"Found {create_func_name} function, registering agent type despite None default_agent")
                        # Set agent name - use directory name without adding _agent if it already has it
                        agent_name = agent_dir.name if agent_dir.name.endswith("_agent") else f"{agent_dir.name}_agent"
                        
                        # Use a generic SimpleAgent class for registration since default_agent is None
                        from src.agents.models.base_agent import BaseAgent
                        class GenericAgent(BaseAgent):
                            def __init__(self, config):
                                super().__init__(config, "Generic agent")
                            def register_tools(self):
                                pass
                        
                        cls._agents[agent_name] = (GenericAgent, agent_type or "generic")
                        logger.info(f"Registered agent type: {agent_name} using GenericAgent class")
                        return True
                    
                    return False
                
                # Get the agent class from the default agent instance
                agent_class = type(default_agent)
                
                # Set agent name - use directory name without adding _agent if it already has it
                agent_name = agent_dir.name if agent_dir.name.endswith("_agent") else f"{agent_dir.name}_agent"

                # Display more detailed debug info
                logger.info(f"Agent class: {agent_class.__name__}, Agent name: {agent_name}")

                # Get config details from module if available
                config_dict = {}
                for config_attr in ["DEFAULT_CONFIG", "CONFIG", "config"]:
                    if hasattr(module, config_attr):
                        config_dict = getattr(module, config_attr)
                        break

                # Extract metadata from module
                description = (
                    getattr(module, "DESCRIPTION", "")
                    or getattr(agent_class, "__doc__", "")
                    or f"{agent_name} agent"
                )
                model = config_dict.get("model", "")
                
                # Add to registry
                cls._agents[agent_name] = (agent_class, agent_type or "generic")
                agent_found = True

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
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")

        return False

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

            # First, try to get from simple type
            try:
                agent_class, agent_type = cls._agents[agent_name]
                
                # Special case handling for the simple agent with simple subdirectory
                if agent_type == "simple" and agent_name == "simple_agent":
                    module_path = "src.agents.simple.simple_agent"
                else:
                    # Regular module path construction
                    # For most agents, the module name is the directory name
                    agent_module_name = agent_name.replace("_agent", "")
                    module_path = (
                        f"src.agents.{agent_type}.{agent_module_name}"
                        if agent_type != "generic"
                        else f"src.agents.{agent_module_name}"
                    )

                logger.info(f"Importing agent module: {module_path}")
                module = importlib.import_module(module_path)
                
                # Get the correct creation function name
                create_func_name = f"create_{agent_name.replace('_agent', '')}_agent"
                logger.info(f"Looking for function: {create_func_name}")
                
                # Check if function exists
                if not hasattr(module, create_func_name):
                    logger.error(f"Function {create_func_name} not found in module {module_path}")
                    available_attrs = [attr for attr in dir(module) if not attr.startswith('_')]
                    logger.info(f"Available attributes in module: {available_attrs}")
                    raise AttributeError(f"Module {module_path} has no attribute '{create_func_name}'")
                    
                create_func = getattr(module, create_func_name)
                
                # Check if function is callable
                if not callable(create_func):
                    logger.error(f"Found {create_func_name} but it's not callable: {type(create_func)}")
                    raise TypeError(f"{create_func_name} is not callable")

                # Create the agent
                logger.info(f"Calling {create_func_name}()")
                agent = create_func()
                logger.info(f"Agent created successfully: {agent}")

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
                logger.error(f"Failed to import agent module {agent_name}: {str(e)}")
                raise ValueError(
                    f"Failed to import agent module {agent_name}: {str(e)}"
                )
            except AttributeError as e:
                logger.error(f"Failed to find create function for agent {agent_name}: {str(e)}")
                raise ValueError(
                    f"Failed to find create function for agent {agent_name}: {str(e)}"
                )
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
