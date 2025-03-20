"""Google Drive tools interface.

This module provides a compatibility layer for Google Drive tools.
"""
import logging
from typing import List, Dict, Any
from pydantic_ai import RunContext

from .tool import search_files, get_file_content

logger = logging.getLogger(__name__)

class GoogleDriveTools:
    """Tools for interacting with Google Drive API."""

    def __init__(self, token: str):
        """Initialize with API token.
        
        Args:
            token: Google API token
        """
        self.token = token

    def get_tools(self) -> List[Any]:
        """Get tools for the agent."""
        return []

    async def search_files(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for files in Google Drive.

        Args:
            query: The search query
            limit: Maximum number of results to return

        Returns:
            List of file information dictionaries
        """
        # Create a mock RunContext
        ctx = RunContext({})
        
        # Call the actual implementation
        result = await search_files(ctx, self.token, query, limit)
        
        # Extract the files from the result
        if result.get("success", False) and "files" in result:
            return result["files"]
        return []

    async def get_file_content(self, file_id: str) -> str:
        """Get the content of a file.

        Args:
            file_id: The ID of the file to get

        Returns:
            The file content as a string
        """
        # Create a mock RunContext
        ctx = RunContext({})
        
        # Call the actual implementation
        result = await get_file_content(ctx, self.token, file_id)
        
        # Extract the content from the result
        if result.get("success", False) and "content" in result:
            return result["content"]
        return f"Error retrieving content for file ID: {file_id}" 