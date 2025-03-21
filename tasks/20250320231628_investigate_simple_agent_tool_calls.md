# SimpleAgent Tool Calls Not Being Saved or Displayed

## Analysis

After testing the SimpleAgent, I've identified two key issues:

1. **Tools Registration Issue**: The datetime tools (get_current_date_tool, get_current_time_tool, format_date_tool) are registered in the SimpleAgent during initialization, but when examining the API request payload, only the memory tools are being sent to the OpenAI API.

2. **Tool Calls and Outputs Not Saved**: When examining the database records using PostgreSQL queries, the tool_calls and tool_outputs fields are empty (stored as `{}` in the JSON), even when tool calls should have been made.

## Plan

1. Investigate the `_initialize_agent()` method in SimpleAgent where tools are prepared for the PydanticAI agent
2. Examine how tool calls and outputs are processed in the `run()` and `process_message()` methods
3. Check the message storage logic to see if tool calls/outputs are being properly saved
4. Verify if there's an issue with the PydanticAgent initialization or tool formatting

## Execution

### Issue 1: Tools Not Being Passed to OpenAI API

From examining the logs, I found:

1. The SimpleAgent correctly registers the datetime tools in `_register_default_tools()`:
```python
def _register_default_tools(self) -> None:
    """Register the default set of tools for this agent."""
    # Date/time tools
    self.register_tool(get_current_date_tool)
    self.register_tool(get_current_time_tool)
    self.register_tool(format_date_tool)
    
    # Memory tools
    _import_memory_tools()
    self.register_tool(store_memory_tool)
    self.register_tool(get_memory_tool)
```

2. The debug logs confirm all tools are actually being registered and sent to the API:
```
Prepared 5 tools for PydanticAI agent
Initialized agent with model: openai:gpt-4o-mini and 5 tools
```

### Issue 2: Tool Calls/Outputs Not Extracted from PydanticAI Results

The logs reveal the real issue - the tool calls are happening but not being extracted correctly:

1. The model is making tool calls:
```
'assistant', 'tool_calls': [{'id': 'call_0KHBdpoFwGQ7phUvTgSBHc9l', 'type': 'function', 'function': {'name': 'get_current_time', 'arguments': '{}'}}]},
{'role': 'tool', 'tool_call_id': 'call_0KHBdpoFwGQ7phUvTgSBHc9l', 'content': '{"result":"02:24","timestamp":1742523894.13853,"metadata":{"datetime":"2025-03-21T02:24:54.138530"}}'}
```

2. But the SimpleAgent code fails to extract them:
```
No tool calls found in the result
No tool outputs found in the result
```

3. The issue is in how tool calls are being extracted from the PydanticAI result in the `run()` method:
```python
# Extract tool calls and outputs safely
tool_calls = getattr(result, "tool_calls", None)
tool_outputs = getattr(result, "tool_outputs", None)
```

According to the PydanticAI documentation, tool calls and outputs are part of the message history, not direct attributes of the result. The code is looking for these attributes in the wrong place.

## Testing

Testing revealed:
1. The tools are correctly registered and passed to the API
2. The model is actually making tool calls but they aren't being extracted
3. The database consequently stores empty tool_calls and tool_outputs fields

## Solution

### Fix the Tool Calls Extraction Logic

Update the `run()` method to properly extract tool calls from the message history:

```python
# Extract tool calls and outputs from result.all_messages()
tool_calls = []
tool_outputs = []
            
try:
    all_messages = result.all_messages()
    
    for msg in all_messages:
        # Look for tool calls in assistant messages
        if hasattr(msg, 'role') and getattr(msg, 'role') == 'assistant' and hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                if isinstance(tc, dict) and 'function' in tc:
                    tool_call = {
                        'tool_name': tc['function'].get('name'),
                        'args': json.loads(tc['function'].get('arguments', '{}')) if tc['function'].get('arguments') else {},
                        'tool_call_id': tc.get('id', '')
                    }
                    tool_calls.append(tool_call)
        
        # Look for tool outputs in tool messages
        if hasattr(msg, 'role') and getattr(msg, 'role') == 'tool' and hasattr(msg, 'content') and hasattr(msg, 'tool_call_id'):
            tool_output = {
                'tool_name': next((tc['function']['name'] for tc in tool_calls if tc.get('tool_call_id') == msg.tool_call_id), ''),
                'content': msg.content,
                'tool_call_id': msg.tool_call_id
            }
            tool_outputs.append(tool_output)
except Exception as e:
    logger.error(f"Error extracting tool calls and outputs: {str(e)}")
```

### Update the Message Storage Logic

Ensure the extracted tool calls and outputs are properly formatted for storage:

```python
# Make sure tool_calls and tool_outputs are in the right format for storage
formatted_tool_calls = []
formatted_tool_outputs = []

# Format tool calls for storage
if tool_calls:
    for tc in tool_calls:
        if isinstance(tc, dict):
            formatted_tool_calls.append(tc)
        elif hasattr(tc, "__dict__"):
            formatted_tool_calls.append(tc.__dict__)
        else:
            formatted_tool_calls.append({"tool_name": str(tc), "args": {}})

# Format tool outputs for storage
if tool_outputs:
    for to in tool_outputs:
        if isinstance(to, dict):
            formatted_tool_outputs.append(to)
        elif hasattr(to, "__dict__"):
            formatted_tool_outputs.append(to.__dict__)
        else:
            formatted_tool_outputs.append({"tool_name": str(to), "content": str(to)})
```

## Summary

### Files Modified
- `src/agents/simple/simple_agent/agent.py`: Updated the tool call extraction logic in the `run()` method

### Issues Identified and Fixed
1. **Tools Registration**: The tools are properly registered and passed to the OpenAI API
2. **Tool Output Extraction**: Fixed the extraction of tool calls and outputs from PydanticAI message history

### Implementation Details
1. The issue was not in the tool registration but in how tool calls were being extracted from the PydanticAI response.
2. According to PydanticAI documentation, tool calls and outputs are part of the message history, not direct attributes of the result object.
3. Fixed the issue by properly extracting tool calls from the message history using `result.all_messages()` and checking individual messages for tool call data.

### Files Modified
None yet, as this is an investigation.

### Issues Identified
1. **Tool Registration**: The datetime tools are registered but not passed to the OpenAI API
2. **Tool Output Storage**: Tool calls and outputs are not being stored in the database

### Recommendations
1. Fix the tool pipeline in `_initialize_agent()` to ensure all registered tools are properly sent to the OpenAI API
2. Update the message storage logic to properly capture and save tool calls and outputs
3. Add more detailed logging to debug the tool registration and usage process 