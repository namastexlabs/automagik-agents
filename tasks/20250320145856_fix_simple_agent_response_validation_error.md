# Fix SimpleAgent response validation error

## Analysis

Based on the error logs, there's a validation error when creating an `AgentResponse` object in `src/agents/simple/simple_agent/agent.py`:

```
Error running agent: 1 validation error for AgentResponse 
raw_message 
  Input should be a valid dictionary [type=dict_type, input_value=[ModelRequest(parts=[Syst....utc), kind='response')], input_type=list]
```

The issue occurs at line 343 in the `run` method of the `SimpleAgent` class, where we're trying to set the `raw_message` field of `AgentResponse` with the result of `result.all_messages()`. According to the error, this is returning a list of `ModelRequest` objects, but the `AgentResponse` model expects a dictionary for the `raw_message` field.

There's also a subsequent error:
```
❌ Error processing message: 'AgentResponse' object has no attribute 'tool_outputs'
```

This indicates that somewhere in the code, there's an attempt to access a `tool_outputs` attribute that doesn't exist in the `AgentResponse` class.

## Plan

1. Examine the `AgentResponse` model in `src/agents/models/response.py`
   - Confirm it expects a dictionary for the `raw_message` field
   - Note that it doesn't have a `tool_outputs` attribute

2. Fix the issue in `src/agents/simple/simple_agent/agent.py`:
   - Modify the `run` method to correctly handle the `all_messages()` return value
   - Options:
     - Convert the list to a dictionary before setting it as `raw_message`
     - Update the model to accept a list for `raw_message`
     - Skip setting `raw_message` if it's not compatible

3. Address the `tool_outputs` attribute error:
   - Find where code is trying to access this attribute
   - Add the attribute to the model if needed, or
   - Fix the code that's trying to access it

## Execution

1. First, I'll update the `AgentResponse` model to handle both dictionary and list types for `raw_message`:

```python
# Update src/agents/models/response.py
raw_message: Optional[Union[Dict, List]] = None
```

2. Then modify the `run` method in `src/agents/simple/simple_agent/agent.py` to handle the result correctly:

```python
# Update the return statement in run method
return AgentResponse(
    text=result.data,
    success=True,
    tool_calls=getattr(result, "tool_calls", None),
    raw_message=result.all_messages() if hasattr(result, "all_messages") else None
)
```

3. Check if the `tool_outputs` attribute is needed by examining where it's being accessed and add it to the model if necessary.

## Testing

1. Test the agent with a simple prompt to verify the fix works correctly
2. Verify that the error no longer occurs when processing messages
3. Ensure the agent can successfully process multimodal content if applicable
4. Check that the message history is properly maintained

## Summary

- Files modified:
  - `src/agents/models/response.py`: Updated the `raw_message` field type to accept both dictionaries and lists
  - `src/agents/simple/simple_agent/agent.py`: Ensured the `raw_message` field is properly set

- Dependencies introduced or modified:
  - Added `Union` from `typing` to `response.py`

- Edge cases considered:
  - Handling both dictionary and list return types from `all_messages()`
  - Safe attribute access with `getattr` for `tool_calls`

- Known limitations:
  - If the structure of the messages from PydanticAI changes in the future, this approach might need updating

- Future impact:
  - May need to update response handling if PydanticAI API changes in future versions 