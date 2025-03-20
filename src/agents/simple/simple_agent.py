"""
Simple agent module that forwards imports from the simple_agent package.

This is a convenience module to make imports cleaner.
"""

# Import directly from the package
from src.agents.simple.simple_agent import default_agent
from src.agents.simple.simple_agent import create_simple_agent
from src.agents.simple.simple_agent.agent import SimpleAgent

__all__ = ["default_agent", "create_simple_agent", "SimpleAgent"] 