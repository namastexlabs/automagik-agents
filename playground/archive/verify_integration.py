#!/usr/bin/env python3
"""
Script to verify the database integration for Automagik Agents.
This script tests each part of the integration step by step.
"""

import logging
import os
import sys
import uuid
import json
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

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


def get_db_connection():
    """Create a database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        sys.exit(1)


def create_default_user():
    """Create a default user in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info("Creating default user...")
        now = datetime.utcnow()
        cursor.execute(
            """
            INSERT INTO users (id, email, created_at, updated_at) 
            VALUES (%s, %s, %s, %s)
            RETURNING id, email
            """,
            (1, "admin@automagik", now, now)
        )
        user = cursor.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Default user created: {user}")
        return user
    except Exception as e:
        logger.error(f"Error creating default user: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        sys.exit(1)


def create_test_agent():
    """Create a test agent in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info("Creating test agent...")
        now = datetime.utcnow()
        
        config = {
            "system_prompt": "You are a helpful test assistant.",
            "tools": [],
            "parameters": {
                "temperature": 0.7,
                "top_p": 0.95
            }
        }
        
        cursor.execute(
            """
            INSERT INTO agents (
                name, type, model, active, config, 
                created_at, updated_at, version, description
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, name, type, model
            """,
            (
                "test_agent", 
                "simple", 
                "openai:gpt-4o-mini", 
                True, 
                json.dumps(config),
                now, 
                now, 
                "1.0.0", 
                "A test agent for integration verification"
            )
        )
        agent = cursor.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Test agent created: {agent}")
        return agent
    except Exception as e:
        logger.error(f"Error creating test agent: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        sys.exit(1)


def create_test_session(user_id):
    """Create a test session in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info(f"Creating test session for user {user_id}...")
        now = datetime.utcnow()
        session_id = f"test-session-{uuid.uuid4()}"
        
        cursor.execute(
            """
            INSERT INTO sessions (id, user_id, platform, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, user_id, platform
            """,
            (session_id, user_id, "test", now, now)
        )
        session = cursor.fetchone()
        
        # Add some session metadata
        cursor.execute(
            """
            INSERT INTO session_metadata (session_id, key, value, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (session_id, "test_key", "test_value", now, now)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Test session created: {session}")
        return session
    except Exception as e:
        logger.error(f"Error creating test session: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        sys.exit(1)


def create_test_messages(session_id, user_id, agent_id):
    """Create test messages in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info(f"Creating test messages for session {session_id}...")
        now = datetime.utcnow()
        
        # Create a user message
        user_message_id = f"user-msg-{uuid.uuid4()}"
        user_content = "Hello, this is a test message."
        user_raw_payload = json.dumps({
            "role": "user",
            "content": user_content
        })
        
        cursor.execute(
            """
            INSERT INTO messages (
                id, session_id, role, text_content, raw_payload, 
                created_at, updated_at, message_type, user_id
            ) VALUES (
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s
            )
            RETURNING id, role, text_content
            """,
            (
                user_message_id,
                session_id,
                "user",
                user_content,
                user_raw_payload,
                now,
                now,
                "text",
                user_id
            )
        )
        user_message = cursor.fetchone()
        logger.info(f"✅ User message created: {user_message}")
        
        # Create an assistant message with tool calls
        tool_calls = [{
            "id": f"tool-call-{uuid.uuid4()}",
            "type": "function",
            "function": {
                "name": "get_time",
                "arguments": "{}"
            }
        }]
        
        tool_outputs = [{
            "tool_call_id": tool_calls[0]["id"],
            "output": json.dumps({"time": now.isoformat()})
        }]
        
        assistant_message_id = f"assistant-msg-{uuid.uuid4()}"
        assistant_content = "Here is the current time."
        assistant_raw_payload = json.dumps({
            "role": "assistant",
            "content": assistant_content,
            "tool_calls": tool_calls
        })
        
        cursor.execute(
            """
            INSERT INTO messages (
                id, session_id, role, text_content, raw_payload, 
                created_at, updated_at, message_type, user_id, agent_id,
                tool_calls, tool_outputs
            ) VALUES (
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s,
                %s, %s
            )
            RETURNING id, role, text_content
            """,
            (
                assistant_message_id,
                session_id,
                "assistant",
                assistant_content,
                assistant_raw_payload,
                now,
                now,
                "text",
                user_id,
                agent_id,
                json.dumps(tool_calls),
                json.dumps(tool_outputs)
            )
        )
        assistant_message = cursor.fetchone()
        logger.info(f"✅ Assistant message created: {assistant_message}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "user_message": user_message,
            "assistant_message": assistant_message
        }
    except Exception as e:
        logger.error(f"Error creating test messages: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        sys.exit(1)


def create_test_memory(user_id):
    """Create a test memory in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info(f"Creating test memory for user {user_id}...")
        now = datetime.utcnow()
        memory_id = f"memory-{uuid.uuid4()}"
        memory_content = "This is a test memory for integration verification."
        memory_metadata = {
            "source": "integration_test",
            "importance": "high"
        }
        
        cursor.execute(
            """
            INSERT INTO memories (
                id, user_id, content, metadata, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            )
            RETURNING id, content
            """,
            (
                memory_id,
                user_id,
                memory_content,
                json.dumps(memory_metadata),
                now,
                now
            )
        )
        memory = cursor.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Test memory created: {memory}")
        return memory
    except Exception as e:
        logger.error(f"Error creating test memory: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        sys.exit(1)


def verify_data():
    """Verify that all data was created correctly."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info("Verifying data in all tables...")
        
        # Check users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()["count"]
        logger.info(f"Users count: {user_count}")
        
        # Check agents
        cursor.execute("SELECT COUNT(*) FROM agents")
        agent_count = cursor.fetchone()["count"]
        logger.info(f"Agents count: {agent_count}")
        
        # Check sessions
        cursor.execute("SELECT COUNT(*) FROM sessions")
        session_count = cursor.fetchone()["count"]
        logger.info(f"Sessions count: {session_count}")
        
        # Check session_metadata
        cursor.execute("SELECT COUNT(*) FROM session_metadata")
        metadata_count = cursor.fetchone()["count"]
        logger.info(f"Session metadata count: {metadata_count}")
        
        # Check messages
        cursor.execute("SELECT COUNT(*) FROM messages")
        message_count = cursor.fetchone()["count"]
        logger.info(f"Messages count: {message_count}")
        
        # Check memories
        cursor.execute("SELECT COUNT(*) FROM memories")
        memory_count = cursor.fetchone()["count"]
        logger.info(f"Memories count: {memory_count}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        if (user_count > 0 and agent_count > 0 and session_count > 0 and 
            metadata_count > 0 and message_count > 0 and memory_count > 0):
            logger.info("✅ All tables have data - verification successful!")
            return True
        else:
            logger.error("❌ Some tables don't have data - verification failed!")
            return False
    except Exception as e:
        logger.error(f"Error verifying data: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        sys.exit(1)


def main():
    """Main function to verify the database integration."""
    logger.info("🔍 Starting database integration verification")
    
    # Step 1: Create default user
    user = create_default_user()
    
    # Step 2: Create test agent
    agent = create_test_agent()
    
    # Step 3: Create test session
    session = create_test_session(user["id"])
    
    # Step 4: Create test messages
    messages = create_test_messages(session["id"], user["id"], agent["id"])
    
    # Step 5: Create test memory
    memory = create_test_memory(user["id"])
    
    # Step 6: Verify all data
    success = verify_data()
    
    if success:
        logger.info("🎉 Database integration verification successful!")
    else:
        logger.error("❌ Database integration verification failed!")


if __name__ == "__main__":
    main() 