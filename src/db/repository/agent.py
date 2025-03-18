"""Agent repository functions for database operations."""

import uuid
import json
import logging
from typing import List, Optional, Dict, Any

from src.db.connection import execute_query
from src.db.models import Agent, Session
from src.version import SERVICE_INFO

# Configure logger
logger = logging.getLogger(__name__)


def get_agent(agent_id: int) -> Optional[Agent]:
    """Get an agent by ID.
    
    Args:
        agent_id: The agent ID
        
    Returns:
        Agent object if found, None otherwise
    """
    try:
        result = execute_query(
            "SELECT * FROM agents WHERE id = %s",
            (agent_id,)
        )
        return Agent.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting agent {agent_id}: {str(e)}")
        return None


def get_agent_by_name(name: str) -> Optional[Agent]:
    """Get an agent by name.
    
    Args:
        name: The agent name
        
    Returns:
        Agent object if found, None otherwise
    """
    try:
        result = execute_query(
            "SELECT * FROM agents WHERE name = %s",
            (name,)
        )
        return Agent.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting agent by name {name}: {str(e)}")
        return None


def list_agents(active_only: bool = True) -> List[Agent]:
    """List all agents.
    
    Args:
        active_only: Whether to only include active agents
        
    Returns:
        List of Agent objects
    """
    try:
        if active_only:
            result = execute_query(
                "SELECT * FROM agents WHERE active = TRUE ORDER BY name"
            )
        else:
            result = execute_query(
                "SELECT * FROM agents ORDER BY name"
            )
        return [Agent.from_db_row(row) for row in result]
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        return []


def create_agent(agent: Agent) -> Optional[int]:
    """Create a new agent.
    
    Args:
        agent: The agent to create
        
    Returns:
        The created agent ID if successful, None otherwise
    """
    try:
        # Check if agent with this name already exists
        existing = get_agent_by_name(agent.name)
        if existing:
            # Update existing agent
            agent.id = existing.id
            return update_agent(agent)
        
        # Prepare the agent for insertion
        if not agent.version:
            agent.version = SERVICE_INFO.get("version", "0.1.0")
        
        config_json = json.dumps(agent.config) if agent.config else None
        
        # Insert the agent
        result = execute_query(
            """
            INSERT INTO agents (
                name, type, model, description, 
                config, version, active, run_id, system_prompt,
                created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, 
                %s, %s, %s, %s, %s,
                NOW(), NOW()
            ) RETURNING id
            """,
            (
                agent.name,
                agent.type,
                agent.model,
                agent.description,
                config_json,
                agent.version,
                agent.active,
                agent.run_id,
                agent.system_prompt
            )
        )
        
        agent_id = result[0]["id"] if result else None
        logger.info(f"Created agent {agent.name} with ID {agent_id}")
        return agent_id
    except Exception as e:
        logger.error(f"Error creating agent {agent.name}: {str(e)}")
        return None


def update_agent(agent: Agent) -> Optional[int]:
    """Update an existing agent.
    
    Args:
        agent: The agent to update
        
    Returns:
        The updated agent ID if successful, None otherwise
    """
    try:
        if not agent.id:
            existing = get_agent_by_name(agent.name)
            if existing:
                agent.id = existing.id
            else:
                return create_agent(agent)
        
        config_json = json.dumps(agent.config) if agent.config else None
        
        execute_query(
            """
            UPDATE agents SET 
                name = %s,
                type = %s,
                model = %s,
                description = %s,
                config = %s,
                version = %s,
                active = %s,
                run_id = %s,
                system_prompt = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (
                agent.name,
                agent.type,
                agent.model,
                agent.description,
                config_json,
                agent.version,
                agent.active,
                agent.run_id,
                agent.system_prompt,
                agent.id
            ),
            fetch=False
        )
        
        logger.info(f"Updated agent {agent.name} with ID {agent.id}")
        return agent.id
    except Exception as e:
        logger.error(f"Error updating agent {agent.name}: {str(e)}")
        return None


def delete_agent(agent_id: int) -> bool:
    """Delete an agent.
    
    Args:
        agent_id: The agent ID to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        execute_query(
            "DELETE FROM agents WHERE id = %s",
            (agent_id,),
            fetch=False
        )
        logger.info(f"Deleted agent with ID {agent_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting agent {agent_id}: {str(e)}")
        return False


def increment_agent_run_id(agent_id: int) -> bool:
    """Increment the run_id of an agent.
    
    Args:
        agent_id: The agent ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        execute_query(
            "UPDATE agents SET run_id = run_id + 1, updated_at = NOW() WHERE id = %s",
            (agent_id,),
            fetch=False
        )
        logger.info(f"Incremented run_id for agent {agent_id}")
        return True
    except Exception as e:
        logger.error(f"Error incrementing run_id for agent {agent_id}: {str(e)}")
        return False


def link_session_to_agent(session_id: uuid.UUID, agent_id: int) -> bool:
    """Link a session to an agent in the database.
    
    Args:
        session_id: The session ID
        agent_id: The agent ID
        
    Returns:
        True on success, False on failure
    """
    try:
        # Check if agent exists
        agent = get_agent(agent_id)
        if not agent:
            logger.error(f"Cannot link session to non-existent agent {agent_id}")
            return False
        
        # Import here to avoid circular imports
        from src.db.repository.session import get_session
        
        # First, check if this session is already linked to this agent in the session table
        # This avoids unnecessary updates to messages
        session = get_session(session_id)
        
        # If session is already linked to this agent, no need to update anything
        if session and session.agent_id == agent_id:
            logger.debug(f"Session {session_id} already associated with agent {agent_id}, skipping updates")
            return True
            
        # Check if any messages in this session need updating
        message_count = execute_query(
            """
            SELECT COUNT(*) as count FROM messages 
            WHERE session_id = %s AND (agent_id IS NULL OR agent_id != %s)
            """,
            (str(session_id), agent_id)
        )
        
        needs_update = message_count and message_count[0]["count"] > 0
        
        if needs_update:
            # Only update messages that don't already have the correct agent_id
            execute_query(
                """
                UPDATE messages
                SET agent_id = %s
                WHERE session_id = %s AND (agent_id IS NULL OR agent_id != %s)
                """,
                (agent_id, str(session_id), agent_id),
                fetch=False
            )
            logger.debug(f"Updated {message_count[0]['count']} messages to associate with agent {agent_id}")
        else:
            logger.debug(f"No messages need updating for session {session_id}")
        
        # Update the sessions table with the agent_id
        execute_query(
            """
            UPDATE sessions
            SET agent_id = %s, updated_at = NOW()
            WHERE id = %s AND (agent_id IS NULL OR agent_id != %s)
            """,
            (agent_id, str(session_id), agent_id),
            fetch=False
        )
        logger.debug(f"Updated sessions table with agent_id {agent_id} for session {session_id}")
        
        logger.info(f"Session {session_id} associated with agent {agent_id} in database")
        return True
    except Exception as e:
        logger.error(f"Error linking session {session_id} to agent {agent_id}: {str(e)}")
        return False
