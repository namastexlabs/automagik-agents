#!/usr/bin/env python3
"""
Synchronize message timestamps script for Automagik Agents.

This script ensures that message_timestamp, created_at, and updated_at 
fields in the messages table are properly synchronized.
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
logger = logging.getLogger("synchronize_timestamps")

# Import database utilities
from src.utils.db import get_db_connection, execute_query

def synchronize_message_timestamps():
    """
    Synchronize message_timestamp, created_at, and updated_at fields in the messages table.
    
    For each message:
    1. If message_timestamp exists but created_at or updated_at is NULL, use message_timestamp for those fields
    2. If created_at exists but message_timestamp is NULL, use created_at for message_timestamp
    3. If both message_timestamp and created_at are NULL, use the current time for all fields
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info("Starting synchronization of message timestamps...")
        
        # 1. First check how many messages need updating
        cursor.execute("""
            SELECT 
                COUNT(*) as total_messages,
                COUNT(*) FILTER (WHERE message_timestamp IS NULL) as missing_timestamp,
                COUNT(*) FILTER (WHERE created_at IS NULL) as missing_created_at,
                COUNT(*) FILTER (WHERE updated_at IS NULL) as missing_updated_at
            FROM messages
        """)
        stats = cursor.fetchone()
        
        logger.info(f"Found {stats['total_messages']} total messages")
        logger.info(f"- {stats['missing_timestamp']} messages missing message_timestamp")
        logger.info(f"- {stats['missing_created_at']} messages missing created_at")
        logger.info(f"- {stats['missing_updated_at']} messages missing updated_at")
        
        # 2. Update messages where message_timestamp exists but created_at or updated_at is NULL
        cursor.execute("""
            UPDATE messages
            SET 
                created_at = message_timestamp,
                updated_at = message_timestamp
            WHERE 
                message_timestamp IS NOT NULL AND
                (created_at IS NULL OR updated_at IS NULL)
            RETURNING COUNT(*) as updated_count
        """)
        updated_from_timestamp = cursor.fetchone()
        conn.commit()
        
        if updated_from_timestamp and 'updated_count' in updated_from_timestamp:
            logger.info(f"Updated {updated_from_timestamp['updated_count']} messages using message_timestamp")
        
        # 3. Update messages where created_at exists but message_timestamp is NULL
        cursor.execute("""
            UPDATE messages
            SET 
                message_timestamp = created_at,
                updated_at = created_at
            WHERE 
                created_at IS NOT NULL AND
                message_timestamp IS NULL
            RETURNING COUNT(*) as updated_count
        """)
        updated_from_created_at = cursor.fetchone()
        conn.commit()
        
        if updated_from_created_at and 'updated_count' in updated_from_created_at:
            logger.info(f"Updated {updated_from_created_at['updated_count']} messages using created_at")
        
        # 4. Update messages where both message_timestamp and created_at are NULL
        now = datetime.utcnow()
        cursor.execute("""
            UPDATE messages
            SET 
                message_timestamp = %s,
                created_at = %s,
                updated_at = %s
            WHERE 
                message_timestamp IS NULL AND
                created_at IS NULL
            RETURNING COUNT(*) as updated_count
        """, (now, now, now))
        updated_with_now = cursor.fetchone()
        conn.commit()
        
        if updated_with_now and 'updated_count' in updated_with_now:
            logger.info(f"Updated {updated_with_now['updated_count']} messages using current time")
        
        # 5. Verify all messages now have proper timestamps
        cursor.execute("""
            SELECT 
                COUNT(*) as total_messages,
                COUNT(*) FILTER (WHERE message_timestamp IS NULL) as missing_timestamp,
                COUNT(*) FILTER (WHERE created_at IS NULL) as missing_created_at,
                COUNT(*) FILTER (WHERE updated_at IS NULL) as missing_updated_at
            FROM messages
        """)
        after_stats = cursor.fetchone()
        
        logger.info("After synchronization:")
        logger.info(f"- {after_stats['missing_timestamp']} messages still missing message_timestamp")
        logger.info(f"- {after_stats['missing_created_at']} messages still missing created_at")
        logger.info(f"- {after_stats['missing_updated_at']} messages still missing updated_at")
        
        if (after_stats['missing_timestamp'] == 0 and 
            after_stats['missing_created_at'] == 0 and 
            after_stats['missing_updated_at'] == 0):
            logger.info("✅ Synchronization completed successfully. All messages have proper timestamps.")
        else:
            logger.warning("⚠️ Synchronization completed but some messages still have missing timestamps.")
            
        # Close the database connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ Error synchronizing message timestamps: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False
        
    return True

if __name__ == "__main__":
    if synchronize_message_timestamps():
        print("✅ Message timestamp synchronization completed successfully")
        sys.exit(0)
    else:
        print("❌ Failed to synchronize message timestamps")
        sys.exit(1) 