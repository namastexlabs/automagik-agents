#!/usr/bin/env python3
"""Cleanup script to fix inconsistent read_mode values in the memories table.

This script:
1. Converts any memories with read_mode='tool_calling' to 'tool'
2. Deletes any test memories created by the test script
"""

import os
import logging
from src.db import execute_query, list_memories, update_memory

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cleanup_database():
    """Fix inconsistent read_mode values and delete test memories."""
    try:
        # 1. First check what we have
        logger.info("Checking current read_mode distribution:")
        
        # Use repository function to get all memories
        memories = list_memories()
        
        # Count memories by read_mode
        read_mode_counts = {}
        for memory in memories:
            if getattr(memory, 'agent_id', None) == 3:
                read_mode = getattr(memory, 'read_mode', None)
                if read_mode not in read_mode_counts:
                    read_mode_counts[read_mode] = 0
                read_mode_counts[read_mode] += 1
        
        for read_mode, count in read_mode_counts.items():
            logger.info(f"  - {read_mode}: {count} memories")
        
        # 2. Update 'tool_calling' to 'tool'
        logger.info("Converting 'tool_calling' read_mode to 'tool'...")
        updated_count = 0
        
        for memory in memories:
            if getattr(memory, 'read_mode', None) == 'tool_calling':
                # Update the memory with new read_mode
                memory_dict = memory.dict() if hasattr(memory, 'dict') else memory.__dict__
                memory_dict['read_mode'] = 'tool'
                update_result = update_memory(memory.id, memory_dict)
                if update_result:
                    updated_count += 1
        
        logger.info(f"Updated {updated_count} memories from 'tool_calling' to 'tool'")
        
        # 3. Delete test memories
        # For deletion, we still need to use execute_query since we don't have a 
        # repository function that supports complex WHERE clauses
        logger.info("Deleting test memories...")
        delete_query = "DELETE FROM memories WHERE name LIKE 'api\_test\_%' ESCAPE '\\'"
        delete_result = execute_query(delete_query)
        logger.info(f"Deleted test memories: {delete_result}")
        
        # 4. Verify the cleanup
        logger.info("Verifying cleanup:")
        
        # Use repository function to get updated list of memories
        updated_memories = list_memories()
        
        # Count memories by read_mode after updates
        updated_read_mode_counts = {}
        for memory in updated_memories:
            if getattr(memory, 'agent_id', None) == 3:
                read_mode = getattr(memory, 'read_mode', None)
                if read_mode not in updated_read_mode_counts:
                    updated_read_mode_counts[read_mode] = 0
                updated_read_mode_counts[read_mode] += 1
        
        for read_mode, count in updated_read_mode_counts.items():
            logger.info(f"  - {read_mode}: {count} memories")
        
        # 5. Make sure there are no test memories left
        test_query = "SELECT COUNT(*) as count FROM memories WHERE name LIKE 'api\_test\_%' ESCAPE '\\'"
        test_result = execute_query(test_query)
        test_count = 0
        
        if isinstance(test_result, list) and test_result:
            test_count = test_result[0].get('count', 0)
        elif test_result.get('rows', []):
            test_count = test_result.get('rows', [])[0].get('count', 0)
            
        if test_count == 0:
            logger.info("✅ All test memories have been successfully removed")
        else:
            logger.warning(f"⚠️ There are still {test_count} test memories in the database")
        
        logger.info("✅ Database cleanup completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during database cleanup: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting database cleanup for memory read_mode values...")
    success = cleanup_database()
    if success:
        logger.info("✅ Cleanup operation completed successfully")
    else:
        logger.error("❌ Cleanup operation failed") 