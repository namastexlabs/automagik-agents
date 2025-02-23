import shutil
from pathlib import Path
import typer
import os
import uvicorn
from typing import Optional, List
from src.config import load_settings

app = typer.Typer()
api_app = typer.Typer()
app.add_typer(api_app, name="api")

def get_available_templates() -> List[str]:
    """Get list of available agent templates (full folder names)."""
    agents_dir = Path(__file__).resolve().parent.parent / 'src' / 'agents'
    templates = []
    for item in agents_dir.iterdir():
        if item.is_dir() and item.name not in ['models', '__pycache__']:
            templates.append(item.name)
    return templates

@app.command("create-agent")
def create_agent(
    name: str = typer.Option(..., "--name", "-n", help="Name of the new agent to create"),
    template: str = typer.Option("simple_agent", "--template", "-t", help="Template folder to use as base (e.g., 'simple_agent', 'notion_agent')")
):
    """
    Create a new agent by cloning an existing agent template.
    
    The template should be the full folder name from src/agents directory.
    By default, it uses the simple_agent template.
    """
    # Define the agents directory and the destination folder
    agents_dir = Path(__file__).resolve().parent.parent / 'src' / 'agents'
    destination = agents_dir / f"{name}_agent"
    
    # Check if destination already exists
    if destination.exists():
        typer.echo(f"Error: Folder {destination} already exists.")
        raise typer.Exit(code=1)

    # Get available templates
    available_templates = get_available_templates()
    if template not in available_templates:
        typer.echo(f"Error: Template '{template}' not found. Available templates: {', '.join(available_templates)}")
        raise typer.Exit(code=1)

    # Define the template folder
    template_path = agents_dir / template
    if not template_path.exists() or not template_path.is_dir():
        typer.echo(f"Error: Template folder {template_path} does not exist.")
        raise typer.Exit(code=1)

    # Copy the template folder to the destination folder
    shutil.copytree(template_path, destination)

    # Get the base names without _agent suffix for class naming
    template_base = template.replace('_agent', '')
    
    # Compute the new agent class name and the template class name
    new_agent_class = ''.join(word.capitalize() for word in name.split('_')) + "Agent"
    template_class = ''.join(word.capitalize() for word in template_base.split('_')) + "Agent"
    create_func_name = f"create_{name}_agent"
    template_func_name = f"create_{template_base}_agent"

    # Recursively update file contents and filenames in the destination folder
    for root, dirs, files in os.walk(destination, topdown=False):
        for file in files:
            file_path = Path(root) / file
            # Attempt to read file as text
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace class names and function names, but preserve config requirements
                new_content = content
                
                # Update import statements
                new_content = new_content.replace(
                    f"from src.agents.{template}.agent",
                    f"from src.agents.{name}_agent.agent"
                )
                new_content = new_content.replace(
                    f"from src.agents.{template_base}_agent.agent",
                    f"from src.agents.{name}_agent.agent"
                )
                
                # Only replace exact class name matches (with word boundaries)
                new_content = new_content.replace(f" {template_class}", f" {new_agent_class}")
                new_content = new_content.replace(f"({template_class}", f"({new_agent_class}")
                new_content = new_content.replace(f"[{template_class}", f"[{new_agent_class}")
                new_content = new_content.replace(f":{template_class}", f":{new_agent_class}")
                
                # Replace function names
                new_content = new_content.replace(template_func_name, create_func_name)
                
                # Special handling for __init__.py to update docstrings
                if file == "__init__.py":
                    new_content = new_content.replace(
                        f"Create and initialize a {template_class} instance",
                        f"Create and initialize a {new_agent_class} instance"
                    )
                
                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
            except Exception as e:
                typer.echo(f"Warning: Could not process file {file_path}: {str(e)}")
                continue

            # Rename file if it contains the template name
            if template_base in file:
                new_file = file.replace(template_base, name)
                new_file_path = Path(root) / new_file
                file_path.rename(new_file_path)

        # Rename directories if needed
        for dir_name in dirs:
            if template_base in dir_name:
                old_dir = Path(root) / dir_name
                new_dir = Path(root) / dir_name.replace(template_base, name)
                os.rename(old_dir, new_dir)

    typer.echo(f"Agent '{name}' created successfully in {destination} (based on {template} template).")
    typer.echo(f"The new agent class is named '{new_agent_class}'.")
    typer.echo(f"The initialization function is named '{create_func_name}'.")
    typer.echo("\nYou can now:")
    typer.echo(f"1. Edit {destination}/prompts/prompt.py to customize the agent's system prompt")
    typer.echo(f"2. Edit {destination}/agent.py to customize agent behavior")
    typer.echo(f"3. Edit {destination}/__init__.py to customize initialization config")

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
