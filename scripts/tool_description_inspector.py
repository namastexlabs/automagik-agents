#!/usr/bin/env python

"""
This script provides a comprehensive inspection of memory tool descriptions
by showing both the raw docstrings and the final descriptions used in the agent.

It extracts and prints:
1. The raw docstrings from the memory_tools module
2. The description text used in the SimpleAgent class
3. The actual descriptions registered with the LLM
"""

import sys
import os
import json
import re
import subprocess
from typing import Dict, Any, List

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Configure basic logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Import memory tools
from src.tools.memory_tools import read_memory, write_memory
from src.agents.simple.simple_agent.agent import SimpleAgent


def extract_descriptions_from_agent_run(message: str = "Show read_memory and write_memory parameters") -> Dict[str, Any]:
    """Extract tool descriptions by running the agent and capturing its response.
    
    Args:
        message: Message to send to the agent to get tool descriptions
        
    Returns:
        Dictionary with extracted descriptions
    """
    # Run the agent through the CLI
    cmd = [
        "automagik-agents", "agent", "run", "message",
        "--agent", "simple_agent",
        "--message", message,
        "--session", f"desc-inspect-{os.getpid()}"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        response = result.stdout
        
        # Save the full output to a file
        output_file = "agent_response_full.txt"
        with open(output_file, "w") as f:
            f.write(response)
        logging.info(f"Full agent response saved to {output_file}")
        
        # Extract the assistant's response
        assistant_response = ""
        match = re.search(r'assistant: (.+?)Session', response, re.DOTALL)
        if match:
            assistant_response = match.group(1).strip()
            
            # Save just the assistant response
            with open("assistant_response.txt", "w") as f:
                f.write(assistant_response)
        
        # Try to find memory tool descriptions in the response
        extracted = {}
        
        # Extract read_memory description from response
        read_memory_match = re.search(r'read_memory[^\n]*:\s*([^\n].+?)(?:###|$)', 
                                     assistant_response, re.DOTALL)
        if read_memory_match:
            read_desc = read_memory_match.group(1).strip()
            extracted['read_memory'] = read_desc
        
        # Extract write_memory description from response
        write_memory_match = re.search(r'write_memory[^\n]*:\s*([^\n].+?)(?:Session|$)', 
                                      assistant_response, re.DOTALL)
        if write_memory_match:
            write_desc = write_memory_match.group(1).strip()
            extracted['write_memory'] = write_desc
        
        return {
            'assistant_response': assistant_response,
            'extracted_descriptions': extracted
        }
        
    except Exception as e:
        logging.error(f"Error running agent: {e}")
        return {'error': str(e)}


def extract_memory_names_from_db() -> List[str]:
    """Extract memory names directly from the database.
    
    Returns:
        List of memory names found in the database
    """
    try:
        from src.db import list_memories
        
        # Use repository function to get all memories
        memories = list_memories()
        
        # Extract memory names
        memory_names = []
        for memory in memories:
            # Handle case where memory object might be a Pydantic model or a dict
            if hasattr(memory, 'name'):
                memory_names.append(memory.name)
            elif isinstance(memory, dict) and 'name' in memory:
                memory_names.append(memory['name'])
        
        # Sort memory names alphabetically
        memory_names.sort()
        
        return memory_names
    
    except Exception as e:
        logging.error(f"Error fetching memory names: {e}")
        return []


def main():
    """Main function to run the script."""
    print("\n===== MEMORY TOOL DESCRIPTION INSPECTOR =====\n")
    
    # Get memory names from DB
    print("Fetching memory names from database...")
    memory_names = extract_memory_names_from_db()
    print(f"Found {len(memory_names)} memories: {', '.join(memory_names)}\n")
    
    # Print original docstrings
    print("===== ORIGINAL DOCSTRINGS FROM MEMORY_TOOLS MODULE =====\n")
    print("READ_MEMORY DOCSTRING:")
    print("-" * 80)
    print(read_memory.__doc__)
    print("-" * 80)

    print("\nWRITE_MEMORY DOCSTRING:")
    print("-" * 80)
    print(write_memory.__doc__)
    print("-" * 80)

    # Print modified descriptions in SimpleAgent registration
    # Pull out the code directly from the file
    print("\n===== TOOL DESCRIPTION CODE FROM SIMPLE_AGENT =====\n")
    agent_file_path = os.path.join(project_root, "src/agents/simple/simple_agent/agent.py")

    with open(agent_file_path, 'r') as f:
        agent_code = f.read()

    # Extract the read_memory description code
    read_desc_start = agent_code.find("# Create read_memory description")
    read_desc_end = agent_code.find("logger.info(f\"Created parameter-focused read_memory")
    if read_desc_start > 0 and read_desc_end > read_desc_start:
        read_desc_code = agent_code[read_desc_start:read_desc_end].strip()
        print("READ_MEMORY DESCRIPTION CODE:")
        print("-" * 80)
        print(read_desc_code)
        print("-" * 80)

    # Extract the write_memory description code
    write_desc_start = agent_code.find("# Create write_memory description")
    write_desc_end = agent_code.find("logger.info(f\"Created parameter-focused write_memory")
    if write_desc_start > 0 and write_desc_end > write_desc_start:
        write_desc_code = agent_code[write_desc_start:write_desc_end].strip()
        print("\nWRITE_MEMORY DESCRIPTION CODE:")
        print("-" * 80)
        print(write_desc_code)
        print("-" * 80)
    
    # Extract and print actual descriptions from agent response
    print("\n===== ACTUAL DESCRIPTIONS FROM AGENT RESPONSE =====\n")
    print("Running agent to extract tool descriptions as seen by users...")
    
    result = extract_descriptions_from_agent_run()
    
    if 'extracted_descriptions' in result:
        descriptions = result['extracted_descriptions']
        
        if 'read_memory' in descriptions:
            print("\nREAD_MEMORY DESCRIPTION AS SEEN BY USERS:")
            print("-" * 80)
            print(descriptions['read_memory'])
            print("-" * 80)
        
        if 'write_memory' in descriptions:
            print("\nWRITE_MEMORY DESCRIPTION AS SEEN BY USERS:")
            print("-" * 80)
            print(descriptions['write_memory'])
            print("-" * 80)
    
    print("\n===== INSPECTION COMPLETE =====\n")
    print("This script has inspected:")
    print("1. Original docstrings from the memory_tools module")
    print("2. Description code in the SimpleAgent class")
    print("3. Actual descriptions as seen by users in agent responses")
    print("\nAll output has been saved to:")
    print("- agent_response_full.txt: Full output from the agent run")
    print("- assistant_response.txt: Just the assistant's response")
    

if __name__ == "__main__":
    main()
