# Task: Fix Assistant Message Storage Issue

## Problem Description
Currently, assistant messages are not being properly stored in the database:
1. System prompts are being added as separate row entries with role="system"
2. Assistant responses are missing from the database (no rows with role="assistant")
3. The system_prompt field in assistant messages is not being populated correctly

## Updated Approach
After review, we're focusing on fixing the storage of new messages going forward rather than migrating old data:

1. Implement message repository functions to follow clean repository pattern
2. Update PostgresMessageStore to use repository functions and fix assistant message storage
3. Test the fix with new conversations

## Implementation Plan

Following the db_instructions.md guidelines, we need to:

1. Create message repository functions in src/db/repository.py
2. Modify PostgresMessageStore to use these repository functions
3. Ensure proper handling of assistant messages and system prompts

### Step 1: Add Message Repository Functions (completed)

Added the following functions to src/db/repository.py:

* create_message(message: Message) -> Optional[uuid.UUID]
* get_message(message_id: uuid.UUID) -> Optional[Message]
* list_messages(session_id: uuid.UUID, limit: int = 100, offset: int = 0) -> List[Message]
* update_message(message: Message) -> Optional[uuid.UUID]
* delete_message(message_id: uuid.UUID) -> bool
* get_system_prompt(session_id: uuid.UUID) -> Optional[str]

### Step 2: Update PostgresMessageStore (in progress)

Modified PostgresMessageStore to:
1. Use repository functions instead of direct SQL queries
2. Ensure proper role setting for assistant messages
3. Make sure system_prompt is correctly set when creating assistant messages

Methods updated:
- add_message()
- update_system_prompt()
- get_messages()
- _ensure_session_exists()

### Step 3: Testing

- Test creating new conversations with system prompts and assistant responses
- Verify assistant messages are stored correctly in database
- Verify system prompts are attached to assistant messages rather than as separate rows

## Implementation Status

- [x] Add message repository functions
- [x] Update PostgresMessageStore.add_message
- [x] Update PostgresMessageStore.update_system_prompt
- [x] Update PostgresMessageStore.get_messages
- [x] Update PostgresMessageStore._ensure_session_exists
- [ ] Test fix with new conversations

## Expected Outcome

After these changes:
1. New system prompts will be stored in the system_prompt field of assistant messages
2. New assistant messages will be properly stored with role="assistant"
3. Repository pattern will be followed per db_instructions.md
4. Legacy data will remain as-is until (optionally) addressed in a future task 