#!/usr/bin/env python3
"""
Migration script to update the session ID type from TEXT to UUID in the database.
This script will:
1. Create a temporary table with the new UUID schema
2. Copy data from the old table to the new table, converting TEXT IDs to UUIDs
3. Rename tables to complete the migration
"""

import logging
import os
import sys
import uuid
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Determine the project root directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Load environment variables from .env in the project root
env_path = os.path.join(project_root, '.env')
logger.info(f"Looking for .env file at: {env_path}")
if os.path.exists(env_path):
    logger.info(f"Found .env file at: {env_path}")
    load_dotenv(dotenv_path=env_path)
    logger.info("Environment variables loaded from .env file")
else:
    logger.warning(f"No .env file found at {env_path}")

# Try to get database configuration from various sources
database_url = os.getenv("DATABASE_URL")
if database_url:
    logger.info(f"Using DATABASE_URL")
    conn_string = database_url
else:
    # Use individual parameters
    db_host = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("POSTGRES_USER") or os.getenv("DB_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD", "postgres")
    
    conn_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    logger.info(f"Using database connection: {db_host}:{db_port}/{db_name}")

def is_valid_uuid(val):
    """Check if a string is a valid UUID."""
    try:
        uuid_obj = uuid.UUID(val)
        return True
    except (ValueError, AttributeError):
        return False

def format_as_uuid(val):
    """Format a string as a UUID, or generate a new UUID if invalid."""
    try:
        if val:
            # Try to parse it as a UUID to validate
            uuid_obj = uuid.UUID(val)
            return str(uuid_obj)
        else:
            # Generate a new UUID if the value is empty
            return str(uuid.uuid4())
    except (ValueError, AttributeError):
        # For invalid values, generate a new UUID
        logger.warning(f"Invalid session ID '{val}', generating a new UUID")
        return str(uuid.uuid4())

