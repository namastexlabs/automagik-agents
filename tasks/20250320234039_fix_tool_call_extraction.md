# Fix Tool Call Extraction in SimpleAgent

## Analysis

After a careful review of the PydanticAI documentation, I've discovered that our approach to extracting tool calls and outputs from agent results is incorrect. According to the documentation in `agent.md`, tool calls are stored in the `parts` field of message objects, not as direct attributes of the result.

The current implementation looks for `tool_calls` and `tool_outputs` as direct attributes:

```python
# Extract tool calls and outputs safely
tool_calls = getattr(result, "tool_calls", None)
tool_outputs = getattr(result, "tool_outputs", None)
```

But according to the documentation, tool calls should be found in `ModelResponse` objects with `ToolCallPart` objects in their `parts` list, and tool outputs in `ModelRequest` objects with `ToolReturnPart` objects in their `parts` list.

## Plan

1. Update the `run()` method to correctly extract tool calls and outputs from the parts of messages
2. Verify that this approach matches the PydanticAI documentation examples
3. Test the implementation with a simple time query

## Execution

Using the documentation as a guide, I need to:

1. Get all messages with `result.all_messages()`
2. Look for messages that have a `parts` attribute
3. For each part, check if it's a `ToolCallPart` (for tool calls) or a `ToolReturnPart` (for tool outputs)
4. Extract the necessary information from these parts

The code should look like:

```python
# Extract tool calls and outputs from message parts
tool_calls = []
tool_outputs = []

try:
    all_messages = result.all_messages()
    logger.info(f"Retrieved {len(all_messages)} messages from result")
    
    for msg in all_messages:
        if hasattr(msg, 'parts'):
            for part in msg.parts:
                # Check if this is a tool call part
                if hasattr(part, 'part_kind') and part.part_kind == 'tool-call':
                    tool_call = {
                        'tool_name': getattr(part, 'tool_name', ''),
                        'args': getattr(part, 'args', {}),
                        'tool_call_id': getattr(part, 'tool_call_id', '')
                    }
                    tool_calls.append(tool_call)
                    logger.info(f"Found tool call: {tool_call['tool_name']} with args: {tool_call['args']}")
                
                # Check if this is a tool return part
                if hasattr(part, 'part_kind') and part.part_kind == 'tool-return':
                    tool_output = {
                        'tool_name': getattr(part, 'tool_name', ''),
                        'content': getattr(part, 'content', ''),
                        'tool_call_id': getattr(part, 'tool_call_id', '')
                    }
                    tool_outputs.append(tool_output)
                    logger.info(f"Found tool output for {tool_output['tool_name']} with content: {tool_output['content'][:50]}...")
except Exception as e:
    logger.error(f"Error extracting tool calls and outputs: {str(e)}")
    logger.error(traceback.format_exc())
```

This matches the structure shown in the documentation examples:

```python
print(dice_result.all_messages())
"""
[
    ModelRequest(...),
    ModelResponse(
        parts=[
            ToolCallPart(
                tool_name='roll_die', args={}, tool_call_id=None, part_kind='tool-call'
            )
        ],
        model_name='gemini-1.5-flash',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
    ModelRequest(
        parts=[
            ToolReturnPart(
                tool_name='roll_die',
                content='4',
                tool_call_id=None,
                timestamp=datetime.datetime(...),
                part_kind='tool-return',
            )
        ],
        kind='request',
    ),
    ...
]
"""
```

## Testing

The correct approach should:
1. Identify tool calls as `ToolCallPart` objects with `part_kind='tool-call'`
2. Identify tool outputs as `ToolReturnPart` objects with `part_kind='tool-return'`
3. Extract the relevant attributes (tool_name, args, content, etc.)
4. Format them for storage in the database

## Summary

### Files Modified
- `src/agents/simple/simple_agent/agent.py`: Updated the tool call extraction logic in the `run()` method to correctly look for tools in message parts

### Issues Identified and Fixed
1. **Incorrect Tool Extraction**: The previous implementation was looking for tool calls as direct attributes of the result, but they're actually in the `parts` attribute of message objects.

### Implementation Details
1. Now properly iterates through all messages and their parts
2. Identifies tool calls by checking for parts with `part_kind='tool-call'`
3. Identifies tool outputs by checking for parts with `part_kind='tool-return'`
4. Extracts all the relevant information from these parts for storage and display 