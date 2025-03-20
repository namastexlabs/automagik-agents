#!/usr/bin/env python3
"""Test script for datetime tools.

This script demonstrates how to use the datetime tools and can be run directly
to verify the tools are working correctly.
"""
import asyncio
import sys
import os
import logging
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("datetime_tools_test")

# Import datetime tools
from src.tools.datetime.tool import get_current_date, get_current_time
from src.tools.datetime.schema import DatetimeOutput
from pydantic_ai.tools import RunContext
from pydantic_ai.messages import ModelRequest

async def test_datetime_tools():
    """Test the datetime tools functionality."""
    # Step 1: Create a RunContext for testing
    logger.info("Creating RunContext for testing...")
    mock_model = {"name": "mock-model", "provider": "mock"}
    mock_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    mock_prompt = ModelRequest(parts=[])
    
    ctx = RunContext({}, model=mock_model, usage=mock_usage, prompt=mock_prompt)
    
    # Step 2: Test get_current_date with default format
    logger.info("Testing get_current_date with default format...")
    date_result = await get_current_date(ctx)
    
    # Check that result matches expected format (YYYY-MM-DD)
    default_date = date_result["result"]
    logger.info(f"Default date result: {default_date}")
    
    # Verify format
    try:
        datetime.strptime(default_date, "%Y-%m-%d")
        logger.info("✅ Default date format is correct (YYYY-MM-DD)")
    except ValueError:
        logger.error(f"❌ Default date format is incorrect: {default_date}")
        return False
    
    # Step 3: Test get_current_date with custom format
    logger.info("Testing get_current_date with custom format...")
    custom_format = "%d/%m/%Y"
    custom_date_result = await get_current_date(ctx, format=custom_format)
    
    # Check that result matches custom format
    custom_date = custom_date_result["result"]
    logger.info(f"Custom date result: {custom_date}")
    
    # Verify format
    try:
        datetime.strptime(custom_date, custom_format)
        logger.info(f"✅ Custom date format is correct ({custom_format})")
    except ValueError:
        logger.error(f"❌ Custom date format is incorrect: {custom_date}")
        return False
    
    # Step 4: Test get_current_time with default format
    logger.info("Testing get_current_time with default format...")
    time_result = await get_current_time(ctx)
    
    # Check that result matches expected format (HH:MM)
    default_time = time_result["result"]
    logger.info(f"Default time result: {default_time}")
    
    # Verify format
    try:
        datetime.strptime(default_time, "%H:%M")
        logger.info("✅ Default time format is correct (HH:MM)")
    except ValueError:
        logger.error(f"❌ Default time format is incorrect: {default_time}")
        return False
    
    # Step 5: Test get_current_time with custom format
    logger.info("Testing get_current_time with custom format...")
    custom_format = "%I:%M %p"  # 12-hour format with AM/PM
    custom_time_result = await get_current_time(ctx, format=custom_format)
    
    # Check that result matches custom format
    custom_time = custom_time_result["result"]
    logger.info(f"Custom time result: {custom_time}")
    
    # Verify format
    try:
        datetime.strptime(custom_time, custom_format)
        logger.info(f"✅ Custom time format is correct ({custom_format})")
    except ValueError:
        logger.error(f"❌ Custom time format is incorrect: {custom_time}")
        return False
    
    # Step 6: Verify metadata structure
    logger.info("Verifying metadata structure...")
    if "timestamp" in date_result:
        logger.info(f"✅ Timestamp included in results: {date_result['timestamp']}")
    else:
        logger.error("❌ Timestamp missing from results")
        return False
    
    if "metadata" in date_result:
        logger.info(f"✅ Metadata included in results: {date_result['metadata']}")
    else:
        logger.error("❌ Metadata missing from results")
        return False
    
    logger.info("🎉 All datetime tools tests completed successfully!")
    return True

if __name__ == "__main__":
    logger.info("=== DATETIME TOOLS TEST SCRIPT ===")
    
    try:
        result = asyncio.run(test_datetime_tools())
        
        if result:
            logger.info("✅ All tests passed!")
            sys.exit(0)
        else:
            logger.error("❌ Some tests failed.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error during testing: {str(e)}", exc_info=True)
        sys.exit(1) 