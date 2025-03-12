"""
CLI module for Automagik Agents.
This module contains the CLI commands and utilities.
"""
import typer
from src.cli.db import db_app
from src.cli.api import api_app
from src.cli.agent import agent_app

# Create the main CLI app
app = typer.Typer()

# Add subcommands
app.add_typer(api_app, name="api")
app.add_typer(db_app, name="db")
app.add_typer(agent_app, name="agent")

# Default callback
@app.callback()
def main():
    """
    Automagik CLI tool.
    """
    pass 