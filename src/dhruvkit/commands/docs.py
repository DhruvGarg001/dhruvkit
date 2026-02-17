"""
'docs' command - Show documentation for dhruvkit commands
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dhruvkit.templates import TEMPLATES, TEMPLATE_ADDONS
from dhruvkit.licenses import AVAILABLE_LICENSES

console = Console()

# Documentation for each command
DOCS = {
    "new": {
        "usage": "dhruvkit new [folder_name] [--template|-t TEMPLATE] [--license LICENSE] [addons...]",
        "description": "Create a new project",
        "examples": [
            "dhruvkit new              # Prompts for folder name",
            "dhruvkit new my_project   # Creates 'my_project' folder",
            "dhruvkit new my_app --template fastapi            # Creates FastAPI project",
            "dhruvkit new my_api --template fastapi --mongodb  # FastAPI with MongoDB",
            "dhruvkit new my_api --template fastapi --firebase # FastAPI with Firebase",
            "dhruvkit new my_api --template fastapi --mongodb --firebase  # Combine both!",
            "dhruvkit new my_app --license apache              # Add Apache 2.0 license",
            "dhruvkit new my_app --template flask --license mit  # Flask with MIT license"
        ]
    },
    "init": {
        "usage": "dhruvkit init [--template|-t TEMPLATE] [--license LICENSE] [addons...]",
        "description": "Initialize a project in the current directory",
        "examples": [
            "dhruvkit init            # Creates files in current directory",
            "dhruvkit init --template fastapi         # Initialize FastAPI project",
            "dhruvkit init --template fastapi --mongodb # Initialize FastAPI with MongoDB",
            "dhruvkit init --template fastapi --firebase # Initialize FastAPI with Firebase",
            "dhruvkit init --template fastapi --mongodb --firebase # Combine both!",
            "dhruvkit init --license gpl              # Add GPL-2.0 license"
        ]
    },
    "add": {
        "usage": "dhruvkit add --license LICENSE",
        "description": "Add components to existing project",
        "examples": [
            "dhruvkit add --license mit      # Add MIT license to current project",
            "dhruvkit add --license apache   # Add Apache 2.0 license",
            "dhruvkit add --license gpl      # Add GPL-2.0 license"
        ]
    },
    "docs": {
        "usage": "dhruvkit docs [command]",
        "description": "Show documentation for dhruvkit commands",
        "examples": [
            "dhruvkit docs           # Show all documentation",
            "dhruvkit docs new       # Show docs for 'new' command",
            "dhruvkit docs init      # Show docs for 'init' command"
        ]
    }
}

def cmd_docs(args: list):
    """
    Show documentation
    
    Usage:
        dhruvkit docs [command]
    
    Args:
        args: Command line arguments (sys.argv)
    """
    console.print(Panel("[bold blue]📚 DhruvKit Documentation[/bold blue]", style="blue"))
    console.print()
    console.print("[dim]💡 Tip: Use [bold]dk[/bold] as a shorthand for [bold]dhruvkit[/bold] in all commands![/dim]")
    console.print()
    
    # Show specific command docs if a command name is provided
    # args = ["dhruvkit", "docs", "new"] -> show docs for "new"
    # args = ["dhruvkit", "docs"] -> show all docs
    if len(args) > 2:
        cmd = args[2]
        if cmd in DOCS:
            doc = DOCS[cmd]
            console.print(f"[bold cyan]Command:[/bold cyan] {cmd}")
            console.print(f"[bold]Usage:[/bold] {doc['usage']}")
            console.print(f"[bold]Description:[/bold] {doc['description']}")
            console.print("\n[bold]Examples:[/bold]")
            for example in doc['examples']:
                console.print(f"  [green]•[/green] {example}")
            console.print()
        else:
            console.print(f"[red]❌ Error:[/red] No documentation found for '{cmd}'")
            console.print(f"[yellow]Available commands:[/yellow] {', '.join(DOCS.keys())}")
        return
    
    # Show all commands
    table = Table(title="Available Commands", show_header=True, header_style="bold cyan")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")
    
    for cmd, doc in DOCS.items():
        table.add_row(cmd, doc['description'])
    
    console.print(table)
    console.print()
    
    # Show examples for key commands
    console.print("[bold cyan]Quick Examples:[/bold cyan]")
    console.print()
    
    for cmd in ["new", "init", "add"]:  # Show examples for main commands
        doc = DOCS[cmd]
        console.print(f"[bold]{cmd}:[/bold] [yellow]{doc['usage']}[/yellow]")
        for example in doc['examples']:  # Show all examples
            console.print(f"  [green]•[/green] {example}")
        console.print()
    
    # Show templates
    console.print("[bold cyan]Available Templates:[/bold cyan] [dim](default: basic)[/dim]")
    for template_name, template in TEMPLATES.items():
        console.print(f"  [green]•[/green] [bold]{template_name}[/bold] - {template['description']}")
        
        # Show add-ons for this template if any
        if template_name in TEMPLATE_ADDONS and TEMPLATE_ADDONS[template_name]:
            addons = TEMPLATE_ADDONS[template_name]
            console.print(f"    [yellow]Add-ons:[/yellow]")
            for addon_name, addon_info in addons.items():
                console.print(f"      [cyan]--{addon_name}[/cyan] - {addon_info['description']}")
    console.print()
    
    # Show licenses
    console.print("[bold cyan]Available Licenses:[/bold cyan] [dim](optional)[/dim]")
    for license_key, license_desc in AVAILABLE_LICENSES.items():
        console.print(f"  [green]•[/green] [bold]{license_key}[/bold] - {license_desc}")
    console.print()
    
    # Show installation info
    console.print("[bold cyan]💡 Installation with Dependencies:[/bold cyan]")
    console.print("  [green]•[/green] [bold]pip install dhruvkit\\[fastapi][/bold] - Install with FastAPI dependencies")
    console.print("  [green]•[/green] [bold]pip install dhruvkit\\[flask][/bold] - Install with Flask dependencies")
    console.print("  [green]•[/green] [bold]pip install dhruvkit\\[mongodb][/bold] - Install with MongoDB dependencies")
    console.print("  [green]•[/green] [bold]pip install dhruvkit\\[firebase][/bold] - Install with Firebase dependencies")
    console.print("  [green]•[/green] [bold]pip install dhruvkit\\[fastapi,mongodb,firebase][/bold] - Combine multiple")
    console.print()
    
    console.print("[dim]Use 'dhruvkit docs <command>' or 'dk docs <command>' for detailed help on a specific command.[/dim]")
    console.print()
