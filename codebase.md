# .cursor/rules/db-rules.mdc

```mdc
---
description: 
globs: 
alwaysApply: true
---

# Your rule content
whenever doing any db operations, refer to [db_instructions.md](mdc:src/db/db_instructions.md), not to recreate anything that exists.


```

# .cursor/rules/task-rules.mdc

```mdc
---
description: 
globs: 
alwaysApply: true
---
## Task Management Protocol

1. **Task Documentation**:
   - For each new task, create a single Markdown file in the format `YYYYMMDD_HHMMSS_task_name.md` (use `get_datetime`) in the `tasks/` directory (which already exists, do not try to recreate.)
   - This file will serve as the complete record of the task's lifecycle

2. **Task File Structure**:
   - Each task file should contain these clearly labeled sections:
     - **Analysis**: Initial assessment of requirements and challenges
     - **Plan**: Step-by-step approach with file references and dependencies
     - **Execution**: Implementation details and decisions made during coding
     - **Testing**: Evidence of functionality with test cases and results
     - **Summary**: Brief overview of changes made and potential future impact

3. **Workflow Progression**:
   - Update the task file as you progress through each phase
   - Each section should be completed in sequence before moving to the next
   - Never proceed to the Summary without documented testing evidence
   
4. **Testing Requirements**:
   - All code changes must include specific test scenarios
   - Document both expected and actual outcomes
   - Include error handling tests where applicable
   
5. **Debugging-Focused Documentation**:
   - In the Summary section, always document:
     - Files modified with line number ranges
     - Dependencies introduced or modified
     - Edge cases considered
     - Known limitations
     - Potential future impact points
```

# .env-example

```
# Authentication
AM_API_KEY=your_api_key_here  # Required for accessing protected endpoints

# Server Configuration
AM_PORT=8881
AM_HOST=0.0.0.0
AM_ENV=development  # development, production, testing

# Logging Configuration
AM_LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key

LOGFIRE_TOKEN=your_logfire_token

# Notion Integration (Optional)
NOTION_TOKEN=your_notion_integration_token_here

# Discord
DISCORD_BOT_TOKEN=your_discord_bot_token_here

```

# pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "automagik-agents"
dynamic = ["version"]
description = "Automagik agents templates"
readme = "README.md"
requires-python = ">=3.10, <3.13"
license = {text = "MIT"}
authors = [
    {name = "Cezar Vasconcelos", email = "cezar@namastex.ai"}
]
keywords = ["ai", "agents", "pydantic", "fastapi", "notion"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "python-dotenv>=1.0.1",
    "notion-client>=2.3.0",
    "rich>=13.9.4",
    "logfire>=3.6.1",
    "fastapi>=0.104.1",
    "uvicorn>=0.24.0",
    "pydantic-settings>=2.8.0",
    "typer>=0.9.0",
    "build>=1.2.2.post1",
    "twine>=6.1.0",
    "discord-py>=2.4.0",
    "psycopg2-binary>=2.9.10",
    "pydantic-ai-graph>=0.0.0",
    "pydantic-ai>=0.0.36",
    "pytest>=8.3.5",
    "pytest-html>=4.1.1",
    "pytest-json-report>=1.5.0",
    "pytest-xdist>=3.6.1",
    "requests>=2.32.3",
    "ruff>=0.10.0",
    "uv>=0.6.8",
    "pydantic-ai-slim[duckduckgo]>=0.0.42",
    "pip>=25.0.1",
]

[project.urls]
Homepage = "https://github.com/namastexlabs/automagik-agents"
Repository = "https://github.com/namastexlabs/automagik-agents"
Issues = "https://github.com/namastexlabs/automagik-agents/issues"

[project.scripts]
automagik-agents = "src.cli:app"

[tool.setuptools]
packages = ["src"]

[tool.setuptools.dynamic]
version = {attr = "src.version.__version__"}

[tool.logfire]
ignore_no_config = true

[tool.codeflash]
# All paths are relative to this pyproject.toml's directory.
module-root = "src"
tests-root = "tests"
test-framework = "pytest"
ignore-paths = []
formatter-cmds = ["ruff check --exit-zero --fix $file", "ruff format $file"]

```

# requirements.txt

```txt
# Core dependencies
fastapi>=0.105.0
uvicorn>=0.25.0
pydantic>=2.5.0
pydantic-ai>=0.3.0
httpx>=0.25.0
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
typer>=0.9.0
asyncio>=3.4.3

# Tools and utilities
pillow>=10.1.0      # For image processing
requests>=2.31.0    # For HTTP requests
python-multipart>=0.0.6   # For form data handling
mimetypes>=2.0.0    # For content type detection

# Command line interface
rich>=13.7.0        # For pretty terminal output
click>=8.1.7        # For command line interfaces

# Required for multimodal support
base64io>=1.0.3     # For base64 encoding/decoding 
```

# src/__init__.py

```py
# This file is intentionally left empty to mark the directory as a Python package. 
```

# src/__main__.py

```py
"""Main entry point for the application when run as a module.

This allows running the Sofia application with:
    python -m src
"""

import sys
import logging
from importlib import import_module

# Import necessary modules for logging configuration
try:
    from src.utils.logging import configure_logging
    from src.config import settings
    
    # Configure logging before anything else
    configure_logging()
    
    # Get our module's logger
    logger = logging.getLogger(__name__)
except ImportError as e:
    print(f"Error importing core modules: {e}")
    sys.exit(1)

def main():
    """Run the Sofia application."""
    try:
        # Log startup message
        logger.info("Starting Sofia application via 'python -m src'")
        
        # Check if application is being run directly
        if len(sys.argv) > 1:
            # If arguments are passed, use them with the main module's argument parser
            import argparse
            
            # Create argument parser (duplicating what's in main.py)
            parser = argparse.ArgumentParser(description="Run the Sofia application server")
            parser.add_argument(
                "--reload", 
                action="store_true", 
                default=None,
                help="Enable auto-reload for development (default: auto-enabled in development mode)"
            )
            parser.add_argument(
                "--host", 
                type=str, 
                default=settings.AM_HOST,
                help=f"Host to bind the server to (default: {settings.AM_HOST})"
            )
            parser.add_argument(
                "--port", 
                type=int, 
                default=int(settings.AM_PORT),
                help=f"Port to bind the server to (default: {settings.AM_PORT})"
            )
            
            # Parse arguments
            args = parser.parse_args()
            
            # Determine if auto-reload should be enabled
            # If --reload flag is explicitly provided, use that value
            # Otherwise, auto-enable in development mode
            from src.config import Environment
            should_reload = args.reload
            if should_reload is None:
                should_reload = settings.AM_ENV == Environment.DEVELOPMENT
            
            # Log the configuration
            reload_status = "Enabled" if should_reload else "Disabled"
            logger.info("Starting server with configuration:")
            logger.info(f"├── Host: {args.host}")
            logger.info(f"├── Port: {args.port}")
            logger.info(f"└── Auto-reload: {reload_status}")
            
            # Run the server with the provided arguments
            import uvicorn
            uvicorn.run(
                "src.main:app",
                host=args.host,
                port=args.port,
                reload=should_reload
            )
        else:
            # If no arguments are passed, run with default settings
            import uvicorn
            
            # Auto-enable reload in development mode
            from src.config import Environment
            should_reload = settings.AM_ENV == Environment.DEVELOPMENT
            reload_status = "Enabled" if should_reload else "Disabled"
            
            # Log the default configuration
            logger.info("Starting server with default configuration:")
            logger.info(f"├── Host: {settings.AM_HOST}")
            logger.info(f"├── Port: {settings.AM_PORT}")
            logger.info(f"└── Auto-reload: {reload_status}")
            
            uvicorn.run(
                "src.main:app",
                host=settings.AM_HOST,
                port=int(settings.AM_PORT),
                reload=should_reload
            )
    except Exception as e:
        logger.error(f"Error running application: {str(e)}")
        # Print traceback for easier debugging
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 
```

# src/agents/__init__.py

```py
"""Agents package.

This package contains all agent implementations.
"""

```

# src/agents/models/__init__.py

```py
from typing import Dict, Type, Optional
from src.agents.models.base_agent import BaseAgent

def initialize_agent(agent_class: Type[BaseAgent], config: Optional[Dict[str, str]] = None) -> BaseAgent:
    """Initialize an agent with configuration.
    
    Args:
        agent_class: The agent class to initialize
        config: Optional configuration override
        
    Returns:
        Initialized agent instance
    """
    if config is None:
        config = {}
    return agent_class(config) 
```

# src/agents/models/agent_db.py

```py
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
```

# src/agents/models/agent_factory.py

```py
import importlib
import logging
from pathlib import Path
from typing import Dict, Type, List, Tuple
import uuid

from src.agents.models.base_agent import BaseAgent
from src.agents.models.agent_db import (
    register_agent,
    get_agent_by_name,
)

logger = logging.getLogger(__name__)


class AgentFactory:
    """Factory class for creating and managing agents."""

    _agents: Dict[
        str, Tuple[Type[BaseAgent], str]
    ] = {}  # Maps agent_name -> (agent_class, agent_type)
    _initialized_agents: Dict[str, BaseAgent] = {}
    _agent_db_ids: Dict[str, str] = {}  # Maps agent_name -> database_id

    @classmethod
    def discover_agents(cls) -> None:
        """Discover all available agents using standardized create_agent functions."""
        agents_dir = Path(__file__).parent.parent
        logger.info(f"Scanning for agents in directory: {agents_dir}")

        # Clear existing agents
        cls._agents.clear()
        cls._initialized_agents.clear()
        cls._agent_db_ids.clear()

        # Scan for agent type directories
        for type_dir in agents_dir.iterdir():
            if type_dir.is_dir() and type_dir.name not in ["models", "__pycache__"]:
                agent_type = type_dir.name
                
                # Check if the directory has an __init__.py file
                init_file = type_dir / "__init__.py"
                if init_file.exists():
                    logger.info(f"Found agent type directory with __init__.py: {type_dir}")
                    
                    # For each agent subdirectory, register it as an agent
                    for agent_dir in type_dir.iterdir():
                        if agent_dir.is_dir() and agent_dir.name != "__pycache__":
                            agent_name = agent_dir.name
                            full_agent_name = agent_name if agent_name.endswith("_agent") else f"{agent_name}_agent"
                            
                            logger.info(f"Registering agent: {full_agent_name} [Type: {agent_type}]")
                            
                            # Store the agent name and type for later initialization
                            # We'll use GenericAgent as a placeholder until actual initialization
                            class GenericAgent(BaseAgent):
                                def __init__(self, config=None):
                                    super().__init__(config or {}, f"Generic {full_agent_name}")
                                def register_tools(self):
                                    pass
                                def run(self, *args, **kwargs):
                                    pass
                                    
                            cls._agents[full_agent_name] = (GenericAgent, agent_type)

        # Report discovered agents
        if cls._agents:
            logger.info(f"Discovered {len(cls._agents)} agents: {', '.join(cls._agents.keys())}")
        else:
            logger.warning("No agents discovered!")

    @classmethod
    def get_agent(cls, agent_name: str) -> BaseAgent:
        """Get an initialized agent instance by name."""
        # Add _agent suffix if not present
        original_name = agent_name
        if not agent_name.endswith("_agent"):
            agent_name = f"{agent_name}_agent"

        # Refresh the agent instance to ensure run_id is always up to date
        if agent_name in cls._initialized_agents:
            # Force recreation of agent to refresh run_id
            del cls._initialized_agents[agent_name]
            logger.info(f"Forcing recreation of {agent_name} to refresh run_id")

        if agent_name not in cls._initialized_agents:
            if agent_name not in cls._agents:
                cls.discover_agents()
                if agent_name not in cls._agents:
                    available_agents = cls.list_available_agents()
                    raise ValueError(
                        f"Agent {agent_name} not found. Available agents: {', '.join(available_agents)}"
                    )

            # Get the agent type
            _, agent_type = cls._agents[agent_name]
            
            try:
                # Import the agent type module (e.g., src.agents.simple)
                type_module_path = f"src.agents.{agent_type}"
                type_module = importlib.import_module(type_module_path)
                
                # Get the base name without _agent suffix if needed
                base_name = agent_name.replace("_agent", "") if agent_name.endswith("_agent") else agent_name
                
                # Create the agent using the standardized function
                if hasattr(type_module, "create_agent") and callable(type_module.create_agent):
                    logger.info(f"Using create_agent from {type_module_path}")
                    agent = type_module.create_agent(base_name)
                else:
                    # Try to import the specific agent module as a fallback
                    agent_module_path = f"src.agents.{agent_type}.{base_name}"
                    try:
                        agent_module = importlib.import_module(agent_module_path)
                        if hasattr(agent_module, "create_agent"):
                            logger.info(f"Using create_agent from {agent_module_path}")
                            agent = agent_module.create_agent()
                        else:
                            raise AttributeError(f"Could not find create_agent function in {agent_module_path}")
                    except ImportError:
                        # Try with _agent suffix in the module path if base_name doesn't have it
                        if not base_name.endswith("_agent"):
                            agent_module_path = f"src.agents.{agent_type}.{base_name}_agent"
                            agent_module = importlib.import_module(agent_module_path)
                            if hasattr(agent_module, "create_agent"):
                                logger.info(f"Using create_agent from {agent_module_path}")
                                agent = agent_module.create_agent()
                            else:
                                raise AttributeError(f"Could not find create_agent function in {agent_module_path}")
                        else:
                            raise
                
                # Extract agent metadata for database registration
                agent_class = type(agent)
                config_dict = {}
                
                if hasattr(agent, "config"):
                    config = getattr(agent, "config")
                    # Ensure config is a dictionary
                    if isinstance(config, dict):
                        config_dict = config
                    else:
                        # Try to convert to dict if it has __dict__ attribute
                        if hasattr(config, "__dict__"):
                            config_dict = config.__dict__
                        else:
                            config_dict = {"value": str(config)}
                
                description = (
                    getattr(agent, "description", "") 
                    or getattr(agent_class, "__doc__", "") 
                    or f"{agent_name} agent"
                )
                model = config_dict.get("model", "")
                
                # Update the agent class in the registry
                cls._agents[agent_name] = (agent_class, agent_type)
                
                # Register in database if not already registered
                if agent_name not in cls._agent_db_ids:
                    try:
                        db_id = register_agent(
                            name=agent_name,
                            agent_type=agent_type,
                            model=model,
                            description=description,
                            config=config_dict,
                        )
                        cls._agent_db_ids[agent_name] = db_id
                        agent.db_id = db_id
                    except Exception as e:
                        logger.error(f"Failed to register agent {agent_name} in database: {str(e)}")
                else:
                    agent.db_id = cls._agent_db_ids[agent_name]
                
                # Store the initialized agent
                cls._initialized_agents[agent_name] = agent
                logger.info(f"Successfully initialized agent: {agent_name}")
                
            except Exception as e:
                logger.error(f"Failed to initialize agent {agent_name}: {str(e)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise ValueError(f"Failed to initialize agent {agent_name}: {str(e)}")

        return cls._initialized_agents[agent_name]

    @classmethod
    def list_available_agents(cls) -> List[str]:
        """List all available agent names."""
        if not cls._agents:
            cls.discover_agents()
        return list(cls._agents.keys())

    @classmethod
    def get_agent_type(cls, agent_name: str) -> str:
        """Get the type of an agent by name."""
        if not cls._agents:
            cls.discover_agents()

        if not agent_name.endswith("_agent"):
            agent_name = f"{agent_name}_agent"

        if agent_name not in cls._agents:
            available_agents = cls.list_available_agents()
            raise ValueError(
                f"Agent {agent_name} not found. Available agents: {', '.join(available_agents)}"
            )

        return cls._agents[agent_name][1]

    @classmethod
    def link_agent_to_session(cls, agent_name: str, session_id_or_name: str) -> bool:
        """Link an agent to a session in the database.
        
        Args:
            agent_name: The name of the agent to link
            session_id_or_name: Either a session ID or name
            
        Returns:
            True if the link was successful, False otherwise
        """
        # Check if the input is potentially a session name rather than a UUID
        session_id = session_id_or_name
        try:
            # Try to parse as UUID
            uuid.UUID(session_id_or_name)
        except ValueError:
            # Not a UUID, try to look up by name
            logger.info(f"Session ID is not a UUID, treating as session name: {session_id_or_name}")
            
            # Use the appropriate database function to get session by name
            from src.db import get_session_by_name
            
            session = get_session_by_name(session_id_or_name)
            if not session:
                logger.error(f"Session with name '{session_id_or_name}' not found")
                return False
                
            session_id = str(session.id)
            logger.info(f"Found session ID {session_id} for name {session_id_or_name}")

        # Now that we have a valid session ID, proceed with linking
        try:
            # Get the database ID for the agent name
            agent = None
            for name, (a_class, _) in cls._agents.items():
                if name == agent_name or f"{name}_agent" == agent_name:
                    a_instance = cls.get_agent(name)
                    agent_id = getattr(a_instance, "db_id", None)
                    if agent_id:
                        from src.db import link_session_to_agent
                        return link_session_to_agent(uuid.UUID(session_id), agent_id)

            # Try direct lookup by name in case the agent was registered directly in the database
            from src.db import get_agent_by_name, link_session_to_agent

            agent = get_agent_by_name(agent_name)
            if agent:
                return link_session_to_agent(uuid.UUID(session_id), agent.id)

            # Try with _agent suffix if needed
            agent_full_name = f"{agent_name}_agent" if not agent_name.endswith("_agent") else agent_name
            agent = get_agent_by_name(agent_full_name)
            if agent:
                return link_session_to_agent(uuid.UUID(session_id), agent.id)
                
            logger.error(f"Could not find agent with name '{agent_name}' to link to session")
            return False
        except Exception as e:
            logger.error(f"Error linking agent {agent_name} to session {session_id}: {str(e)}")
            return False

```

# src/agents/models/agent.py

```py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any, Dict
import logging

from src.memory.message_history import MessageHistory
from pydantic_ai.messages import SystemPromptPart, UserPromptPart, ModelResponse, ModelRequest

class MessageModel(BaseModel):
    role: str
    content: str

class HistoryModel(BaseModel):
    messages: List[MessageModel]

    @classmethod
    def from_message_history(cls, history: MessageHistory):
        messages = []
        for msg in history._messages:
            if isinstance(msg, SystemPromptPart):
                messages.append(MessageModel(role="system", content=msg.system_prompt))
            elif isinstance(msg, UserPromptPart):
                messages.append(MessageModel(role="user", content=msg.prompt))
            elif isinstance(msg, ModelResponse):
                # Extract just the text content from ModelResponse
                content = ""
                for part in msg.parts:
                    if hasattr(part, "content"):
                        content += part.content
                messages.append(MessageModel(role="assistant", content=content))
            elif isinstance(msg, ModelRequest):
                # Process each part of the ModelRequest separately
                for part in msg.parts:
                    if isinstance(part, SystemPromptPart):
                        messages.append(MessageModel(role="system", content=part.content))
                    elif isinstance(part, UserPromptPart):
                        messages.append(MessageModel(role="user", content=part.content))
            else:
                # For any other type, try to get content or convert to string
                content = getattr(msg, "content", str(msg))
                role = getattr(msg, "role", "unknown")
                messages.append(MessageModel(role=role, content=content))
        
        return cls(messages=messages)

class AgentBaseResponse_v2(BaseModel):
    message: str
    history: Dict
    error: Optional[str] = None
    session_id: str

    @classmethod
    def from_agent_response(
        cls,
        message: str,
        history: MessageHistory,
        error: Optional[str] = None,
        tool_calls: List[Dict] = [],
        tool_outputs: List[Dict] = [],
        session_id: str = None
    ) -> "AgentBaseResponse_v2":
        """Create an AgentBaseResponse from the agent's response components.
        
        Args:
            message: The response message from the agent.
            history: The message history object.
            error: Optional error message.
            tool_calls: List of tool calls made during processing (ignored as it's in history).
            tool_outputs: List of outputs from tool calls (ignored as it's in history).
            session_id: The session identifier used for this conversation.
            
        Returns:
            An AgentBaseResponse instance.
        """
        # Create a safe history dict
        try:
            # First try a direct conversion to dictionary
            history_dict = history.to_dict()
            
            # Assert that we have a valid structure
            if not isinstance(history_dict, dict) or "messages" not in history_dict:
                raise ValueError("Invalid history dictionary structure")
                
            # Validate each message has the proper structure
            for i, msg in enumerate(history_dict["messages"]):
                if not isinstance(msg, dict):
                    logging.warning(f"Message at index {i} is not a dict, removing it")
                    history_dict["messages"][i] = None
            
            # Filter out None messages
            history_dict["messages"] = [msg for msg in history_dict["messages"] if msg is not None]
            
        except Exception as e:
            # If history serialization fails, provide a minimal valid dict
            logging.error(f"Error serializing history: {str(e)}")
            history_dict = {"messages": []}
            
        return cls(
            message=message,
            history=history_dict,
            error=error,
            session_id=session_id or history.session_id
        )
```

# src/agents/models/base_agent.py

```py
import logging
import re
from typing import Dict, Optional, Union, List, Any, Set, Type, TypeVar, Generic
from pydantic import BaseModel
from pydantic_ai import Agent as PydanticAgent
from pydantic_ai.usage import UsageLimits
from pydantic_ai.settings import ModelSettings
from src.agents.models.agent import AgentBaseResponse_v2
from src.memory.message_history import MessageHistory
from src.agents.models.dependencies import BaseDependencies
import time
from abc import ABC, abstractmethod
import json
import uuid
from pydantic_ai.messages import SystemPromptPart

logger = logging.getLogger(__name__)

# Define a generic type variable for dependencies
T = TypeVar('T', bound=BaseDependencies)

class AgentConfig:
    """Configuration for an agent.

    Attributes:
        model: The LLM model to use.
        temperature: The temperature to use for LLM calls.
        retries: The number of retries to perform for LLM calls.
    """

    def __init__(self, config: Dict[str, str] = None):
        """Initialize the agent configuration.

        Args:
            config: A dictionary of configuration options.
        """
        self.config = config or {}
        self.model = self.config.get("model", "openai:gpt-3.5-turbo")
        self.temperature = float(self.config.get("temperature", "0.7"))
        self.retries = int(self.config.get("retries", "1"))
        
    def get(self, key: str, default=None):
        """Get a configuration value.
        
        Args:
            key: The configuration key to get
            default: Default value if key is not found
            
        Returns:
            The configuration value or default
        """
        return self.config.get(key, default)
        
    def __getattr__(self, name):
        """Get configuration attribute.
        
        Args:
            name: Attribute name to get
            
        Returns:
            The attribute value or None
            
        Raises:
            AttributeError: If configuration attribute doesn't exist
        """
        if name in self.config:
            return self.config[name]
        return None


class BaseAgent(ABC, Generic[T]):
    """Base class for all agents.

    This class defines the interface that all agents must implement and
    provides common functionality for agent initialization and management.
    """

    def __init__(self, config: Union[Dict[str, str], AgentConfig], system_prompt: str):
        """Initialize the agent.

        Args:
            config: Dictionary or AgentConfig object with configuration options.
            system_prompt: The system prompt to use for this agent.
        """
        
        # Convert config to AgentConfig if it's a dictionary
        if isinstance(config, dict):
            self.config = AgentConfig(config)
        else:
            self.config = config
            
        # Store the system prompt
        self.system_prompt = system_prompt
        
        # Initialize agent ID (will be set later if available)
        self.db_id = None
        
        # Initialize message history (will be set in process_message)
        self.message_history = None
        
        return self
   
```

# src/agents/models/dependencies.py

```py
"""Dependency models for agent implementations.

This module provides typed dependencies for all agents in the system,
following pydantic-ai best practices for dependency injection.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List, Union, Generic, TypeVar
import logging
from datetime import datetime

# Import constants
from src.constants import (
    DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS, DEFAULT_RETRIES
)

# Import httpx for typed HTTP client if available
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    # Create a placeholder class
    class httpx:
        class AsyncClient:
            pass

# Import pydantic-ai types if available
try:
    from pydantic_ai.tools import RunContext
    from pydantic_ai.messages import ModelMessage
    from pydantic_ai.usage import UsageLimits
    from pydantic_ai.settings import ModelSettings
    PYDANTIC_AI_AVAILABLE = True
except ImportError:
    PYDANTIC_AI_AVAILABLE = False
    # Create placeholder types for better error handling
    class RunContext:
        pass
    class ModelMessage:
        pass
    class UsageLimits:
        pass
    class ModelSettings:
        pass

logger = logging.getLogger(__name__)

@dataclass
class BaseDependencies:
    """Base dependencies shared by all agents.
    
    This class provides core functionality needed by any agent type,
    including memory management, user context, and configuration.
    """
    # Context properties
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    
    # Configuration
    api_keys: Dict[str, str] = field(default_factory=dict)
    
    # Database connection (optional, can be None for tests)
    db_connection: Any = None
    
    # Private fields (not part of the initializer)
    _agent_id_numeric: Optional[int] = field(default=None, init=False)
    
    # Memory provider (initialized lazily)
    _memory_provider: Optional[Any] = field(default=None, init=False)
    
    @property
    def memory_provider(self) -> Any:
        """Get the memory provider for this agent.
        
        Returns:
            MemoryProvider instance
        """
        if self._memory_provider is None and self._agent_id_numeric:
            from src.tools.memory_tools.provider import MemoryProvider
            self._memory_provider = MemoryProvider(self._agent_id_numeric)
            logger.debug(f"Created memory provider for agent {self._agent_id_numeric}")
        
        if self._memory_provider is None:
            # Create a fallback provider if agent ID isn't set
            from src.tools.memory_tools.provider import MemoryProvider
            self._memory_provider = MemoryProvider(999)
            logger.warning("Created fallback memory provider with agent ID 999")
        
        return self._memory_provider
    
    def set_agent_id(self, agent_id: int) -> None:
        """Set the agent ID for database operations.
        
        Args:
            agent_id: Numeric ID of the agent in the database
        """
        self._agent_id_numeric = agent_id
        # Reset memory provider to use new agent ID
        self._memory_provider = None
        logger.debug(f"Set agent ID to {agent_id} for dependency object")
    
    async def get_memory(self, name: str) -> Optional[Dict[str, Any]]:
        """Fetch memory from database by name.
        
        Args:
            name: Name of the memory to retrieve
            
        Returns:
            Memory object or None if not found
        """
        from src.db import get_memory_by_name
        try:
            if not self._agent_id_numeric:
                logger.warning(f"Agent ID not set for memory retrieval: {name}")
                return None
                
            memory = get_memory_by_name(name, agent_id=self._agent_id_numeric)
            if memory:
                return {
                    "id": str(memory.id),
                    "name": memory.name,
                    "description": memory.description,
                    "content": memory.content,
                    "created_at": memory.created_at,
                    "updated_at": memory.updated_at
                }
            return None
        except Exception as e:
            logger.error(f"Error in get_memory({name}): {str(e)}")
            return None
    
    async def get_all_memories(self) -> List[Dict[str, Any]]:
        """Get all memories for this agent.
        
        Returns:
            List of all memory objects for this agent
        """
        from src.db import list_memories
        try:
            if not self._agent_id_numeric:
                logger.warning("Agent ID not set for memory listing")
                return []
                
            memories = list_memories(agent_id=self._agent_id_numeric)
            return [
                {
                    "id": str(m.id),
                    "name": m.name,
                    "description": m.description,
                    "content": m.content if hasattr(m, "content") else None
                }
                for m in memories
            ]
        except Exception as e:
            logger.error(f"Error in get_all_memories: {str(e)}")
            return []
    
    async def store_memory(self, 
                          name: str, 
                          content: Union[str, Dict[str, Any]], 
                          description: Optional[str] = None) -> Dict[str, Any]:
        """Store a memory in the database.
        
        Args:
            name: Name of the memory to store
            content: Content to store (string or JSON-serializable dict)
            description: Optional description of the memory
            
        Returns:
            Result of the operation with success status
        """
        from src.db import get_memory_by_name, update_memory, create_memory
        try:
            if not self._agent_id_numeric:
                return {"success": False, "error": "Agent ID not set"}
                
            existing = get_memory_by_name(name, agent_id=self._agent_id_numeric)
            
            if existing:
                memory = update_memory({
                    "id": existing.id,
                    "name": name,
                    "content": content,
                    "description": description or existing.description,
                    "agent_id": self._agent_id_numeric
                })
                # Invalidate memory provider cache
                if self._memory_provider:
                    self._memory_provider.invalidate_cache()
                    
                return {
                    "success": True,
                    "action": "updated",
                    "memory_id": str(memory)
                }
            else:
                memory_data = {
                    "name": name,
                    "content": content,
                    "description": description,
                    "agent_id": self._agent_id_numeric
                }
                memory_id = create_memory(memory_data)
                # Invalidate memory provider cache
                if self._memory_provider:
                    self._memory_provider.invalidate_cache()
                    
                return {
                    "success": True,
                    "action": "created",
                    "memory_id": str(memory_id)
                }
        except Exception as e:
            logger.error(f"Error in store_memory({name}): {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def increment_run_id(self) -> int:
        """Increment and get the run_id for this agent.
        
        Returns:
            The new run_id after incrementing
        """
        from src.db import increment_agent_run_id, get_agent
        try:
            if not self._agent_id_numeric:
                logger.warning("Agent ID not set for run_id increment")
                return 1
                
            increment_agent_run_id(self._agent_id_numeric)
            agent = get_agent(self._agent_id_numeric)
            return agent.run_id if agent and hasattr(agent, "run_id") else 1
        except Exception as e:
            logger.error(f"Error incrementing run_id: {str(e)}")
            return 1
    
    async def get_current_time(self) -> str:
        """Get the current time formatted as a string.
        
        Returns:
            Current time as formatted string
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class SimpleAgentDependencies(BaseDependencies):
    """Dependencies for SimpleAgent.
    
    Extends the base dependencies with SimpleAgent-specific
    functionality and data following PydanticAI best practices.
    """
    # Message history for the current conversation - properly typed
    message_history: Optional[List["ModelMessage"]] = None
    
    # Tool-specific configuration
    tool_config: Dict[str, Any] = field(default_factory=dict)
    
    # HTTP client for external API calls
    http_client: Optional[Any] = None  # Type as Any for compatibility
    
    # Model configuration
    model_name: str = DEFAULT_MODEL
    model_settings: Dict[str, Any] = field(default_factory=dict)
    usage_limits: Optional[Any] = None  # Type as Any for compatibility
    
    # Search API keys
    duckduckgo_enabled: bool = False
    tavily_api_key: Optional[str] = None
    
    def get_http_client(self) -> Any:
        """Get or initialize the HTTP client.
        
        Returns:
            Configured HTTP client instance
        """
        if not HTTPX_AVAILABLE:
            logger.warning("httpx not available. Install with: pip install httpx")
            return None
            
        if self.http_client is None:
            self.http_client = httpx.AsyncClient(timeout=30)  # 30 second timeout default
        return self.http_client
    
    async def close_http_client(self) -> None:
        """Close the HTTP client if initialized.
        
        This should be called during cleanup to properly release resources.
        """
        if HTTPX_AVAILABLE and self.http_client is not None:
            await self.http_client.aclose()
            self.http_client = None
    
    def set_message_history(self, message_history: List[Any]) -> None:
        """Set the message history for the agent.
        
        Args:
            message_history: Message history as list of messages
        """
        self.message_history = message_history
    
    def get_message_history(self) -> List[Any]:
        """Get the current message history.
        
        Returns:
            List of model messages or empty list if none
        """
        return self.message_history or []
    
    def clear_message_history(self) -> None:
        """Clear the message history.
        
        This is useful when starting a new conversation.
        """
        self.message_history = None
    
    def enable_duckduckgo_search(self, enabled: bool = True) -> None:
        """Enable or disable DuckDuckGo search functionality.
        
        Args:
            enabled: Whether search should be enabled
        """
        self.duckduckgo_enabled = enabled
    
    def set_tavily_api_key(self, api_key: Optional[str]) -> None:
        """Set the Tavily API key for search.
        
        Args:
            api_key: Tavily API key or None to disable
        """
        self.tavily_api_key = api_key
        
    def is_search_enabled(self) -> bool:
        """Check if any search capability is enabled.
        
        Returns:
            True if either DuckDuckGo or Tavily search is available
        """
        return self.duckduckgo_enabled or self.tavily_api_key is not None
    
    def set_model_settings(self, settings: Dict[str, Any]) -> None:
        """Set model settings for the agent.
        
        Args:
            settings: Dictionary of model settings (temperature, etc.)
        """
        self.model_settings.update(settings)
    
    def set_usage_limits(self, 
                         response_tokens_limit: Optional[int] = None,
                         request_limit: Optional[int] = None,
                         total_tokens_limit: Optional[int] = None) -> None:
        """Set usage limits for the agent.
        
        Args:
            response_tokens_limit: Maximum tokens in response
            request_limit: Maximum number of requests
            total_tokens_limit: Maximum total tokens
        """
        if not PYDANTIC_AI_AVAILABLE:
            logger.warning("pydantic-ai not available, usage limits not applied")
            return
            
        self.usage_limits = UsageLimits(
            response_tokens_limit=response_tokens_limit,
            request_limit=request_limit, 
            total_tokens_limit=total_tokens_limit
        )
    
    async def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences from memory if available.
        
        This method fetches user preferences from the agent's memory.
        
        Returns:
            User preferences as a dictionary or empty dict if not found
        """
        prefs = await self.get_memory("user_preferences")
        if prefs and "content" in prefs:
            return prefs["content"] if isinstance(prefs["content"], dict) else {}
        return {}
    
    async def store_user_preferences(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Store user preferences in memory.
        
        This method updates or creates user preferences in the agent's memory.
        
        Args:
            preferences: Dictionary of user preferences to store
            
        Returns:
            Dictionary with success status and action performed
        """
        result = await self.store_memory(
            "user_preferences",
            preferences,
            "User preferences and settings"
        )
        return {"success": result.get("success", False), 
                "action": result.get("action", "unknown")}
                
    def configure_for_multimodal(self, enable: bool = True, modality: str = "image") -> None:
        """Configure the agent for multimodal capabilities.
        
        Note: This method doesn't change the model. If the current model doesn't support
        the requested modality, errors will occur naturally when trying to use it.
        
        Args:
            enable: Whether to enable multimodal support
            modality: The modality to support: "image", "audio", or "document"
        """
        # This is now a placeholder method that does nothing
        # We'll let errors occur naturally if the model doesn't support the modality
        pass 
```

# src/agents/models/placeholder.py

```py
"""Placeholder agent implementation.

This module provides a PlaceholderAgent that can be used as a fallback
when a real agent initialization fails. This ensures the system doesn't 
completely break when an agent can't be properly initialized.
"""
import logging
from typing import Dict, Optional, List, Any, Union

from src.agents.models.base_agent import BaseAgent
from src.agents.models.response import AgentResponse
from src.memory.message_history import MessageHistory

logger = logging.getLogger(__name__)

class PlaceholderAgent(BaseAgent):
    """Placeholder agent implementation for fallback when initialization fails.
    
    This agent provides minimal functionality and will return error messages
    when attempts are made to use it. It allows the system to continue running
    even when a real agent fails to initialize.
    """
    
    def __init__(self, config: Dict[str, str]):
        """Initialize the placeholder agent.
        
        Args:
            config: Configuration dictionary
        """
        # Create a useful name for logging
        self.name = config.get("name", "placeholder_agent")
        self.agent_type = config.get("type", "placeholder")
        
        # Set a descriptive system prompt
        system_prompt = "This is a placeholder agent that cannot process requests. Please check logs for initialization errors."
        
        # Initialize the base agent
        super().__init__(config, system_prompt)
        logger.info(f"Created PlaceholderAgent with name: {self.name}")
    
    def register_tools(self):
        """Register tools with the agent.
        
        This is required by BaseAgent but does nothing in the placeholder.
        """
        logger.debug(f"PlaceholderAgent.register_tools called for {self.name}")
        pass
    
    async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[Union[int, str]] = None, user_id: int = 1, context: Optional[Dict] = None) -> AgentResponse:
        """Process a user message and return an error response.
        
        Args:
            user_message: The message to process
            session_id: Optional session ID for message context
            agent_id: Optional agent ID
            user_id: Optional user ID
            context: Optional additional context
            
        Returns:
            Error response indicating this is a placeholder agent
        """
        logger.warning(f"Attempt to use PlaceholderAgent {self.name} to process message")
        
        # Return an error response
        return AgentResponse(
            text=f"This agent ({self.name}) failed to initialize properly. Please check logs for more information.",
            success=False,
            error_message="Agent initialization failed"
        )
    
    async def run(self, *args, **kwargs) -> AgentResponse:
        """Placeholder run method that returns an error.
        
        Returns:
            Error response indicating this is a placeholder agent
        """
        logger.warning(f"Attempt to use PlaceholderAgent {self.name} to run")
        
        return AgentResponse(
            text=f"This agent ({self.name}) failed to initialize properly. Please check logs for more information.",
            success=False,
            error_message="Agent initialization failed"
        ) 
```

# src/agents/models/response.py

```py
from pydantic import BaseModel
from typing import Optional, List, Any, Dict, Union


class AgentResponse(BaseModel):
    """Standard response format for SimpleAgent.
    
    This class provides a standardized response format for the SimpleAgent
    that includes the text response, success status, and any tool calls or
    outputs that were made during processing.
    """
    text: str
    success: bool = True
    error_message: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_outputs: Optional[List[Dict]] = None
    raw_message: Optional[Union[Dict, List]] = None 
```

# src/agents/simple/__init__.py

```py
"""Simple agents type package.

This package contains agents with basic functionality.
"""

import os
import importlib
import logging
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)

# Discover agents in subfolders
def discover_agents():
    """Discover agent modules in the simple agent type directory."""
    agents = {}
    current_dir = Path(__file__).parent
    
    for item in current_dir.iterdir():
        if item.is_dir() and not item.name.startswith('__'):
            try:
                # Try to import the module
                module_name = f"src.agents.simple.{item.name}"
                module = importlib.import_module(module_name)
                
                # Check if the module has a create_agent function
                if hasattr(module, "create_agent") and callable(module.create_agent):
                    agent_name = item.name
                    agents[agent_name] = module.create_agent
                    logger.info(f"Discovered agent: {agent_name}")
            except Exception as e:
                logger.error(f"Error importing agent from {item.name}: {str(e)}")
    
    return agents

# Get discovered agents
_discovered_agents = discover_agents()

def create_agent(agent_name=None):
    """Create an agent instance by name.
    
    Args:
        agent_name: The name of the agent to create
                   If None, creates a simple agent.
        
    Returns:
        An instance of the requested agent
    
    Raises:
        ValueError: If the agent cannot be found or created
    """
    # If no agent_name specified or it's "simple", default to simple_agent
    if agent_name is None or agent_name == "simple":
        agent_name = "simple_agent"
    
    # Remove _agent suffix if present (for normalization)
    if agent_name.endswith("_agent"):
        base_name = agent_name
    else:
        base_name = f"{agent_name}_agent"
    
    logger.info(f"Creating agent: {base_name}")
    
    # Try to find the agent in discovered agents
    if base_name in _discovered_agents:
        return _discovered_agents[base_name]()
    
    # Direct import approach if agent wasn't discovered
    try:
        module_path = f"src.agents.simple.{base_name}"
        module = importlib.import_module(module_path)
        
        if hasattr(module, "create_agent"):
            return module.create_agent()
        else:
            raise ValueError(f"Module {module_path} has no create_agent function")
            
    except ImportError as e:
        raise ValueError(f"Could not import agent module for {base_name}: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error creating agent {base_name}: {str(e)}")

```

# src/agents/simple/simple_agent/__init__.py

```py
from typing import Dict, Optional, Any
import os
import logging
import traceback

from src.agents.simple.simple_agent.prompts.prompt import SIMPLE_AGENT_PROMPT

# Setup logging first
logger = logging.getLogger(__name__)


try:
    from src.agents.simple.simple_agent.agent import SimpleAgent
    from src.agents.models.placeholder import PlaceholderAgent
    
    # Standardized create_agent function
    def create_agent(config: Optional[Dict[str, str]] = None) -> Any:
        """Create and initialize a SimpleAgent instance.
        
        Args:
            config: Optional configuration override
            
        Returns:
            Initialized SimpleAgent instance
        """
        logger.info("Creating SimpleAgent with PydanticAI ")
        
        default_config = {
            "model": "openai:gpt-4o-mini",  
            "retries": "3"
        }
        
        # Check for environment variables
        if os.environ.get("OPENAI_API_KEY"):
            default_config["openai_api_key"] = os.environ.get("OPENAI_API_KEY")
         
        # Apply user config overrides
        if config:
            default_config.update(config)
        
        # Initialize the agent
        try:
            logger.info(f"Initializing SimpleAgent with config: {default_config}")
            agent = SimpleAgent(default_config)
            logger.info(f"SimpleAgent initialized successfully: {agent}")
            return agent
        except Exception as e:
            logger.error(f"Failed to initialize SimpleAgent: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return PlaceholderAgent({"name": "simple_agent_error", "error": str(e)})
    
except Exception as e:
    logger.error(f"Failed to initialize SimpleAgent module: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
```

# src/agents/simple/simple_agent/agent.py

```py
"""SimpleAgent implementation.

This module provides the SimpleAgent implementation, which is a basic
agent that follows PydanticAI conventions for multimodal support.
"""
import logging
import asyncio
import traceback
import re
from typing import Dict, List, Any, Optional, Callable, Union, TypeVar, Tuple, Set
from functools import partial
import json
import os
import uuid
from datetime import datetime

from pydantic_ai import Agent

from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import UsageLimits

# Tool-related imports
from pydantic_ai.tools import Tool as PydanticTool, RunContext

# Import constants
from src.constants import (
    DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS, DEFAULT_RETRIES
)

# Import dependencies
from src.agents.models.base_agent import BaseAgent
from src.agents.models.dependencies import SimpleAgentDependencies
from src.agents.models.response import AgentResponse
from src.memory.message_history import MessageHistory

from src.tools.datetime import get_current_date_tool, get_current_time_tool, format_date_tool

# Import memory tools but delay actual import until needed to avoid circular imports
memory_tools_imported = False
get_memory_tool = None
store_memory_tool = None
read_memory = None
create_memory = None
update_memory = None

def _import_memory_tools():
    global memory_tools_imported, get_memory_tool, store_memory_tool, read_memory, create_memory, update_memory
    if not memory_tools_imported:
        from src.tools.memory.tool import get_memory_tool as _get_memory_tool
        from src.tools.memory.tool import store_memory_tool as _store_memory_tool
        from src.tools.memory.tool import read_memory as _read_memory
        from src.tools.memory.tool import create_memory as _create_memory
        from src.tools.memory.tool import update_memory as _update_memory
        
        get_memory_tool = _get_memory_tool
        store_memory_tool = _store_memory_tool
        read_memory = _read_memory
        create_memory = _create_memory
        update_memory = _update_memory
        
        memory_tools_imported = True

# Setup logging
logger = logging.getLogger(__name__)
T = TypeVar('T')  # Generic type for callable return values

class SimpleAgent(BaseAgent):
    """SimpleAgent implementation using PydanticAI.
    
    This agent provides a basic implementation that follows the PydanticAI
    conventions for multimodal support and tool calling.
    """
    
    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize the SimpleAgent.
        
        Args:
            config: Dictionary with configuration options
        """
        # Import prompt template from prompt.py
        from src.agents.simple.simple_agent.prompts.prompt import SIMPLE_AGENT_PROMPT
        self.prompt_template = SIMPLE_AGENT_PROMPT
        
        # Store agent_id if provided
        self.db_id = config.get("agent_id")
        if self.db_id and isinstance(self.db_id, str) and self.db_id.isdigit():
            self.db_id = int(self.db_id)
            logger.info(f"Initialized SimpleAgent with database ID: {self.db_id}")
        else:
            # Don't log a warning here, as this is expected during discovery
            # The actual agent_id will be set later in the API routes
            self.db_id = None
        
        # Extract template variables from the prompt
        self.template_vars = self._extract_template_variables(self.prompt_template)
        if self.template_vars:
            logger.info(f"Detected template variables: {', '.join(self.template_vars)}")
            
            # Initialize memory variables if agent ID is available
            if self.db_id:
                try:
                    # Create a basic context with the agent ID
                    context = {"agent_id": self.db_id, "user_id": None}
                    self._initialize_memory_variables_sync(context=context)
                    logger.info(f"Memory variables initialized for agent ID {self.db_id}")
                except Exception as e:
                    logger.error(f"Error initializing memory variables: {str(e)}")
        
        # Create initial system prompt - dynamic parts will be added via decorators
        base_system_prompt = self._create_base_system_prompt()
        
        # Initialize the BaseAgent with proper arguments
        super().__init__(config, base_system_prompt)
        
        # Initialize variables
        self._agent_instance: Optional[Agent] = None
        self._registered_tools: Dict[str, Callable] = {}
        
        # Create dependencies
        self.dependencies = SimpleAgentDependencies(
            model_name=config.get("model", DEFAULT_MODEL),
            model_settings=self._parse_model_settings(config)
        )
        
        # Set agent ID in dependencies
        if self.db_id:
            self.dependencies.set_agent_id(self.db_id)
        
        # Set usage limits if specified
        if "response_tokens_limit" in config or "request_limit" in config or "total_tokens_limit" in config:
            self._set_usage_limits(config)
        
        # Register default tools
        self._register_default_tools()
        
        # Set up message history with a valid session ID but don't auto-create in database during init
        session_id = config.get("session_id", str(uuid.uuid4()))
        self.message_history = MessageHistory(session_id=session_id, no_auto_create=True)
        
        # Initialize context for memory tools
        self.context = {"agent_id": self.db_id}
               
        logger.info("SimpleAgent initialized successfully")
    
    def _extract_template_variables(self, template: str) -> List[str]:
        """Extract all template variables from a string.
        
        Args:
            template: Template string with {{variable}} placeholders
            
        Returns:
            List of variable names without braces
        """
        pattern = r'\{\{([a-zA-Z_]+)\}\}'
        matches = re.findall(pattern, template)
        return list(set(matches))  # Remove duplicates
    
    def _initialize_memory_variables_sync(self, user_id: Optional[int] = None, context: Optional[dict] = None) -> None:
        """Initialize memory variables in the database.
        
        This ensures all template variables exist in memory with default values.
        Uses direct repository calls to avoid async/await issues.
        
        Args:
            user_id: Optional user ID to associate with the memory variables
            context: Optional context dictionary containing agent_id and user_id
        """
        if not self.db_id:
            logger.warning("Cannot initialize memory variables: No agent ID available")
            return
            
        try:
            # Import the repository functions for direct database access
            from src.db.repository.memory import get_memory_by_name, create_memory
            from src.db.models import Memory
            
            # Create context if not provided
            if context is None:
                context = {
                    "agent_id": self.db_id,
                    "user_id": user_id
                }
                
            # Extract all variables except run_id which is handled separately
            memory_vars = [var for var in self.template_vars if var != "run_id"]
            
            # Log the user_id we're using (if any)
            if user_id:
                logger.info(f"Initializing memory variables for user_id={user_id}")
            else:
                logger.warning("No user_id provided, memories will be created with NULL user_id")
            
            for var_name in memory_vars:
                try:
                    # Check if memory already exists with direct repository call for this user
                    existing_memory = get_memory_by_name(var_name, agent_id=self.db_id, user_id=user_id)
                    
                    # If not found, create it with default value
                    if not existing_memory:
                        logger.info(f"Creating missing memory variable: {var_name} for user: {user_id}")
                        
                        # Prepare a proper description based on the variable name
                        description = f"Auto-created template variable for SimpleAgent"
                        if var_name == "personal_attributes":
                            description = "Personal attributes and preferences for the agent"
                            content = "None stored yet. You can update this by asking the agent to remember personal details."
                        elif var_name == "technical_knowledge":
                            description = "Technical knowledge and capabilities for the agent"
                            content = "None stored yet. You can update this by asking the agent to remember technical information."
                        elif var_name == "user_preferences":
                            description = "User preferences and settings for the agent"
                            content = "None stored yet. You can update this by asking the agent to remember your preferences."
                        else:
                            content = "None stored yet"
                        
                        # Create the memory directly using repository function
                        memory = Memory(
                            name=var_name,
                            content=content,
                            description=description,
                            agent_id=self.db_id,
                            user_id=user_id,  # Include the user_id here
                            read_mode="system_prompt",
                            access="read_write"  # Ensure it can be written to
                        )
                        
                        memory_id = create_memory(memory)
                        if memory_id:
                            logger.info(f"Created memory variable: {var_name} with ID: {memory_id} for user: {user_id}")
                        else:
                            logger.error(f"Failed to create memory variable: {var_name}")
                    else:
                        logger.info(f"Memory variable already exists: {var_name}")
                        
                except Exception as e:
                    logger.error(f"Error initializing memory variable {var_name}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error in _initialize_memory_variables_sync: {str(e)}")
    
    def _create_base_system_prompt(self) -> str:
        """Create the base system prompt.
        
        Returns:
            Base system prompt template
        """
        return self.prompt_template

    def _parse_model_settings(self, config: Dict[str, str]) -> Dict[str, Any]:
        """Parse model settings from config.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dictionary with model settings
        """
        settings = {}
        
        # Extract model settings from config
        for key, value in config.items():
            if key.startswith("model_settings."):
                setting_key = key.replace("model_settings.", "")
                settings[setting_key] = value
        
        # Add default settings if not specified
        if "temperature" not in settings and "model_settings.temperature" not in config:
            settings["temperature"] = DEFAULT_TEMPERATURE
        if "max_tokens" not in settings and "model_settings.max_tokens" not in config:
            settings["max_tokens"] = DEFAULT_MAX_TOKENS
            
        return settings
    
    def _set_usage_limits(self, config: Dict[str, str]) -> None:
        """Set usage limits from config.
        
        Args:
            config: Configuration dictionary
        """
            
        # Parse limits from config
        response_tokens_limit = config.get("response_tokens_limit")
        request_limit = config.get("request_limit")
        total_tokens_limit = config.get("total_tokens_limit")
        
        # Convert string values to integers
        if response_tokens_limit:
            response_tokens_limit = int(response_tokens_limit)
        if request_limit:
            request_limit = int(request_limit)
        if total_tokens_limit:
            total_tokens_limit = int(total_tokens_limit)
            
        # Create UsageLimits object
        self.dependencies.set_usage_limits(
            response_tokens_limit=response_tokens_limit,
            request_limit=request_limit,
            total_tokens_limit=total_tokens_limit
        )
    
    async def __aenter__(self):
        """Async context manager entry method."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit method."""
        await self.cleanup()
    
    def _register_default_tools(self) -> None:
        """Register the default set of tools for this agent."""
        # Date/time tools
        self.register_tool(get_current_date_tool)
        self.register_tool(get_current_time_tool)
        self.register_tool(format_date_tool)
        
        # Memory tools
        _import_memory_tools()
        self.register_tool(store_memory_tool)
        self.register_tool(get_memory_tool)
        
        logger.info("Default tools registered for SimpleAgent")
    
    def register_tool(self, tool_func: Callable) -> None:
        """Register a tool with the agent.
        
        Args:
            tool_func: The tool function to register
        """
        name = getattr(tool_func, "__name__", str(tool_func))
        self._registered_tools[name] = tool_func
    
    async def _initialize_agent(self) -> None:
        """Initialize the underlying PydanticAI agent with dynamic system prompts."""
        if self._agent_instance is not None:
            return
            
        # Get model settings
        model_name = self.dependencies.model_name
        model_settings = self._get_model_settings()
        
        # Get available tools
        tools = []
        for name, func in self._registered_tools.items():
            try:
                if hasattr(func, "get_pydantic_tool"):
                    # Use the PydanticAI tool definition if available
                    tool = func.get_pydantic_tool()
                    tools.append(tool)
                    logger.info(f"Registered PydanticAI tool: {name}")
                elif isinstance(func, PydanticTool):
                    # If it's already a PydanticTool instance, use it directly
                    tools.append(func)
                    logger.info(f"Added existing PydanticTool: {name}")
                elif hasattr(func, "__doc__") and callable(func):
                    # Create a basic wrapper for regular functions
                    doc = func.__doc__ or f"Tool for {name}"
                    # Create a simple PydanticTool
                    tool = PydanticTool(
                        name=name,
                        description=doc,
                        function=func
                    )
                    tools.append(tool)
                    logger.info(f"Created PydanticTool for function: {name}")
                else:
                    logger.warning(f"Could not register tool {name}: not a function or missing documentation")
            except Exception as e:
                logger.error(f"Error creating tool {name}: {str(e)}")
        
        logger.info(f"Prepared {len(tools)} tools for PydanticAI agent")
                    
        # Create the agent with a base static system prompt
        try:
            # Initialize with just the template as the base system prompt
            # The template variables will be filled by the dynamic system prompt
            self._agent_instance = Agent(
                model=model_name,
                system_prompt=self.prompt_template,
                tools=tools,
                model_settings=model_settings,
                deps_type=SimpleAgentDependencies
            )
            
            # Register dynamic system prompts before first use
            self._register_system_prompts()
            
            logger.info(f"Initialized agent with model: {model_name} and {len(tools)} tools")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}")
            raise
    
    def _register_system_prompts(self) -> None:
        """Initialize system prompts for the agent.
        
        Since we're manually adding the system prompt to the message history
        before each run, we don't need to use PydanticAI's dynamic system prompt
        decorator, which doesn't work properly with message history.
        """
        if not self._agent_instance:
            logger.error("Cannot register system prompts: Agent not initialized")
            return
            
        logger.info("System prompts will be explicitly added to message history")
        # We're not using the decorator approach since it doesn't work reliably with message history
        # Instead, we explicitly add the system prompt to message history in the run method
    
    def _get_model_settings(self) -> Optional[ModelSettings]:
        """Get model settings for the PydanticAI agent.
        
        Returns:
            ModelSettings object with model configuration
        """
   
        settings = self.dependencies.model_settings.copy()
        
        # Apply defaults if not specified
        if "temperature" not in settings:
            settings["temperature"] = DEFAULT_TEMPERATURE
        if "max_tokens" not in settings:
            settings["max_tokens"] = DEFAULT_MAX_TOKENS
        
        return ModelSettings(**settings)
    
    async def cleanup(self) -> None:
        """Clean up resources used by the agent."""
        if self.dependencies.http_client:
            await self.dependencies.close_http_client()
    
    def _check_and_ensure_memory_variables(self, user_id: Optional[int] = None) -> bool:
        """Check if memory variables are properly initialized and initialize if needed.
        
        Args:
            user_id: Optional user ID to associate with the memory variables
            
        Returns:
            True if all memory variables are properly initialized, False otherwise
        """
        if not self.db_id:
            logger.warning("Cannot check memory variables: No agent ID available")
            return False
            
        try:
            from src.db.repository.memory import get_memory_by_name
            
            # Create a context dict for memory operations
            context = {
                "agent_id": self.db_id,
                "user_id": user_id
            }
            
            # Extract all variables except run_id which is handled separately
            memory_vars = [var for var in self.template_vars if var != "run_id"]
            missing_vars = []
            
            for var_name in memory_vars:
                # Check if memory exists for this user
                existing_memory = get_memory_by_name(var_name, agent_id=self.db_id, user_id=user_id)
                
                if not existing_memory:
                    missing_vars.append(var_name)
            
            # If we found missing variables, try to initialize them
            if missing_vars:
                logger.warning(f"Found {len(missing_vars)} uninitialized memory variables: {', '.join(missing_vars)}")
                # Pass the context to initialization
                self._initialize_memory_variables_sync(user_id, context=context)
                return False
                
            return True
        except Exception as e:
            logger.error(f"Error checking memory variables: {str(e)}")
            return False
            
    async def run(self, input_text: str, *, multimodal_content=None, system_message=None, message_history_obj=None) -> AgentResponse:
        """Run the agent with the given input.
        
        Args:
            input_text: Text input for the agent
            multimodal_content: Optional multimodal content
            system_message: Optional system message for this run (ignored in favor of template)
            message_history_obj: Optional MessageHistory instance for DB storage
            
        Returns:
            AgentResponse object with result and metadata
        """
        # Check and ensure memory variables are initialized if we have an agent ID
        if self.db_id:
            # Get user_id from dependencies if available
            user_id = getattr(self.dependencies, 'user_id', None)
            self._check_and_ensure_memory_variables(user_id)
            if user_id:
                logger.info(f"Checked memory variables for user_id={user_id}")
            else:
                logger.warning("No user_id available in dependencies for memory initialization")
        
        # Initialize agent if not done already
        await self._initialize_agent()
        
        # Get message history from dependencies
        pydantic_message_history = self.dependencies.get_message_history()
        logger.info(f"Got message history from dependencies with {len(pydantic_message_history) if pydantic_message_history else 0} messages")
        
        # Check if we need multimodal support
        agent_input = input_text
        if multimodal_content:
            agent_input = self._configure_for_multimodal(input_text, multimodal_content)
        
        # We will ignore any provided system_message and always use our template
        # with dynamic variables from _register_system_prompts
        if system_message:
            logger.warning("Ignoring provided system_message in favor of template with dynamic variables")
        
        # Store user message in message history database if provided
        if message_history_obj:
            logger.info(f"Using MessageHistory for database storage of messages")
        
        # Log that we're using the dynamic system prompt
        logger.info("Running agent with dynamic system prompt from template.py (reevaluated each run)")
        
        # Run the agent
        try:
            # Include usage_limits if available
            usage_limits = self.dependencies.usage_limits if hasattr(self.dependencies, "usage_limits") else None
            
            # Explicitly include system prompt in message history
            # First, get the filled system prompt
            filled_system_prompt = await self._get_filled_system_prompt()
            
            # Create a new message history with the system prompt at the beginning
            # Import needed types from pydantic_ai
            from pydantic_ai.messages import ModelRequest, SystemPromptPart
            
            # Create system prompt message
            system_message = ModelRequest(
                parts=[SystemPromptPart(content=filled_system_prompt)]
            )
            
            # Add system message to beginning of history (if history exists)
            if pydantic_message_history is None:
                pydantic_message_history = [system_message]
                logger.info("Created new message history with system prompt")
            else:
                # Check if the first message is already a system prompt
                has_system = False
                if pydantic_message_history:
                    first_msg = pydantic_message_history[0]
                    if hasattr(first_msg, 'parts') and first_msg.parts:
                        first_part = first_msg.parts[0]
                        if hasattr(first_part, 'part_kind') and first_part.part_kind == 'system-prompt':
                            has_system = True
                
                if not has_system:
                    # Prepend system message to history
                    pydantic_message_history = [system_message] + pydantic_message_history
                    logger.info("Prepended system prompt to message history")
            
            # Log the system prompt being used
            logger.info(f"Using system prompt: {filled_system_prompt[:100]}...")
            
            result = await self._agent_instance.run(
                agent_input,
                message_history=pydantic_message_history,
                usage_limits=usage_limits,
                deps=self.dependencies
            )
            
            # Extract tool calls and outputs from message parts
            tool_calls = []
            tool_outputs = []
            
            try:
                all_messages = result.all_messages()
                logger.info(f"Retrieved {len(all_messages)} messages from result")
                
                for msg in all_messages:
                    # Handle direct message attributes containing tool calls/returns
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tc in msg.tool_calls:
                            tool_call = {
                                'tool_name': getattr(tc, 'name', getattr(tc, 'tool_name', '')),
                                'args': getattr(tc, 'args', getattr(tc, 'arguments', {})),
                                'tool_call_id': getattr(tc, 'id', getattr(tc, 'tool_call_id', ''))
                            }
                            tool_calls.append(tool_call)
                            logger.info(f"Found direct tool call: {tool_call['tool_name']}")
                            
                    if hasattr(msg, 'tool_outputs') and msg.tool_outputs:
                        for to in msg.tool_outputs:
                            tool_output = {
                                'tool_name': getattr(to, 'name', getattr(to, 'tool_name', '')),
                                'content': getattr(to, 'content', ''),
                                'tool_call_id': getattr(to, 'id', getattr(to, 'tool_call_id', ''))
                            }
                            tool_outputs.append(tool_output)
                            logger.info(f"Found direct tool output: {tool_output['tool_name']}")
                    
                    # Process message parts if available
                    if hasattr(msg, 'parts'):
                        for part in msg.parts:
                            # Check if this part is a tool call by looking for multiple indicators
                            if (hasattr(part, 'part_kind') and part.part_kind == 'tool-call') or \
                               type(part).__name__ == 'ToolCallPart' or \
                               hasattr(part, 'tool_name') and hasattr(part, 'args'):
                                
                                tool_call = {
                                    'tool_name': getattr(part, 'tool_name', ''),
                                    'args': getattr(part, 'args', {}),
                                    'tool_call_id': getattr(part, 'tool_call_id', getattr(part, 'id', ''))
                                }
                                tool_calls.append(tool_call)
                                logger.info(f"Found part tool call: {tool_call['tool_name']}")
                            
                            # Check if this part is a tool return by looking for multiple indicators
                            if (hasattr(part, 'part_kind') and part.part_kind == 'tool-return') or \
                               type(part).__name__ == 'ToolReturnPart' or \
                               (hasattr(part, 'tool_name') and hasattr(part, 'content')):
                                
                                # Extract content, handling both string and object formats
                                content = getattr(part, 'content', None)
                                
                                tool_output = {
                                    'tool_name': getattr(part, 'tool_name', ''),
                                    'content': content,
                                    'tool_call_id': getattr(part, 'tool_call_id', getattr(part, 'id', ''))
                                }
                                tool_outputs.append(tool_output)
                                
                                # Safely log a preview of the content
                                try:
                                    if content is None:
                                        content_preview = "None"
                                    elif isinstance(content, str):
                                        content_preview = content[:50]
                                    elif isinstance(content, dict):
                                        content_preview = f"Dict with keys: {', '.join(content.keys())[:50]}"
                                    else:
                                        content_preview = f"{type(content).__name__}[...]"
                                    
                                    logger.info(f"Found part tool output for {tool_output['tool_name']} with content: {content_preview}")
                                except Exception as e:
                                    logger.warning(f"Error creating content preview: {str(e)}")
                    
                    # Also check for any direct attributes on the message that might contain tool info
                    for attr_name in dir(msg):
                        # Skip private attributes and already processed ones
                        if attr_name.startswith('_') or attr_name in ('parts', 'tool_calls', 'tool_outputs'):
                            continue
                        
                        try:
                            attr_value = getattr(msg, attr_name)
                            # Check if this attribute looks like a tool call or return object
                            if hasattr(attr_value, 'tool_name') and (hasattr(attr_value, 'args') or hasattr(attr_value, 'content')):
                                if hasattr(attr_value, 'args'):
                                    # It's likely a tool call
                                    tool_call = {
                                        'tool_name': getattr(attr_value, 'tool_name', ''),
                                        'args': getattr(attr_value, 'args', {}),
                                        'tool_call_id': getattr(attr_value, 'tool_call_id', getattr(attr_value, 'id', ''))
                                    }
                                    tool_calls.append(tool_call)
                                    logger.info(f"Found attribute tool call: {tool_call['tool_name']}")
                                else:
                                    # It's likely a tool return
                                    content = getattr(attr_value, 'content', None)
                                    tool_output = {
                                        'tool_name': getattr(attr_value, 'tool_name', ''),
                                        'content': content,
                                        'tool_call_id': getattr(attr_value, 'tool_call_id', getattr(attr_value, 'id', ''))
                                    }
                                    tool_outputs.append(tool_output)
                                    logger.info(f"Found attribute tool output: {tool_output['tool_name']}")
                        except Exception:
                            # Skip any attributes that can't be accessed
                            pass
                            
            except Exception as e:
                logger.error(f"Error extracting tool calls and outputs: {str(e)}")
                logger.error(traceback.format_exc())
            
            # Log the extracted tool calls and outputs
            if tool_calls:
                logger.info(f"Found {len(tool_calls)} tool calls in the result")
                for i, tc in enumerate(tool_calls):
                    args_preview = str(tc.get('args', {}))[:50] + ('...' if len(str(tc.get('args', {}))) > 50 else '')
                    logger.info(f"Tool call {i+1}: {tc.get('tool_name', 'unknown')} with args: {args_preview}")
            else:
                logger.info("No tool calls found in the result")
                
            if tool_outputs:
                logger.info(f"Found {len(tool_outputs)} tool outputs in the result")
                for i, to in enumerate(tool_outputs):
                    content = to.get('content', '')
                    try:
                        if content is None:
                            content_preview = "None"
                        elif isinstance(content, str):
                            content_preview = f"string[{len(content)} chars]"
                        elif isinstance(content, dict):
                            content_preview = f"dict[{len(content)} keys]"
                        else:
                            content_preview = f"{type(content).__name__}"
                        logger.info(f"Tool output {i+1}: {to.get('tool_name', 'unknown')} with content: {content_preview}")
                    except Exception as e:
                        logger.warning(f"Error logging tool output: {str(e)}")
            else:
                logger.info("No tool outputs found in the result")
            
            # Store assistant response in database if we have a MessageHistory object
            if message_history_obj:
                logger.info(f"Adding assistant response to MessageHistory in the database")
                
                # Extract the response content
                response_content = result.data
                
                # Make sure tool_calls and tool_outputs are in the right format for storage
                formatted_tool_calls = []
                formatted_tool_outputs = []
                
                # Format tool calls for storage
                if tool_calls:
                    for tc in tool_calls:
                        formatted_tc = {
                            'tool_name': tc.get('tool_name', ''),
                            'args': tc.get('args', {}),
                            'tool_call_id': tc.get('tool_call_id', '')
                        }
                        formatted_tool_calls.append(formatted_tc)
                
                # Format tool outputs for storage, ensuring content is properly serializable
                if tool_outputs:
                    for to in tool_outputs:
                        content = to.get('content', '')
                        # Ensure content is JSON serializable
                        if not isinstance(content, (str, dict, list, int, float, bool, type(None))):
                            try:
                                # Try to convert to a string representation
                                content = str(content)
                            except Exception as e:
                                logger.warning(f"Could not convert tool output content to string: {str(e)}")
                                content = f"[Unserializable content of type {type(content).__name__}]"
                        
                        formatted_to = {
                            'tool_name': to.get('tool_name', ''),
                            'content': content,
                            'tool_call_id': to.get('tool_call_id', '')
                        }
                        formatted_tool_outputs.append(formatted_to)
                
                # Store in database with properly formatted tool calls/outputs and filled system prompt
                message_history_obj.add_response(
                    content=response_content,
                    tool_calls=formatted_tool_calls if formatted_tool_calls else None,
                    tool_outputs=formatted_tool_outputs if formatted_tool_outputs else None,
                    agent_id=getattr(self, "db_id", None),
                    system_prompt=filled_system_prompt  # Use the filled system prompt we already have
                )
            
            # Create response with the tool calls and outputs
            return AgentResponse(
                text=result.data,
                success=True,
                tool_calls=tool_calls,
                tool_outputs=tool_outputs,
                raw_message=result.all_messages() if hasattr(result, "all_messages") else None
            )
        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            logger.error(traceback.format_exc())
            return AgentResponse(
                text="An error occurred while processing your request.",
                success=False,
                error_message=str(e)
            )
    
    def _configure_for_multimodal(self, input_text: str, multimodal_content: Dict[str, Any]) -> List[Any]:
        """Configure the agent input for multimodal content.
        
        Args:
            input_text: The text input from the user
            multimodal_content: Dictionary of multimodal content
            
        Returns:
            List containing text and multimodal content objects
        """
            
        result = [input_text]
        
        # Process different content types
        for content_type, content in multimodal_content.items():
            if content_type == "image":
                if isinstance(content, str) and (content.startswith("http://") or content.startswith("https://")):
                    result.append(ImageUrl(url=content))
                else:
                    result.append(BinaryContent(data=content, media_type="image/jpeg"))
            elif content_type == "audio":
                if isinstance(content, str) and (content.startswith("http://") or content.startswith("https://")):
                    result.append(AudioUrl(url=content))
                else:
                    result.append(BinaryContent(data=content, media_type="audio/mp3"))
            elif content_type == "document":
                if isinstance(content, str) and (content.startswith("http://") or content.startswith("https://")):
                    result.append(DocumentUrl(url=content))
                else:
                    result.append(BinaryContent(data=content, media_type="application/pdf"))
            else:
                logger.warning(f"Unsupported content type: {content_type}")
                
        return result
    
    async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[Union[int, str]] = None, user_id: int = 1, context: Optional[Dict] = None, message_history: Optional['MessageHistory'] = None) -> AgentResponse:
        """Process a user message with this agent.
        
        Args:
            user_message: User message to process
            session_id: Optional session ID
            agent_id: Optional agent ID for database tracking
            user_id: User ID
            context: Optional additional context
            message_history: Optional MessageHistory object
            
        Returns:
            Agent response
        """
        # Set session and user info in dependencies
        if session_id:
            self.dependencies.session_id = session_id
        self.dependencies.user_id = user_id
        logger.info(f"Processing message from user {user_id} with session {session_id}")
        
        # If agent_id is provided and different from the current db_id, update it
        agent_id_updated = False
        if agent_id and str(agent_id) != str(getattr(self, "db_id", None)):
            self.db_id = int(agent_id) if isinstance(agent_id, (str, int)) and str(agent_id).isdigit() else agent_id
            self.dependencies.set_agent_id(self.db_id)
            logger.info(f"Updated agent ID to {self.db_id}")
            agent_id_updated = True
            
            # Initialize memory variables if they haven't been initialized yet
            if agent_id_updated and self.template_vars:
                try:
                    # Pass user_id to memory initialization
                    self._initialize_memory_variables_sync(user_id)
                    logger.info(f"Memory variables initialized for agent ID {self.db_id} and user ID {user_id}")
                except Exception as e:
                    logger.error(f"Error initializing memory variables: {str(e)}")
        
        # Check and ensure memory variables for this user explicitly
        if self.db_id and self.template_vars:
            try:
                self._check_and_ensure_memory_variables(user_id)
                logger.info(f"Checked and ensured memory variables for user {user_id}")
            except Exception as e:
                logger.error(f"Error checking memory variables: {str(e)}")
        
        # Extract multimodal content from context
        multimodal_content = None
        if context and "multimodal_content" in context:
            multimodal_content = context["multimodal_content"]
        
        # If message_history is provided, store user message in database
        # but don't try to handle system messages from database
        if message_history:
            logger.info(f"Using provided MessageHistory for session {session_id} to store user message")
            # Add user message to database (but not system message)
            message_history.add(user_message, agent_id=self.db_id, context=context)
            
            # Get messages to pass to PydanticAI
            all_messages = message_history.all_messages()
            logger.info(f"Retrieved {len(all_messages) if all_messages else 0} messages from message history")
            
            # Filter out previous tool calls and returns to avoid compatibility issues
            # with PydanticAI's message history processing
            from pydantic_ai.messages import ModelRequest, ModelResponse, SystemPromptPart, UserPromptPart, TextPart
            
            filtered_messages = []
            for msg in all_messages:
                # Keep system messages and user messages intact
                if isinstance(msg, ModelRequest):
                    has_system_part = False
                    for part in msg.parts:
                        if hasattr(part, 'part_kind') and part.part_kind == 'system-prompt':
                            has_system_part = True
                            break
                    
                    if has_system_part:
                        # System message - keep as is
                        filtered_messages.append(msg)
                    else:
                        # User message - keep as is
                        filtered_messages.append(msg)
                elif isinstance(msg, ModelResponse):
                    # For assistant messages, only keep the text content parts
                    # to avoid issues with tool calls/returns in history
                    text_parts = []
                    for part in msg.parts:
                        if hasattr(part, 'part_kind') and part.part_kind == 'text':
                            text_parts.append(part)
                    
                    # Only add if we have some text parts
                    if text_parts:
                        filtered_messages.append(ModelResponse(parts=text_parts))
                else:
                    # Unknown message type, add as is
                    filtered_messages.append(msg)
            
            # Update message history in dependencies with filtered messages
            self.dependencies.set_message_history(filtered_messages)
            logger.info(f"Set filtered message history in dependencies with {len(filtered_messages)} messages (stripped tool parts)")
        else:
            logger.info(f"No MessageHistory provided, will not store messages in database")
        
        # Reinitialize the agent if needed to use updated config
        if agent_id_updated:
            # Force agent to reinitialize with new ID
            self._agent_instance = None
            logger.info(f"Agent will be reinitialized with updated ID {self.db_id}")
        
        logger.info(f"Processing message for agent {self.db_id} with dynamic system prompts from template")
        
        # Run the agent with the MessageHistory object for database storage
        # but don't pass any system_message as we'll use our template
        logger.info(f"message_history: {message_history}")
        return await self.run(
            user_message, 
            multimodal_content=multimodal_content,
            message_history_obj=message_history
        )

    async def _handle_memory_variables(self, template: str) -> str:
        """Replace memory variable references with actual memory contents.
        
        Args:
            template: String containing memory variable references
            
        Returns:
            Template with variables replaced with their values
        """
        memory_var_pattern = r'\$memory\.([a-zA-Z0-9_]+)'
        memory_vars = re.findall(memory_var_pattern, template)
        
        if not memory_vars:
            return template
            
        # Create a copy of the template to modify
        result = template
        template_values = {}
        
        _import_memory_tools()
        for var_name in memory_vars:
            try:
                # Make sure context has the latest user_id and agent_id
                user_id = getattr(self.dependencies, 'user_id', None)
                if hasattr(self, 'context'):
                    self.context.update({
                        "agent_id": self.db_id,
                        "user_id": user_id
                    })
                else:
                    self.context = {"agent_id": self.db_id, "user_id": user_id}
                
                # Use get_memory_tool to get memory content - pass context but not separate user_id to avoid duplicates
                response = await get_memory_tool(self.context, var_name)
                
                if isinstance(response, dict):
                    if 'success' in response and response['success'] and 'content' in response:
                        memory_content = response['content']
                    elif 'error' in response:
                        memory_content = f"[Memory Error: {response['error']}]"
                    else:
                        memory_content = str(response)
                else:
                    memory_content = str(response)
                
                template_values[var_name] = memory_content
            except Exception as e:
                logger.error(f"Error retrieving memory '{var_name}': {str(e)}")
                template_values[var_name] = f"[Memory Error: {str(e)}]"
        
        # Replace all memory references with their values
        for var_name, value in template_values.items():
            result = result.replace(f"$memory.{var_name}", value)
            
        return result

    def _get_current_system_prompt(self) -> str:
        """Retrieve the current system prompt with template variables replaced.
        
        Returns the filled system prompt from our template variables.
        
        Returns:
            The current system prompt with all template variables filled
        """
        try:
            # Get the filled system prompt directly
            return asyncio.run(self._get_filled_system_prompt())
        except Exception as e:
            logger.error(f"Error in _get_current_system_prompt: {str(e)}")
            return self.prompt_template

    def dependencies_to_message_history(self) -> None:
        """Ensure dependencies message history includes the system prompt.
        
        When using existing dependencies for message history,
        we need to manually ensure the system prompt is included as the first message.
        This is handled in the run method.
        """
        # The system prompt is manually added in the run method
        # See the run method for implementation
        pass

    async def _get_filled_system_prompt(self) -> str:
        """Get the system prompt with all template variables filled.
        
        This is a helper method for testing purposes that directly fills in the
        template variables in the system prompt, similar to what the dynamic
        system prompt decorator would do.
        
        Returns:
            System prompt with all template variables filled
        """
        # Make sure memory tools are imported
        _import_memory_tools()
        
        # Get user_id from dependencies if available
        user_id = getattr(self.dependencies, 'user_id', None)
        
        # Update context with user_id and agent_id
        if hasattr(self, 'context'):
            self.context.update({
                "agent_id": self.db_id,
                "user_id": user_id
            })
            logger.info(f"Updated context for memory tools: agent_id={self.db_id}, user_id={user_id}")
        else:
            # Create context if it doesn't exist
            self.context = {"agent_id": self.db_id, "user_id": user_id}
            logger.info(f"Created new context for memory tools: agent_id={self.db_id}, user_id={user_id}")
        
        # Start with template values dictionary
        template_values = {}
        
        # Get run_id value
        if self.db_id:
            try:
                from src.db.repository import increment_agent_run_id, get_agent
                # Get current value without incrementing (we'll increment in the decorator)
                agent = get_agent(self.db_id)
                if agent and hasattr(agent, 'run_id'):
                    template_values["run_id"] = str(agent.run_id)
                else:
                    template_values["run_id"] = "1"
            except Exception as e:
                logger.error(f"Error getting run_id: {str(e)}")
                template_values["run_id"] = "1"
        else:
            template_values["run_id"] = "1"
        
        # Get system prompt memory variables directly from the repository
        memory_vars = [var for var in self.template_vars if var != "run_id"]
        try:
            # Import repository function for direct database access to system prompt memories
            from src.db.repository.memory import list_memories
            
            # Get all memories with read_mode='system_prompt' for this agent and user
            system_memories = list_memories(
                agent_id=self.db_id,
                user_id=user_id,
                read_mode="system_prompt"
            )
            
            # Create a dictionary of memory name to content
            memory_dict = {mem.name: mem.content for mem in system_memories}
            logger.info(f"Retrieved {len(memory_dict)} system_prompt memories: {', '.join(memory_dict.keys())}")
            
            # Fill in template values with memory content
            for var_name in memory_vars:
                if var_name in memory_dict:
                    template_values[var_name] = memory_dict[var_name]
                    logger.info(f"Using system_prompt memory for {var_name}: {memory_dict[var_name][:50]}...")
                else:
                    # Fallback to regular memory tool if not found
                    try:
                        # Make sure context has up-to-date user_id
                        context_copy = dict(self.context) if hasattr(self, 'context') and self.context else {}
                        if user_id:
                            context_copy["user_id"] = user_id
                        
                        memory_content = await get_memory_tool(context_copy, var_name)
                        
                        if memory_content and not memory_content.startswith("Memory with key"):
                            template_values[var_name] = memory_content
                            logger.info(f"Using regular memory for {var_name}: {memory_content[:50]}...")
                        else:
                            template_values[var_name] = "None stored yet"
                            logger.info(f"No memory found for {var_name}, using default")
                    except Exception as e:
                        logger.error(f"Error getting memory for {var_name}: {str(e)}")
                        template_values[var_name] = "None stored yet"
        except Exception as e:
            logger.error(f"Error accessing system memories: {str(e)}")
            # Fall back to regular memory tool if repository access fails
            for var_name in memory_vars:
                try:
                    # Make sure context has up-to-date user_id
                    context_copy = dict(self.context) if hasattr(self, 'context') and self.context else {}
                    if user_id:
                        context_copy["user_id"] = user_id
                    
                    memory_content = await get_memory_tool(context_copy, var_name)
                    
                    if memory_content and not memory_content.startswith("Memory with key"):
                        template_values[var_name] = memory_content
                    else:
                        template_values[var_name] = "None stored yet"
                except Exception as e:
                    logger.error(f"Error getting memory for {var_name}: {str(e)}")
                    template_values[var_name] = "None stored yet"
        
        # Now fill the template
        prompt_template = self.prompt_template
        for var_name, value in template_values.items():
            placeholder = f"{{{{{var_name}}}}}"
            prompt_template = prompt_template.replace(placeholder, value)
        
        logger.info(f"Filled system prompt with {len(template_values)} template variables")
        return prompt_template 
```

# src/agents/simple/simple_agent/prompts/__init__.py

```py
from .prompt import SIMPLE_AGENT_PROMPT

__all__ = [
    'SIMPLE_AGENT_PROMPT'
] 
```

# src/agents/simple/simple_agent/prompts/prompt.py

```py
SIMPLE_AGENT_PROMPT = (
"""
DEBUG MODE, YOUR NAME IS TESTONHO, if the user asks about your name, you should say "TESTONHO"
# Simple Agent with Memory

## System Role
You are an Agent, a versatile assistant with memory capabilities. You have access to a persistent memory store that allows you to recall information across conversations. Your primary purpose is to demonstrate the capabilities of the pydantic-ai framework while providing helpful assistance.

Current memory ID: {{run_id}}

## Core Capabilities
- **Memory**: Can store and retrieve information across sessions
- **Function Tools**: Uses specialized tools to perform tasks
- **Multimodal Processing**: Can understand and process text, images, audio, and documents
- **Contextual Understanding**: Can maintain context through conversation history

## Primary Responsibilities
1. **Information Retrieval**: Access stored memories to provide consistent responses
2. **Memory Management**: Store new information when requested
3. **Tool Usage**: Utilize function tools efficiently to accomplish tasks
4. **Multimodal Interaction**: Process various input types including text, images, and documents

## Communication Style
- **Clear and Concise**: Provide direct and relevant information
- **Helpful**: Always attempt to assist with user requests
- **Contextual**: Maintain and utilize conversation context
- **Memory-Aware**: Leverage stored memories when relevant to the conversation

## Technical Knowledge
- You have access to the following memory attributes:
  - {{personal_attributes}}
  - {{technical_knowledge}}
  - {{user_preferences}}

## Operational Guidelines
1. When asked about previous conversations, use memory retrieval tools
2. When encountering new information that may be useful later, suggest storing it
3. When processing multimodal inputs, describe what you observe before responding
4. When you're unsure about something, check memory before stating you don't know

Remember that you exist to demonstrate modern agent capabilities using pydantic-ai while providing helpful assistance to users.
"""
) 
```

# src/api/__init__.py

```py
"""API package for the Automagik Agents service.

This package contains the API models, routes, and documentation endpoints.
"""

# Empty init file to mark the directory as a Python package 
```

# src/api/docs.py

```py
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi

# Create docs router (no auth required)
router = APIRouter()

@router.get("/api/v1/docs", include_in_schema=False)
async def custom_docs():
    """Swagger UI documentation endpoint."""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI - Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            const ui = SwaggerUIBundle({
                url: '/api/v1/openapi.json',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout",
                deepLinking: true,
                displayRequestDuration: true,
                filter: true
            });
        </script>
    </body>
    </html>
    """)

@router.get("/api/v1/redoc", include_in_schema=False)
async def custom_redoc():
    """ReDoc documentation endpoint."""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI - ReDoc</title>
        <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <div id="redoc"></div>
        <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
        <script>
            Redoc.init('/api/v1/openapi.json', {}, document.getElementById('redoc'));
        </script>
    </body>
    </html>
    """)

@router.get("/api/v1/openapi.json", include_in_schema=False)
async def get_openapi_json(request: Request):
    """OpenAPI schema endpoint."""
    # Get the app from the request
    app = request.app
    
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add API Key security scheme
    openapi_schema["components"] = openapi_schema.get("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key",
            "description": "API key authentication"
        },
        "APIKeyQuery": {
            "type": "apiKey",
            "in": "query",
            "name": "x-api-key",
            "description": "API key authentication via query parameter"
        }
    }
    
    # Apply security to all endpoints except those that don't need auth
    security_requirement = [{"APIKeyHeader": []}, {"APIKeyQuery": []}]
    no_auth_paths = ["/", "/health", "/api/v1/docs", "/api/v1/redoc", "/api/v1/openapi.json"]
    
    # Update the schema to use /api/v1 prefix in the OpenAPI docs
    paths = {}
    for path, path_item in openapi_schema["paths"].items():
        if not path.startswith("/api/v1") and path not in ["/", "/health"]:
            continue
        
        # Add security requirement to protected endpoints
        if path not in no_auth_paths:
            for operation in path_item.values():
                operation["security"] = security_requirement
                
                # Add authentication description to each endpoint
                if "description" in operation:
                    operation["description"] += "\n\n**Requires Authentication**: This endpoint requires an API key."
                else:
                    operation["description"] = "**Requires Authentication**: This endpoint requires an API key."
        
        paths[path] = path_item
        
    openapi_schema["paths"] = paths
    
    # Apply global security if needed (alternative approach)
    # openapi_schema["security"] = security_requirement
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema 
```

# src/api/memory_models.py

```py
from datetime import datetime
from typing import Dict, Any, Optional, List
from uuid import UUID
from pydantic import BaseModel, Field

class MemoryCreate(BaseModel):
    name: str = Field(..., description="Name of the memory")
    description: Optional[str] = Field(None, description="Description of the memory")
    content: str = Field(..., description="Content of the memory")
    session_id: Optional[str] = Field(None, description="Associated session ID - can be a UUID string or None")
    user_id: Optional[int] = Field(None, description="Associated user ID")
    agent_id: Optional[int] = Field(None, description="Associated agent ID")
    read_mode: Optional[str] = Field(None, description="Read mode of the memory (e.g., system_prompt, tool_call)")
    access: Optional[str] = Field(None, description="Access permissions of the memory (e.g., read, write)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the memory")

class MemoryUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the memory")
    description: Optional[str] = Field(None, description="Description of the memory")
    content: Optional[str] = Field(None, description="Content of the memory")
    session_id: Optional[str] = Field(None, description="Associated session ID - can be a UUID string or None")
    user_id: Optional[int] = Field(None, description="Associated user ID")
    agent_id: Optional[int] = Field(None, description="Associated agent ID")
    read_mode: Optional[str] = Field(None, description="Read mode of the memory (e.g., system_prompt, tool_call)")
    access: Optional[str] = Field(None, description="Access permissions of the memory (e.g., read, write)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the memory")

class MemoryResponse(BaseModel):
    id: UUID = Field(..., description="Memory ID")
    name: str = Field(..., description="Name of the memory")
    description: Optional[str] = Field(None, description="Description of the memory")
    content: str = Field(..., description="Content of the memory")
    session_id: Optional[str] = Field(None, description="Associated session ID - can be a UUID string or None")
    user_id: Optional[int] = Field(None, description="Associated user ID")
    agent_id: Optional[int] = Field(None, description="Associated agent ID")
    read_mode: Optional[str] = Field(None, description="Read mode of the memory")
    access: Optional[str] = Field(None, description="Access permissions of the memory")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the memory")
    created_at: datetime = Field(..., description="Memory creation timestamp")
    updated_at: datetime = Field(..., description="Memory update timestamp")

class MemoryListResponse(BaseModel):
    memories: List[MemoryResponse] = Field(..., description="List of memories")
    count: int = Field(..., description="Total count of memories")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of memories per page")
    pages: int = Field(..., description="Total number of pages")

```

# src/api/memory_routes.py

```py
import logging
import json
import math
import uuid
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List

from src.api.memory_models import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse,
    MemoryListResponse
)
from src.db import (
    Memory, 
    get_memory, 
    create_memory as repo_create_memory,
    update_memory as repo_update_memory,
    list_memories as repo_list_memories,
    delete_memory as repo_delete_memory,
    execute_query
)
from src.config import settings
from src.memory.message_history import MessageHistory

# Create API router for memory endpoints
memory_router = APIRouter()

# Get our module's logger
logger = logging.getLogger(__name__)

# Validate UUID helper function (duplicated from routes.py for modularity)
def is_valid_uuid(value: str) -> bool:
    """Check if a string is a valid UUID.
    
    Args:
        value: The string to check
        
    Returns:
        True if the string is a valid UUID, False otherwise
    """
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False

@memory_router.get("/memories", response_model=MemoryListResponse, tags=["Memories"],
            summary="List Memories",
            description="List all memories with optional filters and pagination.")
async def list_memories(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    agent_id: Optional[int] = Query(None, description="Filter by agent ID"),
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    page: int = Query(1, description="Page number (1-based)"),
    page_size: int = Query(50, description="Number of memories per page"),
    sort_desc: bool = Query(True, description="Sort by most recent first if True")
):
    # Validate and parse session_id as UUID if provided
    session_uuid = None
    if session_id:
        try:
            session_uuid = uuid.UUID(session_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid session_id format: {session_id}")
    
    # Use the repository pattern to list memories
    memories = repo_list_memories(
        agent_id=agent_id,
        user_id=user_id,
        session_id=session_uuid
    )
    
    # Total number of memories
    total_count = len(memories)
    
    # Calculate total pages
    total_pages = math.ceil(total_count / page_size)
    
    # Apply sorting
    if sort_desc:
        memories.sort(key=lambda x: x.created_at or datetime.min, reverse=True)
    else:
        memories.sort(key=lambda x: x.created_at or datetime.min)
    
    # Apply pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_memories = memories[start_idx:end_idx]
    
    # Convert to response format
    memory_responses = []
    for memory in paginated_memories:
        memory_responses.append({
            "id": str(memory.id),
            "name": memory.name,
            "description": memory.description,
            "content": memory.content,
            "session_id": str(memory.session_id) if memory.session_id else None,
            "user_id": memory.user_id,
            "agent_id": memory.agent_id,
            "read_mode": memory.read_mode,
            "access": memory.access,
            "metadata": memory.metadata,
            "created_at": memory.created_at,
            "updated_at": memory.updated_at
        })
    
    return {
        "items": memory_responses,
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages
    }

@memory_router.post("/memories", response_model=MemoryResponse, tags=["Memories"],
             summary="Create Memory",
             description="Create a new memory with the provided details.")
async def create_memory(memory: MemoryCreate):
    try:
        # Convert session_id to UUID if provided
        session_uuid = None
        if memory.session_id:
            try:
                session_uuid = uuid.UUID(memory.session_id)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid session_id format: {memory.session_id}")
        
        # Create a Memory model for the repository
        memory_model = Memory(
            id=None,  # Will be generated
            name=memory.name,
            description=memory.description,
            content=memory.content,
            session_id=session_uuid,
            user_id=memory.user_id,
            agent_id=memory.agent_id,
            read_mode=memory.read_mode,
            access=memory.access,
            metadata=memory.metadata,
            created_at=None,  # Will be set by DB
            updated_at=None   # Will be set by DB
        )
        
        # Create the memory using the repository
        memory_id = repo_create_memory(memory_model)
        
        if memory_id is None:
            raise HTTPException(status_code=500, detail="Failed to create memory")
        
        # Retrieve the created memory to get all fields
        created_memory = get_memory(memory_id)
        
        if not created_memory:
            raise HTTPException(status_code=404, detail=f"Memory created but not found with ID {memory_id}")
        
        # Convert to response format
        return {
            "id": str(created_memory.id),
            "name": created_memory.name,
            "description": created_memory.description,
            "content": created_memory.content,
            "session_id": str(created_memory.session_id) if created_memory.session_id else None,
            "user_id": created_memory.user_id,
            "agent_id": created_memory.agent_id,
            "read_mode": created_memory.read_mode,
            "access": created_memory.access,
            "metadata": created_memory.metadata,
            "created_at": created_memory.created_at,
            "updated_at": created_memory.updated_at
        }
    except Exception as e:
        logger.error(f"Error creating memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating memory: {str(e)}")

@memory_router.post("/memories/batch", response_model=List[MemoryResponse], tags=["Memories"],
             summary="Create Multiple Memories",
             description="Create multiple memories in a single batch operation.")
async def create_memories_batch(memories: List[MemoryCreate]):
    try:
        results = []
        
        for memory in memories:
            try:
                # Convert session_id to UUID if provided
                session_uuid = None
                if memory.session_id:
                    try:
                        session_uuid = uuid.UUID(memory.session_id)
                    except ValueError:
                        logger.warning(f"Invalid session_id format in batch: {memory.session_id}")
                        # Skip invalid UUIDs but continue with the operation
                        pass
                
                # Create a Memory model for the repository
                memory_model = Memory(
                    id=None,  # Will be generated
                    name=memory.name,
                    description=memory.description,
                    content=memory.content,
                    session_id=session_uuid,
                    user_id=memory.user_id,
                    agent_id=memory.agent_id,
                    read_mode=memory.read_mode,
                    access=memory.access,
                    metadata=memory.metadata,
                    created_at=None,  # Will be set by DB
                    updated_at=None   # Will be set by DB
                )
                
                # Create the memory using the repository
                memory_id = repo_create_memory(memory_model)
                
                if memory_id is None:
                    logger.warning(f"Failed to create memory in batch: {memory.name}")
                    continue
                
                # Retrieve the created memory to get all fields
                created_memory = get_memory(memory_id)
                
                if not created_memory:
                    logger.warning(f"Memory created but not found with ID {memory_id}")
                    continue
                
                # Add to results
                results.append(MemoryResponse(
                    id=str(created_memory.id),
                    name=created_memory.name,
                    description=created_memory.description,
                    content=created_memory.content,
                    session_id=str(created_memory.session_id) if created_memory.session_id else None,
                    user_id=created_memory.user_id,
                    agent_id=created_memory.agent_id,
                    read_mode=created_memory.read_mode,
                    access=created_memory.access,
                    metadata=created_memory.metadata,
                    created_at=created_memory.created_at,
                    updated_at=created_memory.updated_at
                ))
            except Exception as e:
                # Log error but continue with other memories
                logger.error(f"Error creating memory in batch: {str(e)}")
                continue
        
        # Return all successfully created memories
        return results
    except Exception as e:
        logger.error(f"Error creating memories in batch: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating memories in batch: {str(e)}")

@memory_router.get("/memories/{memory_id}", response_model=MemoryResponse, tags=["Memories"],
            summary="Get Memory",
            description="Get a memory by its ID.")
async def get_memory_endpoint(memory_id: str = Path(..., description="The memory ID")):
    try:
        # Validate UUID format
        try:
            uuid_obj = uuid.UUID(memory_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid memory ID format: {memory_id}")
        
        # Query the database using the repository function
        # The repository get_memory function is synchronous, so no need to await
        memory = get_memory(uuid_obj)
        
        if not memory:
            raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
        
        # Return the memory response
        return MemoryResponse(
            id=str(memory.id),
            name=memory.name,
            description=memory.description,
            content=memory.content,
            session_id=str(memory.session_id) if memory.session_id else None,
            user_id=memory.user_id,
            agent_id=memory.agent_id,
            read_mode=memory.read_mode,
            access=memory.access,
            metadata=memory.metadata,
            created_at=memory.created_at,
            updated_at=memory.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving memory: {str(e)}")

@memory_router.put("/memories/{memory_id}", response_model=MemoryResponse, tags=["Memories"],
            summary="Update Memory",
            description="Update an existing memory with the provided details.")
async def update_memory_endpoint(
    memory_update: MemoryUpdate,
    memory_id: str = Path(..., description="The memory ID")
):
    try:
        # Validate UUID format
        try:
            uuid_obj = uuid.UUID(memory_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid memory ID format: {memory_id}")
        
        # Check if memory exists using repository function
        existing_memory = get_memory(uuid_obj)
        
        if not existing_memory:
            raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
        
        # Update existing memory with new values
        if memory_update.name is not None:
            existing_memory.name = memory_update.name
            
        if memory_update.description is not None:
            existing_memory.description = memory_update.description
            
        if memory_update.content is not None:
            existing_memory.content = memory_update.content
            
        if memory_update.session_id is not None:
            try:
                if isinstance(memory_update.session_id, str):
                    existing_memory.session_id = uuid.UUID(memory_update.session_id)
                else:
                    existing_memory.session_id = memory_update.session_id
            except ValueError:
                # If not a valid UUID, store as None
                existing_memory.session_id = None
                
        if memory_update.user_id is not None:
            existing_memory.user_id = memory_update.user_id
            
        if memory_update.agent_id is not None:
            existing_memory.agent_id = memory_update.agent_id
            
        if memory_update.read_mode is not None:
            existing_memory.read_mode = memory_update.read_mode
            
        if memory_update.access is not None:
            existing_memory.access = memory_update.access
            
        if memory_update.metadata is not None:
            existing_memory.metadata = memory_update.metadata
        
        # Update the memory using repository function
        updated_memory_id = repo_update_memory(existing_memory)
        
        if not updated_memory_id:
            raise HTTPException(status_code=500, detail="Failed to update memory")
        
        # Get the updated memory
        updated_memory = get_memory(uuid_obj)
        
        # Return the updated memory
        return MemoryResponse(
            id=str(updated_memory.id),
            name=updated_memory.name,
            description=updated_memory.description,
            content=updated_memory.content,
            session_id=str(updated_memory.session_id) if updated_memory.session_id else None,
            user_id=updated_memory.user_id,
            agent_id=updated_memory.agent_id,
            read_mode=updated_memory.read_mode,
            access=updated_memory.access,
            metadata=updated_memory.metadata,
            created_at=updated_memory.created_at,
            updated_at=updated_memory.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating memory: {str(e)}")

@memory_router.delete("/memories/{memory_id}", response_model=MemoryResponse, tags=["Memories"],
               summary="Delete Memory",
               description="Delete a memory by its ID.")
async def delete_memory_endpoint(memory_id: str = Path(..., description="The memory ID")):
    try:
        # Validate UUID format
        try:
            uuid_obj = uuid.UUID(memory_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid memory ID format: {memory_id}")
        
        # Get the memory for response before deletion
        existing_memory = get_memory(uuid_obj)
        
        if not existing_memory:
            raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
        
        # Create memory response before deletion
        memory_response = MemoryResponse(
            id=str(existing_memory.id),
            name=existing_memory.name,
            description=existing_memory.description,
            content=existing_memory.content,
            session_id=str(existing_memory.session_id) if existing_memory.session_id else None,
            user_id=existing_memory.user_id,
            agent_id=existing_memory.agent_id,
            read_mode=existing_memory.read_mode,
            access=existing_memory.access,
            metadata=existing_memory.metadata,
            created_at=existing_memory.created_at,
            updated_at=existing_memory.updated_at
        )
        
        # Delete the memory using repository function
        success = repo_delete_memory(uuid_obj)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete memory")
        
        # Return the deleted memory details
        return memory_response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting memory: {str(e)}")

```

# src/api/models.py

```py
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Literal
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class BaseResponseModel(BaseModel):
    """Base model for all response models with common configuration."""
    model_config = ConfigDict(
        exclude_none=True,  # Exclude None values from response
        validate_assignment=True,  # Validate values on assignment
        extra='ignore'  # Ignore extra fields
    )

# Multimodal content models
class MediaContent(BaseResponseModel):
    """Base model for media content."""
    mime_type: str
    
class UrlMediaContent(MediaContent):
    """Media content accessible via URL."""
    media_url: str

class BinaryMediaContent(MediaContent):
    """Media content with binary data."""
    data: str  # Base64 encoded binary data
    
class ImageContent(MediaContent):
    """Image content with metadata."""
    mime_type: str = Field(pattern=r'^image/')
    width: Optional[int] = None
    height: Optional[int] = None
    alt_text: Optional[str] = None
    
class ImageUrlContent(ImageContent, UrlMediaContent):
    """Image content accessible via URL."""
    pass
    
class ImageBinaryContent(ImageContent, BinaryMediaContent):
    """Image content with binary data."""
    thumbnail_url: Optional[str] = None
    
class AudioContent(MediaContent):
    """Audio content with metadata."""
    mime_type: str = Field(pattern=r'^audio/')
    duration_seconds: Optional[float] = None
    transcript: Optional[str] = None
    
class AudioUrlContent(AudioContent, UrlMediaContent):
    """Audio content accessible via URL."""
    pass
    
class AudioBinaryContent(AudioContent, BinaryMediaContent):
    """Audio content with binary data."""
    pass
    
class DocumentContent(MediaContent):
    """Document content with metadata."""
    mime_type: str = Field(pattern=r'^(application|text)/')
    name: Optional[str] = None
    size_bytes: Optional[int] = None
    page_count: Optional[int] = None
    
class DocumentUrlContent(DocumentContent, UrlMediaContent):
    """Document content accessible via URL."""
    pass
    
class DocumentBinaryContent(DocumentContent, BinaryMediaContent):
    """Document content with binary data."""
    pass

# Update AgentRunRequest to support multimodal content
class AgentRunRequest(BaseResponseModel):
    """Request model for running an agent."""
    message_content: str
    message_type: Optional[str] = None
    # Legacy single media fields (maintained for backward compatibility)
    mediaUrl: Optional[str] = None
    mime_type: Optional[str] = None
    # New multimodal content support
    media_contents: Optional[List[Union[
        ImageUrlContent, ImageBinaryContent,
        AudioUrlContent, AudioBinaryContent,
        DocumentUrlContent, DocumentBinaryContent
    ]]] = None
    channel_payload: Optional[Dict[str, Any]] = None
    context: dict = {}
    session_id: Optional[str] = None
    session_name: Optional[str] = None  # Optional friendly name for the session
    user_id: Optional[int] = 1  # User ID is now an integer with default value 1
    message_limit: Optional[int] = 10  # Default to last 10 messages
    session_origin: Optional[str] = "automagik-agent"
    agent_id: Optional[Any] = None  # Agent ID to store with messages, can be int or string
    preserve_system_prompt: Optional[bool] = False  # Whether to preserve the existing system prompt

class AgentInfo(BaseResponseModel):
    """Information about an available agent."""
    name: str
    type: str
    model: Optional[str] = None
    description: Optional[str] = None

class HealthResponse(BaseResponseModel):
    """Response model for health check endpoint."""
    status: str
    timestamp: datetime
    version: str
    environment: str = "development"  # Default to development if not specified

class DeleteSessionResponse(BaseResponseModel):
    """Response model for session deletion."""
    status: str
    session_id: str
    message: str

class ToolCallModel(BaseResponseModel):
    """Model for a tool call."""
    tool_name: str
    args: Dict
    tool_call_id: str

class ToolOutputModel(BaseResponseModel):
    """Model for a tool output."""
    tool_name: str
    tool_call_id: str
    content: Any

class MessageModel(BaseResponseModel):
    """Model for a single message in the conversation."""
    role: str
    content: str
    assistant_name: Optional[str] = None
    # Legacy media fields (maintained for backward compatibility)
    media_url: Optional[str] = None
    mime_type: Optional[str] = None
    # New multimodal content support
    media_contents: Optional[List[Union[
        ImageUrlContent, ImageBinaryContent, 
        AudioUrlContent, AudioBinaryContent,
        DocumentUrlContent, DocumentBinaryContent
    ]]] = None
    tool_calls: Optional[List[ToolCallModel]] = None
    tool_outputs: Optional[List[ToolOutputModel]] = None

    model_config = ConfigDict(
        exclude_none=True,
        json_schema_extra={"examples": [{"role": "assistant", "content": "Hello!"}]}
    )

class PaginationParams(BaseResponseModel):
    """Pagination parameters."""
    page: int = 1
    page_size: int = 50
    sort_desc: bool = True  # True for most recent first

class SessionResponse(BaseResponseModel):
    """Response model for session retrieval."""
    session_id: str
    messages: List[MessageModel]
    exists: bool
    total_messages: int
    current_page: int
    total_pages: int

class SessionInfo(BaseResponseModel):
    """Information about a session."""
    session_id: str
    user_id: Optional[int] = None
    agent_id: Optional[int] = None
    session_name: Optional[str] = None
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    message_count: Optional[int] = None
    agent_name: Optional[str] = None
    session_origin: Optional[str] = None  # Origin of the session (e.g., "web", "api", "discord")

class SessionListResponse(BaseResponseModel):
    """Response model for listing all sessions."""
    sessions: List[SessionInfo]
    total_count: int
    page: int = 1
    page_size: int = 50
    total_pages: int = 1

class UserCreate(BaseResponseModel):
    """Request model for creating a new user."""
    email: Optional[str] = None
    phone_number: Optional[str] = None
    user_data: Optional[Dict[str, Any]] = None

class UserUpdate(BaseResponseModel):
    """Request model for updating an existing user."""
    email: Optional[str] = None
    phone_number: Optional[str] = None
    user_data: Optional[Dict[str, Any]] = None

class UserInfo(BaseResponseModel):
    """Response model for user information."""
    id: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    user_data: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserListResponse(BaseResponseModel):
    """Response model for listing users."""
    users: List[UserInfo]
    total_count: int
    page: int = 1
    page_size: int = 50
    total_pages: int = 1 
```

# src/api/routes.py

```py
import logging
from datetime import datetime
from typing import List, Optional
import json
import math
import uuid
import inspect

from fastapi import APIRouter, HTTPException, Query, Path, Depends, Response
from starlette.responses import JSONResponse
from src.agents.models.agent_factory import AgentFactory
from src.config import settings
from src.memory.message_history import MessageHistory
from src.api.models import (
    AgentRunRequest,
    AgentInfo,
    DeleteSessionResponse,
    MessageModel,
    SessionResponse,
    SessionListResponse,
    SessionInfo,
    UserCreate,
    UserUpdate,
    UserInfo,
    UserListResponse
)

# Import memory router
from src.api.memory_routes import memory_router
from src.db import execute_query, get_db_connection, get_user_by_identifier, list_users, update_user, list_sessions, create_session
from src.db.connection import generate_uuid, safe_uuid
from psycopg2.extras import RealDictCursor

# Create API router for v1 endpoints
router = APIRouter()

# Include memory router
router.include_router(memory_router)

# Get our module's logger
logger = logging.getLogger(__name__)

# Create an additional helper function for UUID validation
def is_valid_uuid(value: str) -> bool:
    """Check if a string is a valid UUID.
    
    Args:
        value: The string to check
        
    Returns:
        True if the string is a valid UUID, False otherwise
    """
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False

@router.get("/agent/list", response_model=List[AgentInfo], tags=["Agents"], 
           summary="List Available Agents",
           description="Returns a list of all available agent templates that can be used.")
async def list_agents():
    """List all available agents."""
    agent_list = []
    for name in AgentFactory.list_available_agents():
        # Get agent type from factory
        agent_type = AgentFactory._agents[name][0].__name__
        
        # Get model and description from database if available
        model = "unknown"
        description = None
        
        try:
            from src.db import get_agent_by_name
            agent = get_agent_by_name(name)
            if agent:
                model = agent.model or "unknown"
                description = agent.description
        except Exception as e:
            logger.warning(f"Error getting agent details from database: {str(e)}")
        
        # Create agent info object with all fields
        agent_info = AgentInfo(
            name=name,
            type=agent_type,
            model=model,
            description=description
        )
        agent_list.append(agent_info)
    
    return agent_list

@router.post("/agent/{agent_name}/run", tags=["Agents"],
            summary="Run Agent",
            description="Execute an agent with the specified name. Optionally provide a session ID or name to maintain conversation context.")
async def run_agent(agent_name: str, request: AgentRunRequest):
    """Run an agent with the given name."""
    try:
        # Get the pre-initialized agent
        agent = AgentFactory.get_agent(agent_name)
        
        # Get session_origin from request
        session_origin = request.session_origin
        
        # Extract session_name if provided
        session_name = request.session_name
        
        # We'll initialize message_history later once we have a valid session_id
        # Removing this initialization to prevent duplicate session creation
        
        # Get the agent database ID if available
        agent_id = getattr(agent, "db_id", None)
        
        # If agent_id is not set, try to get it from the database
        if agent_id is None:
            from src.db import get_agent_by_name
            agent_db = get_agent_by_name(f"{agent_name}_agent" if not agent_name.endswith('_agent') else agent_name)
            if agent_db:
                agent_id = agent_db.id
                # Save it back to the agent instance for future use
                agent.db_id = agent_id
                logging.info(f"Found agent ID {agent_id} for agent {agent_name}")
            else:
                logging.warning(f"Could not find agent ID for agent {agent_name}")
        
        # Check if session name is provided, use it to lookup existing sessions
        if session_name:
            # Look up the session by name
            from src.db import get_session_by_name
            existing_session = get_session_by_name(session_name)
            if existing_session:
                # Found an existing session with this name
                session_id = existing_session.id
                existing_agent_id = existing_session.agent_id
                
                # Check if the session is already associated with a different agent
                if existing_agent_id is not None and existing_agent_id != agent_id:
                    logger.error(f"Session name '{session_name}' is already associated with agent ID {existing_agent_id}, cannot use with agent ID {agent_id}")
                    raise HTTPException(
                        status_code=409,
                        detail=f"Session name '{session_name}' is already associated with a different agent. Please use a different session name."
                    )
                
                # Found an existing session with this name, use it
                request.session_id = str(session_id)
                logger.info(f"Found existing session with name '{session_name}', using ID: {session_id}")
        
        # Check if session_id is provided
        if not request.session_id:
            # If no session_id is provided or no session found with the provided name
            # Create a new session with the session_name if provided
            try:
                # Use the repository pattern to create a session
                from src.db.models import Session
                
                # Create metadata with session_origin if provided
                metadata = {}
                if session_origin:
                    metadata['session_origin'] = session_origin
                
                # Create a Session model
                new_session = Session(
                    id=generate_uuid(),  # Use safe UUID generation
                    user_id=request.user_id,
                    agent_id=agent_id,
                    name=session_name,
                    platform=session_origin or 'web',
                    metadata=metadata
                )
                
                # Create the session using the repository function
                session_id = create_session(new_session)
                if not session_id:
                    logger.error("Failed to create session")
                    raise HTTPException(status_code=500, detail="Failed to create session")
                    
                request.session_id = str(session_id)
                logger.info(f"Created new session with ID: {session_id}, name: {session_name}, and origin: {session_origin}")
            except Exception as e:
                # Check for unique constraint violation
                if "duplicate key value violates unique constraint" in str(e) and "sessions_name_key" in str(e):
                    logger.error(f"Session name '{session_name}' already exists")
                    raise HTTPException(
                        status_code=409,
                        detail=f"Session name '{session_name}' already exists. Please use a different session name."
                    )
                # Re-raise other exceptions
                logger.error(f"Error creating session: {str(e)}")
                raise
        else:
            # Check if request.session_id is a session name instead of a UUID
            session_id = request.session_id
            try:
                # Validate if it's a UUID using our helper function
                if is_valid_uuid(request.session_id):
                    # It's a valid UUID, continue
                    pass
                else:
                    # Not a UUID, raise ValueError to trigger the except block
                    raise ValueError("Not a valid UUID")
            except ValueError:
                # Not a UUID, try to look up by name
                logger.info(f"Looking up session by name: {request.session_id}")
                
                # Use the db function to get session by name
                from src.db import get_session_by_name
                resolved_session = get_session_by_name(request.session_id)
                
                if resolved_session:
                    # Found a session with matching name
                    session_id = resolved_session.id
                    existing_agent_id = resolved_session.agent_id
                    
                    # Check if the session is already associated with a different agent
                    if existing_agent_id is not None and existing_agent_id != agent_id:
                        logger.error(f"Session name '{request.session_id}' is already associated with agent ID {existing_agent_id}, cannot use with agent ID {agent_id}")
                        raise HTTPException(
                            status_code=409,
                            detail=f"Session name '{request.session_id}' is already associated with a different agent. Please use a different session name."
                        )
                    
                    logger.info(f"Found session ID {session_id} for name {request.session_id}")
                else:
                    # Name doesn't exist yet, create a new session with this name
                    try:
                        # Use the repository pattern to create a session
                        from src.db.models import Session
                        
                        # Create metadata with session_origin if provided
                        metadata = {}
                        if session_origin:
                            metadata['session_origin'] = session_origin
                        
                        # Create a Session model
                        new_session = Session(
                            id=generate_uuid(),  # Use safe UUID generation
                            user_id=request.user_id,
                            agent_id=agent_id,
                            name=request.session_id,
                            platform=session_origin or 'web',
                            metadata=metadata
                        )
                        
                        # Create the session using the repository function
                        session_id = create_session(new_session)
                        if not session_id:
                            logger.error("Failed to create session")
                            raise HTTPException(status_code=500, detail="Failed to create session")
                            
                        session_id = str(session_id)
                        logger.info(f"Created new session with ID: {session_id} and name: {request.session_id}")
                    except Exception as e:
                        # Check for unique constraint violation
                        if "duplicate key value violates unique constraint" in str(e) and "sessions_name_key" in str(e):
                            logger.error(f"Session name '{request.session_id}' already exists")
                            raise HTTPException(
                                status_code=409,
                                detail=f"Session name '{request.session_id}' already exists. Please use a different session name."
                            )
                        # Re-raise other exceptions
                        logger.error(f"Error creating session: {str(e)}")
                        raise
                
                # Update the request.session_id with the actual UUID
                request.session_id = str(session_id)
            
            # Initialize message_history with the proper session_id
            message_history = MessageHistory(session_id=request.session_id, user_id=request.user_id)
        
        # Store channel_payload in the users table if provided
        if request.channel_payload:
            try:
                # Use the user_id directly as an integer
                user_id_int = request.user_id
                if user_id_int:
                    # Look up or create user
                    from src.db import User, get_user, create_user, update_user
                    
                    user = get_user(user_id_int)
                    if not user:
                        # Create a new user with this ID
                        user = User(
                            id=user_id_int,
                            user_data={"channel_payload": request.channel_payload}
                        )
                        create_user(user)
                    else:
                        # Update existing user with channel_payload
                        user_data = user.user_data or {}
                        user_data["channel_payload"] = request.channel_payload
                        user.user_data = user_data
                        update_user(user)
                    
                    logger.info(f"Updated user {user_id_int} with channel_payload")
            except Exception as e:
                logger.error(f"Error storing channel_payload for user {request.user_id}: {str(e)}")
        
        # Resolve the agent name to a numeric ID if needed
        try:
            # If agent_id is a string, try to look up the actual agent ID from the database
            if isinstance(agent_id, str) and not agent_id.isdigit():
                from src.db import get_agent_by_name
                agent_db = get_agent_by_name(agent_id)
                if agent_db and agent_db.id:
                    resolved_agent_id = agent_db.id
                    logger.info(f"Resolved agent name '{agent_id}' to numeric ID {resolved_agent_id}")
                    agent_id = resolved_agent_id
        except Exception as e:
            logger.warning(f"Error resolving agent name to ID: {str(e)}")
        
        # Update agent_id in the request
        request.agent_id = agent_id
        
        # Initialize message_history with the proper session_id
        message_history = MessageHistory(session_id=request.session_id, user_id=request.user_id)
        
        # Link the agent to the session in the database
        AgentFactory.link_agent_to_session(agent_name, request.session_id)
        
        # Get filtered messages up to the limit for agent processing
        filtered_messages = None
        if message_history and hasattr(message_history, 'get_filtered_messages'):
            filtered_messages = message_history.get_filtered_messages(
                message_limit=request.message_limit,
                sort_desc=False  # Sort chronologically for agent processing
            )

        # Process the message with additional metadata if available
        message_metadata = {
            "message_type": request.message_type,
            "media_url": request.mediaUrl, 
            "mime_type": request.mime_type
        }
        
        # Create a combined context with all available information
        combined_context = {**request.context, **message_metadata}
        
        # Add channel_payload to context if available
        if request.channel_payload:
            combined_context["channel_payload"] = request.channel_payload
        
        # Log incoming message details
        logger.info(f"Processing message from user {request.user_id} with type: {request.message_type}")
        if request.mediaUrl:
            logger.info(f"Media URL: {request.mediaUrl}, MIME type: {request.mime_type}")
        
        # Prepare multimodal content
        multimodal_content = {}
        
        # Handle legacy single media fields
        if request.mediaUrl and request.mime_type:
            logger.info(f"Processing legacy single media with URL: {request.mediaUrl} and type: {request.mime_type}")
            media_type = "unknown"
            if request.mime_type.startswith("image/"):
                media_type = "image"
                multimodal_content["image_url"] = request.mediaUrl
            elif request.mime_type.startswith("audio/"):
                media_type = "audio"
                multimodal_content["audio_url"] = request.mediaUrl
            elif request.mime_type.startswith(("application/", "text/")):
                media_type = "document"
                multimodal_content["document_url"] = request.mediaUrl
            logger.info(f"Detected media type: {media_type}")
        
        # Handle new multimodal content array
        if request.media_contents:
            logger.info(f"Processing {len(request.media_contents)} multimodal content items")
            for item in request.media_contents:
                if isinstance(item, ImageUrlContent):
                    multimodal_content["image_url"] = item.media_url
                    logger.info(f"Added image URL: {item.media_url}")
                elif isinstance(item, ImageBinaryContent):
                    multimodal_content["image_data"] = item.data
                    logger.info(f"Added binary image data (length: {len(item.data) if item.data else 0})")
                elif isinstance(item, AudioUrlContent):
                    multimodal_content["audio_url"] = item.media_url
                    logger.info(f"Added audio URL: {item.media_url}")
                elif isinstance(item, AudioBinaryContent):
                    multimodal_content["audio_data"] = item.data
                    logger.info(f"Added binary audio data (length: {len(item.data) if item.data else 0})")
                elif isinstance(item, DocumentUrlContent):
                    multimodal_content["document_url"] = item.media_url
                    logger.info(f"Added document URL: {item.media_url}")
                elif isinstance(item, DocumentBinaryContent):
                    multimodal_content["document_data"] = item.data
                    logger.info(f"Added binary document data (length: {len(item.data) if item.data else 0})")

        # If preserve_system_prompt flag is set, check for existing system_prompt in session
        if request.preserve_system_prompt:
            try:
                # Look up existing system_prompt in session metadata
                from src.db import get_session
                existing_session = get_session(uuid.UUID(request.session_id))
                if existing_session and existing_session.metadata:
                    try:
                        metadata = existing_session.metadata
                        if isinstance(metadata, str):
                            metadata = json.loads(metadata)
                            
                        if metadata and "system_prompt" in metadata:
                            # Use the existing system_prompt
                            if hasattr(agent, "system_prompt"):
                                agent.system_prompt = metadata["system_prompt"]
                                logger.info("Using existing system_prompt from session metadata")
                    except Exception as e:
                        logger.error(f"Error retrieving system_prompt from metadata: {str(e)}")
            except Exception as e:
                logger.error(f"Error handling preserve_system_prompt flag: {str(e)}")
        
        try:        
            # Check if the agent's process_message accepts message_already_added parameter
            agent_process_signature = inspect.signature(agent.process_message)
            supports_message_already_added = 'message_already_added' in agent_process_signature.parameters
            
            # Prepare base arguments for all agents
            process_args = {
                "session_id": request.session_id,
                "user_id": request.user_id,
                "context": combined_context,
                "message_history": message_history,  # Pass the existing MessageHistory object
            }
            
            # Let the agent handle adding the message to avoid formatting issues with tools
            # Do not add message_already_added=True as this is causing tool handling issues
            
            # Ensure system_prompt is stored for this session
            if hasattr(agent, "system_prompt") and agent.system_prompt:
                # Store in session metadata if not already present
                try:
                    from src.db import get_session, update_session
                    session = get_session(uuid.UUID(request.session_id))
                    if session:
                        # Get existing metadata or create new dictionary
                        metadata = session.metadata or {}
                        if isinstance(metadata, str):
                            try:
                                import json
                                metadata = json.loads(metadata)
                            except json.JSONDecodeError:
                                metadata = {}
                        
                        # Update system_prompt in metadata if not already set
                        if "system_prompt" not in metadata:
                            metadata["system_prompt"] = agent.system_prompt
                            session.metadata = metadata
                            
                            # Update session
                            update_session(session)
                            logger.info(f"Stored system prompt in session metadata")
                except Exception as e:
                    logger.error(f"Error updating session metadata with system prompt: {str(e)}")
            
            # Process the message with agent
            # Call process_message with appropriate arguments
            response = await agent.process_message(
                request.message_content,
                **process_args
            )
            
            # Return the parsed response
            return {
                "message": response.text,
                "session_id": request.session_id,
                "success": response.success,
                "tool_calls": response.tool_calls,
                "tool_outputs": response.tool_outputs,
            }
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": f"Error processing message: {str(e)}"}
            )
    except HTTPException as http_ex:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error running agent {agent_name}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Error running agent: {str(e)}"}
        )

@router.get("/sessions", response_model=SessionListResponse, tags=["Sessions"],
            summary="List All Sessions",
            description="Retrieve a list of all sessions with pagination options.")
async def list_sessions_route(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    sort_desc: bool = Query(True, description="Sort by most recent first")
):
    """List all sessions with pagination.
    
    Args:
        page: Page number (1-based).
        page_size: Number of sessions per page.
        sort_desc: Sort by most recent first if True.
        
    Returns:
        List of sessions with pagination info.
    """
    try:
        logger.info(f"Listing sessions - page={page}, page_size={page_size}, sort_desc={sort_desc}")
        
        # Use the enhanced repository function with pagination
        sessions, total_count = list_sessions(
            page=page,
            page_size=page_size,
            sort_desc=sort_desc
        )
        
        # Calculate total pages
        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
        
        # Convert to session info objects
        session_info_list = [
            SessionInfo(
                id=str(session.id),
                name=session.name,
                user_id=session.user_id,
                agent_id=session.agent_id,
                platform=session.platform,
                metadata=session.metadata,
                created_at=session.created_at,
                updated_at=session.updated_at,
                run_finished_at=session.run_finished_at
            ) 
            for session in sessions
        ]
        
        logger.info(f"Found {len(session_info_list)} sessions (total {total_count})")
        
        # Create response
        response = SessionListResponse(
            sessions=session_info_list,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
        return response
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list sessions: {str(e)}"
        )

@router.get("/sessions/{session_id_or_name}", response_model=SessionResponse, response_model_exclude_none=True, 
           tags=["Sessions"],
           summary="Get Session History",
           description="Retrieve a session's message history with pagination options. You can use either the session ID (UUID) or a session name.")
async def get_session_route(
    session_id_or_name: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    sort_desc: bool = Query(True, description="Sort by most recent first"),
    hide_tools: bool = Query(False, description="Exclude tool calls and outputs")
):
    """Get a session's message history with pagination.
    
    Args:
        session_id_or_name: The ID or name of the session to retrieve.
        page: Page number (1-based).
        page_size: Number of messages per page.
        sort_desc: Sort by most recent first if True.
        hide_tools: If True, excludes tool calls and outputs from the response.
        
    Returns:
        The session's message history with pagination info.
    """
    try:
        logger.info(f"Retrieving session with identifier: {session_id_or_name}")
        
        # Use repository functions to get the session
        from src.db import get_session, get_session_by_name
        
        # Determine if the input is a UUID or session name
        session = None
        try:
            # Try to parse as UUID using our helper
            if is_valid_uuid(session_id_or_name):
                session_id = uuid.UUID(session_id_or_name)
                logger.info(f"Looking up session by ID: {session_id}")
                session = get_session(session_id)
        except ValueError:
            # Not a UUID, try to look up by name
            logger.info(f"Looking up session by name: {session_id_or_name}")
            session = get_session_by_name(session_id_or_name)
        
        # Check if session exists
        if not session:
            logger.warning(f"Session not found with identifier: {session_id_or_name}")
            return SessionResponse(
                session_id=session_id_or_name,
                messages=[],
                exists=False,
                total_messages=0,
                current_page=1,
                total_pages=0
            )
        
        session_id = session.id
        logger.info(f"Found session with ID: {session_id}")
        
        # Get message history
        message_history = MessageHistory(str(session_id))
        
        # Get paginated messages
        paginated_messages, total_messages, current_page, total_pages = message_history.get_paginated_messages(
            page=page,
            page_size=page_size,
            sort_desc=sort_desc
        )
        
        # Format messages for API response
        formatted_messages = [
            message for message in (
                message_history.format_message_for_api(msg, hide_tools=hide_tools)
                for msg in paginated_messages
            )
            if message is not None
        ]
        
        # Wrap each formatted message dict into a MessageModel to ensure Pydantic processing
        clean_messages = [MessageModel(**msg) for msg in formatted_messages]
        
        session_response = SessionResponse(
            session_id=str(session_id),
            messages=clean_messages,
            exists=True,
            total_messages=total_messages,
            current_page=current_page,
            total_pages=total_pages
        )
        
        return session_response
    except Exception as e:
        logger.error(f"Error retrieving session {session_id_or_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve session: {str(e)}"
        )

@router.delete("/sessions/{session_id_or_name}", tags=["Sessions"],
              summary="Delete Session",
              description="Delete a session's message history by its ID or name.")
async def delete_session_route(session_id_or_name: str):
    """Delete a session by ID or name."""
    try:
        # First determine if the input is a UUID or a name
        try:
            # Try to parse as UUID using our helper
            if is_valid_uuid(session_id_or_name):
                session_id = uuid.UUID(session_id_or_name)
                # It's a valid UUID, use it directly
                from src.db import get_session, delete_session, delete_session_messages
                
                # Get the session to verify it exists
                session = get_session(session_id)
                if not session:
                    return JSONResponse(
                        status_code=404,
                        content={"error": f"Session with ID {session_id_or_name} not found"}
                    )
                    
                # Delete all messages first
                delete_session_messages(session_id)
                
                # Then delete the session itself
                success = delete_session(session_id)
                
                if success:
                    return {"status": "success", "message": f"Session {session_id_or_name} deleted successfully"}
                else:
                    return JSONResponse(
                        status_code=500,
                        content={"error": f"Failed to delete session {session_id_or_name}"}
                    )
                
        except ValueError:
            # Not a valid UUID, try to find by name
            from src.db import get_session_by_name, delete_session, delete_session_messages
            
            # Get the session to verify it exists and get its ID
            session = get_session_by_name(session_id_or_name)
            if not session:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"Session with name '{session_id_or_name}' not found"}
                )
                
            session_id = session.id
                
            # Delete all messages first
            delete_session_messages(session_id)
            
            # Then delete the session itself
            success = delete_session(session_id)
            
            if success:
                return {"status": "success", "message": f"Session '{session_id_or_name}' deleted successfully"}
            else:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to delete session '{session_id_or_name}'"}
                )
    except Exception as e:
        logger.error(f"Error deleting session {session_id_or_name}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to delete session: {str(e)}"}
        )

# User management endpoints
@router.get("/users", response_model=UserListResponse, tags=["Users"],
           summary="List Users",
           description="Returns a paginated list of users.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def list_users_route(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
):
    """List all users with pagination."""
    try:
        logger.info(f"Listing users - page={page}, page_size={page_size}")
        
        # Use the repository function
        users, total_count = list_users(page=page, page_size=page_size)
        
        # Create the response
        user_list = [
            UserInfo(
                id=user.id,
                email=user.email,
                phone_number=user.phone_number,
                user_data=user.user_data,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]
        
        # Calculate pagination metadata
        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1
        
        logger.info(f"Found {len(user_list)} users (total {total_count})")
        
        # Return paginated response
        return UserListResponse(
            users=user_list,
            total=total_count,
            page=page,
            page_size=page_size,
            has_next=has_next,
            has_prev=has_prev
        )
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/users", response_model=UserInfo, tags=["Users"],
            summary="Create User",
            description="Creates a new user with email, phone_number, and/or user_data fields.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def create_user_route(user_create: UserCreate):
    """Create a new user."""
    try:
        # Need at least one identifier - email or phone_number
        if not user_create.email and not user_create.phone_number:
            raise HTTPException(status_code=400, detail="At least one of email or phone_number must be provided")

        logger.info(f"Creating user with email: {user_create.email}, phone_number: {user_create.phone_number}")
        if user_create.user_data:
            logger.info(f"User data: {json.dumps(user_create.user_data)}")
        
        # Create a User model from the UserCreate data
        from src.db.models import User
        from src.db import create_user
        
        user = User(
            email=user_create.email,
            phone_number=user_create.phone_number,
            user_data=user_create.user_data
        )
        
        # Use the repository function to create the user
        user_id = create_user(user)
        
        if not user_id:
            logger.error("Failed to create user")
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        # Get the created user
        from src.db import get_user
        created_user = get_user(user_id)
        
        if not created_user:
            logger.error(f"Could not retrieve created user with ID: {user_id}")
            raise HTTPException(status_code=500, detail="User was created but could not be retrieved")
        
        logger.info(f"User created with ID: {created_user.id}")
        
        # Return user info
        return UserInfo(
            id=created_user.id,
            email=created_user.email,
            phone_number=created_user.phone_number,
            user_data=created_user.user_data,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/users/{user_identifier}", response_model=UserInfo, tags=["Users"],
            summary="Get User",
            description="Returns details for a specific user by ID, email, or phone number.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def get_user_route(user_identifier: str = Path(..., description="The user ID, email, or phone number")):
    """Get user details by ID, email, or phone number."""
    try:
        logger.info(f"Looking up user with identifier: {user_identifier}")
        
        # Use the repository function instead of direct SQL
        user = get_user_by_identifier(user_identifier)
        
        # Check if user exists
        if not user:
            logger.warning(f"User not found with identifier: {user_identifier}")
            raise HTTPException(status_code=404, detail=f"User not found with identifier: {user_identifier}")
        
        # Log the found user details
        logger.info(f"Found user with ID: {user.id}")
        logger.info(f"  Email: {user.email}")
        logger.info(f"  Phone number: {user.phone_number}")
        
        # Return user info
        return UserInfo(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            user_data=user.user_data,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/users/{user_identifier}", response_model=UserInfo, tags=["Users"],
            summary="Update User",
            description="Updates an existing user identified by ID, email, or phone number.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def update_user_route(user_update: UserUpdate, user_identifier: str = Path(..., description="The user ID, email, or phone number")):
    """Update an existing user."""
    try:
        logger.info(f"Updating user with identifier: {user_identifier}")
        logger.info(f"Update data: email={user_update.email}, phone_number={user_update.phone_number}")
        if user_update.user_data:
            logger.info(f"user_data={json.dumps(user_update.user_data)}")
        
        # Find the user using the repository function
        from src.db import get_user_by_identifier, update_user, get_user
        
        # Get the existing user
        user = get_user_by_identifier(user_identifier)
        
        # Check if user exists
        if not user:
            logger.warning(f"User not found with identifier: {user_identifier}")
            raise HTTPException(status_code=404, detail=f"User not found with identifier: {user_identifier}")
        
        logger.info(f"Found user with ID: {user.id}")
        
        # Update the user fields with new data if provided
        if user_update.email is not None:
            user.email = user_update.email
            
        if user_update.phone_number is not None:
            user.phone_number = user_update.phone_number
            
        if user_update.user_data is not None:
            user.user_data = user_update.user_data
        
        # Use the repository function to update the user
        updated_user_id = update_user(user)
        
        if not updated_user_id:
            logger.error(f"Failed to update user with ID: {user.id}")
            raise HTTPException(status_code=500, detail="Failed to update user")
        
        # Get the updated user
        updated_user = get_user(updated_user_id)
        
        if not updated_user:
            logger.error(f"Could not retrieve updated user with ID: {updated_user_id}")
            raise HTTPException(status_code=500, detail="User was updated but could not be retrieved")
        
        logger.info(f"User updated - ID: {updated_user.id}")
        
        return UserInfo(
            id=updated_user.id,
            email=updated_user.email,
            phone_number=updated_user.phone_number,
            user_data=updated_user.user_data,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/users/{user_identifier}", response_model=DeleteSessionResponse, tags=["Users"],
               summary="Delete User",
               description="Deletes a user account by ID, email, or phone number.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def delete_user_route(user_identifier: str = Path(..., description="The user ID, email, or phone number")):
    """Delete a user account by ID, email, or phone number."""
    try:
        logger.info(f"Attempting to delete user with identifier: {user_identifier}")
        
        # Find the user using the repository function
        from src.db import get_user_by_identifier, delete_user
        
        # Get the user to delete
        user = get_user_by_identifier(user_identifier)
        
        # Check if user exists
        if not user:
            logger.warning(f"User not found with identifier: {user_identifier}")
            raise HTTPException(status_code=404, detail=f"User not found with identifier: {user_identifier}")
        
        user_id = user.id
        logger.info(f"Found user with ID: {user_id}")
        
        # Use the repository function to delete the user
        success = delete_user(user_id)
        
        if not success:
            logger.error(f"Failed to delete user with ID: {user_id}")
            raise HTTPException(status_code=500, detail=f"Failed to delete user with ID: {user_id}")
        
        logger.info(f"Successfully deleted user with ID: {user_id}")
        
        # Return a successful response
        return DeleteSessionResponse(
            status="success",
            session_id=str(user_id),  # Use the session_id field to return the user_id
            message=f"User with ID {user_id} deleted successfully"
        )
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 
```

# src/auth.py

```py
from fastapi import HTTPException, Request, Depends, Header
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Optional
from src.config import settings

API_KEY_NAME = "x-api-key"

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for health check, root, and documentation endpoints
        no_auth_paths = [
            "/health", 
            "/",
            "/api/v1/docs",
            "/api/v1/redoc",
            "/api/v1/openapi.json"
        ]
        
        # Check if this path should bypass authentication
        if request.url.path in no_auth_paths:
            return await call_next(request)

        api_key = request.headers.get(API_KEY_NAME) or request.query_params.get(API_KEY_NAME)
        if api_key is None:
            return JSONResponse(status_code=401, content={"detail": "x-api-key is missing in headers or query parameters"})
        if api_key != settings.AM_API_KEY:
            return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})
            
        return await call_next(request)

async def get_api_key(x_api_key: Optional[str] = Header(None, alias=API_KEY_NAME)):
    """Dependency to validate API key in FastAPI routes.
    
    Args:
        x_api_key: The API key provided in the request header
        
    Returns:
        The validated API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="API key is missing"
        )
    
    if x_api_key != settings.AM_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return x_api_key 
```

# src/cli.py

```py
"""
Main CLI entry point that simply re-exports the CLI app from the src.cli package.
"""
from src.cli import app

if __name__ == "__main__":
    app()

```

# src/cli/__init__.py

```py
"""
CLI module for Automagik Agents.
This module contains the CLI commands and utilities.
"""
import typer
import os
import sys
from typing import Optional, List, Callable
from src.cli.db import db_app
from src.cli.api import api_app
from src.cli.agent import agent_app

# Handle --debug flag immediately before any other imports
# This makes sure the environment variable is set before any module is imported
debug_mode = "--debug" in sys.argv
if debug_mode:
    os.environ["AM_LOG_LEVEL"] = "DEBUG"
    print(f"Debug mode enabled. Environment variable AM_LOG_LEVEL set to DEBUG")

# Now import config after setting environment variables
from src.config import LogLevel, Settings, mask_connection_string
from pathlib import Path
from dotenv import load_dotenv

# Create the main CLI app with global options
app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Define a callback that runs before any command
def global_callback(ctx: typer.Context, debug: bool = False):
    """Global callback for all commands to process common options."""
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"
        # Print configuration info
        try:
            from src.config import settings
            print("🔧 Configuration loaded:")
            print(f"├── Environment: {settings.AM_ENV}")
            print(f"├── Log Level: {settings.AM_LOG_LEVEL}")
            print(f"├── Server: {settings.AM_HOST}:{settings.AM_PORT}")
            print(f"├── OpenAI API Key: {settings.OPENAI_API_KEY[:5]}...{settings.OPENAI_API_KEY[-5:]}")
            print(f"├── API Key: {settings.AM_API_KEY[:5]}...{settings.AM_API_KEY[-5:]}")
            print(f"├── Discord Bot Token: {settings.DISCORD_BOT_TOKEN[:5]}...{settings.DISCORD_BOT_TOKEN[-5:]}")
            print(f"├── Database URL: {mask_connection_string(settings.DATABASE_URL)}")

            if settings.NOTION_TOKEN:
                print(f"└── Notion Token: {settings.NOTION_TOKEN[:5]}...{settings.NOTION_TOKEN[-5:]}")
            else:
                print("└── Notion Token: Not set")
        except Exception as e:
            print(f"Error displaying configuration: {str(e)}")

# Add subcommands with the global debug option
app.add_typer(api_app, name="api")
app.add_typer(db_app, name="db")
app.add_typer(agent_app, name="agent")

# Default callback for main app
@app.callback()
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode (shows detailed configuration)", is_flag=True)
):
    """
    Automagik CLI tool.
    """
    # Call the global callback with the debug flag
    global_callback(ctx, debug) 
```

# src/cli/agent.py

```py
"""
Agent management commands for Automagik Agents.
"""
import typer

# Import agent command modules
from src.cli.agent import create, run, chat

# Create the agent command group
agent_app = typer.Typer()

# Add the subcommands
agent_app.add_typer(create.create_app, name="create", help="Create a new agent from a template")
agent_app.add_typer(run.run_app, name="run", help="Run a single message through an agent")
agent_app.add_typer(chat.chat_app, name="chat", help="Start an interactive chat session with an agent") 
```

# src/cli/agent/__init__.py

```py
"""
Agent subcommands for the Automagik Agents CLI.

This package contains commands related to agent management, creation, and usage.
"""

import typer
import os
from src.cli.agent.create import create_app
from src.cli.agent.run import run_app
from src.cli.agent.chat import chat_app

# Create a subgroup for all agent commands
agent_app = typer.Typer(
    help="Agent management and interaction commands",
    no_args_is_help=True
)

# Add the subcommands
agent_app.add_typer(create_app, name="create", help="Create a new agent from a template")
agent_app.add_typer(run_app, name="run", help="Run a single message through an agent")
agent_app.add_typer(chat_app, name="chat", help="Start an interactive chat session with an agent")

@agent_app.callback()
def agent_callback(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    Manage and interact with Automagik Agents.
    
    This command group provides tools to create, run, and chat with agents.
    
    Common commands:
      - To create a new agent:
        automagik-agents agent create agent --name my_agent --template simple_agent
        
      - To list available templates:
        automagik-agents agent create list
        
      - To run a single message:
        automagik-agents agent run message --agent my_agent --message "Hello"
        
      - To start a chat session:
        automagik-agents agent chat start --agent my_agent
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG" 
```

# src/cli/agent/chat.py

```py
"""
Command for interactive chat with an agent.

This command provides an interactive chat interface to converse with an agent.
It maintains a conversation history and supports chat commands.
"""
import sys
import asyncio
import json
import typer
from typing import Dict, List, Optional, Any, Set
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich import print as rich_print
import uuid
import os
from pathlib import Path
import re

from src.config import settings

# Create app for the chat command
chat_app = typer.Typer(no_args_is_help=True)

# Create a rich console for output
console = Console()

@chat_app.callback()
def chat_callback(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    Start an interactive chat session with an agent.
    
    Use 'start' command with --agent option to begin chatting:
      automagik-agents agent chat start --agent <agent_name>
    
    Or list available agents first:
      automagik-agents agent chat list
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"

def get_api_endpoint(path: str) -> str:
    """Build a consistent API endpoint URL with the correct prefix."""
    # Ensure the path doesn't start with a slash
    if path.startswith("/"):
        path = path[1:]
    
    # Always use /api/v1/ prefix
    if not path.startswith("api/v1/"):
        path = f"api/v1/{path}"
    
    # Build the full URL with server from settings
    # The host and port values are stored in AM_HOST and AM_PORT
    server = f"http://{settings.AM_HOST}:{settings.AM_PORT}"
    if not server.endswith('/'):
        server = f"{server}/"
    url = f"{server}{path}"
    
    return url

def get_available_agents() -> List[Dict[str, Any]]:
    """Get a list of available agents using the API."""
    try:
        # Define the API endpoint for listing agents
        endpoint = get_api_endpoint("agent/list")
        if settings.AM_LOG_LEVEL == "DEBUG":
            console.print(f"Getting agents from: {endpoint}")
        
        # Prepare headers with API key if available
        headers = {}
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY
        
        # Make the API request
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            # Check if the request was successful
            if response.status_code == 200:
                agents = response.json()
                if settings.AM_LOG_LEVEL == "DEBUG":
                    console.print(f"Successfully retrieved {len(agents)} agents")
                
                # Convert the API response to a format compatible with the rest of the code
                for agent in agents:
                    # Ensure id field is present (use name as fallback)
                    if "id" not in agent:
                        agent["id"] = agent["name"]
                    
                    # If description is missing, provide a default
                    if "description" not in agent or not agent["description"]:
                        agent["description"] = f"Agent of type {agent.get('type', 'unknown')}"
                    
                    # If model is missing, provide a default
                    if "model" not in agent or not agent["model"]:
                        agent["model"] = "unknown"
                
                return agents
            else:
                console.print(f"Error getting agents: HTTP {response.status_code}", style="bold red")
                if settings.AM_LOG_LEVEL == "DEBUG":
                    console.print(f"Response: {response.text}", style="red")
                return []
        except requests.exceptions.ConnectionError:
            console.print(f"Connection error: Could not connect to API server at {endpoint}", style="bold red")
            return []
    except Exception as e:
        console.print(f"Error getting agents from API: {str(e)}", style="bold red")
        return []

def list_available_agents() -> None:
    """Print a list of available agents."""
    agents = get_available_agents()
    
    if not agents:
        console.print("No agents available or could not connect to the API.", style="bold red")
        console.print("\n[yellow]Possible reasons:[/]")
        console.print("1. The server might not be running. Start it with:")
        console.print("   [cyan]automagik-agents api start[/]")
        console.print("2. Your API server could be running on a different host/port.")
        console.print(f"   Current server setting: [cyan]{settings.AM_HOST}:{settings.AM_PORT}[/]")
        console.print("3. You might not have added any agents yet.")
        
        console.print("\n[green]Try creating an agent first:[/]")
        console.print("  automagik-agents agent create agent --name my_agent --template simple_agent")
        
        console.print("\n[green]Or check if you can access the API directly:[/]")
        console.print(f"  curl http://{settings.AM_HOST}:{settings.AM_PORT}/api/v1/agent/list -H 'x-api-key: {settings.AM_API_KEY}'")
        return
    
    console.print("\nAvailable Agents:", style="bold green")
    for i, agent in enumerate(agents, 1):
        name = agent.get("name", "Unknown")
        description = agent.get("description", "No description")
        model = agent.get("model", "Unknown model")
        
        console.print(f"{i}. [bold cyan]{name}[/] - {description} [dim](Model: {model})[/]")
    
    console.print("\nUse the agent name to start a chat session:", style="green")
    console.print(f"  automagik-agents agent chat start --agent <agent_name>", style="bright_black")

async def get_user_by_id(user_id: int) -> Dict[str, Any]:
    """Get user data from the API by ID."""
    try:
        # Define the API endpoint
        endpoint = get_api_endpoint(f"users/{user_id}")
        if settings.AM_LOG_LEVEL == "DEBUG":
            console.print(f"Getting user data from: {endpoint}")
        
        # Prepare headers with API key if available
        headers = {}
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY
        
        # Make the API request
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            user_data = response.json()
            if settings.AM_LOG_LEVEL == "DEBUG":
                console.print(f"Successfully retrieved user {user_id} from API")
            return user_data
        else:
            if settings.AM_LOG_LEVEL == "DEBUG":
                console.print(f"Error getting user by ID {user_id}: HTTP {response.status_code}", style="red")
                console.print(f"Using fallback user data", style="yellow")
            # Return fallback data
            return {"id": user_id, "email": f"user{user_id}@example.com", "name": f"User {user_id}"}
    except Exception as e:
        if settings.AM_LOG_LEVEL == "DEBUG":
            console.print(f"Error getting user from API: {str(e)}", style="red")
            console.print(f"Using fallback user data", style="yellow")
        # Return fallback data
        return {"id": user_id, "email": f"user{user_id}@example.com", "name": f"User {user_id}"}

async def run_agent(agent_name: str, input_message: str, session_name: str = None, user_id: int = 1) -> dict:
    """Run the agent with the given message using the API."""
    try:
        # Check if debug mode is enabled either via settings or directly from environment variable
        debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (os.environ.get("AM_LOG_LEVEL") == "DEBUG")
        
        # Define the API endpoint with the correct prefix
        endpoint = get_api_endpoint(f"agent/{agent_name}/run")
        
        # Only show endpoint in debug mode
        if debug_mode:
            console.print(f"Using endpoint: {endpoint}")
        
        # Prepare the payload according to the API's expected format
        payload = {
            "message_content": input_message,
            "user_id": user_id,
            "context": {"debug": debug_mode},
            "session_origin": "cli"  # Always include session_origin for consistency
        }
        
        # Add session_name if provided
        if session_name:
            payload["session_name"] = session_name
            # Include debugging info
            if debug_mode:
                console.print(f"Using session name: {session_name}")
        
        if debug_mode:
            console.print(f"Request payload: {json.dumps(payload, indent=2)}")
        
        # Prepare headers with API key
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add API key to headers if available
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY
            
            if debug_mode:
                masked_key = f"{settings.AM_API_KEY[:4]}...{settings.AM_API_KEY[-4:]}" if len(settings.AM_API_KEY) > 8 else "****"
                console.print(f"Using API key: {masked_key}")
        
        # Make the API request
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        
        # Check response status
        if response.status_code == 200:
            result = response.json()
            if debug_mode:
                console.print(f"API Response: {json.dumps(result, indent=2)}")
                if "session_id" in result:
                    console.print(f"Session ID from response: {result['session_id']}")
            return result
        else:
            error_msg = f"API Error: Status {response.status_code}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg = f"API Error: {error_data['detail']}"
                    
                    # Detect specific errors related to session name uniqueness
                    if "duplicate key value violates unique constraint" in error_data.get("detail", "") and "sessions_name_key" in error_data.get("detail", ""):
                        error_msg = f"Session name '{session_name}' is already in use but with a different agent. Please use a different session name."
                    
                    # Detect session agent mismatch errors
                    elif "already associated with a different agent" in error_data.get("detail", ""):
                        if debug_mode:
                            console.print(f"Session agent mismatch error. Will retry with agent ID from the existing session.", style="yellow")
                        # For CLI usage, we want to recover and use the session anyway
                        # Retry without specifying an agent_id to let the server use the existing one
                        retry_payload = payload.copy()
                        # Remove any agent_id if present in context
                        if "agent_id" in retry_payload:
                            del retry_payload["agent_id"]
                        if debug_mode:
                            console.print(f"Retrying with payload: {json.dumps(retry_payload, indent=2)}")
                        
                        # Make the retry request
                        retry_response = requests.post(endpoint, json=retry_payload, headers=headers, timeout=30)
                        if retry_response.status_code == 200:
                            retry_result = retry_response.json()
                            if debug_mode:
                                console.print(f"Retry successful!", style="green")
                            return retry_result
                        else:
                            error_msg = f"API Error on retry: {retry_response.status_code}"
                            if debug_mode:
                                console.print(f"Retry failed: {retry_response.text}", style="red")
            except Exception:
                error_msg = f"API Error: {response.text}"
            
            console.print(f"{error_msg}", style="bold red")
            return {"error": error_msg}
                
    except Exception as e:
        error_msg = f"Error running agent: {str(e)}"
        console.print(f"{error_msg}", style="bold red")
        return {"error": error_msg}

def display_message(message: str, role: str, tool_calls: List = None, tool_outputs: List = None) -> None:
    """Display a message with proper formatting and panels similar to run_chat.py."""
    # Get terminal width to adjust message formatting
    term_width = console.width
    message_width = min(term_width - 20, 80)  # Keep messages reasonably sized
    
    if role == "user":
        # Skip displaying user messages - they're already shown in the chat loop
        pass
    
    elif role == "assistant":
        # Format tool usage in a compact, readable way
        if tool_calls:
            tool_panel_content = []
            
            for i, tool_call in enumerate(tool_calls):
                tool_name = tool_call.get('tool_name', 'Unknown Tool')
                tool_args = tool_call.get('args', {})
                
                # Format tool arguments nicely
                args_str = ""
                if tool_args:
                    if isinstance(tool_args, dict) and len(tool_args) > 0:
                        args_str = ", ".join(f"{k}={v}" for k, v in tool_args.items())
                    else:
                        args_str = str(tool_args)
                
                # Simplified tool call display
                if args_str:
                    tool_call_str = f"🔍 {tool_name}({args_str})"
                else:
                    tool_call_str = f"🔍 {tool_name}()"
                
                # Find and display matching output if available
                if tool_outputs:
                    matching_output = next(
                        (output for output in tool_outputs if output.get("tool_call_id") == tool_call.get("tool_call_id")),
                        None
                    )
                    if matching_output:
                        output_content = matching_output.get('content', '')
                        # Combine tool call and result in a single entry
                        tool_call_str = f"{tool_call_str} → {output_content}"
                
                tool_panel_content.append(tool_call_str)
            
            # Make tool panel very compact and subtle
            if tool_panel_content:
                from rich.panel import Panel
                from rich import box
                console.print(Panel(
                    "\n".join(tool_panel_content),
                    border_style="dim blue",
                    padding=(0, 1),
                    expand=False,
                    width=message_width
                ), justify="right")
        
        # Render the message in a panel
        from rich.panel import Panel
        from rich import box
        console.print(Panel(
            message,
            box=box.ROUNDED,
            border_style="blue",
            padding=(0, 1),
            expand=False,
            width=message_width
        ), justify="right")
    
    elif role == "system":
        # Make system messages subtle and compact
        from rich.panel import Panel
        console.print(Panel(
            message,
            border_style="dim red",
            padding=(0, 1),
            expand=False
        ))
    else:
        # Fallback for any other role
        console.print(f"[{role}] {message}")

def print_help() -> None:
    """Print help information for chat commands."""
    console.print("\n[bold]Available commands:[/]")
    console.print("[cyan]/help[/] - Show this help message")
    console.print("[cyan]/exit[/] or [cyan]/quit[/] - Exit the chat")
    console.print("[cyan]/new[/] - Start a new session (clears history)")
    console.print("[cyan]/history[/] - Show message history for the current session")
    console.print("[cyan]/clear[/] - Clear the screen")
    console.print("[cyan]/debug[/] - Toggle debug mode")
    console.print("[cyan]/session [name][/] - Set or show the current session name")
    console.print("")

async def chat_loop(agent_name: str, session_name: str = None, user_id: int = 1) -> None:
    """Run an interactive chat loop with the specified agent."""
    # Check if debug mode is enabled either via settings or directly from environment variable
    debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (os.environ.get("AM_LOG_LEVEL") == "DEBUG")
    
    current_session_name = session_name
    current_session_id = None
    
    # Get user info
    user = await get_user_by_id(user_id)
    
    # First check if the agent exists
    agents = get_available_agents()
    agent = next((a for a in agents if a["name"].lower() == agent_name.lower()), None)
    
    if not agent:
        console.print(f"Error: Agent '{agent_name}' not found", style="bold red")
        console.print("Available agents:", style="yellow")
        list_available_agents()
        return
    
    # If session_name wasn't provided, generate a random one
    if not current_session_name:
        current_session_name = f"cli-{uuid.uuid4().hex[:8]}"
    
    # Display welcome message in a box
    from rich.panel import Panel
    from rich import box
    
    console.print(Panel(
        f"Welcome to the {agent_name} Agent Chat",
        box=box.HEAVY,
        border_style="green",
        expand=False
    ), justify="center")
    
    console.print(f"Starting chat with [bold cyan]{agent_name}[/]")
    console.print(f"Session: [dim]{current_session_name}[/]")
    console.print("[dim]Type your messages and press Enter to send. Type /help for available commands.[/]")
    console.print("")
    
    # Add an initial greeting from the agent
    try:
        # Process a greeting message
        response = await run_agent(agent_name, "Hello", current_session_name, user_id)
        
        # Get the message content
        message_content = ""
        if "message" in response:
            message_content = response.get("message", "")
        elif "history" in response and "messages" in response["history"]:
            # Find the last assistant message
            messages = response["history"]["messages"]
            assistant_msgs = [msg for msg in messages if msg.get("role") == "assistant"]
            if assistant_msgs:
                message_content = assistant_msgs[-1].get("content", "")
        
        # Only display if we got a message
        if message_content:
            # Display assistant greeting
            display_message(message_content, "assistant")
            console.print("")
    except Exception as e:
        if debug_mode:
            console.print(f"[dim]Error displaying initial greeting: {str(e)}[/dim]")
    
    # Chat loop
    while True:
        try:
            # Get user input with a prompt style matching run_chat.py
            console.print("> ", end="")
            user_message = input().strip()
            
            # Check for commands
            if user_message.startswith("/"):
                command = user_message.lower()
                
                # Exit commands
                if command in ["/exit", "/quit"]:
                    console.print("[italic]Exiting chat session.[/]")
                    break
                
                # Help command
                elif command == "/help":
                    print_help()
                    continue
                
                # New session command
                elif command == "/new":
                    # Generate a new session name
                    current_session_name = f"cli-{uuid.uuid4().hex[:8]}"
                    current_session_id = None
                    console.print(f"[italic]Starting new session: {current_session_name}[/]")
                    continue
                
                # History command - to be implemented
                elif command == "/history":
                    console.print("[italic yellow]History view not implemented yet.[/]")
                    continue
                
                # Clear screen command
                elif command == "/clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                
                # Debug toggle command
                elif command == "/debug":
                    debug_mode = not debug_mode
                    console.print(f"[italic]Debug mode: {'enabled' if debug_mode else 'disabled'}[/]")
                    continue
                
                # Session command
                elif command.startswith("/session"):
                    parts = command.split(maxsplit=1)
                    if len(parts) > 1 and parts[1].strip():
                        # Set new session name
                        current_session_name = parts[1].strip()
                        current_session_id = None
                        console.print(f"[italic]Using session: {current_session_name}[/]")
                    else:
                        # Show current session name
                        console.print(f"[italic]Current session: {current_session_name}[/]")
                    continue
                
                # Unknown command
                else:
                    console.print(f"[italic red]Unknown command: {command}[/]")
                    print_help()
                    continue
            
            # Don't duplicate displaying user message - our input prompt already shows it
            # Process message through the agent
            response = await run_agent(agent_name, user_message, current_session_name, user_id)
            
            # Check for errors
            if "error" in response and response["error"]:
                console.print(f"Error: {response['error']}", style="bold red")
                
                # Handle session-specific errors
                if current_session_name and "already in use" in response["error"]:
                    console.print("\n[yellow]This session name is already being used with a different agent.[/]")
                    console.print("[yellow]You can use /session <new_name> to set a different session name.[/]")
                
                # Continue with the next message
                continue
            
            # Store session ID if provided
            if "session_id" in response and response["session_id"]:
                current_session_id = response["session_id"]
                if debug_mode:
                    console.print(f"[dim]Session ID: {current_session_id}[/]")
            
            # Extract response parts
            message_content = ""
            tool_calls = []
            tool_outputs = []
            
            # Check for different response formats and adapt accordingly
            if "message" in response:
                # Direct message in response
                message_content = response.get("message", "")
                
                # Look for tool information in history
                if "history" in response and "messages" in response["history"]:
                    # Find the last assistant message in history
                    messages = response["history"]["messages"]
                    
                    for msg in reversed(messages):
                        if msg.get("role") == "assistant":
                            # If we find a more complete assistant message with tools, use that
                            tool_calls = msg.get("tool_calls", [])
                            tool_outputs = msg.get("tool_outputs", [])
                            break
            elif "history" in response and "messages" in response["history"]:
                # If no direct message, look in history
                messages = response["history"]["messages"]
                
                # Find only the assistant message we care about - skip user messages entirely
                assistant_msgs = [msg for msg in messages if msg.get("role") == "assistant"]
                if assistant_msgs:
                    # Get the last assistant message
                    last_assistant_msg = assistant_msgs[-1]
                    message_content = last_assistant_msg.get("content", "")
                    tool_calls = last_assistant_msg.get("tool_calls", [])
                    tool_outputs = last_assistant_msg.get("tool_outputs", [])
            
            # Display assistant response
            display_message(message_content, "assistant", tool_calls, tool_outputs)
            console.print("")  # Add a blank line after each response for better readability
            
        except KeyboardInterrupt:
            console.print("\n[italic]Chat session interrupted. Exiting...[/]")
            break
        except EOFError:
            console.print("\n[italic]End of input. Exiting...[/]")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/] {str(e)}")
            console.print("[italic]Try again or type /exit to quit.[/]")

@chat_app.command()
def start(
    agent: str = typer.Option(..., "--agent", "-a", help="Agent to chat with"),
    session: Optional[str] = typer.Option(None, "--session", "-s", help="Session name to use/create"),
    user: int = typer.Option(1, "--user", "-u", help="User ID to use"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    Start an interactive chat session with an agent.
    
    This opens a conversational interface where you can talk to the agent
    and receive responses. The conversation history is preserved within
    the session.
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"
        
    try:
        import asyncio
        asyncio.run(chat_loop(
            agent_name=agent,
            session_name=session,
            user_id=user
        ))
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)

@chat_app.command()
def list():
    """
    List all available agents that can be used for chat.
    """
    list_available_agents()

def get_chats(agent_name: str = None) -> list:
    """Get all chats from the API."""
    try:
        # Check if debug mode is enabled either via settings or directly from environment variable
        debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (os.environ.get("AM_LOG_LEVEL") == "DEBUG")
        
        # Define the API endpoint with the correct prefix
        endpoint = get_api_endpoint("chats")
        if agent_name:
            endpoint = f"{endpoint}?agent_name={agent_name}"
        
        # Only show endpoint in debug mode
        if debug_mode:
            console.print(f"Using endpoint: {endpoint}")
        
        # Prepare headers with API key
        headers = {}
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY
            
            if debug_mode:
                masked_key = f"{settings.AM_API_KEY[:4]}...{settings.AM_API_KEY[-4:]}" if len(settings.AM_API_KEY) > 8 else "****"
                console.print(f"Using API key: {masked_key}")
        
        # Make the API request
        response = requests.get(endpoint, headers=headers, timeout=30)
        
        # Check response status
        if response.status_code == 200:
            result = response.json()
            
            if debug_mode:
                console.print(f"Successfully retrieved {len(result)} chats")
            
            return result
        else:
            error_msg = f"API Error: Status {response.status_code}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg = f"API Error: {error_data['detail']}"
            except Exception:
                error_msg = f"API Error: {response.text}"
            
            console.print(f"{error_msg}", style="bold red")
            if debug_mode:
                console.print(f"Response content: {response.text}")
            
            return []
    except Exception as e:
        console.print(f"Error getting chats: {str(e)}", style="bold red")
        if debug_mode:
            import traceback
            console.print(traceback.format_exc())
        return []

def get_chat(session_id: str) -> dict:
    """Get a specific chat by ID from the API."""
    try:
        # Check if debug mode is enabled either via settings or directly from environment variable
        debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (os.environ.get("AM_LOG_LEVEL") == "DEBUG")
        
        # Define the API endpoint with the correct prefix
        endpoint = get_api_endpoint(f"chats/{session_id}")
        
        # Only show endpoint in debug mode
        if debug_mode:
            console.print(f"Using endpoint: {endpoint}")
        
        # Prepare headers with API key
        headers = {}
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY
            
            if debug_mode:
                masked_key = f"{settings.AM_API_KEY[:4]}...{settings.AM_API_KEY[-4:]}" if len(settings.AM_API_KEY) > 8 else "****"
                console.print(f"Using API key: {masked_key}")
        
        # Make the API request
        response = requests.get(endpoint, headers=headers, timeout=30)
        
        # Check response status
        if response.status_code == 200:
            result = response.json()
            
            if debug_mode:
                console.print(f"Successfully retrieved chat with ID: {session_id}")
            
            return result
        else:
            error_msg = f"API Error: Status {response.status_code}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg = f"API Error: {error_data['detail']}"
            except Exception:
                error_msg = f"API Error: {response.text}"
            
            console.print(f"{error_msg}", style="bold red")
            if debug_mode:
                console.print(f"Response content: {response.text}")
            
            return {}
    except Exception as e:
        console.print(f"Error getting chat: {str(e)}", style="bold red")
        if debug_mode:
            import traceback
            console.print(traceback.format_exc())
        return {}

def delete_chat(session_id: str) -> bool:
    """Delete a specific chat by ID using the API."""
    try:
        # Check if debug mode is enabled either via settings or directly from environment variable
        debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (os.environ.get("AM_LOG_LEVEL") == "DEBUG")
        
        # Define the API endpoint with the correct prefix
        endpoint = get_api_endpoint(f"chats/{session_id}")
        
        # Only show endpoint in debug mode
        if debug_mode:
            console.print(f"Using endpoint for DELETE: {endpoint}")
        
        # Prepare headers with API key
        headers = {}
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY
            
            if debug_mode:
                masked_key = f"{settings.AM_API_KEY[:4]}...{settings.AM_API_KEY[-4:]}" if len(settings.AM_API_KEY) > 8 else "****"
                console.print(f"Using API key: {masked_key}")
        
        # Make the API request
        response = requests.delete(endpoint, headers=headers, timeout=30)
        
        # Check response status
        if response.status_code == 200:
            if debug_mode:
                console.print(f"Successfully deleted chat with ID: {session_id}")
            
            return True
        else:
            error_msg = f"API Error: Status {response.status_code}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg = f"API Error: {error_data['detail']}"
            except Exception:
                error_msg = f"API Error: {response.text}"
            
            console.print(f"{error_msg}", style="bold red")
            if debug_mode:
                console.print(f"Response content: {response.text}")
            
            return False
    except Exception as e:
        console.print(f"Error deleting chat: {str(e)}", style="bold red")
        if debug_mode:
            import traceback
            console.print(traceback.format_exc())
        return False 
```

# src/cli/agent/create.py

```py
"""
Command for creating new agents from templates.
"""
import os
import shutil
from pathlib import Path
import typer
from typing import List
from src.config import settings

# Create the app for the create command
create_app = typer.Typer(no_args_is_help=True)

def get_available_categories() -> List[str]:
    """Get available agent categories from the agents directory."""
    try:
        agents_dir = Path("src/agents")
        if not agents_dir.exists() or not agents_dir.is_dir():
            if settings.AM_LOG_LEVEL == "DEBUG":
                typer.echo(f"Agents directory not found: {agents_dir}")
            return []
        
        # Get all directories in the agents directory, excluding 'models' and '__pycache__'
        categories = [d.name for d in agents_dir.iterdir() 
                     if d.is_dir() and d.name not in ["models", "__pycache__"]]
        
        if settings.AM_LOG_LEVEL == "DEBUG":
            typer.echo(f"Found agent categories: {categories}")
        
        return categories
    except Exception as e:
        if settings.AM_LOG_LEVEL == "DEBUG":
            typer.echo(f"Error getting available categories: {str(e)}")
        return []

def get_available_templates(category: str) -> List[str]:
    """Get available templates for a specific agent category."""
    try:
        category_dir = Path(f"src/agents/{category}")
        if not category_dir.exists() or not category_dir.is_dir():
            if settings.AM_LOG_LEVEL == "DEBUG":
                typer.echo(f"Category directory not found: {category_dir}")
            return []
        
        # Get all directories in the category directory, excluding '__pycache__'
        templates = [d.name for d in category_dir.iterdir() 
                    if d.is_dir() and d.name != "__pycache__"]
        
        if settings.AM_LOG_LEVEL == "DEBUG":
            typer.echo(f"Found templates for category '{category}': {templates}")
        
        return templates
    except Exception as e:
        if settings.AM_LOG_LEVEL == "DEBUG":
            typer.echo(f"Error getting available templates for category '{category}': {str(e)}")
        return []

@create_app.callback()
def create_callback(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    Create new agents from templates.
    
    This command provides tools to create new agents from existing templates.
    Use 'list' to see available templates, or 'agent' to create a new agent.
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"

@create_app.command("agent")
def create_agent(
    name: str = typer.Option(..., "--name", "-n", help="Name of the new agent to create"),
    category: str = typer.Option("simple", "--category", "-c", help="Category folder to use (e.g., 'simple', 'graph')"),
    template: str = typer.Option("simple_agent", "--template", "-t", help="Template folder to use as base (e.g., 'simple_agent', 'notion_agent')")
):
    """
    Create a new agent by cloning an existing agent template.
    
    The agent will be created in the specified category folder (e.g., simple, graph).
    The template should be the name of an existing agent within that category.
    By default, it uses the simple_agent template in the simple category.
    """
    # Define the agents directory and category paths
    agents_dir = Path(__file__).resolve().parent.parent.parent.parent / 'src' / 'agents'
    category_dir = agents_dir / category
    
    # Ensure category exists
    available_categories = get_available_categories()
    if category not in available_categories:
        typer.echo(f"Error: Category '{category}' not found. Available categories: {', '.join(available_categories)}")
        raise typer.Exit(code=1)
    
    # Define the destination folder inside the category
    destination = category_dir / f"{name}_agent"
    
    # Check if destination already exists
    if destination.exists():
        typer.echo(f"Error: Folder {destination} already exists.")
        raise typer.Exit(code=1)

    # Get available templates in the category
    available_templates = get_available_templates(category)
    if not available_templates:
        typer.echo(f"Error: No templates found in category '{category}'.")
        raise typer.Exit(code=1)
    
    if template not in available_templates:
        typer.echo(f"Error: Template '{template}' not found in category '{category}'. Available templates: {', '.join(available_templates)}")
        raise typer.Exit(code=1)

    # Define the template folder
    template_path = category_dir / template
    if not template_path.exists() or not template_path.is_dir():
        typer.echo(f"Error: Template folder {template_path} does not exist.")
        raise typer.Exit(code=1)

    # Copy the template folder to the destination folder
    shutil.copytree(template_path, destination)

    # Get the base names without _agent suffix for class naming
    template_base = template.replace('_agent', '')
    name_base = name
    
    # Compute the new agent class name and the template class name
    new_agent_class = ''.join(word.capitalize() for word in name.split('_')) + "Agent"
    template_class = ''.join(word.capitalize() for word in template_base.split('_')) + "Agent"
    create_func_name = f"create_{name}_agent"
    template_func_name = f"create_{template_base}_agent"

    # Recursively update file contents and filenames in the destination folder
    for root, dirs, files in os.walk(destination, topdown=False):
        for file in files:
            file_path = Path(root) / file
            # Skip binary files like __pycache__
            if '__pycache__' in str(file_path) or file.endswith('.pyc'):
                continue
                
            # Attempt to read file as text
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace class names and function names, but preserve config requirements
                new_content = content
                
                # Handle various import patterns
                # 1. Direct imports from the template's module
                for potential_import_path in [
                    f"from src.agents.{template}",
                    f"from src.agents.{template_base}_agent",
                    f"from src.agents.{category}.{template}",
                    f"from src.agents.{category}.{template_base}_agent",
                    f"import src.agents.{template}",
                    f"import src.agents.{template_base}_agent",
                    f"import src.agents.{category}.{template}",
                    f"import src.agents.{category}.{template_base}_agent",
                ]:
                    replacement = potential_import_path.replace(
                        template if template in potential_import_path else template_base + "_agent", 
                        f"{name}_agent"
                    )
                    new_content = new_content.replace(potential_import_path, replacement)
                
                # 2. Handle any other template references in import statements
                new_content = new_content.replace(
                    f"src.agents.{template}.agent",
                    f"src.agents.{category}.{name}_agent.agent"
                )
                new_content = new_content.replace(
                    f"src.agents.{template_base}_agent.agent",
                    f"src.agents.{category}.{name}_agent.agent"
                )
                new_content = new_content.replace(
                    f"src.agents.{category}.{template}.agent",
                    f"src.agents.{category}.{name}_agent.agent"
                )
                new_content = new_content.replace(
                    f"src.agents.{category}.{template_base}_agent.agent",
                    f"src.agents.{category}.{name}_agent.agent"
                )
                
                # Handle references to simple_agent specifically (common in many templates)
                if template != "simple_agent" and template_base != "simple":
                    new_content = new_content.replace(
                        "src.agents.simple.simple_agent",
                        f"src.agents.{category}.{name}_agent"
                    )
                    new_content = new_content.replace(
                        f"src.agents.{category}.simple_agent",
                        f"src.agents.{category}.{name}_agent"
                    )
                
                # Handle direct simple_agent imports in any category
                new_content = new_content.replace(
                    "from src.agents.test_agent.simple_agent",
                    f"from src.agents.{category}.{name}_agent"
                )
                
                # Only replace exact class name matches (with word boundaries)
                new_content = new_content.replace(f" {template_class}", f" {new_agent_class}")
                new_content = new_content.replace(f"({template_class}", f"({new_agent_class}")
                new_content = new_content.replace(f"[{template_class}", f"[{new_agent_class}")
                new_content = new_content.replace(f":{template_class}", f":{new_agent_class}")
                new_content = new_content.replace(f"\"{template_class}", f"\"{new_agent_class}")
                new_content = new_content.replace(f"'{template_class}", f"'{new_agent_class}")
                
                # Replace function names
                new_content = new_content.replace(template_func_name, create_func_name)
                
                # Special handling for __init__.py to update docstrings
                if file == "__init__.py":
                    new_content = new_content.replace(
                        f"Create and initialize a {template_class} instance",
                        f"Create and initialize a {new_agent_class} instance"
                    )
                
                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
            except Exception as e:
                typer.echo(f"Warning: Could not process file {file_path}: {str(e)}")
                continue

            # Rename file if it contains the template name
            if template_base in file:
                new_file = file.replace(template_base, name)
                new_file_path = Path(root) / new_file
                file_path.rename(new_file_path)

        # Rename directories if needed
        for dir_name in dirs:
            if template_base in dir_name:
                old_dir = Path(root) / dir_name
                new_dir = Path(root) / dir_name.replace(template_base, name)
                os.rename(old_dir, new_dir)

    typer.echo(f"Agent '{name}' created successfully in {destination} (based on {template} template in {category} category).")
    typer.echo(f"The new agent class is named '{new_agent_class}'.")
    typer.echo(f"The initialization function is named '{create_func_name}'.")
    typer.echo("\nYou can now:")
    typer.echo(f"1. Edit {destination}/prompts/prompt.py to customize the agent's system prompt")
    typer.echo(f"2. Edit {destination}/agent.py to customize agent behavior")
    typer.echo(f"3. Edit {destination}/__init__.py to customize initialization config")

@create_app.command()
def list_templates():
    """
    List all available agent templates in all categories.
    
    This command shows all available templates that can be used 
    to create new agents using the 'agent create' command.
    """
    categories = get_available_categories()
    
    if not categories:
        typer.echo("No agent categories found. Your installation might be incomplete.")
        return
    
    typer.echo("\nAvailable Agent Templates by Category:")
    typer.echo("======================================")
    
    for category in sorted(categories):
        templates = get_available_templates(category)
        if templates:
            typer.echo(f"\n[Category: {category}]")
            for i, template in enumerate(sorted(templates), 1):
                typer.echo(f"  {i}. {template}")
    
    typer.echo("\nTo create a new agent using a template, run:")
    typer.echo("  automagik-agents agent create agent --name my_agent --category simple --template simple_agent")
    typer.echo("\nWhere 'simple' is the category and 'simple_agent' is the template name.")

@create_app.command()
def list_categories():
    """
    List all available agent categories.
    
    Agent categories are top-level directories that organize
    related agent templates.
    """
    categories = get_available_categories()
    
    if not categories:
        typer.echo("No agent categories found. Your installation might be incomplete.")
        return
    
    typer.echo("\nAvailable Agent Categories:")
    typer.echo("==========================")
    
    for i, category in enumerate(sorted(categories), 1):
        typer.echo(f"{i}. {category}")
    
    typer.echo("\nTo see templates in a specific category, use:")
    typer.echo("  automagik-agents agent create list-templates")

@create_app.command()
def list():
    """
    List all available agent templates and categories.
    
    This is a shortcut for the list-templates command.
    """
    list_templates() 
```

# src/cli/agent/run.py

```py
"""
Command for running a single message through an agent.

This command provides a simplified interface to send a single message to an agent.
It's designed for quick tests and integrations.
"""

import sys
import asyncio
import json
import typer
from typing import Dict, List, Optional, Any
import requests
from pathlib import Path
import os
import logging
import re
import argparse
import cmd
import tempfile
import httpx

from src.config import settings
from src.agents.models.agent_factory import AgentFactory
from src.agents.models.dependencies import SimpleAgentDependencies
from src.agents.simple.simple_agent.agent import SimpleAgent
from src.constants import (
    DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS
)

# Create app for the run command
run_app = typer.Typer(no_args_is_help=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@run_app.callback()
def run_callback(
    debug: bool = typer.Option(
        False, "--debug", help="Enable debug mode", is_flag=True, hidden=True
    ),
):
    """
    Run a single message through an agent and get the response.

    Use the 'message' command with required options:
      automagik-agents agent run message --agent <agent_name> --message "Your message here"

    Example:
      automagik-agents agent run message --agent simple --message "Hello, how are you?"

    For multimodal content:
      automagik-agents agent run message --agent simple --message "Describe this image" --image-url "https://example.com/image.jpg"
      automagik-agents agent run message --agent simple --message "What does this audio say?" --audio-url "https://example.com/audio.mp3"
      automagik-agents agent run message --agent simple --message "Summarize this document" --document-url "https://example.com/document.pdf"
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"


def get_api_endpoint(path: str) -> str:
    """Build a consistent API endpoint URL with the correct prefix."""
    # Ensure the path doesn't start with a slash
    if path.startswith("/"):
        path = path[1:]

    # Always use /api/v1/ prefix
    if not path.startswith("api/v1/"):
        path = f"api/v1/{path}"

    # Build the full URL with server from settings
    # The host and port values are stored in AM_HOST and AM_PORT
    server = f"http://{settings.AM_HOST}:{settings.AM_PORT}"
    if not server.endswith('/'):
        server = f"{server}/"
    url = f"{server}{path}"

    return url


def get_available_agents() -> List[Dict[str, Any]]:
    """Get a list of available agents using the API."""
    # Check if debug mode is enabled either via settings or directly from environment variable
    debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (
        os.environ.get("AM_LOG_LEVEL") == "DEBUG"
    )

    try:
        # Define the API endpoint for listing agents
        endpoint = get_api_endpoint("agent/list")
        if debug_mode:
            typer.echo(f"Getting agents from: {endpoint}")

        # Prepare headers with API key if available
        headers = {}
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY

        # Make the API request
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)

            # Check if the request was successful
            if response.status_code == 200:
                agents = response.json()
                if debug_mode:
                    typer.echo(f"Successfully retrieved {len(agents)} agents")

                # Convert the API response to a format compatible with the rest of the code
                for agent in agents:
                    # Ensure id field is present (use name as fallback)
                    if "id" not in agent:
                        agent["id"] = agent["name"]

                    # If description is missing, provide a default
                    if "description" not in agent or not agent["description"]:
                        agent["description"] = (
                            f"Agent of type {agent.get('type', 'unknown')}"
                        )

                    # If model is missing, provide a default
                    if "model" not in agent or not agent["model"]:
                        agent["model"] = "openai:gpt-4o-mini"  # Updated default model

                return agents
            else:
                typer.echo(
                    f"Error getting agents: HTTP {response.status_code}", err=True
                )
                if debug_mode:
                    typer.echo(f"Response: {response.text}", err=True)
                return []
        except requests.exceptions.ConnectionError:
            typer.echo(
                f"Connection error: Could not connect to API server at {endpoint}",
                err=True,
            )
            return []
    except Exception as e:
        typer.echo(f"Error getting agents from API: {str(e)}", err=True)
        return []


async def get_user_by_id(user_id: int) -> Dict[str, Any]:
    """Get user data from the API by ID."""
    # Check if debug mode is enabled either via settings or directly from environment variable
    debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (
        os.environ.get("AM_LOG_LEVEL") == "DEBUG"
    )

    try:
        # Define the API endpoint
        endpoint = get_api_endpoint(f"users/{user_id}")
        if debug_mode:
            typer.echo(f"Getting user data from: {endpoint}")

        # Prepare headers with API key if available
        headers = {}
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY

        # Make the API request
        response = requests.get(endpoint, headers=headers, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            user_data = response.json()
            if debug_mode:
                typer.echo(f"Successfully retrieved user {user_id} from API")
            return user_data
        else:
            if debug_mode:
                typer.echo(
                    f"Error getting user by ID {user_id}: HTTP {response.status_code}"
                )
                typer.echo("Using fallback user data")
            # Return fallback data
            return {
                "id": user_id,
                "email": f"user{user_id}@example.com",
                "name": f"User {user_id}",
            }
    except Exception as e:
        if debug_mode:
            typer.echo(f"Error getting user from API: {str(e)}")
            typer.echo("Using fallback user data")
        # Return fallback data
        return {
            "id": user_id,
            "email": f"user{user_id}@example.com",
            "name": f"User {user_id}",
        }


async def run_agent(
    agent_name: str, input_message: str, session_name: str = None, user_id: int = 1,
    multimodal_content: Dict[str, str] = None
) -> dict:
    """Run the agent with the given message using the API."""
    try:
        # Check if debug mode is enabled either via settings or directly from environment variable
        debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (
            os.environ.get("AM_LOG_LEVEL") == "DEBUG"
        )

        # Define the API endpoint with the correct prefix
        endpoint = get_api_endpoint(f"agent/{agent_name}/run")

        # Only show endpoint in debug mode
        if debug_mode:
            typer.echo(f"Using endpoint: {endpoint}")

        # Prepare the payload according to the API's expected format
        payload = {
            "message_content": input_message,
            "user_id": user_id,
            "context": {"debug": debug_mode},
            "session_origin": "cli",
        }

        # Add multimodal content if provided
        if multimodal_content:
            payload["multimodal_content"] = multimodal_content

            if debug_mode:
                typer.echo(f"Adding multimodal content: {json.dumps(multimodal_content, indent=2)}")

        # Add session_name if provided
        if session_name:
            payload["session_name"] = session_name
            
            # Check if this is an existing session, so we can preserve its system_prompt
            try:
                # Make a call to get the session info first if it's an existing session
                session_endpoint = get_api_endpoint(f"sessions/{session_name}")
                session_response = requests.get(
                    session_endpoint, 
                    headers={"x-api-key": settings.AM_API_KEY} if settings.AM_API_KEY else {},
                    timeout=10
                )
                if session_response.status_code == 200:
                    session_data = session_response.json()
                    if session_data.get("exists", False):
                        # It's an existing session, add preserve_system_prompt flag
                        payload["preserve_system_prompt"] = True
                        if debug_mode:
                            typer.echo("Adding preserve_system_prompt flag for existing session")
            except Exception as e:
                if debug_mode:
                    typer.echo(f"Error checking session: {str(e)}")

        if debug_mode:
            typer.echo(f"Request payload: {json.dumps(payload, indent=2)}")

        # Prepare headers with API key
        headers = {"Content-Type": "application/json"}

        # Add API key to headers if available
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY

            if debug_mode:
                masked_key = (
                    f"{settings.AM_API_KEY[:4]}...{settings.AM_API_KEY[-4:]}"
                    if len(settings.AM_API_KEY) > 8
                    else "****"
                )
                typer.echo(f"Using API key: {masked_key}")

        # Make the API request
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)

        # Check response status
        if response.status_code == 200:
            result = response.json()
            if debug_mode:
                typer.echo(f"API Response: {json.dumps(result, indent=2)}")
                if "session_id" in result:
                    typer.echo(f"Session ID from response: {result['session_id']}")
            return result
        else:
            error_msg = f"API Error: Status {response.status_code}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg = f"API Error: {error_data['detail']}"

                    # Detect specific errors related to session name uniqueness
                    if (
                        "duplicate key value violates unique constraint"
                        in error_data.get("detail", "")
                        and "sessions_name_key" in error_data.get("detail", "")
                    ):
                        error_msg = f"Session name '{session_name}' is already in use. Please use a different session name."
            except Exception:
                error_msg = f"API Error: {response.text}"

            typer.echo(f"{error_msg}", err=True)
            return {"error": error_msg}

    except Exception as e:
        error_msg = f"Error running agent: {str(e)}"
        typer.echo(f"{error_msg}", err=True)
        return {"error": error_msg}


def display_message(
    message: str, role: str, tool_calls: List = None, tool_outputs: List = None
) -> None:
    """Display a message in plain text format."""
    # Format tool usage in a simple way if present
    if role == "assistant" and tool_calls:
        tool_usage = []

        for i, tool_call in enumerate(tool_calls):
            tool_name = tool_call.get("tool_name", "Unknown Tool")
            tool_args = tool_call.get("args", {})

            # Format tool arguments
            args_str = ""
            if tool_args:
                if isinstance(tool_args, dict) and len(tool_args) > 0:
                    args_str = ", ".join(f"{k}={v}" for k, v in tool_args.items())
                else:
                    args_str = str(tool_args)

            # Simple tool call display
            tool_call_str = f"{tool_name}({args_str})"

            # Find and display matching output if available
            if tool_outputs:
                matching_output = next(
                    (
                        output
                        for output in tool_outputs
                        if output.get("tool_call_id") == tool_call.get("tool_call_id")
                    ),
                    None,
                )
                if matching_output:
                    output_content = matching_output.get("content", "")
                    # Combine tool call and result
                    tool_call_str = f"{tool_call_str} → {output_content}"

            tool_usage.append(tool_call_str)

        if tool_usage:
            typer.echo("\n".join([f"[Tool] {tool}" for tool in tool_usage]))

    # Print the message with role prefix
    if message.strip():
        typer.echo(f"{role}: {message}")


async def process_single_message(
    agent_name: str, message: str, session_name: str = None, user_id: int = 1,
    multimodal_content: Dict[str, str] = None
) -> None:
    """Run a single message through an agent and display the response.
    
    Args:
        agent_name: Name of the agent to use
        message: Message to send to the agent
        session_name: Optional session name for continuity
        user_id: User ID to associate with this run
        multimodal_content: Optional multimodal content dictionary
    """
    # Check if debug mode is enabled
    debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (
        os.environ.get("AM_LOG_LEVEL") == "DEBUG"
    )

    if debug_mode:
        typer.echo(f"Processing message: {message}")
        if multimodal_content:
            typer.echo(f"With multimodal content: {json.dumps(multimodal_content, indent=2)}")

    # Extract model override if provided
    model_override = None
    if multimodal_content and "model_override" in multimodal_content:
        model_override = multimodal_content["model_override"]
        # Remove the model_override from multimodal_content as it's not actual content
        del multimodal_content["model_override"]
        if debug_mode:
            typer.echo(f"Using model override: {model_override}")
    
    # Use API to run the agent
    try:
        if debug_mode:
            typer.echo(f"Using API at {settings.AM_HOST}:{settings.AM_PORT}")
        
        response = await run_agent(
            agent_name, message, session_name, user_id,
            multimodal_content=multimodal_content
        )
        
        # Check if the response is valid
        if response and "message" in response:
            # Display the message with proper formatting
            display_message(
                message=response["message"],
                role="assistant",
                tool_calls=response.get("tool_calls", []),
                tool_outputs=response.get("tool_outputs", [])
            )
        else:
            typer.echo("Error: Invalid response from API", err=True)
            if debug_mode and response:
                typer.echo(f"API response: {json.dumps(response, indent=2)}", err=True)
            
    except Exception as e:
        typer.echo(f"Error running agent through API: {str(e)}", err=True)
        if debug_mode:
            import traceback
            typer.echo(traceback.format_exc(), err=True)


@run_app.command()
def message(
    agent: str = typer.Option(..., "--agent", "-a", help="Agent to use"),
    session: Optional[str] = typer.Option(
        None, "--session", "-s", help="Session name to use/create"
    ),
    user: int = typer.Option(1, "--user", "-u", help="User ID to use"),
    message: Optional[str] = typer.Option(
        None,
        "--message",
        "-m",
        help="Message to send (if not provided, will read from stdin)",
    ),
    image_url: Optional[str] = typer.Option(None, "--image-url", help="URL to an image for multimodal processing"),
    audio_url: Optional[str] = typer.Option(None, "--audio-url", help="URL to an audio file for multimodal processing"),
    document_url: Optional[str] = typer.Option(None, "--document-url", help="URL to a document for multimodal processing"),
    model: Optional[str] = typer.Option(None, "--model", help="Model to use (overrides agent's default)"),
    debug: bool = typer.Option(
        False, "--debug", help="Enable debug mode", is_flag=True, hidden=True
    ),
):
    """
    Run a single message through an agent and get the response.

    This command sends a message to an agent and displays the response.
    It can include multimodal content like images, audio, and documents.

    Example:
      automagik-agents agent run message --agent simple --message "Hello, how are you?"
      automagik-agents agent run message --agent simple --message "Describe this image" --image-url "https://example.com/image.jpg"
      automagik-agents agent run message --agent simple --message "What does this audio say?" --audio-url "https://example.com/audio.mp3"
      automagik-agents agent run message --agent simple --message "Summarize this document" --document-url "https://example.com/document.pdf"
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"
        typer.echo(f"Debug mode enabled. Using endpoint: {settings.AM_HOST}:{settings.AM_PORT}")

    # If message is not provided, read from stdin
    if not message:
        typer.echo("Enter your message (Ctrl+D to submit):", err=True)
        message = ""
        for line in sys.stdin:
            message += line
        message = message.strip()
        if not message:
            typer.echo("Error: Message cannot be empty", err=True)
            sys.exit(1)

    # Ensure agent name is valid
    if not agent:
        typer.echo("Error: Agent name is required", err=True)
        sys.exit(1)

    # Prepare multimodal content
    multimodal_content = {}
    if image_url:
        multimodal_content["image_url"] = image_url
    if audio_url:
        multimodal_content["audio_url"] = audio_url
    if document_url:
        multimodal_content["document_url"] = document_url

    # If model is specified, update the agent's model
    if model:
        # Setting the model requires API access, we'll include it in the request payload
        typer.echo(f"Using custom model: {model}")
        multimodal_content["model_override"] = model

    # Run the agent and display the response
    asyncio.run(
        process_single_message(
            agent, message, session_name=session, user_id=user, 
            multimodal_content=multimodal_content if multimodal_content else None
        )
    )


def list_available_agents() -> None:
    """Print a list of available agents."""
    agents = get_available_agents()

    if not agents:
        typer.echo(
            "Error: No agents available or could not connect to the API.", err=True
        )
        typer.echo("\nPossible reasons:")
        typer.echo("1. The server might not be running. Start it with:")
        typer.echo("     automagik-agents api start")
        typer.echo("2. Your API server could be running on a different host/port.")
        typer.echo(f"   Current server setting: {settings.AM_HOST}:{settings.AM_PORT}")
        typer.echo("3. You might not have added any agents yet.")

        typer.echo("\nTry creating an agent first:")
        typer.echo(
            "  automagik-agents agent create agent --name my_agent --template simple_agent"
        )

        typer.echo("\nOr check if you can access the API directly:")
        typer.echo(
            f"  curl http://{settings.AM_HOST}:{settings.AM_PORT}/api/v1/agent/list -H 'x-api-key: {settings.AM_API_KEY}'"
        )
        return

    typer.echo("\nAvailable Agents:")
    for i, agent in enumerate(agents, 1):
        name = agent.get("name", "Unknown")
        description = agent.get("description", "No description")
        model = agent.get("model", "openai:gpt-4o-mini")  # Updated default model

        typer.echo(f"{i}. {name} - {description} (Model: {model})")

    typer.echo("\nUse the agent name with the run command:")
    typer.echo(
        '  automagik-agents agent run message --agent <agent_name> --message "Your message here"'
    )
    typer.echo("\nFor multimodal content:")
    typer.echo(f"  automagik-agents agent run message --agent <agent_name> --message \"Describe this image\" --image-url \"https://example.com/image.jpg\"")
    typer.echo(f"  automagik-agents agent run message --agent <agent_name> --message \"Transcribe this audio\" --audio-url \"https://example.com/audio.mp3\"")
    typer.echo(f"  automagik-agents agent run message --agent <agent_name> --message \"Summarize this document\" --document-url \"https://example.com/document.pdf\"")


@run_app.command()
def list():
    """
    List all available agents that can be used for running messages.
    """
    list_available_agents()

```

# src/cli/api.py

```py
"""
API server management commands for Automagik Agents.
"""
import os
import typer
import uvicorn
from typing import Optional
from src.config import load_settings

# Create the API command group
api_app = typer.Typer()

@api_app.callback()
def api_callback(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    API server management commands.
    
    Use the 'start' command to launch the API server.
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"

@api_app.command("start")
def start_api(
    host: str = typer.Option(None, "--host", "-h", help="Host to bind the server to (overrides AM_HOST from .env)"),
    port: int = typer.Option(None, "--port", "-p", help="Port to bind the server to (overrides AM_PORT from .env)"),
    reload: bool = typer.Option(None, "--reload", help="Enable auto-reload on code changes (default: auto-enabled in development mode)"),
    workers: Optional[int] = typer.Option(None, "--workers", "-w", help="Number of worker processes"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode (sets LOG_LEVEL to DEBUG)", is_flag=True, hidden=True)
):
    """
    Start the FastAPI server with uvicorn using settings from .env
    """
    # Set debug mode if requested
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"
        
    # Load settings from .env
    settings = load_settings()
    
    # Use command line arguments if provided, otherwise use settings from .env
    final_host = host or settings.AM_HOST
    final_port = port or settings.AM_PORT

    # If reload is not explicitly set, auto-enable it in development mode
    if reload is None:
        from src.config import Environment
        reload = settings.AM_ENV == Environment.DEVELOPMENT
    
    # Log the reload status
    reload_status = "enabled" if reload else "disabled"
    typer.echo(f"Starting API server on {final_host}:{final_port} (auto-reload: {reload_status})")
    
    uvicorn.run(
        "src.main:app",
        host=final_host,
        port=final_port,
        reload=reload,
        workers=workers
    ) 
```

# src/cli/db.py

```py
"""
Database management commands for Automagik Agents.
"""
import os
import typer
import logging
from dotenv import load_dotenv
import psycopg2

# Create the database command group
db_app = typer.Typer()

@db_app.callback()
def db_callback(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    Database management commands.
    
    Use these commands to initialize, backup, and manage the database.
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"

@db_app.command("init")
def db_init(
    force: bool = typer.Option(False, "--force", "-f", help="Force initialization even if database already exists")
):
    """
    Initialize the database if it doesn't exist yet.
    
    This command creates the database and required tables if they don't exist already.
    Use --force to recreate tables even if they already exist.
    """
    typer.echo("Initializing database...")
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger("db_init")
    
    # Load environment variables
    load_dotenv()
    
    # Get database connection parameters from environment
    db_host = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost") 
    db_port = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME", "automagik_agents")
    db_user = os.getenv("POSTGRES_USER") or os.getenv("DB_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD", "postgres")
    
    # Try to parse from DATABASE_URL if available
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        try:
            import urllib.parse
            parsed = urllib.parse.urlparse(database_url)
            db_host = parsed.hostname or db_host
            db_port = str(parsed.port) if parsed.port else db_port
            db_name = parsed.path.lstrip('/') or db_name
            db_user = parsed.username or db_user
            db_password = parsed.password or db_password
        except Exception as e:
            logger.warning(f"Error parsing DATABASE_URL: {str(e)}")
    
    typer.echo(f"Using database: {db_host}:{db_port}/{db_name}")
    
    # First, connect to PostgreSQL to check if database exists
    try:
        # Create a connection to PostgreSQL (without a specific database)
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            dbname="postgres"
        )
        conn.autocommit = True  # Needed to create database
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"✅ Created database: {db_name}")
        else:
            logger.info(f"Database already exists: {db_name}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL or create database: {e}")
        return
    
    # Now connect to the target database and create tables
    create_required_tables(
        db_host, db_port, db_name, db_user, db_password, 
        logger=logger, force=force
    )
    
    if force:
        typer.echo("✅ Database initialization completed!")
    else:
        typer.echo("✅ Database verification completed!")

def create_required_tables(
    db_host, db_port, db_name, db_user, db_password,
    logger=None, force=False
):
    """Create required tables in the database."""
    if logger is None:
        logger = logging.getLogger("create_tables")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create users table if not exists
        if force:
            logger.info("Force mode enabled. Dropping existing tables...")
            # Drop tables in the correct order to respect foreign key constraints
            cursor.execute("DROP TABLE IF EXISTS memories CASCADE")
            cursor.execute("DROP TABLE IF EXISTS messages CASCADE")
            cursor.execute("DROP TABLE IF EXISTS sessions CASCADE")
            cursor.execute("DROP TABLE IF EXISTS users CASCADE")
            cursor.execute("DROP TABLE IF EXISTS agents CASCADE")
            logger.info("Existing tables dropped.")
        
        # Create the agents table
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'agents')")
        table_exists = cursor.fetchone()[0]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                type VARCHAR(50),
                model VARCHAR(255),
                description TEXT,
                version VARCHAR(50),
                config JSONB,
                active BOOLEAN DEFAULT TRUE,
                run_id INTEGER DEFAULT 0,
                system_prompt TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        if table_exists:
            logger.info("Verified agents table exists")
        else:
            logger.info("Created agents table")
        
        # Create the users table
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
        table_exists = cursor.fetchone()[0]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email TEXT,
                phone_number VARCHAR(50),
                user_data JSONB,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        if table_exists:
            logger.info("Verified users table exists")
        else:
            logger.info("Created users table")
        
        # Create the sessions table
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sessions')")
        table_exists = cursor.fetchone()[0]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id INTEGER REFERENCES users(id),
                agent_id INTEGER REFERENCES agents(id),
                name VARCHAR(255),
                platform VARCHAR(50),
                metadata JSONB,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW(),
                run_finished_at TIMESTAMPTZ
            )
        """)
        if table_exists:
            logger.info("Verified sessions table exists")
        else:
            logger.info("Created sessions table")
        
        # Create the messages table based on the actual schema
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'messages')")
        table_exists = cursor.fetchone()[0]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                session_id UUID REFERENCES sessions(id),
                user_id INTEGER REFERENCES users(id),
                agent_id INTEGER REFERENCES agents(id),
                role VARCHAR(20) NOT NULL,
                text_content TEXT,
                media_url TEXT,
                mime_type TEXT,
                message_type TEXT,
                raw_payload JSONB,
                tool_calls JSONB,
                tool_outputs JSONB,
                system_prompt TEXT,
                user_feedback TEXT,
                flagged TEXT,
                context JSONB,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        if table_exists:
            logger.info("Verified messages table exists")
        else:
            logger.info("Created messages table")
        
        # Create the memories table
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'memories')")
        table_exists = cursor.fetchone()[0]
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(255) NOT NULL,
                description TEXT,
                content TEXT,
                session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                agent_id INTEGER REFERENCES agents(id) ON DELETE CASCADE,
                read_mode VARCHAR(50),
                access VARCHAR(20),
                metadata JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        if table_exists:
            logger.info("Verified memories table exists")
        else:
            logger.info("Created memories table")
        
        # Create default user if needed
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0 or force:
            # Create default user
            cursor.execute("""
                INSERT INTO users (email, phone_number, user_data)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (
                "admin@automagik", 
                "88888888888", 
                '{"name": "Automagik Admin"}'
            ))
            user_id = cursor.fetchone()[0]
            logger.info(f"✅ Created default user with ID: {user_id}")
        
        cursor.close()
        conn.close()
        
        if force:
            logger.info("✅ All required tables created successfully!")
        else:
            logger.info("✅ Database schema verified successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False

@db_app.command("clear")
def db_clear(
    confirm: bool = typer.Option(False, "--yes", "-y", help="Confirm database clear without prompt"),
    no_default_user: bool = typer.Option(False, "--no-default-user", help="Skip creating the default user after clearing")
):
    """
    Clear all data from the database while preserving the schema.
    
    This command truncates all tables but keeps the database structure intact.
    WARNING: This will delete ALL data in the database. Use with caution!
    """
    if not confirm:
        confirmed = typer.confirm("⚠️ This will DELETE ALL DATA in the database but keep the schema. Are you sure?", default=False)
        if not confirmed:
            typer.echo("Database clear cancelled.")
            return
    
    typer.echo("Clearing all data from database...")
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger("db_clear")
    
    # Load environment variables
    load_dotenv()
    
    # Get database connection parameters from environment
    db_host = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost") 
    db_port = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME", "automagik_agents")
    db_user = os.getenv("POSTGRES_USER") or os.getenv("DB_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD", "postgres")
    
    # Try to parse from DATABASE_URL if available
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        try:
            import urllib.parse
            parsed = urllib.parse.urlparse(database_url)
            db_host = parsed.hostname or db_host
            db_port = str(parsed.port) if parsed.port else db_port
            db_name = parsed.path.lstrip('/') or db_name
            db_user = parsed.username or db_user
            db_password = parsed.password or db_password
        except Exception as e:
            logger.warning(f"Error parsing DATABASE_URL: {str(e)}")
    
    typer.echo(f"Using database: {db_host}:{db_port}/{db_name}")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Get all tables in the public schema
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)
        all_tables = [table[0] for table in cursor.fetchall()]
        
        if not all_tables:
            typer.echo("No tables found in database.")
            return
        
        typer.echo(f"Found {len(all_tables)} tables in the database")
        
        # Define table clearing order to respect foreign key constraints
        # If a table is not in this list, it will be cleared after the ordered ones
        table_order = [
            "memories",       # Clear first as it references sessions, users, and agents
            "messages",       # References sessions, users, and agents
            "sessions",       # References users and agents
            "users",          # Base table
            "agents"          # Base table
        ]
        
        # Sort tables based on defined order
        ordered_tables = []
        
        # First add tables in our defined order (if they exist in the database)
        for table in table_order:
            if table in all_tables:
                ordered_tables.append(table)
                all_tables.remove(table)
        
        # Then add any remaining tables
        ordered_tables.extend(all_tables)
        
        typer.echo("Clearing tables in the following order to respect foreign key constraints:")
        for i, table in enumerate(ordered_tables):
            typer.echo(f"  {i+1}. {table}")
        
        # Truncate each table in order
        for table_name in ordered_tables:
            typer.echo(f"  - Clearing table: {table_name}")
            try:
                # Try with CASCADE first, which will handle foreign key constraints
                try:
                    cursor.execute(f'TRUNCATE TABLE "{table_name}" CASCADE;')
                    typer.echo(f"    ✓ Table {table_name} cleared successfully (with CASCADE)")
                except Exception as e:
                    # If CASCADE fails, try without it
                    if "permission denied" in str(e):
                        try:
                            cursor.execute(f'TRUNCATE TABLE "{table_name}";')
                            typer.echo(f"    ✓ Table {table_name} cleared successfully")
                        except Exception as e2:
                            # If regular TRUNCATE fails too, try DELETE as a last resort
                            typer.echo(f"    ⚠️ TRUNCATE failed, trying DELETE FROM...")
                            cursor.execute(f'DELETE FROM "{table_name}";')
                            typer.echo(f"    ✓ Table {table_name} cleared using DELETE (might be slower)")
                    else:
                        raise e
            except Exception as e:
                typer.echo(f"    ✗ Failed to clear table {table_name}: {str(e)}")
        
        # Create default user if not exists
        if not no_default_user:
            cursor.execute("SELECT COUNT(*) FROM users WHERE id = 1")
            if cursor.fetchone()[0] == 0:
                logger.info("Creating default user...")
                cursor.execute("""
                    INSERT INTO users (id, email, created_at, updated_at)
                    VALUES (1, 'admin@automagik', NOW(), NOW())
                """)
                conn.commit()
                typer.echo("✅ Created default user (ID: 1)")
        else:
            typer.echo("Skipping default user creation as requested")
        
        # Close the connection
        cursor.close()
        conn.close()
        
        typer.echo("✅ All data has been cleared from the database!")
        
    except Exception as e:
        logger.error(f"❌ Failed to clear database: {e}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False 
```

# src/config.py

```py
import os
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import urllib.parse
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Warning: python-dotenv is not installed. Environment variables may not be loaded from .env file.")
    load_dotenv = lambda: None

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

class Settings(BaseSettings):
    # Authentication
    AM_API_KEY: str = Field(..., description="API key for authenticating requests")

    # OpenAI
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key for agent operations")

    # Notion (Optional)
    NOTION_TOKEN: Optional[str] = Field(None, description="Notion integration token")

    # BlackPearl, Omie, Google Drive, Evolution (Optional)
    BLACKPEARL_TOKEN: Optional[str] = Field(None, description="BlackPearl API token")
    OMIE_TOKEN: Optional[str] = Field(None, description="Omie API token")
    GOOGLE_DRIVE_TOKEN: Optional[str] = Field(None, description="Google Drive API token")
    EVOLUTION_TOKEN: Optional[str] = Field(None, description="Evolution API token")

    # BlackPearl API URL and DB URI
    BLACKPEARL_API_URL: Optional[str] = Field(None, description="BlackPearl API URL")
    BLACKPEARL_DB_URI: Optional[str] = Field(None, description="BlackPearl database URI")

    # Discord
    DISCORD_BOT_TOKEN: str = Field(..., description="Discord bot token for authentication")

    # Database (PostgreSQL)
    DATABASE_URL: str = Field("postgresql://postgres:postgres@localhost:5432/automagik", 
                          description="PostgreSQL connection string")
    POSTGRES_HOST: str = Field("localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(5432, description="PostgreSQL port")
    POSTGRES_USER: str = Field("postgres", description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field("postgres", description="PostgreSQL password")
    POSTGRES_DB: str = Field("automagik", description="PostgreSQL database name")
    POSTGRES_POOL_MIN: int = Field(1, description="Minimum connections in the pool")
    POSTGRES_POOL_MAX: int = Field(10, description="Maximum connections in the pool")

    # Server
    AM_PORT: int = Field(8881, description="Port to run the server on")
    AM_HOST: str = Field("0.0.0.0", description="Host to bind the server to")
    AM_ENV: Environment = Field(Environment.DEVELOPMENT, description="Environment (development, production, testing)")

    # Logging
    AM_LOG_LEVEL: LogLevel = Field(LogLevel.INFO, description="Logging level")
    AM_VERBOSE_LOGGING: bool = Field(False, description="Enable verbose logging with additional details")
    LOGFIRE_TOKEN: Optional[str] = Field(None, description="Logfire token for logging service")
    LOGFIRE_IGNORE_NO_CONFIG: bool = Field(True, description="Suppress Logfire warning if no token")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields in environment variables

def load_settings() -> Settings:
    """Load and validate settings from environment variables and .env file."""
    # Check if we're in debug mode (AM_LOG_LEVEL set to DEBUG)
    debug_mode = os.environ.get('AM_LOG_LEVEL', '').upper() == 'DEBUG'
    
    # Load environment variables from .env file
    try:
        load_dotenv(override=True)
        print(f"📝 .env file loaded from: {Path('.env').absolute()}")
    except Exception as e:
        print(f"⚠️ Error loading .env file: {str(e)}")

    # Debug DATABASE_URL only if in debug mode
    if debug_mode:
        print(f"🔍 DATABASE_URL from environment after dotenv: {os.environ.get('DATABASE_URL', 'Not set')}")

    # Strip comments from environment variables
    for key in os.environ:
        if isinstance(os.environ[key], str) and '#' in os.environ[key]:
            os.environ[key] = os.environ[key].split('#')[0].strip()
            if debug_mode:
                print(f"📝 Stripped comments from environment variable: {key}")

    try:
        # Explicitly set reload=True to ensure environment variables are reloaded
        settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
        
        # Debug DATABASE_URL after loading settings - only in debug mode
        if debug_mode:
            print(f"🔍 DATABASE_URL after loading settings: {settings.DATABASE_URL}")
        
        # Final check - if there's a mismatch, use the environment value
        env_db_url = os.environ.get('DATABASE_URL')
        if env_db_url and env_db_url != settings.DATABASE_URL:
            if debug_mode:
                print(f"⚠️ Overriding settings.DATABASE_URL with environment value")
            # This is a bit hacky but necessary to fix mismatches
            settings.DATABASE_URL = env_db_url
            if debug_mode:
                print(f"📝 Final DATABASE_URL: {settings.DATABASE_URL}")
                
        # We no longer print the detailed configuration here
        # This is now handled by the CLI's debug flag handler in src/cli/__init__.py
        
        return settings
    except Exception as e:
        print("❌ Error loading configuration:")
        print(f"   {str(e)}")
        raise

def mask_connection_string(conn_string: str) -> str:
    """Mask sensitive information in a connection string."""
    try:
        # Parse the connection string
        parsed = urllib.parse.urlparse(conn_string)
        
        # Create a masked version
        if parsed.password:
            # Replace password with asterisks
            masked_netloc = f"{parsed.username}:****@{parsed.hostname}"
            if parsed.port:
                masked_netloc += f":{parsed.port}"
                
            # Reconstruct the URL with masked password
            masked_url = urllib.parse.urlunparse((
                parsed.scheme,
                masked_netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
            return masked_url
        
        return conn_string  # No password to mask
    except Exception:
        # If parsing fails, just show the first and last few characters
        return f"{conn_string[:10]}...{conn_string[-10:]}"

# Create a global settings instance
settings = load_settings()
```

# src/constants.py

```py
"""Constants for the Automagik Agents project.

This module defines constants that are used throughout the project.
Centralizing these values makes it easier to maintain and update the codebase.
"""

# Default model settings
DEFAULT_MODEL = "openai:gpt-4o-mini"  # Default model for all agents
DEFAULT_TEMPERATURE = 0.1  # Default temperature setting
DEFAULT_MAX_TOKENS = 4000  # Default max tokens for responses
DEFAULT_RETRIES = 3  # Default number of retries for API calls

# API settings
DEFAULT_API_TIMEOUT = 30  # Default timeout for API calls in seconds
DEFAULT_REQUEST_LIMIT = 5  # Default limit on number of API requests

# Session settings
DEFAULT_SESSION_PLATFORM = "automagik"  # Default platform for sessions 
```

# src/db/__init__.py

```py
"""Database module for Automagik Agents.

This module provides a clean repository pattern for database operations,
with specialized repository functions for each entity type.
"""

# Export models
from src.db.models import (
    Agent,
    User,
    Session,
    Memory,
    Message
)

# Export connection utilities
from src.db.connection import (
    get_connection_pool,
    get_db_connection,
    get_db_cursor,
    execute_query,
    execute_batch
)

# Export all repository functions
from src.db.repository import (
    # Agent repository
    get_agent,
    get_agent_by_name,
    list_agents,
    create_agent,
    update_agent,
    delete_agent,
    increment_agent_run_id,
    link_session_to_agent,
    
    # User repository
    get_user,
    get_user_by_email,
    get_user_by_identifier,
    list_users,
    create_user,
    update_user,
    delete_user,
    ensure_default_user_exists,
    
    # Session repository
    get_session,
    get_session_by_name,
    list_sessions,
    create_session,
    update_session,
    delete_session,
    finish_session,
    update_session_name_if_empty,
    
    # Message repository
    get_message,
    list_messages,
    count_messages,
    create_message,
    update_message,
    delete_message,
    delete_session_messages,
    get_system_prompt,
    
    # Memory repository
    get_memory,
    get_memory_by_name,
    list_memories,
    create_memory,
    update_memory,
    delete_memory
)
```

# src/db/connection.py

```py
"""Database connection management and query utilities."""

import logging
import os
import time
import urllib.parse
import uuid
from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import psycopg2
import psycopg2.extensions
from psycopg2.extras import RealDictCursor, execute_values
from psycopg2.pool import ThreadedConnectionPool

from src.config import settings

# Configure logger
logger = logging.getLogger(__name__)

# Connection pool for database connections
_pool: Optional[ThreadedConnectionPool] = None

# Register UUID adapter for psycopg2
psycopg2.extensions.register_adapter(uuid.UUID, lambda u: psycopg2.extensions.AsIs(f"'{u}'"))


def generate_uuid() -> uuid.UUID:
    """Safely generate a new UUID.
    
    This function ensures that the uuid module is properly accessed
    and not shadowed by local variables.
    
    Returns:
        A new UUID4 object
    """
    return uuid.uuid4()


def safe_uuid(value: Any) -> Any:
    """Convert UUID objects to strings for safe database use.
    
    This is a utility function for cases where direct SQL queries are used
    instead of repository functions. It ensures UUID objects are properly
    converted to strings to prevent adaptation errors.
    
    Args:
        value: The value to convert if it's a UUID
        
    Returns:
        String representation of UUID or the original value
    """
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


def get_db_config() -> Dict[str, Any]:
    """Get database configuration from connection string or individual settings."""
    # Try to use DATABASE_URL first
    if settings.DATABASE_URL:
        try:
            # Parse the database URL
            env_db_url = os.environ.get("DATABASE_URL")
            actual_db_url = env_db_url if env_db_url else settings.DATABASE_URL
            parsed = urllib.parse.urlparse(actual_db_url)

            dbname = parsed.path.lstrip("/")

            return {
                "host": parsed.hostname,
                "port": parsed.port,
                "user": parsed.username,
                "password": parsed.password,
                "database": dbname,
                "client_encoding": "UTF8",  # Explicitly set client encoding to UTF8
            }
        except Exception as e:
            logger.warning(
                f"Failed to parse DATABASE_URL: {str(e)}. Falling back to individual settings."
            )

    # Fallback to individual settings
    return {
        "host": settings.POSTGRES_HOST,
        "port": settings.POSTGRES_PORT,
        "user": settings.POSTGRES_USER,
        "password": settings.POSTGRES_PASSWORD,
        "database": settings.POSTGRES_DB,
        "client_encoding": "UTF8",  # Explicitly set client encoding to UTF8
    }


def get_connection_pool() -> ThreadedConnectionPool:
    """Get or create a database connection pool."""
    global _pool

    if _pool is None:
        config = get_db_config()
        max_retries = 5
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                min_conn = getattr(settings, "POSTGRES_POOL_MIN", 1)
                max_conn = getattr(settings, "POSTGRES_POOL_MAX", 10)

                logger.info(
                    f"Connecting to PostgreSQL at {config['host']}:{config['port']}/{config['database']} with UTF8 encoding..."
                )

                # Can either connect with individual params or with a connection string
                if settings.DATABASE_URL and attempt == 0:
                    try:
                        # Add client_encoding to the connection string if not already present
                        dsn = settings.DATABASE_URL
                        if "client_encoding" not in dsn.lower():
                            if "?" in dsn:
                                dsn += "&client_encoding=UTF8"
                            else:
                                dsn += "?client_encoding=UTF8"

                        _pool = ThreadedConnectionPool(
                            minconn=min_conn, maxconn=max_conn, dsn=dsn
                        )
                        logger.info(
                            "Successfully connected to PostgreSQL using DATABASE_URL with UTF8 encoding"
                        )
                        # Make sure we set the encoding correctly
                        with _pool.getconn() as conn:
                            with conn.cursor() as cursor:
                                cursor.execute("SET client_encoding = 'UTF8';")
                                conn.commit()
                            _pool.putconn(conn)
                        break
                    except Exception as e:
                        logger.warning(
                            f"Failed to connect using DATABASE_URL: {str(e)}. Will try with individual params."
                        )

                # Try with individual params
                _pool = ThreadedConnectionPool(
                    minconn=min_conn,
                    maxconn=max_conn,
                    host=config["host"],
                    port=config["port"],
                    user=config["user"],
                    password=config["password"],
                    database=config["database"],
                    client_encoding="UTF8",  # Explicitly set client encoding
                )
                # Make sure we set the encoding correctly
                with _pool.getconn() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SET client_encoding = 'UTF8';")
                        conn.commit()
                    _pool.putconn(conn)
                logger.info(
                    "Successfully connected to PostgreSQL database with UTF8 encoding"
                )
                break
            except psycopg2.Error as e:
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Failed to connect to database (attempt {attempt + 1}/{max_retries}): {str(e)}"
                    )
                    time.sleep(retry_delay)
                else:
                    logger.error(
                        f"Failed to connect to database after {max_retries} attempts: {str(e)}"
                    )
                    raise

    return _pool


@contextmanager
def get_db_connection() -> Generator:
    """Get a database connection from the pool."""
    pool = get_connection_pool()
    conn = None
    try:
        conn = pool.getconn()
        # Ensure UTF-8 encoding for this connection
        with conn.cursor() as cursor:
            cursor.execute("SET client_encoding = 'UTF8';")
            conn.commit()
        yield conn
    finally:
        if conn:
            pool.putconn(conn)


@contextmanager
def get_db_cursor(commit: bool = False) -> Generator:
    """Get a database cursor with automatic commit/rollback."""
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            cursor.close()


def execute_query(query: str, params: tuple = None, fetch: bool = True, commit: bool = True) -> List[Dict[str, Any]]:
    """Execute a database query and return the results.
    
    Args:
        query: SQL query to execute
        params: Query parameters
        fetch: Whether to fetch and return results
        commit: Whether to commit the transaction
        
    Returns:
        List of records as dictionaries if fetch=True, otherwise empty list
    """
    with get_db_cursor(commit=commit) as cursor:
        cursor.execute(query, params)
        
        if fetch and cursor.description:
            return [dict(record) for record in cursor.fetchall()]
        return []


def execute_batch(query: str, params_list: List[Tuple], commit: bool = True) -> None:
    """Execute a batch query with multiple parameter sets.
    
    Args:
        query: SQL query template
        params_list: List of parameter tuples
        commit: Whether to commit the transaction
    """
    with get_db_cursor(commit=commit) as cursor:
        execute_values(cursor, query, params_list)


def close_connection_pool() -> None:
    """Close the database connection pool."""
    global _pool
    if _pool:
        _pool.closeall()
        _pool = None
        logger.info("Closed all database connections") 
```

# src/db/models.py

```py
"""Pydantic models representing database tables."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field, ConfigDict


class BaseDBModel(BaseModel):
    """Base model for all database models."""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        validate_assignment=True,
    )


class User(BaseDBModel):
    """User model corresponding to the users table."""
    id: Optional[int] = Field(None, description="User ID")
    email: Optional[str] = Field(None, description="User email")
    phone_number: Optional[str] = Field(None, description="User phone number")
    user_data: Optional[Dict[str, Any]] = Field(None, description="Additional user data")
    created_at: Optional[datetime] = Field(None, description="Created at timestamp")
    updated_at: Optional[datetime] = Field(None, description="Updated at timestamp")

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "User":
        """Create a User instance from a database row dictionary."""
        if not row:
            return None
        return cls(**row)


class Agent(BaseDBModel):
    """Agent model corresponding to the agents table."""
    id: Optional[int] = Field(None, description="Agent ID")
    name: str = Field(..., description="Agent name")
    type: str = Field(..., description="Agent type")
    model: str = Field(..., description="Model used by the agent")
    description: Optional[str] = Field(None, description="Agent description")
    version: Optional[str] = Field(None, description="Agent version")
    config: Optional[Dict[str, Any]] = Field(None, description="Agent configuration")
    active: bool = Field(True, description="Whether the agent is active")
    run_id: int = Field(0, description="Current run ID")
    system_prompt: Optional[str] = Field(None, description="System prompt for the agent")
    created_at: Optional[datetime] = Field(None, description="Created at timestamp")
    updated_at: Optional[datetime] = Field(None, description="Updated at timestamp")

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "Agent":
        """Create an Agent instance from a database row dictionary."""
        if not row:
            return None
        return cls(**row)


class Session(BaseDBModel):
    """Session model corresponding to the sessions table."""
    id: Optional[uuid.UUID] = Field(None, description="Session ID")
    user_id: Optional[int] = Field(None, description="User ID")
    agent_id: Optional[int] = Field(None, description="Agent ID")
    name: Optional[str] = Field(None, description="Session name")
    platform: Optional[str] = Field(None, description="Platform")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    created_at: Optional[datetime] = Field(None, description="Created at timestamp")
    updated_at: Optional[datetime] = Field(None, description="Updated at timestamp")
    run_finished_at: Optional[datetime] = Field(None, description="Run finished at timestamp")

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "Session":
        """Create a Session instance from a database row dictionary."""
        if not row:
            return None
        return cls(**row)


class Message(BaseDBModel):
    """Message model corresponding to the messages table."""
    id: Optional[uuid.UUID] = Field(None, description="Message ID")
    session_id: Optional[uuid.UUID] = Field(None, description="Session ID")
    user_id: Optional[int] = Field(None, description="User ID")
    agent_id: Optional[int] = Field(None, description="Agent ID")
    role: str = Field(..., description="Message role (user, assistant, system)")
    text_content: Optional[str] = Field(None, description="Message text content")
    media_url: Optional[str] = Field(None, description="Media URL")
    mime_type: Optional[str] = Field(None, description="MIME type")
    message_type: Optional[str] = Field(None, description="Message type")
    raw_payload: Optional[Dict[str, Any]] = Field(None, description="Raw message payload")
    tool_calls: Optional[Dict[str, Any]] = Field(None, description="Tool calls")
    tool_outputs: Optional[Dict[str, Any]] = Field(None, description="Tool outputs")
    system_prompt: Optional[str] = Field(None, description="System prompt")
    user_feedback: Optional[str] = Field(None, description="User feedback")
    flagged: Optional[str] = Field(None, description="Flagged status")
    context: Optional[Dict[str, Any]] = Field(None, description="Message context")
    created_at: Optional[datetime] = Field(None, description="Created at timestamp")
    updated_at: Optional[datetime] = Field(None, description="Updated at timestamp")

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "Message":
        """Create a Message instance from a database row dictionary."""
        if not row:
            return None
        return cls(**row)


class Memory(BaseDBModel):
    """Memory model corresponding to the memories table."""
    id: Optional[uuid.UUID] = Field(None, description="Memory ID")
    name: str = Field(..., description="Memory name")
    description: Optional[str] = Field(None, description="Memory description")
    content: Optional[str] = Field(None, description="Memory content")
    session_id: Optional[uuid.UUID] = Field(None, description="Session ID")
    user_id: Optional[int] = Field(None, description="User ID")
    agent_id: Optional[int] = Field(None, description="Agent ID")
    read_mode: Optional[str] = Field(None, description="Read mode")
    access: Optional[str] = Field(None, description="Access permissions")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    created_at: Optional[datetime] = Field(None, description="Created at timestamp")
    updated_at: Optional[datetime] = Field(None, description="Updated at timestamp")

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> "Memory":
        """Create a Memory instance from a database row dictionary."""
        if not row:
            return None
        return cls(**row)
```

# src/db/repository.py

```py
"""Repository functions for database operations."""

import uuid
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Union, Tuple

from src.db.connection import execute_query, execute_batch
from src.db.models import Agent, User, Session, Message, Memory
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


def get_user_by_identifier(identifier: str) -> Optional[User]:
    """Get a user by ID, email, or phone number.
    
    Args:
        identifier: The user ID, email, or phone number
        
    Returns:
        User object if found, None otherwise
    """
    try:
        # First check if it's an ID
        if identifier.isdigit():
            return get_user(int(identifier))
        
        # Try email
        user = get_user_by_email(identifier)
        if user:
            return user
        
        # Try phone number
        result = execute_query(
            "SELECT * FROM users WHERE phone_number = %s",
            (identifier,)
        )
        return User.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting user by identifier {identifier}: {str(e)}")
        return None


def list_users(page: int = 1, page_size: int = 100) -> Tuple[List[User], int]:
    """List users with pagination.
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        Tuple of (list of User objects, total count)
    """
    try:
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Get total count
        count_result = execute_query("SELECT COUNT(*) as count FROM users")
        total_count = count_result[0]["count"]
        
        # Get paginated results
        result = execute_query(
            "SELECT * FROM users ORDER BY id LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        
        users = [User.from_db_row(row) for row in result]
        return users, total_count
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        return [], 0


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


def list_sessions(
    user_id: Optional[int] = None, 
    agent_id: Optional[int] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    sort_desc: bool = True
) -> Union[List[Session], Tuple[List[Session], int]]:
    """List sessions with optional filtering and pagination.
    
    Args:
        user_id: Filter by user ID
        agent_id: Filter by agent ID
        page: Page number (1-based, optional)
        page_size: Number of items per page (optional)
        sort_desc: Sort by most recent first if True
        
    Returns:
        If pagination is requested (page and page_size provided):
            Tuple of (list of Session objects, total count)
        Otherwise:
            List of Session objects
    """
    try:
        count_query = "SELECT COUNT(*) as count FROM sessions"
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
            count_query += " WHERE " + " AND ".join(conditions)
        
        # Add sorting
        sort_direction = "DESC" if sort_desc else "ASC"
        query += f" ORDER BY updated_at {sort_direction}, created_at {sort_direction}"
        
        # Get total count for pagination
        count_result = execute_query(count_query, tuple(params) if params else None)
        total_count = count_result[0]['count'] if count_result else 0
        
        # Add pagination if requested
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            query += f" LIMIT %s OFFSET %s"
            params.append(page_size)
            params.append(offset)
        
        result = execute_query(query, tuple(params) if params else None)
        sessions = [Session.from_db_row(row) for row in result]
        
        # Return with count for pagination or just the list
        if page is not None and page_size is not None:
            return sessions, total_count
        return sessions
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        if page is not None and page_size is not None:
            return [], 0
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
        
        # Ensure session has an ID
        if session.id is None:
            session.id = uuid.uuid4()
            logger.info(f"Generated new UUID for session: {session.id}")
        
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


#
# Message Repository Functions
#

def create_message(message: Message) -> Optional[uuid.UUID]:
    """Create a new message.
    
    Args:
        message: The message to create
        
    Returns:
        The created message ID if successful, None otherwise
    """
    try:
        # Generate ID if not provided
        if not message.id:
            message.id = uuid.uuid4()
            
        # Handle JSON fields
        raw_payload_json = json.dumps(message.raw_payload) if message.raw_payload else None
        tool_calls_json = json.dumps(message.tool_calls) if message.tool_calls else None
        tool_outputs_json = json.dumps(message.tool_outputs) if message.tool_outputs else None
        context_json = json.dumps(message.context) if message.context else None
        
        execute_query(
            """
            INSERT INTO messages (
                id, session_id, user_id, agent_id, role, 
                text_content, media_url, mime_type, message_type,
                raw_payload, tool_calls, tool_outputs, 
                system_prompt, user_feedback, flagged, context,
                created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s,
                %s, %s, %s, 
                %s, %s, %s, %s,
                NOW(), NOW()
            )
            """,
            (
                str(message.id), 
                str(message.session_id) if message.session_id else None,
                message.user_id,
                message.agent_id,
                message.role,
                message.text_content,
                message.media_url,
                message.mime_type,
                message.message_type,
                raw_payload_json,
                tool_calls_json,
                tool_outputs_json,
                message.system_prompt,
                message.user_feedback,
                message.flagged,
                context_json,
            ),
            fetch=False
        )
        
        logger.info(f"Created message with ID {message.id}")
        return message.id
    except Exception as e:
        logger.error(f"Error creating message: {str(e)}")
        return None


def get_message(message_id: uuid.UUID) -> Optional[Message]:
    """Get a message by ID.
    
    Args:
        message_id: The message ID
        
    Returns:
        Message object if found, None otherwise
    """
    try:
        result = execute_query(
            "SELECT * FROM messages WHERE id = %s",
            (str(message_id),)
        )
        return Message.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting message {message_id}: {str(e)}")
        return None


def list_messages(session_id: uuid.UUID, limit: int = 100, offset: int = 0) -> List[Message]:
    """List messages for a session with pagination.
    
    Args:
        session_id: The session ID
        limit: Maximum number of messages to retrieve (default: 100)
        offset: Number of messages to skip (default: 0)
        
    Returns:
        List of Message objects
    """
    try:
        result = execute_query(
            """
            SELECT * FROM messages 
            WHERE session_id = %s
            ORDER BY created_at ASC, updated_at ASC
            LIMIT %s OFFSET %s
            """,
            (str(session_id), limit, offset)
        )
        
        messages = []
        for row in result:
            message = Message.from_db_row(row)
            if message:
                messages.append(message)
                
        return messages
    except Exception as e:
        logger.error(f"Error listing messages for session {session_id}: {str(e)}")
        return []


def update_message(message: Message) -> Optional[uuid.UUID]:
    """Update a message.
    
    Args:
        message: The message to update
        
    Returns:
        The updated message ID if successful, None otherwise
    """
    try:
        if not message.id:
            return create_message(message)
            
        # Handle JSON fields
        raw_payload_json = json.dumps(message.raw_payload) if message.raw_payload else None
        tool_calls_json = json.dumps(message.tool_calls) if message.tool_calls else None
        tool_outputs_json = json.dumps(message.tool_outputs) if message.tool_outputs else None
        context_json = json.dumps(message.context) if message.context else None
        
        execute_query(
            """
            UPDATE messages SET 
                session_id = %s,
                user_id = %s,
                agent_id = %s,
                role = %s,
                text_content = %s,
                media_url = %s,
                mime_type = %s,
                message_type = %s,
                raw_payload = %s,
                tool_calls = %s,
                tool_outputs = %s,
                system_prompt = %s,
                user_feedback = %s,
                flagged = %s,
                context = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (
                str(message.session_id) if message.session_id else None,
                message.user_id,
                message.agent_id,
                message.role,
                message.text_content,
                message.media_url,
                message.mime_type,
                message.message_type,
                raw_payload_json,
                tool_calls_json,
                tool_outputs_json,
                message.system_prompt,
                message.user_feedback,
                message.flagged,
                context_json,
                str(message.id)
            ),
            fetch=False
        )
        
        logger.info(f"Updated message with ID {message.id}")
        return message.id
    except Exception as e:
        logger.error(f"Error updating message {message.id}: {str(e)}")
        return None


def delete_message(message_id: uuid.UUID) -> bool:
    """Delete a message.
    
    Args:
        message_id: The message ID to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        execute_query(
            "DELETE FROM messages WHERE id = %s",
            (str(message_id),),
            fetch=False
        )
        logger.info(f"Deleted message with ID {message_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting message {message_id}: {str(e)}")
        return False


def get_system_prompt(session_id: uuid.UUID) -> Optional[str]:
    """Get the system prompt for a session.
    
    Args:
        session_id: The session ID
        
    Returns:
        The system prompt if found, None otherwise
    """
    try:
        # First check if system prompt is stored in session metadata
        session_result = execute_query(
            """
            SELECT metadata FROM sessions 
            WHERE id = %s
            """,
            (str(session_id),)
        )
        
        if session_result and session_result[0]["metadata"]:
            metadata = session_result[0]["metadata"]
            
            # Log metadata format for debugging
            logger.debug(f"Session metadata type: {type(metadata)}")
            
            if isinstance(metadata, dict) and "system_prompt" in metadata:
                system_prompt = metadata["system_prompt"]
                logger.debug(f"Found system prompt in session metadata (dict): {system_prompt[:50]}...")
                return system_prompt
            elif isinstance(metadata, str):
                try:
                    metadata_dict = json.loads(metadata)
                    if "system_prompt" in metadata_dict:
                        system_prompt = metadata_dict["system_prompt"]
                        logger.debug(f"Found system prompt in session metadata (string->dict): {system_prompt[:50]}...")
                        return system_prompt
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse session metadata as JSON: {metadata[:100]}...")
                    # Continue to fallback
            
            # If we got here but couldn't find a system prompt, log the metadata for debugging
            logger.debug(f"No system_prompt found in metadata: {str(metadata)[:100]}...")
        
        # Fallback: look for a system role message
        logger.debug("Falling back to system role message search")
        result = execute_query(
            """
            SELECT text_content FROM messages 
            WHERE session_id = %s AND role = 'system'
            ORDER BY created_at DESC, updated_at DESC
            LIMIT 1
            """,
            (str(session_id),)
        )
        
        if result and result[0]["text_content"]:
            system_prompt = result[0]["text_content"]
            logger.debug(f"Found system prompt in system role message: {system_prompt[:50]}...")
            return system_prompt
        
        logger.warning(f"No system prompt found for session {session_id}")
        return None
    except Exception as e:
        logger.error(f"Error getting system prompt for session {session_id}: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None
```

# src/db/repository/__init__.py

```py
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
    link_session_to_agent
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

```

# src/db/repository/agent.py

```py
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

```

# src/db/repository/memory.py

```py
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

```

# src/db/repository/message.py

```py
"""Message repository functions for database operations."""

import uuid
import json
import logging
from typing import List, Optional, Dict, Any, Tuple, Union
from datetime import datetime

from src.db.connection import execute_query
from src.db.models import Message

# Configure logger
logger = logging.getLogger(__name__)


def get_message(message_id: Union[uuid.UUID, str]) -> Optional[Message]:
    """Get a message by ID.
    
    Args:
        message_id: The UUID of the message to retrieve
        
    Returns:
        Message object if found, None otherwise
    """
    try:
        # Convert string UUID to UUID object if needed
        if isinstance(message_id, str):
            message_id = uuid.UUID(message_id)
            
        query = """
            SELECT * FROM messages WHERE id = %s
        """
        result = execute_query(query, [message_id])
        
        if isinstance(result, list) and len(result) > 0:
            # Convert result dictionary to Message model
            return Message(**result[0])
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            return Message(**result['rows'][0])
            
        return None
    except Exception as e:
        logger.error(f"Error retrieving message {message_id}: {str(e)}")
        return None


def list_messages(session_id: uuid.UUID, page: int = 1, page_size: int = 100, 
                 sort_desc: bool = True) -> List[Message]:
    """List messages for a session with pagination.
    
    Args:
        session_id: The UUID of the session to get messages for
        page: The page number to return (1-indexed)
        page_size: The number of messages per page
        sort_desc: Whether to sort by created_at in descending order (newest first)
        
    Returns:
        List of Message objects
    """
    try:
        order_dir = "DESC" if sort_desc else "ASC"
        offset = (page - 1) * page_size
        
        query = f"""
            SELECT * FROM messages 
            WHERE session_id = %s
            ORDER BY created_at {order_dir}
            LIMIT %s OFFSET %s
        """
        
        result = execute_query(query, [session_id, page_size, offset])
        
        messages = []
        if isinstance(result, list):
            for row in result:
                messages.append(Message(**row))
        elif isinstance(result, dict) and 'rows' in result:
            for row in result['rows']:
                messages.append(Message(**row))
                
        return messages
    except Exception as e:
        logger.error(f"Error listing messages for session {session_id}: {str(e)}")
        return []


def count_messages(session_id: uuid.UUID) -> int:
    """Count the total number of messages in a session.
    
    Args:
        session_id: The UUID of the session
        
    Returns:
        Total message count
    """
    try:
        query = "SELECT COUNT(*) as count FROM messages WHERE session_id = %s"
        result = execute_query(query, [session_id])
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('count', 0)
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            return result['rows'][0].get('count', 0)
            
        return 0
    except Exception as e:
        logger.error(f"Error counting messages for session {session_id}: {str(e)}")
        return 0


def create_message(message: Message) -> Optional[uuid.UUID]:
    """Create a new message in the database.
    
    Args:
        message: The Message object to create
        
    Returns:
        UUID of the created message if successful, None otherwise
    """
    try:
        # Log message parameters for debugging
        logger.debug(f"Creating message with parameters: session_id={message.session_id}, role={message.role}, "
                    f"user_id={message.user_id}, agent_id={message.agent_id}, "
                    f"message_type={message.message_type}, text_length={len(message.text_content or '') if message.text_content else 0}")
        
        # Prepare raw_payload, tool_calls, and tool_outputs for storage
        raw_payload = message.raw_payload
        if raw_payload is not None and not isinstance(raw_payload, str):
            raw_payload = json.dumps(raw_payload)
            
        tool_calls = message.tool_calls
        if tool_calls is not None and not isinstance(tool_calls, str):
            tool_calls = json.dumps(tool_calls)
            
        tool_outputs = message.tool_outputs
        if tool_outputs is not None and not isinstance(tool_outputs, str):
            tool_outputs = json.dumps(tool_outputs)
            
        # Handle context and system_prompt
        context = message.context
        if context is not None and not isinstance(context, str):
            context = json.dumps(context)
            
        system_prompt = message.system_prompt
        
        # Use current time if not provided
        created_at = message.created_at or datetime.utcnow()
        updated_at = message.updated_at or datetime.utcnow()
        
        query = """
            INSERT INTO messages (
                id, session_id, user_id, agent_id, role, text_content, 
                message_type, raw_payload, tool_calls, tool_outputs,
                context, system_prompt, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING id
        """
        
        params = [
            message.id, message.session_id, message.user_id, message.agent_id,
            message.role, message.text_content, message.message_type,
            raw_payload, tool_calls, tool_outputs,
            context, system_prompt, created_at, updated_at
        ]
        
        # Log the SQL query and parameters for debugging
        logger.debug(f"Executing message creation query: {query}")
        logger.debug(f"Query parameters: id={message.id}, session_id={message.session_id}, "
                    f"user_id={message.user_id}, agent_id={message.agent_id}")
        
        result = execute_query(query, params)
        
        if isinstance(result, list) and len(result) > 0:
            message_id = result[0].get('id')
            logger.info(f"Successfully created message {message_id} for session {message.session_id}")
            return message_id
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            message_id = result['rows'][0].get('id')
            logger.info(f"Successfully created message {message_id} for session {message.session_id}")
            return message_id
            
        logger.error(f"Error creating message: Unexpected result format: {result}")
        return None
    except Exception as e:
        logger.error(f"Error creating message: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        logger.error(f"Message details: session_id={message.session_id}, role={message.role}, "
                     f"id={message.id}, text_length={len(message.text_content or '') if message.text_content else 0}")
        return None


def update_message(message: Message) -> Optional[uuid.UUID]:
    """Update an existing message in the database.
    
    Args:
        message: The Message object to update
        
    Returns:
        UUID of the updated message if successful, None otherwise
    """
    try:
        # Prepare raw_payload, tool_calls, and tool_outputs for storage
        raw_payload = message.raw_payload
        if raw_payload is not None and not isinstance(raw_payload, str):
            raw_payload = json.dumps(raw_payload)
            
        tool_calls = message.tool_calls
        if tool_calls is not None and not isinstance(tool_calls, str):
            tool_calls = json.dumps(tool_calls)
            
        tool_outputs = message.tool_outputs
        if tool_outputs is not None and not isinstance(tool_outputs, str):
            tool_outputs = json.dumps(tool_outputs)
            
        # Handle context and system_prompt
        context = message.context
        if context is not None and not isinstance(context, str):
            context = json.dumps(context)
            
        system_prompt = message.system_prompt
        
        # Use current time for updated_at
        updated_at = datetime.utcnow()
        
        query = """
            UPDATE messages
            SET session_id = %s,
                user_id = %s,
                agent_id = %s,
                role = %s,
                text_content = %s,
                message_type = %s,
                raw_payload = %s,
                tool_calls = %s,
                tool_outputs = %s,
                context = %s,
                system_prompt = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING id
        """
        
        params = [
            message.session_id, message.user_id, message.agent_id,
            message.role, message.text_content, message.message_type,
            raw_payload, tool_calls, tool_outputs,
            context, system_prompt, updated_at, message.id
        ]
        
        result = execute_query(query, params)
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('id')
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            return result['rows'][0].get('id')
            
        return None
    except Exception as e:
        logger.error(f"Error updating message {message.id}: {str(e)}")
        return None


def delete_message(message_id: Union[uuid.UUID, str]) -> bool:
    """Delete a message from the database.
    
    Args:
        message_id: The UUID of the message to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert string UUID to UUID object if needed
        if isinstance(message_id, str):
            message_id = uuid.UUID(message_id)
            
        query = "DELETE FROM messages WHERE id = %s RETURNING id"
        result = execute_query(query, [message_id])
        
        # If we got a result, the delete was successful
        return (isinstance(result, list) and len(result) > 0) or \
               (isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0)
    except Exception as e:
        logger.error(f"Error deleting message {message_id}: {str(e)}")
        return False


def delete_session_messages(session_id: Union[uuid.UUID, str]) -> bool:
    """Delete all messages for a session.
    
    Args:
        session_id: The UUID of the session
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert string UUID to UUID object if needed
        if isinstance(session_id, str):
            session_id = uuid.UUID(session_id)
            
        query = "DELETE FROM messages WHERE session_id = %s"
        execute_query(query, [session_id])
        
        # We don't return any rows, so just return True
        return True
    except Exception as e:
        logger.error(f"Error deleting messages for session {session_id}: {str(e)}")
        return False


def get_system_prompt(session_id: Union[uuid.UUID, str]) -> Optional[str]:
    """Get the system prompt for a session from metadata or messages.
    
    Args:
        session_id: The UUID of the session
        
    Returns:
        System prompt string if found, None otherwise
    """
    try:
        # Convert string UUID to UUID object if needed
        if isinstance(session_id, str):
            session_id = uuid.UUID(session_id)
            
        # First try to get system prompt from session metadata
        query = "SELECT metadata FROM sessions WHERE id = %s"
        result = execute_query(query, [session_id])
        
        metadata = None
        if isinstance(result, list) and len(result) > 0 and result[0].get('metadata'):
            metadata = result[0].get('metadata')
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0 and result['rows'][0].get('metadata'):
            metadata = result['rows'][0].get('metadata')
        
        if metadata:
            # Parse metadata if it's a string
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except json.JSONDecodeError:
                    pass
                
            # Check if metadata is a dict with system_prompt
            if isinstance(metadata, dict) and 'system_prompt' in metadata:
                return metadata['system_prompt']
        
        # If no system prompt in metadata, look for system messages
        query = """
            SELECT text_content FROM messages 
            WHERE session_id = %s AND role = 'system'
            ORDER BY created_at DESC
            LIMIT 1
        """
        
        result = execute_query(query, [session_id])
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('text_content')
        elif isinstance(result, dict) and 'rows' in result and len(result['rows']) > 0:
            return result['rows'][0].get('text_content')
            
        return None
    except Exception as e:
        logger.error(f"Error retrieving system prompt for session {session_id}: {str(e)}")
        return None

```

# src/db/repository/session.py

```py
"""Session repository functions for database operations."""

import uuid
import json
import logging
from typing import List, Optional, Dict, Any, Union, Tuple

from src.db.connection import execute_query
from src.db.models import Session

# Configure logger
logger = logging.getLogger(__name__)


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


def list_sessions(
    user_id: Optional[int] = None, 
    agent_id: Optional[int] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    sort_desc: bool = True
) -> Union[List[Session], Tuple[List[Session], int]]:
    """List sessions with optional filtering and pagination.
    
    Args:
        user_id: Filter by user ID
        agent_id: Filter by agent ID
        page: Page number (1-based, optional)
        page_size: Number of items per page (optional)
        sort_desc: Sort by most recent first if True
        
    Returns:
        If pagination is requested (page and page_size provided):
            Tuple of (list of Session objects, total count)
        Otherwise:
            List of Session objects
    """
    try:
        count_query = "SELECT COUNT(*) as count FROM sessions"
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
            count_query += " WHERE " + " AND ".join(conditions)
        
        # Add sorting
        sort_direction = "DESC" if sort_desc else "ASC"
        query += f" ORDER BY updated_at {sort_direction}, created_at {sort_direction}"
        
        # Get total count for pagination
        count_result = execute_query(count_query, tuple(params) if params else None)
        total_count = count_result[0]['count'] if count_result else 0
        
        # Add pagination if requested
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            query += f" LIMIT %s OFFSET %s"
            params.append(page_size)
            params.append(offset)
        
        result = execute_query(query, tuple(params) if params else None)
        sessions = [Session.from_db_row(row) for row in result]
        
        # Return with count for pagination or just the list
        if page is not None and page_size is not None:
            return sessions, total_count
        return sessions
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        if page is not None and page_size is not None:
            return [], 0
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
        
        # Ensure session has an ID
        if session.id is None:
            session.id = uuid.uuid4()
            logger.info(f"Generated new UUID for session: {session.id}")
        
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


def get_system_prompt(session_id: uuid.UUID) -> Optional[str]:
    """Get the system prompt for a session.
    
    Args:
        session_id: The session ID
        
    Returns:
        The system prompt if found, None otherwise
    """
    try:
        # First check if system prompt is stored in session metadata
        session_result = execute_query(
            """
            SELECT metadata FROM sessions 
            WHERE id = %s
            """,
            (str(session_id),)
        )
        
        if session_result and session_result[0]["metadata"]:
            metadata = session_result[0]["metadata"]
            
            # Log metadata format for debugging
            logger.debug(f"Session metadata type: {type(metadata)}")
            
            if isinstance(metadata, dict) and "system_prompt" in metadata:
                system_prompt = metadata["system_prompt"]
                logger.debug(f"Found system prompt in session metadata (dict): {system_prompt[:50]}...")
                return system_prompt
            elif isinstance(metadata, str):
                try:
                    metadata_dict = json.loads(metadata)
                    if "system_prompt" in metadata_dict:
                        system_prompt = metadata_dict["system_prompt"]
                        logger.debug(f"Found system prompt in session metadata (string->dict): {system_prompt[:50]}...")
                        return system_prompt
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse session metadata as JSON: {metadata[:100]}...")
                    # Continue to fallback
            
            # If we got here but couldn't find a system prompt, log the metadata for debugging
            logger.debug(f"No system_prompt found in metadata: {str(metadata)[:100]}...")
        
        # Fallback: look for a system role message
        logger.debug("Falling back to system role message search")
        result = execute_query(
            """
            SELECT text_content FROM messages 
            WHERE session_id = %s AND role = 'system'
            ORDER BY created_at DESC, updated_at DESC
            LIMIT 1
            """,
            (str(session_id),)
        )
        
        if result and result[0]["text_content"]:
            system_prompt = result[0]["text_content"]
            logger.debug(f"Found system prompt in system role message: {system_prompt[:50]}...")
            return system_prompt
        
        logger.warning(f"No system prompt found for session {session_id}")
        return None
    except Exception as e:
        logger.error(f"Error getting system prompt for session {session_id}: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None


def update_session_name_if_empty(session_id: uuid.UUID, new_name: str) -> bool:
    """Updates a session's name only if it's currently empty or None.
    
    Args:
        session_id: Session ID
        new_name: New session name to set if current name is empty
        
    Returns:
        True if update was performed, False if not needed or failed
    """
    try:
        # Get current session
        session = get_session(session_id)
        if not session:
            logger.error(f"Session {session_id} not found")
            return False
            
        # Check if name is empty or None
        if not session.name:
            # Update the session name
            session.name = new_name
            updated_id = update_session(session)
            if updated_id:
                logger.info(f"Updated session {session_id} name to '{new_name}'")
                return True
            else:
                logger.error(f"Failed to update session {session_id} name")
                return False
            
        # No update needed
        logger.debug(f"Session {session_id} already has name '{session.name}', no update needed")
        return False
    except Exception as e:
        logger.error(f"Error updating session name: {str(e)}")
        return False

```

# src/db/repository/user.py

```py
"""User repository functions for database operations."""

import json
import logging
from typing import List, Optional, Dict, Any, Tuple

from src.db.connection import execute_query
from src.db.models import User

# Configure logger
logger = logging.getLogger(__name__)


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


def get_user_by_identifier(identifier: str) -> Optional[User]:
    """Get a user by ID, email, or phone number.
    
    Args:
        identifier: The user ID, email, or phone number
        
    Returns:
        User object if found, None otherwise
    """
    try:
        # First check if it's an ID
        if identifier.isdigit():
            return get_user(int(identifier))
        
        # Try email
        user = get_user_by_email(identifier)
        if user:
            return user
        
        # Try phone number
        result = execute_query(
            "SELECT * FROM users WHERE phone_number = %s",
            (identifier,)
        )
        return User.from_db_row(result[0]) if result else None
    except Exception as e:
        logger.error(f"Error getting user by identifier {identifier}: {str(e)}")
        return None


def list_users(page: int = 1, page_size: int = 100) -> Tuple[List[User], int]:
    """List users with pagination.
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        Tuple of (list of User objects, total count)
    """
    try:
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Get total count
        count_result = execute_query("SELECT COUNT(*) as count FROM users")
        total_count = count_result[0]["count"]
        
        # Get paginated results
        result = execute_query(
            "SELECT * FROM users ORDER BY id LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        
        users = [User.from_db_row(row) for row in result]
        return users, total_count
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        return [], 0


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


def ensure_default_user_exists(user_id: int = 1, email: str = "admin@automagik") -> bool:
    """Ensures a default user exists in the database, creating it if necessary.
    
    Args:
        user_id: The default user ID
        email: The default user email
    
    Returns:
        True if user already existed or was created successfully, False otherwise
    """
    try:
        # Check if user exists
        user = get_user(user_id)
        if user:
            logger.debug(f"Default user {user_id} already exists")
            return True
            
        # Create default user
        from datetime import datetime
        user = User(
            id=user_id,
            email=email,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        created_id = create_user(user)
        if created_id:
            logger.info(f"Created default user with ID {user_id} and email {email}")
            return True
        else:
            logger.warning(f"Failed to create default user with ID {user_id}")
            return False
    except Exception as e:
        logger.error(f"Error ensuring default user exists: {str(e)}")
        return False

```

# src/main.py

```py
import logging
from datetime import datetime
import json
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings, Environment
from src.utils.logging import configure_logging
from src.version import SERVICE_INFO
from src.auth import APIKeyMiddleware
from src.api.models import HealthResponse
from src.api.routes import router as api_router
from src.memory.message_history import MessageHistory
from src.agents.models.agent_factory import AgentFactory
from src.db import execute_query, get_connection_pool, ensure_default_user_exists, create_session, Session

# Configure loggingg
configure_logging()

# Get our module's logger
logger = logging.getLogger(__name__)

def initialize_all_agents():
    """Initialize all available agents at startup.
    
    This ensures that agents are created and registered in the database
    before any API requests are made, rather than waiting for the first
    run request.
    """
    try:
        logger.info("🔧 Initializing all available agents...")
        
        # Discover all available agents
        AgentFactory.discover_agents()
        
        # Get the list of available agents
        available_agents = AgentFactory.list_available_agents()
        logger.info(f"Found {len(available_agents)} available agents: {', '.join(available_agents)}")
        
        # Initialize each agent
        for agent_name in available_agents:
            try:
                logger.info(f"Initializing agent: {agent_name}")
                # This will create and register the agent
                AgentFactory.get_agent(agent_name)
                logger.info(f"✅ Agent {agent_name} initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize agent {agent_name}: {str(e)}")
        
        logger.info("✅ All agents initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize agents: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Create FastAPI application
    app = FastAPI(
        title=SERVICE_INFO["name"],
        description=SERVICE_INFO["description"],
        version=SERVICE_INFO["version"],
        docs_url=None,  # Disable default docs url
        redoc_url=None,  # Disable default redoc url
        openapi_url=None,  # Disable default openapi url
        openapi_tags=[
            {
                "name": "System",
                "description": "System endpoints for status and health checking",
                "order": 1,
            },
            {
                "name": "Agents",
                "description": "Endpoints for listing available agents and running agent tasks",
                "order": 2,
            },
            {
                "name": "Sessions",
                "description": "Endpoints to manage and retrieve agent conversation sessions",
                "order": 3,
            },
        ]
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # Add authentication middleware
    app.add_middleware(APIKeyMiddleware)
    
    # Register startup event to initialize agents
    @app.on_event("startup")
    async def startup_event():
        # Initialize all agents at startup
        initialize_all_agents()
    
    # Set up database message store regardless of environment
    try:
        logger.info("🔧 Initializing database connection for message storage")
        
        # First test database connection
        from src.db.connection import get_connection_pool
        pool = get_connection_pool()
        
        # Test the connection with a simple query
        with pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                logger.info(f"✅ Database connection test successful: {version}")
                
                # Check if required tables exist
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sessions')")
                sessions_table_exists = cur.fetchone()[0]
                
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'messages')")
                messages_table_exists = cur.fetchone()[0]
                
                logger.info(f"Database tables check - Sessions: {sessions_table_exists}, Messages: {messages_table_exists}")
                
                if not (sessions_table_exists and messages_table_exists):
                    logger.error("❌ Required database tables are missing - sessions or messages tables not found")
                    raise ValueError("Required database tables not found")
            pool.putconn(conn)
            
        logger.info("✅ Database connection pool initialized successfully")
        
        # Verify database functionality without creating persistent test data
        logger.info("🔍 Performing verification test of message storage without creating persistent sessions...")
        test_user_id = 1  # Use numeric ID instead of string
        
        # First ensure the default user exists using repository function
        ensure_default_user_exists(user_id=test_user_id, email="admin@automagik")
        
        # Verify message store functionality without creating test sessions
        # Use a transaction that we'll roll back to avoid persisting test data
        try:
            logger.info("Testing database message storage functionality with transaction rollback...")
            with pool.getconn() as conn:
                conn.autocommit = False  # Start a transaction
                
                # Generate test UUIDs
                test_session_id = uuid.uuid4()
                test_message_id = uuid.uuid4()
                
                # Test inserting temporary session
                from src.db import create_session, Session, create_message, Message
                
                # Create a test session
                test_session = Session(
                    id=test_session_id,
                    user_id=test_user_id,
                    platform="verification_test",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                # Test inserting a test message
                test_message = Message(
                    id=test_message_id,
                    session_id=test_session_id,
                    role="user",
                    text_content="Test database connection",
                    raw_payload={"content": "Test database connection"},
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                # Create the session and message within the transaction
                with conn.cursor() as cur:
                    # Import safe_uuid to handle UUID objects
                    from src.db.connection import safe_uuid
                    
                    # Insert test session
                    cur.execute(
                        """
                        INSERT INTO sessions (id, user_id, platform, created_at, updated_at) 
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (safe_uuid(test_session_id), test_user_id, "verification_test", datetime.utcnow(), datetime.utcnow())
                    )
                    
                    # Insert test message
                    cur.execute(
                        """
                        INSERT INTO messages (
                            id, session_id, role, text_content, raw_payload, created_at, updated_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            safe_uuid(test_message_id),
                            safe_uuid(test_session_id),
                            "user",
                            "Test database connection",
                            json.dumps({"content": "Test database connection"}),
                            datetime.utcnow(),
                            datetime.utcnow()
                        )
                    )
                    
                    # Verify we can read the data back
                    cur.execute("SELECT COUNT(*) FROM sessions WHERE id = %s", (safe_uuid(test_session_id),))
                    session_count = cur.fetchone()[0]
                    
                    cur.execute("SELECT COUNT(*) FROM messages WHERE id = %s", (safe_uuid(test_message_id),))
                    message_count = cur.fetchone()[0]
                    
                    if session_count > 0 and message_count > 0:
                        logger.info("✅ Database read/write test successful")
                    else:
                        logger.error("❌ Failed to verify database read operations")
                        raise Exception("Database verification failed")
                    
                    # Roll back the transaction to avoid persisting test data
                    conn.rollback()
                    logger.info("✅ Test transaction rolled back - no test data persisted")
                
                # Return connection to pool
                pool.putconn(conn)
                
            logger.info("✅ Database verification completed successfully without creating persistent test data")
        except Exception as test_e:
            logger.error(f"❌ Database verification test failed: {str(test_e)}")
            # Ensure any open transaction is rolled back
            try:
                conn.rollback()
            except:
                pass
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
            raise
        
        # Log success
        logger.info("✅ Database message storage initialized successfully")
        
        # Configure MessageHistory to use database by default
        from src.memory.message_history import MessageHistory
        logger.info("✅ MessageHistory configured to use database storage")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database connection for message storage: {str(e)}")
        logger.error("⚠️ Application will fall back to in-memory message store")
        # Include traceback for debugging
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        
        # Create an in-memory message history as fallback
        # Don't reference the non-existent message_store module
        logger.warning("⚠️ Using in-memory storage as fallback - MESSAGES WILL NOT BE PERSISTED!")
    
    # Remove direct call since we're using the startup event
    # initialize_all_agents()

    # Root and health endpoints (no auth required)
    @app.get("/", tags=["System"], summary="Root Endpoint", description="Returns service information and status")
    async def root():
        return {
            "status": "online",
            **SERVICE_INFO
        }

    @app.get("/health", tags=["System"], summary="Health Check", description="Returns health status of the service")
    async def health_check() -> HealthResponse:
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow(),
            version=SERVICE_INFO["version"],
            environment=settings.AM_ENV
        )

    # Include API router (with versioned prefix)
    app.include_router(api_router, prefix="/api/v1")

    return app

# Create the app instance
app = create_app()

# Include Documentation router after app is created (to avoid circular imports)
from src.api.docs import router as docs_router
app.include_router(docs_router)

if __name__ == "__main__":
    import uvicorn
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description="Run the Sofia application server")
    parser.add_argument(
        "--reload", 
        action="store_true", 
        default=False,
        help="Enable auto-reload for development (default: False)"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default=settings.AM_HOST,
        help=f"Host to bind the server to (default: {settings.AM_HOST})"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(settings.AM_PORT),
        help=f"Port to bind the server to (default: {settings.AM_PORT})"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Log the configuration
    logger.info(f"Starting server with configuration:")
    logger.info(f"├── Host: {args.host}")
    logger.info(f"├── Port: {args.port}")
    logger.info(f"└── Auto-reload: {'Enabled' if args.reload else 'Disabled'}")
    
    # Run the server
    uvicorn.run(
        "src.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

```

# src/memory/__init__.py

```py
"""Memory management module for Sofia."""

```

# src/memory/message_history.py

```py
"""Message history management for PydanticAI compatibility.

This module provides a simplified MessageHistory class that directly uses
the repository pattern for database operations and implements PydanticAI-compatible 
message history methods.
"""

import logging
import uuid
from typing import List, Optional, Dict, Any, Union, Tuple
from datetime import datetime, UTC

# PydanticAI imports
from pydantic_ai.messages import (
    ModelMessage, 
    ModelRequest, 
    ModelResponse,
    SystemPromptPart, 
    UserPromptPart, 
    TextPart,
    ToolCallPart,
    ToolReturnPart
)

# Import repository functions
from src.db.repository.message import (
    create_message,
    get_message,
    list_messages,
    delete_session_messages,
    get_system_prompt
)
from src.db.repository.session import (
    get_session,
    create_session,
    update_session
)
from src.db.models import Message, Session

# Configure logger
logger = logging.getLogger(__name__)

# Helper function for UUID validation
def is_valid_uuid(value: Any) -> bool:
    """Check if a value is a valid UUID or can be converted to one.
    
    Args:
        value: The value to check
        
    Returns:
        True if the value is a valid UUID or can be converted to one
    """
    if value is None:
        return False
    if isinstance(value, uuid.UUID):
        return True
    if not isinstance(value, str):
        return False
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False


class MessageHistory:
    """Maintains a history of messages between the user and the agent.
    
    This class integrates with pydantic-ai's message system to maintain context
    across multiple agent runs. It handles system prompts, user messages, and
    assistant responses in a format compatible with pydantic-ai.
    
    This simplified implementation directly uses the repository pattern
    for database operations without intermediate abstractions.
    """
    
    def __init__(self, session_id: str, system_prompt: Optional[str] = None, user_id: int = 1, no_auto_create: bool = False):
        """Initialize a new message history.
        
        Args:
            session_id: The unique session identifier.
            system_prompt: Optional system prompt to set at initialization.
            user_id: The user identifier to associate with this session (defaults to 1).
            no_auto_create: If True, don't automatically create a session in the database.
        """
        self.session_id = self._ensure_session_id(session_id, user_id, no_auto_create)
        self.user_id = user_id
        
        # Add system prompt if provided
        if system_prompt:
            self.add_system_prompt(system_prompt)
    
    def _ensure_session_id(self, session_id: str, user_id: int, no_auto_create: bool = False) -> str:
        """Ensure the session exists, creating it if necessary.
        
        Args:
            session_id: The session ID (string or UUID)
            user_id: The user ID to associate with the session
            no_auto_create: If True, don't automatically create a session
            
        Returns:
            The validated session ID as a string
        """
        try:
            # Generate new UUID if session_id is None or invalid
            if not session_id or not is_valid_uuid(session_id):
                new_uuid = uuid.uuid4()
                logger.info(f"Creating new session with UUID: {new_uuid}")
                
                if not no_auto_create:
                    # Create a new session
                    session = Session(
                        id=new_uuid,
                        user_id=user_id,
                        name=f"Session-{new_uuid}",
                        platform="automagik"
                    )
                    create_session(session)
                else:
                    logger.info("Auto-creation disabled, not creating session in database")
                
                return str(new_uuid)
            
            # Convert string to UUID
            if isinstance(session_id, str):
                session_uuid = uuid.UUID(session_id)
            else:
                session_uuid = session_id
                
            # Check if session exists
            session = get_session(session_uuid)
            if not session and not no_auto_create:
                # Create new session with this ID
                session = Session(
                    id=session_uuid,
                    user_id=user_id,
                    name=f"Session-{session_uuid}",
                    platform="automagik"
                )
                create_session(session)
                
            return str(session_uuid)
        except Exception as e:
            logger.error(f"Error ensuring session ID: {str(e)}")
            # Create a fallback UUID
            fallback_uuid = uuid.uuid4()
            return str(fallback_uuid)
    
    def add_system_prompt(self, content: str, agent_id: Optional[int] = None) -> ModelMessage:
        """Add or update the system prompt for this conversation.
        
        Args:
            content: The system prompt content.
            agent_id: Optional agent ID associated with the message.
            
        Returns:
            The created system prompt message.
        """
        try:
            # Create a system prompt message
            system_message = ModelRequest(parts=[SystemPromptPart(content=content)])
            
            # Store the system prompt in the session metadata
            session_uuid = uuid.UUID(self.session_id)
            session = get_session(session_uuid)
            
            if session:
                # Get existing metadata or create new dictionary
                metadata = session.metadata or {}
                if isinstance(metadata, str):
                    try:
                        import json
                        metadata = json.loads(metadata)
                    except json.JSONDecodeError:
                        metadata = {}
                
                # Store system prompt in metadata
                metadata["system_prompt"] = content
                session.metadata = metadata
                
                # Update session
                update_session(session)
                logger.debug(f"Stored system prompt in session metadata: {content[:50]}...")
            
            # Also create a system message in the database
            message = Message(
                id=uuid.uuid4(),
                session_id=session_uuid,
                user_id=self.user_id,
                agent_id=agent_id,
                role="system",
                text_content=content,
                message_type="text",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            )
            create_message(message)
            
            return system_message
        except Exception as e:
            logger.error(f"Error adding system prompt: {str(e)}")
            # Return a basic system message as fallback
            return ModelRequest(parts=[SystemPromptPart(content=content)])
    
    def add(self, content: str, agent_id: Optional[int] = None, context: Optional[Dict] = None) -> ModelMessage:
        """Add a user message to the history.
        
        Args:
            content: The message content.
            agent_id: Optional agent ID associated with the message.
            context: Optional context data to include with the message.
            
        Returns:
            The created user message.
        """
        try:
            # Create a user message in the database
            message = Message(
                id=uuid.uuid4(),
                session_id=uuid.UUID(self.session_id),
                user_id=self.user_id,
                agent_id=agent_id,
                role="user",
                text_content=content,
                message_type="text",
                context=context,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            )
            
            # Log before attempting to create message
            logger.info(f"Adding user message to history for session {self.session_id}, user {self.user_id}")
            logger.debug(f"Message details: id={message.id}, session_id={self.session_id}, content_length={len(content) if content else 0}")
            
            # Create the message in the database
            message_id = create_message(message)
            
            if not message_id:
                # If message creation failed, log a more detailed error
                logger.error(f"Failed to create user message in database: message_id={message.id}, session_id={self.session_id}, user_id={self.user_id}")
                # Don't raise exception to maintain backward compatibility, but log the error
            else:
                logger.info(f"Successfully added user message {message_id} to history")
            
            # Create and return a PydanticAI compatible message
            return ModelRequest(parts=[UserPromptPart(content=content)])
        except Exception as e:
            import traceback
            logger.error(f"Exception adding user message: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.error(f"Message details: session_id={self.session_id}, user_id={self.user_id}, content_length={len(content) if content else 0}")
            
            # Return a basic user message as fallback to maintain backwards compatibility
            return ModelRequest(parts=[UserPromptPart(content=content)])
    
    def add_response(
        self, 
        content: str, 
        assistant_name: Optional[str] = None, 
        tool_calls: Optional[List[Dict]] = None, 
        tool_outputs: Optional[List[Dict]] = None,
        agent_id: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> ModelMessage:
        """Add an assistant response message to the history.
        
        Args:
            content: The text content of the assistant's response.
            assistant_name: Optional name of the assistant.
            tool_calls: Optional list of tool calls made during processing.
            tool_outputs: Optional list of outputs from tool calls.
            agent_id: Optional agent ID associated with the message.
            system_prompt: Optional system prompt to store directly with the message.
            
        Returns:
            The created assistant response message.
        """
        try:
            # Prepare tool calls and outputs for storage
            tool_calls_dict = {}
            tool_outputs_dict = {}
            
            if tool_calls:
                for i, tc in enumerate(tool_calls):
                    if isinstance(tc, dict) and "tool_name" in tc:
                        tool_calls_dict[str(i)] = tc
            
            if tool_outputs:
                for i, to in enumerate(tool_outputs):
                    if isinstance(to, dict) and "tool_name" in to:
                        tool_outputs_dict[str(i)] = to
            
            # Prepare raw payload
            raw_payload = {
                "content": content,
                "assistant_name": assistant_name,
                "tool_calls": tool_calls,
                "tool_outputs": tool_outputs,
            }
            
            # If system_prompt isn't directly provided or is None, try to get it from:
            # 1. Session metadata
            # 2. Last system prompt in the message history
            # 3. Agent configuration (through agent_id)
            if not system_prompt:
                try:
                    # Try to get from session metadata first
                    session_system_prompt = get_system_prompt(uuid.UUID(self.session_id))
                    if session_system_prompt:
                        system_prompt = session_system_prompt
                        logger.debug(f"Using system prompt from session metadata")
                    else:
                        # If not found, try other sources
                        if agent_id:
                            # Try to get system prompt from agent configuration
                            from src.db.repository.agent import get_agent
                            agent = get_agent(agent_id)
                            if agent and agent.system_prompt:
                                system_prompt = agent.system_prompt
                                logger.debug(f"Using system prompt from agent configuration")
                except Exception as e:
                    logger.error(f"Error getting system prompt: {str(e)}")
            
            # Log message details - reduced logging
            tool_calls_count = len(tool_calls_dict) if tool_calls_dict else 0
            tool_outputs_count = len(tool_outputs_dict) if tool_outputs_dict else 0
            content_length = len(content) if content else 0
            
            # For INFO level, just log basic info
            logger.info(f"Adding assistant response to MessageHistory in the database")
            logger.info(f"System prompt status: {'Present' if system_prompt else 'Not provided'}")
            
            # For DEBUG level (verbose logging), add more details
            logger.debug(f"Adding assistant response to history for session {self.session_id}, user {self.user_id}")
            logger.debug(f"Assistant response details: tool_calls={tool_calls_count}, tool_outputs={tool_outputs_count}, content_length={content_length}")
            
            # Create message in database
            logger.debug(f"Creating message with parameters: session_id={self.session_id}, role=assistant, user_id={self.user_id}, agent_id={agent_id}, message_type=text, text_length={content_length}")
            
            message = Message(
                id=uuid.uuid4(),
                session_id=uuid.UUID(self.session_id),
                user_id=self.user_id,
                agent_id=agent_id,
                role="assistant",
                text_content=content,
                message_type="text",
                raw_payload=raw_payload,
                tool_calls=tool_calls_dict,
                tool_outputs=tool_outputs_dict,
                system_prompt=system_prompt,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            )
            
            # Log query only in debug mode
            logger.debug("Executing message creation query: \n            INSERT INTO messages (\n                id, session_id, user_id, agent_id, role, text_content, \n                message_type, raw_payload, tool_calls, tool_outputs, \n                context, system_prompt, created_at, updated_at\n            ) VALUES (\n                %s, %s, %s, %s, %s, %s, \n                %s, %s, %s, %s, \n                %s, %s, %s, %s\n            )\n            RETURNING id\n         ")
            logger.debug(f"Query parameters: id={message.id}, session_id={self.session_id}, user_id={self.user_id}, agent_id={agent_id}")
            
            # Create the message in the database
            message_id = create_message(message)
            
            if not message_id:
                # If message creation failed, log a more detailed error
                logger.error(f"Failed to create assistant message in database: message_id={message.id}, session_id={self.session_id}, user_id={self.user_id}")
                # Don't raise exception to maintain backward compatibility, but log the error
            else:
                logger.info(f"Successfully created message {message_id} for session {self.session_id}")
                logger.debug(f"Successfully added assistant message {message_id} to history for session {self.session_id}")
            
            # Create parts for PydanticAI message
            parts = [TextPart(content=content)]
            
            # Add tool call parts
            if tool_calls:
                for tc in tool_calls:
                    if isinstance(tc, dict) and "tool_name" in tc and "args" in tc:
                        parts.append(
                            ToolCallPart(
                                tool_name=tc["tool_name"],
                                args=tc["args"],
                                tool_call_id=tc.get("tool_call_id", "")
                            )
                        )
            
            # Add tool output parts
            if tool_outputs:
                for to in tool_outputs:
                    if isinstance(to, dict) and "tool_name" in to and "content" in to:
                        parts.append(
                            ToolReturnPart(
                                tool_name=to["tool_name"],
                                content=to["content"],
                                tool_call_id=to.get("tool_call_id", "")
                            )
                        )
            
            # Create and return PydanticAI message
            return ModelResponse(parts=parts)
        except Exception as e:
            import traceback
            logger.error(f"Exception adding assistant message: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.error(f"Message details: session_id={self.session_id}, user_id={self.user_id}, content_length={len(content) if content else 0}, tool_calls={len(tool_calls) if tool_calls else 0}")
            
            # Return a basic assistant message as fallback to maintain backward compatibility
            return ModelResponse(parts=[TextPart(content=content)])
    
    def clear(self) -> None:
        """Clear all messages in the current session."""
        try:
            delete_session_messages(uuid.UUID(self.session_id))
        except Exception as e:
            logger.error(f"Error clearing session messages: {str(e)}")
    
    # PydanticAI compatible methods
    
    def all_messages(self) -> List[ModelMessage]:
        """Return all messages in the history, including those from prior runs.
        
        This method is required for PydanticAI compatibility.
        
        Returns:
            List of all messages in the history
        """
        try:
            # Get all messages from the database
            logger.debug(f"Retrieving all messages for session {self.session_id}")
            db_messages = list_messages(uuid.UUID(self.session_id))
            
            # Convert to PydanticAI format - only log detailed info in debug mode
            messages = self._convert_db_messages_to_model_messages(db_messages)
            logger.debug(f"Retrieved and converted {len(messages)} messages for session {self.session_id}")
            return messages
        except Exception as e:
            import traceback
            logger.error(f"Error retrieving messages: {str(e)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return []
    
    def new_messages(self) -> List[ModelMessage]:
        """Return only the messages from the current run.
        
        This method is required for PydanticAI compatibility.
        Since we don't track runs explicitly, this returns all messages.
        
        Returns:
            List of messages from the current run
        """
        # For now, identical to all_messages since we don't track runs
        return self.all_messages()
    
    def all_messages_json(self) -> bytes:
        """Return all messages as JSON.
        
        This method is required for PydanticAI compatibility.
        
        Returns:
            JSON bytes representation of all messages
        """
        try:
            from pydantic_core import to_json
            return to_json(self.all_messages())
        except Exception as e:
            logger.error(f"Error serializing messages to JSON: {str(e)}")
            return b"[]"
    
    def new_messages_json(self) -> bytes:
        """Return only the messages from the current run as JSON.
        
        This method is required for PydanticAI compatibility.
        
        Returns:
            JSON bytes representation of messages from the current run
        """
        # For now, identical to all_messages_json since we don't track runs
        return self.all_messages_json()
    
    @classmethod
    def from_model_messages(cls, messages: List[ModelMessage], session_id: Optional[str] = None) -> 'MessageHistory':
        """Create a new MessageHistory from a list of model messages.
        
        Args:
            messages: List of ModelMessage objects to populate the history with
            session_id: Optional session ID to use, otherwise generates a new one
            
        Returns:
            A new MessageHistory instance with the provided messages
        """
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
            
        # Create a new MessageHistory instance
        history = cls(session_id=session_id)
        
        # Add system prompt message if present
        system_prompt = None
        for msg in messages:
            if hasattr(msg, "parts"):
                for part in msg.parts:
                    if isinstance(part, SystemPromptPart):
                        system_prompt = part.content
                        break
                if system_prompt:
                    history.add_system_prompt(system_prompt)
                    break
        
        # Add all user messages
        for msg in messages:
            if hasattr(msg, "parts"):
                # Skip system messages as we've already handled them
                if any(isinstance(part, SystemPromptPart) for part in msg.parts):
                    continue
                    
                # Handle user messages
                for part in msg.parts:
                    if isinstance(part, UserPromptPart):
                        history.add(part.content)
                        break
                        
                # Handle assistant messages with potential tool calls
                if any(isinstance(part, TextPart) and not isinstance(part, UserPromptPart) for part in msg.parts):
                    content = ""
                    tool_calls = []
                    tool_outputs = []
                    
                    # Extract content
                    for part in msg.parts:
                        if isinstance(part, TextPart) and not isinstance(part, UserPromptPart):
                            content = part.content
                            break
                    
                    # Extract tool calls
                    for part in msg.parts:
                        if isinstance(part, ToolCallPart):
                            tool_calls.append({
                                "tool_name": part.tool_name,
                                "args": part.args,
                                "tool_call_id": part.tool_call_id
                            })
                    
                    # Extract tool outputs
                    for part in msg.parts:
                        if isinstance(part, ToolReturnPart):
                            tool_outputs.append({
                                "tool_name": part.tool_name,
                                "content": part.content,
                                "tool_call_id": part.tool_call_id
                            })
                    
                    # Add response if we have content
                    if content:
                        history.add_response(
                            content=content,
                            tool_calls=tool_calls if tool_calls else None,
                            tool_outputs=tool_outputs if tool_outputs else None
                        )
        
        return history
    
    @classmethod
    def from_json(cls, json_data: Union[str, bytes], session_id: Optional[str] = None) -> 'MessageHistory':
        """Create a MessageHistory from JSON data.
        
        Args:
            json_data: JSON string or bytes containing serialized messages
            session_id: Optional session ID to use, otherwise generates a new one
            
        Returns:
            New MessageHistory instance with the deserialized messages
        """
        try:
            from pydantic_ai.messages import ModelMessagesTypeAdapter
            messages = ModelMessagesTypeAdapter.validate_json(json_data)
            return cls.from_model_messages(messages, session_id)
        except Exception as e:
            logger.error(f"Error deserializing messages from JSON: {str(e)}")
            # Return an empty history with a new session
            return cls(session_id=session_id or str(uuid.uuid4()))
    
    def to_json(self) -> bytes:
        """Serialize all messages to JSON.
        
        Returns:
            JSON bytes representation of all messages
        """
        return self.all_messages_json()
    
    # Helper methods for converting between database and PydanticAI models
    
    def _convert_db_messages_to_model_messages(self, db_messages: List[Message]) -> List[ModelMessage]:
        """Convert database messages to PydanticAI ModelMessage objects.
        
        Args:
            db_messages: List of database Message objects
            
        Returns:
            List of PydanticAI ModelMessage objects
        """
        model_messages = []
        
        for db_message in db_messages:
            # Convert database message to ModelMessage
            if db_message.role == "system":
                # Create system message
                model_messages.append(
                    ModelRequest(parts=[SystemPromptPart(content=db_message.text_content or "")])
                )
            elif db_message.role == "user":
                # Create user message
                model_messages.append(
                    ModelRequest(parts=[UserPromptPart(content=db_message.text_content or "")])
                )
            elif db_message.role == "assistant":
                # Create assistant message with potential tool calls and outputs
                parts = [TextPart(content=db_message.text_content or "")]
                
                # Add tool calls if present
                if db_message.tool_calls:
                    tool_calls = db_message.tool_calls
                    if isinstance(tool_calls, dict):
                        for tc in tool_calls.values():
                            if isinstance(tc, dict) and "tool_name" in tc and "args" in tc:
                                parts.append(
                                    ToolCallPart(
                                        tool_name=tc["tool_name"],
                                        args=tc["args"],
                                        tool_call_id=tc.get("tool_call_id", "")
                                    )
                                )
                
                # Add tool outputs if present
                if db_message.tool_outputs:
                    tool_outputs = db_message.tool_outputs
                    if isinstance(tool_outputs, dict):
                        for to in tool_outputs.values():
                            if isinstance(to, dict) and "tool_name" in to and "content" in to:
                                parts.append(
                                    ToolReturnPart(
                                        tool_name=to["tool_name"],
                                        content=to["content"],
                                        tool_call_id=to.get("tool_call_id", "")
                                    )
                                )
                
                # Create and add assistant message
                model_messages.append(ModelResponse(parts=parts))
        
        return model_messages

```

# src/tools/__init__.py

```py
"""Tools package.

This package includes various tools used by Sofia.
"""

from .datetime import datetime_tools
from .discord import discord_tools
from .evolution import evolution_tools
from .google_drive import google_drive_tools
from .memory.tool import (
    read_memory,
    create_memory,
    update_memory,
    get_memory_tool,
    store_memory_tool,
    list_memories_tool
)
from .notion import notion_tools

# Export individual tools and groups
__all__ = [
    # DateTime tools
    "datetime_tools",
    
    # Discord tools
    "discord_tools",
    
    # Evolution tools
    "evolution_tools",
    
    # Google Drive tools
    "google_drive_tools",
    
    # Memory tools
    "read_memory",
    "create_memory",
    "update_memory",
    "get_memory_tool",
    "store_memory_tool",
    "list_memories_tool",
    
    # Notion tools
    "notion_tools",
] 
```

# src/tools/datetime/__init__.py

```py
"""Datetime tools for Automagik Agents.

Provides tools for retrieving date and time information.
"""

# Import from tool module
from src.tools.datetime.tool import (
    get_current_date,
    get_current_time,
    get_current_date_description,
    get_current_time_description,
    format_date,
    format_date_description
)

# Import schema models
from src.tools.datetime.schema import DatetimeInput, DatetimeOutput

# Create a collection of all datetime tools for easy import
from pydantic_ai import Tool

# Create Tool instances
get_current_date_tool = Tool(
    name="get_current_date",
    description=get_current_date_description(),
    function=get_current_date
)

get_current_time_tool = Tool(
    name="get_current_time",
    description=get_current_time_description(),
    function=get_current_time
)

format_date_tool = Tool(
    name="format_date",
    description=format_date_description(),
    function=format_date
)

# Group all datetime tools
datetime_tools = [
    get_current_date_tool,
    get_current_time_tool,
    format_date_tool
]

# Export public API
__all__ = [
    'get_current_date',
    'get_current_time',
    'get_current_date_description',
    'get_current_time_description',
    'format_date',
    'format_date_description',
    'DatetimeInput',
    'DatetimeOutput',
    'datetime_tools',
    'get_current_date_tool',
    'get_current_time_tool',
    'format_date_tool'
] 
```

# src/tools/datetime/schema.py

```py
"""Datetime tool schemas.

This module defines the Pydantic models for datetime tool input and output.
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime as dt

class DatetimeInput(BaseModel):
    """Input for datetime tools."""
    format: Optional[str] = Field(None, description="Optional format string for date/time")

class DatetimeOutput(BaseModel):
    """Output from datetime tools."""
    result: str = Field(..., description="The formatted date or time string")
    timestamp: float = Field(..., description="Unix timestamp of when the result was generated")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @classmethod
    def create(cls, result: str) -> "DatetimeOutput":
        """Create a standard output object.
        
        Args:
            result: The formatted date or time string
            
        Returns:
            A DatetimeOutput object
        """
        now = dt.now()
        return cls(
            result=result,
            timestamp=now.timestamp(),
            metadata={"datetime": now.isoformat()}
        ) 
```

# src/tools/datetime/tool.py

```py
"""Datetime tool implementation.

This module provides the core functionality for datetime tools.
"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic_ai import RunContext

from .schema import DatetimeInput, DatetimeOutput

logger = logging.getLogger(__name__)

def get_current_date_description() -> str:
    """Get the description for the current date tool."""
    return "Get the current date in ISO format (YYYY-MM-DD)."

def get_current_time_description() -> str:
    """Get the description for the current time tool."""
    return "Get the current time in 24-hour format (HH:MM)."

def format_date_description() -> str:
    """Get the description for the format date tool."""
    return "Format a date string from one format to another."

async def get_current_date(ctx: RunContext[Dict], format: Optional[str] = None) -> Dict[str, Any]:
    """Get the current date.
    
    Args:
        ctx: The run context.
        format: Optional format string (default: ISO format YYYY-MM-DD).
        
    Returns:
        Dict with the formatted date string.
    """
    try:
        logger.info("Getting current date")
        now = datetime.now()
        
        if format:
            # Use the provided format string
            result = now.strftime(format)
            logger.info(f"Formatted date with custom format: {format}")
        else:
            # Use ISO format by default
            result = now.date().isoformat()
            logger.info(f"Formatted date with default ISO format")
        
        # Create and return standardized output
        output = DatetimeOutput.create(result)
        logger.info(f"Date result: {result}")
        return output.dict()
    except Exception as e:
        logger.error(f"Error getting current date: {str(e)}")
        return {
            "result": f"Error: {str(e)}",
            "timestamp": datetime.now().timestamp(),
            "metadata": {"error": str(e)}
        }

async def get_current_time(ctx: RunContext[Dict], format: Optional[str] = None) -> Dict[str, Any]:
    """Get the current time.
    
    Args:
        ctx: The run context.
        format: Optional format string (default: 24-hour format HH:MM).
        
    Returns:
        Dict with the formatted time string.
    """
    try:
        logger.info("Getting current time")
        now = datetime.now()
        
        if format:
            # Use the provided format string
            result = now.strftime(format)
            logger.info(f"Formatted time with custom format: {format}")
        else:
            # Use 24-hour format by default
            result = now.strftime("%H:%M")
            logger.info(f"Formatted time with default 24-hour format")
        
        # Create and return standardized output
        output = DatetimeOutput.create(result)
        logger.info(f"Time result: {result}")
        return output.dict()
    except Exception as e:
        logger.error(f"Error getting current time: {str(e)}")
        return {
            "result": f"Error: {str(e)}",
            "timestamp": datetime.now().timestamp(),
            "metadata": {"error": str(e)}
        }

async def format_date(ctx: RunContext[Dict], date_str: str, input_format: str = "%Y-%m-%d", output_format: str = "%B %d, %Y") -> Dict[str, Any]:
    """Format a date string from one format to another.
    
    Args:
        ctx: The run context.
        date_str: The date string to format
        input_format: The format of the input date string
        output_format: The desired output format
        
    Returns:
        Dict with the reformatted date string.
    """
    try:
        logger.info(f"Formatting date: {date_str} from {input_format} to {output_format}")
        parsed_date = datetime.strptime(date_str, input_format)
        result = parsed_date.strftime(output_format)
        logger.info(f"Formatted date result: {result}")
        
        # Create and return standardized output
        output = DatetimeOutput.create(result)
        return output.dict()
    except ValueError as e:
        error_msg = f"Error parsing date: {str(e)}"
        logger.error(error_msg)
        return {
            "result": error_msg,
            "timestamp": datetime.now().timestamp(),
            "metadata": {"error": str(e)}
        }
```

# src/tools/discord/__init__.py

```py
"""Discord tools for Automagik Agents.

Provides tools for interacting with Discord via API.
"""

# Import from tool module
from src.tools.discord.tool import (
    list_guilds_and_channels,
    get_guild_info,
    fetch_messages,
    send_message,
    get_list_guilds_description,
    get_guild_info_description,
    get_fetch_messages_description,
    get_send_message_description
)

# Import schema models
from src.tools.discord.schema import (
    DiscordChannel,
    DiscordGuild,
    DiscordMessage,
    DiscordResponse,
    ListGuildsResponse,
    GuildInfoResponse,
    FetchMessagesResponse,
    SendMessageResponse
)

# Import interface
from src.tools.discord.interface import (
    DiscordTools,
    discord_tools
)

# Export public API
__all__ = [
    # Tool functions
    'list_guilds_and_channels',
    'get_guild_info',
    'fetch_messages',
    'send_message',
    
    # Description functions
    'get_list_guilds_description',
    'get_guild_info_description',
    'get_fetch_messages_description',
    'get_send_message_description',
    
    # Schema models
    'DiscordChannel',
    'DiscordGuild',
    'DiscordMessage',
    'DiscordResponse',
    'ListGuildsResponse',
    'GuildInfoResponse',
    'FetchMessagesResponse',
    'SendMessageResponse',
    
    # Interface
    'DiscordTools',
    'discord_tools'
] 
```

# src/tools/discord/interface.py

```py
"""Discord tools interface.

This module provides a compatibility layer for Discord tools.
"""
import logging
from typing import List, Dict, Any
from pydantic_ai import RunContext
from pydantic_ai.tools import Tool

from .tool import (
    list_guilds_and_channels,
    get_guild_info,
    fetch_messages,
    send_message,
    get_list_guilds_description,
    get_guild_info_description,
    get_fetch_messages_description,
    get_send_message_description
)

logger = logging.getLogger(__name__)

class DiscordTools:
    """Discord tools interface for compatibility with old code."""
    
    def __init__(self, bot_token: str):
        """Initialize Discord tools with a bot token.
        
        Args:
            bot_token: Discord bot token
        """
        self.bot_token = bot_token
    
    async def list_guilds_and_channels(self, ctx: RunContext[Dict]) -> Dict[str, Any]:
        """Lists all guilds and channels the bot has access to.
        
        Args:
            ctx: The run context
            
        Returns:
            Dict with the guild and channel information
        """
        return await list_guilds_and_channels(ctx, self.bot_token)
    
    async def get_guild_info(self, ctx: RunContext[Dict], guild_id: str) -> Dict[str, Any]:
        """Retrieves information about a specific guild.
        
        Args:
            ctx: The run context
            guild_id: ID of the guild to retrieve information for
            
        Returns:
            Dict with the guild information
        """
        return await get_guild_info(ctx, self.bot_token, guild_id)
    
    async def fetch_messages(self, ctx: RunContext[Dict], channel_id: str, limit: int = 100) -> Dict[str, Any]:
        """Fetches messages from a specific channel.
        
        Args:
            ctx: The run context
            channel_id: ID of the channel to fetch messages from
            limit: Maximum number of messages to retrieve
            
        Returns:
            Dict with the fetched messages
        """
        return await fetch_messages(ctx, self.bot_token, channel_id, limit)
    
    async def send_message(self, ctx: RunContext[Dict], channel_id: str, content: str) -> Dict[str, Any]:
        """Sends a message to a specific channel.
        
        Args:
            ctx: The run context
            channel_id: ID of the channel to send the message to
            content: Content of the message to send
            
        Returns:
            Dict with information about the sent message
        """
        return await send_message(ctx, self.bot_token, channel_id, content)
    
    @property
    def tools(self) -> List:
        """Returns the list of available tool functions."""
        return [
            self.list_guilds_and_channels,
            self.get_guild_info,
            self.fetch_messages,
            self.send_message
        ]

# Create Discord tool instances
discord_list_guilds_tool = Tool(
    name="discord_list_guilds",
    description=get_list_guilds_description(),
    function=list_guilds_and_channels
)

discord_guild_info_tool = Tool(
    name="discord_guild_info",
    description=get_guild_info_description(),
    function=get_guild_info
)

discord_fetch_messages_tool = Tool(
    name="discord_fetch_messages",
    description=get_fetch_messages_description(),
    function=fetch_messages
)

discord_send_message_tool = Tool(
    name="discord_send_message",
    description=get_send_message_description(),
    function=send_message
)

# Group all Discord tools
discord_tools = [
    discord_list_guilds_tool,
    discord_guild_info_tool,
    discord_fetch_messages_tool,
    discord_send_message_tool
] 
```

# src/tools/discord/schema.py

```py
"""Discord tool schemas.

This module defines the Pydantic models for Discord tool input and output.
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List

class DiscordAttachment(BaseModel):
    """Model for Discord message attachments."""
    filename: str = Field(..., description="Name of the attached file")
    url: str = Field(..., description="URL of the attachment")

class DiscordReference(BaseModel):
    """Model for Discord message references."""
    message_id: Optional[str] = Field(None, description="ID of the referenced message")
    channel_id: Optional[str] = Field(None, description="ID of the channel containing the referenced message")
    guild_id: Optional[str] = Field(None, description="ID of the guild containing the referenced message")

class DiscordMessage(BaseModel):
    """Model for Discord messages."""
    id: str = Field(..., description="Message ID")
    content: str = Field(..., description="Message content")
    author: str = Field(..., description="Message author")
    timestamp: str = Field(..., description="Message timestamp")
    attachments: List[DiscordAttachment] = Field(default_factory=list, description="Message attachments")
    embeds: List[Dict[str, Any]] = Field(default_factory=list, description="Message embeds")
    type: str = Field(..., description="Message type")
    reference: Optional[DiscordReference] = Field(None, description="Message reference")

class DiscordChannel(BaseModel):
    """Model for Discord channels."""
    name: str = Field(..., description="Channel name")
    id: str = Field(..., description="Channel ID")
    type: str = Field(..., description="Channel type")

class DiscordGuild(BaseModel):
    """Model for Discord guilds."""
    name: str = Field(..., description="Guild name")
    id: str = Field(..., description="Guild ID")
    channels: List[DiscordChannel] = Field(default_factory=list, description="Guild channels")
    member_count: Optional[int] = Field(None, description="Number of members in the guild")

class DiscordResponse(BaseModel):
    """Base response model for Discord tools."""
    success: bool = Field(..., description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if the operation failed")

class ListGuildsResponse(DiscordResponse):
    """Response model for list_guilds_and_channels."""
    guilds: List[DiscordGuild] = Field(default_factory=list, description="List of guilds")

class GuildInfoResponse(DiscordResponse):
    """Response model for get_guild_info."""
    guild_info: Optional[DiscordGuild] = Field(None, description="Guild information")

class FetchMessagesResponse(DiscordResponse):
    """Response model for fetch_messages."""
    messages: List[DiscordMessage] = Field(default_factory=list, description="List of messages")

class SendMessageResponse(DiscordResponse):
    """Response model for send_message."""
    message: Optional[DiscordMessage] = Field(None, description="The sent message") 
```

# src/tools/discord/tool.py

```py
"""Discord tool implementation.

This module provides the core functionality for Discord tools.
"""
import logging
from typing import List, Optional, Dict, Any, Callable, Awaitable
import discord
import asyncio
from pydantic_ai import RunContext

from .schema import (
    DiscordChannel, DiscordGuild, DiscordMessage, DiscordResponse,
    ListGuildsResponse, GuildInfoResponse, FetchMessagesResponse, SendMessageResponse
)

logger = logging.getLogger(__name__)

class DiscordError(Exception):
    """Base exception for Discord API errors."""
    pass

def get_list_guilds_description() -> str:
    """Get description for the list_guilds_and_channels function."""
    return "Lists all guilds and channels the bot has access to."

def get_guild_info_description() -> str:
    """Get description for the get_guild_info function."""
    return "Retrieves information about a specific guild."

def get_fetch_messages_description() -> str:
    """Get description for the fetch_messages function."""
    return "Fetches messages from a specific channel."

def get_send_message_description() -> str:
    """Get description for the send_message function."""
    return "Sends a message to a specific channel."

async def _with_temp_client(bot_token: str, func: Callable[[discord.Client], Awaitable[Any]]) -> Any:
    """
    Helper function to create a temporary Discord client, perform an operation, then close the client.
    
    Args:
        bot_token: Discord bot token
        func: Async function to execute with the client
        
    Returns:
        Result of the function execution
    """
    client = discord.Client(intents=discord.Intents.default())
    ready_event = asyncio.Event()

    @client.event
    async def on_ready():
        ready_event.set()

    await client.login(bot_token)
    # Start the client in the background
    client_task = asyncio.create_task(client.connect())
    # Wait until the client signals it is ready
    await ready_event.wait()
    # Optional delay to ensure connection stability and guild population
    await asyncio.sleep(2)
    
    try:
        result = await func(client)
    finally:
        await client.close()
        await client_task
    
    return result

async def list_guilds_and_channels(ctx: RunContext[Dict], bot_token: str) -> Dict[str, Any]:
    """
    Lists all guilds and channels the bot has access to.
    
    Args:
        ctx: The run context
        bot_token: Discord bot token
        
    Returns:
        Dict with the guild and channel information
    """
    try:
        logger.info("Listing Discord guilds and channels")
        
        async def _list(client: discord.Client):
            guilds_info = []
            for guild in client.guilds:
                channels_info = [
                    {"name": channel.name, "id": str(channel.id), "type": str(channel.type)}
                    for channel in guild.channels
                ]
                guilds_info.append({
                    "name": guild.name,
                    "id": str(guild.id),
                    "channels": channels_info
                })
            return guilds_info

        guilds_info = await _with_temp_client(bot_token, _list)
        response = ListGuildsResponse(success=True, guilds=guilds_info)
        return response.dict()
    except Exception as e:
        logger.error(f"Error listing Discord guilds: {str(e)}")
        response = ListGuildsResponse(success=False, error=f"Error: {str(e)}")
        return response.dict()

async def get_guild_info(ctx: RunContext[Dict], bot_token: str, guild_id: str) -> Dict[str, Any]:
    """
    Retrieves information about a specific guild.
    
    Args:
        ctx: The run context
        bot_token: Discord bot token
        guild_id: ID of the guild to retrieve information for
        
    Returns:
        Dict with the guild information
    """
    try:
        logger.info(f"Getting information for Discord guild ID: {guild_id}")
        
        async def _get(client: discord.Client):
            guild = client.get_guild(int(guild_id))
            if guild:
                info = {
                    "name": guild.name,
                    "id": str(guild.id),
                    "member_count": guild.member_count,
                    "channels": [{"name": channel.name, "id": str(channel.id), "type": str(channel.type)} for channel in guild.channels]
                }
            else:
                info = None
            return info

        guild_info = await _with_temp_client(bot_token, _get)
        if guild_info:
            response = GuildInfoResponse(success=True, guild_info=guild_info)
        else:
            response = GuildInfoResponse(success=False, error=f"Guild with ID {guild_id} not found.")
        return response.dict()
    except Exception as e:
        logger.error(f"Error getting Discord guild info: {str(e)}")
        response = GuildInfoResponse(success=False, error=f"Error: {str(e)}")
        return response.dict()

async def fetch_messages(ctx: RunContext[Dict], bot_token: str, channel_id: str, limit: int = 100) -> Dict[str, Any]:
    """
    Fetches messages from a specific channel.
    
    Args:
        ctx: The run context
        bot_token: Discord bot token
        channel_id: ID of the channel to fetch messages from
        limit: Maximum number of messages to retrieve
        
    Returns:
        Dict with the fetched messages
    """
    try:
        logger.info(f"Fetching messages from Discord channel ID: {channel_id}, limit: {limit}")
        
        async def _fetch(client: discord.Client):
            channel = client.get_channel(int(channel_id))
            if isinstance(channel, discord.TextChannel):
                messages = []
                async for msg in channel.history(limit=limit):
                    messages.append(msg)
                message_data = [
                    {
                        "id": str(msg.id),
                        "content": msg.content,
                        "author": str(msg.author),
                        "timestamp": str(msg.created_at),
                        "attachments": [{"filename": a.filename, "url": a.url} for a in msg.attachments],
                        "embeds": [e.to_dict() for e in msg.embeds],
                        "type": str(msg.type),
                        "reference": {
                            "message_id": str(msg.reference.message_id),
                            "channel_id": str(msg.reference.channel_id),
                            "guild_id": str(msg.reference.guild_id)
                        } if msg.reference else None
                    }
                    for msg in messages
                ]
            else:
                message_data = None
            return message_data

        messages = await _with_temp_client(bot_token, _fetch)
        if messages is not None:
            response = FetchMessagesResponse(success=True, messages=messages)
        else:
            response = FetchMessagesResponse(success=False, error=f"Channel with ID {channel_id} is not a text channel or not found.")
        return response.dict()
    except Exception as e:
        logger.error(f"Error fetching Discord messages: {str(e)}")
        response = FetchMessagesResponse(success=False, error=f"Error: {str(e)}")
        return response.dict()

async def send_message(ctx: RunContext[Dict], bot_token: str, channel_id: str, content: str) -> Dict[str, Any]:
    """
    Sends a message to a specific channel.
    
    Args:
        ctx: The run context
        bot_token: Discord bot token
        channel_id: ID of the channel to send the message to
        content: Content of the message to send
        
    Returns:
        Dict with information about the sent message
    """
    try:
        logger.info(f"Sending message to Discord channel ID: {channel_id}")
        
        async def _send(client: discord.Client):
            channel = client.get_channel(int(channel_id))
            if isinstance(channel, discord.TextChannel):
                message = await channel.send(content)
                result = {
                    "id": str(message.id),
                    "content": message.content,
                    "author": str(message.author),
                    "timestamp": str(message.created_at)
                }
            else:
                result = None
            return result

        sent_message = await _with_temp_client(bot_token, _send)
        if sent_message:
            response = SendMessageResponse(success=True, message=sent_message)
        else:
            response = SendMessageResponse(success=False, error=f"Channel with ID {channel_id} is not a text channel or not found.")
        return response.dict()
    except Exception as e:
        logger.error(f"Error sending Discord message: {str(e)}")
        response = SendMessageResponse(success=False, error=f"Error: {str(e)}")
        return response.dict() 
```

# src/tools/evolution/__init__.py

```py
"""Evolution tools for Automagik Agents.

Provides tools for interacting with Evolution messaging API.
"""

# Import from tool module
from src.tools.evolution.tool import (
    send_message,
    get_chat_history,
    get_send_message_description,
    get_chat_history_description
)

# Import schema models
from src.tools.evolution.schema import (
    Message,
    SendMessageResponse,
    GetChatHistoryResponse
)

# Import interface
from src.tools.evolution.interface import (
    EvolutionTools,
    evolution_tools
)

# Export public API
__all__ = [
    # Tool functions
    'send_message',
    'get_chat_history',
    
    # Description functions
    'get_send_message_description',
    'get_chat_history_description',
    
    # Schema models
    'Message',
    'SendMessageResponse',
    'GetChatHistoryResponse',
    
    # Interface
    'EvolutionTools',
    'evolution_tools'
] 
```

# src/tools/evolution/interface.py

```py
"""Evolution tools interface.

This module provides a compatibility layer for Evolution tools.
"""
import logging
from typing import List, Dict, Any
from pydantic_ai import RunContext
from pydantic_ai.tools import Tool

from .tool import (
    send_message, 
    get_chat_history,
    get_send_message_description,
    get_chat_history_description
)

logger = logging.getLogger(__name__)

class EvolutionTools:
    """Tools for interacting with Evolution API."""

    def __init__(self, token: str):
        """Initialize with API token.
        
        Args:
            token: Evolution API token
        """
        self.token = token

    def get_tools(self) -> List[Any]:
        """Get tools for the agent."""
        return []

    async def send_message(self, phone: str, message: str) -> Dict[str, Any]:
        """Send a message to a phone number.

        Args:
            phone: The phone number to send the message to
            message: The message content

        Returns:
            Response data from the API
        """
        # Create a mock RunContext
        ctx = RunContext({})
        
        # Call the actual implementation
        result = await send_message(ctx, self.token, phone, message)
        
        # Simplify the result structure for backward compatibility
        if result.get("success", False):
            return {
                "success": True,
                "message_id": result.get("message_id", "unknown"),
                "timestamp": result.get("timestamp", "")
            }
        return {
            "success": False,
            "error": result.get("error", "Unknown error")
        }

    async def get_chat_history(self, phone: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat history for a phone number.

        Args:
            phone: The phone number to get history for
            limit: Maximum number of messages to return

        Returns:
            List of message objects
        """
        # Create a mock RunContext
        ctx = RunContext({})
        
        # Call the actual implementation
        result = await get_chat_history(ctx, self.token, phone, limit)
        
        # Extract the messages from the result
        if result.get("success", False) and "messages" in result:
            return result["messages"]
        return []

# Create Evolution tool instances
evolution_send_message_tool = Tool(
    name="evolution_send_message",
    description=get_send_message_description(),
    function=send_message
)

evolution_get_chat_history_tool = Tool(
    name="evolution_get_chat_history",
    description=get_chat_history_description(),
    function=get_chat_history
)

# Group all Evolution tools
evolution_tools = [
    evolution_send_message_tool,
    evolution_get_chat_history_tool
] 
```

# src/tools/evolution/schema.py

```py
"""Evolution tool schemas.

This module defines the Pydantic models for Evolution tool input and output.
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List

class Message(BaseModel):
    """Model for Evolution message data."""
    id: str = Field(..., description="Message ID")
    from_field: str = Field(..., description="Sender of the message", alias="from")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="Timestamp of the message")
    type: str = Field(..., description="Type of message (incoming/outgoing)")
    
    class Config:
        allow_population_by_field_name = True

class SendMessageResponse(BaseModel):
    """Response model for send_message."""
    success: bool = Field(..., description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if the operation failed")
    message_id: Optional[str] = Field(None, description="ID of the sent message")
    timestamp: Optional[str] = Field(None, description="Timestamp of the sent message")

class GetChatHistoryResponse(BaseModel):
    """Response model for get_chat_history."""
    success: bool = Field(..., description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if the operation failed")
    messages: List[Message] = Field(default_factory=list, description="List of messages in the chat history") 
```

# src/tools/evolution/tool.py

```py
"""Evolution tool implementation.

This module provides the core functionality for Evolution tools.
"""
import logging
from typing import Dict, List, Any, Optional
from pydantic_ai import RunContext

from .schema import Message, SendMessageResponse, GetChatHistoryResponse

logger = logging.getLogger(__name__)

def get_send_message_description() -> str:
    """Get description for the send_message function."""
    return "Send a message to a phone number via Evolution API."

def get_chat_history_description() -> str:
    """Get description for the get_chat_history function."""
    return "Get chat history for a phone number from Evolution API."

async def send_message(ctx: RunContext[Dict], token: str, phone: str, message: str) -> Dict[str, Any]:
    """Send a message to a phone number.

    Args:
        ctx: The run context
        token: Evolution API token
        phone: The phone number to send the message to
        message: The message content

    Returns:
        Dict with the response data
    """
    try:
        logger.info(f"Sending message to {phone}: {message}")
        
        # Mock implementation - in a real implementation, this would use the Evolution API
        # Return mock data
        response = SendMessageResponse(
            success=True,
            message_id="mock-message-id-12345",
            timestamp="2023-06-01T12:00:00.000Z"
        )
        return response.dict()
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        response = SendMessageResponse(
            success=False,
            error=f"Error: {str(e)}"
        )
        return response.dict()

async def get_chat_history(ctx: RunContext[Dict], token: str, phone: str, limit: int = 50) -> Dict[str, Any]:
    """Get chat history for a phone number.

    Args:
        ctx: The run context
        token: Evolution API token
        phone: The phone number to get history for
        limit: Maximum number of messages to return

    Returns:
        Dict with the chat history
    """
    try:
        logger.info(f"Getting chat history for {phone}, limit: {limit}")
        
        # Mock implementation - in a real implementation, this would use the Evolution API
        # Return mock data
        mock_messages = [
            {
                "id": "msg1",
                "from": phone,
                "content": "Hello, I need information about your products",
                "timestamp": "2023-06-01T11:50:00.000Z",
                "type": "incoming",
            },
            {
                "id": "msg2",
                "from": "system",
                "content": "Hi there! I'd be happy to help with information about our products. What specific products are you interested in?",
                "timestamp": "2023-06-01T11:51:00.000Z",
                "type": "outgoing",
            },
        ][:limit]
        
        response = GetChatHistoryResponse(
            success=True,
            messages=mock_messages
        )
        return response.dict()
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        response = GetChatHistoryResponse(
            success=False,
            error=f"Error: {str(e)}"
        )
        return response.dict() 
```

# src/tools/google_drive/__init__.py

```py
"""Google Drive tools for Automagik Agents.

Provides tools for interacting with Google Drive via API.
"""

# Import from tool module
from src.tools.google_drive.tool import (
    search_files,
    get_file_content,
    get_search_files_description,
    get_file_content_description
)

# Import schema models
from src.tools.google_drive.schema import (
    GoogleDriveFile,
    SearchFilesResponse,
    GetFileContentResponse
)

# Import interface
from src.tools.google_drive.interface import (
    GoogleDriveTools,
    google_drive_tools
)

# Export public API
__all__ = [
    # Tool functions
    'search_files',
    'get_file_content',
    
    # Description functions
    'get_search_files_description',
    'get_file_content_description',
    
    # Schema models
    'GoogleDriveFile',
    'SearchFilesResponse',
    'GetFileContentResponse',
    
    # Interface
    'GoogleDriveTools',
    'google_drive_tools'
] 
```

# src/tools/google_drive/interface.py

```py
"""Google Drive tools interface.

This module provides a compatibility layer for Google Drive tools.
"""
import logging
from typing import List, Dict, Any
from pydantic_ai import RunContext
from pydantic_ai.tools import Tool

from .tool import (
    search_files, 
    get_file_content,
    get_search_files_description,
    get_file_content_description
)

logger = logging.getLogger(__name__)

class GoogleDriveTools:
    """Tools for interacting with Google Drive API."""

    def __init__(self, token: str):
        """Initialize with API token.
        
        Args:
            token: Google API token
        """
        self.token = token

    def get_tools(self) -> List[Any]:
        """Get tools for the agent."""
        return []

    async def search_files(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for files in Google Drive.

        Args:
            query: The search query
            limit: Maximum number of results to return

        Returns:
            List of file information dictionaries
        """
        # Create a mock RunContext
        ctx = RunContext({})
        
        # Call the actual implementation
        result = await search_files(ctx, self.token, query, limit)
        
        # Extract the files from the result
        if result.get("success", False) and "files" in result:
            return result["files"]
        return []

    async def get_file_content(self, file_id: str) -> str:
        """Get the content of a file.

        Args:
            file_id: The ID of the file to get

        Returns:
            The file content as a string
        """
        # Create a mock RunContext
        ctx = RunContext({})
        
        # Call the actual implementation
        result = await get_file_content(ctx, self.token, file_id)
        
        # Extract the content from the result
        if result.get("success", False) and "content" in result:
            return result["content"]
        return f"Error retrieving content for file ID: {file_id}"

# Create Google Drive tool instances
google_drive_search_files_tool = Tool(
    name="google_drive_search_files",
    description=get_search_files_description(),
    function=search_files
)

google_drive_get_file_content_tool = Tool(
    name="google_drive_get_file_content",
    description=get_file_content_description(),
    function=get_file_content
)

# Group all Google Drive tools
google_drive_tools = [
    google_drive_search_files_tool,
    google_drive_get_file_content_tool
] 
```

# src/tools/google_drive/schema.py

```py
"""Google Drive tool schemas.

This module defines the Pydantic models for Google Drive tool input and output.
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List

class GoogleDriveFile(BaseModel):
    """Model for Google Drive file metadata."""
    id: str = Field(..., description="Google Drive file ID")
    name: str = Field(..., description="File name")
    mimeType: str = Field(..., description="MIME type of the file")
    webViewLink: str = Field(..., description="Web view link for the file")
    createdTime: str = Field(..., description="Creation time of the file")

class SearchFilesResponse(BaseModel):
    """Response model for search_files."""
    success: bool = Field(..., description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if the operation failed")
    files: List[GoogleDriveFile] = Field(default_factory=list, description="List of files matching the search query")

class GetFileContentResponse(BaseModel):
    """Response model for get_file_content."""
    success: bool = Field(..., description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if the operation failed")
    content: Optional[str] = Field(None, description="File content as a string")
    file_id: str = Field(..., description="ID of the requested file") 
```

# src/tools/google_drive/tool.py

```py
"""Google Drive tool implementation.

This module provides the core functionality for Google Drive tools.
"""
import logging
from typing import Dict, List, Any, Optional
from pydantic_ai import RunContext

from .schema import GoogleDriveFile, SearchFilesResponse, GetFileContentResponse

logger = logging.getLogger(__name__)

def get_search_files_description() -> str:
    """Get description for the search_files function."""
    return "Search for files in Google Drive by query."

def get_file_content_description() -> str:
    """Get description for the get_file_content function."""
    return "Get the content of a file from Google Drive by file ID."

async def search_files(ctx: RunContext[Dict], token: str, query: str, limit: int = 10) -> Dict[str, Any]:
    """Search for files in Google Drive.

    Args:
        ctx: The run context
        token: Google API token
        query: The search query
        limit: Maximum number of results to return

    Returns:
        Dict with the search results
    """
    try:
        logger.info(f"Searching for files with query: {query}, limit: {limit}")
        
        # Mock implementation - in a real implementation, this would use the Google Drive API
        # Return mock data
        mock_files = [
            {
                "id": "file1",
                "name": "Product Catalog.pdf",
                "mimeType": "application/pdf",
                "webViewLink": "https://drive.google.com/file/d/mock1/view",
                "createdTime": "2023-01-01T12:00:00.000Z",
            },
            {
                "id": "file2",
                "name": "Price List.xlsx",
                "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "webViewLink": "https://drive.google.com/file/d/mock2/view",
                "createdTime": "2023-02-01T12:00:00.000Z",
            },
        ][:limit]
        
        response = SearchFilesResponse(
            success=True,
            files=mock_files
        )
        return response.dict()
    except Exception as e:
        logger.error(f"Error searching Google Drive files: {str(e)}")
        response = SearchFilesResponse(
            success=False,
            error=f"Error: {str(e)}"
        )
        return response.dict()

async def get_file_content(ctx: RunContext[Dict], token: str, file_id: str) -> Dict[str, Any]:
    """Get the content of a file.

    Args:
        ctx: The run context
        token: Google API token
        file_id: The ID of the file to get

    Returns:
        Dict with the file content
    """
    try:
        logger.info(f"Getting file content for file_id: {file_id}")
        
        # Mock implementation - in a real implementation, this would use the Google Drive API
        # Return mock data
        mock_content = f"This is mock file content for file ID: {file_id}"
        
        response = GetFileContentResponse(
            success=True,
            content=mock_content,
            file_id=file_id
        )
        return response.dict()
    except Exception as e:
        logger.error(f"Error getting Google Drive file content: {str(e)}")
        response = GetFileContentResponse(
            success=False,
            error=f"Error: {str(e)}",
            file_id=file_id
        )
        return response.dict() 
```

# src/tools/memory/__init__.py

```py
"""Memory tools for Automagik Agents.

Provides tools for reading and writing memories for agents, implementing the pydantic-ai tool interface.
These tools allow agents to store and retrieve information across conversations and sessions.
"""

# Import core functionality
from src.tools.memory.tool import (
    read_memory,
    create_memory,
    update_memory,
    get_read_memory_description,
    get_create_memory_description,
    get_update_memory_description,
    # SimpleAgent compatibility functions
    get_memory_tool,
    store_memory_tool,
    list_memories_tool
)

# Import schemas
from src.tools.memory.schema import (
    MemoryReadResult,
    MemoryCreateResponse,
    MemoryUpdateResponse,
    Memory,
    ReadMemoryInput,
    CreateMemoryInput,
    UpdateMemoryInput
)

# Import utility functions
from src.tools.memory.interface import (
    invalidate_memory_cache,
    validate_memory_name,
    format_memory_content
)

# Import provider
from src.tools.memory.provider import (
    MemoryProvider,
    get_memory_provider_for_agent
)

# For backwards compatibility (to be removed in future versions)
def write_memory(*args, **kwargs):
    """Deprecated: Use create_memory or update_memory instead.
    
    This function is maintained for backward compatibility only.
    It will decide whether to create or update a memory based on the presence of memory_id.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("write_memory is deprecated - use create_memory or update_memory instead")
    
    # Check if memory_id exists in kwargs
    if 'memory_id' in kwargs and kwargs['memory_id'] is not None:
        # Update existing memory
        # Re-map parameters to match update_memory's signature
        # update_memory expects: content, memory_id, name
        if len(args) >= 3:
            return update_memory(args[0], args[2], memory_id=kwargs.get('memory_id'))
        else:
            return update_memory(kwargs.get('ctx'), kwargs.get('content', ''), 
                             memory_id=kwargs.get('memory_id'))
    else:
        # Create new memory
        # create_memory expects: ctx, name, content, description, read_mode, access, metadata
        return create_memory(*args, **kwargs)

# Expose only these functions at the package level
__all__ = [
    # Core memory functions
    'read_memory',
    'create_memory',
    'update_memory',
    'write_memory',  # For backwards compatibility
    
    # Description functions
    'get_read_memory_description',
    'get_create_memory_description',
    'get_update_memory_description',
    
    # SimpleAgent compatibility functions
    'get_memory_tool',
    'store_memory_tool', 
    'list_memories_tool',
    
    # Schemas
    'MemoryReadResult',
    'MemoryCreateResponse',
    'MemoryUpdateResponse',
    'Memory',
    'ReadMemoryInput',
    'CreateMemoryInput',
    'UpdateMemoryInput',
    
    # Utilities
    'invalidate_memory_cache',
    'validate_memory_name',
    'format_memory_content',
    'MemoryProvider',
    'get_memory_provider_for_agent'
] 
```

# src/tools/memory/interface.py

```py
"""Memory tool interface helpers.

This module provides helper functions and decorators for memory tools.
"""
from typing import Dict, Any, Optional, Callable
import logging
import re
from functools import wraps

logger = logging.getLogger(__name__)

def invalidate_memory_cache(func: Callable) -> Callable:
    """Decorator that invalidates the memory cache after the function is called.
    
    This ensures that any memory updates are immediately reflected in
    subsequent system prompt generation.
    
    Args:
        func: The function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Call the original function
        result = await func(*args, **kwargs)
        
        # Get the memory provider
        from src.tools.memory.provider import get_memory_provider_for_agent
        
        # Try to extract agent_id from args/kwargs
        agent_id = None
        
        # Check if first argument might be a context with dependencies
        if args and hasattr(args[0], 'deps'):
            deps = args[0].deps
            if hasattr(deps, '_agent_id_numeric'):
                agent_id = deps._agent_id_numeric
        
        # Check if agent_id is in kwargs
        if 'agent_id' in kwargs:
            agent_id = kwargs['agent_id']
        
        # If we found an agent_id, invalidate its cache
        if agent_id:
            provider = get_memory_provider_for_agent(agent_id)
            if provider:
                provider.invalidate_cache()
                logger.debug(f"Invalidated memory cache for agent {agent_id}")
            else:
                logger.warning(f"No memory provider found for agent {agent_id}")
        else:
            logger.warning(f"Could not determine agent_id for cache invalidation in {func.__name__}")
        
        return result
    
    return wrapper

def validate_memory_name(name: str) -> bool:
    """Validate that a memory name contains only allowed characters.
    
    Args:
        name: Memory name to validate
        
    Returns:
        True if valid, False otherwise
    """
    return bool(re.match(r'^[a-zA-Z0-9_]+$', name))

def format_memory_content(content: Any) -> str:
    """Format memory content for storage.
    
    Args:
        content: Memory content to format
        
    Returns:
        Formatted string representation
    """
    if isinstance(content, str):
        return content
    
    # For other types, convert to string representation
    try:
        import json
        return json.dumps(content)
    except:
        return str(content) 
```

# src/tools/memory/provider.py

```py
"""Memory provider for the memory tool.

This module provides a class to manage memory retrieval and caching.
"""
from typing import Dict, Any, Optional, List, Callable, Set
import logging
from functools import lru_cache
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Global registry of memory providers by agent ID
_memory_providers: Dict[int, "MemoryProvider"] = {}

def get_memory_provider_for_agent(agent_id: int) -> Optional["MemoryProvider"]:
    """Get a memory provider for a specific agent.
    
    Args:
        agent_id: The numeric ID of the agent
        
    Returns:
        MemoryProvider instance or None
    """
    return _memory_providers.get(agent_id)

class MemoryProvider:
    """Provider interface for memory-related system prompt functions.
    
    This class acts as a bridge between our database-backed memory system
    and pydantic-ai's dynamic system prompt functions.
    """
    
    def __init__(self, agent_id: int):
        """Initialize the memory provider.
        
        Args:
            agent_id: The ID of the agent this provider serves
        """
        self.agent_id = agent_id
        self._cache_expiry = datetime.now()
        self._memory_cache = {}
        self._cache_ttl = timedelta(seconds=30)  # 30-second TTL by default
        
        # Register this provider in the global registry
        _memory_providers[agent_id] = self
        
    def set_cache_ttl(self, seconds: int) -> None:
        """Set the cache time-to-live in seconds.
        
        Args:
            seconds: Cache TTL in seconds
        """
        self._cache_ttl = timedelta(seconds=seconds)
    
    def invalidate_cache(self) -> None:
        """Invalidate the memory cache to force fresh fetches."""
        self._cache_expiry = datetime.now()
        self._memory_cache = {}
        logger.debug(f"Memory cache for agent {self.agent_id} invalidated")
    
    def _should_refresh_cache(self) -> bool:
        """Check if the cache should be refreshed."""
        return datetime.now() > self._cache_expiry
    
    def _refresh_cache(self) -> None:
        """Refresh the memory cache from database."""
        from src.db import list_memories
        
        try:
            memories = list_memories(agent_id=self.agent_id)
            
            # Build a new cache
            new_cache = {}
            for memory in memories:
                if hasattr(memory, 'name') and memory.name:
                    new_cache[memory.name] = memory.content
            
            # Update the cache and expiry
            self._memory_cache = new_cache
            self._cache_expiry = datetime.now() + self._cache_ttl
            logger.debug(f"Refreshed memory cache for agent {self.agent_id} with {len(new_cache)} items")
            
        except Exception as e:
            logger.error(f"Error refreshing memory cache for agent {self.agent_id}: {str(e)}")
    
    def get_memory(self, name: str, default: Any = None) -> Any:
        """Get a memory value by name.
        
        Args:
            name: Name of the memory to retrieve
            default: Default value if memory doesn't exist
            
        Returns:
            Memory content or default value
        """
        # Refresh cache if needed
        if self._should_refresh_cache():
            self._refresh_cache()
        
        # Return from cache
        return self._memory_cache.get(name, default)
    
    def get_all_memories(self) -> Dict[str, Any]:
        """Get all memories as a dictionary.
        
        Returns:
            Dictionary of all memory name-value pairs
        """
        # Refresh cache if needed
        if self._should_refresh_cache():
            self._refresh_cache()
        
        return self._memory_cache.copy()
    
    def get_memories_by_prefix(self, prefix: str) -> Dict[str, Any]:
        """Get all memories with names starting with the given prefix.
        
        Args:
            prefix: Prefix to filter memories by
            
        Returns:
            Dictionary of matching memory name-value pairs
        """
        # Refresh cache if needed
        if self._should_refresh_cache():
            self._refresh_cache()
        
        return {
            name: value for name, value in self._memory_cache.items() 
            if name.startswith(prefix)
        }
    
    def create_system_prompt_function(self, memory_name: str, template: str = "{value}") -> Callable:
        """Create a function that can be used as a system prompt function.
        
        This creates a function that can be decorated with @agent.system_prompt
        to dynamically inject memory values into the system prompt.
        
        Args:
            memory_name: Name of the memory to inject
            template: Template string with {value} placeholder
            
        Returns:
            Function that returns the formatted memory value
        """
        def memory_prompt_function() -> str:
            """System prompt function for memory injection."""
            value = self.get_memory(memory_name, f"No memory found for {memory_name}")
            try:
                return template.format(value=value)
            except Exception as e:
                logger.error(f"Error formatting memory {memory_name}: {str(e)}")
                return f"Error formatting memory {memory_name}"
        
        # Set metadata for better debugging
        memory_prompt_function.__name__ = f"memory_{memory_name}"
        memory_prompt_function.__doc__ = f"Inject memory '{memory_name}' into system prompt"
        
        return memory_prompt_function 
```

# src/tools/memory/schema.py

```py
"""Memory tool schemas.

This module defines the Pydantic models for memory tool input and output.
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List, Union
from uuid import UUID
from datetime import datetime

# Common models
class MemoryBase(BaseModel):
    """Base model for memory objects."""
    name: str = Field(..., description="The name of the memory")
    content: Any = Field(..., description="The content of the memory")
    
class MemoryMetadata(BaseModel):
    """Metadata associated with a memory."""
    created_at: Optional[datetime] = Field(None, description="When the memory was created")
    updated_at: Optional[datetime] = Field(None, description="When the memory was last updated")
    agent_id: Optional[int] = Field(None, description="ID of the agent that owns this memory")
    user_id: Optional[int] = Field(None, description="ID of the user that owns this memory")
    session_id: Optional[str] = Field(None, description="ID of the session that owns this memory")
    
class Memory(MemoryBase):
    """Complete memory object with all fields."""
    id: str = Field(..., description="Unique identifier for the memory")
    description: Optional[str] = Field(None, description="Optional description of the memory")
    read_mode: str = Field("tool_calling", description="How this memory should be used (system_prompt or tool_calling)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

# Input models
class ReadMemoryInput(BaseModel):
    """Input for reading a memory."""
    name: Optional[str] = Field(None, description="The name of the memory to read")
    memory_id: Optional[str] = Field(None, description="The ID of the memory to read")
    list_all: bool = Field(False, description="Whether to list all memories")
    
class CreateMemoryInput(BaseModel):
    """Input for creating a memory."""
    name: str = Field(..., description="The name of the memory to create")
    content: Union[str, Dict[str, Any]] = Field(..., description="The content to store in the memory")
    description: Optional[str] = Field(None, description="Optional description of the memory")
    read_mode: str = Field("tool_calling", description="How this memory should be used (system_prompt or tool_calling)")
    scope: Optional[str] = Field(None, description="Scope of the memory (global, user, or session)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
class UpdateMemoryInput(BaseModel):
    """Input for updating a memory."""
    memory_id: str = Field(..., description="The ID of the memory to update")
    content: Union[str, Dict[str, Any]] = Field(..., description="The new content for the memory")
    name: Optional[str] = Field(None, description="Optional new name for the memory")
    description: Optional[str] = Field(None, description="Optional new description for the memory")
    
# Output models
class MemoryReadResult(BaseModel):
    """Result of a memory read operation."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    content: Optional[Any] = Field(None, description="The content of the memory if found")
    memory: Optional[Memory] = Field(None, description="The complete memory object if found")
    memories: Optional[List[Memory]] = Field(None, description="List of memories if list_all was True")

class MemoryCreateResponse(BaseModel):
    """Response for a memory creation operation."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    id: Optional[str] = Field(None, description="The ID of the created memory if successful")
    name: Optional[str] = Field(None, description="The name of the created memory if successful")

class MemoryUpdateResponse(BaseModel):
    """Response for a memory update operation."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message describing the result")
    id: Optional[str] = Field(None, description="The ID of the updated memory if successful")
    name: Optional[str] = Field(None, description="The name of the updated memory if successful") 
```

# src/tools/memory/tool.py

```py
"""Memory tool implementation.

This module provides the core functionality for reading, creating,
and updating memories for agents.
"""
import logging
import json
import os
import requests
import uuid
from typing import Dict, Any, Optional, Union, List
from uuid import UUID
from datetime import datetime

from pydantic_ai import RunContext
from pydantic_ai.messages import ModelRequest
from src.db import get_agent_by_name, create_memory as create_memory_in_db
from src.db import list_memories as list_memories_in_db
from src.db import get_memory as get_memory_in_db
from src.db import update_memory as update_memory_in_db
from src.db.repository.memory import get_memory_by_name as db_get_memory_by_name
from src.db.repository.memory import create_memory as db_create_memory
from src.db.models import Memory as DBMemory
from src.agents.models.agent_factory import AgentFactory

from .schema import (
    ReadMemoryInput, CreateMemoryInput, UpdateMemoryInput,
    MemoryReadResult, MemoryCreateResponse, MemoryUpdateResponse,
    Memory
)
from .interface import invalidate_memory_cache, validate_memory_name, format_memory_content

logger = logging.getLogger(__name__)

def get_read_memory_description() -> str:
    """Basic description for the read_memory tool."""
    return "Read memories from the database by name or ID, or list all available memories."

def get_create_memory_description() -> str:
    """Basic description for the create_memory tool."""
    return "Create a new memory in the database with the specified name, content, and metadata."

def get_update_memory_description() -> str:
    """Basic description for the update_memory tool."""
    return "Update an existing memory in the database with new content or metadata."

# Create mock objects for the RunContext initialization
def _create_mock_context():
    """Create a mock context with the required parameters for RunContext."""
    # Create minimal mock objects to satisfy RunContext requirements
    model = {"name": "mock-model", "provider": "mock"}
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    prompt = ModelRequest(parts=[])
    
    return model, usage, prompt

def map_agent_id(ctx: Optional[RunContext], agent_id_raw: Optional[str] = None) -> tuple:
    """Map agent ID to numeric ID and get user/session context.
    
    Args:
        ctx: The run context.
        agent_id_raw: Optional raw agent ID string.
        
    Returns:
        Tuple of (agent_id, user_id, session_id)
    """
    # Default values
    agent_id = None
    user_id = 1  # Default user ID
    session_id = None
    
    # Try to extract from context first
    if ctx and hasattr(ctx, 'deps'):
        deps = ctx.deps
        
        # Try to get agent_id from deps
        if hasattr(deps, '_agent_id_numeric'):
            agent_id = deps._agent_id_numeric
        
        # Try to get user_id from deps
        if hasattr(deps, '_user_id'):
            user_id = deps._user_id
        
        # Try to get session_id from deps
        if hasattr(deps, '_session_id'):
            session_id = deps._session_id
    
    # If agent_id is still None, try agent_id_raw
    if agent_id is None and agent_id_raw:
        try:
            # Try to get agent by name from database
            agent = get_agent_by_name(agent_id_raw)
            if agent and hasattr(agent, 'id'):
                agent_id = agent.id
        except Exception as e:
            logger.warning(f"Could not get agent by name '{agent_id_raw}': {str(e)}")
    
    # If still no agent_id, try to use first available agent
    if agent_id is None:
        try:
            available_agents = AgentFactory.list_available_agents()
            if available_agents:
                agent = get_agent_by_name(available_agents[0])
                if agent and hasattr(agent, 'id'):
                    agent_id = agent.id
        except Exception as e:
            logger.warning(f"Could not get first available agent: {str(e)}")
    
    return agent_id, user_id, session_id

def _convert_to_memory_object(memory_dict: Dict[str, Any]) -> Memory:
    """Convert a memory dictionary to a Memory object.
    
    Args:
        memory_dict: Dictionary representation of a memory
        
    Returns:
        Memory object
    """
    # Copy only the fields we need for the Memory model
    memory_data = {
        "id": str(memory_dict.get("id", "")),
        "name": memory_dict.get("name", ""),
        "content": memory_dict.get("content", ""),
        "description": memory_dict.get("description", None),
        "read_mode": memory_dict.get("read_mode", "tool_calling"),
    }
    
    # Add metadata if available
    metadata = memory_dict.get("metadata", None)
    if metadata:
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except:
                pass
        memory_data["metadata"] = metadata
    
    # Create Memory object
    return Memory(**memory_data)

# SimpleAgent compatibility functions
async def get_memory_tool(ctx_or_key, key_or_user_id=None, user_id=None):
    """Retrieve a memory by key.
    
    This function can be called in two ways:
    1. get_memory_tool(context, key) - where context contains user_id
    2. get_memory_tool(key, user_id=user_id) - directly passing key and optional user_id
    
    Args:
        ctx_or_key: Either a context dictionary or the memory key to retrieve
        key_or_user_id: Either the memory key (if ctx_or_key is context) or user_id (if ctx_or_key is key)
        user_id: Optional user ID to filter memories (only used in the second calling pattern)
        
    Returns:
        The memory content as a string, or an error message if not found
    """
    # Determine which calling pattern is being used
    if isinstance(ctx_or_key, dict):
        # First calling pattern: get_memory_tool(context, key)
        context = ctx_or_key
        key = key_or_user_id
        user_id = context.get("user_id")
        logger.info(f"Getting memory with key: {key} from context (user_id: {user_id})")
    else:
        # Second calling pattern: get_memory_tool(key, user_id)
        key = ctx_or_key
        if user_id is None:
            user_id = key_or_user_id
        logger.info(f"Getting memory with key: {key} for user_id: {user_id}")
    
    try:
        # Create a proper context with required parameters
        model, usage, prompt = _create_mock_context()
        ctx = RunContext({}, model=model, usage=usage, prompt=prompt)
        
        # Try to get memory by name with user_id filter if provided
        memory = db_get_memory_by_name(name=key, user_id=user_id)
        if memory:
            content = memory.content
            if isinstance(content, dict):
                return str(content)
            return content
        
        # If not found with user_id, try without user_id filter
        if user_id is not None:
            memory = db_get_memory_by_name(name=key)
            if memory:
                logger.info(f"Found memory {key} without user_id filter")
                content = memory.content
                if isinstance(content, dict):
                    return str(content)
                return content
                
        return f"Memory with key '{key}' not found"
    except Exception as e:
        logger.error(f"Error getting memory: {str(e)}")
        return f"Error getting memory with key '{key}': {str(e)}"

async def store_memory_tool(ctx: dict, key: str, content: str) -> str:
    """Store a memory with the given key.
    
    Args:
        ctx: The context dictionary with agent and user information
        key: The key to store the memory under
        content: The memory content to store
        
    Returns:
        Confirmation message
    """
    logger.info(f"Storing memory with key: {key}")
    try:
        # Create a proper context with required parameters
        model, usage, prompt = _create_mock_context()
        run_ctx = RunContext({}, model=model, usage=usage, prompt=prompt)
        logger.info(f"Create memory context: {run_ctx}")
        logger.info(f"Context deps: {run_ctx.deps}")
        
        # Extract agent_id and user_id from the provided context if available
        agent_id = ctx.get("agent_id", 1)  # Default agent ID
        user_id = ctx.get("user_id", None)  # Default to None, will look for thread context
        
        # If still no user_id, try the thread context
        if user_id is None:
            try:
                # Try to get thread context (if available)
                import threading
                from src.context import ThreadContext
                thread_context = getattr(threading.current_thread(), "_context", None)
                if thread_context and isinstance(thread_context, ThreadContext):
                    if hasattr(thread_context, "user_id") and thread_context.user_id:
                        user_id = thread_context.user_id
                        logger.info(f"Extracted user_id={user_id} from thread context")
            except Exception as e:
                logger.warning(f"Could not extract user/session from thread context: {str(e)}")
        
        # If still no user_id, try the current request context
        if user_id is None:
            try:
                # Try to get from global request state if available
                from src.context import get_current_user_id
                current_user_id = get_current_user_id()
                if current_user_id:
                    user_id = current_user_id
                    logger.info(f"Extracted user_id={user_id} from current request")
            except Exception as e:
                logger.warning(f"Could not extract user_id from request context: {str(e)}")
        
        # Fallback to default user_id if not found
        if user_id is None:
            user_id = 1
            logger.warning(f"Using default user_id={user_id}, could not extract from context")
        
        logger.info(f"Using values: agent_id={agent_id}, user_id={user_id}, session_id=None")
        
        # Check if this memory already exists and get its read_mode
        read_mode = "tool_calling"  # Default for new memories
        try:
            # Import the repository function
            from src.db.repository.memory import get_memory_by_name
            
            # Try to find existing memory with this key
            existing_memory = get_memory_by_name(name=key, agent_id=agent_id, user_id=user_id)
            
            if existing_memory:
                # If memory exists, preserve its read_mode
                read_mode = existing_memory.read_mode
                logger.info(f"Found existing memory with key '{key}', preserving read_mode='{read_mode}'")
        except Exception as e:
            logger.warning(f"Error checking for existing memory: {str(e)}, using default read_mode='tool_calling'")
        
        logger.info(f"Creating/updating memory: name={key}, read_mode={read_mode}")
        
        # Create Memory object
        memory = DBMemory(
            id=uuid.uuid4(),
            name=key,
            content=content,
            description=f"Memory created by SimpleAgent",
            agent_id=agent_id,
            user_id=user_id,
            read_mode=read_mode,  # Use preserved read_mode
            metadata={"created_at": str(datetime.now())}
        )
        
        # Store the memory
        memory_id = db_create_memory(memory)
        
        if memory_id:
            return f"Memory stored with key '{key}'"
        else:
            return f"Failed to store memory with key '{key}'"
    except Exception as e:
        logger.error(f"Error storing memory: {str(e)}")
        return f"Error storing memory with key '{key}': {str(e)}"

async def list_memories_tool(prefix: Optional[str] = None) -> str:
    """List available memories, optionally filtered by prefix.
    
    Args:
        prefix: Optional prefix to filter memory keys
        
    Returns:
        List of memory keys as a string
    """
    try:
        # Get all memories
        memories = list_memories_in_db()
        
        # Filter by prefix if needed
        memory_names = []
        for memory in memories:
            if not prefix or memory.name.startswith(prefix):
                memory_names.append(memory.name)
        
        if not memory_names:
            return "No memories found"
        
        return "\n".join(memory_names)
    except Exception as e:
        logger.error(f"Error listing memories: {str(e)}")
        return f"Error listing memories: {str(e)}"

@invalidate_memory_cache
async def read_memory(ctx: RunContext[Dict], memory_id: Optional[str] = None, 
                name: Optional[str] = None, list_all: bool = False) -> Dict[str, Any]:
    """Read a memory from the database.
    
    Args:
        ctx: The run context.
        memory_id: Optional ID of the memory to read.
        name: Optional name of the memory to read.
        list_all: If True and no specific memory is requested, list all memories.
        
    Returns:
        Dict with memory content or error message.
    """
    try:
        # Map agent ID and get context
        agent_id, user_id, session_id = map_agent_id(ctx)
        
        # Log what we're doing
        if memory_id:
            logger.info(f"Reading memory by ID: {memory_id}")
        elif name:
            logger.info(f"Reading memory by name: {name}")
        elif list_all:
            logger.info(f"Listing all memories for agent {agent_id}")
        else:
            return MemoryReadResult(
                success=False,
                message="Either memory_id, name, or list_all must be provided"
            ).dict()
        
        # Log context
        logger.info(f"Context: agent_id={agent_id}, user_id={user_id}, session_id={session_id}")
        
        # If list_all is True, return all memories
        if list_all:
            try:
                # Use direct database call
                memories = list_memories_in_db(agent_id=agent_id)
                
                # Convert to Memory objects
                memory_objects = []
                for memory in memories:
                    if hasattr(memory, '__dict__'):
                        memory_dict = memory.__dict__
                        memory_objects.append(_convert_to_memory_object(memory_dict))
                
                # Return response
                return MemoryReadResult(
                    success=True,
                    message=f"Found {len(memory_objects)} memories",
                    memories=memory_objects
                ).dict()
            except Exception as e:
                logger.error(f"Error listing memories: {str(e)}")
                return MemoryReadResult(
                    success=False,
                    message=f"Error listing memories: {str(e)}"
                ).dict()
        
        # Try to read specific memory
        try:
            # Determine how to retrieve the memory
            if memory_id:
                # Get memory by ID
                memory = get_memory_in_db(memory_id=memory_id)
            elif name:
                # Get memory by name
                memories = list_memories_in_db(agent_id=agent_id, name=name)
                memory = memories[0] if memories else None
            else:
                memory = None
            
            # Check if memory was found
            if not memory:
                return MemoryReadResult(
                    success=False,
                    message=f"Memory not found"
                ).dict()
            
            # Convert to Memory object
            memory_obj = _convert_to_memory_object(memory.__dict__)
            
            # Return response
            return MemoryReadResult(
                success=True,
                message="Memory found",
                content=memory_obj.content,
                memory=memory_obj
            ).dict()
        except Exception as e:
            logger.error(f"Error reading memory: {str(e)}")
            return MemoryReadResult(
                success=False,
                message=f"Error reading memory: {str(e)}"
            ).dict()
    except Exception as e:
        logger.error(f"Error in read_memory: {str(e)}")
        return MemoryReadResult(
            success=False,
            message=f"Error in read_memory: {str(e)}"
        ).dict()

@invalidate_memory_cache
async def create_memory(ctx: RunContext[Dict], name: str, content: Union[str, Dict[str, Any]], 
                 description: Optional[str] = None, read_mode: str = "tool_calling",
                 scope: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a new memory in the database.
    
    Args:
        ctx: The run context.
        name: The name of the memory to create.
        content: The content to store in the memory.
        description: Optional description of the memory.
        read_mode: How this memory should be used.
        scope: Optional scope of the memory.
        metadata: Optional metadata to store with the memory.
        
    Returns:
        Dict with the result of the operation.
    """
    try:
        # Validate name
        if not validate_memory_name(name):
            return MemoryCreateResponse(
                success=False,
                message=f"Invalid memory name: {name}. Names must contain only letters, numbers, and underscores."
            ).dict()
        
        # Map agent ID and get context
        agent_id, user_id, session_id = map_agent_id(ctx)
        
        # Log what we're doing
        logger.info(f"Creating memory: name={name}, scope={scope}, read_mode={read_mode}")
        logger.info(f"Context: agent_id={agent_id}, user_id={user_id}, session_id={session_id}")
        
        # Format content
        processed_content = format_memory_content(content)
        
        # Determine the scope of the memory
        if scope == "global":
            # Global memories are accessible to all users of this agent
            memory_user_id = None
            memory_session_id = None
        elif scope == "user":
            # User memories are accessible to a specific user across all sessions
            memory_user_id = user_id
            memory_session_id = None
        elif scope == "session":
            # Session memories are accessible only in the current session
            memory_user_id = user_id
            memory_session_id = session_id
        else:
            # Default to user scope if not specified
            memory_user_id = user_id
            memory_session_id = None
        
        # Create the memory
        try:
            # Use direct database call
            memory_data = {
                "name": name,
                "content": processed_content,
                "agent_id": agent_id,
                "user_id": memory_user_id,
                "session_id": memory_session_id,
                "read_mode": read_mode,
                "description": description
            }
            
            # Add metadata if provided
            if metadata is not None:
                if isinstance(metadata, dict):
                    memory_data["metadata"] = json.dumps(metadata)
                else:
                    memory_data["metadata"] = metadata
            
            # Create memory in database
            memory = create_memory_in_db(**memory_data)
            
            # Check if memory was created
            if not memory or not hasattr(memory, 'id'):
                return MemoryCreateResponse(
                    success=False,
                    message="Memory creation failed"
                ).dict()
            
            # Return success response
            return MemoryCreateResponse(
                success=True,
                message="Memory created successfully",
                id=str(memory.id),
                name=memory.name
            ).dict()
        except Exception as e:
            logger.error(f"Error creating memory: {str(e)}")
            return MemoryCreateResponse(
                success=False,
                message=f"Error creating memory: {str(e)}"
            ).dict()
    except Exception as e:
        logger.error(f"Error in create_memory: {str(e)}")
        return MemoryCreateResponse(
            success=False,
            message=f"Error in create_memory: {str(e)}"
        ).dict()

@invalidate_memory_cache
async def update_memory(ctx: RunContext[Dict], content: Union[str, Dict[str, Any]], 
                 memory_id: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None) -> Dict[str, Any]:
    """Update an existing memory in the database.
    
    Args:
        ctx: The run context.
        content: The new content for the memory.
        memory_id: The ID of the memory to update.
        name: The name of the memory to update.
        description: Optional new description for the memory.
        
    Returns:
        Dict with the result of the operation.
    """
    try:
        # Map agent ID and get context
        agent_id, user_id, session_id = map_agent_id(ctx)
        
        # Log what we're doing
        if memory_id:
            logger.info(f"Updating memory by ID: {memory_id}")
        elif name:
            logger.info(f"Updating memory by name: {name}")
        else:
            return MemoryUpdateResponse(
                success=False,
                message="Either memory_id or name must be provided"
            ).dict()
        
        # Log context
        logger.info(f"Context: agent_id={agent_id}, user_id={user_id}, session_id={session_id}")
        
        # Format content
        processed_content = format_memory_content(content)
        
        # Determine which memory to update
        try:
            if memory_id:
                # Get memory by ID first to make sure it exists
                memory = get_memory_in_db(memory_id=memory_id)
                if not memory:
                    return MemoryUpdateResponse(
                        success=False,
                        message=f"Memory with ID {memory_id} not found"
                    ).dict()
                
                # Update memory
                update_data = {"content": processed_content}
                if description is not None:
                    update_data["description"] = description
                if name is not None:
                    update_data["name"] = name
                
                # Update memory in database
                updated_memory = update_memory_in_db(memory_id=memory_id, **update_data)
                
                # Return response
                return MemoryUpdateResponse(
                    success=True,
                    message="Memory updated successfully",
                    id=str(updated_memory.id),
                    name=updated_memory.name
                ).dict()
            elif name:
                # Find memory by name
                memories = list_memories_in_db(agent_id=agent_id, name=name)
                if not memories:
                    return MemoryUpdateResponse(
                        success=False,
                        message=f"Memory with name {name} not found"
                    ).dict()
                
                # Use the first matching memory
                memory = memories[0]
                
                # Update memory
                update_data = {"content": processed_content}
                if description is not None:
                    update_data["description"] = description
                
                # Update memory in database
                updated_memory = update_memory_in_db(memory_id=str(memory.id), **update_data)
                
                # Return response
                return MemoryUpdateResponse(
                    success=True,
                    message="Memory updated successfully",
                    id=str(updated_memory.id),
                    name=updated_memory.name
                ).dict()
        except Exception as e:
            logger.error(f"Error updating memory: {str(e)}")
            return MemoryUpdateResponse(
                success=False,
                message=f"Error updating memory: {str(e)}"
            ).dict()
    except Exception as e:
        logger.error(f"Error in update_memory: {str(e)}")
        return MemoryUpdateResponse(
            success=False,
            message=f"Error in update_memory: {str(e)}"
        ).dict() 
```

# src/tools/notion/__init__.py

```py
"""Notion tools package.

This package provides tools for interacting with Notion API.
"""
from .interface import (
    # Individual tools
    notion_search_databases,
    notion_create_database,
    notion_update_database,
    notion_get_database,
    notion_query_database,
    notion_create_page,
    notion_update_page,
    notion_get_page,
    notion_archive_page,
    notion_get_page_property,
    notion_get_page_property_item,
    notion_get_block,
    notion_update_block,
    notion_delete_block,
    notion_get_block_children,
    notion_append_block_children,
    
    # Tool groups
    notion_database_tools,
    notion_page_tools,
    notion_block_tools,
    
    # All tools
    notion_tools,
)

__all__ = [
    # Individual tools
    "notion_search_databases",
    "notion_create_database",
    "notion_update_database",
    "notion_get_database",
    "notion_query_database",
    "notion_create_page",
    "notion_update_page",
    "notion_get_page",
    "notion_archive_page",
    "notion_get_page_property",
    "notion_get_page_property_item",
    "notion_get_block",
    "notion_update_block",
    "notion_delete_block",
    "notion_get_block_children",
    "notion_append_block_children",
    
    # Tool groups
    "notion_database_tools",
    "notion_page_tools",
    "notion_block_tools",
    
    # All tools
    "notion_tools",
] 
```

# src/tools/notion/interface.py

```py
"""Notion tools interface.

This module defines the interface for Notion tools.
"""
from typing import Dict, List

from pydantic_ai import Tool

from .tool import (
    # Tool descriptions
    get_search_databases_description,
    get_create_database_description,
    get_update_database_description,
    get_get_database_description,
    get_query_database_description,
    get_create_database_item_description,
    get_update_database_item_description,
    get_get_page_description,
    get_create_page_description,
    get_update_page_description,
    get_archive_page_description,
    get_get_page_property_description,
    get_get_page_property_item_description,
    get_get_block_description,
    get_update_block_description,
    get_delete_block_description,
    get_get_block_children_description,
    get_append_block_children_description,
    
    # Tool implementations
    search_databases,
    create_database,
    update_database,
    get_database,
    query_database,
    create_page,
    update_page,
    get_page,
    archive_page,
    get_page_property,
    get_page_property_item,
    get_block,
    update_block,
    delete_block,
    get_block_children,
    append_block_children,
)

# Database tools
notion_search_databases = Tool(
    name="notion_search_databases",
    description=get_search_databases_description(),
    function=search_databases,
)

notion_create_database = Tool(
    name="notion_create_database",
    description=get_create_database_description(),
    function=create_database,
)

notion_update_database = Tool(
    name="notion_update_database",
    description=get_update_database_description(),
    function=update_database,
)

notion_get_database = Tool(
    name="notion_get_database",
    description=get_get_database_description(),
    function=get_database,
)

notion_query_database = Tool(
    name="notion_query_database",
    description=get_query_database_description(),
    function=query_database,
)

# Page tools
notion_create_page = Tool(
    name="notion_create_page",
    description=get_create_page_description(),
    function=create_page,
)

notion_update_page = Tool(
    name="notion_update_page",
    description=get_update_page_description(),
    function=update_page,
)

notion_get_page = Tool(
    name="notion_get_page",
    description=get_get_page_description(),
    function=get_page,
)

notion_archive_page = Tool(
    name="notion_archive_page",
    description=get_archive_page_description(),
    function=archive_page,
)

notion_get_page_property = Tool(
    name="notion_get_page_property",
    description=get_get_page_property_description(),
    function=get_page_property,
)

notion_get_page_property_item = Tool(
    name="notion_get_page_property_item",
    description=get_get_page_property_item_description(),
    function=get_page_property_item,
)

# Block tools
notion_get_block = Tool(
    name="notion_get_block",
    description=get_get_block_description(),
    function=get_block,
)

notion_update_block = Tool(
    name="notion_update_block",
    description=get_update_block_description(),
    function=update_block,
)

notion_delete_block = Tool(
    name="notion_delete_block",
    description=get_delete_block_description(),
    function=delete_block,
)

notion_get_block_children = Tool(
    name="notion_get_block_children",
    description=get_get_block_children_description(),
    function=get_block_children,
)

notion_append_block_children = Tool(
    name="notion_append_block_children",
    description=get_append_block_children_description(),
    function=append_block_children,
)

# Group tools by category
notion_database_tools = [
    notion_search_databases,
    notion_create_database,
    notion_update_database,
    notion_get_database,
    notion_query_database,
]

notion_page_tools = [
    notion_create_page,
    notion_update_page,
    notion_get_page,
    notion_archive_page,
    notion_get_page_property,
    notion_get_page_property_item,
]

notion_block_tools = [
    notion_get_block,
    notion_update_block,
    notion_delete_block,
    notion_get_block_children,
    notion_append_block_children,
]

# All Notion tools
notion_tools: List[Tool] = [
    *notion_database_tools,
    *notion_page_tools,
    *notion_block_tools,
] 
```

# src/tools/notion/schema.py

```py
"""Notion tools schema.

This module defines the schemas for Notion tools.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class NotionResponse(BaseModel):
    """Base response model for Notion tools."""
    success: bool = Field(description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if the operation failed")


class DatabaseSearchResponse(NotionResponse):
    """Response model for notion_search_databases tool."""
    results: List[Dict[str, Any]] = Field(default_factory=list, description="List of database objects")
    has_more: bool = Field(default=False, description="Whether there are more results available")
    next_cursor: Optional[str] = Field(None, description="Cursor for pagination")


class DatabaseQueryResponse(NotionResponse):
    """Response model for notion_query_database tool."""
    results: List[Dict[str, Any]] = Field(default_factory=list, description="List of page objects")
    has_more: bool = Field(default=False, description="Whether there are more results available")
    next_cursor: Optional[str] = Field(None, description="Cursor for pagination")


class PagePropertyResponse(NotionResponse):
    """Response model for notion_get_page_property tool."""
    property: Optional[Dict[str, Any]] = Field(None, description="The page property data")


class PagePropertyItemResponse(NotionResponse):
    """Response model for notion_get_page_property_item tool."""
    results: List[Dict[str, Any]] = Field(default_factory=list, description="List of property items")
    has_more: bool = Field(default=False, description="Whether there are more results available")
    next_cursor: Optional[str] = Field(None, description="Cursor for pagination")


class BlockChildrenResponse(NotionResponse):
    """Response model for notion_get_block_children and notion_append_block_children tools."""
    results: List[Dict[str, Any]] = Field(default_factory=list, description="List of block objects")
    has_more: bool = Field(default=False, description="Whether there are more results available")
    next_cursor: Optional[str] = Field(None, description="Cursor for pagination") 
```

# src/tools/notion/tool.py

```py
"""Notion tool implementation.

This module provides the core functionality for Notion tools.
"""
import logging
import os
from typing import List, Optional, Dict, Any
from pydantic_ai import RunContext
from notion_client import Client

from .schema import (
    NotionResponse,
    DatabaseSearchResponse, 
    DatabaseQueryResponse,
    PagePropertyResponse,
    PagePropertyItemResponse,
    BlockChildrenResponse
)

logger = logging.getLogger(__name__)

class NotionError(Exception):
    """Base exception for Notion API errors"""
    pass

# Helper functions
def get_notion_token() -> str:
    """Gets the Notion token from environment variables."""
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise ValueError("NOTION_TOKEN environment variable not set")
    return token

def initialize_notion_client() -> Client:
    """Initialize a Notion client using the API token."""
    try:
        token = get_notion_token()
        return Client(auth=token)
    except Exception as e:
        logger.error(f"Failed to initialize Notion client: {str(e)}")
        raise NotionError(f"Failed to initialize Notion client: {str(e)}")

# Tool descriptions
def get_search_databases_description() -> str:
    """Get description for search_databases function."""
    return "Search for databases shared with the integration."

def get_create_database_description() -> str:
    """Get description for create_database function."""
    return "Creates a new database as a child of an existing page."

def get_update_database_description() -> str:
    """Get description for update_database function."""
    return "Updates an existing database."

def get_get_database_description() -> str:
    """Get description for get_database function."""
    return "Retrieves a database by ID."

def get_query_database_description() -> str:
    """Get description for query_database function."""
    return "Queries a database with optional filters and sorting."

def get_create_database_item_description() -> str:
    """Get description for create_database_item function."""
    return "Creates a new item in a database."

def get_update_database_item_description() -> str:
    """Get description for update_database_item function."""
    return "Updates an existing database item."

def get_get_page_description() -> str:
    """Get description for get_page function."""
    return "Retrieves a page by ID."

def get_create_page_description() -> str:
    """Get description for create_page function."""
    return "Creates a new page."

def get_update_page_description() -> str:
    """Get description for update_page function."""
    return "Updates an existing page."

def get_archive_page_description() -> str:
    """Get description for archive_page function."""
    return "Archives (deletes) a page."

def get_get_page_property_description() -> str:
    """Get description for get_page_property function."""
    return "Retrieves a page property by ID."

def get_get_page_property_item_description() -> str:
    """Get description for get_page_property_item function."""
    return "Retrieves a page property item."

def get_get_block_description() -> str:
    """Get description for get_block function."""
    return "Retrieves a block by ID."

def get_update_block_description() -> str:
    """Get description for update_block function."""
    return "Updates a block."

def get_delete_block_description() -> str:
    """Get description for delete_block function."""
    return "Deletes (archives) a block."

def get_get_block_children_description() -> str:
    """Get description for get_block_children function."""
    return "Retrieves the children of a block."

def get_append_block_children_description() -> str:
    """Get description for append_block_children function."""
    return "Appends children to a block."

# Database tools
async def search_databases(
    ctx: RunContext[Dict],
    query: str = "",
    start_cursor: Optional[str] = None,
    page_size: int = 100,
) -> Dict[str, Any]:
    """
    Search for databases shared with the integration.

    Args:
        ctx: The run context
        query: Search query (default: "", which returns all databases)
        start_cursor: Starting point for the results
        page_size: Maximum number of databases to return (default: 100)
    
    Returns:
        Dict with search results
    """
    try:
        logger.info(f"Searching Notion databases with query: '{query}'")
        notion = initialize_notion_client()
        
        response = notion.search(
            query=query,
            filter={"property": "object", "value": "database"},
            start_cursor=start_cursor,
            page_size=page_size,
        )

        result = DatabaseSearchResponse(
            success=True,
            results=response.get("results", []),
            has_more=response.get("has_more", False),
            next_cursor=response.get("next_cursor")
        )
        return result.dict()
    except Exception as e:
        logger.error(f"Error searching databases: {str(e)}")
        result = DatabaseSearchResponse(
            success=False,
            error=f"Failed to search databases: {str(e)}",
            results=[]
        )
        return result.dict()

async def create_database(
    ctx: RunContext[Dict],
    parent: Dict[str, Any],
    title: List[Dict[str, Any]],
    properties: Dict[str, Dict[str, Any]],
    icon: Optional[Dict[str, Any]] = None,
    cover: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Creates a new database as a child of an existing page.

    Args:
        ctx: The run context
        parent: Parent page info
        title: Database title
        properties: Database properties schema
        icon: Database icon
        cover: Database cover
    
    Returns:
        Dict with the created database
    """
    try:
        logger.info(f"Creating Notion database with title: {title}")
        notion = initialize_notion_client()
        
        database = notion.databases.create(
            parent=parent, 
            title=title, 
            properties=properties, 
            icon=icon, 
            cover=cover
        )
        
        return {"success": True, "database": database}
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        return {"success": False, "error": f"Failed to create database: {str(e)}"}

async def query_database(
    ctx: RunContext[Dict],
    database_id: str,
    filter_dict: Optional[Dict[str, Any]] = None,
    sorts: Optional[List[Dict[str, Any]]] = None,
    start_cursor: Optional[str] = None,
    page_size: int = 100,
) -> Dict[str, Any]:
    """
    Queries a database with optional filters and sorting.

    Args:
        ctx: The run context
        database_id: The ID of the database to query
        filter_dict: Filter conditions
        sorts: Sort conditions
        start_cursor: Starting point for pagination
        page_size: Maximum number of results to return (default: 100)
    
    Returns:
        Dict with query results
    """
    try:
        logger.info(f"Querying Notion database: {database_id}")
        notion = initialize_notion_client()
        
        # Default sort by created time if no sort specified
        default_sort = [{"timestamp": "created_time", "direction": "descending"}]
        query_args = {
            "database_id": database_id,
            "page_size": page_size,
            "sorts": sorts if sorts is not None else default_sort,
        }

        if filter_dict is not None:
            query_args["filter"] = filter_dict

        if start_cursor is not None:
            query_args["start_cursor"] = start_cursor

        response = notion.databases.query(**query_args)
        
        result = DatabaseQueryResponse(
            success=True,
            results=response.get("results", []),
            has_more=response.get("has_more", False),
            next_cursor=response.get("next_cursor")
        )
        return result.dict()
    except Exception as e:
        logger.error(f"Error querying database: {str(e)}")
        result = DatabaseQueryResponse(
            success=False,
            error=f"Failed to query database: {str(e)}",
            results=[]
        )
        return result.dict()

async def get_database(
    ctx: RunContext[Dict],
    database_id: str,
) -> Dict[str, Any]:
    """
    Retrieves a database by ID.

    Args:
        ctx: The run context
        database_id: The ID of the database to retrieve
    
    Returns:
        Dict with the database details
    """
    try:
        logger.info(f"Getting Notion database: {database_id}")
        notion = initialize_notion_client()
        
        database = notion.databases.retrieve(database_id=database_id)
        
        return {"success": True, "database": database}
    except Exception as e:
        logger.error(f"Error retrieving database: {str(e)}")
        return {"success": False, "error": f"Failed to retrieve database: {str(e)}"}

async def update_database(
    ctx: RunContext[Dict],
    database_id: str,
    title: Optional[List[Dict[str, Any]]] = None,
    properties: Optional[Dict[str, Dict[str, Any]]] = None,
    icon: Optional[Dict[str, Any]] = None,
    cover: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Updates an existing database.

    Args:
        ctx: The run context
        database_id: The ID of the database to update
        title: New database title
        properties: Updated properties schema
        icon: Updated icon
        cover: Updated cover
    
    Returns:
        Dict with the updated database
    """
    try:
        logger.info(f"Updating Notion database: {database_id}")
        notion = initialize_notion_client()
        
        # Build update payload with only provided fields
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if properties is not None:
            update_data["properties"] = properties
        if icon is not None:
            update_data["icon"] = icon
        if cover is not None:
            update_data["cover"] = cover
        
        database = notion.databases.update(database_id=database_id, **update_data)
        
        return {"success": True, "database": database}
    except Exception as e:
        logger.error(f"Error updating database: {str(e)}")
        return {"success": False, "error": f"Failed to update database: {str(e)}"}

# Page tools
async def get_page(
    ctx: RunContext[Dict],
    page_id: str,
) -> Dict[str, Any]:
    """
    Retrieves a page by ID.

    Args:
        ctx: The run context
        page_id: The ID of the page to retrieve
    
    Returns:
        Dict with the page details
    """
    try:
        logger.info(f"Getting Notion page: {page_id}")
        notion = initialize_notion_client()
        
        page = notion.pages.retrieve(page_id=page_id)
        
        return {"success": True, "page": page}
    except Exception as e:
        logger.error(f"Error retrieving page: {str(e)}")
        return {"success": False, "error": f"Failed to retrieve page: {str(e)}"}

async def create_page(
    ctx: RunContext[Dict],
    parent: Dict[str, Any],
    properties: Dict[str, Dict[str, Any]],
    icon: Optional[Dict[str, Any]] = None,
    cover: Optional[Dict[str, Any]] = None,
    children: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Creates a new page.

    Args:
        ctx: The run context
        parent: Parent database or page
        properties: Page properties
        icon: Page icon
        cover: Page cover
        children: Page content blocks
    
    Returns:
        Dict with the created page
    """
    try:
        logger.info(f"Creating Notion page with parent: {parent}")
        notion = initialize_notion_client()
        
        # Build page creation payload
        page_data = {
            "parent": parent,
            "properties": properties,
        }
        
        if icon is not None:
            page_data["icon"] = icon
        if cover is not None:
            page_data["cover"] = cover
        if children is not None:
            page_data["children"] = children
        
        page = notion.pages.create(**page_data)
        
        return {"success": True, "page": page}
    except Exception as e:
        logger.error(f"Error creating page: {str(e)}")
        return {"success": False, "error": f"Failed to create page: {str(e)}"}

async def update_page(
    ctx: RunContext[Dict],
    page_id: str,
    properties: Optional[Dict[str, Dict[str, Any]]] = None,
    icon: Optional[Dict[str, Any]] = None,
    cover: Optional[Dict[str, Any]] = None,
    archived: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Updates an existing page.

    Args:
        ctx: The run context
        page_id: The ID of the page to update
        properties: Updated page properties
        icon: Updated icon
        cover: Updated cover
        archived: Set to True to archive the page
    
    Returns:
        Dict with the updated page
    """
    try:
        logger.info(f"Updating Notion page: {page_id}")
        notion = initialize_notion_client()
        
        # Build update payload with only provided fields
        update_data = {}
        if properties is not None:
            update_data["properties"] = properties
        if icon is not None:
            update_data["icon"] = icon
        if cover is not None:
            update_data["cover"] = cover
        if archived is not None:
            update_data["archived"] = archived
        
        page = notion.pages.update(page_id=page_id, **update_data)
        
        return {"success": True, "page": page}
    except Exception as e:
        logger.error(f"Error updating page: {str(e)}")
        return {"success": False, "error": f"Failed to update page: {str(e)}"}

async def archive_page(
    ctx: RunContext[Dict],
    page_id: str,
) -> Dict[str, Any]:
    """
    Archives (deletes) a page.

    Args:
        ctx: The run context
        page_id: The ID of the page to archive
    
    Returns:
        Dict with the result of the operation
    """
    try:
        logger.info(f"Archiving Notion page: {page_id}")
        notion = initialize_notion_client()
        
        page = notion.pages.update(page_id=page_id, archived=True)
        
        return {"success": True, "page": page}
    except Exception as e:
        logger.error(f"Error archiving page: {str(e)}")
        return {"success": False, "error": f"Failed to archive page: {str(e)}"}

async def get_page_property(
    ctx: RunContext[Dict],
    page_id: str,
    property_id: str,
) -> Dict[str, Any]:
    """
    Retrieves a page property by ID.

    Args:
        ctx: The run context
        page_id: The ID of the page
        property_id: The ID of the property to retrieve
    
    Returns:
        Dict with the property details
    """
    try:
        logger.info(f"Getting Notion page property: {property_id} from page {page_id}")
        notion = initialize_notion_client()
        
        property_data = notion.pages.properties.retrieve(
            page_id=page_id, 
            property_id=property_id
        )
        
        result = PagePropertyResponse(
            success=True,
            property=property_data
        )
        return result.dict()
    except Exception as e:
        logger.error(f"Error retrieving page property: {str(e)}")
        result = PagePropertyResponse(
            success=False,
            error=f"Failed to retrieve page property: {str(e)}"
        )
        return result.dict()

async def get_page_property_item(
    ctx: RunContext[Dict],
    page_id: str,
    property_id: str,
    start_cursor: Optional[str] = None,
    page_size: int = 100,
) -> Dict[str, Any]:
    """
    Retrieves a page property item list.

    Args:
        ctx: The run context
        page_id: The ID of the page
        property_id: The ID of the property to retrieve
        start_cursor: Pagination cursor
        page_size: Maximum number of results to return (default: 100)
    
    Returns:
        Dict with the property items
    """
    try:
        logger.info(f"Getting Notion page property items: {property_id} from page {page_id}")
        notion = initialize_notion_client()
        
        params = {"page_size": page_size}
        if start_cursor:
            params["start_cursor"] = start_cursor
            
        property_items = notion.pages.properties.retrieve(
            page_id=page_id,
            property_id=property_id,
            **params
        )
        
        result = PagePropertyItemResponse(
            success=True,
            results=property_items.get("results", []),
            has_more=property_items.get("has_more", False),
            next_cursor=property_items.get("next_cursor")
        )
        return result.dict()
    except Exception as e:
        logger.error(f"Error retrieving page property items: {str(e)}")
        result = PagePropertyItemResponse(
            success=False,
            error=f"Failed to retrieve page property items: {str(e)}",
            results=[]
        )
        return result.dict()

# Block tools
async def get_block(
    ctx: RunContext[Dict],
    block_id: str,
) -> Dict[str, Any]:
    """
    Retrieves a block by ID.

    Args:
        ctx: The run context
        block_id: The ID of the block to retrieve
    
    Returns:
        Dict with the block details
    """
    try:
        logger.info(f"Getting Notion block: {block_id}")
        notion = initialize_notion_client()
        
        block = notion.blocks.retrieve(block_id=block_id)
        
        return {"success": True, "block": block}
    except Exception as e:
        logger.error(f"Error retrieving block: {str(e)}")
        return {"success": False, "error": f"Failed to retrieve block: {str(e)}"}

async def update_block(
    ctx: RunContext[Dict],
    block_id: str,
    block_data: Dict[str, Any],
    archived: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Updates a block.

    Args:
        ctx: The run context
        block_id: The ID of the block to update
        block_data: The updated block content
        archived: Set to True to archive the block
    
    Returns:
        Dict with the updated block
    """
    try:
        logger.info(f"Updating Notion block: {block_id}")
        notion = initialize_notion_client()
        
        # Build update payload
        update_data = block_data.copy()
        if archived is not None:
            update_data["archived"] = archived
        
        block = notion.blocks.update(block_id=block_id, **update_data)
        
        return {"success": True, "block": block}
    except Exception as e:
        logger.error(f"Error updating block: {str(e)}")
        return {"success": False, "error": f"Failed to update block: {str(e)}"}

async def delete_block(
    ctx: RunContext[Dict],
    block_id: str,
) -> Dict[str, Any]:
    """
    Deletes (archives) a block.

    Args:
        ctx: The run context
        block_id: The ID of the block to delete
    
    Returns:
        Dict with the result of the operation
    """
    try:
        logger.info(f"Deleting Notion block: {block_id}")
        notion = initialize_notion_client()
        
        block = notion.blocks.update(block_id=block_id, archived=True)
        
        return {"success": True, "block": block}
    except Exception as e:
        logger.error(f"Error deleting block: {str(e)}")
        return {"success": False, "error": f"Failed to delete block: {str(e)}"}

async def get_block_children(
    ctx: RunContext[Dict],
    block_id: str,
    start_cursor: Optional[str] = None,
    page_size: int = 100,
) -> Dict[str, Any]:
    """
    Retrieves the children of a block.

    Args:
        ctx: The run context
        block_id: The ID of the block
        start_cursor: Pagination cursor
        page_size: Maximum number of results to return (default: 100)
    
    Returns:
        Dict with the block's children
    """
    try:
        logger.info(f"Getting children of Notion block: {block_id}")
        notion = initialize_notion_client()
        
        params = {"block_id": block_id, "page_size": page_size}
        if start_cursor:
            params["start_cursor"] = start_cursor
            
        response = notion.blocks.children.list(**params)
        
        result = BlockChildrenResponse(
            success=True,
            results=response.get("results", []),
            has_more=response.get("has_more", False),
            next_cursor=response.get("next_cursor")
        )
        return result.dict()
    except Exception as e:
        logger.error(f"Error retrieving block children: {str(e)}")
        result = BlockChildrenResponse(
            success=False,
            error=f"Failed to retrieve block children: {str(e)}",
            results=[]
        )
        return result.dict()

async def append_block_children(
    ctx: RunContext[Dict],
    block_id: str,
    children: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Appends children to a block.

    Args:
        ctx: The run context
        block_id: The ID of the block
        children: The children blocks to append
    
    Returns:
        Dict with the result of the operation
    """
    try:
        logger.info(f"Appending children to Notion block: {block_id}")
        notion = initialize_notion_client()
        
        response = notion.blocks.children.append(
            block_id=block_id,
            children=children
        )
        
        result = BlockChildrenResponse(
            success=True,
            results=response.get("results", []),
            has_more=False,  # Always False for append operation
            next_cursor=None  # Always None for append operation
        )
        return result.dict()
    except Exception as e:
        logger.error(f"Error appending block children: {str(e)}")
        result = BlockChildrenResponse(
            success=False,
            error=f"Failed to append block children: {str(e)}",
            results=[]
        )
        return result.dict() 
```

# src/utils/logging.py

```py
import os
import logging
from typing import Dict, Optional
from src.config import settings, LogLevel

class PrettyFormatter(logging.Formatter):
    """A formatter that adds colors and emojis to log messages."""

    def __init__(self, include_timestamp: bool = True):
        self.include_timestamp = include_timestamp
        format_str = '%(message)s'
        if include_timestamp:
            format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        super().__init__(format_str)
        
        self.colors = {
            logging.INFO: '\033[92m',  # Green
            logging.ERROR: '\033[91m',  # Red
            logging.WARNING: '\033[93m',  # Yellow
            logging.DEBUG: '\033[94m',  # Blue
        }
        self.reset = '\033[0m'

        self.emojis = {
            logging.INFO: '📝',
            logging.ERROR: '❌',
            logging.WARNING: '⚠️',
            logging.DEBUG: '🔍',
        }

    def format(self, record):
        if not record.exc_info:
            level = record.levelno
            if level in self.colors:
                record.msg = f"{self.emojis.get(level, '')} {self.colors[level]}{record.msg}{self.reset}"
        return super().format(record)

def get_log_level(level: LogLevel) -> int:
    """Convert LogLevel enum to logging level."""
    log_levels = {
        LogLevel.DEBUG: logging.DEBUG,
        LogLevel.INFO: logging.INFO,
        LogLevel.WARNING: logging.WARNING,
        LogLevel.ERROR: logging.ERROR,
        LogLevel.CRITICAL: logging.CRITICAL
    }
    return log_levels[level]

def configure_logging():
    """Configure logging with pretty formatting and proper log level."""
    # Get log level from settings
    log_level = get_log_level(settings.AM_LOG_LEVEL)
    verbose_logging = settings.AM_VERBOSE_LOGGING
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create and configure stream handler
    handler = logging.StreamHandler()
    handler.setFormatter(PrettyFormatter(include_timestamp=verbose_logging))
    root_logger.addHandler(handler)

    # Configure module-specific log levels
    configure_module_log_levels(verbose_logging)

    # Configure Logfire if token is present
    if settings.LOGFIRE_TOKEN:
        try:
            import logfire
            os.environ["LOGFIRE_TOKEN"] = settings.LOGFIRE_TOKEN
            logfire.configure(scrubbing=False)  # Logfire reads token from environment
            logfire.instrument_pydantic_ai()
        except Exception as e:
            print(f"Warning: Failed to configure Logfire: {str(e)}")
    elif not settings.LOGFIRE_IGNORE_NO_CONFIG:
        print("Warning: LOGFIRE_TOKEN is not set. Tracing will be disabled.")

def configure_module_log_levels(verbose_logging: bool):
    """Configure log levels for specific modules based on verbosity setting."""
    # Always restrict certain modules regardless of verbosity
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    
    # If not in verbose mode, restrict more modules
    if not verbose_logging:
        # Database operations
        logging.getLogger('src.db').setLevel(logging.INFO)
        
        # HTTP requests - restrict details in non-verbose mode
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        
        # API requests in non-verbose mode
        logging.getLogger('src.api').setLevel(logging.INFO)
        
        # Memory system in non-verbose mode 
        memory_logger = logging.getLogger('src.memory.message_history')
        memory_logger.setLevel(logging.INFO)

```

# src/utils/multimodal.py

```py
"""Utility functions for multimodal content processing.

This module provides helper functions for handling multimodal content 
such as images, audio, and documents.
"""

import base64
import logging
import json
import re
import mimetypes
from typing import Dict, Any, Optional, Tuple, List, Union
import requests
from pathlib import Path
import io

logger = logging.getLogger(__name__)

def detect_content_type(url_or_data: str) -> str:
    """Detect content type based on URL extension or base64 data.
    
    Args:
        url_or_data: URL or base64 data
        
    Returns:
        MIME type string
    """
    # Check if it's a URL
    if url_or_data.startswith(('http://', 'https://')):
        # Try to determine from URL extension
        ext = Path(url_or_data.split('?')[0]).suffix.lower()
        guessed_type = mimetypes.guess_type(url_or_data)[0]
        
        if guessed_type:
            return guessed_type
            
        # If mimetypes module couldn't detect, use common types
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
            return f"image/{ext[1:]}"
        elif ext in ['.mp3', '.wav', '.ogg', '.m4a']:
            return f"audio/{ext[1:]}"
        elif ext in ['.mp4', '.webm', '.mov']:
            return "video/mp4"
        elif ext == '.pdf':
            return "application/pdf"
        elif ext in ['.doc', '.docx']:
            return "application/msword"
        
        # If we can't determine from extension, try HEAD request
        try:
            response = requests.head(url_or_data, timeout=5)
            if 'Content-Type' in response.headers:
                return response.headers['Content-Type'].split(';')[0]
        except Exception as e:
            logger.warning(f"Error determining content type from URL {url_or_data}: {str(e)}")
            
        # Default to octet-stream
        return "application/octet-stream"
        
    # Check if it's base64 data
    if url_or_data.startswith('data:'):
        # Extract MIME type from data URL
        match = re.match(r'data:([^;]+);base64,', url_or_data)
        if match:
            return match.group(1)
    
    # Detect by examining first few bytes
    try:
        # Get first few bytes from base64 content
        if ',' in url_or_data:
            data = url_or_data.split(',')[1]
        else:
            data = url_or_data
            
        # Remove any non-base64 characters
        data = re.sub(r'[^A-Za-z0-9+/=]', '', data)
        
        # Decode first few bytes
        header = base64.b64decode(data[:20] + "=" * ((4 - len(data[:20]) % 4) % 4))
        
        # Detect image types
        if header.startswith(b'\xff\xd8\xff'):
            return 'image/jpeg'
        elif header.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'image/png'
        elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return 'image/gif'
        elif header.startswith(b'RIFF') and header[8:12] == b'WEBP':
            return 'image/webp'
            
        # Detect audio types
        if header.startswith(b'ID3') or header.startswith(b'\xff\xfb') or header.startswith(b'\xff\xf3'):
            return 'audio/mpeg'
        elif header.startswith(b'RIFF') and header[8:12] == b'WAVE':
            return 'audio/wav'
            
        # Detect PDF
        if header.startswith(b'%PDF'):
            return 'application/pdf'
    except Exception as e:
        logger.warning(f"Error detecting MIME type from binary data: {str(e)}")
    
    # Default to binary
    return 'application/octet-stream'

def is_image_type(mime_type: str) -> bool:
    """Check if MIME type is an image type.
    
    Args:
        mime_type: MIME type string
        
    Returns:
        True if image type, False otherwise
    """
    return mime_type.startswith('image/')

def is_audio_type(mime_type: str) -> bool:
    """Check if MIME type is an audio type.
    
    Args:
        mime_type: MIME type string
        
    Returns:
        True if audio type, False otherwise
    """
    return mime_type.startswith('audio/')

def is_document_type(mime_type: str) -> bool:
    """Check if MIME type is a document type.
    
    Args:
        mime_type: MIME type string
        
    Returns:
        True if document type, False otherwise
    """
    return (mime_type.startswith('application/') or 
            mime_type.startswith('text/') or
            mime_type == 'application/pdf')

def encode_binary_to_base64(binary_data: bytes, mime_type: str = None) -> str:
    """Encode binary data as base64 string.
    
    Args:
        binary_data: Binary data to encode
        mime_type: Optional MIME type to include in data URL
        
    Returns:
        Base64 encoded string
    """
    encoded = base64.b64encode(binary_data).decode('utf-8')
    if mime_type:
        return f"data:{mime_type};base64,{encoded}"
    return encoded

def decode_base64_to_binary(base64_data: str) -> bytes:
    """Decode base64 string to binary data.
    
    Args:
        base64_data: Base64 encoded string
        
    Returns:
        Binary data
    """
    # If it's a data URL, extract the base64 part
    if base64_data.startswith('data:'):
        base64_data = base64_data.split(',')[1]
    
    # Remove any non-base64 characters
    base64_data = re.sub(r'[^A-Za-z0-9+/=]', '', base64_data)
    
    # Decode
    return base64.b64decode(base64_data)

def get_binary_from_url(url: str) -> Tuple[bytes, str]:
    """Download binary content from URL.
    
    Args:
        url: URL to download
        
    Returns:
        Tuple of (binary_data, mime_type)
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', 'application/octet-stream').split(';')[0]
        return response.content, content_type
    except Exception as e:
        logger.error(f"Error downloading content from {url}: {str(e)}")
        raise

def prepare_for_db_storage(content_type: str, content: Union[str, bytes]) -> Dict[str, Any]:
    """Prepare multimodal content for database storage.
    
    Args:
        content_type: Type of content ('image', 'audio', 'document')
        content: Content as URL or binary data
        
    Returns:
        Dictionary for database storage
    """
    result = {
        "type": content_type,
        "timestamp": None,  # Will be set by DB
    }
    
    # Handle URL vs binary content
    if isinstance(content, str) and content.startswith(('http://', 'https://')):
        result["url"] = content
        result["mime_type"] = detect_content_type(content)
    elif isinstance(content, str) and content.startswith('data:'):
        # It's a base64 data URL
        mime_match = re.match(r'data:([^;]+);base64,', content)
        if mime_match:
            result["mime_type"] = mime_match.group(1)
        else:
            result["mime_type"] = "application/octet-stream"
        result["base64_data"] = content
    elif isinstance(content, bytes):
        # It's binary data
        result["mime_type"] = detect_content_type(content[:100])
        result["base64_data"] = encode_binary_to_base64(content, result["mime_type"])
    
    return result

def extract_from_context(context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract multimodal content from context dictionary.
    
    Args:
        context: Context dictionary
        
    Returns:
        List of multimodal content dictionaries
    """
    result = []
    
    # Extract from multimodal_content if it exists
    if "multimodal_content" in context:
        mc = context["multimodal_content"]
        
        # Handle image content
        if "image_url" in mc:
            result.append(prepare_for_db_storage("image", mc["image_url"]))
        if "image_data" in mc and mc["image_data"]:
            result.append(prepare_for_db_storage("image", mc["image_data"]))
            
        # Handle audio content
        if "audio_url" in mc:
            result.append(prepare_for_db_storage("audio", mc["audio_url"]))
        if "audio_data" in mc and mc["audio_data"]:
            result.append(prepare_for_db_storage("audio", mc["audio_data"]))
            
        # Handle document content
        if "document_url" in mc:
            result.append(prepare_for_db_storage("document", mc["document_url"]))
        if "document_data" in mc and mc["document_data"]:
            result.append(prepare_for_db_storage("document", mc["document_data"]))
    
    # Handle legacy single media fields
    elif "media_url" in context and "mime_type" in context:
        mime_type = context["mime_type"]
        if is_image_type(mime_type):
            result.append(prepare_for_db_storage("image", context["media_url"]))
        elif is_audio_type(mime_type):
            result.append(prepare_for_db_storage("audio", context["media_url"]))
        elif is_document_type(mime_type):
            result.append(prepare_for_db_storage("document", context["media_url"]))
    
    return result 
```

# src/version.py

```py
"""Service version and metadata information."""

__version__ = "0.1.3"

SERVICE_NAME = "automagik-agents"
SERVICE_DESCRIPTION = "Automagik agents templates and API"

# Service information dictionary for reuse
SERVICE_INFO = {
    "name": SERVICE_NAME,
    "description": SERVICE_DESCRIPTION,
    "version": __version__,
}

```

