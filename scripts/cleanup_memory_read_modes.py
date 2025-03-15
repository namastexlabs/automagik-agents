#!/usr/bin/env python3
"""Cleanup script to fix inconsistent read_mode values in the memories table.

This script:
1. Converts any memories with read_mode='tool_calling' to 'tool'
2. Deletes any test memories created by the test script
"""

import os
import logging
from src.db import execute_query

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cleanup_database():
    """Fix inconsistent read_mode values and delete test memories."""
    try:
        # 1. First check what we have
        logger.info("Checking current read_mode distribution:")
        check_query = "SELECT read_mode, COUNT(*) as count FROM memories WHERE agent_id = 3 GROUP BY read_mode"
        result = execute_query(check_query)
        
        if isinstance(result, list):
            for row in result:
                logger.info(f"  - {row.get('read_mode')}: {row.get('count')} memories")
        else:
            rows = result.get('rows', [])
            for row in rows:
                logger.info(f"  - {row.get('read_mode')}: {row.get('count')} memories")
        
        # 2. Update 'tool_calling' to 'tool'
        logger.info("Converting 'tool_calling' read_mode to 'tool'...")
        update_query = "UPDATE memories SET read_mode = 'tool' WHERE read_mode = 'tool_calling'"
        update_result = execute_query(update_query)
        logger.info(f"Updated read_mode values: {update_result}")
        
        # 3. Delete test memories
        logger.info("Deleting test memories...")
        delete_query = "DELETE FROM memories WHERE name LIKE 'api\_test\_%' ESCAPE '\\'"
        delete_result = execute_query(delete_query)
        logger.info(f"Deleted test memories: {delete_result}")
        
        # 4. Verify the cleanup
        logger.info("Verifying cleanup:")
        verify_query = "SELECT read_mode, COUNT(*) as count FROM memories WHERE agent_id = 3 GROUP BY read_mode"
        verify_result = execute_query(verify_query)
        
        if isinstance(verify_result, list):
            for row in verify_result:
                logger.info(f"  - {row.get('read_mode')}: {row.get('count')} memories")
        else:
            rows = verify_result.get('rows', [])
            for row in rows:
                logger.info(f"  - {row.get('read_mode')}: {row.get('count')} memories")
        
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