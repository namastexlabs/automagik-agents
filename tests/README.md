# Automagik Agents Test Suite

This directory contains various tests for the Automagik Agents platform, organized into different formats for different use cases.

## Test Structure

The test suite is organized as follows:

- `standalone/`: Contains standalone test scripts that can be run independently
  - `api_test_script.py`: Tests all API endpoints
  - `cli_test_script.py`: Tests CLI functionality
  - `memory_test_script.py`: Tests memory features

- `pytest/`: Contains pytest-compatible test modules
  - `test_api_endpoints.py`: Pytest version of API tests
  - `test_all.py`: Unified test runner that imports and runs the standalone scripts

## Which Test File Should I Use?

- **For CI/CD and automated testing**: Use `pytest/test_all.py` which will run all tests
- **For quick API testing**: Use `standalone/api_test_script.py` directly
- **For detailed, fixture-based API testing**: Use `pytest/test_api_endpoints.py`

## Running Tests

### Running All Tests (via pytest)

```bash
# Run all tests
python -m pytest tests/pytest/test_all.py

# Run with verbose output
python -m pytest -v tests/pytest/test_all.py

# Run with detailed output and stop on first failure
python -m pytest -vsx tests/pytest/test_all.py
```

### Running Standalone Scripts

```bash
# Run API tests
python tests/standalone/api_test_script.py

# Run with verbose output
python tests/standalone/api_test_script.py --verbose

# Run with custom API base URL
python tests/standalone/api_test_script.py --url http://localhost:8881
```

### Running Individual Pytest Modules

```bash
# Run API endpoint tests
python -m pytest tests/pytest/test_api_endpoints.py

# Run a specific test function
python -m pytest tests/pytest/test_api_endpoints.py::test_health_endpoint
```

## Troubleshooting

If the tests fail with a "duplicate key value violates unique constraint" error, it means the test is trying to create a user with an ID that already exists. The latest version of the test scripts should handle this automatically by attempting to create a user with a different email/phone.

For other issues, check the API server logs for more details.

## Adding New Tests

When adding new tests:

1. For standalone scripts: Add them to the `STANDALONE_MODULES` list in `pytest/test_all.py`
2. For pytest modules: They will be automatically discovered by pytest

## Test Configuration

Tests use the following configuration from environment variables:

- `API_BASE_URL`: Base URL for the API (default: http://localhost:8881)
- `AM_API_KEY`: API key for authentication (default: namastex-888)

You can set these in a `.env` file in the project root directory. 