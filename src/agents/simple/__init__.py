"""Simple agent type package.

This package contains agents that provide basic functionality like date/time information.
"""

# Export all agents from this type
from src.agents.simple.simple_agent import default_agent as simple_agent
from src.agents.simple.notion_agent import default_agent as notion_agent
from src.agents.simple.discord_agent import default_agent as discord_agent
from src.agents.simple.sofia_agent import default_agent as sofia_agent

# Export creator functions
from src.agents.simple.simple_agent import create_simple_agent
from src.agents.simple.notion_agent import create_notion_agent
from src.agents.simple.discord_agent import create_discord_agent
from src.agents.simple.sofia_agent import create_sofia_agent 