"""Database connection management and query utilities."""

import logging
import os
import time
import urllib.parse
import uuid
from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import psycopg2
import psycopg2.extensions
from psycopg2.extras import RealDictCursor, execute_values
from psycopg2.pool import ThreadedConnectionPool

from src.config import settings

# Configure logger
logger = logging.getLogger(__name__)

# Connection pool for database connections
_pool: Optional[ThreadedConnectionPool] = None

# Register UUID adapter for psycopg2
psycopg2.extensions.register_adapter(uuid.UUID, lambda u: psycopg2.extensions.AsIs(f"'{u}'"))


def safe_uuid(value: Any) -> Any:
    """Convert UUID objects to strings for safe database use.
    
    This is a utility function for cases where direct SQL queries are used
    instead of repository functions. It ensures UUID objects are properly
    converted to strings to prevent adaptation errors.
    
    Args:
        value: The value to convert if it's a UUID
        
    Returns:
        String representation of UUID or the original value
    """
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


def get_db_config() -> Dict[str, Any]:
    """Get database configuration from connection string or individual settings."""
    # Try to use DATABASE_URL first
    if settings.DATABASE_URL:
        try:
            # Parse the database URL
            env_db_url = os.environ.get("DATABASE_URL")
            actual_db_url = env_db_url if env_db_url else settings.DATABASE_URL
            parsed = urllib.parse.urlparse(actual_db_url)

            dbname = parsed.path.lstrip("/")

            return {
                "host": parsed.hostname,
                "port": parsed.port,
                "user": parsed.username,
                "password": parsed.password,
                "database": dbname,
                "client_encoding": "UTF8",  # Explicitly set client encoding to UTF8
            }
        except Exception as e:
            logger.warning(
                f"Failed to parse DATABASE_URL: {str(e)}. Falling back to individual settings."
            )

    # Fallback to individual settings
    return {
        "host": settings.POSTGRES_HOST,
        "port": settings.POSTGRES_PORT,
        "user": settings.POSTGRES_USER,
        "password": settings.POSTGRES_PASSWORD,
        "database": settings.POSTGRES_DB,
        "client_encoding": "UTF8",  # Explicitly set client encoding to UTF8
    }


def get_connection_pool() -> ThreadedConnectionPool:
    """Get or create a database connection pool."""
    global _pool

    if _pool is None:
        config = get_db_config()
        max_retries = 5
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                min_conn = getattr(settings, "POSTGRES_POOL_MIN", 1)
                max_conn = getattr(settings, "POSTGRES_POOL_MAX", 10)

                logger.info(
                    f"Connecting to PostgreSQL at {config['host']}:{config['port']}/{config['database']} with UTF8 encoding..."
                )

                # Can either connect with individual params or with a connection string
                if settings.DATABASE_URL and attempt == 0:
                    try:
                        # Add client_encoding to the connection string if not already present
                        dsn = settings.DATABASE_URL
                        if "client_encoding" not in dsn.lower():
                            if "?" in dsn:
                                dsn += "&client_encoding=UTF8"
                            else:
                                dsn += "?client_encoding=UTF8"

                        _pool = ThreadedConnectionPool(
                            minconn=min_conn, maxconn=max_conn, dsn=dsn
                        )
                        logger.info(
                            "Successfully connected to PostgreSQL using DATABASE_URL with UTF8 encoding"
                        )
                        # Make sure we set the encoding correctly
                        with _pool.getconn() as conn:
                            with conn.cursor() as cursor:
                                cursor.execute("SET client_encoding = 'UTF8';")
                                conn.commit()
                            _pool.putconn(conn)
                        break
                    except Exception as e:
                        logger.warning(
                            f"Failed to connect using DATABASE_URL: {str(e)}. Will try with individual params."
                        )

                # Try with individual params
                _pool = ThreadedConnectionPool(
                    minconn=min_conn,
                    maxconn=max_conn,
                    host=config["host"],
                    port=config["port"],
                    user=config["user"],
                    password=config["password"],
                    database=config["database"],
                    client_encoding="UTF8",  # Explicitly set client encoding
                )
                # Make sure we set the encoding correctly
                with _pool.getconn() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SET client_encoding = 'UTF8';")
                        conn.commit()
                    _pool.putconn(conn)
                logger.info(
                    "Successfully connected to PostgreSQL database with UTF8 encoding"
                )
                break
            except psycopg2.Error as e:
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Failed to connect to database (attempt {attempt + 1}/{max_retries}): {str(e)}"
                    )
                    time.sleep(retry_delay)
                else:
                    logger.error(
                        f"Failed to connect to database after {max_retries} attempts: {str(e)}"
                    )
                    raise

    return _pool


@contextmanager
def get_db_connection() -> Generator:
    """Get a database connection from the pool."""
    pool = get_connection_pool()
    conn = None
    try:
        conn = pool.getconn()
        # Ensure UTF-8 encoding for this connection
        with conn.cursor() as cursor:
            cursor.execute("SET client_encoding = 'UTF8';")
            conn.commit()
        yield conn
    finally:
        if conn:
            pool.putconn(conn)


@contextmanager
def get_db_cursor(commit: bool = False) -> Generator:
    """Get a database cursor with automatic commit/rollback."""
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            cursor.close()


def execute_query(query: str, params: tuple = None, fetch: bool = True, commit: bool = True) -> List[Dict[str, Any]]:
    """Execute a database query and return the results.
    
    Args:
        query: SQL query to execute
        params: Query parameters
        fetch: Whether to fetch and return results
        commit: Whether to commit the transaction
        
    Returns:
        List of records as dictionaries if fetch=True, otherwise empty list
    """
    with get_db_cursor(commit=commit) as cursor:
        cursor.execute(query, params)
        
        if fetch and cursor.description:
            return [dict(record) for record in cursor.fetchall()]
        return []


def execute_batch(query: str, params_list: List[Tuple], commit: bool = True) -> None:
    """Execute a batch query with multiple parameter sets.
    
    Args:
        query: SQL query template
        params_list: List of parameter tuples
        commit: Whether to commit the transaction
    """
    with get_db_cursor(commit=commit) as cursor:
        execute_values(cursor, query, params_list)


def close_connection_pool() -> None:
    """Close the database connection pool."""
    global _pool
    if _pool:
        _pool.closeall()
        _pool = None
        logger.info("Closed all database connections") 