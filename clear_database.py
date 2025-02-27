#!/usr/bin/env python3
"""
Script to clear all database tables.
WARNING: This will delete ALL data in the database. Use with caution!
"""

import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("clear_database")

def clear_database():
    """Clear all tables in the database."""
    try:
        # Import the database utility
        from src.utils.db import execute_query
        
        logger.info("Starting database clearing process...")
        
        # Get a list of all tables in the database
        tables = execute_query(
            """
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
            """
        )
        
        if not tables:
            logger.info("No tables found in the database.")
            return
        
        table_names = [table["tablename"] for table in tables]
        logger.info(f"Found {len(table_names)} tables: {', '.join(table_names)}")
        
        # Ask for confirmation
        confirm = input(f"Are you sure you want to delete ALL data from {len(table_names)} tables? (yes/no): ")
        if confirm.lower() != "yes":
            logger.info("Operation cancelled.")
            return
        
        # Disable foreign key constraints temporarily
        execute_query("SET session_replication_role = 'replica';", fetch=False)
        
        # Clear each table
        for table_name in table_names:
            try:
                logger.info(f"Clearing table: {table_name}")
                execute_query(f"TRUNCATE TABLE {table_name} CASCADE;", fetch=False)
                logger.info(f"✅ Table {table_name} cleared successfully")
            except Exception as e:
                logger.error(f"Error clearing table {table_name}: {str(e)}")
        
        # Re-enable foreign key constraints
        execute_query("SET session_replication_role = 'origin';", fetch=False)
        
        logger.info("Database clearing process completed successfully.")
        
        # Create default user with ID 1 if users table exists
        if "users" in table_names:
            try:
                logger.info("Creating default user with ID 1...")
                execute_query(
                    """
                    INSERT INTO users (id, email, created_at, updated_at, user_data) 
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        1,
                        "user1@example.com",
                        datetime.utcnow(),
                        datetime.utcnow(),
                        '{"name": "Default User"}'
                    ),
                    fetch=False
                )
                logger.info("✅ Default user created successfully")
            except Exception as e:
                logger.error(f"Error creating default user: {str(e)}")
        
    except ImportError as e:
        logger.error(f"Failed to import database utilities: {str(e)}")
        logger.error("Make sure you're running this script from the project root directory.")
        return
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")

if __name__ == "__main__":
    print("WARNING: This script will delete ALL data in the database!")
    print("Make sure you have a backup if you need the data.")
    print()
    
    try:
        clear_database()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1) 