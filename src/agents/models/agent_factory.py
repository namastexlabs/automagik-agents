import importlib
import logging
from pathlib import Path
from typing import Dict, Type, List

from src.agents.models.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class AgentFactory:
    """Factory class for creating and managing agents."""
    
    _agents: Dict[str, Type[BaseAgent]] = {}
    _initialized_agents: Dict[str, BaseAgent] = {}
    
    @classmethod
    def discover_agents(cls) -> None:
        """Discover all available agents in the agents directory."""
        agents_dir = Path(__file__).parent.parent
        
        # Clear existing agents
        cls._agents.clear()
        cls._initialized_agents.clear()
        
        # Look for agent directories (excluding models, __pycache__, etc)
        for item in agents_dir.iterdir():
            if not item.is_dir() or item.name in ['models', '__pycache__']:
                continue
                
            try:
                # Try to import the agent module
                module_path = f"src.agents.{item.name}"
                module = importlib.import_module(module_path)
                
                # Check for default_agent in the module
                if hasattr(module, 'default_agent'):
                    # Use the full folder name as the agent name
                    agent_name = item.name
                    agent_instance = getattr(module, 'default_agent')
                    
                    if agent_instance is not None:  # Some agents might be conditionally initialized
                        cls._initialized_agents[agent_name] = agent_instance
                        cls._agents[agent_name] = type(agent_instance)
                        logger.info(f"Discovered agent: {agent_name} ({type(agent_instance).__name__})")
            
            except ImportError as e:
                logger.error(f"Import error loading agent from {item.name}: {str(e)}")
                logger.error(f"Make sure the agent class and imports are correctly defined in {module_path}")
            except Exception as e:
                logger.error(f"Error loading agent from {item.name}: {str(e)}")
    
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
            
            # Try to get the agent's module
            try:
                module = importlib.import_module(f"src.agents.{agent_name}")
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