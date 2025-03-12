# Automagik Agents

## 🚀 From Ideas to Production in Minutes

Automagik Agents is a powerful deployment layer over Pydantic AI that accelerates your AI agent development from concept to production. Born from our daily work at Namastex Labs, it provides a reliable, tested foundation for rapidly building, deploying, and managing AI agents with advanced capabilities like persistent memory and tool integration.

We built Automagik because we needed to save time while creating high-quality, production-ready agents. By focusing on standardized patterns, best practices, and reusable components, Automagik lets you create sophisticated AI assistants in minutes instead of days.

## 🌟 Features

- **Extensible Agent System**
  - Template-based agent creation
  - Built-in templates: Simple Agent, Sofia Agent, Notion Agent, and Discord Agent
  - Easy-to-use CLI for creating new agents
  - Automatic tool registration and management

- **Powerful API Integration**
  - FastAPI-based RESTful endpoints
  - Session management with conversation history
  - Structured request/response models
  - Built-in authentication and CORS support
  - Health monitoring and version tracking

- **Advanced Memory System**
  - Persistent conversation history
  - Session-based memory management
  - Tool call and output tracking
  - Structured message storage
  - Agent-specific memories with customizable access controls
  - Dynamic memory injection via {{variable}} templating
  - Memory creation, reading, and updating tools

- **Built-in Templates**
  - **Simple Agent**: Basic chat functionality with memory tools
  - **Sofia Agent**: Memory-enhanced agent with comprehensive knowledge management and dynamic prompt templating
  - **Notion Agent**: Full Notion integration with database management
  - **Discord Agent**: Discord integration for managing servers, channels, and messages

## 🚀 Quick Start

1. **Installation**
   ```bash
   git clone https://github.com/namastexlabs/automagik-agents
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```

2. **Environment Setup**
   ```bash
   # Copy example environment file
   cp .env-example .env

   # Configure required variables
   AM_API_KEY=your_api_key_here
   AM_HOST=0.0.0.0
   AM_PORT=8881
   OPENAI_API_KEY=your_openai_key_here
   OPENAI_MODEL=openai:gpt-4o-mini  # or your preferred model
   
   # For Notion agent (optional)
   NOTION_TOKEN=your_notion_token
   
   # For Discord agent (optional)
   DISCORD_BOT_TOKEN=your_discord_token
   ```

3. **Create a Custom Agent**
   ```bash
   # Create from simple template
   automagik-agents agent create agent --name my_agent --template simple_agent

   # Create from Notion template
   automagik-agents agent create agent --name my_notion_agent --template notion_agent
   ```

4. **Start the API Server**
   ```bash
   automagik-agents api start --reload
   ```

## 💡 Usage Examples

### CLI Commands

1. **Interactive Chat** - Useful when developing / debugging without an UI.
   ```bash
   # Start a chat session with an agent
   automagik-agents agent chat start --agent my_agent
   
   # List available agents for chat
   automagik-agents agent chat list
   ```

2. **Agent Mode** - We made this so that we can provide another agent with tools to test the new agents under development.
   ```bash
   # Run a single message through an agent
   automagik-agents agent run message --agent my_agent --message "What time is it?"
   
   # Run with session continuity
   automagik-agents agent run message --agent my_agent --session my_session --message "Remember this information"
   automagik-agents agent run message --agent my_agent --session my_session --message "What did I ask you to remember?"
   ```

3. **Debug Mode**
   ```bash
   # Enable debug mode for detailed output
   automagik-agents --debug agent run message --agent my_agent --message "Debug information"
   ```

### API Endpoints

1. **Health Check**
   ```bash
   curl http://localhost:8881/health
   ```

2. **Run an Agent**
   ```bash
   # Simple agent
   curl -X POST http://localhost:8881/api/v1/agent/simple_agent/run \
     -H "X-API-Key: your_api_key" \
     -H "Content-Type: application/json" \
     -d '{
       "message_content": "What time is it?",
       "session_name": "optional_session_name"
     }'
   ```

