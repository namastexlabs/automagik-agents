"""Simple agent type package.

This package contains agents that provide basic functionality like date/time information.
"""

# Export simple agent with pydantic-ai capabilities
from src.agents.simple.simple_agent import default_agent as simple_agent

# Export creator function for simple agent
from src.agents.simple.simple_agent import create_simple_agent
