#!/usr/bin/env python3
"""
Interactive CLI chat application for testing Automagik Agents.

This script provides an interactive command-line interface to:
1. Create or choose a user
2. Choose an agent from the available agents
3. Chat with the selected agent

Usage:
    python playground/interactive_agent_chat.py [--debug] [--api-url=URL] [--api-key=KEY]

Options:
    --debug     Show detailed debug information including prompts and tool usage
    --api-url   Specify the base URL for the API (default: from .env)
    --api-key   Specify the API key for authentication (default: from .env)

API Endpoints:
    The API uses the following endpoint structure:
    - Agent Run:      /api/v1/agent/{agent_name}/run
    - List Agents:    /api/v1/agent/list
    - Get Session:    /api/v1/session/{session_id}
    - List Sessions:  /api/v1/sessions
    - Delete Session: /api/v1/session/{session_id} (DELETE)
    
    Some deployments may prefix these with /api or /api/v1
"""

import logging
import sys
import argparse
import uuid
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import os
import asyncio
from pprint import pformat
import time
import requests
import io
from contextlib import redirect_stdout, redirect_stderr
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich import box
from rich.console import RenderableType

# Process command-line args to detect headless mode early
def pre_parse_args():
    for arg in sys.argv:
        if arg == '--headless':
            return True
    return False

IS_HEADLESS = pre_parse_args()

# Capture stdout during imports if in headless mode
if IS_HEADLESS:
    # Capture all standard output and error during initialization
    devnull = io.StringIO()
    with redirect_stdout(devnull), redirect_stderr(devnull):
        # Load environment variables from .env file in the root directory
        from dotenv import load_dotenv
        # Load .env from the root directory (relative to this script)
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        if os.path.exists(env_path):
            load_dotenv(dotenv_path=env_path)

        # Configure minimal logging in headless mode
        logging.basicConfig(level=logging.ERROR)
        
        # Silence other loggers
        for logger_name in logging.root.manager.loggerDict:
            logging.getLogger(logger_name).setLevel(logging.ERROR)
            
        # Import logging module with reduced verbosity
        try:
            from src.utils.logging import configure_logging
            # Don't call configure_logging() in headless mode
        except ImportError:
            pass
else:
    # Normal imports for interactive mode
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    print(f"Looking for .env file at: {env_path}")
    if os.path.exists(env_path):
        print(f".env file found at: {env_path}")
        load_dotenv(dotenv_path=env_path)
        print("Environment variables loaded from .env file")
    else:
        print(f"Warning: .env file not found at {env_path}")

    # Configure logging
    from src.utils.logging import configure_logging
    configure_logging()

# Common logger setup regardless of mode
logger = logging.getLogger("interactive_agent_chat")

# Create a rich console for pretty output
console = Console()

# In headless mode, suppress most of the initialization messages
args = None  # Will be set in main()
def is_headless():
    return IS_HEADLESS or (args and args.headless)

# Only print if not in headless mode or if in debug mode
def conditional_print(message):
    if not is_headless() or (args and args.debug):
        print(message)

conditional_print(f"Looking for .env file at: {env_path}")
if os.path.exists(env_path):
    conditional_print(f".env file found at: {env_path}")
    load_dotenv(dotenv_path=env_path)
    conditional_print("Environment variables loaded from .env file")
else:
    conditional_print(f"Warning: .env file not found at {env_path}")

# Global debug flag - can be overridden by command line args
DEBUG_MODE = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")

# Get environment variables with better debugging
def get_env_var(name, default=None, secret=False):
    """Get an environment variable with debug output."""
    value = os.environ.get(name, default)
    if not is_headless():
        if value == default:
            conditional_print(f"Environment variable {name} not found, using default: {'' if secret else default}")
        else:
            conditional_print(f"Environment variable {name} found: {'' if secret else value}")
    return value

# Global variables - Build API URL from AM_* settings if available
AM_HOST = get_env_var("AM_HOST", "localhost")
AM_PORT = get_env_var("AM_PORT", "8000")
AM_ENV = get_env_var("AM_ENV", "development")

# Construct API_BASE_URL from AM_* variables if they exist
if AM_HOST and AM_PORT:
    constructed_url = f"http://{AM_HOST}:{AM_PORT}"
    conditional_print(f"Constructed API URL from AM_HOST and AM_PORT: {constructed_url}")
    API_BASE_URL = constructed_url
else:
    API_BASE_URL = get_env_var("API_BASE_URL", "http://localhost:8000")

# Ensure API_BASE_URL doesn't end with a slash
if API_BASE_URL.endswith("/"):
    API_BASE_URL = API_BASE_URL[:-1]
    if not is_headless():
        console.print(f"[yellow]Removed trailing slash from API_BASE_URL: {API_BASE_URL}[/yellow]")

# Try to find the API key from various possible environment variables
API_KEY = (
    get_env_var("AM_API_KEY", None, secret=True) or 
    get_env_var("API_KEY", None, secret=True) or 
    get_env_var("OPENAI_API_KEY", None, secret=True)
)

if API_KEY and not is_headless():
    # Store the original key for reference
    os.environ["ORIGINAL_API_KEY"] = API_KEY
    conditional_print(f"Using API key from environment (length: {len(API_KEY)})")
    
    # If key looks like a JWT, extract just the token portion
    if API_KEY.count('.') == 2 and "eyJ" in API_KEY:
        conditional_print("API key appears to be a JWT token")
    
    # If key has a sk- prefix (OpenAI), warn that this might not be right
    if API_KEY.startswith("sk-"):
        conditional_print("Warning: API key has OpenAI format (sk-), this may not be correct for Automagik API")
elif not is_headless():
    conditional_print("No API key found in environment variables")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Interactive CLI for Automagik Agents")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--api-url", type=str, help="Override API URL")
    parser.add_argument("--api-key", type=str, help="Override API key")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode (non-interactive)")
    parser.add_argument("--agent", type=str, help="Agent to use in headless mode")
    parser.add_argument("--user", type=int, help="User ID to use in headless mode")
    parser.add_argument("--session", type=str, help="Session ID to use in headless mode")
    parser.add_argument("--session-name", type=str, help="Friendly name for the session in headless mode")
    parser.add_argument("--message", type=str, help="Message to send in headless mode (if not provided, will read from stdin)")
    return parser.parse_args()

