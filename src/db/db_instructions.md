# Database Layer Documentation


# Database Module

This directory contains the database access layer for Automagik Agents, implementing a clean repository pattern.

## Structure

- `__init__.py`: Exports all models and functions for easier imports
- `connection.py`: Database connection management and query execution
- `models.py`: Pydantic models representing database tables
- `repository.py`: CRUD operations for all database entities
- `db_instructions.md`: Detailed documentation and examples

## Quick Start

```python
from src.db import (
    # Models
    Agent, User, Session, Memory,
    
    # Repository functions
    create_agent, get_user, list_sessions,
    
    # Connection utilities
    execute_query
)

# Create a new agent
agent = Agent(
    name="my_agent",
    type="simple",
    model="gpt-4",
    description="A simple test agent"
)

# Save agent to database
agent_id = create_agent(agent)
```

## Design Principles

1. **Clean Architecture**: Separation of concerns between models, repositories, and connection management
2. **Type Safety**: Pydantic models ensure type-checked database operations
3. **Consistent API**: Repository functions follow a consistent pattern
4. **Error Handling**: All functions include error handling and logging 


This document provides a comprehensive guide to using the database components in the Automagik Agents system. It's designed to be useful for both new developers and AI assistants like Claude.

## Directory Structure

The `src/db` directory contains the following components:

- `__init__.py`: Exports all important models and functions for easier imports
- `connection.py`: Handles database connection management and query execution
- `models.py`: Contains Pydantic models representing database tables
- `repository.py`: Provides CRUD operations for all database entities

## Overview

We use a clean repository pattern to abstract database operations:

1. **Models** represent the database tables as Pydantic classes
2. **Repository functions** handle CRUD operations for each entity type
3. **Connection utilities** manage the database pool and query execution

## Models

Models are Pydantic classes that represent database tables. They provide type safety, validation, and easy serialization/deserialization.

Example models:

```python
from src.db import Agent, User, Session

# Create a new user
user = User(
    email="user@example.com",
    phone_number="1234567890",
    user_data={"name": "Example User"}
)

# Create a new agent
agent = Agent(
    name="my_agent",
    type="simple",
    model="gpt-4",
    description="A simple agent",
    config={"temperature": 0.7},
    version="1.0.0"
)

# Create a new session
session = Session(
    id=uuid.uuid4(),
    user_id=1,
    agent_id=2,
    name="Example Session",
    platform="web"
)
```

## Repository Functions

Repository functions provide a clean interface for database operations. They handle all SQL construction, parameter binding, and error handling.

### Agents

```python
from src.db import create_agent, get_agent, list_agents, update_agent, delete_agent

# Create or update an agent
agent_id = create_agent(agent)

# Get an agent by ID
agent = get_agent(agent_id)

# Get an agent by name
agent = get_agent_by_name("my_agent")

# List all agents
agents = list_agents()

# List only active agents
active_agents = list_agents(active_only=True)

# Update an agent
agent.description = "Updated description"
updated_id = update_agent(agent)

# Delete an agent
success = delete_agent(agent_id)
```

### Users

```python
from src.db import create_user, get_user, get_user_by_email, list_users, update_user, delete_user

# Create a user
user_id = create_user(user)

# Get a user by ID
user = get_user(user_id)

# Get a user by email
user = get_user_by_email("user@example.com")

# List all users
users = list_users()

# Update a user
user.email = "updated@example.com"
updated_id = update_user(user)

# Delete a user
success = delete_user(user_id)
```

### Sessions

```python
from src.db import create_session, get_session, list_sessions, update_session, delete_session, finish_session

# Create a session
session_id = create_session(session)

# Get a session by ID
session = get_session(session_id)

# List sessions for a user
user_sessions = list_sessions(user_id=user_id)

# List sessions for an agent
agent_sessions = list_sessions(agent_id=agent_id)

# Update a session
session.name = "Updated Session Name"
updated_id = update_session(session)

# Mark a session as finished
success = finish_session(session_id)

# Delete a session
success = delete_session(session_id)
```

### Memories

```python
from src.db import create_memory, get_memory, get_memory_by_name, list_memories, update_memory, delete_memory

# Create a memory
memory = Memory(
    name="important_info",
    content="This is important information",
    agent_id=agent_id,
    user_id=user_id
)
memory_id = create_memory(memory)

# Get a memory by ID
memory = get_memory(memory_id)

# Get a memory by name
memory = get_memory_by_name("important_info", agent_id=agent_id, user_id=user_id)

# List memories with filters
agent_memories = list_memories(agent_id=agent_id)
user_memories = list_memories(agent_id=agent_id, user_id=user_id)
tool_memories = list_memories(agent_id=agent_id, read_mode="tool")

# Update a memory
memory.content = "Updated content"
updated_id = update_memory(memory)

# Delete a memory
success = delete_memory(memory_id)
```

## Direct Connection Usage

For advanced use cases, you can use the connection utilities directly:

```python
from src.db import execute_query, execute_batch, get_db_connection, get_db_cursor

# Execute a simple query
results = execute_query("SELECT * FROM users WHERE email = %s", ["user@example.com"])

# Execute a batch of queries
execute_batch(
    "INSERT INTO log_entries (user_id, message) VALUES (%s, %s)",
    [(1, "Log message 1"), (1, "Log message 2")]
)

# Use a connection context manager
with get_db_connection() as conn:
    # Connection is automatically returned to the pool when done
    pass

# Use a cursor context manager
with get_db_cursor() as cursor:
    # Cursor is automatically closed when done
    cursor.execute("SELECT NOW()")
    result = cursor.fetchone()
```

## Best Practices

1. **Always use models and repository functions** instead of direct SQL when possible
2. **Handle errors** that might be raised by repository functions
3. **Use type hints** to get better IDE support
4. **Don't bypass the repository layer** by writing direct SQL in application code
5. **Keep repository functions focused** on one entity type

## Common Patterns

### Creating or Updating an Entity

Many repository functions like `create_agent` or `create_user` will automatically update the entity if it already exists with the same name/email.

```python
# This will create a new agent or update an existing one with the same name
agent_id = create_agent(agent)
```

### Working with UUIDs

Session IDs and Memory IDs are UUIDs. Always convert string UUIDs to UUID objects:

```python
import uuid

# Convert string to UUID
session_id_str = "550e8400-e29b-41d4-a716-446655440000"
session_id = uuid.UUID(session_id_str)

# Get a session using the UUID
session = get_session(session_id)
```

### Converting Between Models and Dictionaries

Pydantic models can be easily converted to dictionaries:

```python
# Convert model to dict
user_dict = user.model_dump()

# Convert dict to model
user = User(**user_dict)
```

## For LLMs/AI Assistants

When working with this codebase, here are some tips:

1. Always import from `src.db` rather than directly from sub-modules
2. Use the repository pattern for database operations
3. Use Pydantic models for all database entities
4. Handle errors appropriately in try/except blocks
5. Be aware of the difference between `None`, `[]`, and empty result sets
6. Look at the model definitions in `models.py` to understand the data structure

By following these guidelines, you'll help maintain a clean and consistent codebase. 