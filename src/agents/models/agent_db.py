"""Agent database operations."""

import json
import logging
import uuid
from typing import Dict, List, Optional, Any, Type
from datetime import datetime

from src.utils.db import execute_query
from src.version import SERVICE_INFO

# Configure logger
logger = logging.getLogger(__name__)

def register_agent(name: str, agent_type: str, model: str, description: Optional[str] = None, config: Optional[Dict] = None) -> str:
    """Register an agent in the database.
    
    Args:
        name: Agent name
        agent_type: Agent type class name
        model: The model used by the agent
        description: Optional description
        config: Optional configuration
        
    Returns:
        The agent ID
    """
    try:
        # Check if agent with this name already exists
        existing = execute_query(
            "SELECT id FROM agents WHERE name = %s LIMIT 1",
            (name,)
        )
        
        if existing:
            # Return existing agent ID
            agent_id = existing[0]["id"]
            
            # Update existing agent
            execute_query(
                """
                UPDATE agents 
                SET type = %s, model = %s, description = %s, 
                    config = %s, updated_at = %s, version = %s
                WHERE id = %s
                """,
                (
                    agent_type,
                    model,
                    description,
                    json.dumps(config) if config else None,
                    datetime.utcnow(),
                    SERVICE_INFO.get("version", "0.1.0"),
                    agent_id
                ),
                fetch=False
            )
            
            logger.info(f"Updated agent {name} with ID {agent_id}")
            return agent_id
        
        # Check if a database sequence exists for agent IDs
        seq_exists = execute_query(
            "SELECT EXISTS(SELECT 1 FROM information_schema.sequences WHERE sequence_name = 'agent_seq') AS exists"
        )
        
        use_sequence = seq_exists and seq_exists[0]["exists"]
        
        if use_sequence:
            # Get the next value from the sequence
            seq_result = execute_query("SELECT nextval('agent_seq') as next_id")
            next_id = seq_result[0]["next_id"]
            agent_id = f"a_{next_id}"
            
            # Insert with the generated ID
            execute_query(
                """
                INSERT INTO agents (
                    id, name, type, model, description, 
                    config, created_at, updated_at, active, version
                ) VALUES (
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    agent_id,
                    name,
                    agent_type,
                    model,
                    description,
                    json.dumps(config) if config else None,
                    datetime.utcnow(),
                    datetime.utcnow(),
                    True,  # active
                    SERVICE_INFO.get("version", "0.1.0")
                ),
                fetch=False
            )
        else:
            # Fallback to the old method of generating sequential agent IDs
            result = execute_query("SELECT MAX(id) as max_id FROM agents WHERE id LIKE 'a_%'")
            
            if result and result[0]["max_id"]:
                # Extract number from last ID and increment
                try:
                    last_num = int(result[0]["max_id"].split('_')[1])
                    agent_id = f"a_{last_num + 1}"
                except (ValueError, IndexError):
                    # Fallback if parsing fails
                    agent_id = "a_1"
            else:
                # No existing a_X IDs, start with a_1
                agent_id = "a_1"
            
            # Insert with the generated ID
            execute_query(
                """
                INSERT INTO agents (
                    id, name, type, model, description, 
                    config, created_at, updated_at, active, version
                ) VALUES (
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    agent_id,
                    name,
                    agent_type,
                    model,
                    description,
                    json.dumps(config) if config else None,
                    datetime.utcnow(),
                    datetime.utcnow(),
                    True,  # active
                    SERVICE_INFO.get("version", "0.1.0")
                ),
                fetch=False
            )
        
        logger.info(f"Registered agent {name} with ID {agent_id}")
        return agent_id
    except Exception as e:
        logger.error(f"Error registering agent {name}: {str(e)}")
        raise

def get_agent(agent_id: str) -> Optional[Dict[str, Any]]:
    """Get agent details by ID.
    
    Args:
        agent_id: The agent ID
        
    Returns:
        The agent details as a dictionary, or None if not found
    """
    try:
        agents = execute_query(
            "SELECT * FROM agents WHERE id = %s",
            (agent_id,)
        )
        return agents[0] if agents else None
    except Exception as e:
        logger.error(f"Error getting agent {agent_id}: {str(e)}")
        return None

def get_agent_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Get agent details by name.
    
    Args:
        name: The agent name
        
    Returns:
        The agent details as a dictionary, or None if not found
    """
    try:
        agents = execute_query(
            "SELECT * FROM agents WHERE name = %s",
            (name,)
        )
        return agents[0] if agents else None
    except Exception as e:
        logger.error(f"Error getting agent by name {name}: {str(e)}")
        return None

def list_agents() -> List[Dict[str, Any]]:
    """List all agents.
    
    Returns:
        List of agent details
    """
    try:
        return execute_query("SELECT * FROM agents WHERE active = TRUE ORDER BY name")
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        return []

def link_session_to_agent(session_id: str, agent_id: str) -> bool:
    """Associate a session with an agent in memory (not in database).
    
    Args:
        session_id: The session ID
        agent_id: The agent ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Check if agent exists
        agent = get_agent(agent_id)
        if not agent:
            logger.error(f"Cannot link session to non-existent agent {agent_id}")
            return False
        
        # Log the association in memory only
        logger.debug(f"Session {session_id} associated with agent {agent_id} in memory")
        return True
    except Exception as e:
        logger.error(f"Error linking session {session_id} to agent {agent_id}: {str(e)}")
        return False

def deactivate_agent(agent_id: str) -> bool:
    """Deactivate an agent (mark as inactive).
    
    Args:
        agent_id: The agent ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        execute_query(
            """
            UPDATE agents 
            SET active = FALSE, updated_at = %s
            WHERE id = %s
            """,
            (datetime.utcnow(), agent_id),
            fetch=False
        )
        logger.info(f"Deactivated agent {agent_id}")
        return True
    except Exception as e:
        logger.error(f"Error deactivating agent {agent_id}: {str(e)}")
        return False 