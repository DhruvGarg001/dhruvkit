# DhruvKit Templates

This folder contains all the project templates available in DhruvKit. Each template is defined in its own Python file for easy maintenance and extensibility.

## Available Templates

- **basic**: Simple Python project with basic structure
- **flask**: Flask web application with blueprints
- **fastapi**: Modern FastAPI application with async support
  - Add-ons: `--mongodb` (MongoDB Atlas integration), `--firebase` (Firebase Admin SDK)
  - Can combine multiple add-ons: `--mongodb --firebase`

## Template Structure

Each template file (e.g., `basic.py`, `flask.py`, `fastapi.py`) exports a `TEMPLATE` dictionary with the following structure:

```python
TEMPLATE = {
    "name": "Template Display Name",
    "description": "Short description of the template",
    "files": {
        "path/to/file.ext": lambda name: "file content here",
        # ... more files
    }
}
```

## Adding a New Template

To add a new template:

1. Create a new Python file in this directory (e.g., `django.py`)
2. Define the `TEMPLATE` dictionary following the structure above
3. The file content can be:
   - A lambda function that takes `name` (project name) as parameter
   - Multi-line strings using triple quotes for better readability

Example (`django.py`):

```python
"""
Django Web Application Template

Full-featured Django web application
"""

TEMPLATE = {
    "name": "Django Web Application",
    "description": "Full-featured Django web application",
    "files": {
        "README.md": lambda name: f\"\"\"# {name}

Django application created with dhruvkit.

## Getting Started

\`\`\`bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
\`\`\`
\"\"\",
        ".env": lambda name: \"\"\"SECRET_KEY=your-secret-key-here
DEBUG=True
\"\"\",
        "requirements.txt": lambda name: \"\"\"django>=5.0.0
python-decouple>=3.8
\"\"\",
        "manage.py": lambda name: \"\"\"#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    # ... Django management code
\"\"\"
    }
}
```

4. The template will be automatically loaded by the `__init__.py` module
5. Users can create projects with: `dhruvkit new myproject --template django`

## Template Add-ons

Templates can also export an `ADDONS` dictionary to provide modular extensions. Users can enable add-ons using flags like `--mongodb`, `--postgres`, etc.

### Add-on Structure

```python
ADDONS = {
    "addon_name": {
        "name": "Add-on Display Name",
        "description": "Short description of what this add-on provides",
        "files": {
            "path/to/file.ext": lambda name: "file content here",
            # Files here will be merged with the base template
            # If a file exists in both, the add-on version overwrites it
        }
    }
}
```

### Example: FastAPI with MongoDB Add-on

```python
# fastapi.py

TEMPLATE = {
    "name": "FastAPI Application",
    "description": "FastAPI application with modern async structure",
    "files": {
        "src/main.py": lambda name: "...",
        "src/settings.py": lambda name: "...",
        # ... other files
    }
}

ADDONS = {
    "mongodb": {
        "name": "MongoDB Atlas Integration",
        "description": "Add MongoDB Atlas database support",
        "files": {
            "src/database_functions/__init__.py": lambda name: "...",
            "src/database_functions/MongoDBConfig.py": lambda name: "...",
            "src/dbconfig.py": lambda name: "...",
            "src/main.py": lambda name: "...updated main with lifespan...",
            "src/settings.py": lambda name: "...updated settings with DB config...",
            "docs/mongodb_usage.md": lambda name: "...",
            # These files override or extend the base template
        }
    }
}
```

### Using Add-ons

```bash
# Create FastAPI project with MongoDB add-on
dhruvkit new myapi --template fastapi --mongodb

# Create FastAPI project with Firebase add-on
dhruvkit new myapi --template fastapi --firebase

# Combine multiple add-ons (intelligently merged!)
dhruvkit new myapi --template fastapi --mongodb --firebase

# Initialize with add-ons in current directory
dhruvkit init --template fastapi --mongodb --firebase
```

**Note**: When combining add-ons like `--mongodb` and `--firebase`, dhruvkit intelligently merges conflicting files (like `main.py`, `settings.py`, `.env`) to include both integrations seamlessly.

### Add-on Best Practices

1. **File Overrides**: If an add-on needs to modify a base file (like `main.py` or `settings.py`), include the FULL updated version in the add-on
2. **New Files**: Add-ons can add entirely new files and folders
3. **Documentation**: Include documentation in a `docs/` folder explaining how to use the add-on features
4. **Dependencies**: Update `requirements.txt` to include new dependencies
5. **Environment Variables**: Update `.env` with new configuration variables

## File Paths

- Use forward slashes `/` for paths (works on all platforms)
- Create nested structures like `src/models/user.py`
- Create multiple folder levels like `src/database_functions/MongoDBConfig.py`
- Add documentation folders like `docs/usage.md`
- The directory structure will be created automatically

## Tips

- Use lambda functions for dynamic content (project name, etc.)
- Use triple-quoted strings for multi-line file content
- Add helpful comments in generated files
- Include a comprehensive README.md for each template
- Add .gitignore, .env, and requirements.txt files
- For complex templates, include a `docs/` folder with usage guides
- Use descriptive folder names: `database_functions/`, `api/`, `models/`, etc.

## Complex Template Example

For templates with multiple folders and documentation (like `fastapi_mongodb`):

```python
TEMPLATE = {
    "name": "Complex Application",
    "description": "Application with database and documentation",
    "files": {
        "README.md": lambda name: f"# {name}...",
        "src/database_functions/__init__.py": lambda name: "from .config import Config",
        "src/database_functions/config.py": lambda name: "class Config: ...",
        "src/main.py": lambda name: "from database_functions import Config...",
        "docs/usage.md": lambda name: "# Usage Guide...",
        "docs/api.md": lambda name: "# API Documentation...",
    }
}
```

This will create:
```
project/
├── README.md
├── src/
│   ├── database_functions/
│   │   ├── __init__.py
│   │   └── config.py
│   └── main.py
└── docs/
    ├── usage.md
    └── api.md
```
