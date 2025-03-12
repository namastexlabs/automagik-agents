#!/usr/bin/env python3
"""
Interactive CLI chat application for Automagik Agents.

This script provides an interactive command-line interface to chat with an agent.
Unlike the full interactive_agent_chat.py, this simplified version takes agent and session 
parameters from the command line rather than requiring interactive selection.

Usage:
    python run_chat.py --agent simple_agent --session my-session-name

Options:
    --debug         Show detailed debug information
    --api-url       Specify the base URL for the API (default: from .env)
    --api-key       Specify the API key for authentication (default: from .env)
    --agent         Specify which agent to use (required)
    --session       Specify a session name (will reuse if exists)
    --user          User ID to use (default: 1)
"""

import logging
import sys
import argparse
import uuid
import json
import os
import asyncio
import time
import requests
from typing import Dict, List, Optional, Any, Tuple
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("run_chat")

# Create a rich console for pretty output
console = Console()

# Get environment variables
def get_env_var(name, default=None, secret=False):
    """Get an environment variable with debug output."""
    value = os.environ.get(name, default)
    return value

# Global variables
AM_HOST = get_env_var("AM_HOST", "localhost")
AM_PORT = get_env_var("AM_PORT", "8000")
AM_ENV = get_env_var("AM_ENV", "development")

# Construct API_BASE_URL from AM_* variables if they exist
if AM_HOST and AM_PORT:
    API_BASE_URL = f"http://{AM_HOST}:{AM_PORT}"
else:
    API_BASE_URL = get_env_var("API_BASE_URL", "http://localhost:8000")

# Ensure API_BASE_URL doesn't end with a slash
if API_BASE_URL.endswith("/"):
    API_BASE_URL = API_BASE_URL[:-1]

# Try to find the API key from various possible environment variables
API_KEY = (
    get_env_var("AM_API_KEY", None) or 
    get_env_var("API_KEY", None) or 
    get_env_var("OPENAI_API_KEY", None)
)

# Debug mode flag
DEBUG_MODE = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")

# Session mapping storage
SESSION_NAME_TO_ID = {}
SESSION_ID_TO_NAME = {}

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Interactive chat with Automagik Agents")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--api-url", type=str, help="Override API URL")
    parser.add_argument("--api-key", type=str, help="Override API key")
    parser.add_argument("--agent", type=str, required=True, help="Agent to use")
    parser.add_argument("--user", type=int, default=1, help="User ID to use")
    parser.add_argument("--session", type=str, help="Session name to use/create")
    return parser.parse_args()

def ensure_protocol(url: str) -> str:
    """Ensure the URL has a protocol (default to http if none)."""
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"
        console.print(f"[yellow]Added http:// protocol to URL: {url}[/yellow]")
    return url

def get_api_endpoint(path: str) -> str:
    """Build a consistent API endpoint URL with the correct prefix."""
    # Ensure the path doesn't start with a slash
    if path.startswith("/"):
        path = path[1:]
    
    # Always use /api/v1/ prefix
    if not path.startswith("api/v1/"):
        path = f"api/v1/{path}"
    
    # Build the full URL
    url = f"{API_BASE_URL}/{path}"
    
    return url

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
                    console.print(f"[dim]Loaded {len(SESSION_NAME_TO_ID)} session mappings from {sessions_file}[/dim]")
                    if SESSION_NAME_TO_ID:
                        console.print(f"[dim]Available sessions: {', '.join(SESSION_NAME_TO_ID.keys())}[/dim]")
        elif DEBUG_MODE:
            console.print(f"[dim]Session mappings file not found at {sessions_file}[/dim]")
    except Exception as e:
        if DEBUG_MODE:
            console.print(f"[dim]Error loading session mappings from {sessions_file}: {str(e)}[/dim]")
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
            console.print(f"[dim]Saved {len(SESSION_NAME_TO_ID)} session mappings to {sessions_file}[/dim]")
            if SESSION_NAME_TO_ID:
                console.print(f"[dim]Saved sessions: {', '.join(SESSION_NAME_TO_ID.keys())}[/dim]")
    except Exception as e:
        if DEBUG_MODE:
            console.print(f"[dim]Error saving session mappings to {sessions_file}: {str(e)}[/dim]")

