"""Mock implementation of Chroma vector database tools."""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ChromaTools:
    """Tools for interacting with Chroma vector database."""
    
    def __init__(self, collection_name: str = "products"):
        """Initialize with collection name."""
        self.collection_name = collection_name
        logger.info(f"Initialized ChromaTools with collection: {collection_name}")
        
    def get_tools(self) -> List[Any]:
        """Get tools for the agent."""
        logger.info("Returning empty list of tools")
        return []
        
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for documents in the vector database.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            List of document dictionaries
        """
        logger.info(f"Mock searching for documents with query: {query}, limit: {limit}")
        # Return mock data
        return [
            {
                "id": "prod1",
                "name": "Premium Widget X1",
                "description": "High-quality widget with advanced features",
                "price": 199.99,
                "category": "Widgets",
                "brand": "WidgetCo",
                "in_stock": True,
                "image_url": "https://example.com/images/widget-x1.jpg"
            },
            {
                "id": "prod2",
                "name": "Standard Widget S2",
                "description": "Reliable widget for everyday use",
                "price": 99.99,
                "category": "Widgets",
                "brand": "WidgetCo",
                "in_stock": True,
                "image_url": "https://example.com/images/widget-s2.jpg"
            }
        ][:limit]
        
    async def add_document(self, document: Dict[str, Any]) -> str:
        """Add a document to the vector database.
        
        Args:
            document: The document to add
            
        Returns:
            Document ID
        """
        logger.info(f"Mock adding document: {document}")
        # Return mock data
        return "doc-" + str(hash(str(document)) % 10000) 