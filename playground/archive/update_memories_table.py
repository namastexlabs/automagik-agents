#!/usr/bin/env python

"""
Migration script to update the memories table structure.

This script adds the following columns to the memories table:
- name: Name of the memory
- description: Detailed description of the memory
- session_id: Associated session ID (UUID)
- read_mode: How the memory is accessed by the agent (system_prompt, tool_call)
- access: Access permissions for the memory (read, write, both)

It also preserves existing data where possible.
"""

import psycopg2
import psycopg2.extras
import logging
import sys
import os
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("memories-migration")

# Get database connection parameters from environment or use defaults
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "automagik")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

def get_connection():
    """Get a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        # Use DictCursor for easier column access
        conn.cursor_factory = psycopg2.extras.DictCursor
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        raise

def update_memories_table():
    """Update the memories table structure."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Check if the table exists
            cur.execute(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'memories')"
            )
            table_exists = cur.fetchone()[0]
            
            if not table_exists:
                logger.info("Memories table doesn't exist, creating it with the new structure")
                # Create the table with all the new fields
                cur.execute("""
                CREATE TABLE memories (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name TEXT NOT NULL,
                    description TEXT,
                    content TEXT,
                    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    read_mode TEXT,
                    access TEXT,
                    metadata JSONB,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
                """)
                conn.commit()
                logger.info("Created new memories table with updated structure")
                return
            
            # Check existing columns
            cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'memories'
            """)
            existing_columns = [row[0] for row in cur.fetchall()]
            
            # Add missing columns
            columns_to_add = {
                "name": "TEXT",
                "description": "TEXT",
                "session_id": "UUID REFERENCES sessions(id) ON DELETE CASCADE",
                "read_mode": "TEXT",
                "access": "TEXT"
            }
            
            for column, data_type in columns_to_add.items():
                if column not in existing_columns:
                    logger.info(f"Adding column '{column}' to memories table")
                    cur.execute(f"ALTER TABLE memories ADD COLUMN {column} {data_type}")
            
            # If name column was just added, populate it with default values
            if "name" not in existing_columns:
                logger.info("Populating name column with default values")
                cur.execute("""
                UPDATE memories 
                SET name = 'Untitled Memory ' || id::text
                WHERE name IS NULL
                """)
                
                # Make name column NOT NULL
                cur.execute("ALTER TABLE memories ALTER COLUMN name SET NOT NULL")
            
            # Set default access and read_mode if they were just added
            if "access" not in existing_columns:
                logger.info("Setting default access values")
                cur.execute("UPDATE memories SET access = 'read' WHERE access IS NULL")
                
            if "read_mode" not in existing_columns:
                logger.info("Setting default read_mode values")
                cur.execute("UPDATE memories SET read_mode = 'system_prompt' WHERE read_mode IS NULL")
            
            # Add sample memory if specified
            if "--add-sample" in sys.argv:
                add_sample_memory(cur)
                
            conn.commit()
            logger.info("Successfully updated memories table structure")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error updating memories table: {str(e)}")
        raise
    finally:
        conn.close()

def add_sample_memory(cursor):
    """Add a sample memory record."""
    try:
        # Check if the sample memory already exists
        cursor.execute("SELECT id FROM memories WHERE name = 'agent_knowledge'")
        if cursor.fetchone() is not None:
            logger.info("Sample memory 'agent_knowledge' already exists")
            return
            
        # Get first available session_id
        cursor.execute("SELECT id FROM sessions LIMIT 1")
        result = cursor.fetchone()
        session_id = result[0] if result else None
        
        description = """**`agent_knowledge`** is a special dynamic variable that accumulates insights from every prompt creation session. Whenever you help create or refine prompts, you learn new techniques, edge cases, and preferences. These are stored in **`agent_knowledge`** for future reference.

- **Usage**  
  - Always consult `agent_knowledge` before following any other instructions.  
  - If there's a conflict between newly provided instructions and the knowledge in `agent_knowledge`, prioritize `agent_knowledge` unless the user explicitly overrides it.  
  - Continuously update `agent_knowledge` with new insights or best practices acquired during prompt creation.  
"""
        
        content = "- Initial Knowledge"
        
        cursor.execute("""
        INSERT INTO memories (
            id, name, description, content, session_id, user_id, read_mode, access, created_at, updated_at
        ) VALUES (
            gen_random_uuid(), %s, %s, %s, %s, 1, 'system_prompt', 'read', NOW(), NOW()
        )
        """, (
            "agent_knowledge", 
            description,
            content,
            session_id
        ))
        
        logger.info("Added sample 'agent_knowledge' memory")
    except Exception as e:
        logger.error(f"Error adding sample memory: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Starting memories table migration")
    update_memories_table()
    logger.info("Memories table migration completed")
