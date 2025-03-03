"""Agent database operations."""

import json
import logging
import uuid
from typing import Dict, List, Optional, Any, Type, Union
from datetime import datetime

from src.utils.db import execute_query
from src.version import SERVICE_INFO

# Configure logger
logger = logging.getLogger(__name__)

def register_agent(name: str, agent_type: str, model: str, description: Optional[str] = None, config: Optional[Dict] = None) -> Union[int, str]:
    """Register an agent in the database.
    
    Args:
        name: Agent name
        agent_type: Agent type class name
        model: The model used by the agent
        description: Optional description
        config: Optional configuration
        
    Returns:
        The agent ID (integer)
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
            # Instead of using LIKE on integer column, check for IDs larger than 0
            result = execute_query("SELECT MAX(id) as max_id FROM agents WHERE id > 0")
            
            if result and result[0]["max_id"] is not None:
                # Parse the existing ID to get the next one
                next_id = int(result[0]["max_id"]) + 1
                # Changed to use integer IDs directly rather than string with prefix
                agent_id = next_id
            else:
                # No existing agents with ID pattern - start at 1
                # Changed to use integer IDs directly
                agent_id = 1
            
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

def get_agent(agent_id: Union[int, str]) -> Optional[Dict[str, Any]]:
    """Get agent details by ID.
    
    Args:
        agent_id: The agent ID (integer or string for backwards compatibility)
        
    Returns:
        Agent details as a dictionary, or None if not found
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

def link_session_to_agent(session_id: str, agent_id: Union[int, str]) -> bool:
    """Link a session to an agent in the database.
    
    Args:
        session_id: The session ID
        agent_id: The agent ID (integer or string for backwards compatibility)
        
    Returns:
        True on success, False on failure
    """
    try:
        # Check if agent exists
        agent = get_agent(agent_id)
        if not agent:
            logger.error(f"Cannot link session to non-existent agent {agent_id}")
            return False
        
        # Update all messages in the session that don't have an agent_id
        execute_query(
            """
            UPDATE chat_messages
            SET agent_id = %s
            WHERE session_id = %s AND agent_id IS NULL
            """,
            (agent_id, session_id),
            fetch=False
        )
        
        # Also store the agent_id in the sessions table if it has an agent_id column
        try:
            # Check if the agent_id column exists in the sessions table
            column_exists = execute_query(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = 'sessions' AND column_name = 'agent_id'
                ) as exists
                """
            )
            
            if column_exists and column_exists[0]["exists"]:
                # Update the sessions table with the agent_id
                execute_query(
                    """
                    UPDATE sessions
                    SET agent_id = %s
                    WHERE id = %s
                    """,
                    (agent_id, session_id),
                    fetch=False
                )
                logger.debug(f"Updated sessions table with agent_id {agent_id} for session {session_id}")
        except Exception as inner_e:
            # Log but continue - this is not critical
            logger.warning(f"Could not update sessions table with agent_id: {str(inner_e)}")
        
        logger.debug(f"Session {session_id} associated with agent {agent_id} in database")
        return True
    except Exception as e:
        logger.error(f"Error linking session {session_id} to agent {agent_id}: {str(e)}")
        return False

def deactivate_agent(agent_id: Union[int, str]) -> bool:
    """Deactivate an agent.
    
    Args:
        agent_id: The agent ID (integer or string for backwards compatibility)
        
    Returns:
        True on success, False on failure
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