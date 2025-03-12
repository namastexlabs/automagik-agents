#!/usr/bin/env python3
import uuid
import time
from datetime import datetime
import logging
import sys
import os

# Add the project root to sys.path to allow imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Configure logging
from src.utils.logging import configure_logging
configure_logging()
logger = logging.getLogger("test_timestamps")

# Import database utilities
from src.utils.db import execute_query, get_db_connection
from src.memory.pg_message_store import PostgresMessageStore

def test_timestamps():
    """Test the timestamps functionality with a new session and messages."""
    try:
        # Create a store
        store = PostgresMessageStore()
        
        # Create a new session with session_origin='timestamp_test'
        session_id = store.create_session(user_id=1, session_origin='timestamp_test')
        logger.info(f"Created test session with ID: {session_id}")
        
        # Record initial timestamps
        session_data = execute_query(
            "SELECT created_at, updated_at, run_finished_at FROM sessions WHERE id = %s::uuid",
            (session_id,)
        )[0]
        
        logger.info(f"Initial session timestamps: created_at={session_data['created_at']}, "
                   f"updated_at={session_data['updated_at']}, run_finished_at={session_data['run_finished_at']}")
        
        # Add a user message
        from pydantic_ai.messages import ModelRequest, UserPromptPart, TextPart
        user_msg = ModelRequest(parts=[UserPromptPart(content='Hello from timestamp test!')])
        store.add_message(session_id, user_msg)
        logger.info("Added user message")
        
        # Get all messages and timestamps
        messages = execute_query(
            "SELECT id, role, text_content, created_at, updated_at FROM messages WHERE session_id = %s::uuid ORDER BY created_at",
            (session_id,)
        )
        
        for msg in messages:
            logger.info(f"Message: role={msg['role']}, text={msg['text_content']}, "
                       f"created_at={msg['created_at']}, updated_at={msg['updated_at']}")
        
        # Get session data again
        session_data = execute_query(
            "SELECT created_at, updated_at, run_finished_at FROM sessions WHERE id = %s::uuid",
            (session_id,)
        )[0]
        
        logger.info(f"Session after user message: created_at={session_data['created_at']}, "
                   f"updated_at={session_data['updated_at']}, run_finished_at={session_data['run_finished_at']}")
        
        # Wait a moment to ensure timestamps are different
        logger.info("Waiting 1 second...")
        time.sleep(1)
        
        # Add an assistant message
        from pydantic_ai.messages import ModelResponse, TextPart
        assistant_msg = ModelResponse(parts=[TextPart(content='Hi! This is a test response')])
        store.add_message(session_id, assistant_msg)
        logger.info("Added assistant message")
        
        # Get all messages again
        messages = execute_query(
            "SELECT id, role, text_content, created_at, updated_at FROM messages WHERE session_id = %s::uuid ORDER BY created_at",
            (session_id,)
        )
        
        for msg in messages:
            logger.info(f"Message: role={msg['role']}, text={msg['text_content']}, "
                       f"created_at={msg['created_at']}, updated_at={msg['updated_at']}")
        
        # Get session data again after assistant message
        session_data = execute_query(
            "SELECT created_at, updated_at, run_finished_at FROM sessions WHERE id = %s::uuid",
            (session_id,)
        )[0]
        
        logger.info(f"Session after assistant message: created_at={session_data['created_at']}, "
                   f"updated_at={session_data['updated_at']}, run_finished_at={session_data['run_finished_at']}")
        
        # Check ordered views
        logger.info("Checking ordered views...")
        
        # Check ordered_sessions view
        ordered_sessions = execute_query(
            "SELECT id, last_user_message_time, last_assistant_message_time, message_count, "
            "user_message_count, assistant_message_count, run_finished_at "
            "FROM ordered_sessions WHERE id = %s::uuid",
            (session_id,)
        )
        
        if ordered_sessions:
            s = ordered_sessions[0]
            logger.info(f"ordered_sessions view: last_user_msg={s['last_user_message_time']}, "
                       f"last_assistant_msg={s['last_assistant_message_time']}, "
                       f"message_count={s['message_count']}, user_msgs={s['user_message_count']}, "
                       f"assistant_msgs={s['assistant_message_count']}, run_finished_at={s['run_finished_at']}")
        else:
            logger.warning("Session not found in ordered_sessions view")
        
        logger.info("✅ Timestamp test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during timestamp test: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    if test_timestamps():
        print("✅ Timestamp test completed successfully")
        sys.exit(0)
    else:
        print("❌ Timestamp test failed")
        sys.exit(1) 