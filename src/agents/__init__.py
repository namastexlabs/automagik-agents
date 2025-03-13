"""Agents package.

This package contains all agent implementations.
"""

# Import simple agents
from src.agents.simple import simple_agent, notion_agent, discord_agent
from src.agents.simple import create_simple_agent, create_notion_agent, create_discord_agent

# Graph-based agents (removed)
# The graph folder has been removed from the project
# from src.agents.graph.stan_agent import default_agent as stan_agent
# from src.agents.graph.stan_agent import create_stan_agent 