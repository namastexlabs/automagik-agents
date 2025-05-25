"""Repository modules for database operations.

This package contains the repository modules for each entity type in the database.
All repository functions are re-exported here for easier imports.
"""

# Agent repository functions
from src.db.repository.agent import (
    get_agent,
    get_agent_by_name,
    list_agents,
    create_agent,
    update_agent,
    delete_agent,
    increment_agent_run_id,
    link_session_to_agent,
    register_agent,
    update_agent_active_prompt_id
)

# User repository functions
from src.db.repository.user import (
    get_user,
    get_user_by_email,
    get_user_by_identifier,
    list_users,
    create_user,
    update_user,
    delete_user,
    ensure_default_user_exists
)

# Session repository functions
from src.db.repository.session import (
    get_session,
    get_session_by_name,
    list_sessions,
    create_session,
    update_session,
    delete_session,
    finish_session,
    update_session_name_if_empty
)

# Message repository functions
from src.db.repository.message import (
    get_message,
    list_messages,
    count_messages,
    create_message,
    update_message,
    delete_message,
    delete_session_messages,
    list_session_messages,
    get_system_prompt
)

# Memory repository functions
from src.db.repository.memory import (
    get_memory,
    get_memory_by_name,
    list_memories,
    create_memory,
    update_memory,
    delete_memory
)

# Prompt repository functions
from src.db.repository.prompt import (
    get_prompt_by_id,
    get_active_prompt,
    find_code_default_prompt,
    get_latest_version_for_status,
    create_prompt,
    update_prompt,
    set_prompt_active,
    get_prompts_by_agent_id,
    delete_prompt
)

# MCP repository functions
from src.db.repository.mcp import (
    get_mcp_server,
    get_mcp_server_by_name,
    list_mcp_servers,
    create_mcp_server,
    update_mcp_server,
    update_mcp_server_status,
    update_mcp_server_discovery,
    increment_connection_attempts,
    delete_mcp_server,
    assign_agent_to_server,
    remove_agent_from_server,
    get_agent_servers,
    get_server_agents,
    get_agent_server_assignments
)
