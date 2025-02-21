"""Date and time tools for Sofia."""

from datetime import datetime
from pydantic_ai import RunContext
from typing import Dict

def get_current_date(ctx: RunContext[Dict]) -> str:
    """Get the current date in ISO format (YYYY-MM-DD).
    
    Args:
        ctx: The context.
        
    Returns:
        Current date in ISO format.
    """
    return datetime.now().date().isoformat()

def get_current_time(ctx: RunContext[Dict]) -> str:
    """Get the current time in 24-hour format (HH:MM).
    
    Args:
        ctx: The context.
        
    Returns:
        Current time in 24-hour format.
    """
    return datetime.now().strftime("%H:%M")
