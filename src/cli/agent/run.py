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

from src.config import settings
from src.agents.models.agent_factory import AgentFactory

# Create app for the run command
run_app = typer.Typer(no_args_is_help=True)

@run_app.callback()
def run_callback(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    Run a single message through an agent and get the response.
    
    Use the 'message' command with required options:
      automagik-agents agent run message --agent <agent_name> --message "Your message here"
    
    Example:
      automagik-agents agent run message --agent simple --message "Hello, how are you?"
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
    debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (os.environ.get("AM_LOG_LEVEL") == "DEBUG")
    
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
                        agent["description"] = f"Agent of type {agent.get('type', 'unknown')}"
                    
                    # If model is missing, provide a default
                    if "model" not in agent or not agent["model"]:
                        agent["model"] = "unknown"
                
                return agents
            else:
                typer.echo(f"Error getting agents: HTTP {response.status_code}", err=True)
                if debug_mode:
                    typer.echo(f"Response: {response.text}", err=True)
                return []
        except requests.exceptions.ConnectionError:
            typer.echo(f"Connection error: Could not connect to API server at {endpoint}", err=True)
            return []
    except Exception as e:
        typer.echo(f"Error getting agents from API: {str(e)}", err=True)
        return []

async def get_user_by_id(user_id: int) -> Dict[str, Any]:
    """Get user data from the API by ID."""
    # Check if debug mode is enabled either via settings or directly from environment variable
    debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (os.environ.get("AM_LOG_LEVEL") == "DEBUG")
    
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
                typer.echo(f"Error getting user by ID {user_id}: HTTP {response.status_code}")
                typer.echo(f"Using fallback user data")
            # Return fallback data
            return {"id": user_id, "email": f"user{user_id}@example.com", "name": f"User {user_id}"}
    except Exception as e:
        if debug_mode:
            typer.echo(f"Error getting user from API: {str(e)}")
            typer.echo(f"Using fallback user data")
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
            typer.echo(f"Using endpoint: {endpoint}")
        
        # Prepare the payload according to the API's expected format
        payload = {
            "message_content": input_message,
            "user_id": user_id,
            "context": {"debug": debug_mode},
            "session_origin": "cli"
        }
        
        # Add session_name if provided
        if session_name:
            payload["session_name"] = session_name
        
        if debug_mode:
            typer.echo(f"Request payload: {json.dumps(payload, indent=2)}")
        
        # Prepare headers with API key
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add API key to headers if available
        if settings.AM_API_KEY:
            headers["x-api-key"] = settings.AM_API_KEY
            
            if debug_mode:
                masked_key = f"{settings.AM_API_KEY[:4]}...{settings.AM_API_KEY[-4:]}" if len(settings.AM_API_KEY) > 8 else "****"
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
                    if "duplicate key value violates unique constraint" in error_data.get("detail", "") and "sessions_name_key" in error_data.get("detail", ""):
                        error_msg = f"Session name '{session_name}' is already in use. Please use a different session name."
            except Exception:
                error_msg = f"API Error: {response.text}"
            
            typer.echo(f"{error_msg}", err=True)
            return {"error": error_msg}
                
    except Exception as e:
        error_msg = f"Error running agent: {str(e)}"
        typer.echo(f"{error_msg}", err=True)
        return {"error": error_msg}

def display_message(message: str, role: str, tool_calls: List = None, tool_outputs: List = None) -> None:
    """Display a message in plain text format."""
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
            typer.echo("\n".join([f"[Tool] {tool}" for tool in tool_usage]))
    
    # Print the message with role prefix
    if message.strip():
        typer.echo(f"{role}: {message}")

async def process_single_message(agent_name: str, message: str, session_name: str = None, user_id: int = 1) -> None:
    """Process a single message exchange and exit."""
    # Check if debug mode is enabled either via settings or directly from environment variable
    debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (os.environ.get("AM_LOG_LEVEL") == "DEBUG")
    
    # First, check if the agent exists
    agents = get_available_agents()
    agent = next((a for a in agents if a["name"].lower() == agent_name.lower()), None)
    
    if not agent:
        typer.echo(f"Error: Agent '{agent_name}' not found", err=True)
        raise typer.Exit(code=1)
    
    # Get user info
    user = await get_user_by_id(user_id)
    
    if debug_mode:
        if session_name:
            typer.echo(f"Using session: {session_name}")
        typer.echo(f"Using agent: {agent_name}")
    
    # Check if we have a message to process
    if not message:
        typer.echo("Error: No message provided", err=True)
        raise typer.Exit(code=1)
    
    # Display user message
    typer.echo(f"user: {message}")
    
    # Process the message
    try:
        response = await run_agent(agent_name, message, session_name, user_id)
        
        if "error" in response and response["error"]:
            typer.echo(f"Error: {response['error']}", err=True)
            
            # Add helpful advice for session name errors
            if session_name and "already in use" in response["error"]:
                typer.echo("\nTIP: To see existing sessions, you can run:", err=True)
                api_url = f"http://{settings.AM_HOST}:{settings.AM_PORT}"
                typer.echo(f"  curl {api_url}/api/v1/sessions -H 'x-api-key: {settings.AM_API_KEY}'", err=True)
                typer.echo("\nOr use a different session name:", err=True)
                typer.echo(f"  automagik-agents agent run message --agent {agent_name} --session new-session-name --message \"{message}\"", err=True)
            
            raise typer.Exit(code=1)
        
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
        
        # Display session info for reference
        if session_name and not debug_mode:
            typer.echo(f"\nSession '{session_name}' updated successfully")
        elif debug_mode and "session_id" in response:
            typer.echo(f"\nSession '{session_name}' with ID: {response['session_id']} updated successfully")
        
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(code=1)

@run_app.command()
def message(
    agent: str = typer.Option(..., "--agent", "-a", help="Agent to use"),
    session: Optional[str] = typer.Option(None, "--session", "-s", help="Session name to use/create"),
    user: int = typer.Option(1, "--user", "-u", help="User ID to use"),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="Message to send (if not provided, will read from stdin)"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    Run a single message through an agent and get the response.
    
    If no message is provided, it will be read from stdin.
    Sessions are preserved between calls with the same session name.
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"
        
    # Get the message from command line or stdin
    input_message = message
    if not input_message:
        # Read message from stdin
        if sys.stdin.isatty():
            typer.echo("Enter message: ", nl=False)
        input_message = input().strip()
    
    # Check if debug mode is enabled either via settings or directly from environment variable
    debug_mode = (settings.AM_LOG_LEVEL == "DEBUG") or (os.environ.get("AM_LOG_LEVEL") == "DEBUG")
    
    if debug_mode:
        typer.echo(f"Processing message: {input_message}")
    
    asyncio.run(process_single_message(
        agent_name=agent,
        message=input_message,
        session_name=session,
        user_id=user
    ))

def list_available_agents() -> None:
    """Print a list of available agents."""
    agents = get_available_agents()
    
    if not agents:
        typer.echo("Error: No agents available or could not connect to the API.", err=True)
        typer.echo("\nPossible reasons:")
        typer.echo("1. The server might not be running. Start it with:")
        typer.echo("     automagik-agents api start")
        typer.echo("2. Your API server could be running on a different host/port.")
        typer.echo(f"   Current server setting: {settings.AM_HOST}:{settings.AM_PORT}")
        typer.echo("3. You might not have added any agents yet.")
        
        typer.echo("\nTry creating an agent first:")
        typer.echo("  automagik-agents agent create agent --name my_agent --template simple_agent")
        
        typer.echo("\nOr check if you can access the API directly:")
        typer.echo(f"  curl http://{settings.AM_HOST}:{settings.AM_PORT}/api/v1/agent/list -H 'x-api-key: {settings.AM_API_KEY}'")
        return
    
    typer.echo("\nAvailable Agents:")
    for i, agent in enumerate(agents, 1):
        name = agent.get("name", "Unknown")
        description = agent.get("description", "No description")
        model = agent.get("model", "Unknown model")
        
        typer.echo(f"{i}. {name} - {description} (Model: {model})")
    
    typer.echo("\nUse the agent name with the run command:")
    typer.echo(f"  automagik-agents agent run message --agent <agent_name> --message \"Your message here\"")

@run_app.command()
def list():
    """
    List all available agents that can be used for running messages.
    """
    list_available_agents() 