# Automagik Agents

A toolkit for quickly building and deploying AI agents using the Pydantic AI framework. Create custom agents from templates, expose them through a RESTful API, and manage conversations with built-in memory and tool support. Perfect for teams looking to rapidly prototype and deploy AI agents with standardized patterns and best practices.

## 🌟 Features

- **Extensible Agent System**
  - Template-based agent creation
  - Built-in templates: Simple Agent and Notion Agent
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

- **Built-in Templates**
  - **Simple Agent**: Basic chat functionality with datetime tools
  - **Notion Agent**: Full Notion integration with database management

## 🚀 Quick Start

1. **Installation**
   ```bash
   pip install automagik-agents
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
   ```

3. **Create a Custom Agent**
   ```bash
   # Create from simple template
   automagik-agents create-agent -n my_agent -t simple_agent

   # Create from Notion template
   automagik-agents create-agent -n my_notion_agent -t notion_agent
   ```

4. **Start the API Server**
   ```bash
   automagik-agents api start --reload
   ```

## 💡 Usage Examples

### API Endpoints

1. **Health Check**
   ```bash
   curl http://localhost:8881/health
   ```

2. **Run an Agent**
   ```bash
   # Simple agent
   curl -X POST http://localhost:8881/agent/simple_agent/run \
     -H "X-API-Key: your_api_key" \
     -H "Content-Type: application/json" \
     -d '{
       "message_input": "What time is it?",
       "session_id": "optional_session_id"
     }'

   # Notion agent
   curl -X POST http://localhost:8881/agent/notion_agent/run \
     -H "X-API-Key: your_api_key" \
     -H "Content-Type: application/json" \
     -d '{
       "message_input": "List my databases",
       "session_id": "optional_session_id"
     }'
   ```

3. **Session Management**
   ```bash
   # Get session history
   curl http://localhost:8881/session/your_session_id \
     -H "X-API-Key: your_api_key"

   # Delete session
   curl -X DELETE http://localhost:8881/session/your_session_id \
     -H "X-API-Key: your_api_key"
   ```

### Creating Custom Agents

1. **Create Agent Template**
   ```bash
   automagik-agents create-agent -n custom -t simple_agent
   ```

2. **Customize Agent Files**
   - Edit `src/agents/custom_agent/prompts.py` for system prompts
   - Modify `src/agents/custom_agent/agent.py` for behavior
   - Update `src/agents/custom_agent/__init__.py` for configuration

3. **Register Tools**
   ```python
   def register_tools(self):
       """Register custom tools with the agent."""
       self.agent.tool(your_custom_tool)
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
