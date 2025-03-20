"""Audio processing tools for pydantic-ai agents.

This module provides reusable tools for processing audio in agents.
"""

import logging
from typing import Dict, Optional, Any, Union
from pydantic_ai import AudioUrl, BinaryContent, RunContext

logger = logging.getLogger(__name__)

async def process_audio_url(ctx: RunContext[Dict], url: str) -> Dict[str, Any]:
    """Process an audio file from a URL.
    
    This tool allows an agent to process audio from a URL by directly using
    the AudioUrl capability of pydantic-ai.
    
    Args:
        ctx: Run context with agent context
        url: URL of the audio to process
        
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
            "message": "Audio URL processed successfully"
        }
    except Exception as e:
        logger.error(f"Error processing audio URL: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
        
async def process_audio_data(ctx: RunContext[Dict], 
                             data: bytes, 
                             media_type: str = "audio/mp3") -> Dict[str, Any]:
    """Process audio data directly.
    
    This tool allows an agent to process binary audio data directly using
    the BinaryContent capability of pydantic-ai.
    
    Args:
        ctx: Run context with agent context
        data: Raw binary audio data
        media_type: MIME type of the audio (default: audio/mp3)
        
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
            "message": "Audio data processed successfully"
        }
    except Exception as e:
        logger.error(f"Error processing audio data: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Aliases for SimpleAgent compatibility
process_audio_url_tool = process_audio_url
process_audio_binary_tool = process_audio_data 