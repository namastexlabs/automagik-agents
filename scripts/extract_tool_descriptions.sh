#!/bin/bash

# Script to extract tool descriptions from CLI app output

echo "===== EXTRACTING MEMORY TOOL DESCRIPTIONS ====="
echo ""

# Run the agent with a specific question to get tool descriptions
AUTOMAGIK_OUTPUT=$(automagik-agents --debug agent run message \
  --agent simple_agent \
  --message "Tell me how I can use the read_memory and write_memory tools, including what parameters I can use with them" \
  --session extract-tool-desc-$(date +%s))

# Save full output for reference
echo "$AUTOMAGIK_OUTPUT" > tool_descriptions_full_output.txt
echo "Full output saved to tool_descriptions_full_output.txt"

# Extract and format the assistant's response
echo ""
echo "===== READ_MEMORY TOOL DESCRIPTION ====="
echo ""
echo "$AUTOMAGIK_OUTPUT" | grep -A 15 "read_memory Tool" | head -n 15

echo ""
echo "===== WRITE_MEMORY TOOL DESCRIPTION ====="
echo ""
echo "$AUTOMAGIK_OUTPUT" | grep -A 15 "write_memory Tool" | head -n 15

echo ""
echo "===== EXTRACTION COMPLETE ====="
