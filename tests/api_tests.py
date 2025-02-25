#!/usr/bin/env python3
"""
API Test Script - Tests all endpoints in the Automagik Agents API sequentially.

This script tests the following endpoints in order:
1. Health check - Verify the API is running
2. List agents - Get available agents
3. Run an agent - Create a new session
4. Get session info - Verify session was created correctly
5. List all sessions - Verify session appears in list
6. Delete session - Clean up test session
"""

import json
import os
import requests
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Get the absolute path to the root .env file for debugging
env_path = Path(__file__).parent.parent / '.env'
print(f"Looking for .env file at: {env_path.absolute()}")
print(f"File exists: {env_path.exists()}")

# Load environment variables from root .env file
load_dotenv(env_path)

# Configuration
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("AM_API_KEY")  # Get API key from .env file with the correct variable name

# Print debug info about what was loaded
print(f"Loaded BASE_URL: {BASE_URL}")
print(f"Loaded API_KEY: {API_KEY}")

# Ensure API key is available
if not API_KEY:
    print("⚠️ Warning: AM_API_KEY not found in .env file, using default key for testing")
    API_KEY = "namastex-888"  # Fallback to default key if not in .env

# Hardcode the API key for now (for testing)
API_KEY = "namastex-888"
print(f"Final API_KEY being used: {API_KEY}")

# Set the correct header format - using x-api-key instead of Authorization
HEADERS = {"x-api-key": API_KEY}
TEST_SESSION_ID = f"test-session-{int(time.time())}"  # Generate unique session ID
USER_ID = os.getenv("TEST_USER_ID", "test-user")

def print_response(response, endpoint):
    """Helper function to print formatted API responses"""
    print(f"\n{'=' * 80}")
    print(f"Testing: {endpoint}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {response.elapsed.total_seconds():.3f}s")
    
    # Print headers if needed
    # print("Headers:")
    # for key, value in response.headers.items():
    #     print(f"  {key}: {value}")
    
    try:
        print("Response Body:")
        formatted_json = json.dumps(response.json(), indent=2)
        print(formatted_json)
    except:
        print(f"Raw Response: {response.text}")
    
    print(f"{'=' * 80}\n")
    
    # Ensure we have a valid response
    assert 200 <= response.status_code < 300, f"API call failed with status code {response.status_code}"
    return response.json()

