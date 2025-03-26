"""Blackpearl API interface helpers.

This module provides utility functions and decorators for the Blackpearl API.
"""
import logging
import re
from typing import Dict, Any, Optional, Callable
from functools import wraps

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
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def format_api_request(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format request data by removing None values.
    
    Args:
        data: Request data
        
    Returns:
        Formatted request data
    """
    if data is None:
        return {}
        
    return {k: v for k, v in data.items() if v is not None}

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