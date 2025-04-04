#!/usr/bin/env python
"""
Script to verify agent IDs are correctly set in message records.

This script checks for:
1. User messages that have NULL agent_id
2. Verifies if the fix correctly sets agent_id for new messages
3. Allows updating existing messages with proper agent_id

Usage:
    python scripts/verify_agent_message_ids.py [--fix] [--agent_id=N] [--session=UUID]

Options:
    --fix        Fix NULL agent_id values for user messages in the specified session
    --agent_id   Agent ID to use for fixing NULL agent_id values
    --session    Specific session to check/fix (defaults to all sessions)
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from typing import List, Optional

# Add the project root to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import (
    execute_query,
    get_agent, 
    get_session,
    get_db_cursor
)
from src.db.models import Session, Message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("verify_agent_message_ids")

def get_null_agent_id_messages(session_id: Optional[str] = None) -> List[dict]:
    """Get messages with NULL agent_id.
    
    Args:
        session_id: Optional session ID to filter by
        
    Returns:
        List of message dictionaries with NULL agent_id
    """
    query = """
        SELECT id, session_id, user_id, role, text_content, created_at
        FROM messages
        WHERE agent_id IS NULL AND role = 'user'
    """
    params = []
    
    if session_id:
        query += " AND session_id = %s"
        params.append(session_id)
        
    query += " ORDER BY created_at DESC"
    
    return execute_query(query, params)

def fix_null_agent_id_messages(agent_id: int, session_id: Optional[str] = None) -> int:
    """Fix messages with NULL agent_id.
    
    Args:
        agent_id: Agent ID to set for messages with NULL agent_id
        session_id: Optional session ID to filter by
        
    Returns:
        Number of messages updated
    """
    query = """
        UPDATE messages
        SET agent_id = %s
        WHERE agent_id IS NULL AND role = 'user'
    """
    params = [agent_id]
    
    if session_id:
        query += " AND session_id = %s"
        params.append(session_id)
        
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.rowcount

def main():
    parser = argparse.ArgumentParser(description="Verify agent IDs in message records")
    parser.add_argument("--fix", action="store_true", help="Fix NULL agent_id values")
    parser.add_argument("--agent_id", type=int, help="Agent ID to use for fixing")
    parser.add_argument("--session", type=str, help="Session ID to check/fix")
    
    args = parser.parse_args()
    
    # Find messages with NULL agent_id
    null_agent_messages = get_null_agent_id_messages(args.session)
    logger.info(f"Found {len(null_agent_messages)} user messages with NULL agent_id")
    
    # Show some sample messages
    if null_agent_messages:
        logger.info("Sample messages with NULL agent_id:")
        for msg in null_agent_messages[:5]:
            logger.info(f"ID: {msg['id']}, Session: {msg['session_id']}, Text: {msg['text_content'][:50]}...")
    
    # Fix NULL agent_id values if requested
    if args.fix:
        if not args.agent_id:
            logger.error("--agent_id is required when using --fix")
            return
            
        # Verify that the agent ID exists
        agent = get_agent(args.agent_id)
        if not agent:
            logger.error(f"Agent with ID {args.agent_id} not found")
            return
            
        # Fix the messages
        updated_count = fix_null_agent_id_messages(args.agent_id, args.session)
        logger.info(f"Updated {updated_count} messages with agent_id = {args.agent_id}")
    elif args.agent_id:
        logger.info("Use --fix to update messages with the provided agent_id")

if __name__ == "__main__":
    main() 