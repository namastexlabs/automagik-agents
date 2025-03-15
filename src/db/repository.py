"""Repository functions for database operations."""

import uuid
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Union, Tuple

from src.db.connection import execute_query, execute_batch
from src.db.models import Agent, User, Session, Message, Memory, Conversation
from src.version import SERVICE_INFO

# Configure logger
logger = logging.getLogger(__name__)

#
# Agent Repository Functions
#

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


#
# User Repository Functions
#

def get_user(user_id: int) -> Optional[User]:
    """Get a user by ID.
    
    Args:
        user_id: The user ID
        
    Returns:
        User object if found, None otherwise
    """
    try:
        result = execute_query(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )
        return User.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {str(e)}")
        return None


def get_user_by_email(email: str) -> Optional[User]:
    """Get a user by email.
    
    Args:
        email: The user email
        
    Returns:
        User object if found, None otherwise
    """
    try:
        result = execute_query(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        return User.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting user by email {email}: {str(e)}")
        return None


def list_users() -> List[User]:
    """List all users.
    
    Returns:
        List of User objects
    """
    try:
        result = execute_query("SELECT * FROM users ORDER BY id")
        return [User.from_db_row(row) for row in result]
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        return []


def create_user(user: User) -> Optional[int]:
    """Create a new user.
    
    Args:
        user: The user to create
        
    Returns:
        The created user ID if successful, None otherwise
    """
    try:
        # Check if user with this email already exists
        if user.email:
            existing = get_user_by_email(user.email)
            if existing:
                # Update existing user
                user.id = existing.id
                return update_user(user)
        
        # Prepare user data
        user_data_json = json.dumps(user.user_data) if user.user_data else None
        
        # Insert the user
        result = execute_query(
            """
            INSERT INTO users (
                email, phone_number, user_data, created_at, updated_at
            ) VALUES (
                %s, %s, %s, NOW(), NOW()
            ) RETURNING id
            """,
            (
                user.email,
                user.phone_number,
                user_data_json
            )
        )
        
        user_id = result[0]["id"] if result else None
        logger.info(f"Created user with ID {user_id}")
        return user_id
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return None


def update_user(user: User) -> Optional[int]:
    """Update an existing user.
    
    Args:
        user: The user to update
        
    Returns:
        The updated user ID if successful, None otherwise
    """
    try:
        if not user.id:
            if user.email:
                existing = get_user_by_email(user.email)
                if existing:
                    user.id = existing.id
                else:
                    return create_user(user)
            else:
                return create_user(user)
        
        user_data_json = json.dumps(user.user_data) if user.user_data else None
        
        execute_query(
            """
            UPDATE users SET 
                email = %s,
                phone_number = %s,
                user_data = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (
                user.email,
                user.phone_number,
                user_data_json,
                user.id
            ),
            fetch=False
        )
        
        logger.info(f"Updated user with ID {user.id}")
        return user.id
    except Exception as e:
        logger.error(f"Error updating user {user.id}: {str(e)}")
        return None


def delete_user(user_id: int) -> bool:
    """Delete a user.
    
    Args:
        user_id: The user ID to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        execute_query(
            "DELETE FROM users WHERE id = %s",
            (user_id,),
            fetch=False
        )
        logger.info(f"Deleted user with ID {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        return False


#
# Session Repository Functions
#

def get_session(session_id: uuid.UUID) -> Optional[Session]:
    """Get a session by ID.
    
    Args:
        session_id: The session ID
        
    Returns:
        Session object if found, None otherwise
    """
    try:
        result = execute_query(
            "SELECT * FROM sessions WHERE id = %s",
            (str(session_id),)
        )
        return Session.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting session {session_id}: {str(e)}")
        return None


def get_session_by_name(name: str) -> Optional[Session]:
    """Get a session by name.
    
    Args:
        name: The session name
        
    Returns:
        Session object if found, None otherwise
    """
    try:
        result = execute_query(
            "SELECT * FROM sessions WHERE name = %s",
            (name,)
        )
        return Session.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting session by name {name}: {str(e)}")
        return None


def list_sessions(user_id: Optional[int] = None, agent_id: Optional[int] = None) -> List[Session]:
    """List sessions with optional filtering.
    
    Args:
        user_id: Filter by user ID
        agent_id: Filter by agent ID
        
    Returns:
        List of Session objects
    """
    try:
        query = "SELECT * FROM sessions"
        params = []
        conditions = []
        
        if user_id is not None:
            conditions.append("user_id = %s")
            params.append(user_id)
        
        if agent_id is not None:
            conditions.append("agent_id = %s")
            params.append(agent_id)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY updated_at DESC"
        
        result = execute_query(query, tuple(params) if params else None)
        return [Session.from_db_row(row) for row in result]
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        return []


def create_session(session: Session) -> Optional[uuid.UUID]:
    """Create a new session.
    
    Args:
        session: The session to create
        
    Returns:
        The created session ID if successful, None otherwise
    """
    try:
        # Check if a session with this name already exists
        if session.name:
            existing = get_session_by_name(session.name)
            if existing:
                # Update existing session
                session.id = existing.id
                return update_session(session)
        
        # Prepare session data
        metadata_json = json.dumps(session.metadata) if session.metadata else None
        
        # Use provided ID or let the database generate one
        session_id_param = str(session.id) if session.id else None
        
        # Insert the session
        result = execute_query(
            """
            INSERT INTO sessions (
                id, user_id, agent_id, name, platform,
                metadata, created_at, updated_at, run_finished_at
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, NOW(), NOW(), %s
            ) RETURNING id
            """,
            (
                session_id_param,
                session.user_id,
                session.agent_id,
                session.name,
                session.platform,
                metadata_json,
                session.run_finished_at
            )
        )
        
        session_id = uuid.UUID(result[0]["id"]) if result else None
        logger.info(f"Created session with ID {session_id}")
        return session_id
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        return None


def update_session(session: Session) -> Optional[uuid.UUID]:
    """Update an existing session.
    
    Args:
        session: The session to update
        
    Returns:
        The updated session ID if successful, None otherwise
    """
    try:
        if not session.id:
            if session.name:
                existing = get_session_by_name(session.name)
                if existing:
                    session.id = existing.id
                else:
                    return create_session(session)
            else:
                return create_session(session)
        
        metadata_json = json.dumps(session.metadata) if session.metadata else None
        
        execute_query(
            """
            UPDATE sessions SET 
                user_id = %s,
                agent_id = %s,
                name = %s,
                platform = %s,
                metadata = %s,
                updated_at = NOW(),
                run_finished_at = %s
            WHERE id = %s
            """,
            (
                session.user_id,
                session.agent_id,
                session.name,
                session.platform,
                metadata_json,
                session.run_finished_at,
                str(session.id)
            ),
            fetch=False
        )
        
        logger.info(f"Updated session with ID {session.id}")
        return session.id
    except Exception as e:
        logger.error(f"Error updating session {session.id}: {str(e)}")
        return None


def delete_session(session_id: uuid.UUID) -> bool:
    """Delete a session.
    
    Args:
        session_id: The session ID to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        execute_query(
            "DELETE FROM sessions WHERE id = %s",
            (str(session_id),),
            fetch=False
        )
        logger.info(f"Deleted session with ID {session_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {str(e)}")
        return False


def finish_session(session_id: uuid.UUID) -> bool:
    """Mark a session as finished.
    
    Args:
        session_id: The session ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        execute_query(
            "UPDATE sessions SET run_finished_at = NOW(), updated_at = NOW() WHERE id = %s",
            (str(session_id),),
            fetch=False
        )
        logger.info(f"Marked session {session_id} as finished")
        return True
    except Exception as e:
        logger.error(f"Error finishing session {session_id}: {str(e)}")
        return False


#
# Memory Repository Functions
#

def get_memory(memory_id: uuid.UUID) -> Optional[Memory]:
    """Get a memory by ID.
    
    Args:
        memory_id: The memory ID
        
    Returns:
        Memory object if found, None otherwise
    """
    try:
        result = execute_query(
            """
            SELECT id, name, description, content, session_id, user_id, agent_id,
                   read_mode, access, metadata, created_at, updated_at
            FROM memories 
            WHERE id = %s
            """,
            (str(memory_id),)
        )
        return Memory.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting memory {memory_id}: {str(e)}")
        return None


def get_memory_by_name(name: str, agent_id: Optional[int] = None, 
                      user_id: Optional[int] = None, 
                      session_id: Optional[uuid.UUID] = None) -> Optional[Memory]:
    """Get a memory by name with optional filters for agent, user, and session.
    
    Args:
        name: The memory name
        agent_id: Optional agent ID filter
        user_id: Optional user ID filter
        session_id: Optional session ID filter
        
    Returns:
        Memory object if found, None otherwise
    """
    try:
        query = """
            SELECT id, name, description, content, session_id, user_id, agent_id,
                   read_mode, access, metadata, created_at, updated_at
            FROM memories 
            WHERE name = %s
        """
        params = [name]
        
        # Add optional filters
        if agent_id is not None:
            query += " AND agent_id = %s"
            params.append(agent_id)
        if user_id is not None:
            query += " AND user_id = %s"
            params.append(user_id)
        if session_id is not None:
            query += " AND session_id = %s"
            params.append(str(session_id))
            
        query += " LIMIT 1"
        
        result = execute_query(query, params)
        return Memory.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting memory by name {name}: {str(e)}")
        return None


def list_memories(agent_id: Optional[int] = None, 
                 user_id: Optional[int] = None, 
                 session_id: Optional[uuid.UUID] = None,
                 read_mode: Optional[str] = None,
                 name_pattern: Optional[str] = None) -> List[Memory]:
    """List memories with optional filters.
    
    Args:
        agent_id: Optional agent ID filter
        user_id: Optional user ID filter
        session_id: Optional session ID filter
        read_mode: Optional read mode filter
        name_pattern: Optional name pattern to match (using ILIKE)
        
    Returns:
        List of Memory objects
    """
    try:
        query = """
            SELECT id, name, description, content, session_id, user_id, agent_id,
                   read_mode, access, metadata, created_at, updated_at
            FROM memories 
            WHERE 1=1
        """
        params = []
        
        # Add optional filters
        if agent_id is not None:
            query += " AND agent_id = %s"
            params.append(agent_id)
        if user_id is not None:
            query += " AND user_id = %s"
            params.append(user_id)
        if session_id is not None:
            query += " AND session_id = %s"
            params.append(str(session_id))
        if read_mode is not None:
            query += " AND read_mode = %s"
            params.append(read_mode)
        if name_pattern is not None:
            query += " AND name ILIKE %s"
            params.append(f"%{name_pattern}%")
            
        query += " ORDER BY name ASC"
        
        result = execute_query(query, params)
        return [Memory.from_db_row(row) for row in result] if result else []
    except Exception as e:
        logger.error(f"Error listing memories: {str(e)}")
        return []


def create_memory(memory: Memory) -> Optional[uuid.UUID]:
    """Create a new memory or update an existing one.
    
    Args:
        memory: The memory to create
        
    Returns:
        The memory ID if successful, None otherwise
    """
    try:
        # Check if a memory with this name already exists for the same context
        if memory.name:
            query = "SELECT id FROM memories WHERE name = %s"
            params = [memory.name]
            
            # Add optional filters
            if memory.agent_id is not None:
                query += " AND agent_id = %s"
                params.append(memory.agent_id)
            if memory.user_id is not None:
                query += " AND user_id = %s"
                params.append(memory.user_id)
            if memory.session_id is not None:
                query += " AND session_id = %s"
                params.append(str(memory.session_id))
                
            result = execute_query(query, params)
            
            if result:
                # Update existing memory
                memory.id = result[0]["id"]
                return update_memory(memory)
        
        # Generate a UUID for the memory if not provided
        if not memory.id:
            memory.id = uuid.uuid4()
        
        # Prepare memory data
        metadata_json = json.dumps(memory.metadata) if memory.metadata else None
        
        # Insert the memory
        result = execute_query(
            """
            INSERT INTO memories (
                id, name, description, content, session_id, user_id, agent_id,
                read_mode, access, metadata, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, NOW(), NOW()
            ) RETURNING id
            """,
            (
                str(memory.id),
                memory.name,
                memory.description,
                memory.content,
                str(memory.session_id) if memory.session_id else None,
                memory.user_id,
                memory.agent_id,
                memory.read_mode,
                memory.access,
                metadata_json
            )
        )
        
        memory_id = uuid.UUID(result[0]["id"]) if result else None
        logger.info(f"Created memory {memory.name} with ID {memory_id}")
        return memory_id
    except Exception as e:
        logger.error(f"Error creating memory {memory.name}: {str(e)}")
        return None


def update_memory(memory: Memory) -> Optional[uuid.UUID]:
    """Update an existing memory.
    
    Args:
        memory: The memory to update
        
    Returns:
        The updated memory ID if successful, None otherwise
    """
    try:
        if not memory.id:
            # Try to find by name and context
            query = "SELECT id FROM memories WHERE name = %s"
            params = [memory.name]
            
            # Add optional filters
            if memory.agent_id is not None:
                query += " AND agent_id = %s"
                params.append(memory.agent_id)
            if memory.user_id is not None:
                query += " AND user_id = %s"
                params.append(memory.user_id)
            if memory.session_id is not None:
                query += " AND session_id = %s"
                params.append(str(memory.session_id))
                
            result = execute_query(query, params)
            
            if result:
                memory.id = result[0]["id"]
            else:
                return create_memory(memory)
        
        # Prepare memory data
        metadata_json = json.dumps(memory.metadata) if memory.metadata else None
        
        execute_query(
            """
            UPDATE memories SET 
                name = %s,
                description = %s,
                content = %s,
                session_id = %s,
                user_id = %s,
                agent_id = %s,
                read_mode = %s,
                access = %s,
                metadata = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (
                memory.name,
                memory.description,
                memory.content,
                str(memory.session_id) if memory.session_id else None,
                memory.user_id,
                memory.agent_id,
                memory.read_mode,
                memory.access,
                metadata_json,
                str(memory.id)
            ),
            fetch=False
        )
        
        logger.info(f"Updated memory {memory.name} with ID {memory.id}")
        return memory.id
    except Exception as e:
        logger.error(f"Error updating memory {memory.id}: {str(e)}")
        return None


def delete_memory(memory_id: uuid.UUID) -> bool:
    """Delete a memory.
    
    Args:
        memory_id: The memory ID to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        execute_query(
            "DELETE FROM memories WHERE id = %s",
            (str(memory_id),),
            fetch=False
        )
        logger.info(f"Deleted memory with ID {memory_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting memory {memory_id}: {str(e)}")
        return False