def get_session_id_from_name(session_name):
    """Get a session ID from a name, or None if not found."""
    # First, ensure mappings are loaded
    if not SESSION_NAME_TO_ID:
        load_session_mappings()
    
    return SESSION_NAME_TO_ID.get(session_name)

def get_available_agents() -> List[Dict[str, Any]]:
    """Get a list of available agents using the API."""
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
            if DEBUG_MODE:
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

async def create_session(user_id: int, agent_name: str, session_name: str = None) -> Optional[str]:
    """Create a new session or retrieve an existing one by name."""
    # If a session_name is provided, check if it already exists
    if session_name:
        # Load existing mappings
        load_session_mappings()
        
        # Check if this name already exists
        if session_name in SESSION_NAME_TO_ID:
            existing_id = SESSION_NAME_TO_ID[session_name]
            console.print(f"[yellow]Session name '{session_name}' already exists (ID: {existing_id})[/yellow]")
            console.print(f"[yellow]Using the existing session instead of creating a new one.[/yellow]")
            return existing_id
    
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    
    # If a session_name is provided, associate it with this session ID
    if session_name:
        # Store the mapping
        SESSION_NAME_TO_ID[session_name] = session_id
        SESSION_ID_TO_NAME[session_id] = session_name
        
        # Save the updated mappings
        save_session_mappings()
        console.print(f"[dim]Created session '{session_name}' with ID: {session_id}[/dim]")
    else:
        console.print(f"[dim]Generated new session ID: {session_id}[/dim]")
    
    return session_id

async def run_agent(agent_name: str, input_message: str, session_id: str = None, user_id: int = 1, session_name: str = None) -> dict:
    """Run the agent with the given message using the API."""
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
            # Always include session_name at the top level
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
    """Display a message with proper formatting based on role."""
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
                ), justify="right")
        
        # Render the message in a panel
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
        console.print(Panel(
            message,
            border_style="dim red",
            padding=(0, 1),
            expand=False
        ))

async def chat_loop(user: Dict[str, Any], agent: Dict[str, Any], session_id: str, session_name: Optional[str] = None) -> None:
    """Main chat loop for interacting with the agent."""
    # Show session info
    console.print()
    if session_name:
        console.print(f"[dim]Session: {session_name} (ID: {session_id}) | Agent: {agent['name']}[/dim]")
    else:
        console.print(f"[dim]Session: {session_id} | Agent: {agent['name']}[/dim]")
    console.print("[dim]Type 'exit' or 'quit' to end the chat session.[/dim]\n")
    
    # Display welcome message
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
                
                # Get user input
                user_input = input()
                
                # Handle empty input
                if not user_input.strip():
                    continue
                
                # Check for exit command
                if user_input.lower() in ["exit", "quit", "bye"]:
                    console.print("\n[dim]Chat session ended.[/dim]")
                    break
                
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

async def test_api_connection() -> bool:
    """Test connectivity to the API."""
    try:
        url = get_api_endpoint("agent/list")
        console.print(f"[dim]Testing API connection at {url}...[/dim]")
        
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        with console.status(f"[bold green]Testing API connection...") as status:
            # Try to connect to the API
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code < 400:  # Any successful or redirect status code
                console.print(f"[bold green]✅ Connected to API at {url}: Status {response.status_code}[/bold green]")
                
                # Verify we got a valid response
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
                console.print(f"[yellow]API at {url} responded with status code: {response.status_code}[/yellow]")
                
                # If this is the agent list endpoint and got a 401, it's probably an auth issue
                if response.status_code == 401:
                    console.print(f"[bold red]❌ Authentication failed - your API key may be invalid[/bold red]")
    except requests.exceptions.ConnectionError:
        console.print(f"[yellow]Could not connect to API at {url}[/yellow]")
    except Exception as e:
        console.print(f"[yellow]Error testing API at {url}: {str(e)}[/yellow]")
    
    # If we get here, none of the endpoints worked
    console.print(f"[bold red]❌ Could not connect to API at {API_BASE_URL}[/bold red]")
    console.print("[yellow]Check if the API server is running and try again.[/yellow]")
    return False

