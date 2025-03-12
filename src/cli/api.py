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

@api_app.command("start")
def start_api(
    host: str = typer.Option(None, "--host", "-h", help="Host to bind the server to (overrides AM_HOST from .env)"),
    port: int = typer.Option(None, "--port", "-p", help="Port to bind the server to (overrides AM_PORT from .env)"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload on code changes"),
    workers: Optional[int] = typer.Option(None, "--workers", "-w", help="Number of worker processes"),
):
    """
    Start the FastAPI server with uvicorn using settings from .env
    """
    # Load settings from .env
    settings = load_settings()
    
    # Use command line arguments if provided, otherwise use settings from .env
    final_host = host or settings.AM_HOST
    final_port = port or settings.AM_PORT

    typer.echo(f"Starting API server on {final_host}:{final_port}")
    uvicorn.run(
        "src.main:app",
        host=final_host,
        port=final_port,
        reload=reload,
        workers=workers
    ) 