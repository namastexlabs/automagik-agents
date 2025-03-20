"""Text processing tools for pydantic-ai agents.

This module provides reusable tools for processing text in agents.
"""

import logging
from typing import Dict, Optional, Any, List
from pydantic_ai import RunContext

logger = logging.getLogger(__name__)

async def summarize(ctx: RunContext[Dict], 
                   text: str, 
                   max_length: Optional[int] = 200, 
                   bullet_points: bool = False) -> str:
    """Summarize a text to the specified maximum length.
    
    This tool allows an agent to summarize a long text. In a real implementation,
    this would use the LLM to create a proper summary, but for this example
    we'll use a simple truncation.
    
    Args:
        ctx: Run context with agent context
        text: The text to summarize
        max_length: Maximum length of the summary
        bullet_points: Whether to return as bullet points
        
    Returns:
        Summarized text
    """
    try:
        # Simple implementation for example purposes
        if len(text) <= max_length:
            summary = text
        else:
            summary = text[:max_length] + "..."
        
        if bullet_points:
            # Create some bullet points from the summary
            sentences = summary.split('.')
            bullets = [s.strip() + '.' for s in sentences if s.strip()]
            return "\n".join([f"• {b}" for b in bullets])
        else:
            return summary
            
    except Exception as e:
        logger.error(f"Error summarizing text: {str(e)}")
        return f"Error summarizing text: {str(e)}"

async def translate(ctx: RunContext[Dict], 
                   text: str, 
                   target_language: str) -> str:
    """Translate text to the target language.
    
    This tool allows an agent to translate text to a specified language.
    In a real implementation, this would use a translation service or LLM,
    but for this example we'll return a placeholder.
    
    Args:
        ctx: Run context with agent context
        text: The text to translate
        target_language: The target language code or name
        
    Returns:
        Translated text (or placeholder in this example)
    """
    try:
        # Simple implementation for example purposes
        # In a real implementation, this would call a translation service
        return f"[Translation of '{text[:30]}...' to {target_language}]"
    except Exception as e:
        logger.error(f"Error translating text: {str(e)}")
        return f"Error translating text: {str(e)}" 