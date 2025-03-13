"""Mock implementation of BlackPearl API tools."""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class BlackPearlTools:
    """Tools for interacting with BlackPearl API."""

    def __init__(self, token: str):
        """Initialize with API token."""
        self.token = token

    def get_host_tools(self) -> List[Any]:
        """Get tools for the host agent."""
        logger.info("Returning empty list of host tools")
        return []

    def get_backoffice_tools(self) -> List[Any]:
        """Get tools for the backoffice agent."""
        return []

    async def search_contacts(self, user_id: str) -> Dict[str, Any]:
        """Search for contacts by user ID.

        Args:
            user_id: The user ID to search for

        Returns:
            Dictionary with search results
        """
        logger.info(f"Mock searching for contacts with user_id: {user_id}")
        # Return mock data
        return {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 8,
                    "nome": "Test User",
                    "telefone": "5551234567890",
                    "wpp_session_id": user_id,
                    "ativo": True,
                    "data_registro": "2025-02-24T15:51:39.135341-03:00",
                    "status_aprovacao": "NOT_REGISTERED",
                    "data_aprovacao": None,
                    "detalhes_aprovacao": "",
                    "ultima_atualizacao": "2025-02-24T15:57:06.041086-03:00",
                }
            ],
        }

    async def verify_cnpj(self, cnpj: str) -> Dict[str, Any]:
        """Verify a CNPJ number.

        Args:
            cnpj: The CNPJ to verify

        Returns:
            Dictionary with CNPJ information
        """
        logger.info(f"Mock verifying CNPJ: {cnpj}")
        # Return mock data
        return {
            "updated": "2025-02-18T21:35:47.000Z",
            "taxId": cnpj.replace(".", "").replace("/", "").replace("-", ""),
            "company": {
                "id": 12345678,
                "name": "MOCK COMPANY LTDA",
                "equity": 1000000,
                "nature": {"id": 2062, "text": "Sociedade Empresária Limitada"},
                "size": {"id": 5, "acronym": "DEMAIS", "text": "Demais"},
            },
            "alias": "Mock Internacional",
            "founded": "2013-06-26",
            "head": True,
            "statusDate": "2013-06-26",
            "status": {"id": 2, "text": "Ativa"},
            "address": {
                "municipality": 4208203,
                "street": "Avenida Principal",
                "number": "123",
                "details": "Sala 456",
                "district": "Centro",
                "city": "São Paulo",
                "state": "SP",
                "zip": "01234567",
                "country": {"id": 76, "name": "Brasil"},
            },
        }
