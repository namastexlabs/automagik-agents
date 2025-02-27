"""Mock implementation of Google Drive API tools."""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class GoogleDriveTools:
    """Tools for interacting with Google Drive API."""
    
    def __init__(self, token: str):
        """Initialize with API token."""
        self.token = token
        logger.info("Initialized GoogleDriveTools with token")
        
    def get_tools(self) -> List[Any]:
        """Get tools for the agent."""
        logger.info("Returning empty list of tools")
        return []
        
    async def search_files(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for files in Google Drive.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            List of file information dictionaries
        """
        logger.info(f"Mock searching for files with query: {query}, limit: {limit}")
        # Return mock data
        return [
            {
                "id": "file1",
                "name": "Product Catalog.pdf",
                "mimeType": "application/pdf",
                "webViewLink": "https://drive.google.com/file/d/mock1/view",
                "createdTime": "2023-01-01T12:00:00.000Z"
            },
            {
                "id": "file2",
                "name": "Price List.xlsx",
                "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "webViewLink": "https://drive.google.com/file/d/mock2/view",
                "createdTime": "2023-02-01T12:00:00.000Z"
            }
        ][:limit]
        
    async def get_file_content(self, file_id: str) -> str:
        """Get the content of a file.
        
        Args:
            file_id: The ID of the file to get
            
        Returns:
            The file content as a string
        """
        logger.info(f"Mock getting file content for file_id: {file_id}")
        # Return mock data
        return "This is mock file content for file ID: " + file_id 