def ensure_protocol(url: str) -> str:
    """Ensure the URL has a protocol (default to http if none)."""
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"
        console.print(f"[yellow]Added http:// protocol to URL: {url}[/yellow]")
    return url

def get_api_endpoint(path: str) -> str:
    """Build a consistent API endpoint URL with the correct prefix.
    
    Args:
        path: The API path (without leading slash)
        
    Returns:
        str: The full API endpoint URL
    """
    # Ensure the path doesn't start with a slash
    if path.startswith("/"):
        path = path[1:]
    
    # Always use /api/v1/ prefix
    if not path.startswith("api/v1/"):
        path = f"api/v1/{path}"
    
    # Build the full URL
    url = f"{API_BASE_URL}/{path}"
    
    return url

def get_available_agents() -> List[Dict[str, Any]]:
    """Get a list of available agents using the API.
    
    Returns:
        List[Dict[str, Any]]: List of agent dictionaries
    """
    try:
        # Define the API endpoint for listing agents
        endpoint = get_api_endpoint("agent/list")
        if DEBUG_MODE:
            console.print(f"[dim]Getting agents from: {endpoint}[/dim]")
        
        # Prepare headers with API key if available
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        # Make the API request
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            agents = response.json()
            if not is_headless():
                console.print(f"[green]Successfully retrieved {len(agents)} agents[/green]")
            
            # Convert the API response to a format compatible with the rest of the code
            for agent in agents:
                # Ensure id field is present (use name as fallback)
                if "id" not in agent:
                    agent["id"] = agent["name"]
                
                # If description is missing, provide a default
                if "description" not in agent:
                    agent["description"] = f"Agent of type {agent.get('type', 'unknown')}"
                
                # If model is missing, provide a default
                if "model" not in agent:
                    agent["model"] = "unknown"
            
            return agents
        else:
            console.print(f"[bold red]Error getting agents: HTTP {response.status_code}[/bold red]")
            if DEBUG_MODE:
                console.print(f"[red]Response: {response.text}[/red]")
            return []
    except Exception as e:
        console.print(f"[bold red]Error getting agents from API: {str(e)}[/bold red]")
        return []

def select_user() -> Optional[Dict[str, Any]]:
    """Display UI for selecting or creating a user.
    
    Returns:
        Optional[Dict[str, Any]]: The selected user, or None if cancelled
    """
    console.print("\n[bold]👤 User Selection[/bold]")
    
    try:
        # Get users from API
        endpoint = get_api_endpoint("users")
        console.print(f"[dim]Getting users from: {endpoint}[/dim]")
        
        # Prepare headers with API key if available
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        # Make the API request
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            users_response = response.json()
            users = users_response.get("users", [])
            console.print(f"[green]Successfully retrieved {len(users)} users from API[/green]")
            
            # Display users if any
            if users:
                console.print("\n[bold]Available Users:[/bold]")
                table = Table(show_header=True, header_style="bold")
                table.add_column("ID", style="dim")
                table.add_column("Email")
                table.add_column("Name")
                table.add_column("Created")
                
                for user in users:
                    created_str = user.get("created_at", "Unknown")
                    if isinstance(created_str, str) and len(created_str) > 10:
                        created_str = created_str[:10]  # Truncate to just the date
                    
                    table.add_row(
                        str(user["id"]),
                        user["email"],
                        user.get("name", ""),
                        created_str
                    )
                
                console.print(table)
                
                # Ask if the user wants to create a new user or select existing
                create_new = Confirm.ask("Create a new user?", default=False)
                
                if not create_new:
                    # Select an existing user
                    existing_choices = [str(user["id"]) for user in users]
                    user_id = Prompt.ask(
                        "Enter user ID to select",
                        choices=existing_choices,
                        default=existing_choices[0] if existing_choices else None
                    )
                    
                    # Find and return the selected user
                    selected_user = next((user for user in users if str(user["id"]) == user_id), None)
                    if selected_user:
                        console.print(f"[bold green]Selected user: {selected_user['email']}[/bold green]")
                        return selected_user
            else:
                console.print("[yellow]No users found. Please create a new user.[/yellow]")
        else:
            console.print(f"[bold red]Error getting users: HTTP {response.status_code}[/bold red]")
            console.print(f"[red]Response: {response.text}[/red]")
            console.print("[yellow]Will create a new user instead.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Error getting users from API: {str(e)}[/bold red]")
        console.print("[yellow]Will create a new user instead.[/yellow]")
    
    # Create a new user via API
    email = Prompt.ask("Enter email for new user")
    name = Prompt.ask("Enter name for user", default=email.split("@")[0])
    
    try:
        # Prepare the payload for creating a user
        payload = {
            "email": email,
            "name": name
        }
        
        # Create the user via API
        endpoint = get_api_endpoint("users")
        console.print(f"[dim]Creating user at: {endpoint}[/dim]")
        
        # Prepare headers with API key if available
        headers = {
            "Content-Type": "application/json"
        }
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        # Make the API request
        response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            new_user = response.json()
            console.print(f"[bold green]Created new user: {new_user['email']} (ID: {new_user['id']})[/bold green]")
            return new_user
        else:
            console.print(f"[bold red]Error creating user: HTTP {response.status_code}[/bold red]")
            console.print(f"[red]Response: {response.text}[/red]")
            
            # If we couldn't create the user via API, create a local user as fallback
            return create_local_user(email, name)
    except Exception as e:
        console.print(f"[bold red]Error creating user via API: {str(e)}[/bold red]")
        
        # If we couldn't create the user via API, create a local user as fallback
        return create_local_user(email, name)


