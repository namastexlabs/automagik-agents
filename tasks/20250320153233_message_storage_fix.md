# Message Storage Bug Investigation and Fix

## Analysis
- **Issue Description**: Messages are not being stored in the database when using the CLI run command to talk to the simple agent.
- **Reproduction Steps**: Running `automagik-agents agent run message --agent simple_agent --message "Hello, what's the current date?" --debug --session felipe-teste`
- **Affected Components**:
  - `src/memory/message_history.py` - Manages message history
  - `src/db/repository/message.py` - Handles database operations for messages
  - `src/cli/agent/run.py` - CLI interface for agent interaction

### Initial Observations
The CLI runs `run_agent()` which makes an API call to the agent's run endpoint. The message storage should happen during this API call execution. Possible issues:
1. The message history may not be properly initialized during CLI runs
2. Session handling might be incorrect for CLI-originated messages
3. There could be error handling issues that silently fail when saving messages
4. Database connection or transaction issues may be preventing successful storage

## Plan
1. **Confirm Issue Reproduction**
   - Run the provided command with debug mode and observe the logs
   - Check the database to confirm messages are not being stored

2. **Trace Message Flow**
   - Follow code path from CLI to database storage
   - Identify where the message storage process breaks down
   - Check if session creation works but message storage fails

3. **Inspect Database Operations**
   - Examine errors in logs related to database operations
   - Check if any exceptions are being caught without proper handling
   - Verify that database transactions are being committed properly

4. **Check Message Creation/Serialization**
   - Review the data being passed to create_message function
   - Ensure all required fields are properly populated
   - Check for type conversion issues (e.g., UUID handling)

5. **Implement Fix**
   - Based on findings, implement appropriate fixes
   - Add additional logging for better diagnosis in the future
   - Ensure proper error handling and reporting
   - Verify that session and related message attributes are properly set

6. **Test Solution**
   - Run the command again with the fixed code
   - Verify message storage in database, including:
     - User messages
     - Assistant responses
     - Tool calls and outputs
     - System prompt
     - All related fields in the message table

## Execution

### Step 1: Issue Reproduction
I've confirmed the issue by running the command:
```
automagik-agents agent run message --agent simple_agent --message "Hello, what's the current date?" --debug --session felipe-teste
```

The command successfully interacts with the agent and receives a response. The agent correctly processes the message and returns the current date. However, while the session is created in the database (verified by querying the sessions table), no messages are stored in the messages table.

Database verification:
- Session exists: The session with ID `34f86be7-804f-4610-a3c5-4561f95da5ad` is created in the sessions table
- Messages missing: No messages are stored in the messages table for this session ID

### Step 2: Message Flow Analysis

Based on code inspection, here's the message flow:

1. The CLI `run.py` makes an API call to the agent run endpoint with the message, session name, and other parameters
2. The API endpoint `run_agent()` in `src/api/routes.py` processes the request:
   - Creates or retrieves a session based on the session name
   - Initializes a MessageHistory object with the session ID
   - Calls the agent's `process_message()` method
3. The agent's `process_message()` in `BaseAgent` should:
   - Initialize a MessageHistory object
   - Add the system prompt to the message history
   - Add the user message to the message history
   - Process the message and get a response
   - Return the response with the updated message history
4. The MessageHistory object should store messages in the database via the repository functions

The issue appears to be that while the MessageHistory is being created and used during processing, it's either:
1. Not properly adding messages to the database
2. Adding messages but with errors that prevent successful storage
3. Not being passed the correct session ID or other required parameters

### Step 3: Detailed Analysis of the Issue

After reviewing the logs and code, I've identified the following:

1. The agent correctly processes the message and communicates with the OpenAI API
2. The API successfully responds with the current date using the `get_current_date_tool`
3. The session is successfully created in the database
4. However, no errors are logged when attempting to store messages

Looking at the `MessageHistory` class, I noticed an important pattern:

```python
# In the MessageHistory.add() method:
try:
    # Create message in database
    message_id = create_message(message)
    if not message_id:
        logger.error(f"Failed to create user message in database")
    else:
        logger.info(f"Successfully added user message {message_id} to history")
    # ...
except Exception as e:
    logger.error(f"Exception adding user message: {str(e)}")
    # Return a fallback message without raising exception
```

Similarly in `add_response()`:

```python
try:
    # Create message in database
    message_id = create_message(message)
    if not message_id:
        logger.error(f"Failed to create assistant message in database")
    else:
        logger.info(f"Successfully added assistant message {message_id} to history")
    # ...
except Exception as e:
    logger.error(f"Exception adding assistant message: {str(e)}")
    # Return a fallback message without raising exception
```

This pattern indicates that `MessageHistory` is designed to be fault-tolerant - it catches and logs errors but continues execution even when database operations fail. This is good for resilience but makes failures harder to detect.

A key observation is that no database-related error messages appear in the logs, suggesting that either:
1. The code is never actually calling the database operations
2. The exceptions are being caught at a higher level before they reach these logging statements
3. There's an issue with the session ID being passed to `MessageHistory` that prevents correct database operations

Looking at the `process_message` method in `BaseAgent`, the flow suggests that the MessageHistory object is being initialized twice:

```python
# Initialize message history in the API route handler
message_history = MessageHistory(request.session_id, user_id=request.user_id)

# Later, in BaseAgent.process_message
# Another message history is initialized
message_history = MessageHistory(session_id, user_id=user_id)
```

This double initialization could be problematic if the second instance doesn't properly track or update messages added by the first instance.

