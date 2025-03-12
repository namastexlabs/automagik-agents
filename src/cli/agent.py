"""
Agent management commands for Automagik Agents.
"""
import shutil
from pathlib import Path
import typer
import os

# Create the agent command group
agent_app = typer.Typer()

def get_available_categories() -> list[str]:
    """Get list of available agent categories (top-level directories)."""
    agents_dir = Path(__file__).resolve().parent.parent.parent / 'src' / 'agents'
    categories = []
    for item in agents_dir.iterdir():
        if item.is_dir() and item.name not in ['models', '__pycache__']:
            categories.append(item.name)
    return categories

def get_available_templates(category: str) -> list[str]:
    """Get list of available agent templates within a category."""
    agents_dir = Path(__file__).resolve().parent.parent.parent / 'src' / 'agents'
    category_dir = agents_dir / category
    templates = []
    
    if category_dir.exists() and category_dir.is_dir():
        for item in category_dir.iterdir():
            if item.is_dir() and item.name not in ['__pycache__']:
                templates.append(item.name)
    
    return templates

@agent_app.command("create")
def create_agent(
    name: str = typer.Option(..., "--name", "-n", help="Name of the new agent to create"),
    category: str = typer.Option("simple", "--category", "-c", help="Category folder to use (e.g., 'simple', 'graph')"),
    template: str = typer.Option("simple_agent", "--template", "-t", help="Template folder to use as base (e.g., 'simple_agent', 'notion_agent')")
):
    """
    Create a new agent by cloning an existing agent template.
    
    The agent will be created in the specified category folder (e.g., simple, graph).
    The template should be the name of an existing agent within that category.
    By default, it uses the simple_agent template in the simple category.
    """
    # Define the agents directory and category paths
    agents_dir = Path(__file__).resolve().parent.parent.parent / 'src' / 'agents'
    category_dir = agents_dir / category
    
    # Ensure category exists
    available_categories = get_available_categories()
    if category not in available_categories:
        typer.echo(f"Error: Category '{category}' not found. Available categories: {', '.join(available_categories)}")
        raise typer.Exit(code=1)
    
    # Define the destination folder inside the category
    destination = category_dir / f"{name}_agent"
    
    # Check if destination already exists
    if destination.exists():
        typer.echo(f"Error: Folder {destination} already exists.")
        raise typer.Exit(code=1)

    # Get available templates in the category
    available_templates = get_available_templates(category)
    if not available_templates:
        typer.echo(f"Error: No templates found in category '{category}'.")
        raise typer.Exit(code=1)
    
    if template not in available_templates:
        typer.echo(f"Error: Template '{template}' not found in category '{category}'. Available templates: {', '.join(available_templates)}")
        raise typer.Exit(code=1)

    # Define the template folder
    template_path = category_dir / template
    if not template_path.exists() or not template_path.is_dir():
        typer.echo(f"Error: Template folder {template_path} does not exist.")
        raise typer.Exit(code=1)

    # Copy the template folder to the destination folder
    shutil.copytree(template_path, destination)

    # Get the base names without _agent suffix for class naming
    template_base = template.replace('_agent', '')
    name_base = name
    
    # Compute the new agent class name and the template class name
    new_agent_class = ''.join(word.capitalize() for word in name.split('_')) + "Agent"
    template_class = ''.join(word.capitalize() for word in template_base.split('_')) + "Agent"
    create_func_name = f"create_{name}_agent"
    template_func_name = f"create_{template_base}_agent"

    # Recursively update file contents and filenames in the destination folder
    for root, dirs, files in os.walk(destination, topdown=False):
        for file in files:
            file_path = Path(root) / file
            # Skip binary files like __pycache__
            if '__pycache__' in str(file_path) or file.endswith('.pyc'):
                continue
                
            # Attempt to read file as text
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace class names and function names, but preserve config requirements
                new_content = content
                
                # Handle various import patterns
                # 1. Direct imports from the template's module
                for potential_import_path in [
                    f"from src.agents.{template}",
                    f"from src.agents.{template_base}_agent",
                    f"from src.agents.{category}.{template}",
                    f"from src.agents.{category}.{template_base}_agent",
                    f"import src.agents.{template}",
                    f"import src.agents.{template_base}_agent",
                    f"import src.agents.{category}.{template}",
                    f"import src.agents.{category}.{template_base}_agent",
                ]:
                    replacement = potential_import_path.replace(
                        template if template in potential_import_path else template_base + "_agent", 
                        f"{name}_agent"
                    )
                    new_content = new_content.replace(potential_import_path, replacement)
                
                # 2. Handle any other template references in import statements
                new_content = new_content.replace(
                    f"src.agents.{template}.agent",
                    f"src.agents.{category}.{name}_agent.agent"
                )
                new_content = new_content.replace(
                    f"src.agents.{template_base}_agent.agent",
                    f"src.agents.{category}.{name}_agent.agent"
                )
                new_content = new_content.replace(
                    f"src.agents.{category}.{template}.agent",
                    f"src.agents.{category}.{name}_agent.agent"
                )
                new_content = new_content.replace(
                    f"src.agents.{category}.{template_base}_agent.agent",
                    f"src.agents.{category}.{name}_agent.agent"
                )
                
                # Handle references to simple_agent specifically (common in many templates)
                if template != "simple_agent" and template_base != "simple":
                    new_content = new_content.replace(
                        "src.agents.simple.simple_agent",
                        f"src.agents.{category}.{name}_agent"
                    )
                    new_content = new_content.replace(
                        f"src.agents.{category}.simple_agent",
                        f"src.agents.{category}.{name}_agent"
                    )
                
                # Handle direct simple_agent imports in any category
                new_content = new_content.replace(
                    "from src.agents.test_agent.simple_agent",
                    f"from src.agents.{category}.{name}_agent"
                )
                
                # Only replace exact class name matches (with word boundaries)
                new_content = new_content.replace(f" {template_class}", f" {new_agent_class}")
                new_content = new_content.replace(f"({template_class}", f"({new_agent_class}")
                new_content = new_content.replace(f"[{template_class}", f"[{new_agent_class}")
                new_content = new_content.replace(f":{template_class}", f":{new_agent_class}")
                new_content = new_content.replace(f"\"{template_class}", f"\"{new_agent_class}")
                new_content = new_content.replace(f"'{template_class}", f"'{new_agent_class}")
                
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

    typer.echo(f"Agent '{name}' created successfully in {destination} (based on {template} template in {category} category).")
    typer.echo(f"The new agent class is named '{new_agent_class}'.")
    typer.echo(f"The initialization function is named '{create_func_name}'.")
    typer.echo("\nYou can now:")
    typer.echo(f"1. Edit {destination}/prompts/prompt.py to customize the agent's system prompt")
    typer.echo(f"2. Edit {destination}/agent.py to customize agent behavior")
    typer.echo(f"3. Edit {destination}/__init__.py to customize initialization config") 