"""
Basic Python Project Template

Simple Python project with settings and main entry point
"""

TEMPLATE = {
    "name": "Basic Python Project",
    "description": "Simple Python project with settings and main entry point",
    "files": {
        "README.md": lambda name: f"""# {name}

Created with dhruvkit.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python src/main.py
```

## Project Structure

```
{name}/
├── src/
│   ├── main.py       # Main entry point
│   └── settings.py   # Configuration and environment variables
├── .env              # Environment variables (not committed to git)
├── .gitignore
├── requirements.txt
└── README.md
```
""",
        ".env": lambda name: """# Environment Variables
ENV_VARIABLE=your_value_here
""",
        ".gitignore": lambda name: """__pycache__/
.env
.venv/
venv/
*.pyc
*.pyo
*.egg-info/
dist/
build/
*.xlsx
.DS_Store
""",
        "requirements.txt": lambda name: """python-decouple>=3.8
""",
        "src/main.py": lambda name: """def main():
    print("Hello, World! This is a basic Python project created with dhruvkit.")

if __name__ == '__main__':
    main()
""",
        "src/settings.py": lambda name: """from decouple import config

ENV_VARIABLE = config('ENV_VARIABLE', default='')
"""
    }
}
