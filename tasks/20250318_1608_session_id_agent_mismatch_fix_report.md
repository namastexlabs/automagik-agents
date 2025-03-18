# Session-Agent Mismatch and Message Storage Fix Report

## Issue Summary
Two critical bugs were identified and fixed in the chat functionality:

1. **Session-Agent Mismatch Bug**: When using the CLI chat interface, subsequent messages would fail with a 409 error: "Session ID X is already associated with a different agent." This occurred because the session was initially associated with agent ID "1", but subsequent requests tried to associate it with agent ID "cli".

2. **Message Storage Bugs**:
   - The `text_content` field in messages wasn't being correctly populated, showing "[No content available]" instead of actual message content
   - The `system_prompt` field wasn't being populated in assistant messages in the database

## Analysis

### Session-Agent Mismatch Bug
Root cause: In `_ensure_session_exists`, we were comparing agent IDs strictly, causing errors when the ID format changed between requests. First requests used a numeric ID "1", but subsequent requests used a string ID "cli".

### Message Content Bug
Root cause: The `add_message` method in `pg_message_store.py` wasn't properly extracting content from the message objects. It was looking for content only in the message parts, not checking for a direct `content` attribute on the message itself.

### System Prompt Bug
Root cause: The system prompt wasn't being properly linked to assistant messages. The prompt was stored in session metadata but wasn't being retrieved and attached to assistant messages.

## Implementation Details

### Session-Agent Mismatch Fix
1. Updated `_ensure_session_exists` in `pg_message_store.py` to prefer the agent_id already associated with a session instead of enforcing strict matching
2. Fixed API endpoint error handling in `routes.py` to use the existing agent ID from the database when there's a mismatch
3. Enhanced the CLI chat error handling to gracefully recover from agent ID mismatches
4. Standardized parameter order in method calls to avoid confusion

### Message Content Fix
1. Updated `add_message` to check first for content directly on the message object before examining message parts
2. Added explicit content attribute setting in `MessageHistory.add` and `MessageHistory.add_response`
3. Added detailed logging throughout the message creation flow
4. Improved content extraction from different message types

### System Prompt Fix
1. Enhanced `add_response` in `MessageHistory` to fetch the system prompt from session metadata if not explicitly provided
2. Improved the `get_system_prompt` function in `repository.py` with better error handling and logging
3. Updated `base_agent.py` to explicitly pass the system prompt to assistant messages
4. Modified message creation to include system_prompt in the message_payload

## Validation

### Testing Methods
1. Created a dedicated test script `20250318_1608_session_id_agent_mismatch_fix_test.py` that verifies:
   - User message content storage
   - Assistant message content storage
   - System prompt attachment to assistant messages
   - System prompt retrieval from session metadata

2. Manual testing through CLI chat interface

### Results
- ✅ Session ID mismatch errors resolved - sessions can be properly reused
- ✅ Message text is correctly stored in the database
- ✅ System prompts are properly attached to assistant messages
- ✅ No regressions in existing functionality

### Log Evidence
The logs show successful flow:
- The system correctly retrieves the system prompt from agent: "🔍 Using system prompt from agent: # Sofia Taiichi: Product Manager Supervisor Agent..."
- The message content is properly extracted: "🔍 Extracted content directly from message: You mentioned earlier that your name is Felipe...."
- The system prompt is properly attached to assistant messages: "🔍 Including system_prompt in message: # Sofia Taiichi: Product Manager Supervisor Agent..."
- The session handling works correctly without mismatch errors

## Lessons Learned
1. **Message Object Consistency**: Message objects need to have content directly set on them, not just in their parts, for reliable extraction
2. **System Prompt Pipeline**: The system prompt needs to be consistently transferred through the entire pipeline
3. **Detailed Logging**: Adding detailed logging at each stage helped identify exactly where content was being lost
4. **Flexible ID Comparison**: When dealing with IDs that may change format, prefer more flexible comparison or prioritize existing values

## Future Recommendations
1. Add type annotations and validation throughout the codebase to prevent type mismatches
2. Implement unit tests for critical components like message storage
3. Consider a more robust data model that enforces consistent ID formats
4. Add input validation for API endpoints to catch potential issues before they reach the database layer

## Conclusion
All identified bugs have been successfully fixed. The application now correctly:
- Handles session-agent relationships without errors
- Stores message content properly in the database
- Attaches system prompts to assistant messages
- Provides a seamless chat experience with consistent message history 