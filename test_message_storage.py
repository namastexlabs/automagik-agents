#!/usr/bin/env python
"""Test script to diagnose message storage issues.

This script tests the message repository directly to identify why messages aren't being stored.
"""

import uuid
import logging
import sys
from datetime import datetime, UTC

from src.db.models import Message, Session
from src.db.repository.message import create_message, list_messages
from src.db.repository.session import get_session, create_session
from src.db.connection import execute_query

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger(__name__)

def test_session_db():
    """Test that the session can be created and retrieved from the database."""
    session_id = uuid.uuid4()
    logger.info(f"Testing session creation with ID: {session_id}")
    
    # Create a test session - need to use Session object, not dict
    session = Session(
        id=session_id,
        user_id=1,
        name=f"test-session-{session_id}",
        platform="test",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    
    try:
        create_session_result = create_session(session)
        logger.info(f"Session creation result: {create_session_result}")
        
        # Retrieve the session
        retrieved_session = get_session(session_id)
        logger.info(f"Retrieved session: {retrieved_session}")
        
        if retrieved_session:
            logger.info("Session creation and retrieval successful")
            return session_id
        else:
            logger.error("Failed to retrieve created session")
            return None
    except Exception as e:
        logger.error(f"Error testing session database: {str(e)}", exc_info=True)
        return None

def test_message_creation(session_id):
    """Test creating a message directly."""
    if not session_id:
        logger.error("No session ID provided, skipping message creation test")
        return
    
    logger.info(f"Testing message creation for session: {session_id}")
    
    # Create a test message
    message_id = uuid.uuid4()
    message = Message(
        id=message_id,
        session_id=session_id,
        user_id=1,
        agent_id=1,
        role="user",
        text_content="This is a test message",
        message_type="text",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    
    try:
        # Create the message
        create_result = create_message(message)
        logger.info(f"Message creation result: {create_result}")
        
        # List messages for the session
        messages = list_messages(session_id)
        logger.info(f"Retrieved {len(messages)} messages")
        
        # Log the full message objects
        for i, msg in enumerate(messages):
            logger.info(f"Message {i+1}: {vars(msg)}")
        
        return create_result
    except Exception as e:
        logger.error(f"Error testing message creation: {str(e)}", exc_info=True)
        return None

def direct_execute_message_insert():
    """Directly execute an INSERT statement to test database connectivity."""
    session_id = uuid.uuid4()
    message_id = uuid.uuid4()
    logger.info(f"Testing direct SQL execution with session_id: {session_id}, message_id: {message_id}")
    
    try:
        # Create a session first
        session_query = """
            INSERT INTO sessions (id, user_id, name, platform, created_at, updated_at)
            VALUES (%s, %s, %s, %s, NOW(), NOW())
            RETURNING id
        """
        session_result = execute_query(session_query, [session_id, 1, f"direct-test-{session_id}", "test"])
        logger.info(f"Session creation result: {session_result}")
        
        # Insert a message
        message_query = """
            INSERT INTO messages (
                id, session_id, user_id, role, text_content, message_type, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, NOW(), NOW()
            )
            RETURNING id
        """
        message_params = [
            message_id, session_id, 1, "user", "Direct SQL test message", "text"
        ]
        
        message_result = execute_query(message_query, message_params)
        logger.info(f"Direct message insertion result: {message_result}")
        
        # Retrieve the message
        select_query = "SELECT * FROM messages WHERE id = %s"
        select_result = execute_query(select_query, [message_id])
        logger.info(f"Retrieved message: {select_result}")
        
        return message_result
    except Exception as e:
        logger.error(f"Error in direct SQL execution: {str(e)}", exc_info=True)
        return None

def inspect_db_connection():
    """Test basic DB connection and inspect configuration."""
    try:
        # Check if we can connect to the database
        test_query = "SELECT version()"
        result = execute_query(test_query, [])
        logger.info(f"Database version: {result}")
        
        # Check tables
        tables_query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"
        tables = execute_query(tables_query, [])
        logger.info(f"Tables in database: {tables}")
        
        # Check messages table schema
        schema_query = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'messages'
            ORDER BY ordinal_position
        """
        schema = execute_query(schema_query, [])
        logger.info(f"Messages table schema: {schema}")
        
        return True
    except Exception as e:
        logger.error(f"Error inspecting database: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    logger.info("Starting message storage diagnostic test")
    
    # First test basic DB connection
    db_ok = inspect_db_connection()
    if not db_ok:
        logger.error("Database connection test failed, exiting")
        sys.exit(1)
    
    # Test direct SQL execution
    direct_result = direct_execute_message_insert()
    if not direct_result:
        logger.error("Direct SQL execution failed, possible database connection issue")
        
    # Test session creation and retrieval
    session_id = test_session_db()
    
    # Test message creation and retrieval
    message_result = test_message_creation(session_id)
    
    if message_result:
        logger.info("Message storage diagnostic tests PASSED")
    else:
        logger.error("Message storage diagnostic tests FAILED") 