"""
'new' command - Create a new project in a new folder
"""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from dhruvkit.templates import TEMPLATES, TEMPLATE_ADDONS
from dhruvkit.utils import create_project_structure, display_created_files, apply_addons_to_template
from dhruvkit.licenses import get_license, AVAILABLE_LICENSES

console = Console()

def cmd_new(args: list):
    """
    Create a new project in a new folder
    
    Usage:
        dhruvkit new [folder_name] [--template|-t TEMPLATE]
    
    Args:
        args: Command line arguments (sys.argv)
    """
    # Handle help flag
    if "--help" in args or "-h" in args:
        from dhruvkit.commands.docs import cmd_docs
        cmd_docs(["dhruvkit", "docs", "new"])
        return
    
    console.print(Panel("[bold blue]🚀 DhruvKit - New Project[/bold blue]", style="blue"))
    
    # Parse template from args
    template_name = "basic"
    if "--template" in args or "-t" in args:
        idx = args.index("--template") if "--template" in args else args.index("-t")
        if idx + 1 < len(args):
            template_name = args[idx + 1]
            args = [a for i, a in enumerate(args) if i not in [idx, idx + 1]]
    
    # Parse license from args
    license_name = None  # No license by default
    if "--license" in args:
        idx = args.index("--license")
        if idx + 1 < len(args) and not args[idx + 1].startswith("--"):
            # Next arg exists and is not a flag, use it as license name
            license_name = args[idx + 1]
            args = [a for i, a in enumerate(args) if i not in [idx, idx + 1]]
        else:
            # --license flag without value or followed by another flag, use MIT as default
            license_name = "mit"
            args = [a for i, a in enumerate(args) if i != idx]
    
    # Parse add-on flags (e.g., --mongodb)
    addons_to_apply = []
    if template_name in TEMPLATE_ADDONS:
        available_addons = list(TEMPLATE_ADDONS[template_name].keys())
        for addon_name in available_addons:
            addon_flag = f"--{addon_name}"
            if addon_flag in args:
                addons_to_apply.append(addon_name)
                # Remove the flag from args
                args = [a for a in args if a != addon_flag]
    
    # Validate template
    if template_name not in TEMPLATES:
        console.print(f"[red]❌ Error:[/red] Template '{template_name}' not found.")
        console.print(f"[yellow]Available templates:[/yellow] {', '.join(TEMPLATES.keys())}")
        return
    
    # Get folder name
    # args = ["dhruvkit", "new", "my_app"] -> folder name is at args[2]
    if len(args) > 2:
        folder_name = args[2]
    else:
        folder_name = input("📂 Enter folder name: ").strip()
        if not folder_name:
            console.print("[red]❌ Error:[/red] Folder name cannot be empty.")
            return
    
    # Create project
    root = Path.cwd() / folder_name
    
    if root.exists():
        console.print(f"[red]❌ Error:[/red] Folder '{folder_name}' already exists.")
        return
    
    template = TEMPLATES[template_name]
    
    # Apply add-ons if any
    if addons_to_apply:
        template = apply_addons_to_template(template, addons_to_apply, TEMPLATE_ADDONS.get(template_name, {}))
    
    console.print(f"\n[yellow]Creating project with template:[/yellow] [cyan]{template['name']}[/cyan]")
    if addons_to_apply:
        console.print(f"[yellow]With add-ons:[/yellow] [cyan]{', '.join(addons_to_apply)}[/cyan]")
    if license_name:
        console.print(f"[yellow]Adding license:[/yellow] [cyan]{license_name.upper()}[/cyan]")
    
    created_items = create_project_structure(root, folder_name, template, license_name=license_name)
    display_created_files(folder_name, created_items, is_new=True)
    
    console.print(Panel(
        f"[bold green]✅ Success![/bold green]\n\n"
        f"Project '{folder_name}' created successfully.\n\n"
        f"Next steps:\n"
        f"  [cyan]cd {folder_name}[/cyan]\n"
        f"  [cyan]python -m venv .venv[/cyan]\n"
        f"  [cyan]pip install -r requirements.txt[/cyan]",
        style="green"
    ))