async def get_session_history(session_id: str) -> Optional[Dict[str, Any]]:
    """Get session history via API."""
    try:
        # Define the API endpoint
        endpoint = get_api_endpoint(f"session/{session_id}")
        console.print(f"[dim]Getting session history from: {endpoint}[/dim]")
        
        # Prepare headers with API key if available
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        # Make the API request
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            session_data = response.json()
            return session_data
        else:
            error_msg = f"Error getting session history: HTTP {response.status_code}"
            console.print(f"[bold red]{error_msg}[/bold red]")
            if DEBUG_MODE:
                console.print(f"[red]Response: {response.text}[/red]")
            return None
    except Exception as e:
        error_msg = f"Error getting session history: {str(e)}"
        console.print(f"[bold red]{error_msg}[/bold red]")
        return None

async def delete_session(session_id: str) -> bool:
    """Delete a session via API."""
    try:
        # Define the API endpoint
        endpoint = get_api_endpoint(f"session/{session_id}")
        console.print(f"[dim]Deleting session at: {endpoint}[/dim]")
        
        # Prepare headers with API key if available
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY
        
        # Make the API request
        response = requests.delete(endpoint, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            # If this was a session with a name, remove from mappings
            if session_id in SESSION_ID_TO_NAME:
                name = SESSION_ID_TO_NAME.get(session_id)
                if name in SESSION_NAME_TO_ID:
                    del SESSION_NAME_TO_ID[name]
                del SESSION_ID_TO_NAME[session_id]
                save_session_mappings()
                
                console.print(f"[bold green]✅ Session '{name}' (ID: {session_id}) deleted successfully[/bold green]")
            else:
                console.print(f"[bold green]✅ Session {session_id} deleted successfully[/bold green]")
            return True
        else:
            error_msg = f"Error deleting session: HTTP {response.status_code}"
            console.print(f"[bold red]{error_msg}[/bold red]")
            console.print(f"[red]Response: {response.text}[/red]")
            return False
    except Exception as e:
        error_msg = f"Error deleting session: {str(e)}"
        console.print(f"[bold red]{error_msg}[/bold red]")
        return False

async def main():
    """Main function."""
    global DEBUG_MODE, API_BASE_URL, API_KEY
    
    # Parse command-line arguments
    args = parse_args()
    
    # Update global variables from arguments
    if args.debug:
        DEBUG_MODE = True
    if args.api_url:
        API_BASE_URL = ensure_protocol(args.api_url)
    if args.api_key:
        API_KEY = args.api_key
    
    # Show welcome message
    console.print(Panel(
        "[bold]Welcome to the Automagik Agents Chat App[/bold]",
        border_style="green",
        expand=False
    ))
    
    # Display debug info if enabled
    if DEBUG_MODE:
        console.print("[yellow]Debug mode enabled - showing detailed agent operations[/yellow]")
    
    # Test API connection
    await test_api_connection()
    
    # Get required information from command line args
    agent_name = args.agent
    user_id = args.user
    session_name = args.session
    
    # Get user info
    user = await get_user_by_id(user_id)
    
    # Get available agents and find the requested one
    agents = get_available_agents()
    agent = next((a for a in agents if a["name"].lower() == agent_name.lower()), None)
    
    if not agent:
        console.print(f"[bold red]Error: Agent '{agent_name}' not found. Available agents:[/bold red]")
        for a in agents:
            console.print(f"  - {a['name']}")
        sys.exit(1)
    
    console.print(f"[bold green]Using agent: {agent['name']}[/bold green]")
    
    # Create or get session
    session_id = None
    if session_name:
        session_id = get_session_id_from_name(session_name)
        if not session_id:
            console.print(f"[yellow]Session name '{session_name}' not found, creating a new session[/yellow]")
    
    if not session_id:
        session_id = await create_session(user_id, agent["name"], session_name)
        if not session_id:
            console.print("[bold red]Failed to create chat session. Exiting...[/bold red]")
            sys.exit(1)
    
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
                        msg.get("tool_outputs", [])
                    )
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

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold]Chat session terminated by user.[/bold]")
        sys.exit(0) 