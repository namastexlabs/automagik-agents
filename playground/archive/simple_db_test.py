#!/usr/bin/env python3
"""
Simple script to test database connectivity and functionality.
This script follows the project's coding standards from CLAUDE.md.
"""

import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid

# Configure logging
from src.utils.logging import configure_logging
configure_logging()
logger = logging.getLogger("simple_db_test")

def test_db_connection() -> bool:
    """Test database connectivity using the project's utilities.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        from src.utils.db import get_connection_pool, execute_query
        
        logger.info("Testing database connection...")
        
        # Get a connection from the pool
        pool = get_connection_pool()
        with pool.getconn() as conn:
            with conn.cursor() as cur:
                # Test query
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                logger.info(f"✅ Database connection test successful: {version}")
                
                # Check if our tables exist
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sessions')")
                sessions_table_exists = cur.fetchone()[0]
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'messages')")
                messages_table_exists = cur.fetchone()[0]
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
                users_table_exists = cur.fetchone()[0]
                
                logger.info(f"Database tables check - Sessions: {sessions_table_exists}, "
                           f"Messages: {messages_table_exists}, Users: {users_table_exists}")
                
                if not (sessions_table_exists and messages_table_exists and users_table_exists):
                    logger.error("❌ Required database tables are missing")
                    return False
            pool.putconn(conn)
        
        return True
    except ImportError as e:
        logger.error(f"Failed to import database utilities: {str(e)}")
        logger.error("Make sure you're running this script from the project root directory")
        return False
    except Exception as e:
        logger.error(f"Error testing database connection: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False


def get_table_counts() -> Dict[str, int]:
    """Get row counts for each table in the database.
    
    Returns:
        Dict[str, int]: Dictionary mapping table names to row counts
    """
    try:
        from src.utils.db import execute_query
        
        logger.info("Getting table row counts...")
        
        # Get list of tables
        tables = execute_query(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            """
        )
        
        # Count rows in each table
        counts = {}
        for table in tables:
            table_name = table["table_name"]
            result = execute_query(f"SELECT COUNT(*) as count FROM {table_name}")
            count = result[0]["count"] if result else 0
            counts[table_name] = count
            logger.info(f"Table {table_name}: {count} rows")
        
        return counts
    except Exception as e:
        logger.error(f"Error getting table counts: {str(e)}")
        return {}


def cleanup_test_data(test_user_id: int = None, test_session_id: str = None):
    """Clean up test data created during testing.
    
    Args:
        test_user_id: The user ID to clean up
        test_session_id: The session ID to clean up
    """
    try:
        from src.utils.db import execute_query
        
        logger.info("Cleaning up test data...")
        
        # First check if we need to clean up sessions - must happen before users due to foreign key constraints
        if test_session_id:
            logger.info(f"Removing test session {test_session_id}...")
            
            # First clean up any messages associated with this session
            execute_query(
                "DELETE FROM messages WHERE session_id = %s",
                (test_session_id,),
                fetch=False
            )
            
            # Then clean up any session metadata
            execute_query(
                "DELETE FROM session_metadata WHERE session_id = %s",
                (test_session_id,),
                fetch=False
            )
            
            # Finally remove the session itself
            execute_query(
                "DELETE FROM sessions WHERE id = %s",
                (test_session_id,),
                fetch=False
            )
            
            logger.info(f"✅ Test session {test_session_id} removed")
        else:
            # No specific session ID provided - search for and clean up all test sessions
            test_sessions = execute_query(
                "SELECT id FROM sessions WHERE id LIKE 'test-%'"
            )
            
            if test_sessions:
                logger.info(f"Found {len(test_sessions)} test sessions to clean up")
                
                # Clean up associated data for all test sessions
                for session in test_sessions:
                    session_id = session["id"]
                    
                    # Delete associated messages
                    execute_query(
                        "DELETE FROM messages WHERE session_id = %s",
                        (session_id,),
                        fetch=False
                    )
                    
                    # Delete associated metadata
                    execute_query(
                        "DELETE FROM session_metadata WHERE session_id = %s",
                        (session_id,),
                        fetch=False
                    )
                
                # Now delete all test sessions
                execute_query(
                    "DELETE FROM sessions WHERE id LIKE 'test-%'",
                    fetch=False
                )
                
                logger.info(f"✅ Cleaned up {len(test_sessions)} test sessions")
        
        # Clean up test user if specified
        if test_user_id:
            logger.info(f"Removing test user {test_user_id}...")
            
            # Only allow removing test users with ID > 1 (to prevent removing default user)
            if test_user_id > 1:
                # Delete associated data for the test user
                execute_query(
                    "DELETE FROM memories WHERE user_id = %s",
                    (test_user_id,),
                    fetch=False
                )
                
                execute_query(
                    "DELETE FROM users WHERE id = %s",
                    (test_user_id,),
                    fetch=False
                )
                
                logger.info(f"✅ Test user {test_user_id} removed")
            else:
                logger.info(f"Skipping removal of default user with ID {test_user_id}")
        
        logger.info("✅ Test data cleanup complete")
    except Exception as e:
        logger.error(f"Error cleaning up test data: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")


