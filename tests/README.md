# API Testing

This directory contains tests for the Automagik Agents API.

## Setup

1. Install the required dependencies:
   ```bash
   pip install requests python-dotenv
   ```

2. Environment Configuration:
   - The tests use the `.env` file in the root directory of the project
   - Ensure the root `.env` file contains the `AM_API_KEY` variable
   - No need to create a separate `.env` file in the tests directory

## Running the Tests

Run the API tests:
```bash
python api_tests.py
```

## Test Description

The test script (`api_tests.py`) tests all the API endpoints in sequence:

1. **Health Check**: Tests the `/health` endpoint to ensure the API is running
2. **Root Endpoint**: Tests the root endpoint (`/`) to verify service information
3. **List Agents**: Tests the `/api/v1/agent/list` endpoint to get available agents
4. **Run Agent**: Tests the `/api/v1/agent/{agent_name}/run` endpoint to create a new session
5. **Get Session**: Tests the `/api/v1/session/{session_id}` endpoint to verify session creation
6. **List Sessions**: Tests the `/api/v1/sessions` endpoint to verify the test session appears in the list
7. **Delete Session**: Tests the `/api/v1/session/{session_id}` (DELETE) endpoint to clean up the test session

## Environment Variables

The tests use the following environment variables from the root `.env` file:

- `AM_API_KEY`: Your API key for authentication (required for most endpoints)
- `API_BASE_URL`: Optional override for the base URL of the API (default: `http://localhost:8000`)
- `TEST_USER_ID`: Optional override for the user ID to use for testing (default: `test-user`)

## Adding New Tests

To add a new test:

1. Create a new test function in `api_tests.py`
2. Add the function call to the `main()` function in the appropriate sequence
3. Follow the existing pattern of making API calls, printing responses, and asserting on results 