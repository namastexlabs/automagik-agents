#!/usr/bin/env python
"""
Script to clean up auto-generated sessions in the database.

This script deletes sessions that:
1. Have no associated messages
2. Have automagik platform and auto-generated names
3. Were created in a specified timeframe (optional)

Usage:
    python scripts/cleanup_sessions.py [--dry-run] [--days=N] [--keep-test]

Options:
    --dry-run    Show what would be deleted but don't actually delete
    --days=N     Only delete sessions created in the last N days (default: all)
    --keep-test  Keep sessions with 'test' in their names
"""

import argparse
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import List, Any

# Add the project root to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import (
    get_session, 
    list_sessions, 
    delete_session, 
    count_messages, 
    get_db_cursor
)
from src.db.models import Session, Message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("cleanup_sessions")

def is_auto_generated_session(session: Session) -> bool:
    """Check if a session appears to be auto-generated.
    
    Args:
        session: Session object from the database
        
    Returns:
        bool: True if the session appears to be auto-generated
    """
    # Check if the session name follows the auto-generated pattern
    name = session.name if session.name else ""
    platform = session.platform if session.platform else ""
    
    # Session-{uuid} pattern or session with automagik platform are likely auto-generated
    return (
        name.startswith("Session-") or 
        platform.lower() == "automagik"
    )

def has_messages(session_id: str) -> bool:
    """Check if a session has any associated messages.
    
    Args:
        session_id: The session ID to check
        
    Returns:
        bool: True if the session has messages
    """
    # Using the count_messages function from the repository
    count = count_messages(session_id)
    return count > 0

def cleanup_sessions(dry_run: bool = True, days: int = None, keep_test: bool = False) -> None:
    """Clean up auto-generated sessions.
    
    Args:
        dry_run: If True, don't actually delete sessions, just log what would be deleted
        days: Only consider sessions created in the last N days
        keep_test: If True, keep sessions with "test" in the name
    """
    # Get all sessions
    sessions = list_sessions()
    logger.info(f"Found {len(sessions)} sessions in the database")
    
    cutoff_date = None
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        logger.info(f"Only considering sessions created after {cutoff_date}")
    
    to_delete = []
    for session in sessions:
        session_id = str(session.id)
        name = session.name if session.name else ""
        platform = session.platform if session.platform else ""
        created_at = session.created_at
        
        # Skip sessions created before the cutoff date
        if cutoff_date and created_at and created_at < cutoff_date:
            logger.debug(f"Skipping session {session_id} (too old: {created_at})")
            continue
            
        # Skip test sessions if requested
        if keep_test and "test" in name.lower():
            logger.info(f"Keeping test session: {session_id} ({name})")
            continue
        
        # Check if this session is auto-generated and has no messages
        if is_auto_generated_session(session) and not has_messages(session_id):
            to_delete.append(session)
            logger.info(f"Marking for deletion: {session_id} ({name}, {platform})")
        else:
            if has_messages(session_id):
                logger.info(f"Keeping session with messages: {session_id} ({name})")
            else:
                logger.info(f"Keeping non-auto session: {session_id} ({name})")
    
    logger.info(f"Found {len(to_delete)} sessions to delete")
    
    if not dry_run:
        for session in to_delete:
            session_id = str(session.id)
            name = session.name if session.name else ""
            logger.info(f"Deleting session {session_id} ({name})")
            try:
                delete_session(session_id)
                logger.info(f"Deleted session {session_id}")
            except Exception as e:
                logger.error(f"Failed to delete session {session_id}: {e}")
    else:
        logger.info("Dry run - no sessions were actually deleted")

def main():
    parser = argparse.ArgumentParser(description="Clean up auto-generated sessions")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually delete sessions")
    parser.add_argument("--days", type=int, help="Only consider sessions created in the last N days")
    parser.add_argument("--keep-test", action="store_true", help="Keep sessions with 'test' in the name")
    
    args = parser.parse_args()
    
    cleanup_sessions(
        dry_run=args.dry_run, 
        days=args.days,
        keep_test=args.keep_test
    )

if __name__ == "__main__":
    main() 