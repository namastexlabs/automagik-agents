"""
API server management commands for Automagik Agents.
"""
import os
import typer
import uvicorn
from typing import Optional
from src.config import load_settings

# Create the API command group
api_app = typer.Typer()

@api_app.callback()
def api_callback(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode", is_flag=True, hidden=True)
):
    """
    API server management commands.
    
    Use the 'start' command to launch the API server.
    """
    # If debug flag is set, ensure AM_LOG_LEVEL is set to DEBUG
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"

@api_app.command("start")
def start_api(
    host: str = typer.Option(None, "--host", "-h", help="Host to bind the server to (overrides AM_HOST from .env)"),
    port: int = typer.Option(None, "--port", "-p", help="Port to bind the server to (overrides AM_PORT from .env)"),
    reload: bool = typer.Option(None, "--reload", help="Enable auto-reload on code changes (default: auto-enabled in development mode)"),
    workers: Optional[int] = typer.Option(None, "--workers", "-w", help="Number of worker processes"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode (sets LOG_LEVEL to DEBUG)", is_flag=True, hidden=True)
):
    """
    Start the FastAPI server with uvicorn using settings from .env
    """
    # Set debug mode if requested
    if debug:
        os.environ["AM_LOG_LEVEL"] = "DEBUG"
        
    # Load settings from .env
    settings = load_settings()
    
    # Use command line arguments if provided, otherwise use settings from .env
    final_host = host or settings.AM_HOST
    final_port = port or settings.AM_PORT

    # If reload is not explicitly set, auto-enable it in development mode
    if reload is None:
        from src.config import Environment
        reload = settings.AM_ENV == Environment.DEVELOPMENT
    
    # Log the reload status
    reload_status = "enabled" if reload else "disabled"
    typer.echo(f"Starting API server on {final_host}:{final_port} (auto-reload: {reload_status})")
    
    uvicorn.run(
        "src.main:app",
        host=final_host,
        port=final_port,
        reload=reload,
        workers=workers
    ) 