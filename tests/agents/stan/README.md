# Stan Agent Integration Tests

This directory contains integration tests for the Stan Agent API. These tests focus on testing the API endpoints directly, rather than individual functions.

## Test Structure

The tests are structured as follows:

- `conftest.py`: Pytest configuration and fixtures for the Stan Agent tests
- `test_api_integration.py`: Integration tests for the Stan Agent API

## Test Scenarios

The integration tests cover the following scenarios:

1. **Basic Greeting**: Tests a simple greeting message to ensure the agent responds correctly
2. **Contact Creation**: Tests that new contacts are properly created in the BlackPearl system
3. **Conversation Continuity**: Tests that the agent maintains conversation context across multiple messages
4. **Product Information**: Tests that the agent can provide information about products
5. **Error Handling**: Tests that the API properly handles invalid requests

## Running the Tests

To run the tests, you need a running instance of the API. You can then run the tests using pytest:

```bash
# Run all stan agent tests
pytest -xvs tests/agents/stan/

# Run a specific test
pytest -xvs tests/agents/stan/test_api_integration.py::TestStanAgentIntegration::test_basic_greeting

# Run tests with custom configuration
API_BASE_URL=http://localhost:8000 API_KEY=your-api-key pytest -xvs tests/agents/stan/
```

## Environment Variables

The tests use the following environment variables:

- `API_BASE_URL`: Base URL for the API (default: http://localhost:8000)
- `API_KEY`: API key for authentication (default: test-key)
- `API_PATH`: API path prefix (default: /api/v1)
- `AGENT_NAME`: Name of the agent to test (default: stan_agent)
- `TEST_USER_ID`: User ID to use for tests (default: 37)
- `DEFAULT_PHONE`: Default phone number for WhatsApp tests (default: 555197285829)
- `DEFAULT_NAME`: Default name for test users (default: Cezar Vasconcelos)

## Manual Testing

For manual testing, you can run the test file directly:

```bash
python tests/agents/stan/test_api_integration.py
```

This will run a subset of the tests in sequence with output printed to the console.

## Extending the Tests

To add a new test scenario:

1. Add a new test method to the `TestStanAgentIntegration` class in `test_api_integration.py`
2. Use the `call_stan_agent_api` helper function to call the API with a test message
3. Add appropriate assertions to verify the agent's response

For example:

```python
@pytest.mark.asyncio
async def test_new_scenario(self):
    """Test description."""
    # Call the API
    response = await call_stan_agent_api("Your test message")
    
    # Verify the response
    assert "expected text" in response["message"], "Error message"
``` 