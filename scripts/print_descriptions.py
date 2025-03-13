#!/usr/bin/env python

"""
This script prints the raw descriptions from the memory_tools module and
then runs a test with the agent to show what descriptions are actually being used.
"""

import sys
import os
import subprocess
import json

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import memory tools
from src.tools.memory_tools import read_memory, write_memory
from src.agents.simple.simple_agent.agent import SimpleAgent

# Print original docstrings
print("\n=== ORIGINAL DOCSTRINGS FROM MEMORY_TOOLS MODULE ===\n")
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
print("\n=== TOOL DESCRIPTION CODE FROM SIMPLE_AGENT ===\n")
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

# Now run a test to see the actual descriptions used in the agent
print("\n=== ACTUAL DESCRIPTIONS USED IN LIVE AGENT ===\n")
print("Running the agent with a test message to extract descriptions...")

# Run the agent through the CLI
cmd = [
    "automagik-agents", "agent", "run", "message",
    "--agent", "simple_agent",
    "--message", "What are the parameters for the read_memory and write_memory tools?",
    "--session", f"desc-test-{os.getpid()}"
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
    response = result.stdout
    
    # Save the full output to a file
    with open("agent_response.txt", "w") as f:
        f.write(response)
    
    print("\nAgent response saved to agent_response.txt")
    
    # Try to extract the descriptions from the response
    read_desc_start = response.find("read_memory Tool")
    write_desc_start = response.find("write_memory Tool")
    
    if read_desc_start > 0:
        read_part = response[read_desc_start:write_desc_start]
        print("\nREAD_MEMORY FROM AGENT RESPONSE:")
        print("-" * 80)
        print(read_part.strip())
        print("-" * 80)
    
    if write_desc_start > 0:
        write_part = response[write_desc_start:].split("\n\n")[0]
        print("\nWRITE_MEMORY FROM AGENT RESPONSE:")
        print("-" * 80)
        print(write_part.strip())
        print("-" * 80)
    
    # Also extract from the JSON response if present
    json_start = response.find("API Response: {")
    if json_start > 0:
        json_str = response[json_start + len("API Response: "):]
        try:
            # Try to find the JSON part
            json_obj = json.loads(json_str)
            if "message" in json_obj:
                print("\nEXTRACTED FROM JSON RESPONSE:")
                print("-" * 80)
                print(json_obj["message"])
                print("-" * 80)
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            
except Exception as e:
    print(f"Error running agent: {e}")

print("\nScript complete!")
