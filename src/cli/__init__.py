"""
CLI module for Automagik Agents.
This module contains the CLI commands and utilities.
"""
import typer
import os
import sys
from typing import Optional, List, Callable
from src.cli.db import db_app
from src.cli.api import api_app
from src.cli.agent import agent_app

# Handle --debug flag immediately before any other imports
# This makes sure the environment variable is set before any module is imported
debug_mode = "--debug" in sys.argv
if debug_mode:
    os.environ["AM_LOG_LEVEL"] = "DEBUG"
    print(f"Debug mode enabled. Environment variable AM_LOG_LEVEL set to DEBUG")

# Now import config after setting environment variables
from src.config import LogLevel, Settings, mask_connection_string
from pathlib import Path
from dotenv import load_dotenv

# Create the main CLI app with global options
app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Define a callback that runs before any command
def global_callback(ctx: typer.Context, debug: bool = False):
    """Global callback for all commands to process common options."""
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"
        # Print configuration info
        try:
            from src.config import settings
            print("🔧 Configuration loaded:")
            print(f"├── Environment: {settings.AM_ENV}")
            print(f"├── Log Level: {settings.AM_LOG_LEVEL}")
            print(f"├── Server: {settings.AM_HOST}:{settings.AM_PORT}")
            print(f"├── OpenAI API Key: {settings.OPENAI_API_KEY[:5]}...{settings.OPENAI_API_KEY[-5:]}")
            print(f"├── API Key: {settings.AM_API_KEY[:5]}...{settings.AM_API_KEY[-5:]}")
            print(f"├── Discord Bot Token: {settings.DISCORD_BOT_TOKEN[:5]}...{settings.DISCORD_BOT_TOKEN[-5:]}")
            print(f"├── Database URL: {mask_connection_string(settings.DATABASE_URL)}")

            if settings.NOTION_TOKEN:
                print(f"└── Notion Token: {settings.NOTION_TOKEN[:5]}...{settings.NOTION_TOKEN[-5:]}")
            else:
                print("└── Notion Token: Not set")
        except Exception as e:
            print(f"Error displaying configuration: {str(e)}")

# Add subcommands with the global debug option
app.add_typer(api_app, name="api")
app.add_typer(db_app, name="db")
app.add_typer(agent_app, name="agent")

# Default callback for main app
@app.callback()
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode (shows detailed configuration)", is_flag=True)
):
    """
    Automagik CLI tool.
    """
    # Call the global callback with the debug flag
    global_callback(ctx, debug) 