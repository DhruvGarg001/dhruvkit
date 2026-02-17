"""
DhruvKit CLI - Main entry point

A project scaffolding tool to quickly create Python projects
with various templates (basic, flask, fastapi, etc.)
"""

import sys
from rich.console import Console

from dhruvkit.commands import cmd_new, cmd_init, cmd_add, cmd_docs

console = Console()

def main():
    """
    Main CLI entry point
    
    Parses command line arguments and routes to appropriate command handler
    """
    args = sys.argv
    
    if len(args) < 2:
        console.print("[red]❌ Error:[/red] No command specified. \n")
        console.print("[yellow]Usage:[/yellow] dhruvkit <command> [options] \n")
        console.print("[dim]Run 'dhruvkit --help' or 'dhruvkit docs' for help.[/dim] \n")
        return
    
    command = args[1]
    
    # Handle help flags
    if command in ["--help", "-h", "help"]:
        cmd_docs(["dhruvkit", "docs"])
        return
    
    # Route to appropriate command handler
    if command == "new":
        cmd_new(args)
    elif command == "init":
        cmd_init(args)
    elif command == "add":
        cmd_add(args)
    elif command == "docs":
        cmd_docs(args)
    else:
        console.print(f"[red]❌ Error:[/red] Unknown command '{command}' \n")
        console.print("[yellow]Available commands:[/yellow] new, init, add, docs \n")
        console.print("[dim]Run 'dhruvkit --help' or 'dhruvkit docs' for help.[/dim] \n")

if __name__ == "__main__":
    main()
