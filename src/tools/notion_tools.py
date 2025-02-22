"""Notion tools for Sofia."""

from typing import List, Optional, Dict, Any
from pydantic_ai.tools import Tool
from pydantic_ai import RunContext
from notion_client import Client

class NotionError(Exception):
    """Base exception for Notion API errors"""
    pass

class NotionTools:
    def __init__(self):
        # Initialize Notion client with the existing secret
        try:
            self.__notion__ = Client(auth=NotionTools.get_notion_token())
        except Exception as e:
            return {"error": f"Failed to initialize Notion client: {str(e)}"}
            
        self.__tools__ = []

        # Database related tools
        self.__tools__.extend([
            self.search_databases,
            self.get_database,
            self.create_database,
            self.update_database,
            self.query_database,
            self.create_database_item,
            self.update_database_item,
        ])

        # Page related tools
        self.__tools__.extend([
            self.get_page,
            self.create_page,
            self.update_page,
            self.archive_page,
            self.get_page_property,
            self.get_page_property_item,
        ])

        # Block related tools
        self.__tools__.extend([
            self.get_block,
            self.update_block,
            self.delete_block,
            self.get_block_children,
            self.append_block_children,
        ])

    @staticmethod
    def get_notion_token() -> str:
        """Gets the Notion token from environment variables."""
        import os
        token = os.getenv("NOTION_TOKEN")
        if not token:
            raise ValueError("NOTION_TOKEN environment variable not set")
        return token

    #----------------------#
    #      DATABASE       #
    #----------------------#

    def search_databases(self, ctx: RunContext[Dict], query: str = "", start_cursor: Optional[str] = None, page_size: int = 100) -> Dict[str, Any]:
        """
        Search for databases shared with the integration.

        Example call: search_databases(query="Movies", page_size=50)
        
        Args:
            ctx: The run context
            query (str): Search query (default: "", which returns all databases)
            start_cursor (str, optional): Starting point for the results
            page_size (int): Maximum number of databases to return (default: 100)
        Returns:
            Dict[str, Any]: Dictionary containing success status, results, and any error message
        """
        try:
            response = self.__notion__.search(
                query=query,
                filter={
                    "property": "object",
                    "value": "database"
                },
                start_cursor=start_cursor,
                page_size=page_size
            )
            
            return {
                "success": True,
                "results": response.get("results", []),
                "has_more": response.get("has_more", False),
                "next_cursor": response.get("next_cursor")
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to search databases: {str(e)}",
                "results": []
            }

    def create_database(
        self,
        ctx: RunContext[Dict],
        parent: Dict[str, Any],
        title: List[Dict[str, Any]],
        properties: Dict[str, Dict[str, Any]],
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Creates a new database as a child of an existing page.

        Example call: create_database(
            parent={"page_id": "page_id"},
            title=[{"text": {"content": "Movies Database"}}],
            properties={
                "Name": {"title": {}},
                "Rating": {"number": {"format": "number"}},
                "Status": {"select": {"options": [{"name": "Watched"}, {"name": "To Watch"}]}}
            }
        )
        
        Args:
            ctx: The run context
            parent (Dict[str, Any]): Parent page info
            title (List[Dict[str, Any]]): Database title
            properties (Dict[str, Dict[str, Any]]): Database properties schema
            icon (Dict[str, Any], optional): Database icon
            cover (Dict[str, Any], optional): Database cover
        Returns:
            Dict[str, Any]: The created database
        """
        return self.__notion__.databases.create(
            parent=parent,
            title=title,
            properties=properties,
            icon=icon,
            cover=cover
        )

    def update_database(
        self,
        ctx: RunContext[Dict],
        database_id: str,
        title: Optional[List[Dict[str, Any]]] = None,
        properties: Optional[Dict[str, Dict[str, Any]]] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None,
        archived: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Updates a database.

        Example call: update_database(
            database_id="database_id",
            title=[{"text": {"content": "Updated Movies Database"}}],
            properties={
                "New Property": {"rich_text": {}}
            }
        )
        
        Args:
            ctx: The run context
            database_id (str): The ID of the database to update
            title (List[Dict[str, Any]], optional): New database title
            properties (Dict[str, Dict[str, Any]], optional): Updated properties schema
            icon (Dict[str, Any], optional): New database icon
            cover (Dict[str, Any], optional): New database cover
            archived (bool, optional): Set to true to archive (delete) the database
        Returns:
            Dict[str, Any]: The updated database
        """
        return self.__notion__.databases.update(
            database_id=database_id,
            title=title,
            properties=properties,
            icon=icon,
            cover=cover,
            archived=archived
        )

    def get_database(self, ctx: RunContext[Dict], database_id: str) -> Dict[str, Any]:
        """
        Retrieves a database by ID.

        Example call: get_database("database_id")
        
        Args:
            ctx: The run context
            database_id (str): The ID of the database to retrieve.
        Returns:
            Dict[str, Any]: The database object.
        """
        return self.__notion__.databases.retrieve(database_id=database_id)

    def query_database(
        self,
        ctx: RunContext[Dict],
        database_id: str,
        filter_dict: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Queries a database with optional filters and sorting.

        Example call: query_database(
            database_id="database_id",
            filter_dict={"property": "Name", "text": {"contains": "Project"}},
            sorts=[{"timestamp": "created_time", "direction": "descending"}]
        )
        
        Args:
            ctx: The run context
            database_id (str): The ID of the database to query
            filter_dict (Dict[str, Any], optional): Filter conditions
            sorts (List[Dict[str, Any]], optional): Sort conditions
            start_cursor (str, optional): Starting point for pagination
            page_size (int): Maximum number of results to return (default: 100)
        Returns:
            Dict[str, Any]: Query results including items and pagination info
        """
        try:
            # Default sort by created time if no sort specified
            default_sort = [{"timestamp": "created_time", "direction": "descending"}]
            query_args = {
                "database_id": database_id,
                "page_size": page_size,
                "sorts": sorts if sorts is not None else default_sort
            }
            
            if filter_dict is not None:
                query_args["filter"] = filter_dict
                
            if start_cursor is not None:
                query_args["start_cursor"] = start_cursor
                
            response = self.__notion__.databases.query(**query_args)
            return {
                "success": True,
                "results": response.get("results", []),
                "has_more": response.get("has_more", False),
                "next_cursor": response.get("next_cursor")
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to query database: {str(e)}",
                "results": []
            }




    def create_database_item(
        self,
        ctx: RunContext[Dict],
        database_id: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new item in a database.

        Example call: create_database_item("database_id", {"Name": {"title": [{"text": {"content": "New Item"}}]}})
        
        Args:
            database_id (str): The ID of the database.
            properties (Dict[str, Any]): Properties of the new item.
        Returns:
            Dict[str, Any]: The created database item.
        """
        return self.__notion__.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )

    def update_database_item(
        self,
        ctx: RunContext[Dict],
        page_id: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing database item.

        Example call: update_database_item("page_id", {"Status": {"select": {"name": "Done"}}})
        
        Args:
            page_id (str): The ID of the page/item to update.
            properties (Dict[str, Any]): Updated properties.
        Returns:
            Dict[str, Any]: The updated database item.
        """
        return self.__notion__.pages.update(
            page_id=page_id,
            properties=properties
        )

    #----------------------#
    #       PAGES         #
    #----------------------#

    def get_page(self, ctx: RunContext[Dict], page_id: str) -> Dict[str, Any]:
        """
        Retrieves a page by ID.

        Example call: get_page("page_id")
        
        Args:
            page_id (str): The ID of the page to retrieve.
        Returns:
            Dict[str, Any]: The page object.
        """
        return self.__notion__.pages.retrieve(page_id=page_id)

    def create_page(
        self,
        ctx: RunContext[Dict],
        parent: Dict[str, Any],
        properties: Dict[str, Any],
        children: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Creates a new page.

        Example call: create_page({"page_id": "parent_id"}, {"title": {"title": [{"text": {"content": "New Page"}}]}})
        
        Args:
            parent (Dict[str, Any]): Parent object (page or database).
            properties (Dict[str, Any]): Page properties.
            children (List[Dict[str, Any]], optional): Page content blocks.
        Returns:
            Dict[str, Any]: The created page.
        """
        return self.__notion__.pages.create(
            parent=parent,
            properties=properties,
            children=children
        )

    def update_page(
        self,
        ctx: RunContext[Dict],
        page_id: str,
        properties: Dict[str, Any],
        archived: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Updates an existing page.

        Example call: update_page("page_id", {"title": {"title": [{"text": {"content": "Updated Title"}}]}})
        
        Args:
            page_id (str): The ID of the page to update.
            properties (Dict[str, Any]): Updated properties.
            archived (bool, optional): Whether to archive the page.
        Returns:
            Dict[str, Any]: The updated page.
        """
        return self.__notion__.pages.update(
            page_id=page_id,
            properties=properties,
            archived=archived
        )

    def archive_page(self, ctx: RunContext[Dict], page_id: str) -> Dict[str, Any]:
        """
        Archives (soft deletes) a page.

        Example call: archive_page("page_id")
        
        Args:
            ctx: The run context
            page_id (str): The ID of the page to archive.
        Returns:
            Dict[str, Any]: The archived page.
        """
        return self.update_page(ctx, page_id=page_id, properties={}, archived=True)

    def get_page_property(self, ctx: RunContext[Dict], page_id: str, property_id: str) -> Dict[str, Any]:
        """
        Retrieves a page property.

        Example call: get_page_property("page_id", "property_id")
        
        Args:
            ctx: The run context
            page_id (str): The ID of the page
            property_id (str): The ID of the property to retrieve
        Returns:
            Dict[str, Any]: The page property item
        """
        return self.__notion__.pages.properties.retrieve(
            page_id=page_id,
            property_id=property_id
        )

    def get_page_property_item(self, ctx: RunContext[Dict], page_id: str, property_id: str, start_cursor: Optional[str] = None, page_size: int = 100) -> Dict[str, Any]:
        """
        Retrieves a page property item. Use this endpoint to get the value of a page property.

        Example call: get_page_property_item("page_id", "property_id", page_size=50)
        
        Args:
            ctx: The run context
            page_id (str): The ID of the page
            property_id (str): The ID of the property to retrieve
            start_cursor (str, optional): Starting point for the results
            page_size (int): Maximum number of results (default: 100)
        Returns:
            Dict[str, Any]: The page property value and pagination info
        """
        return self.__notion__.pages.properties.retrieve(
            page_id=page_id,
            property_id=property_id,
            start_cursor=start_cursor,
            page_size=page_size
        )

    #----------------------#
    #      BLOCKS         #
    #----------------------#

    def get_block(self, ctx: RunContext[Dict], block_id: str) -> Dict[str, Any]:
        """
        Retrieves a block by ID.

        Example call: get_block("block_id")
        
        Args:
            ctx: The run context
            block_id (str): The ID of the block to retrieve
        Returns:
            Dict[str, Any]: The block object
        """
        return self.__notion__.blocks.retrieve(block_id=block_id)

    def update_block(self, ctx: RunContext[Dict], block_id: str, **properties) -> Dict[str, Any]:
        """
        Updates a block.

        Example call: update_block("block_id", paragraph={"text": [{"text": {"content": "Updated text"}}]})
        
        Args:
            ctx: The run context
            block_id (str): The ID of the block to update
            **properties: Block-type specific update parameters
        Returns:
            Dict[str, Any]: The updated block
        """
        return self.__notion__.blocks.update(block_id=block_id, **properties)

    def delete_block(self, ctx: RunContext[Dict], block_id: str) -> Dict[str, Any]:
        """
        Deletes (archives) a block.

        Example call: delete_block("block_id")
        
        Args:
            ctx: The run context
            block_id (str): The ID of the block to delete
        Returns:
            Dict[str, Any]: The deleted block
        """
        return self.__notion__.blocks.delete(block_id=block_id)

    def get_block_children(self, ctx: RunContext[Dict], block_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all children blocks of a block.

        Example call: get_block_children("block_id")
        
        Args:
            block_id (str): The ID of the block.
        Returns:
            List[Dict[str, Any]]: List of child blocks.
        """
        return self.__notion__.blocks.children.list(block_id=block_id).get("results", [])

    def append_block_children(
        self,
        ctx: RunContext[Dict],
        block_id: str,
        children: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Appends new children blocks to a block.

        Example call: append_block_children("block_id", [{"type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": "New content"}}]}}])
        
        Args:
            block_id (str): The ID of the block to append to.
            children (List[Dict[str, Any]]): List of blocks to append.
        Returns:
            Dict[str, Any]: Result of the append operation.
        """
        return self.__notion__.blocks.children.append(
            block_id=block_id,
            children=children
        )

    @property
    def tools(self) -> List:
        """Returns the list of available tool functions."""
        return self.__tools__
