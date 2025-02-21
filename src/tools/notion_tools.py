'''Notion Tools for interfacing with the Notion API.

This module provides a NotionTools class with implementations for basic Notion operations such as listing databases, querying a database, creating a page, updating a page, and archiving (deleting) a page.

In a production environment, these methods interact with the Notion API using HTTP requests via the requests library.
'''

import os
import requests


class NotionTools:
    def __init__(self):
        # Get Notion token from environment variables; if missing, raise an exception
        self.token = os.environ.get("NOTION_TOKEN", "")
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable is not set.")
        # Setup default headers for Notion API requests
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        # Base URL for Notion API
        self.base_url = "https://api.notion.com/v1"

    def list_databases(self):
        '''List all databases in the workspace.'''
        url = f"{self.base_url}/search"
        payload = {
            "filter": {
                "property": "object",
                "value": "database"
            }
        }
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            return {"error": response.text}
        return response.json()

    def query_database(self, database_id, query_params=None):
        '''Query a database with optional filter parameters.'''
        url = f"{self.base_url}/databases/{database_id}/query"
        payload = query_params or {}
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            return {"error": response.text}
        return response.json()

    def create_page(self, database_id, properties):
        '''Create a new page in a database.'''
        url = f"{self.base_url}/pages"
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code not in (200, 201):
            return {"error": response.text}
        return response.json()

    def update_page(self, page_id, properties):
        '''Update an existing page's properties.'''
        url = f"{self.base_url}/pages/{page_id}"
        payload = {"properties": properties}
        response = requests.patch(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            return {"error": response.text}
        return response.json()

    def delete_page(self, page_id):
        '''Archive a page by setting its "archived" property.'''
        url = f"{self.base_url}/pages/{page_id}"
        payload = {"archived": True}
        response = requests.patch(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            return {"error": response.text}
        return response.json() 