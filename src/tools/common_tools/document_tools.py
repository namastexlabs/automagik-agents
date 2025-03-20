"""Document processing tools for pydantic-ai agents.

This module provides reusable tools for processing documents in agents.
"""

import logging
from typing import Dict, Optional, Any, Union
from pydantic_ai import DocumentUrl, BinaryContent, RunContext

logger = logging.getLogger(__name__)

async def process_document_url(ctx: RunContext[Dict], url: str) -> Dict[str, Any]:
    """Process a document from a URL.
    
    This tool allows an agent to process a document from a URL by directly using
    the DocumentUrl capability of pydantic-ai.
    
    Args:
        ctx: Run context with agent context
        url: URL of the document to process
        
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
            "message": "Document URL processed successfully"
        }
    except Exception as e:
        logger.error(f"Error processing document URL: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
        
async def process_document_data(ctx: RunContext[Dict], 
                               data: bytes, 
                               media_type: str = "application/pdf") -> Dict[str, Any]:
    """Process document data directly.
    
    This tool allows an agent to process binary document data directly using
    the BinaryContent capability of pydantic-ai.
    
    Args:
        ctx: Run context with agent context
        data: Raw binary document data
        media_type: MIME type of the document (default: application/pdf)
        
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
            "message": "Document data processed successfully"
        }
    except Exception as e:
        logger.error(f"Error processing document data: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Aliases for SimpleAgent compatibility
process_document_url_tool = process_document_url
process_document_binary_tool = process_document_data 