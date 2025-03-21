## Task Management: Fix SimpleAgent System Prompt Not Working

### Analysis

Based on the debug output and code review, I've identified a bug in the SimpleAgent's prompt handling system. When a user asks about the agent's name, it should respond with "TESTONHO" as specified in the `SIMPLE_AGENT_PROMPT` in `src/agents/simple/simple_agent/prompts/prompt.py`, but instead it's responding with a generic "I don't have a personal name, but you can call me Assistant!" message.

After reviewing the codebase, I've identified the following key components:

1. **Prompt Loading**: The agent loads the system prompt from `prompts/prompt.py` correctly during initialization:
   ```python
   from src.agents.simple.simple_agent.prompts.prompt import SIMPLE_AGENT_PROMPT
   self.prompt_template = SIMPLE_AGENT_PROMPT
   ```

2. **Template Handling**: The agent uses a dynamic system prompt handler to replace template variables with their values:
   ```python
   @self._agent_instance.system_prompt
   async def replace_template_variables(ctx: RunContext[SimpleAgentDependencies]) -> str:
       # Template variable replacement logic
       # ...
       prompt_template = self.prompt_template
       for var_name, value in template_values.items():
           placeholder = f"{{{{{var_name}}}}}"
           prompt_template = prompt_template.replace(placeholder, value)
       return prompt_template
   ```

3. **Agent Initialization**: The PydanticAI agent is created with a base system prompt, which is initially set to an empty string in `_create_base_system_prompt()`.

The issue appears to be that the agent's message history management isn't correctly applying the system prompt in subsequent runs, or the dynamic system prompt decorator isn't being executed when expected.

### Plan

1. Check if the system prompt is actually being applied by adding debug logs to verify:
   - `src/agents/simple/simple_agent/agent.py`: Add logging for the final system prompt after template replacement

2. Inspect the agent initialization sequence to ensure the system prompt is properly registered:
   - Verify the sequence in `_initialize_agent()` and `_register_system_prompts()`
   - Check if there's a potential race condition in the asynchronous code

3. Fix the system prompt application logic:
   - Ensure the template variables are correctly identified and replaced
   - Make sure the dynamic system prompt is correctly registered with PydanticAI

4. Test the fix with a direct query about the agent's name

### Execution

I've implemented the following changes to fix the issue:

1. Modified `_create_base_system_prompt()` to return the actual prompt template instead of an empty string:
   ```python
   def _create_base_system_prompt(self) -> str:
       # Instead of returning an empty string, we'll use the template directly
       # This ensures the prompt is available even without template replacement
       return self.prompt_template
   ```

2. Added explicit system_prompt setting during agent initialization:
   ```python
   async def _initialize_agent(self) -> None:
       # ...
       # Ensure system_prompt is set properly from the template
       self.system_prompt = self.prompt_template
       logger.info(f"Initializing agent with system prompt template (first 50 chars): {self.system_prompt[:50]}...")
       # ...
   ```

3. Added detailed logging throughout the system prompt handling process:
   - In `replace_template_variables` to log the final processed prompt
   - In `_initialize_agent` to show the system prompt being used
   - In `run` to confirm the system prompt before processing

4. Created a new method `dependencies_to_message_history()` to ensure the system prompt is included in the message history:
   ```python
   def dependencies_to_message_history(self) -> None:
       """Ensure dependencies message history includes the system prompt."""
       # Check if we have dependencies with a message history manager
       if not hasattr(self.dependencies, "message_history_manager"):
           logger.warning("No message_history_manager in dependencies")
           return
           
       # If there are no messages yet, add the system prompt
       messages = self.dependencies.message_history_manager.messages
       if not messages or len(messages) == 0:
           logger.info("Adding system prompt to empty message history manager")
           if hasattr(self, "system_prompt") and self.system_prompt:
               try:
                   # Add system prompt to the beginning of the messages
                   if hasattr(self.dependencies.message_history_manager, "add_system_message"):
                       self.dependencies.message_history_manager.add_system_message(self.system_prompt)
                       logger.info("Added system prompt to message history manager")
                   else:
                       logger.warning("message_history_manager lacks add_system_message method")
               except Exception as e:
                   logger.error(f"Failed to add system prompt to message history: {str(e)}")
   ```

5. Enhanced the `run` method to handle message history properly:
   - Added better logging for system prompt usage
   - Force agent reconstruction if no message history exists
   - Call the new `dependencies_to_message_history()` method to ensure system prompt is included

### Testing

The changes were tested with the following scenarios:

1. Direct test with a query about the agent's name:
   ```
   whats ur name
   ```
   The agent now correctly responds with "TESTONHO" as specified in the prompt.

2. Test with multiple messages in a conversation to ensure the system prompt persists.

3. Verified that template variables are correctly replaced in the system prompt.

The logs now show the system prompt is being properly loaded and applied, and the agent responds correctly to name queries.

### Summary

The issue was fixed by ensuring that:
1. The system prompt is properly set from the template during agent initialization
2. The agent's message history correctly includes the system prompt
3. When no message history exists, we force rebuilding the agent to ensure fresh system prompt application
4. Enhanced logging helps troubleshoot any future issues

#### Files modified:
- `src/agents/simple/simple_agent/agent.py`: 
  - Updated `_create_base_system_prompt()` to return actual template
  - Added explicit system_prompt setting in `_initialize_agent()`
  - Added detailed logging throughout system prompt handling
  - Created new method `dependencies_to_message_history()`
  - Enhanced `run` method to manage message history properly

This fix ensures that the system prompt (including the debug mode with "TESTONHO" name) is consistently applied across all interactions with the agent.

#### Dependencies:
- System prompt from `src/agents/simple/simple_agent/prompts/prompt.py`
- PydanticAI's agent system prompt registration mechanism

#### Potential Impact:
This fix will ensure that all configured system prompt behaviors work correctly, not just the name response. It affects how the agent presents itself and follows instructions in its system prompt. 