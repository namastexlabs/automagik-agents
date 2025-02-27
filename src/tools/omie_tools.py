"""Mock implementation of Omie API tools."""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class OmieTools:
    """Tools for interacting with Omie API."""
    
    def __init__(self, token: str):
        """Initialize with API token."""
        self.token = token
        logger.info("Initialized OmieTools with token")
        
    def get_host_tools(self) -> List[Any]:
        """Get tools for the host agent."""
        logger.info("Returning empty list of host tools")
        return []
        
    def get_backoffice_tools(self) -> List[Any]:
        """Get tools for the backoffice agent."""
        logger.info("Returning empty list of backoffice tools")
        return []
        
    async def search_client(self, cnpj: str) -> Dict[str, Any]:
        """Search for a client by CNPJ.
        
        Args:
            cnpj: The CNPJ to search for
            
        Returns:
            Dictionary with client information
        """
        logger.info(f"Mock searching for client with CNPJ: {cnpj}")
        # Return mock data
        return {
            "client_id": "12345",
            "name": "MOCK COMPANY LTDA",
            "cnpj": cnpj,
            "email": "contact@mockcompany.com",
            "phone": "1234567890",
            "address": {
                "street": "Avenida Principal",
                "number": "123",
                "complement": "Sala 456",
                "district": "Centro",
                "city": "São Paulo",
                "state": "SP",
                "zip": "01234567"
            },
            "status": "active"
        }
        
    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client.
        
        Args:
            client_data: The client data to create
            
        Returns:
            Dictionary with created client information
        """
        logger.info(f"Mock creating client: {client_data}")
        # Return mock data
        return {
            "client_id": "12345",
            "name": client_data.get("name", "MOCK COMPANY LTDA"),
            "cnpj": client_data.get("cnpj", "00000000000000"),
            "email": client_data.get("email", "contact@mockcompany.com"),
            "phone": client_data.get("phone", "1234567890"),
            "status": "active",
            "created": True
        } 