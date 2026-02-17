"""
Flask Web Application Template

Flask web application with basic structure
"""

TEMPLATE = {
    "name": "Flask Web Application",
    "description": "Flask web application with basic structure",
    "files": {
        "README.md": lambda name: f"""# {name}

Flask web application created with dhruvkit.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
flask run
```

## Project Structure

```
{name}/
├── src/
│   ├── main.py       # Flask application
│   └── settings.py   # Configuration
├── .env              # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Features

- Flask web framework
- Environment variable configuration
- Development server ready
""",
        ".env": lambda name: """FLASK_APP=src/main.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
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
instance/
.DS_Store
""",
        "requirements.txt": lambda name: """flask>=3.0.0
python-decouple>=3.8
""",
        "src/main.py": lambda name: """from flask import Flask
from settings import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return 'Hello from Flask!'

@app.route('/health')
def health():
    return {'status': 'healthy'}

@app.route('/dhruvkit')
def dhruvkit():
    return 'I love DhruvKit!'

if __name__ == '__main__':
    app.run(debug=True)
""",
        "src/settings.py": lambda name: """from decouple import config

SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')
FLASK_ENV = config('FLASK_ENV', default='production')
FLASK_APP = config('FLASK_APP', default='src/main.py')
"""
    }
}
