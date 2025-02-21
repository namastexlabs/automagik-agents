# Sofia - Notion AI Assistant

Sofia is an intelligent AI assistant that helps manage Notion databases through natural language conversations. Built using the Pydantic AI framework, Sofia provides a friendly and intuitive interface for interacting with Notion workspaces.

## Features

- **Natural Language Interface**: Communicate with Sofia in plain language to manage your Notion databases
- **Database Operations**: 
  - List available databases
  - Query database contents with filters
  - Create new pages
  - Update existing pages
  - Delete/archive pages
- **Contextual Memory**: Sofia maintains conversation history to provide contextual responses
- **Rich Response Format**: Responses include both reasoning and final messages

## Technical Architecture

### Core Components

1. **NotionAgent Class**
   - Main interface for handling user commands
   - Manages conversation context and database cache
   - Processes responses through the Pydantic AI agent

2. **NotionTools Class**
   - Handles direct interactions with Notion API
   - Implements database operations (list, query, create, update, delete)

3. **Agent Response Model**
   - Structured response format using Pydantic
   - Fields:
     - `reasoning`: Optional explanation of the agent's thought process
     - `message`: The actual response to show to the user

### Dependencies

- `pydantic-ai`: Core AI agent framework
- `notion-client`: Official Notion API client
- `rich`: Terminal formatting and display
- `logfire`: Logging system

## Usage

1. Set up environment variables:
   ```bash
   NOTION_TOKEN=your_notion_integration_token
   ```

2. Run the agent:
   ```bash
   python notion_agent.py
   ```

3. Start interacting with Sofia using natural language commands:
   ```
   > list databases
   > show items in Tasks database
   > create new task with title "Review PR"
   ```

## Development

### Agent Initialization

The agent is initialized with:
- Model: GPT-4 Mini
- Result Type: AgentResponse
- System Prompt: Defines Sofia's personality and response format

### Response Processing

Responses are processed through multiple stages:
1. Command parsing
2. Agent execution
3. Response validation
4. Memory storage
5. Display formatting

### Error Handling

- Comprehensive error catching for API calls
- Graceful fallbacks for failed operations
- Detailed logging for debugging

## Future Enhancements

- Support for more complex database operations
- Enhanced memory management
- Multi-database relationship handling
- Custom database templates
- Batch operations support
