#!/usr/bin/env python

"""
Script to print all tool descriptions for SimpleAgent directly from the agent instance.
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
from pydantic_ai import RunContext

def create_dummy_context():
    """Create a dummy context for agent initialization."""
    return {
        "user_id": 1, 
        "session_id": "test-session", 
        "agent_id": "simple_agent"
    }

def main():
    """Main function to run the script."""
    print("\n=== SIMPLE AGENT TOOL INSPECTOR ===\n")
    
    # Create config dictionary with minimal settings
    config_dict = {
        "AM_API_KEY": "test-key",
        "OPENAI_API_KEY": "sk-test",
        "DISCORD_BOT_TOKEN": "discord-test",
        "DATABASE_URL": os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/automagik")
    }
    
    # Initialize the agent
    print("Initializing SimpleAgent...")
    agent = SimpleAgent(config_dict)
    
    # Register all tools
    agent.register_tools()
    
    # Access the internal agent object to get the tools
    if hasattr(agent, 'agent') and hasattr(agent.agent, '_tools'):
        tools = agent.agent._tools
        print(f"\nFound {len(tools)} tools registered with the agent:\n")
        
        # Print all tool names and descriptions
        for i, tool in enumerate(tools, 1):
            name = getattr(tool, 'name', f'Unknown-Tool-{i}')
            func = getattr(tool, 'function', None)
            doc = getattr(func, '__doc__', 'No description available')
            
            print(f"{i}. {name} - {len(doc)} characters")
        
        # Print memory tool descriptions in detail
        memory_tools = ['read_memory', 'write_memory']
        for tool_name in memory_tools:
            # Find the tool by name
            memory_tool = next((t for t in tools if getattr(t, 'name', '') == tool_name), None)
            
            if memory_tool:
                func = getattr(memory_tool, 'function', None)
                doc = getattr(func, '__doc__', 'No description available')
                
                print(f"\n=== {tool_name.upper()} TOOL ===\n")
                print(f"Description length: {len(doc)} characters")
                print("\nDESCRIPTION:")
                print("-" * 80)
                print(doc)
                print("-" * 80)
                print()
                
                # Also print parameters
                if hasattr(memory_tool, 'parameters') and memory_tool.parameters:
                    print("PARAMETERS:")
                    print("-" * 80)
                    for param_name, param in memory_tool.parameters.items():
                        print(f"  {param_name}: {getattr(param, 'description', 'No description')}")
                    print("-" * 80)
                    print()
            else:
                print(f"\nWARNING: {tool_name} tool not found!\n")
        
        # Try to extract OpenAI tool schema
        if hasattr(agent.agent, 'openai_tools'):
            schema = agent.agent.openai_tools
            schema_file = os.path.join(os.path.dirname(__file__), 'openai_tools_schema.json')
            
            with open(schema_file, 'w') as f:
                json.dump(schema, f, indent=2)
            
            print(f"\nSaved complete OpenAI tools schema to {schema_file}")
            
            # Find memory tools in schema
            for tool in schema:
                if tool.get('function', {}).get('name') in memory_tools:
                    tool_name = tool.get('function', {}).get('name')
                    description = tool.get('function', {}).get('description', '')
                    
                    print(f"\n=== {tool_name.upper()} IN OPENAI SCHEMA ===\n")
                    print(f"Description length: {len(description)} characters")
                    print("\nDESCRIPTION:")
                    print("-" * 80)
                    print(description)
                    print("-" * 80)
                    print()
    else:
        print("ERROR: Could not access agent tools!")
        
    print("\nExecution complete!")

if __name__ == "__main__":
    main()