def create_local_user(email: str, name: str = None) -> Dict[str, Any]:
    """Create a local user as fallback when API is not available.
    
    Args:
        email: Email address for the new user
        name: Name for the new user (optional)
        
    Returns:
        Dict[str, Any]: The created user
    """
    console.print("[yellow]Creating local user as fallback...[/yellow]")
    
    # For local users, we use a simple file-based approach
    local_users = []
    user_file = os.path.join(os.path.dirname(__file__), 'chat_users.json')
    
    try:
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                local_users = json.load(f)
    except Exception as e:
        console.print(f"[yellow]Could not load local users file: {str(e)}[/yellow]")
    
    # Create a unique ID
    new_id = int(time.time()) % 10000 + 1000
    
    # Check if ID is already used
    while any(user["id"] == new_id for user in local_users):
        new_id += 1
    
    # Create the new user object
    now = datetime.utcnow().isoformat()
    new_user = {
        "id": new_id,
        "email": email,
        "name": name or email.split("@")[0],
        "created_at": now,
        "updated_at": now
    }
    
    # Add to local users list
    local_users.append(new_user)
    
    # Save to file
    try:
        with open(user_file, 'w') as f:
            json.dump(local_users, f, indent=2)
        console.print("[green]User saved to local storage[/green]")
    except Exception as e:
        console.print(f"[yellow]Could not save user to file: {str(e)}[/yellow]")
    
    console.print(f"[bold green]Created new local user: {email} (ID: {new_id})[/bold green]")
    return new_user


def display_users(users: List[Dict[str, Any]]) -> None:
    """Display a table of users.
    
    Args:
        users: List of user dictionaries
    """
    if not users:
        console.print("[yellow]No users found in database[/yellow]")
        return
    
    table = Table(title="Available Users")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Email", style="green")
    table.add_column("Details", style="yellow")
    
    for user in users:
        user_data = user.get("user_data", {})
        if isinstance(user_data, str):
            try:
                user_data = json.loads(user_data)
            except:
                user_data = {}
        
        details = ", ".join([f"{k}: {v}" for k, v in user_data.items()]) if user_data else ""
        table.add_row(str(user["id"]), user["email"], details[:50])
    
    console.print(table)


def display_agents(agents: List[Dict[str, Any]]) -> None:
    """Display a table of agents.
    
    Args:
        agents: List of agent dictionaries
    """
    if not agents:
        console.print("[yellow]No agents available[/yellow]")
        return
    
    console.print("\n[bold]Available Agents:[/bold]")
    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="dim")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Model", style="dim")
    
    for agent in agents:
        table.add_row(
            str(agent["id"]) if "id" in agent else "N/A",
            agent["name"],
            agent.get("type", "Unknown"),
            agent.get("model", "Unknown")
        )
    
    console.print(table)


