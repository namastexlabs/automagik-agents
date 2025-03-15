"""Simple agent type package.

This package contains agents that provide basic functionality like date/time information.
"""

# Export sofia agent (the most updated agent)
from src.agents.simple.sofia_agent import default_agent as sofia_agent

# Export creator function
from src.agents.simple.sofia_agent import create_sofia_agent
