# Fix Assistant Message Storage Report

## Issue Analysis

Based on the database testing, we've identified two primary issues with the assistant message storage system:

1. **System messages were being stored as separate rows** in the messages table with `role='system'` instead of being attached to assistant messages via the `system_prompt` field.

2. **Assistant messages weren't being properly saved** to the database or were missing the `system_prompt` field content.

The screenshot provided confirms these issues, showing:
- System messages with `role='system'` as separate rows
- User messages are being stored correctly
- The assistant messages appear to be missing

## Root Causes

After examining the codebase, these issues stemmed from:

1. In `src/memory/pg_message_store.py`:
   - The `update_system_prompt()` method was creating a new standalone message with `role='system'` instead of storing it in the session metadata
   - The `add_message()` method attempted to retrieve the system prompt for assistant messages but had implementation issues

2. In `src/db/repository.py`: 
   - The `get_system_prompt()` function only looked for messages with `role='system'` to find the system prompt
   - There was no mechanism to properly associate system prompts with assistant messages

## Solution Implemented

### 1. Updated System Prompt Storage Approach

**Changed how system prompts are stored:**
- Now storing system prompts in the session metadata instead of as separate messages
- Updated the `update_system_prompt()` method in `pg_message_store.py` to save system prompts to session metadata
- Updated the `get_system_prompt()` function in `repository.py` to first check session metadata for the system prompt

### 2. Fixed Assistant Message Storage

**Ensured assistant messages include system prompts:**
- Modified the `add_message()` method to detect system prompts and store them in session metadata
- Fixed the handling of `tool_calls` and `tool_outputs` fields to properly convert lists to dictionaries
- Added proper fetching of system prompts from session metadata for assistant messages
- Improved error handling throughout the message storage code

### 3. Additional Technical Changes

- Implemented the missing `_determine_message_role()` and `_ensure_session_exists()` methods
- Added missing `session_exists()` and `clear_session()` implementations
- Added the missing `get_session_by_name()` method needed in real-world usage
- Improved debugging and logging for better troubleshooting

## Test Results

We successfully verified that:
1. System prompts are now stored in session metadata rather than as separate messages
2. Assistant messages are properly saved with their system prompts
3. The tool calls and outputs are correctly formatted as required

## Final Status

The fix has been successfully implemented and tested. System prompts are now correctly stored in session metadata and properly attached to assistant messages when retrieved.

Key files modified:
- `src/memory/pg_message_store.py` - Major updates to storage logic
- `src/db/repository.py` - Updated system prompt retrieval
- `src/test_assistant_messages.py` - Created test to verify fixes

This implementation maintains backward compatibility while fixing the issues with assistant message storage. 