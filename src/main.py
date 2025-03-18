import logging
from datetime import datetime
import json
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings, Environment
from src.utils.logging import configure_logging
from src.version import SERVICE_INFO
from src.auth import APIKeyMiddleware
from src.api.models import HealthResponse
from src.api.routes import router as api_router
from src.memory.message_history import MessageHistory
from src.memory.pg_message_store import PostgresMessageStore
from src.agents.models.agent_factory import AgentFactory
from src.db import execute_query, get_connection_pool, ensure_default_user_exists, create_session, Session

# Configure logging
configure_logging()

# Get our module's logger
logger = logging.getLogger(__name__)

def initialize_all_agents():
    """Initialize all available agents at startup.
    
    This ensures that agents are created and registered in the database
    before any API requests are made, rather than waiting for the first
    run request.
    """
    try:
        logger.info("🔧 Initializing all available agents...")
        
        # Discover all available agents
        AgentFactory.discover_agents()
        
        # Get the list of available agents
        available_agents = AgentFactory.list_available_agents()
        logger.info(f"Found {len(available_agents)} available agents: {', '.join(available_agents)}")
        
        # Initialize each agent
        for agent_name in available_agents:
            try:
                logger.info(f"Initializing agent: {agent_name}")
                # This will create and register the agent
                AgentFactory.get_agent(agent_name)
                logger.info(f"✅ Agent {agent_name} initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize agent {agent_name}: {str(e)}")
        
        logger.info("✅ All agents initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize agents: {str(e)}")
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Create FastAPI application
    app = FastAPI(
        title=SERVICE_INFO["name"],
        description=SERVICE_INFO["description"],
        version=SERVICE_INFO["version"],
        docs_url=None,  # Disable default docs url
        redoc_url=None,  # Disable default redoc url
        openapi_url=None,  # Disable default openapi url
        openapi_tags=[
            {
                "name": "System",
                "description": "System endpoints for status and health checking",
                "order": 1,
            },
            {
                "name": "Agents",
                "description": "Endpoints for listing available agents and running agent tasks",
                "order": 2,
            },
            {
                "name": "Sessions",
                "description": "Endpoints to manage and retrieve agent conversation sessions",
                "order": 3,
            },
        ]
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # Add authentication middleware
    app.add_middleware(APIKeyMiddleware)
    
    # Register startup event to initialize agents
    @app.on_event("startup")
    async def startup_event():
        # Initialize all agents at startup
        initialize_all_agents()
    
    # Set up database message store regardless of environment
    try:
        logger.info("🔧 Initializing PostgreSQL message store for persistent storage")
        
        # First test database connection
        from src.db.connection import get_connection_pool
        pool = get_connection_pool()
        
        # Test the connection with a simple query
        with pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                logger.info(f"✅ Database connection test successful: {version}")
                
                # Check if required tables exist
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sessions')")
                sessions_table_exists = cur.fetchone()[0]
                
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'messages')")
                messages_table_exists = cur.fetchone()[0]
                
                logger.info(f"Database tables check - Sessions: {sessions_table_exists}, Messages: {messages_table_exists}")
                
                if not (sessions_table_exists and messages_table_exists):
                    logger.error("❌ Required database tables are missing - sessions or messages tables not found")
                    raise ValueError("Required database tables not found")
            pool.putconn(conn)
            
        logger.info("✅ Database connection pool initialized successfully")
        
        # Initialize PostgreSQL message store
        pg_store = PostgresMessageStore()
        
        # Verify database functionality without creating persistent test data
        logger.info("🔍 Performing verification test of PostgresMessageStore without creating persistent sessions...")
        test_user_id = 1  # Use numeric ID instead of string
        
        # First ensure the default user exists using repository function
        ensure_default_user_exists(user_id=test_user_id, email="admin@automagik")
        
        # Verify message store functionality without creating test sessions
        # Use a transaction that we'll roll back to avoid persisting test data
        try:
            logger.info("Testing database message store functionality with transaction rollback...")
            with pool.getconn() as conn:
                conn.autocommit = False  # Start a transaction
                
                # Generate test UUIDs
                test_session_id = uuid.uuid4()
                test_message_id = uuid.uuid4()
                
                # Test inserting temporary session
                from src.db import create_session, Session, create_message, Message
                
                # Create a test session
                test_session = Session(
                    id=test_session_id,
                    user_id=test_user_id,
                    platform="verification_test",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                # Test inserting a test message
                test_message = Message(
                    id=test_message_id,
                    session_id=test_session_id,
                    role="user",
                    text_content="Test database connection",
                    raw_payload={"content": "Test database connection"},
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                # Create the session and message within the transaction
                with conn.cursor() as cur:
                    # Insert test session
                    cur.execute(
                        """
                        INSERT INTO sessions (id, user_id, platform, created_at, updated_at) 
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (test_session_id, test_user_id, "verification_test", datetime.utcnow(), datetime.utcnow())
                    )
                    
                    # Insert test message
                    cur.execute(
                        """
                        INSERT INTO messages (
                            id, session_id, role, text_content, raw_payload, created_at, updated_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            test_message_id,
                            test_session_id,
                            "user",
                            "Test database connection",
                            json.dumps({"content": "Test database connection"}),
                            datetime.utcnow(),
                            datetime.utcnow()
                        )
                    )
                    
                    # Verify we can read the data back
                    cur.execute("SELECT COUNT(*) FROM sessions WHERE id = %s", (test_session_id,))
                    session_count = cur.fetchone()[0]
                    
                    cur.execute("SELECT COUNT(*) FROM messages WHERE id = %s", (test_message_id,))
                    message_count = cur.fetchone()[0]
                    
                    if session_count > 0 and message_count > 0:
                        logger.info("✅ Database read/write test successful")
                    else:
                        logger.error("❌ Failed to verify database read operations")
                        raise Exception("Database verification failed")
                    
                    # Roll back the transaction to avoid persisting test data
                    conn.rollback()
                    logger.info("✅ Test transaction rolled back - no test data persisted")
                
                # Return connection to pool
                pool.putconn(conn)
                
            logger.info("✅ Database verification completed successfully without creating persistent test data")
        except Exception as test_e:
            logger.error(f"❌ Database verification test failed: {str(test_e)}")
            # Ensure any open transaction is rolled back
            try:
                conn.rollback()
            except:
                pass
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
            raise
        
        # Set PostgresMessageStore as the message store for MessageHistory
        MessageHistory.set_message_store(pg_store)
        
        # Log success
        logger.info("✅ PostgreSQL message store initialized and set for MessageHistory")
    except Exception as e:
        logger.error(f"❌ Failed to initialize PostgreSQL message store: {str(e)}")
        logger.error("⚠️ Application will fall back to in-memory message store")
        # Include traceback for debugging
        import traceback
        logger.error(f"Detailed error: {traceback.format_exc()}")
        
        # Explicitly set CacheMessageStore to make it clear we're falling back
        from src.memory.message_store import CacheMessageStore
        MessageHistory.set_message_store(CacheMessageStore())
        logger.warning("⚠️ Using in-memory CacheMessageStore as fallback - MESSAGES WILL NOT BE PERSISTED!")
    
    # Remove direct call since we're using the startup event
    # initialize_all_agents()

    # Root and health endpoints (no auth required)
    @app.get("/", tags=["System"], summary="Root Endpoint", description="Returns service information and status")
    async def root():
        return {
            "status": "online",
            **SERVICE_INFO
        }

    @app.get("/health", tags=["System"], summary="Health Check", description="Returns health status of the service")
    async def health_check() -> HealthResponse:
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow(),
            version=SERVICE_INFO["version"],
            environment=settings.AM_ENV
        )

    # Include API router (with versioned prefix)
    app.include_router(api_router, prefix="/api/v1")

    return app

# Create the app instance
app = create_app()

# Include Documentation router after app is created (to avoid circular imports)
from src.api.docs import router as docs_router
app.include_router(docs_router)

if __name__ == "__main__":
    import uvicorn
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description="Run the Sofia application server")
    parser.add_argument(
        "--reload", 
        action="store_true", 
        default=False,
        help="Enable auto-reload for development (default: False)"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default=settings.AM_HOST,
        help=f"Host to bind the server to (default: {settings.AM_HOST})"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(settings.AM_PORT),
        help=f"Port to bind the server to (default: {settings.AM_PORT})"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Log the configuration
    logger.info(f"Starting server with configuration:")
    logger.info(f"├── Host: {args.host}")
    logger.info(f"├── Port: {args.port}")
    logger.info(f"└── Auto-reload: {'Enabled' if args.reload else 'Disabled'}")
    
    # Run the server
    uvicorn.run(
        "src.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )
