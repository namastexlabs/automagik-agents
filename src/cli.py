import shutil
from pathlib import Path
import typer
import os
import uvicorn
from typing import Optional, List
from src.config import load_settings

app = typer.Typer()
api_app = typer.Typer()
db_app = typer.Typer()
app.add_typer(api_app, name="api")
app.add_typer(db_app, name="db")

def get_available_templates() -> List[str]:
    """Get list of available agent templates (full folder names)."""
    agents_dir = Path(__file__).resolve().parent.parent / 'src' / 'agents'
    templates = []
    for item in agents_dir.iterdir():
        if item.is_dir() and item.name not in ['models', '__pycache__']:
            templates.append(item.name)
    return templates

@app.command("create-agent")
def create_agent(
    name: str = typer.Option(..., "--name", "-n", help="Name of the new agent to create"),
    template: str = typer.Option("simple_agent", "--template", "-t", help="Template folder to use as base (e.g., 'simple_agent', 'notion_agent')")
):
    """
    Create a new agent by cloning an existing agent template.
    
    The template should be the full folder name from src/agents directory.
    By default, it uses the simple_agent template.
    """
    # Define the agents directory and the destination folder
    agents_dir = Path(__file__).resolve().parent.parent / 'src' / 'agents'
    destination = agents_dir / f"{name}_agent"
    
    # Check if destination already exists
    if destination.exists():
        typer.echo(f"Error: Folder {destination} already exists.")
        raise typer.Exit(code=1)

    # Get available templates
    available_templates = get_available_templates()
    if template not in available_templates:
        typer.echo(f"Error: Template '{template}' not found. Available templates: {', '.join(available_templates)}")
        raise typer.Exit(code=1)

    # Define the template folder
    template_path = agents_dir / template
    if not template_path.exists() or not template_path.is_dir():
        typer.echo(f"Error: Template folder {template_path} does not exist.")
        raise typer.Exit(code=1)

    # Copy the template folder to the destination folder
    shutil.copytree(template_path, destination)

    # Get the base names without _agent suffix for class naming
    template_base = template.replace('_agent', '')
    
    # Compute the new agent class name and the template class name
    new_agent_class = ''.join(word.capitalize() for word in name.split('_')) + "Agent"
    template_class = ''.join(word.capitalize() for word in template_base.split('_')) + "Agent"
    create_func_name = f"create_{name}_agent"
    template_func_name = f"create_{template_base}_agent"

    # Recursively update file contents and filenames in the destination folder
    for root, dirs, files in os.walk(destination, topdown=False):
        for file in files:
            file_path = Path(root) / file
            # Attempt to read file as text
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace class names and function names, but preserve config requirements
                new_content = content
                
                # Update import statements
                new_content = new_content.replace(
                    f"from src.agents.{template}.agent",
                    f"from src.agents.{name}_agent.agent"
                )
                new_content = new_content.replace(
                    f"from src.agents.{template_base}_agent.agent",
                    f"from src.agents.{name}_agent.agent"
                )
                
                # Only replace exact class name matches (with word boundaries)
                new_content = new_content.replace(f" {template_class}", f" {new_agent_class}")
                new_content = new_content.replace(f"({template_class}", f"({new_agent_class}")
                new_content = new_content.replace(f"[{template_class}", f"[{new_agent_class}")
                new_content = new_content.replace(f":{template_class}", f":{new_agent_class}")
                
                # Replace function names
                new_content = new_content.replace(template_func_name, create_func_name)
                
                # Special handling for __init__.py to update docstrings
                if file == "__init__.py":
                    new_content = new_content.replace(
                        f"Create and initialize a {template_class} instance",
                        f"Create and initialize a {new_agent_class} instance"
                    )
                
                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
            except Exception as e:
                typer.echo(f"Warning: Could not process file {file_path}: {str(e)}")
                continue

            # Rename file if it contains the template name
            if template_base in file:
                new_file = file.replace(template_base, name)
                new_file_path = Path(root) / new_file
                file_path.rename(new_file_path)

        # Rename directories if needed
        for dir_name in dirs:
            if template_base in dir_name:
                old_dir = Path(root) / dir_name
                new_dir = Path(root) / dir_name.replace(template_base, name)
                os.rename(old_dir, new_dir)

    typer.echo(f"Agent '{name}' created successfully in {destination} (based on {template} template).")
    typer.echo(f"The new agent class is named '{new_agent_class}'.")
    typer.echo(f"The initialization function is named '{create_func_name}'.")
    typer.echo("\nYou can now:")
    typer.echo(f"1. Edit {destination}/prompts/prompt.py to customize the agent's system prompt")
    typer.echo(f"2. Edit {destination}/agent.py to customize agent behavior")
    typer.echo(f"3. Edit {destination}/__init__.py to customize initialization config")

@api_app.command("start")
def start_api(
    host: str = typer.Option(None, "--host", "-h", help="Host to bind the server to (overrides AM_HOST from .env)"),
    port: int = typer.Option(None, "--port", "-p", help="Port to bind the server to (overrides AM_PORT from .env)"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload on code changes"),
    workers: Optional[int] = typer.Option(None, "--workers", "-w", help="Number of worker processes"),
):
    """
    Start the FastAPI server with uvicorn using settings from .env
    """
    # Load settings from .env
    settings = load_settings()
    
    # Use command line arguments if provided, otherwise use settings from .env
    final_host = host or settings.AM_HOST
    final_port = port or settings.AM_PORT

    typer.echo(f"Starting API server on {final_host}:{final_port}")
    uvicorn.run(
        "src.main:app",
        host=final_host,
        port=final_port,
        reload=reload,
        workers=workers
    )

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
    
    # Import here to avoid circular imports
    import psycopg2
    import logging
    from dotenv import load_dotenv
    
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
                    run_id INTEGER,
                    created_at TIMESTAMP WITH TIME ZONE,
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """,
            "sessions": """
                CREATE TABLE IF NOT EXISTS sessions (
                    id UUID PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
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

@app.callback()
def main():
    """
    Automagik CLI tool.
    """
    pass

if __name__ == "__main__":
    app()
