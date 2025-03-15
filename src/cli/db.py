"""
Database management commands for Automagik Agents.
"""
import os
import typer
import logging
from dotenv import load_dotenv
import psycopg2

# Create the database command group
db_app = typer.Typer()

@db_app.callback()
def db_callback(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    Database management commands.
    
    Use these commands to initialize, backup, and manage the database.
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"

@db_app.command("init")
def db_init(
    force: bool = typer.Option(False, "--force", "-f", help="Force initialization even if database already exists")
):
    """
    Initialize the database if it doesn't exist yet.
    
    This command creates the database and required tables if they don't exist already.
    Use --force to recreate tables even if they already exist.
    """
    typer.echo("Initializing database...")
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger("db_init")
    
    # Load environment variables
    load_dotenv()
    
    # Get database connection parameters from environment
    db_host = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost") 
    db_port = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME", "automagik_agents")
    db_user = os.getenv("POSTGRES_USER") or os.getenv("DB_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD", "postgres")
    
    # Try to parse from DATABASE_URL if available
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        try:
            import urllib.parse
            parsed = urllib.parse.urlparse(database_url)
            db_host = parsed.hostname or db_host
            db_port = str(parsed.port) if parsed.port else db_port
            db_name = parsed.path.lstrip('/') or db_name
            db_user = parsed.username or db_user
            db_password = parsed.password or db_password
        except Exception as e:
            logger.warning(f"Error parsing DATABASE_URL: {str(e)}")
    
    typer.echo(f"Using database: {db_host}:{db_port}/{db_name}")
    
    # Check if database exists
    try:
        # Connect to postgres database to check if our target database exists
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname="postgres",
            user=db_user,
            password=db_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        database_exists = cursor.fetchone() is not None
        
        if database_exists and not force:
            typer.echo(f"Database '{db_name}' already exists.")
            
            # Check if tables already exist
            try:
                # Connect to the actual database
                db_conn = psycopg2.connect(
                    host=db_host,
                    port=db_port,
                    dbname=db_name,
                    user=db_user,
                    password=db_password
                )
                db_cursor = db_conn.cursor()
                
                # Check if sessions table exists
                db_cursor.execute("""
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = 'sessions'
                """)
                tables_exist = db_cursor.fetchone() is not None
                
                db_cursor.close()
                db_conn.close()
                
                if tables_exist:
                    typer.echo("Tables are already initialized. Use 'db reset' to reset the database.")
                    typer.echo("Database initialization skipped.")
                    cursor.close()
                    conn.close()
                    return
                else:
                    typer.echo("Database exists but tables are not initialized. Creating tables...")
            except Exception as e:
                typer.echo(f"Error checking tables: {str(e)}")
                typer.echo("Creating tables...")
        else:
            if not database_exists:
                typer.echo(f"Database '{db_name}' does not exist. Creating...")
                cursor.execute(f"CREATE DATABASE {db_name}")
                typer.echo(f"Database '{db_name}' created successfully.")
            elif force:
                typer.echo(f"Force flag set. Recreating database '{db_name}'...")
                
                # Close connections to database before dropping
                cursor.execute(f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{db_name}'
                    AND pid <> pg_backend_pid()
                """)
                
                cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
                cursor.execute(f"CREATE DATABASE {db_name}")
                typer.echo(f"Database '{db_name}' recreated successfully.")
        
        cursor.close()
        conn.close()
        
        # Create tables directly instead of importing from playground
        if create_required_tables_direct(db_host, db_port, db_name, db_user, db_password):
            typer.echo("✅ Database initialized successfully!")
        else:
            typer.echo("❌ Error creating tables. Check logs for details.")
            
    except Exception as e:
        typer.echo(f"❌ Database initialization failed: {str(e)}")
        
        # Provide more helpful error message for unique constraint issues
        if "duplicate key value violates unique constraint" in str(e) and "sessions_name_key" in str(e):
            typer.echo("\n⚠️ There are duplicate session names in the database.")
            typer.echo("Use '--force' to reset the database and clear all existing data.")
            
        raise typer.Exit(code=1)

def create_required_tables_direct(host, port, dbname, user, password):
    """Create the required tables for Automagik Agents directly."""
    import logging
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    import psycopg2
    
    logger = logging.getLogger("db_init")
    
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
        
        # Create tables if they don't exist
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
                    run_id INTEGER DEFAULT 0,
                    system_prompt TEXT,
                    created_at TIMESTAMP WITH TIME ZONE,
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """,
            "sessions": """
                CREATE TABLE IF NOT EXISTS sessions (
                    id UUID PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    agent_id INTEGER REFERENCES agents(id),
                    name TEXT UNIQUE,
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
                CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at DESC);
                -- Remove the non-unique index on name as we have a UNIQUE constraint now
                DROP INDEX IF EXISTS idx_sessions_name;
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
                    agent_id INTEGER REFERENCES agents(id) ON DELETE CASCADE,
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
        
        # Create a trigger to increment run_id when an agent is used
        cursor.execute("""
        CREATE OR REPLACE FUNCTION increment_agent_run_id()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Increment the run_id for the agent being used
            UPDATE agents
            SET run_id = COALESCE(run_id, 0) + 1
            WHERE id = NEW.agent_id;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """)
        
        cursor.execute("""
        DROP TRIGGER IF EXISTS increment_agent_run_id_on_message ON messages;
        """)
        
        cursor.execute("""
        CREATE TRIGGER increment_agent_run_id_on_message
        AFTER INSERT ON messages
        FOR EACH ROW
        WHEN (NEW.role = 'user')
        EXECUTE FUNCTION increment_agent_run_id();
        """)
        conn.commit()
        logger.info("✅ Added trigger to increment agent run_id")
        
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
            
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False

@db_app.command("reset")
def db_reset(
    confirm: bool = typer.Option(False, "--yes", "-y", help="Confirm database reset without prompt")
):
    """
    Reset the database, removing all existing data.
    
    This command drops and recreates the database with empty tables.
    WARNING: This will delete ALL data in the database. Use with caution!
    """
    if not confirm:
        confirmed = typer.confirm("⚠️ This will DELETE ALL DATA in the database. Are you sure?", default=False)
        if not confirmed:
            typer.echo("Database reset cancelled.")
            return
    
    typer.echo("Resetting database...")
    
    # Use the db_init command with force flag
    db_init(force=True)
    
    typer.echo("✅ Database has been reset successfully!")

@db_app.command("clear")
def db_clear(
    confirm: bool = typer.Option(False, "--yes", "-y", help="Confirm database clear without prompt"),
    no_default_user: bool = typer.Option(False, "--no-default-user", help="Skip creating the default user after clearing")
):
    """
    Clear all data from the database while preserving the schema.
    
    This command truncates all tables but keeps the database structure intact.
    WARNING: This will delete ALL data in the database. Use with caution!
    """
    if not confirm:
        confirmed = typer.confirm("⚠️ This will DELETE ALL DATA in the database but keep the schema. Are you sure?", default=False)
        if not confirmed:
            typer.echo("Database clear cancelled.")
            return
    
    typer.echo("Clearing all data from database...")
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger("db_clear")
    
    # Load environment variables
    load_dotenv()
    
    # Get database connection parameters from environment
    db_host = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost") 
    db_port = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME", "automagik_agents")
    db_user = os.getenv("POSTGRES_USER") or os.getenv("DB_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD", "postgres")
    
    # Try to parse from DATABASE_URL if available
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        try:
            import urllib.parse
            parsed = urllib.parse.urlparse(database_url)
            db_host = parsed.hostname or db_host
            db_port = str(parsed.port) if parsed.port else db_port
            db_name = parsed.path.lstrip('/') or db_name
            db_user = parsed.username or db_user
            db_password = parsed.password or db_password
        except Exception as e:
            logger.warning(f"Error parsing DATABASE_URL: {str(e)}")
    
    typer.echo(f"Using database: {db_host}:{db_port}/{db_name}")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Get all tables in the public schema
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)
        all_tables = [table[0] for table in cursor.fetchall()]
        
        if not all_tables:
            typer.echo("No tables found in database.")
            return
        
        typer.echo(f"Found {len(all_tables)} tables in the database")
        
        # Define table clearing order to respect foreign key constraints
        # If a table is not in this list, it will be cleared after the ordered ones
        table_order = [
            "memories",       # Clear first as it references sessions, users, and agents
            "messages",       # References sessions, users, and agents
            "sessions",       # References users and agents
            "users",          # No foreign keys to other tables
            "agents"          # No foreign keys to other tables
        ]
        
        # Sort tables based on defined order
        ordered_tables = []
        
        # First add tables in our defined order (if they exist in the database)
        for table in table_order:
            if table in all_tables:
                ordered_tables.append(table)
                all_tables.remove(table)
        
        # Then add any remaining tables
        ordered_tables.extend(all_tables)
        
        typer.echo("Clearing tables in the following order to respect foreign key constraints:")
        for i, table in enumerate(ordered_tables):
            typer.echo(f"  {i+1}. {table}")
        
        # Truncate each table in order
        for table_name in ordered_tables:
            typer.echo(f"  - Clearing table: {table_name}")
            try:
                # Try with CASCADE first, which will handle foreign key constraints
                try:
                    cursor.execute(f'TRUNCATE TABLE "{table_name}" CASCADE;')
                    typer.echo(f"    ✓ Table {table_name} cleared successfully (with CASCADE)")
                except Exception as e:
                    # If CASCADE fails, try without it
                    if "permission denied" in str(e):
                        try:
                            cursor.execute(f'TRUNCATE TABLE "{table_name}";')
                            typer.echo(f"    ✓ Table {table_name} cleared successfully")
                        except Exception as e2:
                            # If regular TRUNCATE fails too, try DELETE as a last resort
                            typer.echo(f"    ⚠️ TRUNCATE failed, trying DELETE FROM...")
                            cursor.execute(f'DELETE FROM "{table_name}";')
                            typer.echo(f"    ✓ Table {table_name} cleared using DELETE (might be slower)")
                    else:
                        raise e
            except Exception as e:
                typer.echo(f"    ✗ Failed to clear table {table_name}: {str(e)}")
        
        # Create default user if not exists
        if not no_default_user:
            cursor.execute("SELECT COUNT(*) FROM users WHERE id = 1")
            if cursor.fetchone()[0] == 0:
                logger.info("Creating default user...")
                cursor.execute("""
                    INSERT INTO users (id, email, created_at, updated_at)
                    VALUES (1, 'admin@automagik', NOW(), NOW())
                """)
                conn.commit()
                typer.echo("✅ Created default user (ID: 1)")
        else:
            typer.echo("Skipping default user creation as requested")
        
        # Close the connection
        cursor.close()
        conn.close()
        
        typer.echo("✅ All data has been cleared from the database!")
        
    except Exception as e:
        logger.error(f"❌ Failed to clear database: {e}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False 