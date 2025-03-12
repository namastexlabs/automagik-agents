#!/usr/bin/env python3
"""
Migration script to remove the message_timestamp column from the messages table.

This script:
1. Makes sure all message_timestamp values are migrated to updated_at if needed
2. Removes the message_timestamp column from the messages table
"""

import sys
import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Add the project root to sys.path to allow imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Configure logging
from src.utils.logging import configure_logging
configure_logging()
logger = logging.getLogger("remove_message_timestamp")

# Import database utilities
from src.utils.db import get_db_connection, execute_query

def remove_message_timestamp():
    """
    Migrate data from message_timestamp to updated_at and remove the message_timestamp column.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info("Starting migration to remove message_timestamp column...")
        
        # Check if message_timestamp column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'messages' AND column_name = 'message_timestamp'
        """)
        
        if not cursor.fetchone():
            logger.info("✅ message_timestamp column does not exist. No migration needed.")
            return True
        
        logger.info("message_timestamp column exists. Starting migration...")
        
        # 1. First synchronize any missing updated_at values from message_timestamp
        logger.info("Synchronizing updated_at from message_timestamp where needed...")
        cursor.execute("""
            UPDATE messages
            SET updated_at = message_timestamp
            WHERE message_timestamp IS NOT NULL AND 
                  (updated_at IS NULL OR updated_at < message_timestamp)
        """)
        
        sync_count = cursor.rowcount
        conn.commit()
        logger.info(f"Synchronized {sync_count} messages from message_timestamp to updated_at")
        
        # 2. Drop the message_timestamp column
        logger.info("Removing message_timestamp column...")
        cursor.execute("ALTER TABLE messages DROP COLUMN message_timestamp")
        conn.commit()
        
        logger.info("✅ Successfully removed message_timestamp column")
        
        # Close the database connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ Error during migration: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False
        
    return True

if __name__ == "__main__":
    if remove_message_timestamp():
        print("✅ Migration completed successfully")
        sys.exit(0)
    else:
        print("❌ Migration failed")
        sys.exit(1) 