3. **Memory Management**
   ```bash
   # Create a memory
   curl -X POST http://localhost:8881/api/v1/memories \
     -H "X-API-Key: your_api_key" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "user_preference",
       "description": "User color preference",
       "content": "The user prefers blue",
       "agent_id": 1,
       "read_mode": "tool_calling",
       "access": "write"
     }'
     
   # Get a memory
   curl http://localhost:8881/api/v1/memories/{memory_id} \
     -H "X-API-Key: your_api_key"
     
   # List memories
   curl http://localhost:8881/api/v1/memories \
     -H "X-API-Key: your_api_key"
   ```

4. **Session Management**
   ```bash
   # Get session history
   curl http://localhost:8881/api/v1/sessions/{session_id_or_name} \
     -H "X-API-Key: your_api_key"

   # Delete session
   curl -X DELETE http://localhost:8881/api/v1/sessions/{session_id_or_name} \
     -H "X-API-Key: your_api_key"
   ```

### Dynamic Memory System

Automagik features a powerful dynamic memory system that can inject variable content into agent prompts:

1. **Template Variables in Prompts**
   ```python
   # Example prompt with template variables
   AGENT_PROMPT = (
     """
     You are an AI assistant with the following traits:
     - Name: {{assistant_name}}
     - Personality: {{personality}}
     - Knowledge areas: {{knowledge_areas}}
     
     Current user preferences: {{user_preferences}}
     """
   )
   ```

2. **Creating Memories for Template Variables**
   ```bash
   # Create memories that will be injected into prompts
   curl -X POST http://localhost:8881/api/v1/memories \
     -H "X-API-Key: your_api_key" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "personality",
       "description": "Agent personality traits",
       "content": "friendly, helpful, knowledgeable",
       "agent_id": 3,
       "read_mode": "system_prompt",
       "access": "read"
     }'
   ```

3. **How It Works**
   - Template variables using `{{variable_name}}` syntax are identified in prompts
   - The system automatically fetches memory values with matching names
   - Values are injected into the prompt at runtime
   - Special variables like `{{run_id}}` are handled automatically
   - Memory values can be updated via API or agent tools
   - This allows for dynamic agent personality and knowledge without redeployment

### Creating Custom Agents

1. **Create Agent Using CLI**
   ```bash
   automagik-agents agent create agent --name custom_agent --template simple_agent
   ```

2. **Customize Agent Files**
   - Edit `src/agents/simple/custom_agent/prompts/prompt.py` for system prompts
   - Add template variables with `{{variable_name}}` syntax for dynamic content
   - Modify `src/agents/simple/custom_agent/agent.py` for behavior and tool registration
   - Update `src/agents/simple/custom_agent/__init__.py` for configuration

3. **Register Tools**
   ```python
   def register_tools(self):
       """Register custom tools with the agent."""
       # Register built-in memory tools
       from src.tools.memory_tools import read_memory, create_memory, update_memory
       self.agent.tool(read_memory)
       self.agent.tool(create_memory)
       self.agent.tool(update_memory)
       
       # Register custom tools
       self.agent.tool(your_custom_tool)
   ```

### Testing

Run all tests including memory, API, and CLI tests:
```bash
python tests/run_all_tests.py
```

Run specific test categories:
```bash
# Run only memory tests
python tests/run_all_tests.py --memory --no-api --no-cli

# Run with verbose output
python tests/run_all_tests.py --verbose
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 API Documentation

Explore the complete API documentation at `/api/v1/docs` when running the server.

## 🗺️ Roadmap

- **Graph Agents**: Advanced agent orchestration and workflows
- **Seamless Deployment**: Built-in deployment solutions in namastex/automagik for agent automation
- **Heartbeat Mode**: Our proprietary method to keep agents alive 24hrs doing tasks
- **MCP Integration**: Model Context Protocol for easier tool reusing
- **Support for Other Agent Frameworks**: Expand compatibility across the ecosystem
- **Smart Context Management**: Optimal handling of large context windows

Automagik Agents is and will always be open source. Since this is our daily work tool, we provide high priority maintenance and updates.
