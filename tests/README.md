# Automagik Agents Tests

This directory contains automated tests for the Automagik Agents system. The tests ensure that the API, CLI, and memory features are functioning correctly, handling both valid and invalid requests properly, and maintaining data consistency.

## Directory Structure

```
tests/
├── run_all_tests.py           # Main entry point for running all tests
├── requirements-test.txt      # Test dependencies
├── standalone/                # Simple standalone test scripts
│   ├── api_test_script.py     # Self-contained API test script
│   ├── cli_test_script.py     # CLI commands test script
│   └── memory_test_script.py  # Agent memory capabilities test script
└── pytest/                    # Pytest-based tests
    ├── test_all.py            # Unified pytest runner for all tests
    └── test_api_endpoints.py  # API endpoint tests with pytest fixtures
```

## Running the Tests

### Using the unified test runner (recommended)

The `run_all_tests.py` script provides a unified interface for running all test types:

```bash
# Run all tests with pytest
python tests/run_all_tests.py

# Run only specific test types
python tests/run_all_tests.py --api --no-cli --no-memory

# Run with verbose output
python tests/run_all_tests.py --verbose

# Generate HTML, JSON, and JUnit reports
python tests/run_all_tests.py --html --json --junit

# Run in standalone mode (without pytest)
python tests/run_all_tests.py --standalone

# Specify output directory for reports
python tests/run_all_tests.py --output-dir=my_test_reports
```

### Using pytest directly

You can also run tests directly with pytest:

```bash
# Run all tests with the unified runner
pytest tests/pytest/test_all.py

# Run specific test types
pytest tests/pytest/test_all.py -k "test_api or test_cli"

# Run API endpoint tests only
pytest tests/pytest/test_api_endpoints.py
```

### Running standalone tests directly

During development, you can run the standalone scripts directly:

```bash
# Run the standalone API tests
python tests/standalone/api_test_script.py

# Run the CLI tests
python tests/standalone/cli_test_script.py

# Run the memory tests
python tests/standalone/memory_test_script.py
```

## Available Test Scripts

1. **API Tests**:
   - **Standalone** (`tests/standalone/api_test_script.py`): Tests API endpoints
   - **Pytest** (`tests/pytest/test_api_endpoints.py`): API tests with pytest fixtures

2. **CLI Tests** (`tests/standalone/cli_test_script.py`):
   - Tests all CLI commands and subcommands
   - Verifies expected outputs and error handling
   - Available through unified pytest runner

3. **Memory Tests** (`tests/standalone/memory_test_script.py`):
   - Tests agent memory capabilities through sequential conversations
   - Verifies context retention and conversation flow
   - Available through unified pytest runner

4. **Unified Runner** (`tests/pytest/test_all.py`):
   - Runs all standalone tests through pytest
   - Provides consistent reporting and CI integration
   - Imports and executes the standalone scripts

## Test Dependencies

Install the test dependencies with:

```bash
pip install -r tests/requirements-test.txt
```

## Configuration

Tests use the following environment variables (which can be set in the `.env` file):

- `API_BASE_URL`: The base URL of the API (default: http://localhost:8881)
- `AM_API_KEY`: The API key for authentication

## Test Coverage

The tests cover:

1. **System Endpoints**:
   - Health check
   - Root endpoint
   - OpenAPI schema
   - Swagger and ReDoc documentation

2. **User Management**:
   - Create users
   - Get users by ID, email, and phone number
   - Update user emails and data
   - List users
   - Delete users

3. **Agent Management**:
   - List available agents
   - Run an agent with a new session

4. **Session Management**:
   - Get session by ID
   - List all sessions
   - Delete sessions

5. **CLI Commands**:
   - Global options (--help, --version)
   - API commands (auth, config)
   - Database commands (init, reset)
   - Agent chat and run commands
   - Agent creation and management

6. **Agent Memory**:
   - Context retention across multiple messages
   - Information recall
   - Conversation flow maintenance

## Test Reports

When using pytest mode, various report formats are available:

- **HTML reports**: `--html`
- **JUnit XML**: `--junit`
- **JSON**: `--json`

## Continuous Integration

These tests are designed to be run in CI/CD pipelines to ensure system reliability.

Example GitHub Actions workflow:

```yaml
name: System Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r tests/requirements-test.txt
      - name: Run all tests
        run: |
          python tests/run_all_tests.py --html --json --junit
      - name: Upload test reports
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: test_reports/
``` 