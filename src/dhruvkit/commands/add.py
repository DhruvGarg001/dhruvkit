"""
'add' command - Add components to existing project
"""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from dhruvkit.licenses import get_license, AVAILABLE_LICENSES

console = Console()

def cmd_add(args: list):
    """
    Add components to existing project in current directory
    
    Usage:
        dhruvkit add --license LICENSE
    
    Args:
        args: Command line arguments (sys.argv)
    """
    # Handle help flag
    if "--help" in args or "-h" in args:
        from dhruvkit.commands.docs import cmd_docs
        cmd_docs(["dhruvkit", "docs", "add"])
        return
    
    console.print(Panel("[bold blue]➕ DhruvKit - Add Component[/bold blue]", style="blue"))
    
    # Check for --license flag
    if "--license" not in args:
        console.print("[red]❌ Error:[/red] No component specified.")
        console.print("[yellow]Usage:[/yellow] dhruvkit add --license LICENSE_NAME")
        console.print(f"[yellow]Available licenses:[/yellow] {', '.join(AVAILABLE_LICENSES.keys())}")
        return
    
    # Parse license from args
    license_name = "mit"  # Default to MIT
    idx = args.index("--license")
    if idx + 1 < len(args):
        license_name = args[idx + 1]
    
    if license_name.lower() not in [k.lower() for k in AVAILABLE_LICENSES.keys()]:
        console.print(f"[red]❌ Error:[/red] License '{license_name}' not found.")
        console.print(f"[yellow]Available licenses:[/yellow] {', '.join(AVAILABLE_LICENSES.keys())}")
        return
    
    # Get current directory info
    root = Path.cwd()
    project_name = root.name
    
    # Check if LICENSE already exists
    license_path = root / "LICENSE"
    if license_path.exists():
        overwrite = input(f"⚠️ LICENSE file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite not in ['y', 'yes']:
            console.print("[yellow]Cancelled.[/yellow]")
            return
    
    # Create LICENSE file
    console.print(f"\n[yellow]Adding license:[/yellow] [cyan]{license_name.upper()}[/cyan]")
    license_content = get_license(license_name, project_name)
    license_path.write_text(license_content, encoding='utf-8')
    
    console.print()
    console.print(f"[green]✅[/green] [bold]LICENSE[/bold] file created")
    console.print()
    
    console.print(Panel(
        f"[bold green]✅ Success![/bold green]\n\n"
        f"Added {license_name.upper()} license to your project.",
        style="green"
    ))
