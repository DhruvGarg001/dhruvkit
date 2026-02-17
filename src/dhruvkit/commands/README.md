# DhruvKit Commands

This folder contains all the command implementations for DhruvKit. Each command is in its own file for better organization and maintainability.

## Structure

```
commands/
├── __init__.py      # Exports all commands
├── new.py          # 'dhruvkit new' command
├── init.py         # 'dhruvkit init' command
├── add.py          # 'dhruvkit add' command
└── docs.py         # 'dhruvkit docs' command
```

## Adding a New Command

To add a new command (e.g., `dhruvkit build`):

1. **Create a new file**: `commands/build.py`

```python
"""
'build' command - Build the project
"""

from rich.console import Console

console = Console()

def cmd_build(args: list):
    """
    Build the project
    
    Usage:
        dhruvkit build [options]
    
    Args:
        args: Command line arguments (sys.argv)
    """
    console.print("[bold blue]Building project...[/bold blue]")
    # Your command implementation here
```

2. **Export the command** in `__init__.py`:

```python
from .build import cmd_build

__all__ = ['cmd_new', 'cmd_init', 'cmd_docs', 'cmd_build']
```

3. **Register in CLI** (`cli.py`):

```python
from dhruvkit.commands import cmd_new, cmd_init, cmd_docs, cmd_build

# In main():
elif command == "build":
    cmd_build(args)
```

4. **Add documentation** in `commands/docs.py`:

```python
DOCS = {
    # ... existing docs
    "build": {
        "usage": "dhruvkit build [options]",
        "description": "Build the project",
        "examples": [
            "dhruvkit build           # Build with default settings",
            "dhruvkit build --prod    # Production build"
        ]
    }
}
```

## Command Guidelines

- Each command file should have a single main function: `cmd_<name>(args: list)`
- Use the `rich` library for beautiful console output
- Include docstrings explaining usage and arguments
- Handle errors gracefully with clear error messages
- Keep commands focused on a single responsibility