def test_health_endpoint():
    """Test the health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    data = print_response(response, "Health Endpoint")
    assert data["status"] == "healthy", "Health check failed"
    print("✅ Health check successful")
    return data

def test_root_endpoint():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    data = print_response(response, "Root Endpoint")
    assert "status" in data, "Root endpoint check failed"
    assert data["status"] == "online", "Service is not online"
    print("✅ Root endpoint check successful")
    return data

def test_list_agents():
    """Test listing all available agents"""
    response = requests.get(f"{BASE_URL}/api/v1/agent/list", headers=HEADERS)
    data = print_response(response, "List Agents")
    assert isinstance(data, list), "Expected a list of agents"
    assert len(data) > 0, "No agents found"
    print(f"✅ Found {len(data)} agents")
    return data

def test_run_agent(agent_name="simple"):
    """Test running an agent to create a new session"""
    payload = {
        "message_input": "Hello, this is a test message",
        "session_id": TEST_SESSION_ID,
        "user_id": USER_ID,
        "context": {},
        "message_limit": 10
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/agent/{agent_name}/run", 
        headers=HEADERS,
        json=payload
    )
    data = print_response(response, f"Run Agent: {agent_name}")
    assert "session_id" in data, "No session_id in response"
    assert data["session_id"] == TEST_SESSION_ID, "Session ID mismatch"
    print(f"✅ Successfully ran agent and created session: {TEST_SESSION_ID}")
    return data

def test_get_session():
    """Test getting session information"""
    response = requests.get(
        f"{BASE_URL}/api/v1/session/{TEST_SESSION_ID}",
        headers=HEADERS,
        params={"page": 1, "page_size": 50, "sort_desc": True, "hide_tools": False}
    )
    data = print_response(response, f"Get Session: {TEST_SESSION_ID}")
    assert data["session_id"] == TEST_SESSION_ID, "Session ID mismatch"
    assert data["exists"] == True, "Session does not exist"
    assert len(data["messages"]) > 0, "No messages found in session"
    print(f"✅ Successfully retrieved session with {data['total_messages']} messages")
    return data

def test_list_sessions():
    """Test listing all sessions"""
    response = requests.get(
        f"{BASE_URL}/api/v1/sessions",
        headers=HEADERS,
        params={"page": 1, "page_size": 50, "sort_desc": True}
    )
    data = print_response(response, "List Sessions")
    assert isinstance(data["sessions"], list), "Expected a list of sessions"
    
    # Verify our test session is in the list
    session_found = False
    for session in data["sessions"]:
        if session["session_id"] == TEST_SESSION_ID:
            session_found = True
            break
    
    assert session_found, f"Test session {TEST_SESSION_ID} not found in sessions list"
    print(f"✅ Successfully listed {data['total_count']} sessions including our test session")
    return data

def test_delete_session():
    """Test deleting a session"""
    response = requests.delete(
        f"{BASE_URL}/api/v1/session/{TEST_SESSION_ID}",
        headers=HEADERS
    )
    data = print_response(response, f"Delete Session: {TEST_SESSION_ID}")
    assert data["status"] == "success", "Session deletion failed"
    assert data["session_id"] == TEST_SESSION_ID, "Session ID mismatch"
    print(f"✅ Successfully deleted session: {TEST_SESSION_ID}")
    
    # Verify session is actually gone
    response = requests.get(
        f"{BASE_URL}/api/v1/session/{TEST_SESSION_ID}",
        headers=HEADERS
    )
    verify_data = response.json()
    assert verify_data["exists"] == False, "Session still exists after deletion"
    print("✅ Verified session is no longer accessible")
    return data

def test_openapi_schema():
    """Test the OpenAPI schema endpoint"""
    response = requests.get(f"{BASE_URL}/api/v1/openapi.json")
    data = print_response(response, "OpenAPI Schema")
    assert "paths" in data, "OpenAPI schema is missing paths"
    assert "info" in data, "OpenAPI schema is missing info"
    print(f"✅ Successfully retrieved OpenAPI schema with {len(data['paths'])} endpoints")
    return data

def test_swagger_docs():
    """Test the Swagger UI documentation endpoint"""
    response = requests.get(f"{BASE_URL}/api/v1/docs")
    # This returns HTML, no need to parse as JSON
    print(f"\n{'=' * 80}")
    print(f"Testing: Swagger UI Docs")
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {response.elapsed.total_seconds():.3f}s")
    print(f"Content Type: {response.headers.get('content-type', 'unknown')}")
    print(f"Content Length: {len(response.text)} bytes")
    print(f"{'=' * 80}\n")
    
    assert response.status_code == 200, f"API call failed with status code {response.status_code}"
    assert "text/html" in response.headers.get("content-type", ""), "Expected HTML response"
    assert "swagger" in response.text.lower(), "Swagger UI not found in response"
    print("✅ Successfully retrieved Swagger UI documentation")
    return response.text

def test_redoc_docs():
    """Test the ReDoc documentation endpoint"""
    response = requests.get(f"{BASE_URL}/api/v1/redoc")
    # This returns HTML, no need to parse as JSON
    print(f"\n{'=' * 80}")
    print(f"Testing: ReDoc Docs")
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {response.elapsed.total_seconds():.3f}s")
    print(f"Content Type: {response.headers.get('content-type', 'unknown')}")
    print(f"Content Length: {len(response.text)} bytes")
    print(f"{'=' * 80}\n")
    
    assert response.status_code == 200, f"API call failed with status code {response.status_code}"
    assert "text/html" in response.headers.get("content-type", ""), "Expected HTML response"
    assert "redoc" in response.text.lower(), "ReDoc not found in response"
    print("✅ Successfully retrieved ReDoc documentation")
    return response.text

def main():
    """Run all tests in sequence"""
    print(f"\n{'*' * 80}")
    print(f"* AUTOMAGIK AGENTS API TEST SUITE")
    print(f"* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"* Testing against: {BASE_URL}")
    print(f"* Test session ID: {TEST_SESSION_ID}")
    print(f"{'*' * 80}\n")
    
    # Store test results
    results = {}
    
    try:
        # Test root and health endpoints (no auth required)
        results["health"] = test_health_endpoint()
        results["root"] = test_root_endpoint()
        
        # Test documentation endpoints (no auth required)
        results["openapi_schema"] = test_openapi_schema()
        results["swagger_docs"] = test_swagger_docs()
        results["redoc_docs"] = test_redoc_docs()
        
        # Test agents endpoints
        results["list_agents"] = test_list_agents()
        
        # Create a session by running an agent
        results["run_agent"] = test_run_agent()
        
        # Test session retrieval
        results["get_session"] = test_get_session()
        
        # Test listing all sessions
        results["list_sessions"] = test_list_sessions()
        
        # Test session deletion (cleanup)
        results["delete_session"] = test_delete_session()
        
        print("\n✅ All tests completed successfully!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 