#!/usr/bin/env python3
"""
Script to diagnose database connection issues and test different connection parameters.
"""

import logging
import os
import sys
import subprocess
import socket
import platform
from dotenv import load_dotenv
import psycopg2

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Read connection parameters from environment variables
ENV_DB_HOST = os.getenv("DB_HOST", "localhost")
ENV_DB_PORT = os.getenv("DB_PORT", "5432")
ENV_DB_NAME = os.getenv("DB_NAME", "postgres")
ENV_DB_USER = os.getenv("DB_USER", "postgres")
ENV_DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def check_postgres_running():
    """Check if PostgreSQL is running on the system."""
    system = platform.system().lower()
    
    logger.info(f"Checking if PostgreSQL is running on {system}...")
    
    if system == "linux" or system == "darwin":  # Linux or macOS
        try:
            result = subprocess.run(
                ["ps", "-ef"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            if "postgres" in result.stdout:
                logger.info("✅ PostgreSQL process found in process list")
                return True
            else:
                logger.warning("❌ No PostgreSQL process found in process list")
                return False
        except Exception as e:
            logger.error(f"Error checking PostgreSQL process: {e}")
            return False
    elif system == "windows":
        try:
            result = subprocess.run(
                ["tasklist"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            if "postgres" in result.stdout.lower():
                logger.info("✅ PostgreSQL process found in task list")
                return True
            else:
                logger.warning("❌ No PostgreSQL process found in task list")
                return False
        except Exception as e:
            logger.error(f"Error checking PostgreSQL process: {e}")
            return False
    else:
        logger.warning(f"Unsupported system: {system}")
        return False


def check_port_availability(host, port):
    """Check if the specified port is open on the host."""
    try:
        logger.info(f"Checking if port {port} is open on {host}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2 second timeout
        result = sock.connect_ex((host, int(port)))
        sock.close()
        
        if result == 0:
            logger.info(f"✅ Port {port} is open on {host}")
            return True
        else:
            logger.warning(f"❌ Port {port} is not open on {host}")
            return False
    except Exception as e:
        logger.error(f"Error checking port availability: {e}")
        return False


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


def suggest_fixes(error_message):
    """Suggest fixes based on the error message."""
    fixes = []
    
    if "Connection refused" in error_message:
        fixes.append("- Ensure PostgreSQL is running on the specified host and port")
        fixes.append("- Check if there's a firewall blocking connections")
        fixes.append("- Verify PostgreSQL is configured to accept TCP/IP connections")
        fixes.append("- Check pg_hba.conf to ensure it allows connections from your client")
    
    if "password authentication failed" in error_message.lower():
        fixes.append("- Check if the password is correct")
        fixes.append("- Verify the user has appropriate access rights")
    
    if "database" in error_message.lower() and "does not exist" in error_message.lower():
        fixes.append("- Create the database or use an existing one")
        fixes.append("- Check if the database name is spelled correctly")
    
    if "role" in error_message.lower() and "does not exist" in error_message.lower():
        fixes.append("- Create the user/role in PostgreSQL")
        fixes.append("- Check if the username is spelled correctly")
    
    if not fixes:
        fixes.append("- Check PostgreSQL logs for more detailed error information")
        fixes.append("- Ensure PostgreSQL is properly installed and configured")
    
    return fixes


def get_user_connection_params():
    """Prompt user for connection parameters."""
    print("\nPlease enter PostgreSQL connection parameters (or press Enter to use default values):")
    
    host = input(f"Host [{ENV_DB_HOST}]: ").strip() or ENV_DB_HOST
    port = input(f"Port [{ENV_DB_PORT}]: ").strip() or ENV_DB_PORT
    dbname = input(f"Database [{ENV_DB_NAME}]: ").strip() or ENV_DB_NAME
    user = input(f"User [{ENV_DB_USER}]: ").strip() or ENV_DB_USER
    password = input(f"Password (hidden) [{ENV_DB_PASSWORD}]: ") or ENV_DB_PASSWORD
    
    return host, port, dbname, user, password


def main():
    """Main function."""
    logger.info("🔍 Starting PostgreSQL connection diagnostic")
    
    # Display environment variables
    logger.info("Environment variables found:")
    logger.info(f"  DB_HOST = {ENV_DB_HOST}")
    logger.info(f"  DB_PORT = {ENV_DB_PORT}")
    logger.info(f"  DB_NAME = {ENV_DB_NAME}")
    logger.info(f"  DB_USER = {ENV_DB_USER}")
    logger.info(f"  DB_PASSWORD = {'*' * len(ENV_DB_PASSWORD) if ENV_DB_PASSWORD else 'not set'}")
    
    # Check if PostgreSQL is running
    is_running = check_postgres_running()
    
    # Check port availability
    port_available = check_port_availability(ENV_DB_HOST, ENV_DB_PORT)
    
    # Test connection with environment variables
    success, result = test_connection(
        ENV_DB_HOST, ENV_DB_PORT, ENV_DB_NAME, ENV_DB_USER, ENV_DB_PASSWORD
    )
    
    if success:
        logger.info("✅ Connection successful with environment variables!")
        logger.info(f"PostgreSQL version: {result}")
        return
    else:
        logger.error("❌ Connection failed with environment variables")
        
        # Suggest fixes
        fixes = suggest_fixes(result)
        logger.info("\nPossible solutions:")
        for fix in fixes:
            logger.info(fix)
    
    # Ask if user wants to try with different parameters
    try_different = input("\nDo you want to try different connection parameters? (y/N): ").lower() == 'y'
    
    if try_different:
        while True:
            # Get user input for connection parameters
            host, port, dbname, user, password = get_user_connection_params()
            
            # Test connection with user-provided parameters
            success, result = test_connection(host, port, dbname, user, password)
            
            if success:
                logger.info("\n✅ Connection successful with new parameters!")
                logger.info(f"PostgreSQL version: {result}")
                
                # Suggest updating .env file
                update_env = input("\nDo you want to update your .env file with these parameters? (y/N): ").lower() == 'y'
                
                if update_env:
                    try:
                        with open(".env", "r") as f:
                            env_content = f.read()
                        
                        # Replace or add connection parameters
                        replacements = {
                            r'DB_HOST=.*': f'DB_HOST={host}',
                            r'DB_PORT=.*': f'DB_PORT={port}',
                            r'DB_NAME=.*': f'DB_NAME={dbname}',
                            r'DB_USER=.*': f'DB_USER={user}',
                            r'DB_PASSWORD=.*': f'DB_PASSWORD={password}'
                        }
                        
                        for pattern, replacement in replacements.items():
                            import re
                            if re.search(pattern, env_content):
                                env_content = re.sub(pattern, replacement, env_content)
                            else:
                                env_content += f"\n{replacement}"
                        
                        with open(".env", "w") as f:
                            f.write(env_content)
                        
                        logger.info("✅ .env file updated successfully")
                    except Exception as e:
                        logger.error(f"Error updating .env file: {e}")
                
                break
            else:
                # Suggest fixes
                fixes = suggest_fixes(result)
                logger.info("\nPossible solutions:")
                for fix in fixes:
                    logger.info(fix)
                
                retry = input("\nDo you want to try again with different parameters? (y/N): ").lower() == 'y'
                if not retry:
                    break
    
    logger.info("\n🔍 Diagnostic complete")


if __name__ == "__main__":
    main() 