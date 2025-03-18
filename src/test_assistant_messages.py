"""Test script to verify assistant messages are stored correctly."""
import uuid
import logging
from datetime import datetime
import json

from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    UserPromptPart,
    TextPart
)

from src.memory.message_history import MessageHistory, TextPart as CustomTextPart
from src.memory.pg_message_store import PostgresMessageStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_assistant_messages():
    """Test that assistant messages are stored correctly with system prompts."""
    # Create a unique session ID for this test
    session_id = str(uuid.uuid4())
    logger.info(f"Testing with session ID: {session_id}")
    
    # Initialize MessageStore and MessageHistory
    store = PostgresMessageStore()
    MessageHistory.set_message_store(store)
    message_history = MessageHistory(session_id)
    
    # Add system prompt
    system_prompt = "You are a helpful assistant that provides concise responses."
    message_history.add_system_prompt(system_prompt)
    logger.info("Added system prompt")
    
    # Add user message
    user_message = "Hello, what can you tell me about database migrations?"
    message_history.add(user_message)
    logger.info("Added user message")
    
    # Add assistant response
    assistant_response = "Database migrations are controlled changes to database schemas to evolve the database structure over time."
    message_history.add_response(
        content=assistant_response,
        assistant_name="TestAssistant",
        system_prompt=system_prompt
    )
    logger.info("Added assistant response")
    
    # Retrieve messages and verify
    from src.db import list_messages, get_session
    
    # First check if system prompt is in session metadata
    session = get_session(uuid.UUID(session_id))
    if session and session.metadata:
        metadata = session.metadata
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except:
                metadata = {}
        
        if "system_prompt" in metadata:
            logger.info(f"System prompt found in session metadata: {metadata['system_prompt'][:50]}...")
        else:
            logger.warning("System prompt not found in session metadata!")
    else:
        logger.warning("Session metadata not found or empty!")
    
    # Check messages
    messages = list_messages(uuid.UUID(session_id))
    
    # Check if messages are stored correctly
    logger.info(f"Retrieved {len(messages)} messages")
    
    for msg in messages:
        logger.info(f"Message ID: {msg.id}, Role: {msg.role}")
        logger.info(f"  Content: {msg.text_content[:50]}...")
        if msg.role == "assistant":
            if msg.system_prompt:
                logger.info(f"  System Prompt: {msg.system_prompt[:50]}...")
            else:
                logger.error("Assistant message does not have system_prompt!")
    
    # Count message types
    system_count = len([m for m in messages if m.role == "system"])
    user_count = len([m for m in messages if m.role == "user"])
    assistant_count = len([m for m in messages if m.role == "assistant"])
    
    logger.info(f"System messages: {system_count}")
    logger.info(f"User messages: {user_count}")
    logger.info(f"Assistant messages: {assistant_count}")
    
    # Verify results
    assert system_count == 0, "Should have 0 system messages (stored in metadata instead)"
    assert user_count == 1, "Should have 1 user message"
    assert assistant_count == 1, "Should have 1 assistant message"
    
    # Check assistant message for system_prompt
    assistant_messages = [m for m in messages if m.role == "assistant"]
    if assistant_messages:
        assistant_msg = assistant_messages[0]
        assert assistant_msg.system_prompt == system_prompt, "Assistant message should have system_prompt set"
    
    logger.info("Test completed successfully!")
    return session_id

if __name__ == "__main__":
    test_assistant_messages() 