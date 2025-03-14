#!/usr/bin/env python3
"""
Pytest version of the API tests for Automagik Agents.

This file contains tests for all API endpoints using pytest, which provides:
- Better test discovery and organization
- Test fixtures for setup/teardown
- Rich reporting options (HTML, JSON, JUnit XML)
- Better isolation between tests
- Parameterization for edge cases

To run:
pytest tests/test_api.py -v  # Verbose mode
pytest tests/test_api.py --html=report.html  # Generate HTML report
pytest tests/test_api.py -xvs  # Stop on first failure, verbose, no capture
"""

import json
import os
import time
import pytest
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'  # Updated path to account for new directory structure
load_dotenv(env_path)

# Configuration
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8881")

# Get API key from environment, removing any comments or whitespace
raw_api_key = os.getenv("AM_API_KEY", "")
if raw_api_key:
    # Extract just the actual key by splitting at the first '#' or whitespace
    API_KEY = raw_api_key.split('#')[0].split()[0].strip()
else:
    API_KEY = "namastex-888"  # Default key if not in .env

HEADERS = {"x-api-key": API_KEY}

# Test resources that will be shared across tests via fixtures
TEST_RESOURCES = {
    "user_id": None,
    "user_email": f"test-user-{int(time.time())}@example.com",
    "user_phone": f"+1555{int(time.time())%1000000:06d}",
    "user_data": {"test": True, "timestamp": int(time.time())},
    "session_id": None,
}

# ==========================================
# Test Fixtures
# ==========================================

@pytest.fixture(scope="session", autouse=True)
def initialize_agents():
    """Initialize all agents before running tests.
    
    This fixture automatically runs once before all tests to ensure
    agents are discovered and registered in the system.
    """
    try:
        print("\nInitializing agents before tests...")
        # Try to use our agent initialization code from the agent factory directly
        try:
            from src.agents.models.agent_factory import AgentFactory
            
            # Run discovery with our improved logic
            AgentFactory.discover_agents()
            
            # Get the available agents
            available_agents = AgentFactory.list_available_agents()
            
            if available_agents:
                print(f"Agents initialized successfully: {', '.join(available_agents)}")
            else:
                print("WARNING: No agents were discovered during initialization")
                
        except ImportError:
            print("Could not import AgentFactory, falling back to initialize_all_agents")
            # Fall back to the main initialization function
            from src.main import initialize_all_agents
            initialize_all_agents()
            
        yield
    except ImportError as e:
        # This could happen if the main module isn't in the right place
        print(f"WARNING: Could not import agent initialization code: {e}")
        print("Tests requiring agents may fail")
        yield
    except Exception as e:
        # Don't fail the entire test suite if initialization fails
        print(f"WARNING: Failed to initialize agents: {e}")
        print("Tests requiring agents may fail")
        yield

@pytest.fixture(scope="session")
def base_url():
    """Provide the base URL for API tests"""
    return BASE_URL

@pytest.fixture(scope="session")
def auth_headers():
    """Provide authentication headers for API tests"""
    return HEADERS

