#!/usr/bin/env python3
"""
Script to create ordered views in PostgreSQL for Automagik Agents.
This ensures that messages are displayed in a consistent order by updated_at timestamp.
"""

import logging
import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor

# Add the project root to sys.path to allow imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Configure logging
from src.utils.logging import configure_logging
configure_logging()
logger = logging.getLogger("create_ordered_views")

# Import database utilities
from src.utils.db import get_db_connection, execute_query

def create_ordered_views():
    """
    Create views that automatically order records by timestamp.
    """
    try:
        # Use the connection as a context manager with 'with'
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            logger.info("Creating ordered views in PostgreSQL...")
            
            # Drop existing views to avoid conflicts
            cursor.execute("DROP VIEW IF EXISTS ordered_sessions")
            cursor.execute("DROP VIEW IF EXISTS session_messages")
            cursor.execute("DROP VIEW IF EXISTS ordered_messages")
            conn.commit()
            logger.info("✅ Dropped existing views")
            
            # Create an ordered view for messages
            cursor.execute("""
                CREATE OR REPLACE VIEW ordered_messages AS
                SELECT * FROM messages 
                ORDER BY created_at DESC
            """)
            conn.commit()
            logger.info("✅ Created ordered_messages view")
            
            # Create an ordered view for messages by session
            cursor.execute("""
                CREATE OR REPLACE VIEW session_messages AS
                SELECT * FROM messages 
                ORDER BY session_id, created_at ASC
            """)
            conn.commit()
            logger.info("✅ Created session_messages view")
            
            # Create an ordered view for sessions with run information
            cursor.execute("""
                CREATE OR REPLACE VIEW ordered_sessions AS
                SELECT 
                    s.*, 
                    (SELECT MAX(created_at) FROM messages WHERE session_id = s.id AND role = 'user') as last_user_message_time,
                    (SELECT MAX(created_at) FROM messages WHERE session_id = s.id AND role = 'assistant') as last_assistant_message_time,
                    (SELECT COUNT(*) FROM messages WHERE session_id = s.id) as message_count,
                    (SELECT COUNT(*) FROM messages WHERE session_id = s.id AND role = 'user') as user_message_count,
                    (SELECT COUNT(*) FROM messages WHERE session_id = s.id AND role = 'assistant') as assistant_message_count
                FROM 
                    sessions s
                ORDER BY 
                    COALESCE(s.run_finished_at, s.updated_at) DESC NULLS LAST
            """)
            conn.commit()
            logger.info("✅ Created enhanced ordered_sessions view with run information")
            
            # Create an improved trigger to better handle timestamps
            cursor.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Always set updated_at to current time for any operation
                NEW.updated_at = NOW();
                
                -- For INSERT operations only
                IF TG_OP = 'INSERT' THEN
                    -- If created_at is NULL, set it to the current time
                    IF NEW.created_at IS NULL THEN
                        NEW.created_at = NEW.updated_at;
                    END IF;
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """)
            conn.commit()
            
            # Apply the trigger to the messages table
            cursor.execute("""
            DROP TRIGGER IF EXISTS update_messages_updated_at ON messages;
            """)
            
            cursor.execute("""
            CREATE TRIGGER update_messages_updated_at
            BEFORE UPDATE ON messages
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
            """)
            conn.commit()
            logger.info("✅ Created improved trigger for automatic updated_at timestamps")
            
            # Create an INSERT trigger to ensure created_at is always set
            cursor.execute("""
            CREATE OR REPLACE FUNCTION set_created_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Set created_at and updated_at to the same initial value on insert
                -- This ensures each message gets its own unique timestamp
                IF NEW.created_at IS NULL THEN
                    NEW.created_at = NOW();
                END IF;
                
                IF NEW.updated_at IS NULL THEN
                    NEW.updated_at = NEW.created_at;
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """)
            
            cursor.execute("""
            DROP TRIGGER IF EXISTS set_messages_created_at ON messages;
            """)
            
            cursor.execute("""
            CREATE TRIGGER set_messages_created_at
            BEFORE INSERT ON messages
            FOR EACH ROW
            EXECUTE FUNCTION set_created_at_column();
            """)
            conn.commit()
            logger.info("✅ Created trigger to ensure created_at is set on insert")
            
            # Create a similar trigger for the sessions table
            cursor.execute("""
            DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions;
            """)
            
            cursor.execute("""
            CREATE TRIGGER update_sessions_updated_at
            BEFORE UPDATE ON sessions
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
            """)
            
            cursor.execute("""
            DROP TRIGGER IF EXISTS set_sessions_created_at ON sessions;
            """)
            
            cursor.execute("""
            CREATE TRIGGER set_sessions_created_at
            BEFORE INSERT ON sessions
            FOR EACH ROW
            EXECUTE FUNCTION set_created_at_column();
            """)
            conn.commit()
            logger.info("✅ Created triggers for sessions table timestamps")
            
            # Add indexes to improve query performance
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);
            """)
            
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_updated_at ON messages(updated_at DESC);
            """)
            
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_session_created 
            ON messages(session_id, created_at ASC);
            """)
            
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_run_finished_at 
            ON sessions(run_finished_at DESC NULLS LAST);
            """)
            conn.commit()
            logger.info("✅ Added performance indexes for timestamp queries")
            
            # No need to manually close cursor and connection when using with statement
            # They will be automatically closed when exiting the with block
            
        logger.info("All ordered views and indexes created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating ordered views: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    if create_ordered_views():
        print("✅ Ordered views created successfully")
        sys.exit(0)
    else:
        print("❌ Failed to create ordered views")
        sys.exit(1) 