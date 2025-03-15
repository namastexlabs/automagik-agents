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
    
    # First, connect to PostgreSQL to check if database exists
    try:
        # Create a connection to PostgreSQL (without a specific database)
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            dbname="postgres"
        )
        conn.autocommit = True  # Needed to create database
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"✅ Created database: {db_name}")
        else:
            logger.info(f"Database already exists: {db_name}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL or create database: {e}")
        return
    
    # Now connect to the target database and create tables
    create_required_tables(
        db_host, db_port, db_name, db_user, db_password, 
        logger=logger, force=force
    )
    
    typer.echo("✅ Database initialization completed!")

def create_required_tables(
    db_host, db_port, db_name, db_user, db_password,
    logger=None, force=False
):
    """Create required tables in the database."""
    if logger is None:
        logger = logging.getLogger("create_tables")
    
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
        
        # Create users table if not exists
        if force:
            logger.info("Force mode enabled. Dropping existing tables...")
            cursor.execute("DROP TABLE IF EXISTS user_session CASCADE")
            cursor.execute("DROP TABLE IF EXISTS users CASCADE")
            cursor.execute("DROP TABLE IF EXISTS agent_session CASCADE")
            cursor.execute("DROP TABLE IF EXISTS conversations CASCADE")
            cursor.execute("DROP TABLE IF EXISTS messages CASCADE")
            logger.info("Existing tables dropped.")
        
        # Create the users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email TEXT,
                phone_number VARCHAR(50),
                user_data JSONB,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        
        # Create the user_session table for tracking user authentication
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_session (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                session_id VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW(),
                expires_at TIMESTAMPTZ,
                session_data JSONB
            )
        """)
        
        # Create the agent_session table for tracking agent conversations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_session (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                agent_id VARCHAR(100) NOT NULL,
                session_id VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW(),
                session_data JSONB
            )
        """)
        
        # Create the conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW(),
                metadata JSONB
            )
        """)
        
        # Create the messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                conversation_id INTEGER REFERENCES conversations(id),
                user_id INTEGER REFERENCES users(id),
                role VARCHAR(20) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                metadata JSONB
            )
        """)
        
        # Create default user if needed
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0 or force:
            # Create default user
            cursor.execute("""
                INSERT INTO users (email, phone_number, user_data)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (
                "user@example.com", 
                "1234567890", 
                '{"name": "Default User", "is_default": true}'
            ))
            user_id = cursor.fetchone()[0]
            logger.info(f"✅ Created default user with ID: {user_id}")
        
        cursor.close()
        conn.close()
        
        logger.info("✅ All required tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        return False

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