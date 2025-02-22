# Automagik Agents

A collection of AI agents powered by Pydantic AI and exposed through FastAPI endpoints. This project provides a flexible framework for deploying and interacting with different types of AI agents through a RESTful API.

## Features

- **Multiple Agent Support**: 
  - Simple Agent: Handles basic queries and time-related operations
  - Notion Agent: Manages Notion databases and workspaces
- **FastAPI Integration**: RESTful API endpoints for agent interaction
- **Health Monitoring**: Built-in health check endpoint with version tracking
- **Message History**: Maintains conversation context across interactions
- **Structured Responses**: Standardized response format using Pydantic models
- **Security**: API key authentication for protected endpoints
- **CORS Support**: Configurable CORS middleware for cross-origin requests

## Technical Architecture

### Core Components

1. **FastAPI Application**
   - Health check endpoint (`/health`)
   - Agent endpoints (`/agent/{agent_type}/run`)
   - Standardized request/response models

2. **Agent Framework**
   - Base agent implementation with common functionality
   - Specialized agents (Simple, Notion) with specific capabilities
   - Message history management
   - Tool registration system

3. **Response Models**
   - `AgentBaseResponse`: Standard response format
   - `HistoryModel`: Message history serialization
   - `MessageModel`: Individual message representation

### Dependencies

- `fastapi`: Web framework for building APIs
- `pydantic-ai`: Core AI agent framework
- `notion-client`: Official Notion API client (for Notion agent)
- `uvicorn`: ASGI server for running the API

## Usage

1. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env-example .env
   
   # Edit .env and set your values
   AUTOMAGIK_AGENTS_API_KEY=your_api_key_here  # Required for authentication
   NOTION_TOKEN=your_notion_integration_token  # Only needed for Notion agent
   ```

2. Install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

3. Run the API server:
   ```bash
   uvicorn src.main:app --reload
   ```

4. Interact with the agents:

   Health Check (no authentication required):
   ```bash
   curl http://localhost:8000/health
   ```

   Simple Agent (requires API key):
   ```bash
   curl -X POST http://localhost:8000/agent/simple/run \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key_here" \
     -d '{"message_input": "What time is it?", "context": {}}'
   ```

   Notion Agent (requires API key):
   ```bash
   curl -X POST http://localhost:8000/agent/notion/run \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key_here" \
     -d '{"message_input": "List my databases", "context": {}}'
   ```

## Development

### Agent Implementation

Each agent follows a standard structure:
- Initialization with configuration
- Tool registration
- Message processing
- Response generation

### Response Processing

All agent responses are processed through:
1. Message history management
2. Response serialization
3. Error handling
4. Tool output collection

### Security

The API uses API key authentication for protected endpoints:
- API key must be provided in the `X-API-Key` header
- Key is configured via `AUTOMAGIK_AGENTS_API_KEY` environment variable
- Health check endpoint remains public
- Invalid or missing API keys return 401 Unauthorized

## Future Enhancements

- Additional agent types
- Enhanced tool management system
- Authentication and rate limiting
- Response caching
- Batch operation support