def create_test_user() -> Optional[Dict[str, Any]]:
    """Create a test user for demonstration purposes.
    
    Returns:
        Optional[Dict[str, Any]]: The created user or None if creation failed
    """
    try:
        from src.utils.db import execute_query
        
        logger.info("Creating test user...")
        now = datetime.utcnow()
        
        # Create a test user with a different ID than the default user
        test_user_id = 9999
        test_email = f"test-{uuid.uuid4()}@example.com"
        
        # Check if test user already exists
        existing_user = execute_query(
            "SELECT COUNT(*) as count FROM users WHERE id = %s",
            (test_user_id,)
        )
        
        if existing_user[0]["count"] > 0:
            logger.info(f"Test user with ID {test_user_id} already exists")
            return execute_query("SELECT * FROM users WHERE id = %s", (test_user_id,))[0]
        
        # Create a test user
        execute_query(
            """
            INSERT INTO users (id, email, created_at, updated_at, user_data) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                test_user_id, 
                test_email,
                now,
                now,
                '{"name": "Test User", "type": "test"}'
            ),
            fetch=False
        )
        
        user = execute_query("SELECT * FROM users WHERE id = %s", (test_user_id,))[0]
        logger.info(f"✅ Test user created with ID: {user['id']}")
        return user
    except Exception as e:
        logger.error(f"Error creating test user: {str(e)}")
        return None


def test_message_history(user_id: int) -> tuple:
    """Test the MessageHistory class functionality.
    
    Args:
        user_id: The user ID to use for the test
        
    Returns:
        tuple: (success_bool, session_id) whether test was successful and the session ID
    """
    try:
        from src.memory.message_history import MessageHistory
        from src.memory.pg_message_store import PostgresMessageStore
        
        logger.info("Testing MessageHistory functionality...")
        
        # Initialize PostgreSQL message store
        pg_store = PostgresMessageStore()
        MessageHistory.set_message_store(pg_store)
        
        # Create a test session
        session_id = f"test-{uuid.uuid4()}"
        logger.info(f"Creating test session with ID: {session_id}")
        history = MessageHistory(session_id=session_id, user_id=user_id)
        
        # Add a system message
        logger.info("Adding system message...")
        history.add_system_prompt("You are a test assistant for database integration testing.")
        
        # Add a user message
        logger.info("Adding user message...")
        history.add("Testing database integration.")
        
        # Add an assistant message
        logger.info("Adding assistant message...")
        history.add_response("I can confirm the database integration is working correctly.")
        
        # Get messages
        messages = history.messages
        logger.info(f"Retrieved {len(messages)} messages from the database")
        
        success = len(messages) == 3  # 3 messages (system, user, assistant)
        
        return success, session_id
    except Exception as e:
        logger.error(f"Error testing MessageHistory: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False, None


def main() -> None:
    """Main function."""
    logger.info("🔍 Starting simple database integration test")
    
    # Variables to track resources that need cleanup
    test_user_id = None
    test_session_id = None
    
    try:
        # Step 1: Test database connection
        if not test_db_connection():
            logger.error("❌ Database connection test failed")
            sys.exit(1)
        
        # Step 2: Get table counts
        get_table_counts()
        
        # Step 3: Create test user
        user = create_test_user()
        if not user:
            logger.error("❌ Failed to create test user")
            sys.exit(1)
        test_user_id = user["id"]
        
        # Step 4: Test MessageHistory
        message_history_success, session_id = test_message_history(user["id"])
        test_session_id = session_id
        
        if message_history_success:
            logger.info("✅ MessageHistory test successful")
        else:
            logger.error("❌ MessageHistory test failed")
            sys.exit(1)
        
        logger.info("🎉 All database integration tests passed!")
    finally:
        # Always clean up test data, even if tests fail
        cleanup_test_data(test_user_id=test_user_id, test_session_id=test_session_id)


if __name__ == "__main__":
    main() 