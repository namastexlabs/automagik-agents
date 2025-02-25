#!/usr/bin/env python3
"""
Script to truncate database tables for Automagik Agents.
"""

import logging
import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import database utilities
from src.utils.db import execute_query, get_connection_pool

def truncate_tables(tables):
    """
    Truncate the specified database tables.
    
    Args:
        tables: List of table names to truncate
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get a connection from the pool
        pool = get_connection_pool()
        with pool.getconn() as conn:
            # Disable foreign key constraints temporarily
            with conn.cursor() as cursor:
                cursor.execute("SET session_replication_role = 'replica';")
                
                # Truncate each table
                for table in tables:
                    logger.info(f"Truncating table: {table}")
                    cursor.execute(f"TRUNCATE TABLE {table} CASCADE;")
                
                # Re-enable foreign key constraints
                cursor.execute("SET session_replication_role = 'origin';")
                
            conn.commit()
            pool.putconn(conn)
            
        logger.info(f"Successfully truncated tables: {', '.join(tables)}")
        return True
        
    except Exception as e:
        logger.error(f"Error truncating tables: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False

def main():
    """Main function to truncate database tables."""
    tables_to_truncate = ["sessions", "chat_messages"]
    
    logger.info(f"Starting table truncation for: {', '.join(tables_to_truncate)}")
    success = truncate_tables(tables_to_truncate)
    
    if success:
        logger.info("✅ All specified tables have been truncated successfully")
    else:
        logger.error("❌ Failed to truncate tables")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 