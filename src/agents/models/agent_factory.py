import importlib
import logging
from pathlib import Path
from typing import Dict, Type, List, Tuple

from src.agents.models.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class AgentFactory:
    """Factory class for creating and managing agents."""
    
    _agents: Dict[str, Tuple[Type[BaseAgent], str]] = {}  # Maps agent_name -> (agent_class, agent_type)
    _initialized_agents: Dict[str, BaseAgent] = {}
    
    @classmethod
    def discover_agents(cls) -> None:
        """Discover all available agents in the agents directory."""
        agents_dir = Path(__file__).parent.parent
        
        # Clear existing agents
        cls._agents.clear()
        cls._initialized_agents.clear()
        
        # First, check if we have the new type-based structure
        type_dirs = []
        for item in agents_dir.iterdir():
            if item.is_dir() and item.name not in ['models', '__pycache__']:
                # If it has an __init__.py, it might be a direct agent
                if (item / "__init__.py").exists() and cls._try_load_agent_from_dir(item):
                    continue
                # Otherwise, it might be a type directory
                type_dirs.append(item)
        
        # Now look for agents within each type directory
        for type_dir in type_dirs:
            agent_type = type_dir.name
            for agent_dir in type_dir.iterdir():
                if not agent_dir.is_dir() or agent_dir.name in ['__pycache__']:
                    continue
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
            if hasattr(module, 'default_agent'):
                # Use the folder name as the agent name
                agent_name = agent_dir.name
                agent_instance = getattr(module, 'default_agent')
                
                if agent_instance is not None:  # Some agents might be conditionally initialized
                    cls._initialized_agents[agent_name] = agent_instance
                    cls._agents[agent_name] = (type(agent_instance), agent_type or "generic")
                    logger.info(f"Discovered agent: {agent_name} ({type(agent_instance).__name__}) [Type: {agent_type or 'generic'}]")
                    return True
            
            return False
        except ImportError as e:
            logger.error(f"Import error loading agent from {agent_dir.name}: {str(e)}")
            logger.error(f"Make sure the agent class and imports are correctly defined in {module_path}")
        except Exception as e:
            logger.error(f"Error loading agent from {agent_dir.name}: {str(e)}")
        
        return False

    @classmethod
    def get_agent(cls, agent_name: str) -> BaseAgent:
        """Get an initialized agent instance by name."""
        # Add _agent suffix if not present
        if not agent_name.endswith('_agent'):
            agent_name = f"{agent_name}_agent"
            
        if agent_name not in cls._initialized_agents:
            if agent_name not in cls._agents:
                cls.discover_agents()
                if agent_name not in cls._agents:
                    available_agents = cls.list_available_agents()
                    raise ValueError(f"Agent {agent_name} not found. Available agents: {', '.join(available_agents)}")
            
            # First, try to get from simple type
            try:
                agent_class, agent_type = cls._agents[agent_name]
                module_path = f"src.agents.{agent_type}.{agent_name}" if agent_type != "generic" else f"src.agents.{agent_name}"
                
                module = importlib.import_module(module_path)
                create_func = getattr(module, f"create_{agent_name.replace('_agent', '')}_agent")
                cls._initialized_agents[agent_name] = create_func()
            except ImportError as e:
                raise ValueError(f"Failed to import agent module {agent_name}: {str(e)}")
            except AttributeError as e:
                raise ValueError(f"Failed to find create function for agent {agent_name}: {str(e)}")
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
        if not agent_name.endswith('_agent'):
            agent_name = f"{agent_name}_agent"
            
        if agent_name not in cls._agents:
            cls.discover_agents()
            if agent_name not in cls._agents:
                available_agents = cls.list_available_agents()
                raise ValueError(f"Agent {agent_name} not found. Available agents: {', '.join(available_agents)}")
        
        return cls._agents[agent_name][1] 