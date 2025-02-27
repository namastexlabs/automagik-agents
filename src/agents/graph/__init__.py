"""Graph-based agent type package.

This package contains agents that use graph-based workflows for more complex interactions.
"""

# Export all agents from this type
from src.agents.graph.stan_agent import default_agent as stan_agent

# Export creator functions
from src.agents.graph.stan_agent import create_stan_agent 