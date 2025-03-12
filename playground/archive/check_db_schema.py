#!/usr/bin/env python
from src.utils.db import execute_query

def check_db_schema():
    # Check messages table structure
    print("\n=== MESSAGES TABLE STRUCTURE ===")
    messages_cols = execute_query(
        "SELECT column_name, data_type FROM information_schema.columns "
        "WHERE table_name = 'messages' ORDER BY ordinal_position"
    )
    for col in messages_cols:
        print(f"{col['column_name']} - {col['data_type']}")
    
    # Check sessions table structure
    print("\n=== SESSIONS TABLE STRUCTURE ===")
    sessions_cols = execute_query(
        "SELECT column_name, data_type FROM information_schema.columns "
        "WHERE table_name = 'sessions' ORDER BY ordinal_position"
    )
    for col in sessions_cols:
        print(f"{col['column_name']} - {col['data_type']}")

    # Check if there are any messages in the database
    print("\n=== MESSAGE COUNT ===")
    message_count = execute_query("SELECT COUNT(*) FROM messages")[0]['count']
    print(f"Total messages: {message_count}")
    
    # Check a sample message if any exist
    if message_count > 0:
        print("\n=== SAMPLE MESSAGE ===")
        sample_msg = execute_query("SELECT * FROM messages LIMIT 1")[0]
        for key, value in sample_msg.items():
            print(f"{key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")

if __name__ == "__main__":
    check_db_schema()
