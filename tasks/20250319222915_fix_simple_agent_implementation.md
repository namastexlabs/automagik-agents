# Fix SimpleAgent Implementation According to PydanticAI Documentation

## Analysis

After examining the SimpleAgent implementation and the PydanticAI documentation in `simple_agent_resources`, I've identified several critical issues causing the SimpleAgent to not be properly detected and initialized. The SimpleAgent implementation attempts to use the PydanticAI library but isn't following the prescribed patterns in the documentation, leading to import errors and initialization failures.

Key issues identified:

1. **Incorrect Import Structure**: The current SimpleAgent code is trying to import classes from incorrect locations in the PydanticAI package. According to the documentation, PydanticAI has a specific import structure that must be followed.

2. **Improper Agent Initialization**: The SimpleAgent isn't properly initializing BaseAgent with the required `system_prompt` parameter, which is mandatory according to the documentation.

3. **Inconsistent Tool Registration**: The way tools are registered and used doesn't align with the documentation examples.

4. **Message Handling Mismatch**: Chat history and message handling don't follow the patterns described in the documentation.

## Plan

1. **Fix PydanticAI Imports**:
   - Update imports in `src/agents/simple/simple_agent/agent.py` to match the correct PydanticAI package structure
   - Ensure compatibility with pydantic-ai v0.0.42

2. **Correct Agent Initialization**:
   - Implement proper initialization with system_prompt as required by BaseAgent
   - Ensure dependencies are passed correctly

3. **Update Tool Registration and Handler Methods**:
   - Implement tool registration following the documentation patterns
   - Ensure run methods follow the documented approach

4. **Fix Message and Chat History Handling**:
   - Update to match the patterns in the chat_history.md documentation

## Execution

### Step 1: Fix PydanticAI Imports

According to the documentation, the correct import structure for PydanticAI is different from what's currently implemented. The imports should be updated to:

```python
from pydantic_ai import Agent as PydanticAgent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import UsageLimits
from pydantic_ai.tools import Tool as PydanticTool
from pydantic_ai.tools import RunContext
```

The message-related classes should be imported from the correct modules:

```python
# Based on documentation, correct the imports to:
from pydantic_ai.messages import ModelMessage
from pydantic_ai.content import TextContent, ImageContent, DocumentContent, AudioContent
# Or possibly from pydantic_ai directly if they've been moved
```

### Step 2: Correct Agent Initialization

The SimpleAgent's `__init__` method needs to be updated to properly initialize the BaseAgent with system_prompt:

```python
def __init__(self, dependencies: SimpleAgentDependencies) -> None:
    """Initialize the SimpleAgent.
    
    Args:
        dependencies: SimpleAgentDependencies object with configuration
    """
    # Extract system prompt from dependencies or use default
    system_prompt = dependencies.get_system_prompt() if hasattr(dependencies, 'get_system_prompt') else "You are a helpful assistant."
    
    # Initialize BaseAgent with correct parameters
    super().__init__(dependencies, system_prompt)
    
    self.dependencies = dependencies
    
    # Initialize variables
    self._agent_instance: Optional[PydanticAgent] = None
    self._registered_tools: Dict[str, Callable] = {}
    
    # Register default tools
    self._register_default_tools()
```

### Step 3: Update Tool Registration

Based on the documentation, tools should be registered using the PydanticAI Agent's tool decorator pattern:

```python
def _register_default_tools(self) -> None:
    """Register the default set of tools for this agent."""
    # Register tools following the PydanticAI pattern
    
    # Example:
    # @self._agent_instance.tool
    # async def get_current_date(ctx: RunContext[SimpleAgentDependencies]) -> str:
    #     """Get the current date."""
    #     return date.today().isoformat()
    
    # Register standard tools provided by PydanticAI
    self.register_tool(web_search_tool)
    self.register_tool(get_current_date_tool)
    # etc.
```

The `register_tool` method should be updated to use the correct PydanticAI approach:

```python
def register_tool(self, tool_func: Callable) -> None:
    """Register a tool with the agent.
    
    Args:
        tool_func: The tool function to register
    """
    name = getattr(tool_func, "__name__", str(tool_func))
    self._registered_tools[name] = tool_func
```

### Step 4: Update run methods

The `run` method needs to be updated to follow the PydanticAI patterns:

```python
async def run(self, 
             input_text: str, 
             multimodal_content: Optional[Dict[str, Any]] = None,
             system_message: Optional[str] = None) -> AgentResponse:
    """Run the agent on the input text.
    
    Args:
        input_text: Text input from the user
        multimodal_content: Optional multimodal content dictionary
        system_message: Optional system message for this run
        
    Returns:
        AgentResponse object with result and metadata
    """
    # Initialize agent if not done already
    await self._initialize_agent()
    
    # Get message history or create new if not exists
    message_history = self.dependencies.get_message_history()
    
    # Create agent input
    agent_input = input_text
    if multimodal_content:
        # Handle multimodal content according to documentation
        agent_input = [input_text]
        for content_type, content in multimodal_content.items():
            # Add appropriate content type
            if content_type == "image":
                agent_input.append(ImageContent(url=content))
            # Add other content types as needed
    
    # Run the agent with correct parameters
    try:
        result = await self._agent_instance.run(
            agent_input,
            message_history=message_history,
            system_prompt=system_message if system_message else None
        )
        
        # Format the response according to our expected format
        return AgentResponse(
            text=result.data,
            success=True,
            tool_calls=result.tool_calls if hasattr(result, "tool_calls") else None,
            raw_message=result.all_messages() if hasattr(result, "all_messages") else None
        )
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        return AgentResponse(
            text="An error occurred while processing your request.",
            success=False,
            error_message=str(e)
        )
```

## Testing

To verify that the SimpleAgent implementation is working correctly:

1. Run the agent discovery process to ensure SimpleAgent is detected:
```
PYTHONPATH=/root/automagik-agents python3 -c "from src.agents.models.agent_factory import AgentFactory; AgentFactory.discover_agents(); print(f'Available agents: {AgentFactory.list_available_agents()}')"
```

2. Test the SimpleAgent with a basic query to verify functionality:
```python
from src.agents.simple.simple_agent import create_simple_agent

agent = create_simple_agent()
result = agent.run_sync("Tell me a joke")
print(result.text)
```

3. Test multimodal capabilities if implemented:
```python
result = agent.run_sync("What's in this image?", multimodal_content={"image": "https://example.com/image.jpg"})
print(result.text)
```

## Summary

### Files to Modify
- `src/agents/simple/simple_agent/agent.py`: Fix imports, update initialization, tool registration, and run methods
- `src/agents/simple/simple_agent/__init__.py`: Update default agent creation

### Dependencies Introduced/Modified
- Ensuring compatibility with pydantic-ai v0.0.42, using the correct structure based on documentation

### Edge Cases Considered
- Handling of both text-only and multimodal inputs
- Proper error handling for initialization and runtime errors
- Backward compatibility with existing code using the agent

### Known Limitations
- The implementation is dependent on the specific structure of pydantic-ai v0.0.42
- Some advanced features in the documentation may not be implemented yet

### Potential Future Impact Points
- Any updates to PydanticAI will require corresponding updates to the SimpleAgent
- Adding additional tool types would require extending the registration process 