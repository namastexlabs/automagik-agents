#!/usr/bin/env python

"""
Simple script to print the memory tool descriptions from the SimpleAgent.

This script directly imports the necessary components to register
the memory tools and print their descriptions.
"""

import sys
import os
import logging
from typing import Dict, Any

# Set up the Python path to find the src module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import the necessary modules
from src.agents.simple.simple_agent.agent import SimpleAgent
from pydantic_ai import Agent
from src.tools.memory_tools import read_memory, write_memory
from src.utils.db import execute_query


def register_memory_tools():
    """Register memory tools and return their descriptions."""
    import logging
    import json
    from src.utils.db import execute_query
    
    logger = logging.getLogger(__name__)
    
    # Direct database approach - fetch memories directly from DB
    try:
        logger.info("Directly fetching memories from database for tool descriptions")
        
        # Query to get all available memories
        query = "SELECT id, name, description FROM memories ORDER BY name ASC"
        result = execute_query(query)
        # Handle case where result is a list (DB rows) or dict with 'rows' key
        if isinstance(result, list):
            memories = result
        else:
            memories = result.get('rows', [])
        memory_count = len(memories)
        
        logger.info(f"Found {memory_count} memories directly from database")
        
        # Create read_memory description that focuses on parameters rather than listing memories
        read_desc = "This tool allows retrieving memories stored in the database. It can return a specific memory "
        read_desc += "or a list of memories according to various filters. Available parameters:\n\n"
        read_desc += "- **memory_id**: Optional ID of the specific memory to retrieve\n"
        read_desc += "- **name**: Optional memory name (or partial name) to search for\n"
        read_desc += "- **read_mode**: Optional filter for memory read mode (e.g., system_prompt, user_memory)\n"
        read_desc += "- **list_all**: If True and no specific memory is requested, returns all available memories\n\n"
        read_desc += f"There are currently {memory_count} memories available in the database."
        
        # Create write_memory description that focuses on parameters rather than listing memories
        write_desc = "This tool allows creating or updating a memory in the database. Users can store or update "
        write_desc += "information that can be retrieved later. Available parameters:\n\n"
        write_desc += "- **name**: Required. The name of the memory to create or update\n"
        write_desc += "- **content**: Required. The content to store, can be a string or a dictionary format\n"
        write_desc += "- **description**: Optional. A description of what this memory contains or is used for\n"
        write_desc += "- **memory_id**: Optional. The ID of an existing memory to update\n"
        write_desc += "- **read_mode**: Optional. Controls how this memory is used (e.g., tool_call, system_prompt)\n"
        write_desc += "- **access**: Optional. The access permissions for this memory (e.g., read, write)\n"
        write_desc += "- **metadata**: Optional. Additional metadata to store with the memory\n\n"
        write_desc += f"There are currently {memory_count} memories that can be updated in the database."
        
        # Log memory names for reference without adding to descriptions
        if memory_count > 0:
            memory_names = [m.get('name', 'Unknown') for m in memories]
            memory_names_str = ", ".join(memory_names)
            print(f"\nFound {memory_count} memories: {memory_names_str}\n")
        
        return {
            "read_memory": read_desc,
            "write_memory": write_desc
        }
        
    except Exception as e:
        logger.error(f"Error generating tool descriptions: {e}")
        return {
            "read_memory": "Error retrieving description",
            "write_memory": "Error retrieving description"
        }


def main():
    """Main function to run the script."""
    print("\n=== MEMORY TOOL DESCRIPTION VIEWER ===\n")
    
    # Get the memory tool descriptions
    print("Fetching memory tool descriptions...\n")
    descriptions = register_memory_tools()
    
    # Print memory tool descriptions
    for tool_name, description in descriptions.items():
        print(f"\n=== {tool_name.upper()} TOOL ===\n")
        print(f"Description length: {len(description)} characters")
        print("\nDESCRIPTION:")
        print("-" * 80)
        print(description)
        print("-" * 80)
        print()
    
    print("\nExecution complete!")


if __name__ == "__main__":
    main()
