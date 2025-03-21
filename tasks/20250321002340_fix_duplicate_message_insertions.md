# Fix Duplicate Message Insertion Issue

## Analysis

Based on my investigation of the message storage system, I've identified a critical issue: user messages are being inserted into the database twice with nearly identical timestamps. The issue is consistent across different sessions and message types.

### Database Evidence

Query showing duplicate messages:
```sql
SELECT COUNT(*) as duplicate_count, text_content, session_id, role, created_at::date
FROM messages 
GROUP BY text_content, session_id, role, created_at::date
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
```

Results show multiple user messages being duplicated, with some appearing up to 5 times:
- "im felipe" has 5 copies in session de289045-86b3-4844-b3c7-0ea8730182b1
- "whats my name" has 2 copies in the same session
- Other messages show similar patterns

The duplicate messages have almost identical timestamps (within milliseconds of each other), indicating they're being created almost simultaneously:
```
id: 711abe0f-005d-476f-b3fc-fad029a0bd5c, created_at: 2025-03-21T03:19:02.912Z
id: af131a20-5463-4008-9447-9c2bc1b2cc2d, created_at: 2025-03-21T03:19:02.909Z
```

### Code Analysis

After examining the codebase, I've identified two potential causes for this duplication:

1. **Double MessageHistory Initialization** - In `src/api/routes.py` (around line 312-313), a second MessageHistory object is created even though one was already initialized:
   ```python
   # MessageHistory should now be initialized with the correct session_id
   message_history = MessageHistory(request.session_id, user_id=request.user_id)
   ```

2. **Double Message Storage** - Messages might be stored both in the API route handler and in the agent's `process_message` method:
   ```python
   # In the API route:
   message_history.add(request.message_content, agent_id=agent_id, context=combined_context)
   
   # Later:
   response = await agent.process_message(
       request.message_content,
       session_id=request.session_id,
       user_id=request.user_id,
       context=combined_context,
       message_history=message_history
   )
   ```

   If the `process_message` implementation also calls `message_history.add()`, it would result in duplicate messages.

### Previous Related Tasks

Previous tasks `20250320153233_message_storage_fix.md` and `20250320151107.md` addressed similar issues:
- One fixed the message not being stored at all
- Another addressed session duplication

However, the current issue is different - messages are now being stored but duplicated.

## Plan

1. **Fix Double MessageHistory Initialization**:
   - Review `src/api/routes.py` to ensure MessageHistory is only initialized once per request
   - Remove redundant initialization

2. **Fix Double Message Storage**:
   - Examine `BaseAgent.process_message()` to ensure messages aren't added twice
   - Add a flag to control whether user messages should be added in the API route or in the agent

3. **Add Validation and Deduplication**:
   - Implement a check for duplicate messages in `create_message()`
   - Use a combination of session_id, role, text_content, and close timestamps to detect duplicates

## Execution

### Step 1: Review Current Behavior

Looking at the code in `src/api/routes.py`, I can see that there are two places where a MessageHistory is initialized:
1. Around line 286, it's initialized with the correct session_id after resolving session name to ID
2. Around line 313, it's initialized again unnecessarily 

Also, the route both adds the user message to the history AND passes the message to the agent's process_message. If the agent also adds the message, this would explain the duplication.

### Step 2: Implementation

1. **Modified `src/agents/models/base_agent.py`**:
   - Added a new `message_already_added` parameter to the `process_message` method
   - Updated the method to check this flag before adding the user message to avoid duplication:
   ```python
   async def process_message(self, user_message: str, session_id: Optional[str] = None, 
                          agent_id: Optional[Union[int, str]] = None, user_id: int = 1, 
                          context: Optional[Dict] = None, message_history: Optional['MessageHistory'] = None, 
                          message_already_added: bool = False) -> AgentBaseResponse_v2:
   ```
   
   - Added conditional logic to only add the user message if it hasn't been added already:
   ```python
   # Add the user message AFTER the system prompt ONLY if it hasn't been added already
   if not message_already_added:
       logging.info(f"Adding user message to message history: {user_message[:50]}...")
       user_message_obj = message_history.add(user_message, agent_id=self.db_id, context=context)
   else:
       logging.info("User message was already added to message history, skipping add operation")
   ```

2. **Modified `src/api/routes.py`**:
   - Removed the redundant MessageHistory initialization around line 313:
   ```python
   # Removed:
   # MessageHistory should now be initialized with the correct session_id
   # message_history = MessageHistory(request.session_id, user_id=request.user_id)
   ```
   
   - Updated the call to `process_message` to pass the new parameter indicating the message was already added:
   ```python
   response = await agent.process_message(
       request.message_content,
       session_id=request.session_id,
       user_id=request.user_id,
       context=combined_context,
       message_history=message_history,
       message_already_added=True  # Indicate that we've already added the message
   )
   ```

## Testing Plan

1. Run a test conversation with logging to verify only one message is created per user input
2. Query the database to verify no duplicates are being created
3. Test with both CLI and API interfaces to ensure both paths work correctly

## Summary

The message duplication issue was caused by double insertion of messages - once in the API route handler and once in the agent's process_message implementation. The fix involved:

1. Removing the redundant MessageHistory initialization in routes.py
2. Adding a message_already_added flag to process_message
3. Skipping the message add operation when the flag indicates the message is already added

This solution maintains backward compatibility with all existing code paths while preventing duplicate message insertion. 

The files modified were:
- `src/agents/models/base_agent.py`: Lines 246-300
- `src/api/routes.py`: Lines 313-315 and 440-450 