def select_agent(agents: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Display UI for selecting an agent.
    
    Args:
        agents: List of agent dictionaries
    
    Returns:
        Optional[Dict[str, Any]]: The selected agent, or None if cancelled
    """
    console.print("\n[bold]🤖 Agent Selection[/bold]")
    
    display_agents(agents)
    
    if not agents:
        console.print("[bold red]No agents available. Please create an agent first.[/bold red]")
        return None
    
    agent_id = Prompt.ask(
        "Enter agent ID to select",
        choices=[str(agent["id"]) for agent in agents],
        default=str(agents[0]["id"])
    )
    
    selected_agent = next((agent for agent in agents if str(agent["id"]) == agent_id), None)
    if selected_agent:
        console.print(f"[bold green]Selected agent: {selected_agent['name']} (ID: {selected_agent['id']})[/bold green]")
    
    return selected_agent


# Add a mapping to store session names to IDs
SESSION_NAME_TO_ID = {}
SESSION_ID_TO_NAME = {}

# Path to store session mapping
def get_sessions_file_path():
    """Get the path to the sessions mapping file."""
    return os.path.join(os.path.dirname(__file__), 'chat_sessions.json')

def load_session_mappings():
    """Load session mappings from file."""
    global SESSION_NAME_TO_ID, SESSION_ID_TO_NAME
    sessions_file = get_sessions_file_path()
    
    try:
        if os.path.exists(sessions_file):
            with open(sessions_file, 'r') as f:
                data = json.load(f)
                SESSION_NAME_TO_ID = data.get("name_to_id", {})
                SESSION_ID_TO_NAME = data.get("id_to_name", {})
                if DEBUG_MODE:
                    print(f"Loaded {len(SESSION_NAME_TO_ID)} session mappings from {sessions_file}")
                    if SESSION_NAME_TO_ID:
                        print(f"Available sessions: {', '.join(SESSION_NAME_TO_ID.keys())}")
        elif DEBUG_MODE:
            print(f"Session mappings file not found at {sessions_file}")
    except Exception as e:
        if DEBUG_MODE:
            print(f"Error loading session mappings from {sessions_file}: {str(e)}")
        # Initialize empty mappings if file doesn't exist or is invalid
        SESSION_NAME_TO_ID = {}
        SESSION_ID_TO_NAME = {}

def save_session_mappings():
    """Save session mappings to file."""
    sessions_file = get_sessions_file_path()
    data = {
        "name_to_id": SESSION_NAME_TO_ID,
        "id_to_name": SESSION_ID_TO_NAME
    }
    
    try:
        with open(sessions_file, 'w') as f:
            json.dump(data, f, indent=2)
        if DEBUG_MODE:
            print(f"Saved {len(SESSION_NAME_TO_ID)} session mappings to {sessions_file}")
            if SESSION_NAME_TO_ID:
                print(f"Saved sessions: {', '.join(SESSION_NAME_TO_ID.keys())}")
    except Exception as e:
        if DEBUG_MODE:
            print(f"Error saving session mappings to {sessions_file}: {str(e)}")

def get_session_id_from_name(session_name):
    """Get a session ID from a name, or None if not found."""
    # First, ensure mappings are loaded
    if not SESSION_NAME_TO_ID:
        load_session_mappings()
    
    return SESSION_NAME_TO_ID.get(session_name)

async def run_agent(agent_name: str, input_message: str, session_id: str = None, user_id: int = 1, session_name: str = None) -> dict:
    """Run the agent with the given message using the API.
    
    Args:
        agent_name: Name of the agent to run
        input_message: Message to send to the agent
        session_id: Session ID for the conversation (can be None if session_name is provided)
        user_id: User ID for the conversation (defaults to 1 if not provided)
        session_name: Optional friendly name for the session
    
    Returns:
        dict: The agent response
    """
    try:
        # Define the API endpoint with the correct prefix
        endpoint = get_api_endpoint(f"agent/{agent_name}/run")
        
        # Only show endpoint in debug mode
        if DEBUG_MODE:
            console.print(f"[dim]Using endpoint: {endpoint}[/dim]")
        
        # Prepare the payload according to the API's expected format
        payload = {
            "message_content": input_message,
            "user_id": user_id,
            "context": {"debug": DEBUG_MODE},
            "session_origin": "cli"
        }
        
        # Add session_id if provided
        if session_id:
            payload["session_id"] = session_id
            
        # Add session_name to context if provided
        if session_name:
            payload["context"]["session_name"] = session_name
            # Always include session_name at the top level - not just when session_id is missing
            payload["session_name"] = session_name
        
        if DEBUG_MODE:
            console.print(f"[dim]Request payload: {json.dumps(payload, indent=2)}[/dim]")
        
        # Prepare headers with API key
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add API key to headers if available
        if API_KEY:
            headers["x-api-key"] = API_KEY
            
            if DEBUG_MODE:
                masked_key = f"{API_KEY[:4]}...{API_KEY[-4:]}" if len(API_KEY) > 8 else "****"
                console.print(f"[dim]Using API key: {masked_key}[/dim]")
        
        # Make the API request
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        
        # Check response status
        if response.status_code == 200:
            result = response.json()
            if DEBUG_MODE:
                console.print(f"[dim]API Response: {json.dumps(result, indent=2)}[/dim]")
            return result
        else:
            error_msg = f"API Error: Status {response.status_code}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg = f"API Error: {error_data['detail']}"
            except Exception:
                error_msg = f"API Error: {response.text}"
            
            console.print(f"[bold red]{error_msg}[/bold red]")
            return {"error": error_msg}
                
    except Exception as e:
        error_msg = f"Error running agent: {str(e)}"
        console.print(f"[bold red]{error_msg}[/bold red]")
        return {"error": error_msg}


def display_message(message: str, role: str, tool_calls: List = None, tool_outputs: List = None) -> None:
    """Display a message with proper formatting based on role.
    
    Args:
        message: The message content
        role: The role (user, assistant, system)
        tool_calls: Optional list of tool calls
        tool_outputs: Optional list of tool outputs
    """
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
                console.print(Panel(
                    "\n".join(tool_panel_content),
                    border_style="dim blue",
                    padding=(0, 1),
                    expand=False,
                    width=message_width
                ), justify="right")  # Changed from left to right
        
        # Try to render markdown with improved formatting
        try:
            # Prepare the message content for improved markdown rendering
            # First clean up the message to ensure proper rendering
            message_cleaned = message.strip()
            
            # Create Markdown object with better styling options
            md = Markdown(
                message_cleaned,
                code_theme="monokai",
                justify="left",  # Keep internal content left-aligned within the panel
                inline_code_lexer="python",
                hyperlinks=True
            )
            
            # Render the markdown content in a panel
            console.print(Panel(
                md,
                box=box.ROUNDED,
                border_style="blue",
                padding=(0, 1),
                expand=False,
                width=message_width
            ), justify="right")  # Changed from left to right
        except Exception as e:
            if DEBUG_MODE:
                console.print(f"[dim]Markdown rendering error: {str(e)}[/dim]")
            # Fallback to plain text if markdown rendering fails
            console.print(Panel(
                message,
                box=box.ROUNDED,
                border_style="blue",
                padding=(0, 1),
                expand=False,
                width=message_width
            ), justify="right")  # Changed from left to right
        
        # Only show detailed JSON debug info if explicitly in DEBUG_MODE
        if DEBUG_MODE and tool_calls:
            for i, tool_call in enumerate(tool_calls):
                console.print(Panel(
                    Syntax(json.dumps(tool_call, indent=2), "json", theme="monokai"),
                    title=f"Tool Call #{i+1}",
                    title_align="left",
                    border_style="yellow",
                    expand=False
                ), justify="right")  # Changed from default to right
                
                # Find matching output if available
                if tool_outputs:
                    matching_output = next(
                        (output for output in tool_outputs if output.get("tool_call_id") == tool_call.get("tool_call_id")),
                        None
                    )
                    if matching_output:
                        console.print(Panel(
                            Syntax(json.dumps(matching_output, indent=2), "json", theme="monokai"),
                            title=f"Tool Output #{i+1}",
                            title_align="left",
                            border_style="cyan",
                            expand=False
                        ), justify="right")  # Changed from default to right
    
    elif role == "system":
        # Make system messages subtle and compact
        console.print(Panel(
            message,
            border_style="dim red",
            padding=(0, 1),
            expand=False
        ))


async def chat_loop(user: Dict[str, Any], agent: Dict[str, Any], session_id: str, session_name: Optional[str] = None) -> None:
    """Main chat loop for interacting with the agent.
    
    Args:
        user: The user dictionary
        agent: The agent dictionary
        session_id: The session ID for the conversation
        session_name: Optional friendly name for the session
    """
    # Show minimal session info
    console.print()
    if not args.headless:
        if session_name:
            console.print(f"[dim]Session: {session_name} (ID: {session_id}) | Agent: {agent['name']}[/dim]")
        else:
            console.print(f"[dim]Session: {session_id} | Agent: {agent['name']}[/dim]")
        console.print("[dim]Type 'exit' or 'quit' to end the chat session.[/dim]\n")
    
    # Display minimal welcome message
    display_message(
        f"Hello! I'm {agent['name']}. How can I help you today?",
        "assistant"
    )
    
    # Flag to track if we're currently processing a message
    is_processing = False
    
    # Main chat loop
    while True:
        # Only show input prompt when not processing
        if not is_processing:
            try:
                # Simple left-aligned green prompt
                console.print()
                console.print("[green bold]>[/green bold] ", end="")
                
                # Get user input with left alignment (default)
                user_input = input()  # No extra space needed
                
                # Handle empty input
                if not user_input.strip():
                    continue
                
                # Check for exit command
                if user_input.lower() in ["exit", "quit", "bye"]:
                    if not args.headless:
                        console.print("\n[dim]Chat session ended.[/dim]")
                    break
                
                # No need to display user message again - it's already shown by the terminal's echo
                # after the green prompt
                
                # Set processing flag to prevent further input
                is_processing = True
                
                # Run the agent with a minimal status indicator
                try:
                    with console.status("[dim]Thinking...[/dim]", spinner="dots"):
                        response = await run_agent(agent['name'], user_input, session_id, user['id'], session_name)
                
                except KeyboardInterrupt:
                    console.print("\n[dim]Request cancelled.[/dim]")
                    is_processing = False
                    continue
                
                if "error" in response and response["error"]:
                    display_message(f"Error: {response['error']}", "system")
                    is_processing = False
                    continue
                
                # Extract response parts based on the API format
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
                
                # Reset processing flag
                is_processing = False
            
            except Exception as e:
                # Handle any other errors
                console.print(f"[red]Error: {str(e)}[/red]")
                is_processing = False


def test_api_connection() -> bool:
    """Test connectivity to the API.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    # Try the main API endpoints in order of importance
    endpoints_to_try = [
        "agent/list",  # Most important - needs to work
        "health",
        "users"
    ]
    
    for endpoint in endpoints_to_try:
        try:
            url = get_api_endpoint(endpoint)
            console.print(f"[dim]Testing API connection at {url}...[/dim]")
            
            headers = {}
            if API_KEY and endpoint in ["agent/list", "users"]:
                headers["x-api-key"] = API_KEY
            
            with console.status(f"[bold green]Testing API connection at {endpoint}...") as status:
                # Try to connect to the API
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code < 400:  # Any successful or redirect status code
                    console.print(f"[bold green]✅ Connected to API at {url}: Status {response.status_code}[/bold green]")
                    
                    # For agent list endpoint, verify we got a valid response
                    if endpoint == "agent/list":
                        try:
                            agents = response.json()
                            if isinstance(agents, list):
                                console.print(f"[bold green]✅ Agent list API works! Found {len(agents)} agents[/bold green]")
                                return True
                            else:
                                console.print(f"[yellow]Agent list API responded but returned unexpected data format[/yellow]")
                        except Exception as e:
                            console.print(f"[yellow]Agent list API responded but returned invalid JSON: {str(e)}[/yellow]")
                    else:
                        return True
                else:
                    console.print(f"[yellow]API at {url} responded with status code: {response.status_code}[/yellow]")
                    
                    # If this is the agent list endpoint and got a 401, it's probably an auth issue
                    if endpoint == "agent/list" and response.status_code == 401:
                        console.print(f"[bold red]❌ Authentication failed - your API key may be invalid[/bold red]")
        except requests.exceptions.ConnectionError:
            console.print(f"[yellow]Could not connect to API at {url}[/yellow]")
        except Exception as e:
            console.print(f"[yellow]Error testing API at {url}: {str(e)}[/yellow]")
    
    # If we get here, none of the endpoints worked
    console.print(f"[bold red]❌ Could not connect to API at {API_BASE_URL}[/bold red]")
    console.print("[yellow]Tips:[/yellow]")
    console.print("1. Check if the API server is running")
    console.print("2. Make sure the API URL is correct (includes http:// or https://)")
    console.print("3. Check if there are firewall or network issues")
    console.print(f"4. Try accessing the API in a browser: {API_BASE_URL}")
    console.print("5. Try manually setting the API URL with --api-url parameter")
    return False


async def create_session(user_id: int, agent_name: str, session_name: str = None) -> Optional[str]:
    """Create a new session via API.
    
    Args:
        user_id: User ID for the session
        agent_name: Name of the agent for the session
        session_name: Optional friendly name for the session
    
    Returns:
        Optional[str]: The created session ID or None if creation failed
    """
    # If a session_name is provided, check if it already exists
    if session_name:
        # Load existing mappings
        load_session_mappings()
        
        # Check if this name already exists
        if session_name in SESSION_NAME_TO_ID:
            existing_id = SESSION_NAME_TO_ID[session_name]
            if not is_headless():
                console.print(f"[yellow]Session name '{session_name}' already exists (ID: {existing_id})[/yellow]")
                console.print(f"[yellow]Using the existing session instead of creating a new one.[/yellow]")
            else:
                print(f"Using existing session: {session_name} (ID: {existing_id})")
            return existing_id
    
    # Generate a unique session ID as UUID string WITH hyphens (don't remove them)
    session_id = str(uuid.uuid4())
    
    # If a session_name is provided, associate it with this session ID
    if session_name:
        # Store the mapping
        SESSION_NAME_TO_ID[session_name] = session_id
        SESSION_ID_TO_NAME[session_id] = session_name
        
        # Save the updated mappings
        save_session_mappings()
        
        if DEBUG_MODE or not is_headless():
            if not is_headless():
                console.print(f"[dim]Created session '{session_name}' with ID: {session_id}[/dim]")
            else:
                print(f"Created session '{session_name}' with ID: {session_id}")
    elif DEBUG_MODE or not is_headless():
        if not is_headless():
            console.print(f"[dim]Generated new session ID: {session_id}[/dim]")
        else:
            print(f"Generated new session ID: {session_id}")
    
    # We don't need to explicitly create the session via API as it will be created
    # automatically on the first agent run with this session ID
    
    if not is_headless():
        if session_name:
            console.print(f"[green]New chat session ready: {session_name} (ID: {session_id})[/green]")
        else:
            console.print(f"[green]New chat session ready: {session_id}[/green]")
    elif DEBUG_MODE:
        if session_name:
            print(f"New chat session ready: {session_name} (ID: {session_id})")
        else:
            print(f"New chat session ready: {session_id}")
    
    return session_id


async def chat_init() -> Tuple[Dict[str, Any], Dict[str, Any], str, Optional[str]]:
    """Initialize a chat session by selecting a user, agent, and creating a session.
    
    Returns:
        Tuple[Dict[str, Any], Dict[str, Any], str, Optional[str]]: 
            Selected user, agent, session ID, and optional session name
    """
    # Step 1: Select or create a user
    user = select_user()
    if not user:
        console.print("[bold red]No user selected. Exiting...[/bold red]")
        sys.exit(1)
    
    # Step 2: Select an agent
    agents = get_available_agents()
    agent = select_agent(agents)
    if not agent:
        console.print("[bold red]No agent selected. Exiting...[/bold red]")
        sys.exit(1)
    
    # Step 3: Ask for an optional session name
    session_name = None
    if Confirm.ask("Would you like to name this session?", default=False):
        session_name = Prompt.ask("Enter a name for this session", default=f"{agent['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    # Step 4: Create a new session (always create a new session on app start)
    session_id = await create_session(user["id"], agent["name"], session_name)
    if not session_id:
        console.print("[bold red]Failed to create chat session. Exiting...[/bold red]")
        sys.exit(1)
    
    return user, agent, session_id, session_name


async def get_session_history(session_id_or_name: str, page: int = 1, page_size: int = 50) -> Optional[Dict[str, Any]]:
    """Get session history via API.
    
    Args:
        session_id_or_name: The session ID or name
        page: Page number (1-based)
        page_size: Number of messages per page
        
    Returns:
        Optional[Dict[str, Any]]: Session history or None if retrieval failed
    """
    try:
        # Check if this is a session name rather than an ID
        session_id = session_id_or_name
        is_name = False
        
        # UUID format usually has 4 hyphens and is at least 36 characters long
        if not (session_id_or_name.count('-') == 4 and len(session_id_or_name) >= 36):
            is_name = True
            # Look up the session ID from the name
            session_id = get_session_id_from_name(session_id_or_name)
            if not session_id:
                if not is_headless():
                    console.print(f"[yellow]Session name '{session_id_or_name}' not found[/yellow]")
                else:
                    print(f"Error: Session name '{session_id_or_name}' not found", file=sys.stderr)
                return None
            
            if DEBUG_MODE:
                if not is_headless():
                    console.print(f"[dim]Found session ID {session_id} for name '{session_id_or_name}'[/dim]")
                else:
                    print(f"Found session ID {session_id} for name '{session_id_or_name}'")
        
        # Define the API endpoint
        endpoint = get_api_endpoint(f"session/{session_id}")
        if not is_headless():
            console.print(f"[dim]Getting session history from: {endpoint}[/dim]")
        elif DEBUG_MODE:
            print(f"Getting session history from: {endpoint}")
        
        # Add query parameters
        params = {
            "page": page,
            "page_size": page_size,
            "sort_desc": True  # Most recent messages first
        }
        
        # Prepare headers with API key if available
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        # Make the API request
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            session_data = response.json()
            
            # If we used a session name to look up, add/update the name in the response
            if is_name and session_data and "metadata" in session_data:
                if not isinstance(session_data["metadata"], dict):
                    session_data["metadata"] = {}
                
                # Store the session name in metadata
                session_data["metadata"]["session_name"] = session_id_or_name
                
                # Also store at top level for convenience
                session_data["session_name"] = session_id_or_name
            
            return session_data
        else:
            error_msg = f"Error getting session history: HTTP {response.status_code}"
            if not is_headless():
                console.print(f"[bold red]{error_msg}[/bold red]")
                if DEBUG_MODE:
                    console.print(f"[red]Response: {response.text}[/red]")
            else:
                print(error_msg, file=sys.stderr)
                if DEBUG_MODE:
                    print(f"Response: {response.text}", file=sys.stderr)
            return None
    except Exception as e:
        error_msg = f"Error getting session history: {str(e)}"
        if not is_headless():
            console.print(f"[bold red]{error_msg}[/bold red]")
        else:
            print(error_msg, file=sys.stderr)
        return None

async def delete_session(session_id_or_name: str) -> bool:
    """Delete a session via API.
    
    Args:
        session_id_or_name: The session ID or name to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        # Check if this is a session name rather than an ID
        session_id = session_id_or_name
        is_name = False
        original_name = None
        
        # UUID format usually has 4 hyphens and is at least 36 characters long
        if not (session_id_or_name.count('-') == 4 and len(session_id_or_name) >= 36):
            is_name = True
            original_name = session_id_or_name
            # Look up the session ID from the name
            session_id = get_session_id_from_name(session_id_or_name)
            if not session_id:
                if not is_headless():
                    console.print(f"[yellow]Session name '{session_id_or_name}' not found[/yellow]")
                else:
                    print(f"Error: Session name '{session_id_or_name}' not found", file=sys.stderr)
                return False
            
            if DEBUG_MODE:
                if not is_headless():
                    console.print(f"[dim]Found session ID {session_id} for name '{session_id_or_name}'[/dim]")
                else:
                    print(f"Found session ID {session_id} for name '{session_id_or_name}'")
        
        # Define the API endpoint
        endpoint = get_api_endpoint(f"session/{session_id}")
        if not is_headless():
            console.print(f"[dim]Deleting session at: {endpoint}[/dim]")
        elif DEBUG_MODE:
            print(f"Deleting session at: {endpoint}")
        
        # Prepare headers with API key if available
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        # Make the API request
        response = requests.delete(endpoint, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            # If this was a session with a name, remove from mappings
            if session_id in SESSION_ID_TO_NAME or is_name:
                name = SESSION_ID_TO_NAME.get(session_id, original_name)
                if name in SESSION_NAME_TO_ID:
                    del SESSION_NAME_TO_ID[name]
                if session_id in SESSION_ID_TO_NAME:
                    del SESSION_ID_TO_NAME[session_id]
                save_session_mappings()
                
                if not is_headless():
                    console.print(f"[bold green]✅ Session '{name}' (ID: {session_id}) deleted successfully[/bold green]")
                else:
                    print(f"Session '{name}' (ID: {session_id}) deleted successfully")
            else:
                if not is_headless():
                    console.print(f"[bold green]✅ Session {session_id} deleted successfully[/bold green]")
                else:
                    print(f"Session {session_id} deleted successfully")
            return True
        else:
            error_msg = f"Error deleting session: HTTP {response.status_code}"
            if not is_headless():
                console.print(f"[bold red]{error_msg}[/bold red]")
                console.print(f"[red]Response: {response.text}[/red]")
            else:
                print(error_msg, file=sys.stderr)
                print(f"Response: {response.text}", file=sys.stderr)
            return False
    except Exception as e:
        error_msg = f"Error deleting session: {str(e)}"
        if not is_headless():
            console.print(f"[bold red]{error_msg}[/bold red]")
        else:
            print(error_msg, file=sys.stderr)
        return False

async def list_sessions(page: int = 1, page_size: int = 50) -> Optional[Dict[str, Any]]:
    """List all sessions via API.
    
    Args:
        page: Page number (1-based)
        page_size: Number of sessions per page
        
    Returns:
        Optional[Dict[str, Any]]: Session list response or None if retrieval failed
    """
    try:
        # Define the API endpoint
        endpoint = get_api_endpoint("sessions")
        console.print(f"[dim]Listing sessions from: {endpoint}[/dim]")
        
        # Add query parameters
        params = {
            "page": page,
            "page_size": page_size,
            "sort_desc": True  # Most recent sessions first
        }
        
        # Prepare headers with API key if available
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        # Make the API request
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            sessions_data = response.json()
            return sessions_data
        else:
            console.print(f"[bold red]Error listing sessions: HTTP {response.status_code}[/bold red]")
            console.print(f"[red]Response: {response.text}[/red]")
            return None
    except Exception as e:
        console.print(f"[bold red]Error listing sessions: {str(e)}[/bold red]")
        return None


def display_message_plain(message: str, role: str, tool_calls: List = None, tool_outputs: List = None) -> None:
    """Display a message in plain text format for headless mode.
    
    Args:
        message: The message content
        role: The role (user, assistant, system)
        tool_calls: Optional list of tool calls
        tool_outputs: Optional list of tool outputs
    """
    # Format tool usage in a simple way if present
    if role == "assistant" and tool_calls:
        tool_usage = []
        
        for i, tool_call in enumerate(tool_calls):
            tool_name = tool_call.get('tool_name', 'Unknown Tool')
            tool_args = tool_call.get('args', {})
            
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
                    (output for output in tool_outputs if output.get("tool_call_id") == tool_call.get("tool_call_id")),
                    None
                )
                if matching_output:
                    output_content = matching_output.get('content', '')
                    # Combine tool call and result
                    tool_call_str = f"{tool_call_str} → {output_content}"
            
            tool_usage.append(tool_call_str)
        
        if tool_usage:
            print("\n".join([f"[Tool] {tool}" for tool in tool_usage]))
    
    # Print the message with role prefix
    if message.strip():
        print(f"{role}: {message}")

async def get_user_by_id(user_id: int) -> Dict[str, Any]:
    """Get user data from the API by ID."""
    try:
        # Define the API endpoint
        endpoint = get_api_endpoint(f"users/{user_id}")
        if DEBUG_MODE:
            console.print(f"[dim]Getting user data from: {endpoint}[/dim]")
        
        # Prepare headers with API key if available
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        # Make the API request
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            user_data = response.json()
            if DEBUG_MODE:
                console.print(f"[green]Successfully retrieved user {user_id} from API[/green]")
            return user_data
        else:
            if DEBUG_MODE:
                console.print(f"[yellow]Error getting user by ID {user_id}: HTTP {response.status_code}[/yellow]")
                console.print(f"[yellow]Using fallback user data[/yellow]")
            # Return fallback data
            return {"id": user_id, "email": f"user{user_id}@example.com", "name": f"User {user_id}"}
    except Exception as e:
        if DEBUG_MODE:
            console.print(f"[yellow]Error getting user from API: {str(e)}[/yellow]")
            console.print(f"[yellow]Using fallback user data[/yellow]")
        # Return fallback data
        return {"id": user_id, "email": f"user{user_id}@example.com", "name": f"User {user_id}"}


async def headless_chat_once(user: Dict[str, Any], agent: Dict[str, Any], session_id: str, message: str = None, session_name: str = None) -> None:
    """Process a single message exchange in headless mode and exit.
    
    Args:
        user: The user dictionary
        agent: The agent dictionary
        session_id: The session ID for the conversation
        message: Optional message to process (if not provided, read from stdin)
        session_name: Optional friendly name for the session
    """
    # Display session info if in debug mode
    if DEBUG_MODE:
        if session_name:
            print(f"Session: {session_name} (ID: {session_id})")
        else:
            print(f"Session ID: {session_id}")
        print(f"Agent: {agent['name']}")
        print(f"User: {user['id']} ({user.get('name', 'Unknown')})")
    
    # Get the message from command line or stdin
    if not message:
        # Read message from stdin
        if sys.stdin.isatty():  # Interactive terminal
            print("Enter message: ", end="", flush=True)
        user_input = input().strip()
    else:
        user_input = message.strip()
    
    # Check if we have a message to process
    if not user_input:
        print("Error: No message provided", file=sys.stderr)
        sys.exit(1)
    
    # Display user message in plain text
    print(f"user: {user_input}")
    
    # Process the message
    try:
        response = await run_agent(agent['name'], user_input, session_id, user['id'], session_name)
        
        if "error" in response and response["error"]:
            print(f"Error: {response['error']}", file=sys.stderr)
            sys.exit(1)
        
        # Extract response parts based on the API format
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
        
        # Display assistant response in plain text
        display_message_plain(message_content, "assistant", tool_calls, tool_outputs)
        
        # If session has a name, display it for future reference
        if session_name and not DEBUG_MODE:
            print(f"\nSession '{session_name}' (ID: {session_id}) updated successfully")
        elif not DEBUG_MODE:
            print(f"\nSession ID: {session_id}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

async def main() -> None:
    """Main function."""
    global args, DEBUG_MODE, API_BASE_URL, API_KEY
    # Parse command line arguments
    args = parse_args()
    
    # Command-line args override environment variables
    if args.debug:
        DEBUG_MODE = True
    if args.api_url:
        API_BASE_URL = args.api_url
    if args.api_key:
        API_KEY = args.api_key
        os.environ["API_KEY"] = API_KEY  # Set in environment
    
    # Ensure API_BASE_URL has protocol
    API_BASE_URL = ensure_protocol(API_BASE_URL)
    
    # Check if we're in headless mode
    headless_mode = args.headless
    
    # If headless mode is enabled, ensure we have an agent specified
    if headless_mode and not args.agent:
        console.print("[bold red]Error: --agent parameter is required with --headless mode[/bold red]")
        sys.exit(1)
    
    # Skip welcome and API messages in headless mode
    if not headless_mode:
        # Print welcome message
        welcome_message = "Welcome to the Automagik Agents Chat App"
        
        console.print(Panel(
            f"[bold]{welcome_message}[/bold]",
            border_style="green",
            expand=False
        ))
        
        # Display debug info if enabled
        if DEBUG_MODE:
            console.print("[yellow]Debug mode enabled - showing detailed agent operations[/yellow]")
        
        # Print API information
        console.print(f"[dim]Using API at: {API_BASE_URL}[/dim]")
        if API_KEY:
            masked_key = f"{API_KEY[:4]}...{API_KEY[-4:]}" if len(API_KEY) > 8 else "****"
            console.print(f"[dim]API key loaded: {masked_key}[/dim]")
        
        # Allow the user to modify the API URL if needed
        change_api = Confirm.ask("Would you like to modify the API URL?", default=False)
        if change_api:
            new_api_url = Prompt.ask(
                "Enter the API URL",
                default=API_BASE_URL
            )
            API_BASE_URL = ensure_protocol(new_api_url)
            console.print(f"[green]API URL updated to: {API_BASE_URL}[/green]")
        
        # Always offer to enter an API key manually, even if one was found
        manually_enter_key = Confirm.ask("Would you like to manually enter an API key?", default=(not API_KEY))
        
        if manually_enter_key:
            new_api_key = Prompt.ask(
                "Enter your API key",
                password=True,
                default=""
            )
            if new_api_key:
                API_KEY = new_api_key
                os.environ["API_KEY"] = new_api_key
                console.print("[green]API key updated[/green]")
        
        # Test API connection
        test_api_connection()
    else:
        # In headless mode, verify API connection only if DEBUG_MODE is on
        if DEBUG_MODE:
            test_api_connection()
    
    # Initialize the session based on mode
    try:
        if headless_mode:
            # Load existing session mappings
            load_session_mappings()
            
            # Get session name from argument
            session_name = args.session_name
            
            # Check if the --session parameter was used instead of --session-name
            # This is what we need to fix - use args.session as the session name if provided
            if args.session and not session_name:
                session_name = args.session
                if DEBUG_MODE:
                    print(f"Using session name from --session parameter: {session_name}")
            
            # If session name is provided, try to find the corresponding session ID
            session_id = None
            if session_name:
                session_id = get_session_id_from_name(session_name)
                if not session_id and DEBUG_MODE:
                    print(f"Session name '{session_name}' not found, will create a new session")
            
            # If user ID is provided, use it; otherwise use default (1)
            user_id = args.user if args.user is not None else 1
            user = await get_user_by_id(user_id)
            
            # Get available agents and find the requested one
            agents = get_available_agents()
            agent = next((a for a in agents if a["name"].lower() == args.agent.lower()), None)
            
            if not agent:
                print(f"Error: Agent '{args.agent}' not found", file=sys.stderr)
                sys.exit(1)
            
            # Create a session if not found by name
            if not session_id:
                session_id = await create_session(user["id"], agent["name"], session_name)
            
            if DEBUG_MODE:
                if session_name:
                    print(f"Using session: {session_name} (ID: {session_id})")
                else:
                    print(f"Using session ID: {session_id}")
                print(f"Using user: {user['id']} ({user.get('name', 'Unknown')})")
                print(f"Using agent: {agent['name']}")
            
            # Process a single message and exit
            await headless_chat_once(user, agent, session_id, args.message, session_name)
        else:
            # Interactive mode
            user, agent, session_id, session_name = await chat_init()
            
            # Start the interactive chat loop
            await chat_loop(user, agent, session_id, session_name)
            
            # Prompt if the user wants to see previous messages from the session
            view_history = Confirm.ask("\nWould you like to view the complete chat history?", default=False)
            if view_history:
                try:
                    session_history = await get_session_history(session_id)
                    if session_history and session_history.get("messages"):
                        console.print("\n[bold]Complete Chat History[/bold]")
                        for msg in session_history.get("messages", []):
                            display_message(
                                msg.get("content", ""),
                                msg.get("role", "system"),
                                msg.get("tool_calls", []),
                                msg.get("tool_outputs", []))
                    else:
                        console.print("[yellow]No messages found in the session history[/yellow]")
                except Exception as e:
                    console.print(f"[bold red]Error retrieving session history: {str(e)}[/bold red]")
            
            # Ask if user wants to delete the session
            delete_sess = Confirm.ask("\nWould you like to delete this chat session?", default=False)
            if delete_sess:
                try:
                    if await delete_session(session_id):
                        console.print(f"[green]Session {session_id} deleted[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error deleting session: {str(e)}[/bold red]")
    except Exception as e:
        if headless_mode:
            print(f"Error: {str(e)}", file=sys.stderr)
        else:
            console.print(f"[bold red]Error initializing chat: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 