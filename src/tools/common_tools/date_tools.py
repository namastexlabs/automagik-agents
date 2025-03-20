"""Date and time related tools for agents.

This module provides date and time tools that can be used by agents.
"""
import logging
from typing import Optional
from datetime import datetime, date

logger = logging.getLogger(__name__)

async def get_current_date_tool(format: str = "%Y-%m-%d") -> str:
    """Get the current date in the specified format.
    
    Args:
        format: The format to use for the date (strftime format)
        
    Returns:
        Current date as a formatted string
    """
    current_date = datetime.now().strftime(format)
    return current_date


async def get_current_time_tool(format: str = "%H:%M:%S") -> str:
    """Get the current time in the specified format.
    
    Args:
        format: The format to use for the time (strftime format)
        
    Returns:
        Current time as a formatted string
    """
    current_time = datetime.now().strftime(format)
    return current_time


async def format_date_tool(date_str: str, input_format: str = "%Y-%m-%d", output_format: str = "%B %d, %Y") -> str:
    """Format a date string from one format to another.
    
    Args:
        date_str: The date string to format
        input_format: The format of the input date string
        output_format: The desired output format
        
    Returns:
        Reformatted date string
    """
    try:
        parsed_date = datetime.strptime(date_str, input_format)
        formatted_date = parsed_date.strftime(output_format)
        return formatted_date
    except ValueError as e:
        return f"Error parsing date: {str(e)}" 