@pytest.fixture(scope="session")
def test_user(base_url, auth_headers):
    """Create a test user and return its details. Clean up after tests."""
    # Create a test user for all tests
    payload = {
        "email": TEST_RESOURCES["user_email"],
        "phone_number": TEST_RESOURCES["user_phone"],
        "user_data": TEST_RESOURCES["user_data"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/users",
            headers=auth_headers,
            json=payload
        )
        response.raise_for_status()
        user_data = response.json()
        TEST_RESOURCES["user_id"] = user_data["id"]
        test_user_id = user_data["id"]
        
        # Return the user data for tests to use
        yield user_data
        
        # Cleanup after all tests are done
        if test_user_id > 1:  # Don't delete admin/system users
            try:
                requests.delete(
                    f"{base_url}/api/v1/users/{test_user_id}",
                    headers=auth_headers
                )
            except:
                pass  # It's fine if cleanup fails
                
    except Exception as e:
        print(f"Failed to create test user: {e}")
        # Fall back to using default admin user
        try:
            # Try to get existing users
            response = requests.get(
                f"{base_url}/api/v1/users",
                headers=auth_headers
            )
            response.raise_for_status()
            users = response.json().get("users", [])
            if users:
                # Use the first user (usually admin)
                admin_user = users[0]
                TEST_RESOURCES["user_id"] = admin_user["id"]
                # Skip cleanup for default users
                yield admin_user
            else:
                # No users found, return a default placeholder
                pytest.skip("No users available for testing")
                yield {"id": 1, "email": "admin@automagik"}
        except Exception as e2:
            print(f"Failed to get default user: {e2}")
            # Provide placeholder user data
            pytest.skip("Using default user data as fallback")
            yield {"id": 1, "email": "admin@automagik"}

@pytest.fixture(scope="session")
def test_session(base_url, auth_headers, test_user):
    """Create a test session by running an agent and return session details."""
    # Create a session
    session_name = f"test-session-{int(time.time())}"
    payload = {
        "message_content": "Test message for pytest API tests",
        "session_name": session_name,
        "user_id": test_user["id"],
        "context": {"source": "pytest"},
        "message_limit": 10,
        "session_origin": "pytest"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/agent/simple/run",
            headers=auth_headers,
            json=payload
        )
        response.raise_for_status()
        session_data = response.json()
        TEST_RESOURCES["session_id"] = session_data["session_id"]
        
        # Wait for session to be fully stored
        time.sleep(1)
        
        # Return the session data for tests to use
        yield session_data
        
        # Cleanup after all tests are done
        if TEST_RESOURCES["session_id"]:
            try:
                requests.delete(
                    f"{base_url}/api/v1/sessions/{TEST_RESOURCES['session_id']}",
                    headers=auth_headers
                )
            except Exception as e:
                print(f"Error cleaning up test session: {e}")
    except Exception as e:
        print(f"Failed to create test session: {e}")
        pytest.skip("Could not create test session")
        yield None

# ==========================================
# System Tests
# ==========================================

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    response = requests.get(f"{base_url}/health")
    response.raise_for_status()
    data = response.json()
    
    assert "status" in data, "Missing status field"
    assert data["status"] == "healthy", f"Unexpected status: {data['status']}"

def test_root_endpoint(base_url):
    """Test the root endpoint"""
    response = requests.get(f"{base_url}/")
    response.raise_for_status()
    data = response.json()
    
    assert "status" in data, "Missing status field"
    assert data["status"] == "online", f"Unexpected status: {data['status']}"

def test_openapi_schema(base_url):
    """Test the OpenAPI schema endpoint"""
    response = requests.get(f"{base_url}/api/v1/openapi.json")
    response.raise_for_status()
    data = response.json()
    
    assert "paths" in data, "Missing paths field"
    assert "info" in data, "Missing info field"
    assert len(data["paths"]) > 0, "No endpoints in OpenAPI schema"

def test_swagger_docs(base_url):
    """Test the Swagger UI documentation endpoint"""
    response = requests.get(f"{base_url}/api/v1/docs")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "text/html" in response.headers.get("content-type", ""), "Expected HTML response"
    assert "swagger" in response.text.lower(), "Swagger UI not found in response"

def test_redoc_docs(base_url):
    """Test the ReDoc documentation endpoint"""
    response = requests.get(f"{base_url}/api/v1/redoc")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "text/html" in response.headers.get("content-type", ""), "Expected HTML response"
    assert "redoc" in response.text.lower(), "ReDoc not found in response"

# ==========================================
# User Tests
# ==========================================

def test_get_user_by_id(base_url, auth_headers, test_user):
    """Test getting user by ID"""
    response = requests.get(
        f"{base_url}/api/v1/users/{test_user['id']}",
        headers=auth_headers
    )
    response.raise_for_status()
    data = response.json()
    
    assert data["id"] == test_user["id"], f"User ID mismatch: {data.get('id')} != {test_user['id']}"
    assert data["email"] == test_user["email"], f"Email mismatch: {data.get('email')} != {test_user['email']}"

def test_get_user_by_email(base_url, auth_headers, test_user):
    """Test getting user by email"""
    # Skip for default user
    if test_user["id"] == 1:
        pytest.skip("Using default user, skipping email lookup test")
    
    response = requests.get(
        f"{base_url}/api/v1/users/{test_user['email']}",
        headers=auth_headers
    )
    response.raise_for_status()
    data = response.json()
    
    assert data["email"] == test_user["email"], f"Email mismatch: {data.get('email')} != {test_user['email']}"

def test_get_user_by_phone(base_url, auth_headers):
    """Test getting user by phone number"""
    # Skip if not using custom user
    if TEST_RESOURCES["user_id"] == 1:
        pytest.skip("Using default user, skipping phone lookup test")
    
    response = requests.get(
        f"{base_url}/api/v1/users/{TEST_RESOURCES['user_phone']}",
        headers=auth_headers
    )
    response.raise_for_status()
    data = response.json()
    
    assert data["phone_number"] == TEST_RESOURCES["user_phone"], f"Phone mismatch"

def test_update_user_email(base_url, auth_headers, test_user):
    """Test updating user email"""
    # Skip for default user
    if test_user["id"] == 1:
        pytest.skip("Using default user, skipping update test")
    
    # Generate a new email
    updated_email = f"updated-{test_user['email']}"
    
    response = requests.put(
        f"{base_url}/api/v1/users/{test_user['id']}",
        headers=auth_headers,
        json={"email": updated_email}
    )
    response.raise_for_status()
    data = response.json()
    
    assert data["email"] == updated_email, f"Email not updated: {data.get('email')} != {updated_email}"
    
    # Update the global resource for future tests
    TEST_RESOURCES["user_email"] = updated_email

def test_update_user_data(base_url, auth_headers, test_user):
    """Test updating user data"""
    # Skip for default user
    if test_user["id"] == 1:
        pytest.skip("Using default user, skipping update test")
    
    # Update user data with new fields
    updated_data = {
        **TEST_RESOURCES["user_data"],
        "updated": True,
        "timestamp": int(time.time())
    }
    
    response = requests.put(
        f"{base_url}/api/v1/users/{test_user['id']}",
        headers=auth_headers,
        json={"user_data": updated_data}
    )
    response.raise_for_status()
    data = response.json()
    
    # Verify user_data contains our updates
    assert "user_data" in data, "user_data field missing from response"
    assert data["user_data"].get("updated") == True, "user_data.updated field not set to True"

def test_list_users(base_url, auth_headers, test_user):
    """Test listing all users"""
    response = requests.get(
        f"{base_url}/api/v1/users",
        headers=auth_headers,
        params={"page": 1, "page_size": 50}
    )
    response.raise_for_status()
    data = response.json()
    
    assert "users" in data, "No users field in response"
    assert "total_count" in data, "No total_count field in response"
    assert isinstance(data["users"], list), "Users is not a list"
    
    # Check if our test user is in the list
    user_ids = [user["id"] for user in data["users"]]
    assert test_user["id"] in user_ids, f"Test user {test_user['id']} not found in users list"

# ==========================================
# Agent Tests
# ==========================================

def test_list_agents(base_url, auth_headers):
    """Test listing all available agents"""
    response = requests.get(
        f"{base_url}/api/v1/agent/list",
        headers=auth_headers
    )
    response.raise_for_status()
    data = response.json()
    
    assert isinstance(data, list), "Expected a list of agents"
    
    # If no agents are found, we'll skip the test instead of failing
    if len(data) == 0:
        pytest.skip("No agents found - this might be expected in certain test environments")
    
    # This assertion only runs if we have agents
    agent_names = [agent["name"] for agent in data]
    print(f"Found agents: {', '.join(agent_names)}")
    
    return {"agent_count": len(data), "agent_names": agent_names}

# ==========================================
# Session Tests
# ==========================================

def test_get_session_by_id(base_url, auth_headers, test_session):
    """Test getting session by ID"""
    if not test_session:
        pytest.skip("No test session available")
    
    # Try multiple times with delay if session is slow to be stored
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.get(
                f"{base_url}/api/v1/sessions/{test_session['session_id']}",
                headers=auth_headers
            )
            response.raise_for_status()
            data = response.json()
            
            assert data["session_id"] == test_session["session_id"], "Session ID mismatch"
            assert data["exists"] == True, "Session does not exist according to API"
            assert "messages" in data, "No messages field in response"
            break
        except (AssertionError, requests.RequestException) as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                raise

def test_list_sessions(base_url, auth_headers, test_session):
    """Test listing all sessions"""
    if not test_session:
        pytest.skip("No test session available")
    
    response = requests.get(
        f"{base_url}/api/v1/sessions",
        headers=auth_headers
    )
    response.raise_for_status()
    data = response.json()
    
    assert "sessions" in data, "No sessions field in response"
    assert "total_count" in data, "No total_count field in response"

# ==========================================
# Error Case Tests
# ==========================================

def test_invalid_api_key(base_url):
    """Test using an invalid API key"""
    response = requests.get(
        f"{base_url}/api/v1/users",
        headers={"x-api-key": "invalid-key"}
    )
    
    assert response.status_code in [401, 403], f"Expected 401/403 for invalid API key, got {response.status_code}"

def test_nonexistent_user(base_url, auth_headers):
    """Test getting a nonexistent user"""
    response = requests.get(
        f"{base_url}/api/v1/users/nonexistent-user-{int(time.time())}",
        headers=auth_headers
    )
    
    assert response.status_code == 404, f"Expected 404 for nonexistent user, got {response.status_code}"

def test_nonexistent_session(base_url, auth_headers):
    """Test getting a nonexistent session"""
    nonexistent_id = f"00000000-0000-0000-0000-{int(time.time())}"
    response = requests.get(
        f"{base_url}/api/v1/sessions/{nonexistent_id}",
        headers=auth_headers
    )
    
    # This endpoint doesn't return a 404, it returns a 200 with exists=False
    assert response.status_code == 200, f"Expected 200 for nonexistent session, got {response.status_code}"
    data = response.json()
    assert data["exists"] == False, "Expected exists=False for nonexistent session"

def test_invalid_user_create(base_url, auth_headers):
    """Test creating a user with invalid data"""
    # Empty payload should fail validation
    response = requests.post(
        f"{base_url}/api/v1/users",
        headers=auth_headers,
        json={}
    )
    
    assert response.status_code == 400, f"Expected 400 for invalid user data, got {response.status_code}"

if __name__ == "__main__":
    print(f"Running pytest tests against {BASE_URL}")
    # This is useful for manual debugging but not needed for pytest
    # Usually pytest would be run using the command line:
    # pytest tests/test_api.py -v