def migrate_database():
    """Perform the migration to update session IDs to UUID type."""
    try:
        # Connect to the database
        logger.info("Connecting to database...")
        conn = psycopg2.connect(conn_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if sessions table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'sessions'
            )
        """)
        sessions_exists = cursor.fetchone()[0]
        
        if not sessions_exists:
            logger.warning("Sessions table does not exist. No migration needed.")
            return
        
        # Check the data type of the id column
        cursor.execute("""
            SELECT data_type FROM information_schema.columns 
            WHERE table_name = 'sessions' AND column_name = 'id'
        """)
        id_type = cursor.fetchone()[0]
        
        logger.info(f"Current sessions.id type: {id_type}")
        
        if id_type.lower() == 'uuid':
            logger.info("Sessions.id is already UUID type. No migration needed.")
            return
        
        # Begin transaction
        conn.set_isolation_level(0)  # AUTOCOMMIT
        
        # Step 1: Create backup of the original table
        logger.info("Creating backup of sessions table...")
        cursor.execute("CREATE TABLE sessions_backup AS SELECT * FROM sessions")
        logger.info("Sessions table backed up to sessions_backup")
        
        # Step 2: Create new sessions table with UUID column
        logger.info("Creating new sessions table with UUID column...")
        cursor.execute("""
            CREATE TABLE sessions_new (
                id UUID PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                platform TEXT,
                created_at TIMESTAMP WITH TIME ZONE,
                updated_at TIMESTAMP WITH TIME ZONE
            )
        """)
        
        # Step 3: Get all session IDs from the original table
        cursor.execute("SELECT id FROM sessions")
        session_ids = cursor.fetchall()
        logger.info(f"Found {len(session_ids)} sessions to migrate")
        
        # Step 4: Insert data into the new table, converting session IDs to UUID
        migrated_count = 0
        for (session_id,) in session_ids:
            try:
                # Convert to UUID
                uuid_str = format_as_uuid(session_id)
                
                # Copy row with the new UUID
                cursor.execute("""
                    INSERT INTO sessions_new (id, user_id, platform, created_at, updated_at)
                    SELECT %s, user_id, platform, created_at, updated_at
                    FROM sessions WHERE id = %s
                """, (uuid_str, session_id))
                
                migrated_count += 1
            except Exception as e:
                logger.error(f"Error migrating session {session_id}: {str(e)}")
        
        logger.info(f"Successfully migrated {migrated_count} of {len(session_ids)} sessions")
        
        # Step 5: Create new session_metadata table with UUID column
        logger.info("Creating new session_metadata table with UUID column...")
        cursor.execute("""
            CREATE TABLE session_metadata_new (
                session_id UUID REFERENCES sessions_new(id),
                key TEXT,
                value TEXT,
                created_at TIMESTAMP WITH TIME ZONE,
                updated_at TIMESTAMP WITH TIME ZONE,
                PRIMARY KEY (session_id, key)
            )
        """)
        
        # Step 6: Get all session_metadata rows
        cursor.execute("SELECT session_id FROM session_metadata")
        session_metadata_ids = cursor.fetchall()
        logger.info(f"Found {len(session_metadata_ids)} session metadata rows to migrate")
        
        # Step 7: Copy session_metadata data
        metadata_migrated = 0
        for (session_id,) in session_metadata_ids:
            try:
                # Convert to UUID
                uuid_str = format_as_uuid(session_id)
                
                # Copy rows with the new UUID
                cursor.execute("""
                    INSERT INTO session_metadata_new (session_id, key, value, created_at, updated_at)
                    SELECT %s, key, value, created_at, updated_at
                    FROM session_metadata WHERE session_id = %s
                """, (uuid_str, session_id))
                
                metadata_migrated += 1
            except Exception as e:
                logger.error(f"Error migrating session_metadata for session {session_id}: {str(e)}")
        
        logger.info(f"Successfully migrated {metadata_migrated} of {len(session_metadata_ids)} session metadata rows")
        
        # Step 8: Create new messages table with UUID reference
        logger.info("Creating new messages table with UUID reference...")
        cursor.execute("""
        CREATE TABLE messages_new (
            id TEXT PRIMARY KEY,
            session_id UUID REFERENCES sessions(id),
            role TEXT,
            text_content TEXT,
            raw_payload JSONB,
            media_url TEXT,
            mime_type TEXT,
            message_type TEXT,
            user_id INTEGER,
            agent_id INTEGER,
            system_prompt TEXT,
            user_feedback TEXT,
            flagged TEXT,
            channel_payload JSONB,
            tool_calls JSONB,
            tool_outputs JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
        """)
        conn.commit()
        
        # Step 9: Get all messages
        cursor.execute("SELECT session_id FROM messages")
        old_session_ids = cursor.fetchall()
        session_ids = set([row[0] for row in old_session_ids])
        
        # Step 10: Copy messages data
        for session_id in session_ids:
            try:
                # Get the new UUID for this session
                new_id = session_id_mapping.get(session_id)
                if not new_id:
                    logger.warning(f"No mapping found for session {session_id}, skipping messages migration")
                    continue
                
                # Migration for this session
                logger.info(f"Migrating messages for session {session_id} -> {new_id}")
                cursor.execute("""
                INSERT INTO messages_new (
                    id, session_id, role, text_content, raw_payload,
                    media_url, mime_type, message_type,
                    user_id, agent_id, system_prompt, user_feedback,
                    flagged, channel_payload, tool_calls, tool_outputs,
                    created_at, updated_at
                )
                SELECT 
                    id, %s::uuid, role, text_content, raw_payload,
                    media_url, mime_type, message_type,
                    user_id, agent_id, system_prompt, user_feedback,
                    flagged, channel_payload, tool_calls, tool_outputs,
                    created_at, updated_at
                FROM messages WHERE session_id = %s
                """, (new_id, session_id))
                conn.commit()
            except Exception as e:
                logger.error(f"Error migrating messages for session {session_id}: {str(e)}")
                conn.rollback()
        
        # Step 11: Rename tables
        logger.info("Renaming message tables...")
        cursor.execute("ALTER TABLE messages RENAME TO messages_old")
        cursor.execute("ALTER TABLE messages_new RENAME TO messages")
        
        # Step 12: Swap tables
        logger.info("Swapping tables to complete the migration...")
        cursor.execute("ALTER TABLE sessions RENAME TO sessions_old")
        cursor.execute("ALTER TABLE sessions_new RENAME TO sessions")
        cursor.execute("ALTER TABLE session_metadata RENAME TO session_metadata_old")
        cursor.execute("ALTER TABLE session_metadata_new RENAME TO session_metadata")
        
        logger.info("Migration completed successfully!")
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    logger.info("Starting session ID migration to UUID type")
    success = migrate_database()
    if success:
        logger.info("🎉 Migration completed successfully!")
    else:
        logger.error("❌ Migration failed!") 