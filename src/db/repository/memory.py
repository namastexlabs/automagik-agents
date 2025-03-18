"""Memory repository functions for database operations."""

import uuid
import json
import logging
from typing import List, Optional, Dict, Any

from src.db.connection import execute_query
from src.db.models import Memory

# Configure logger
logger = logging.getLogger(__name__)


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