Additionally, from the `SimpleAgent` class, we see:

```python
async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[Union[int, str]] = None, user_id: int = 1, context: Optional[Dict] = None) -> AgentResponse:
    # Set session and user info in dependencies
    if session_id:
        self.dependencies.session_id = session_id
    self.dependencies.user_id = user_id
    
    # Extract multimodal content from context
    multimodal_content = None
    if context and "multimodal_content" in context:
        multimodal_content = context["multimodal_content"]
        
    # Run the agent
    return await self.run(user_message, multimodal_content=multimodal_content)
```

This method doesn't explicitly handle message history, instead passing control to `self.run()`, which may or may not be properly integrated with the MessageHistory object from the parent class.

### Step 4: Root Cause Identified

Based on the analysis, the most likely root cause is a potential mismatch in how the MessageHistory is initialized and used between the CLI/API code path and the internal agent processing.

Specifically:
1. The message history is created in the API route handler
2. But it's created again in the BaseAgent class
3. These two instances don't share state
4. When messages are added in one context, they're not available in the other

The BaseAgent is using its own internal message history, but the agent responses may not be properly stored in the database because:
- Either the message storage is bypassed
- Or exceptions are being silently caught

### Step 5: Proposed Fix

The fix should ensure that:
1. Only one MessageHistory instance is created per session
2. Messages are properly added to that instance and stored in the database
3. Error handling is improved to better report database issues

Here's the proposed implementation:

1. Modify `BaseAgent.process_message()` to use the existing MessageHistory object passed from the API route handler, rather than creating a new one.
2. Add more detailed logging in the MessageHistory methods to better track message storage failures.
3. Ensure database connection and transaction handling is correct.

Specific code changes:

```python
# In src/agents/models/base_agent.py:

async def process_message(self, user_message: str, session_id: Optional[str] = None, agent_id: Optional[Union[int, str]] = None, user_id: int = 1, context: Optional[Dict] = None, message_history: Optional[MessageHistory] = None) -> AgentBaseResponse_v2:
    """Process a user message with this agent.
    
    Args:
        user_message: User message to process
        session_id: Optional session ID
        agent_id: Optional agent ID for database tracking
        user_id: User ID
        context: Optional additional context
        message_history: Optional existing MessageHistory object
        
    Returns:
        Agent response
    """
    if not session_id:
        # Using empty string is no longer allowed - we need a valid session ID
        logging.error("Empty session_id provided, session must be created before calling process_message")
        return AgentBaseResponse_v2.from_agent_response(
            message="Error: No valid session ID provided. A session must be created before processing messages.",
            history=MessageHistory(""),
            error="No valid session ID provided",
            session_id=""
        )
    
    # Set default context if None is provided
    context = context or {}
        
    logging.info(f"Using existing session ID: {session_id}")
    
    # Log any additional context provided
    if context:
        logging.info(f"Additional message context: {context}")
        
    # Use provided message history or initialize a new one
    if not message_history:
        logging.info(f"Creating new MessageHistory for session {session_id}")
        message_history = MessageHistory(session_id, user_id=user_id)
    else:
        logging.info(f"Using existing MessageHistory for session {session_id}")
    
    # CRITICAL: Add the system prompt explicitly BEFORE adding the user message
    # This ensures it will be the first message in the sequence sent to OpenAI
    if hasattr(self, "system_prompt") and self.system_prompt:
        logging.info("Adding system prompt to message history before user message")
        message_history.add_system_prompt(self.system_prompt, agent_id=agent_id)
    
    # Add the user message AFTER the system prompt
    user_message_obj = message_history.add(user_message, agent_id=agent_id, context=context)
    
    # ... rest of the method stays the same ...
```

Then in the API route handler, pass the MessageHistory to the agent:

```python
# In src/api/routes.py:

# Initialize MessageHistory with the correct session_id
message_history = MessageHistory(request.session_id, user_id=request.user_id)

# ... later when calling process_message:

response = await agent.process_message(
    request.message_content,
    session_id=request.session_id,
    user_id=request.user_id,
    context=message_context,
    message_history=message_history  # Pass the existing MessageHistory
)
```

Additionally, we should improve error handling in the MessageHistory class to provide more detailed logs when database operations fail:

```python
# In src/memory/message_history.py:

def add(self, content: str, agent_id: Optional[int] = None, context: Optional[Dict] = None) -> ModelMessage:
    """Add a user message to the history."""
    try:
        # Create message object
        message = Message(...)
        
        # Log before attempting to create message
        logger.info(f"Adding user message to history for session {self.session_id}, user {self.user_id}")
        
        # Create message in database with more detailed error handling
        message_id = create_message(message)
        
        if not message_id:
            # More detailed error message
            logger.error(f"Failed to create user message in database. Session: {self.session_id}, User: {self.user_id}")
            # Don't raise exception to maintain backward compatibility, but log the error
        else:
            logger.info(f"Successfully added user message {message_id} to history")
        
        # ... rest of the method ...
    except Exception as e:
        import traceback
        logger.error(f"Exception adding user message: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        # Add more details to help diagnosis
        logger.error(f"Message details: session_id={self.session_id}, user_id={self.user_id}, content_length={len(content) if content else 0}")
        
        # Return a basic user message as fallback
        return ModelRequest(parts=[UserPromptPart(content=content)])
```

This approach should resolve the message storage issues while maintaining backward compatibility with existing code.

### Step 6: Implementation

I'll now implement these changes to the codebase and test if they resolve the message storage issue.