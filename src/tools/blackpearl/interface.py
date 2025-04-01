"""Blackpearl API interface helpers.

This module provides utility functions and decorators for the Blackpearl API.
"""
import logging
import re
from typing import Dict, Any, Optional, Callable
from functools import wraps
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

def validate_api_response(func):
    """Decorator to validate API response.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if result is None:
            logger.error(f"API call {func.__name__} returned None")
            raise ValueError(f"API call {func.__name__} returned None")
        return result
    return wrapper

def handle_api_error(func):
    """Decorator to handle API errors.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            # If result is a tuple with status code 204, it's a successful deletion
            if isinstance(result, tuple) and len(result) == 2 and result[0] == 204:
                return None
            return result
        except Exception as e:
            # If the error is about 204 response, it's actually a success
            if "204" in str(e) and "Attempt to decode JSON with unexpected mimetype" in str(e):
                return None
            logger.error(f"API error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def format_api_request(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format request data by removing None values and converting datetime to ISO format.
    
    Args:
        data: Request data
        
    Returns:
        Formatted request data
    """
    if data is None:
        return {}
        
    formatted_data = {}
    for k, v in data.items():
        if v is not None:
            if isinstance(v, datetime):
                # Ensure datetime is timezone-aware
                if v.tzinfo is None:
                    v = pytz.timezone('America/Sao_Paulo').localize(v)
                # Format with microseconds and timezone offset
                formatted_data[k] = v.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            else:
                formatted_data[k] = v
                
    return formatted_data

def filter_none_params(params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Filter out None values from request parameters.
    
    Args:
        params: Request parameters
        
    Returns:
        Filtered parameters
    """
    if params is None:
        return {}
        
    return {k: v for k, v in params.items() if v is not None} 