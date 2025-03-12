#!/usr/bin/env python3
"""
Headless CLI for testing Automagik Agents.

This script provides a simplified command-line interface to send a single message to an agent.
It's designed for quick tests and integrations.

Usage:
    python agent_test.py --agent simple_agent --session test-session --message "What time is it now?"

Options:
    --debug     Show detailed debug information
    --api-url   Specify the base URL for the API (default: from .env)
    --api-key   Specify the API key for authentication (default: from .env)
    --agent     Specify which agent to use (required)
    --session   Specify the session name (will reuse if exists)
    --user      Specify the user ID (default: 1)
    --message   The message to send to the agent
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
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

# Configure minimal logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("agent_test")

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
    parser = argparse.ArgumentParser(description="Headless CLI for Automagik Agents")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--api-url", type=str, help="Override API URL")
    parser.add_argument("--api-key", type=str, help="Override API key")
    parser.add_argument("--agent", type=str, required=True, help="Agent to use")
    parser.add_argument("--user", type=int, default=1, help="User ID to use")
    parser.add_argument("--session", type=str, help="Session name to use/create")
    parser.add_argument("--message", type=str, help="Message to send (if not provided, will read from stdin)")
    return parser.parse_args()

def ensure_protocol(url: str) -> str:
    """Ensure the URL has a protocol (default to http if none)."""
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"
        if DEBUG_MODE:
            print(f"Added http:// protocol to URL: {url}")
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

def get_available_agents() -> List[Dict[str, Any]]:
    """Get a list of available agents using the API."""
    try:
        # Define the API endpoint for listing agents
        endpoint = get_api_endpoint("agent/list")
        if DEBUG_MODE:
            print(f"Getting agents from: {endpoint}")
        
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
                print(f"Successfully retrieved {len(agents)} agents")
            
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
            print(f"Error getting agents: HTTP {response.status_code}", file=sys.stderr)
            if DEBUG_MODE:
                print(f"Response: {response.text}", file=sys.stderr)
            return []
    except Exception as e:
        print(f"Error getting agents from API: {str(e)}", file=sys.stderr)
        return []

async def get_user_by_id(user_id: int) -> Dict[str, Any]:
    """Get user data from the API by ID."""
    try:
        # Define the API endpoint
        endpoint = get_api_endpoint(f"users/{user_id}")
        if DEBUG_MODE:
            print(f"Getting user data from: {endpoint}")
        
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
                print(f"Successfully retrieved user {user_id} from API")
            return user_data
        else:
            if DEBUG_MODE:
                print(f"Error getting user by ID {user_id}: HTTP {response.status_code}")
                print(f"Using fallback user data")
            # Return fallback data
            return {"id": user_id, "email": f"user{user_id}@example.com", "name": f"User {user_id}"}
    except Exception as e:
        if DEBUG_MODE:
            print(f"Error getting user from API: {str(e)}")
            print(f"Using fallback user data")
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
            if DEBUG_MODE:
                print(f"Using existing session: {session_name} (ID: {existing_id})")
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
        
        if DEBUG_MODE:
            print(f"Created session '{session_name}' with ID: {session_id}")
    elif DEBUG_MODE:
        print(f"Generated new session ID: {session_id}")
    
    return session_id

async def run_agent(agent_name: str, input_message: str, session_id: str = None, user_id: int = 1, session_name: str = None) -> dict:
    """Run the agent with the given message using the API."""
    try:
        # Define the API endpoint with the correct prefix
        endpoint = get_api_endpoint(f"agent/{agent_name}/run")
        
        # Only show endpoint in debug mode
        if DEBUG_MODE:
            print(f"Using endpoint: {endpoint}")
        
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
            print(f"Request payload: {json.dumps(payload, indent=2)}")
        
        # Prepare headers with API key
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add API key to headers if available
        if API_KEY:
            headers["x-api-key"] = API_KEY
            
            if DEBUG_MODE:
                masked_key = f"{API_KEY[:4]}...{API_KEY[-4:]}" if len(API_KEY) > 8 else "****"
                print(f"Using API key: {masked_key}")
        
        # Make the API request
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        
        # Check response status
        if response.status_code == 200:
            result = response.json()
            if DEBUG_MODE:
                print(f"API Response: {json.dumps(result, indent=2)}")
            return result
        else:
            error_msg = f"API Error: Status {response.status_code}"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_msg = f"API Error: {error_data['detail']}"
            except Exception:
                error_msg = f"API Error: {response.text}"
            
            print(f"{error_msg}", file=sys.stderr)
            return {"error": error_msg}
                
    except Exception as e:
        error_msg = f"Error running agent: {str(e)}"
        print(f"{error_msg}", file=sys.stderr)
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
            print("\n".join([f"[Tool] {tool}" for tool in tool_usage]))
    
    # Print the message with role prefix
    if message.strip():
        print(f"{role}: {message}")

async def process_single_message(agent_name: str, message: str, session_name: str = None, user_id: int = 1) -> None:
    """Process a single message exchange and exit."""
    # First, check if the agent exists
    agents = get_available_agents()
    agent = next((a for a in agents if a["name"].lower() == agent_name.lower()), None)
    
    if not agent:
        print(f"Error: Agent '{agent_name}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Get user info
    user = await get_user_by_id(user_id)
    
    # Get or create session ID
    session_id = None
    if session_name:
        session_id = get_session_id_from_name(session_name)
        if not session_id:
            if DEBUG_MODE:
                print(f"Session name '{session_name}' not found, creating a new session")
    
    # Create a session if needed
    if not session_id:
        session_id = await create_session(user_id, agent_name, session_name)
    
    if DEBUG_MODE:
        if session_name:
            print(f"Using session: {session_name} (ID: {session_id})")
        else:
            print(f"Using session ID: {session_id}")
        print(f"Using agent: {agent_name}")
    
    # Get the message from command line or stdin
    if not message:
        # Read message from stdin
        if sys.stdin.isatty():
            print("Enter message: ", end="", flush=True)
        message = input().strip()
    
    # Check if we have a message to process
    if not message:
        print("Error: No message provided", file=sys.stderr)
        sys.exit(1)
    
    # Display user message
    print(f"user: {message}")
    
    # Process the message
    try:
        response = await run_agent(agent_name, message, session_id, user_id, session_name)
        
        if "error" in response and response["error"]:
            print(f"Error: {response['error']}", file=sys.stderr)
            sys.exit(1)
        
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
        if session_name and not DEBUG_MODE:
            print(f"\nSession '{session_name}' (ID: {session_id}) updated successfully")
        elif not DEBUG_MODE:
            print(f"\nSession ID: {session_id}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

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
    
    # Process the message
    await process_single_message(
        agent_name=args.agent,
        message=args.message,
        session_name=args.session,
        user_id=args.user
    )

if __name__ == "__main__":
    asyncio.run(main()) 