"""Pytest configuration for Stan Agent integration tests.

This module provides fixtures and configuration for the Stan Agent integration tests.
"""
import os
import pytest
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_API_URL = "http://localhost:8000"
DEFAULT_API_PATH = "/api/v1"
DEFAULT_AGENT_NAME = "stan_agent"

@pytest.fixture
def api_base_url() -> str:
    """Get the base URL for API calls."""
    return os.environ.get("API_BASE_URL", DEFAULT_API_URL)

@pytest.fixture
def api_key() -> str:
    """Get the API key for authentication."""
    return os.environ.get("API_KEY", "test-key")

@pytest.fixture
def headers(api_key: str) -> Dict[str, str]:
    """Get the headers for API calls."""
    return {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

@pytest.fixture
def test_config() -> Dict[str, Any]:
    """Get the test configuration."""
    return {
        "api_base_url": os.environ.get("API_BASE_URL", DEFAULT_API_URL),
        "api_path": os.environ.get("API_PATH", DEFAULT_API_PATH),
        "agent_name": os.environ.get("AGENT_NAME", DEFAULT_AGENT_NAME),
        "test_user_id": int(os.environ.get("TEST_USER_ID", "37")),
        "default_phone": os.environ.get("DEFAULT_PHONE", "555197285829"),
        "default_name": os.environ.get("DEFAULT_NAME", "Cezar Vasconcelos")
    }

def pytest_configure(config):
    """Configure pytest for the Stan Agent integration tests."""
    logger.info("Configuring Stan Agent integration tests")
    
    # Check if the API is available
    import httpx
    
    try:
        response = httpx.get(f"{DEFAULT_API_URL}/health", timeout=2.0)
        if response.status_code == 200:
            logger.info(f"API is available at {DEFAULT_API_URL}")
        else:
            logger.warning(f"API returned unexpected status code: {response.status_code}")
    except Exception as e:
        logger.warning(f"API health check failed: {str(e)}")
        logger.warning(f"Make sure the API is running at {DEFAULT_API_URL} before running tests") 