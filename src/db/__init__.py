"""Database module for Automagik Agents."""

# Export models
from src.db.models import (
    Agent,
    User,
    Session,
    Message,
    Memory,
    Conversation,
)

# Export connection functions
from src.db.connection import (
    execute_query,
    execute_batch,
    get_db_connection,
    get_db_cursor,
    close_connection_pool,
)

# Export repository functions
from src.db.repository import (
    # Agent operations
    get_agent,
    get_agent_by_name,
    list_agents,
    create_agent,
    update_agent,
    delete_agent,
    increment_agent_run_id,
    
    # User operations
    get_user,
    get_user_by_email,
    list_users,
    create_user,
    update_user,
    delete_user,
    
    # Session operations
    get_session,
    get_session_by_name,
    list_sessions,
    create_session,
    update_session,
    delete_session,
    finish_session,
    
    # Memory operations
    get_memory,
    get_memory_by_name,
    list_memories,
    create_memory,
    update_memory,
    delete_memory,
)