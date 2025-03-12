#!/usr/bin/env python3
"""
Script to set up the PostgreSQL database and required tables for Automagik Agents.
This is helpful when setting up the project from scratch or on a new environment.
"""

import logging
import os
import sys
import subprocess
import getpass
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Determine the project root directory (parent of the directory this script is in)
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

# Read connection parameters from environment variables with fallbacks from other env vars
ENV_DB_HOST = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost")
ENV_DB_PORT = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")
ENV_DB_NAME = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME", "postgres")
ENV_DB_USER = os.getenv("POSTGRES_USER") or os.getenv("DB_USER", "postgres")
ENV_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD", "postgres")

# Try to parse from DATABASE_URL if available
database_url = os.getenv("DATABASE_URL")
if database_url:
    logger.info(f"Found DATABASE_URL: {database_url.split('@')[0]}...@...")
    try:
        import urllib.parse
        parsed = urllib.parse.urlparse(database_url)
        ENV_DB_HOST = parsed.hostname or ENV_DB_HOST
        ENV_DB_PORT = str(parsed.port) if parsed.port else ENV_DB_PORT
        ENV_DB_NAME = parsed.path.lstrip('/') or ENV_DB_NAME
        ENV_DB_USER = parsed.username or ENV_DB_USER
        ENV_DB_PASSWORD = parsed.password or ENV_DB_PASSWORD
        logger.info(f"Parsed database connection parameters from DATABASE_URL")
    except Exception as e:
        logger.warning(f"Error parsing DATABASE_URL: {str(e)}")

logger.info(f"Using database connection parameters: {ENV_DB_HOST}:{ENV_DB_PORT}/{ENV_DB_NAME}")


def test_connection(host, port, dbname, user, password):
    """Test a connection to PostgreSQL with the given parameters."""
    try:
        logger.info(f"Testing connection to PostgreSQL at {host}:{port}/{dbname} as {user}...")
        
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=5
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Connection successful! PostgreSQL version: {version}")
        return True, version
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False, str(e)


def get_user_connection_params():
    """Prompt user for connection parameters."""
    print("\nPlease enter PostgreSQL connection parameters (or press Enter to use default/current values):")
    
    host = input(f"Host [{ENV_DB_HOST}]: ").strip() or ENV_DB_HOST
    port = input(f"Port [{ENV_DB_PORT}]: ").strip() or ENV_DB_PORT
    dbname = input(f"Database [{ENV_DB_NAME}]: ").strip() or ENV_DB_NAME
    user = input(f"User [{ENV_DB_USER}]: ").strip() or ENV_DB_USER
    password = getpass.getpass(f"Password (hidden) [current]: ") or ENV_DB_PASSWORD
    
    return host, port, dbname, user, password


def create_database(host, port, user, password, dbname):
    """Create a new PostgreSQL database."""
    try:
        logger.info(f"Creating database '{dbname}'...")
        
        # Connect to the 'postgres' database to create a new database
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname="postgres",  # Connect to default postgres database
            user=user,
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # First check if database already exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        exists = cursor.fetchone()
        
        if exists:
            logger.info(f"Database '{dbname}' already exists, skipping creation")
        else:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {dbname}")
            logger.info(f"✅ Database '{dbname}' created successfully")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create database: {e}")
        return False


