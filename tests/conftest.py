"""Test configuration for pytest."""
import os
from pathlib import Path
from dotenv import load_dotenv
import pytest
from unittest.mock import Mock, AsyncMock
from src.agents.models.dependencies import AutomagikAgentsDependencies

# Get the project root directory
project_root = Path(__file__).parent.parent

# Load environment variables from .env file
env_path = project_root / '.env'
load_dotenv(env_path)

@pytest.fixture
def optimized_test_dependencies():
    """Create optimized dependencies for testing that skip expensive operations."""
    return AutomagikAgentsDependencies(
        test_mode=True,
        disable_memory_operations=True,
        mock_external_apis=True,
        model_name="openai:gpt-4.1-mini",  # Use faster model for tests
        model_settings={"temperature": 0.0}  # Deterministic responses
    )

@pytest.fixture
def mock_graphiti_client():
    """Mock Graphiti client to avoid expensive memory operations."""
    mock_client = AsyncMock()
    mock_client.add_episode = AsyncMock(return_value={"success": True, "episode_id": "test-episode"})
    mock_client.search = AsyncMock(return_value={"nodes": [], "edges": []})
    return mock_client

@pytest.fixture(autouse=True)
def fast_test_environment():
    """Automatically configure fast test environment for all tests."""
    # Set environment variables for faster testing
    os.environ["DISABLE_MEMORY_OPERATIONS"] = "true"
    os.environ["MOCK_EXTERNAL_APIS"] = "true"
    os.environ["TEST_MODE"] = "true"
    
    yield
    
    # Cleanup
    os.environ.pop("DISABLE_MEMORY_OPERATIONS", None)
    os.environ.pop("MOCK_EXTERNAL_APIS", None)
    os.environ.pop("TEST_MODE", None) 