#!/usr/bin/env python

"""
Script to print the complete tool descriptions for the SimpleAgent.

This script loads the SimpleAgent instance, extracts its tools,
and prints the complete descriptions for all tools to verify what
is being generated, especially for memory tools.
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


from src.agents.simple.simple_agent.agent import SimpleAgent


def extract_tools_info(agent) -> Dict[str, Any]:
    """Extract tool information from the agent.
    
    Args:
        agent: The agent instance
        
    Returns:
        Dictionary of tool information including names and descriptions
    """
    result = {}
    
    # Try multiple possible structures for accessing tools
    # First check if the agent has our new registered_tools dictionary
    if hasattr(agent, 'registered_tools') and isinstance(agent.registered_tools, dict):
        print("Found registered_tools dictionary! Using it to extract tool info.")
        # Extract tools from the registered_tools dictionary
        for tool_name, tool_func in agent.registered_tools.items():
            if tool_func and hasattr(tool_func, '__doc__'):
                result[tool_name] = {
                    'description': tool_func.__doc__,
                    'length': len(tool_func.__doc__) if tool_func.__doc__ else 0,
                }
    # If registered_tools isn't available, try the legacy approaches
    elif hasattr(agent, 'agent'):
        # Method 1: Look for direct tool references in the SimpleAgent
        # Try the new tool attributes we added
        read_func = getattr(agent, 'read_memory_tool', None)
        create_func = getattr(agent, 'create_memory_tool', None)
        update_func = getattr(agent, 'update_memory_tool', None)
        
        if read_func and hasattr(read_func, '__doc__'):
            result['read_memory'] = {
                'description': read_func.__doc__,
                'length': len(read_func.__doc__) if read_func.__doc__ else 0,
            }
            
        if create_func and hasattr(create_func, '__doc__'):
            result['create_memory'] = {
                'description': create_func.__doc__,
                'length': len(create_func.__doc__) if create_func.__doc__ else 0,
            }
            
        if update_func and hasattr(update_func, '__doc__'):
            result['update_memory'] = {
                'description': update_func.__doc__,
                'length': len(update_func.__doc__) if update_func.__doc__ else 0,
            }
        
        # Method 2: Standard pydantic-ai tools extraction
        if not result and hasattr(agent.agent, '_tools'):
            for tool in agent.agent._tools:
                tool_name = getattr(tool, 'name', 'Unknown Tool')
                tool_function = getattr(tool, 'function', None)
                
                # Get the docstring from the function
                doc = getattr(tool_function, '__doc__', 'No description available')
                
                # Store tool info
                result[tool_name] = {
                    'description': doc,
                    'length': len(doc) if doc else 0,
                }
    
    # If we still couldn't find tools, use debugging information
    if not result:
        print("\nWARNING: Could not extract tools using standard methods.")
        print("Here's the agent structure for debugging:")
        
        # List all non-private attributes of the agent
        for attr_name in dir(agent):
            if not attr_name.startswith('_'):
                print(f" - {attr_name}")
                
        # List all non-private attributes of agent.agent if it exists
        if hasattr(agent, 'agent'):
            print("\nAttributes of agent.agent:")
            for attr_name in dir(agent.agent):
                if not attr_name.startswith('_'):
                    print(f" - {attr_name}")
    
    return result


def main():
    """Main function to run the script."""
    print("\n=== TOOL DESCRIPTION EXTRACTOR ===\n")
    
    # Use a basic configuration for testing
    config_dict = {
        "model": "gpt-4",
        "retries": 3,
        "agent_id": "simple_memory_agent"
    }
    
    # Create an instance of the SimpleAgent
    # The SimpleAgent will register tools during initialization
    print("Initializing SimpleAgent...")
    agent = SimpleAgent(config_dict)
    
    # Extract tool information
    print("Extracting tool descriptions...\n")
    tools_info = extract_tools_info(agent)
    
    # Print memory tool descriptions specifically
    memory_tools = ['read_memory', 'create_memory', 'update_memory']
    
    for tool_name in memory_tools:
        if tool_name in tools_info:
            tool_info = tools_info[tool_name]
            print(f"\n=== {tool_name.upper()} TOOL ===\n")
            print(f"Description length: {tool_info['length']} characters")
            print("\nDESCRIPTION:")
            print("-" * 80)
            print(tool_info['description'])
            print("-" * 80)
            print()
        else:
            print(f"\nWARNING: {tool_name} tool not found in the agent!\n")
    
    # Print all available tools
    print("\n=== ALL AVAILABLE TOOLS ===\n")
    print(f"Found {len(tools_info)} tools registered with the agent:\n")
    
    for idx, (tool_name, tool_info) in enumerate(tools_info.items(), 1):
        if tool_name not in memory_tools:  # Skip memory tools as they were shown above
            print(f"{idx}. {tool_name} - {tool_info['length']} characters")
    
    print("\nExecution complete!")


if __name__ == "__main__":
    main()