def create_required_tables(host, port, dbname, user, password):
    """Create the required tables for Automagik Agents."""
    try:
        logger.info(f"Creating required tables in '{dbname}'...")
        
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Check for existing sessions table with session_name column
        # If it does, we need to migrate data to name column
        logger.info("Checking for existing sessions table with session_name column...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'sessions' AND column_name = 'session_name'
        """)
        
        if cursor.fetchone():
            logger.info("Found sessions table with session_name column. Will rename to name...")
            
            # First check if the 'name' column already exists to avoid conflicts
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'sessions' AND column_name = 'name'
            """)
            
            if not cursor.fetchone():
                # If name column doesn't exist, add it
                cursor.execute("""
                    ALTER TABLE sessions 
                    ADD COLUMN name TEXT
                """)
                conn.commit()
                logger.info("Added name column to sessions table")
                
                # Copy data from session_name to name
                cursor.execute("""
                    UPDATE sessions
                    SET name = session_name
                    WHERE session_name IS NOT NULL
                """)
                
                rename_count = cursor.rowcount
                conn.commit()
                logger.info(f"Copied {rename_count} session names from session_name to name")
            else:
                logger.info("Both session_name and name columns exist. Will only drop session_name after recreation.")
                
            logger.info("Will drop session_name column during table recreation")
        
        # First check if messages table exists with message_timestamp column
        # If it does, migrate data before dropping
        logger.info("Checking for existing messages table with message_timestamp column...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'messages' AND column_name = 'message_timestamp'
        """)
        
        if cursor.fetchone():
            logger.info("Found messages table with message_timestamp column. Migrating data...")
            
            # Migrate message_timestamp data to updated_at
            cursor.execute("""
                UPDATE messages
                SET updated_at = message_timestamp
                WHERE message_timestamp IS NOT NULL AND 
                     (updated_at IS NULL OR updated_at < message_timestamp)
            """)
            
            sync_count = cursor.rowcount
            conn.commit()
            logger.info(f"Synchronized {sync_count} messages from message_timestamp to updated_at")
            logger.info("Migration completed. Will now recreate tables with updated schema.")
        
        # Drop existing tables if they exist
        drop_tables = [
            "messages", 
            "chat_messages",  # Include both to handle existing installations
            "session_metadata",  # Keep for backward compatibility, will be removed in future
            "sessions", 
            "memories", 
            "agents", 
            "users"
        ]
        
        # Drop existing views if they exist
        logger.info("Dropping existing views if they exist...")
        drop_views = [
            "ordered_sessions",
            "session_messages",
            "ordered_messages"
        ]
        
        for view in drop_views:
            try:
                cursor.execute(f"DROP VIEW IF EXISTS {view} CASCADE")
                conn.commit()
                logger.info(f"Dropped view '{view}' if it existed")
            except Exception as e:
                logger.warning(f"Error dropping view '{view}': {e}")
                conn.rollback()
        
        # Drop tables in reverse order to handle foreign key constraints
        logger.info("Dropping existing tables if they exist...")
        for table in drop_tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                conn.commit()
                logger.info(f"Dropped table '{table}' if it existed")
            except Exception as e:
                logger.warning(f"Error dropping table '{table}': {e}")
                conn.rollback()
        
        # Create the tables if they don't exist
        tables = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email TEXT,
                    phone_number VARCHAR(20),
                    user_data JSONB,
                    created_at TIMESTAMP WITH TIME ZONE,
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """,
            "agents": """
                CREATE TABLE IF NOT EXISTS agents (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR,
                    type VARCHAR,
                    model VARCHAR,
                    description VARCHAR,
                    version VARCHAR,
                    config JSONB,
                    active BOOLEAN DEFAULT TRUE,
                    run_id INTEGER,
                    created_at TIMESTAMP WITH TIME ZONE,
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """,
            "sessions": """
                CREATE TABLE IF NOT EXISTS sessions (
                    id UUID PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    agent_id INTEGER REFERENCES agents(id),
                    name TEXT,
                    platform TEXT,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP WITH TIME ZONE,
                    updated_at TIMESTAMP WITH TIME ZONE,
                    run_finished_at TIMESTAMP WITH TIME ZONE
                )
            """,
            # session_metadata table has been removed, metadata is now in sessions table
            
            "sessions_indexes": """
                CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
                CREATE INDEX IF NOT EXISTS idx_sessions_agent_id ON sessions(agent_id);
                CREATE INDEX IF NOT EXISTS idx_sessions_name ON sessions(name);
                CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at DESC);
            """,
            
            "messages": """
                CREATE TABLE IF NOT EXISTS messages (
                    id UUID PRIMARY KEY,
                    session_id UUID REFERENCES sessions(id),
                    user_id INTEGER REFERENCES users(id),
                    agent_id INTEGER REFERENCES agents(id),
                    role TEXT,
                    text_content TEXT,
                    media_url TEXT,
                    mime_type TEXT,
                    message_type TEXT,
                    raw_payload JSONB,
                    tool_calls JSONB,
                    tool_outputs JSONB,
                    system_prompt TEXT,
                    user_feedback TEXT,
                    flagged TEXT,
                    context JSONB,
                    created_at TIMESTAMP WITH TIME ZONE,
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """,
            "memories": """
                CREATE TABLE IF NOT EXISTS memories (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name TEXT NOT NULL,
                    description TEXT,
                    content TEXT,
                    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    read_mode TEXT,
                    access TEXT,
                    metadata JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """
        }
        
        # Execute each table creation statement
        for table_name, create_statement in tables.items():
            logger.info(f"Creating table '{table_name}'...")
            cursor.execute(create_statement)
            conn.commit()
            logger.info(f"✅ Table '{table_name}' created or already exists")
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        # Check which tables were successfully created
        missing_tables = set(tables.keys()) - set(existing_tables)
        if missing_tables:
            logger.warning(f"⚠️ Some tables are missing: {', '.join(missing_tables)}")
        else:
            logger.info("✅ All required tables have been created")
            
        # Insert sample data
        logger.info("Creating sample data...")
        
        # Create default user if not exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = 1")
        if cursor.fetchone()[0] == 0:
            logger.info("Creating default user...")
            cursor.execute("""
                INSERT INTO users (id, email, created_at, updated_at)
                VALUES (1, 'admin@automagik', NOW(), NOW())
            """)
            conn.commit()
            logger.info("✅ Created default user")
        
        # Create ordered views
        logger.info("Creating ordered views in PostgreSQL...")
        
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
            -- Simple update for updated_at timestamp, always preserve created_at
            NEW.updated_at = NOW();
            
            -- For UPDATE operations, always preserve the original created_at timestamp
            IF TG_OP = 'UPDATE' THEN
                NEW.created_at = OLD.created_at;
            -- For INSERT, set created_at if not provided
            ELSIF NEW.created_at IS NULL THEN
                NEW.created_at = NEW.updated_at;
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
        logger.info("✅ Created simplified trigger for automatic updated_at timestamps")

        # Create an INSERT trigger to ensure created_at is always set
        cursor.execute("""
        CREATE OR REPLACE FUNCTION set_created_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Set created_at and updated_at to the same initial value on insert
            -- This ensures each record gets its own unique timestamp
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
        
        # Remove all sample/test data creation
        # We don't want to create any blank sessions or memories at startup
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False


def update_env_file(host, port, dbname, user, password):
    """Update the .env file with the database connection parameters."""
    try:
        logger.info("Updating .env file with database connection parameters...")
        
        env_path = ".env"
        
        # Read the current .env file if it exists
        env_content = ""
        if os.path.isfile(env_path):
            with open(env_path, "r") as f:
                env_content = f.read()
        
        # Define replacements or additions
        replacements = {
            r'DB_HOST=.*': f'DB_HOST={host}',
            r'DB_PORT=.*': f'DB_PORT={port}',
            r'DB_NAME=.*': f'DB_NAME={dbname}',
            r'DB_USER=.*': f'DB_USER={user}',
            r'DB_PASSWORD=.*': f'DB_PASSWORD={password}'
        }
        
        # Apply replacements or add new variables
        import re
        for pattern, replacement in replacements.items():
            if re.search(pattern, env_content):
                env_content = re.sub(pattern, replacement, env_content)
            else:
                env_content += f"\n{replacement}"
        
        # Write the updated content back to the .env file
        with open(env_path, "w") as f:
            f.write(env_content)
        
        logger.info("✅ .env file updated successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to update .env file: {e}")
        return False


def main():
    """Main function."""
    logger.info("🔧 Starting PostgreSQL database setup for Automagik Agents")
    
    # Display environment variables
    logger.info("Current environment variables:")
    logger.info(f"  DB_HOST = {ENV_DB_HOST}")
    logger.info(f"  DB_PORT = {ENV_DB_PORT}")
    logger.info(f"  DB_NAME = {ENV_DB_NAME}")
    logger.info(f"  DB_USER = {ENV_DB_USER}")
    logger.info(f"  DB_PASSWORD = {'*' * len(ENV_DB_PASSWORD) if ENV_DB_PASSWORD else 'not set'}")
    
    # Test connection with current parameters
    success, result = test_connection(
        ENV_DB_HOST, ENV_DB_PORT, "postgres", ENV_DB_USER, ENV_DB_PASSWORD
    )
    
    # If connection fails, prompt for new parameters
    if not success:
        logger.warning("❌ Failed to connect with current parameters")
        logger.info("Let's configure the database connection...")
        
        # Get user input for connection parameters
        host, port, dbname, user, password = get_user_connection_params()
        
        # Test connection with new parameters (to postgres database first)
        success, result = test_connection(host, port, "postgres", user, password)
        
        if not success:
            logger.error("❌ Still unable to connect to PostgreSQL")
            logger.error("Please ensure PostgreSQL is installed and running")
            logger.error("Then run this script again with correct parameters")
            return
    else:
        host, port, dbname, user, password = ENV_DB_HOST, ENV_DB_PORT, ENV_DB_NAME, ENV_DB_USER, ENV_DB_PASSWORD
    
    # Confirm database name
    dbname = input(f"Enter the name for your database [{dbname}]: ").strip() or dbname
    
    # Create the database
    if create_database(host, port, user, password, dbname):
        # Create required tables
        if create_required_tables(host, port, dbname, user, password):
            # Update .env file
            update_env_file(host, port, dbname, user, password)
            
            logger.info("\n🎉 Database setup complete!")
            logger.info(f"PostgreSQL database '{dbname}' is ready to use")
            logger.info("You can now run the verification scripts:")
            logger.info("  1. python truncate_tables.py")
            logger.info("  2. python verify_integration.py")
            logger.info("  3. python test_message_history.py")
        else:
            logger.error("❌ Failed to create required tables")
    else:
        logger.error(f"❌ Failed to create database '{dbname}'")


if __name__ == "__main__":
    main() 