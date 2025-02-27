"""Omie tools for Stan agent."""

from typing import List, Optional, Dict, Any
from pydantic_ai.tools import Tool
from pydantic_ai import RunContext

class OmieTools:
    def __init__(self, token: str):
        """Initialize Omie tools with API token."""
        self.token = token
        self.__host_tools__ = []
        self.__backoffice_tools__ = []
        
        # Initialize host tools
        self.__host_tools__.extend([
            self.search_clients,
            self.get_client_status,
        ])
        
        # Initialize backoffice tools
        self.__backoffice_tools__.extend([
            self.search_clients,
            self.get_client_status,
            self.update_client,
        ])
    
    def get_host_tools(self) -> List:
        """Get tools for the Host agent."""
        return self.__host_tools__
    
    def get_backoffice_tools(self) -> List:
        """Get tools for the Backoffice agent."""
        return self.__backoffice_tools__
    
    async def search_clients(self, ctx: RunContext[Dict], search_term: str) -> List[Dict[str, Any]]:
        """Search for clients in Omie by name, CNPJ, or email.
        
        Args:
            ctx: The run context
            search_term: The search term (name, CNPJ, or email)
            
        Returns:
            List of matching clients
        """
        # Mock implementation - replace with actual API call
        if "example" in search_term.lower():
            return [{
                "client_id": "OMI12345",
                "name": "Example Company Ltd",
                "cnpj": "12.345.678/0001-90",
                "email": "contact@example.com",
                "status": "APPROVED"
            }]
        
        # Mock empty response
        return []
    
    async def get_client_status(self, ctx: RunContext[Dict], client_id: str) -> Dict[str, Any]:
        """Get a client's status in Omie.
        
        Args:
            ctx: The run context
            client_id: The client's ID
            
        Returns:
            Dictionary with client status information
        """
        # Mock implementation - replace with actual API call
        if client_id == "OMI12345":
            return {
                "client_id": client_id,
                "status": "APPROVED",
                "registration_date": "2023-01-15",
                "approval_date": "2023-01-20"
            }
        
        # Mock not found response
        return {
            "error": "Client not found",
            "client_id": client_id
        }
    
    async def update_client(self, ctx: RunContext[Dict], client_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update client information in Omie.
        
        Args:
            ctx: The run context
            client_id: The client's ID
            data: Dictionary with fields to update
            
        Returns:
            Dictionary with update result
        """
        # Mock implementation - replace with actual API call
        return {
            "success": True,
            "client_id": client_id,
            "message": "Client information updated successfully"
        } 