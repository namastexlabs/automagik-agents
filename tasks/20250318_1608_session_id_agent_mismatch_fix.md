# Task: Fix Session-Agent Mismatch and Message Storage Bugs [COMPLETED]

## Problem Description
Two issues have been identified in the chat functionality:

1. **Session-Agent Mismatch Bug**: When using the CLI chat interface, the second message fails with a 409 error: "Session ID X is already associated with a different agent." This occurs because the session is initially associated with agent ID "1", but subsequent requests try to associate it with agent ID "cli".

2. **Message Storage Bugs**:
   - The `text_content` field in messages is not being correctly populated, showing "[No content available]"
   - The `system_prompt` field is not being populated in assistant messages in the database

## Requirements
- ✅ Fix the session management bug so sessions can be properly reused between requests
- ✅ Fix the text_content issue to store the actual message content in the database
- ✅ Ensure system_prompt is correctly linked to assistant messages in the database
- ✅ Maintain backward compatibility with existing sessions
- ✅ Keep the feature of automatically reusing existing sessions by name

## Files Modified
1. `src/memory/pg_message_store.py` - Fixed the `_ensure_session_exists` method and message storage
2. `src/api/routes.py` - Updated session handling in the `run_agent` endpoint
3. `src/cli/agent/run.py` - Fixed consistent agent_id parameter passing
4. `src/memory/message_history.py` - Fixed how messages are processed and content is extracted
5. `src/agents/models/base_agent.py` - Ensured system_prompt is properly passed to messages
6. `src/db/repository.py` - Improved system_prompt retrieval

## Implementation Summary

### 1. Session-Agent Mismatch Bug Fix
- ✅ Updated the `_ensure_session_exists` method to handle cases where agent ID can change format
- ✅ Modified the method to use the agent_id that's already associated with the session when one exists
- ✅ Updated the API endpoint error handling to use existing agent ID when there's a mismatch
- ✅ Enhanced the CLI chat to better handle session ID reuse errors

### 2. Message Content Fix
- ✅ Updated `add_message` to check first for content directly on the message object before examining parts
- ✅ Added explicit content attribute setting in message objects
- ✅ Added extensive logging to track content extraction
- ✅ Improved content extraction for different message types

### 3. System Prompt Fix
- ✅ Enhanced `add_response` in `MessageHistory` to fetch the system prompt from session metadata if not provided
- ✅ Improved the `get_system_prompt` function with better error handling and detailed logging
- ✅ Updated `base_agent.py` to explicitly pass system_prompt to assistant messages
- ✅ Ensured system_prompt is included in message payloads

### 4. Testing and Verification
- ✅ Created test script `20250318_1608_session_id_agent_mismatch_fix_test.py` to verify fixes
- ✅ Added extensive logging throughout the pipeline
- ✅ Verified all fixes through manual testing
- ✅ Confirmed no regression in other functionality

## Results
All tests have passed successfully. The fixes solved the identified issues:
- Sessions can be properly reused between requests without agent ID mismatch errors
- Message content is correctly stored in the database
- System prompts are properly attached to assistant messages in the database

## Detailed Report
For a comprehensive analysis of the issues, implementation details, and validation results, see the [full implementation report](20250318_1608_session_id_agent_mismatch_fix_report.md).

## Next Steps
1. Add more unit tests for critical components like message storage
2. Consider adding type annotations and validation throughout the codebase
3. Document the message flow and session handling for future reference 