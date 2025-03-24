from typing import Dict, Optional, Type, Union, List
import logging
import os
import traceback
import uuid

from src.agents.models.automagik_agent import AutomagikAgent
from src.agents.models.dependencies import BaseDependencies
from src.agents.simple.simple_agent import create_agent as create_simple_agent
from src.agents.models.placeholder import PlaceholderAgent

logger = logging.getLogger(__name__)

class AgentFactory:
    """A factory for creating agent instances."""

    _agent_classes = {}
    _agent_creators = {
        "simple": create_simple_agent,
    }
    _initialized_agents = {}  # Store initialized agents for re-use
    
    @classmethod
    def register_agent_class(cls, name: str, agent_class: Type[AutomagikAgent]) -> None:
        """Register an agent class with the factory.
        
        Args:
            name: The name of the agent class
            agent_class: The agent class to register
        """
        cls._agent_classes[name] = agent_class
        logger.info(f"Registered agent class {name}")
        
    @classmethod
    def register_agent_creator(cls, name: str, creator_fn) -> None:
        """Register an agent creator function with the factory.
        
        Args:
            name: The name of the agent type
            creator_fn: The function to create an agent
        """
        cls._agent_creators[name] = creator_fn
        logger.info(f"Registered agent creator {name}")
    
    @classmethod
    def create_agent(cls, agent_type: str, config: Optional[Dict[str, str]] = None) -> AutomagikAgent:
        """Create an agent of the specified type.
        
        Args:
            agent_type: The type of agent to create
            config: Optional configuration override
            
        Returns:
            An initialized agent instance
            
        Raises:
            ValueError: If the agent type is unknown
        """
        if config is None:
            config = {}
            
        logger.info(f"Creating agent of type {agent_type}")
        
        # Default to simple agent
        if not agent_type:
            agent_type = "simple"
        
        # Try to create using a registered creator function
        if agent_type in cls._agent_creators:
            try:
                agent = cls._agent_creators[agent_type](config)
                logger.info(f"Successfully created {agent_type} agent using creator function")
                return agent
            except Exception as e:
                logger.error(f"Error creating {agent_type} agent: {str(e)}")
                logger.error(traceback.format_exc())
                return PlaceholderAgent({"name": f"{agent_type}_error", "error": str(e)})
        
        # Try to create using a registered class
        if agent_type in cls._agent_classes:
            try:
                agent = cls._agent_classes[agent_type](config)
                logger.info(f"Successfully created {agent_type} agent using agent class")
                return agent
            except Exception as e:
                logger.error(f"Error creating {agent_type} agent: {str(e)}")
                logger.error(traceback.format_exc())
                return PlaceholderAgent({"name": f"{agent_type}_error", "error": str(e)})
                
        # Unknown agent type
        logger.error(f"Unknown agent type: {agent_type}")
        return PlaceholderAgent({"name": "unknown_agent_type", "error": f"Unknown agent type: {agent_type}"})
        
    @classmethod
    def discover_agents(cls) -> None:
        """Discover available agents (simplified compatibility version).
        
        This method is provided for backward compatibility with existing code.
        In the new implementation, agents are registered directly via
        register_agent_class and register_agent_creator methods.
        """
        logger.info("Simplified agent discovery - using registered creators and classes")
        
        # Nothing to do in this simplified version, since agents are registered directly
        # Just log the already registered agents
        creators = list(cls._agent_creators.keys())
        classes = list(cls._agent_classes.keys())
        
        logger.info(f"Already registered creator functions: {', '.join(creators) if creators else 'None'}")
        logger.info(f"Already registered agent classes: {', '.join(classes) if classes else 'None'}")
    
    @classmethod
    def list_available_agents(cls) -> List[str]:
        """List all available agent names.
        
        Returns:
            List of available agent names
        """
        # Combine creators and classes
        agents = list(cls._agent_creators.keys()) + list(cls._agent_classes.keys())
        
        # Ensure each agent is listed only once
        return list(set(agents))
        
    @classmethod
    def get_agent(cls, agent_name: str) -> AutomagikAgent:
        """Get an agent instance by name.
        
        Args:
            agent_name: Name of the agent to get
            
        Returns:
            Agent instance
            
        Raises:
            ValueError: If the agent is not found
        """
        # Compatibility method for getting agents by name
        if not agent_name.endswith("_agent"):
            agent_name = f"{agent_name}_agent"
            
        # Check if we already have an initialized instance
        if agent_name in cls._initialized_agents:
            return cls._initialized_agents[agent_name]
            
        # First check creator functions
        if agent_name.replace("_agent", "") in cls._agent_creators:
            base_name = agent_name.replace("_agent", "")
            config = {}
            agent = cls._agent_creators[base_name](config)
            cls._initialized_agents[agent_name] = agent
            return agent
            
        # Then check classes
        if agent_name in cls._agent_classes:
            config = {}
            agent = cls._agent_classes[agent_name](config)
            cls._initialized_agents[agent_name] = agent
            return agent
            
        # Finally, default to simple agent if nothing found
        logger.warning(f"Agent {agent_name} not found, defaulting to simple agent")
        agent = create_simple_agent({})
        cls._initialized_agents[agent_name] = agent
        return agent
    
    @classmethod
    def link_agent_to_session(cls, agent_name: str, session_id_or_name: str) -> bool:
        """Link an agent to a session in the database.
        
        Args:
            agent_name: The name of the agent to link
            session_id_or_name: Either a session ID or name
            
        Returns:
            True if the link was successful, False otherwise
        """
        try:
            # Make sure the session_id is a UUID string
            session_id = session_id_or_name
            try:
                # Try to parse as UUID
                uuid.UUID(session_id_or_name)
            except ValueError:
                # Not a UUID, try to look up by name
                logger.info(f"Session ID is not a UUID, treating as session name: {session_id_or_name}")
                
                # Use the appropriate database function to get session by name
                try:
                    from src.db import get_session_by_name
                    
                    session = get_session_by_name(session_id_or_name)
                    if not session:
                        logger.error(f"Session with name '{session_id_or_name}' not found")
                        return False
                        
                    session_id = str(session.id)
                    logger.info(f"Found session ID {session_id} for name {session_id_or_name}")
                except Exception as e:
                    logger.error(f"Error looking up session by name: {str(e)}")
                    return False

            # Get the agent (creating it if necessary)
            agent = cls.get_agent(agent_name)
            agent_id = getattr(agent, "db_id", None)
            
            if not agent_id:
                # Try to register the agent in the database
                try:
                    from src.db import register_agent
                    
                    # Extract agent metadata
                    agent_type = agent_name.replace("_agent", "")
                    description = getattr(agent, "description", f"{agent_name} agent")
                    model = getattr(getattr(agent, "config", {}), "model", "")
                    config = getattr(agent, "config", {})
                    
                    # If config is not a dict, convert it
                    if not isinstance(config, dict):
                        if hasattr(config, "__dict__"):
                            config = config.__dict__
                        else:
                            config = {"config": str(config)}
                    
                    # Register the agent
                    agent_id = register_agent(
                        name=agent_name,
                        agent_type=agent_type,
                        model=model,
                        description=description,
                        config=config
                    )
                    
                    # Update the agent's db_id
                    agent.db_id = agent_id
                    logger.info(f"Registered agent {agent_name} with ID {agent_id}")
                    
                except Exception as e:
                    logger.error(f"Error registering agent in database: {str(e)}")
                    logger.error(traceback.format_exc())
                    return False
            
            # Link the session to the agent
            if agent_id:
                try:
                    from src.db import link_session_to_agent
                    return link_session_to_agent(uuid.UUID(session_id), agent_id)
                except Exception as e:
                    logger.error(f"Error linking agent to session: {str(e)}")
                    logger.error(traceback.format_exc())
                    return False
            else:
                logger.error(f"Could not find or create agent ID for agent {agent_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error linking agent {agent_name} to session {session_id_or_name}: {str(e)}")
            logger.error(traceback.format_exc())
            return False
