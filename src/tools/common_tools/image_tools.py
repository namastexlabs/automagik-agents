"""Image processing tools for pydantic-ai agents.

This module provides reusable tools for processing images in agents.
"""

import logging
from typing import Dict, Optional, Any, Union
from pydantic_ai import ImageUrl, BinaryContent, RunContext

logger = logging.getLogger(__name__)

async def process_image_url(ctx: RunContext[Dict], url: str) -> Dict[str, Any]:
    """Process an image from a URL.
    
    This tool allows an agent to process an image from a URL by directly using
    the ImageUrl capability of pydantic-ai.
    
    Args:
        ctx: Run context with agent context
        url: URL of the image to process
        
    Returns:
        Dictionary containing processing information
    """
    try:
        # In a real implementation, this would be passed to the LLM
        # But in this example we'll just return metadata
        return {
            "success": True,
            "source": "url",
            "url": url,
            "processed": True,
            "message": "Image URL processed successfully"
        }
    except Exception as e:
        logger.error(f"Error processing image URL: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
        
async def process_image_data(ctx: RunContext[Dict], 
                             data: bytes, 
                             media_type: str = "image/jpeg") -> Dict[str, Any]:
    """Process image data directly.
    
    This tool allows an agent to process binary image data directly using
    the BinaryContent capability of pydantic-ai.
    
    Args:
        ctx: Run context with agent context
        data: Raw binary image data
        media_type: MIME type of the image (default: image/jpeg)
        
    Returns:
        Dictionary containing processing information
    """
    try:
        # In a real implementation, this would be passed to the LLM
        # But in this example we'll just return metadata
        return {
            "success": True,
            "source": "binary",
            "size_bytes": len(data),
            "media_type": media_type,
            "processed": True,
            "message": "Image data processed successfully"
        }
    except Exception as e:
        logger.error(f"Error processing image data: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Aliases for SimpleAgent compatibility
process_image_url_tool = process_image_url
process_image_binary_tool = process_image_data 