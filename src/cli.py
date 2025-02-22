import shutil
from pathlib import Path
import typer
import os
import uvicorn
from typing import Optional
from src.config import load_settings

app = typer.Typer()
api_app = typer.Typer()
app.add_typer(api_app, name="api")

@app.command("create-agent")
def create_agent(
    name: str = typer.Option(..., "--name", "-n", help="Name of the new agent to create")
):
    """
    Create a new agent by cloning the simple_agent template in src/agents/simple_agent,
    and renaming placeholders accordingly.
    """
    # Define the agents directory and the destination folder
    agents_dir = Path(__file__).resolve().parent.parent / 'src' / 'agents'
    destination = agents_dir / name
    if destination.exists():
        typer.echo(f"Error: Folder {destination} already exists.")
        raise typer.Exit(code=1)

    # Define the template folder
    template_path = agents_dir / 'simple_agent'
    if not template_path.exists() or not template_path.is_dir():
        typer.echo(f"Error: Simple agent template folder {template_path} does not exist.")
        raise typer.Exit(code=1)

    # Copy the entire template folder to the destination folder
    shutil.copytree(template_path, destination)

    # Compute the new agent class name based on the provided name
    new_agent_class = ''.join(word.capitalize() for word in name.split('_')) + "Agent"

    # Recursively update file contents and filenames in the destination folder
    for root, dirs, files in os.walk(destination, topdown=False):
        for file in files:
            file_path = Path(root) / file
            # Attempt to read file as text
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Replace the placeholder 'SimpleAgent' with new_agent_class in file contents
                new_content = content.replace("SimpleAgent", new_agent_class)
                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
            except Exception:
                # Skip non-text files
                pass

            # Rename file if its name contains 'simple_agent'
            if "simple_agent" in file:
                new_file = file.replace("simple_agent", name)
                new_file_path = Path(root) / new_file
                file_path.rename(new_file_path)

        # Rename directories if needed
        for dir_name in dirs:
            if "simple_agent" in dir_name:
                old_dir = Path(root) / dir_name
                new_dir = Path(root) / dir_name.replace("simple_agent", name)
                os.rename(old_dir, new_dir)

    typer.echo(f"Agent '{name}' created successfully in {destination}.")

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

@app.callback()
def main():
    """
    Automagik CLI tool.
    """
    pass

if __name__ == "__main__":
    app()
