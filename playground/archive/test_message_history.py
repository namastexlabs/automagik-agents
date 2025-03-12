#!/usr/bin/env python3
"""
Script to test the MessageHistory implementation with the populated test data.
This validates that the project can properly read and write to the database.
"""

import logging
import os
import sys
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database connection parameters - use the same variable names as the main project
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Log the database connection parameters (but mask password)
logger.info(f"Database connection parameters:")
logger.info(f"  Host: {DB_HOST}")
logger.info(f"  Port: {DB_PORT}")
logger.info(f"  Database: {DB_NAME}")
logger.info(f"  User: {DB_USER}")
logger.info(f"  Password: {'*' * len(DB_PASSWORD) if DB_PASSWORD else 'not set'}")

# Import project modules
try:
    from src.memory.message_history import MessageHistory
    from src.memory.pg_message_store import PostgresMessageStore
    from pydantic_ai.messages import SystemPromptPart, UserPromptPart, TextPart
except ImportError as e:
    logger.error(f"Failed to import project modules: {str(e)}")
    logger.error("Make sure you're running this script from the project root directory")
    sys.exit(1)


def test_message_history_with_existing_session(session_id):
    """Test reading messages from an existing session."""
    try:
        logger.info(f"Testing MessageHistory with existing session {session_id}...")
        
        # Initialize PostgreSQL message store
        store = PostgresMessageStore()
        
        # Set PostgresMessageStore as the message store for MessageHistory
        MessageHistory.set_message_store(store)
        
        # Create a MessageHistory instance with the session_id
        history = MessageHistory(session_id=session_id)
        
        # Get existing messages
        messages = history.get_messages()
        
        if messages:
            logger.info(f"✅ Successfully retrieved {len(messages)} messages from session {session_id}")
            for i, msg in enumerate(messages):
                logger.info(f"  Message {i+1}: {msg.role} - {msg.content[:30]}...")
            return True
        else:
            logger.error(f"❌ No messages found for session {session_id}")
            return False
    except Exception as e:
        logger.error(f"Error testing MessageHistory with existing session: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False


def test_create_new_session_and_messages():
    """Test creating a new session and adding messages."""
    try:
        # Generate a new session ID
        new_session_id = f"test-history-{uuid.uuid4()}"
        logger.info(f"Testing creation of new session {new_session_id}...")
        
        # Initialize PostgreSQL message store
        store = PostgresMessageStore()
        
        # Set PostgresMessageStore as the message store for MessageHistory
        MessageHistory.set_message_store(store)
        
        # Create a MessageHistory instance with the new session_id
        history = MessageHistory(session_id=new_session_id)
        
        # Add a system message
        system_message = [
            SystemPromptPart(content="You are a helpful test assistant for the MessageHistory integration test.")
        ]
        history.append_system_prompt(system_message)
        logger.info("✅ Added system message")
        
        # Add a user message
        user_message = [
            UserPromptPart(content=[
                TextPart(text="Can you test if this message is properly stored in the database?")
            ])
        ]
        history.append_user_message(user_message)
        logger.info("✅ Added user message")
        
        # Add an assistant message
        assistant_message = "Yes, I've received your message and it's being stored in the database correctly."
        history.append_assistant_message(assistant_message)
        logger.info("✅ Added assistant message")
        
        # Get all messages to verify
        messages = history.get_messages()
        
        if messages and len(messages) == 3:  # System, user, and assistant messages
            logger.info(f"✅ Successfully created new session {new_session_id} with {len(messages)} messages")
            for i, msg in enumerate(messages):
                logger.info(f"  Message {i+1}: {msg.role} - {msg.content[:30]}...")
            return new_session_id
        else:
            logger.error(f"❌ Failed to create proper message history for session {new_session_id}")
            return None
    except Exception as e:
        logger.error(f"Error creating new session and messages: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return None


def test_update_messages(session_id):
    """Test updating messages in an existing session."""
    try:
        logger.info(f"Testing updating messages in session {session_id}...")
        
        # Initialize PostgreSQL message store
        store = PostgresMessageStore()
        
        # Set PostgresMessageStore as the message store for MessageHistory
        MessageHistory.set_message_store(store)
        
        # Create a MessageHistory instance with the session_id
        history = MessageHistory(session_id=session_id)
        
        # Get existing messages before update
        messages_before = history.get_messages()
        logger.info(f"Session has {len(messages_before)} messages before update")
        
        # Add a new assistant message
        new_message = "This is an updated message to test the message history functionality."
        history.append_assistant_message(new_message)
        logger.info("✅ Added new assistant message")
        
        # Get messages after update
        messages_after = history.get_messages()
        
        if len(messages_after) > len(messages_before):
            logger.info(f"✅ Successfully updated session {session_id}: {len(messages_before)} -> {len(messages_after)} messages")
            return True
        else:
            logger.error(f"❌ Failed to update messages for session {session_id}")
            return False
    except Exception as e:
        logger.error(f"Error updating messages: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False


def main():
    """Main function to test MessageHistory implementation."""
    logger.info("🔍 Starting MessageHistory implementation test")
    
    # Import the session ID from verify_integration.py's output
    # or use a hardcoded test session ID if available
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        # Get a session ID from the database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id FROM sessions LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            existing_session_id = result["id"]
            logger.info(f"Using existing session ID: {existing_session_id}")
            
            # Test 1: Read existing session
            success1 = test_message_history_with_existing_session(existing_session_id)
            
            # Test 2: Create new session and messages
            new_session_id = test_create_new_session_and_messages()
            success2 = new_session_id is not None
            
            # Test 3: Update existing session
            if success2:
                success3 = test_update_messages(new_session_id)
            else:
                success3 = False
                logger.error("Skipping update test since new session creation failed")
            
            # Final verdict
            if success1 and success2 and success3:
                logger.info("🎉 All MessageHistory integration tests passed!")
            else:
                logger.error("❌ Some MessageHistory integration tests failed!")
        else:
            logger.error("No existing sessions found in the database")
            logger.info("Run verify_integration.py first to create test data")
            
            # Test creating a new session anyway
            new_session_id = test_create_new_session_and_messages()
            if new_session_id:
                logger.info("✅ Successfully created new test session without existing data")
                test_update_messages(new_session_id)
            else:
                logger.error("❌ Failed to create new test session")
    except Exception as e:
        logger.error(f"Error in main test function: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")


if __name__ == "__main__":
    main() 