"""Agent database operations."""

import json
import logging
import uuid
from typing import Dict, List, Optional, Any, Type, Union
from datetime import datetime
import traceback

from src.db import execute_query, Agent, create_agent, get_agent_by_name
from src.version import SERVICE_INFO

# Configure logger
logger = logging.getLogger(__name__)

def register_agent(name: str, agent_type: str, model: str, description: Optional[str] = None, config: Optional[Dict] = None) -> Union[int, str]:
    """Register an agent in the database.
    
    Args:
        name: The name of the agent
        agent_type: The type of agent (e.g., "simple")
        model: The model used by the agent (e.g., "gpt-4")
        description: Optional description of the agent
        config: Optional configuration for the agent
        
    Returns:
        The agent ID (integer)
    """
    try:
        # Use repository functions instead of direct SQL queries
        from src.db import Agent, create_agent, get_agent_by_name
        
        # Create agent object
        agent = Agent(
            name=name,
            type=agent_type,
            model=model,
            description=description,
            config=config,
            active=True
        )
        
        # Use repository function to create or update the agent
        agent_id = create_agent(agent)
        
        if agent_id:
            logger.info(f"Registered agent {name} with ID {agent_id}")
            return agent_id
        else:
            logger.error(f"Failed to register agent {name}")
            return None
            
    except Exception as e:
        logger.error(f"Error registering agent {name}: {str(e)}")
        traceback.print_exc()
        return None

def get_agent(agent_id: Union[int, str]) -> Optional[Dict[str, Any]]:
    """Get an agent by ID.
    
    Args:
        agent_id: The agent ID to retrieve
        
    Returns:
        The agent as a dictionary, or None if not found
    """
    try:
        # Convert string IDs to integers if needed
        if isinstance(agent_id, str) and agent_id.isdigit():
            agent_id = int(agent_id)
            
        # Use repository function to get agent
        from src.db import get_agent
        agent = get_agent(agent_id)
        
        if agent:
            # Convert model to dictionary
            return agent.model_dump()
        return None
    except Exception as e:
        logger.error(f"Error getting agent {agent_id}: {str(e)}")
        return None

def get_agent_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Get an agent by name.
    
    Args:
        name: The agent name to retrieve
        
    Returns:
        The agent as a dictionary, or None if not found
    """
    try:
        # Use repository function to get agent by name
        from src.db import get_agent_by_name
        agent = get_agent_by_name(name)
        
        if agent:
            # Convert model to dictionary
            return agent.model_dump()
        return None
    except Exception as e:
        logger.error(f"Error getting agent by name {name}: {str(e)}")
        return None

def list_agents() -> List[Dict[str, Any]]:
    """List all active agents.
    
    Returns:
        List of agents as dictionaries
    """
    try:
        # Use repository function to list active agents
        from src.db import list_agents
        agents = list_agents(active_only=True)
        
        # Convert models to dictionaries
        return [agent.model_dump() for agent in agents]
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        return []

def link_session_to_agent(session_id: str, agent_id: Union[int, str]) -> bool:
    """Link a session to an agent in the database.
    
    Args:
        session_id: The session ID (UUID)
        agent_id: The agent ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert string IDs to integers if needed
        if isinstance(agent_id, str) and agent_id.isdigit():
            agent_id = int(agent_id)
            
        # Convert session_id to UUID
        session_id_uuid = uuid.UUID(session_id)
        
        # Use repository function to link session to agent
        from src.db import link_session_to_agent
        success = link_session_to_agent(session_id_uuid, agent_id)
        
        if success:
            logger.info(f"Successfully linked session {session_id} to agent {agent_id}")
        else:
            logger.warning(f"Failed to link session {session_id} to agent {agent_id}")
            
        return success
    except ValueError as e:
        if "already associated with agent ID" in str(e):
            # This is actually an expected case that's handled in higher level code
            # Just re-raise to let the higher level handle it
            raise
        logger.error(f"Invalid session ID format: {session_id}")
        return False
    except Exception as e:
        logger.error(f"Error linking session {session_id} to agent {agent_id}: {str(e)}")
        return False

def deactivate_agent(agent_id: Union[int, str]) -> bool:
    """Deactivate an agent.
    
    Args:
        agent_id: The agent ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert string IDs to integers if needed
        if isinstance(agent_id, str) and agent_id.isdigit():
            agent_id = int(agent_id)
            
        # Get the agent first
        from src.db import get_agent, update_agent
        agent = get_agent(agent_id)
        
        if not agent:
            logger.error(f"Agent {agent_id} not found")
            return False
            
        # Update agent to set active=False
        agent.active = False
        updated_id = update_agent(agent)
        
        if updated_id:
            logger.info(f"Deactivated agent {agent_id}")
            return True
        else:
            logger.error(f"Failed to deactivate agent {agent_id}")
            return False
    except Exception as e:
        logger.error(f"Error deactivating agent {agent_id}: {str(e)}")
        return False 