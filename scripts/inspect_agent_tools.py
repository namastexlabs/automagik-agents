#!/usr/bin/env python

"""
Script to inspect and print all tool descriptions for SimpleAgent as they appear in API calls.
"""

import sys
import os
import json
import logging

# Set up the Python path to find the src module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import the necessary modules
from src.agents.simple.simple_agent.agent import SimpleAgent
from src.settings import Settings


def get_agent_tool_descriptions(user_id=1, session_id="test-session"):
    """Get the exact tool descriptions used in API calls.
    
    Args:
        user_id: The user ID to use for the agent context
        session_id: The session ID to use for the agent context
        
    Returns:
        Dictionary containing the tool descriptions as they would appear in API calls
    """
    try:
        # Create settings for agent initialization
        settings = Settings()
        
        # Initialize agent
        agent = SimpleAgent(settings.dict())
        
        # Register tools - this is where dynamic descriptions are generated
        agent.register_tools()
        
        # Access the internal pydantic-ai agent to get tool schemas
        pai_agent = agent.agent
        
        # Initialize dictionary to hold tool descriptions
        tool_descriptions = {}
        
        # Get tools from the pydantic-ai agent
        if hasattr(pai_agent, '_tools'):
            tools = pai_agent._tools
            
            print(f"\nFound {len(tools)} tools registered with the agent:\n")
            
            # Extract tool information
            for i, tool in enumerate(tools, 1):
                tool_name = getattr(tool, 'name', f'Unknown-Tool-{i}')
                tool_function = getattr(tool, 'function', None)
                
                # Get the description (docstring)
                description = getattr(tool_function, '__doc__', 'No description available')
                
                # Store tools in result dict
                tool_descriptions[tool_name] = {
                    'description': description,
                    'length': len(description) if description else 0,
                }
                
                print(f"{i}. {tool_name} - {len(description) if description else 0} characters")
        
        # Extract the actual OpenAI API schema
        if hasattr(pai_agent, 'openai_tools'):
            openai_tools = pai_agent.openai_tools
            print(f"\nOpenAI API schema: {len(json.dumps(openai_tools))} characters")
            tool_descriptions['_openai_tools_schema'] = openai_tools
        
        return tool_descriptions
    
    except Exception as e:
        logging.error(f"Error getting agent tool descriptions: {e}")
        return {'error': str(e)}


def main():
    """Main function to run the script."""
    print("\n=== AGENT TOOL INSPECTOR ===\n")
    
    # Get all tool descriptions
    print("Initializing SimpleAgent and getting tool descriptions...")
    tool_descriptions = get_agent_tool_descriptions()
    
    # Display memory tools with full descriptions
    memory_tools = ['read_memory', 'write_memory']
    
    for tool_name in memory_tools:
        if tool_name in tool_descriptions:
            tool_info = tool_descriptions[tool_name]
            print(f"\n=== {tool_name.upper()} TOOL ===\n")
            print(f"Description length: {tool_info['length']} characters")
            print("\nDESCRIPTION:")
            print("-" * 80)
            print(tool_info['description'])
            print("-" * 80)
            print()
    
    # Save the full OpenAI tools schema to a file for inspection
    if '_openai_tools_schema' in tool_descriptions:
        schema_file = 'openai_tools_schema.json'
        with open(schema_file, 'w') as f:
            json.dump(tool_descriptions['_openai_tools_schema'], f, indent=2)
        print(f"\nSaved OpenAI tools schema to {schema_file}")
    
    print("\nExecution complete!")


if __name__ == "__main__":
    main()
