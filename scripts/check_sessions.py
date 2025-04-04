#!/usr/bin/env python
"""
Script to check remaining sessions in the database.
"""

import os
import sys

# Add the project root to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import list_sessions

def main():
    sessions = list_sessions()
    print(f'Total sessions remaining: {len(sessions)}')
    
    # Count auto-generated sessions
    auto_sessions = [s for s in sessions if s.name and s.name.startswith('Session-') and s.platform == 'automagik']
    print(f'Auto-generated sessions remaining: {len(auto_sessions)}')
    
    # Print some details about remaining auto-generated sessions
    if auto_sessions:
        print("\nRemaining auto-generated sessions:")
        for s in auto_sessions[:5]:  # Show up to 5 sessions
            print(f'- ID: {s.id}, Name: {s.name}, Platform: {s.platform}')
        if len(auto_sessions) > 5:
            print(f'... and {len(auto_sessions) - 5} more')
    else:
        print("\nNo auto-generated sessions remain.")
    
    # Print details about regular sessions
    regular_sessions = [s for s in sessions if s not in auto_sessions]
    if regular_sessions:
        print("\nRegular sessions:")
        for s in regular_sessions[:5]:  # Show up to 5 sessions
            print(f'- ID: {s.id}, Name: {s.name or "Unnamed"}, Platform: {s.platform or "Unknown"}')
        if len(regular_sessions) > 5:
            print(f'... and {len(regular_sessions) - 5} more')

if __name__ == "__main__":
    main() 