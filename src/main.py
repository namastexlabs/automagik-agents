import logging
from datetime import datetime

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

# Configure logging
configure_logging()

# Get our module's logger
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Create FastAPI application
    app = FastAPI(
        title=SERVICE_INFO["name"],
        description=SERVICE_INFO["description"],
        version=SERVICE_INFO["version"],
        docs_url=None,  # Disable default docs url
        redoc_url=None,  # Disable default redoc url
        openapi_url=None  # Disable default openapi url
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
    
    # Set up database message store regardless of environment
    try:
        logger.info("🔧 Initializing PostgreSQL message store for persistent storage")
        
        # First test database connection
        from src.utils.db import get_connection_pool, execute_query
        pool = get_connection_pool()
        
        # Test the connection with a simple query
        with pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                logger.info(f"✅ Database connection test successful: {version}")
                
                # Check if our tables exist
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sessions')")
                sessions_table_exists = cur.fetchone()[0]
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'chat_messages')")
                messages_table_exists = cur.fetchone()[0]
                cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
                users_table_exists = cur.fetchone()[0]
                
                logger.info(f"Database tables check - Sessions: {sessions_table_exists}, Messages: {messages_table_exists}, Users: {users_table_exists}")
                
                if not (sessions_table_exists and messages_table_exists and users_table_exists):
                    logger.error("❌ Required database tables are missing - sessions, messages, or users tables not found")
                    raise ValueError("Required database tables not found")
            pool.putconn(conn)
            
        logger.info("✅ Database connection pool initialized successfully")
        
        # Initialize PostgreSQL message store
        pg_store = PostgresMessageStore()
        
        # Create a test session and message to verify it works
        logger.info("🔍 Performing verification test of PostgresMessageStore...")
        import uuid
        from datetime import datetime
        test_session_id = f"startup-test-{uuid.uuid4()}"
        test_user_id = "default_user"
        
        # First ensure the default user exists
        default_user_exists = execute_query(
            "SELECT COUNT(*) as count FROM users WHERE id = %s",
            (test_user_id,)
        )
        
        if not default_user_exists or default_user_exists[0]["count"] == 0:
            logger.warning(f"⚠️ Default user '{test_user_id}' not found, creating it...")
            execute_query(
                """
                INSERT INTO users (id, email, created_at, updated_at) 
                VALUES (%s, %s, %s, %s)
                """,
                (test_user_id, "default@example.com", datetime.utcnow(), datetime.utcnow()),
                fetch=False
            )
            logger.info(f"✅ Created default user '{test_user_id}'")
        else:
            logger.info(f"✅ Default user '{test_user_id}' already exists")
        
        # Create a test session
        try:
            logger.info(f"Creating test session {test_session_id}...")
            execute_query(
                """
                INSERT INTO sessions (id, user_id, platform, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (test_session_id, test_user_id, "web", datetime.utcnow(), datetime.utcnow()),
                fetch=False
            )
            
            # Check if session was actually created
            session_exists = execute_query(
                "SELECT COUNT(*) as count FROM sessions WHERE id = %s",
                (test_session_id,)
            )
            
            if session_exists and session_exists[0]["count"] > 0:
                logger.info(f"✅ Test session {test_session_id} created successfully")
                
                # Try adding a test message
                test_message_id = f"startup-test-msg-{uuid.uuid4()}"
                execute_query(
                    """
                    INSERT INTO chat_messages (
                        id, session_id, role, text_content, raw_payload, 
                        message_timestamp, message_type, user_id
                    ) VALUES (
                        %s, %s, %s, %s, %s, 
                        %s, %s, %s
                    )
                    """,
                    (
                        test_message_id,
                        test_session_id,
                        "system",
                        "This is a test message to verify database connectivity",
                        '{"role": "system", "content": "This is a test message to verify database connectivity"}',
                        datetime.utcnow(),
                        "text",
                        test_user_id
                    ),
                    fetch=False
                )
                
                # Verify message was created
                message_exists = execute_query(
                    "SELECT COUNT(*) as count FROM chat_messages WHERE id = %s",
                    (test_message_id,)
                )
                
                if message_exists and message_exists[0]["count"] > 0:
                    logger.info(f"✅ Test message {test_message_id} created successfully")
                    logger.info("✅ Database store verification successful - can create sessions and messages")
                else:
                    logger.error(f"❌ Failed to create test message {test_message_id}")
                    raise ValueError("Failed to create test message")
                
                # Clean up test data
                execute_query("DELETE FROM chat_messages WHERE id = %s", (test_message_id,), fetch=False)
                execute_query("DELETE FROM sessions WHERE id = %s", (test_session_id,), fetch=False)
                logger.info("✅ Test data cleaned up")
            else:
                logger.error(f"❌ Failed to create test session {test_session_id}")
                raise ValueError("Failed to create test session")
        except Exception as test_e:
            logger.error(f"❌ Database verification test failed: {str(test_e)}")
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

    # Root and health endpoints (no auth required)
    @app.get("/")
    async def root():
        return {
            "status": "online",
            **SERVICE_INFO
        }

    @app.get("/health")
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
    uvicorn.run(
        "src.main:app",
        host=settings.AM_HOST,
        port=int(settings.AM_PORT),
        reload=True
    )
