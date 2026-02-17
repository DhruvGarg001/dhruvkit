# 🚀 DhruvKit

> A powerful Python scaffolding toolkit for rapid project creation with intelligent template system, modular add-ons, and beautiful CLI interface.

[![PyPI version](https://img.shields.io/pypi/v/dhruvkit.svg)](https://pypi.org/project/dhruvkit/)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPL--2.0-blue.svg)](LICENSE)

---

<div align="center">

### 🎯 Create production-ready Python projects in seconds

```bash
pip install dhruvkit && dk new myproject --template fastapi --license mit
```

**[Get Started](#-quick-start)** • **[View Features](#-features)** • **[Documentation](#-documentation)**

</div>

---

## ✨ Features

- 🎨 **Beautiful CLI Interface** - Rich terminal output with colors, panels, and progress indicators
- 📦 **Smart Templates** - Pre-configured templates for FastAPI, Flask, and basic Python projects
- 🧩 **Modular Add-ons** - Mix and match features like MongoDB, Firebase, and security middleware
- 🔐 **License Support** - Generates projects with multiple license options (MIT, Apache, GPL, BSD, Unlicense, CC0)
- ⚡ **Intelligent Merging** - Automatically combines multiple add-ons without conflicts
- 🎯 **Zero configuration** - Ready to run immediately
- 📚 **Auto Documentation** - Generates comprehensive README and usage guides

> **📝 Note:** DhruvKit itself is licensed under GPL v2.0. Generated projects may use a different license.

## 🚄 Quick Start

### Installation

```bash
pip install dhruvkit
```

> **💡 Tip:** You can use `dk` as a shorthand for `dhruvkit` in all commands!

### ⚡ Recommended Flow

```bash
# Create a full-featured app with MongoDB, Firebase, and security in one command
dhruvkit new myapp --template fastapi --mongodb --firebase --secure

# Set up and run
cd myapp
pip install -r requirements.txt
uvicorn src.main:app --reload
```

🎉 **That's it!** You now have a production-ready FastAPI app with MongoDB, Firebase auth, and security middleware.

<details>
<summary><b>Install from source</b></summary>

```bash
git clone https://github.com/dhruvgarg001/dhruvkit.git
cd dhruvkit
pip install -e .
```

</details>

<details>
<summary><b>Optional: Install with runtime dependencies</b></summary>

Optional: Install extras if you want to test templates locally.

```bash
# For testing FastAPI template generation
pip install dhruvkit[fastapi]

# For testing Flask template generation
pip install dhruvkit[flask]

# For testing Firebase integration
pip install dhruvkit[firebase]

# For testing MongoDB integration
pip install dhruvkit[mongodb]

# Install all extras
pip install dhruvkit[fastapi,flask,mongodb,firebase]
```

</details>

### More Examples

```bash
# Basic FastAPI project
dk new myapp --template fastapi

# Flask project with MIT license
dk new myapp -t flask --license mit

# Initialize in current directory
dk init --template basic

# Add a license later
dk add --license apache
```

## 📖 Usage

### Commands

#### `new` - Create a new project

```bash
dhruvkit new <project_name> [--template TEMPLATE] [--license LICENSE] [addons...]
```

**Examples:**
```bash
dhruvkit new blog --template fastapi
dk new api -t fastapi --mongodb --firebase  # Using short aliases
dhruvkit new myapp --template flask --license apache
```

#### `init` - Initialize in current directory

```bash
dhruvkit init [--template TEMPLATE] [--license LICENSE] [addons...]
```

**Examples:**
```bash
dhruvkit init --template fastapi
dhruvkit init --template fastapi --mongodb --secure
```

#### `add` - Add license to existing project

```bash
dhruvkit add --license LICENSE
```

**Examples:**
```bash
dhruvkit add --license mit
dhruvkit add --license apache
```

#### `docs` - View documentation

```bash
dhruvkit docs [command]
```

### Available Templates

| Template | Description | Add-ons Available |
|----------|-------------|-------------------|
| `basic` | Minimal Python project | None |
| `flask` | Flask web application | None |
| `fastapi` | FastAPI application | mongodb, firebase, secure |

### FastAPI Add-ons

#### `--mongodb` - MongoDB Atlas Integration
- Complete database connection management
- Collection utilities and indexing
- Lifespan event handling
- Usage documentation

#### `--firebase` - Firebase Admin SDK
- Firebase authentication support
- Firestore database access
- Real-time database support
- Comprehensive integration guide

#### `--secure` - Security Middleware
- CORS configuration
- Host checking middleware
- Security headers (CSP, X-Frame-Options, X-Content-Type-Options)
- Production-ready security setup

### Mix & Match Add-ons

DhruvKit intelligently combines multiple add-ons:

```bash
# MongoDB + Firebase
dhruvkit new myapp --template fastapi --mongodb --firebase

# All three add-ons together
dhruvkit new myapp --template fastapi --mongodb --firebase --secure
```

The generated code automatically merges:
- ✅ Import statements
- ✅ Configuration files (.env, settings.py)
- ✅ Dependencies (requirements.txt)
- ✅ README documentation
- ✅ Application initialization

### Supported Licenses

- `mit` - MIT License
- `apache` - Apache License 2.0
- `gpl` - GNU General Public License v3.0
- `bsd` - BSD 3-Clause License
- `unlicense` - The Unlicense
- `cc` / `cc0` - Creative Commons Zero v1.0

## 🏗️ Project Structure

A typical FastAPI project with add-ons:

```
myapp/
├── src/
│   ├── database_functions/      # MongoDB utilities (if --mongodb)
│   │   ├── __init__.py
│   │   └── MongoDBConfig.py
│   ├── main.py                  # FastAPI application
│   ├── dbconfig.py              # Database initialization (if --mongodb)
│   └── settings.py              # Configuration
├── docs/                        # Auto-generated documentation
│   ├── mongodb_usage.md
│   ├── firebase_usage.md
│   └── security_guide.md
├── .env                         # Environment variables
├── .gitignore
├── requirements.txt
├── LICENSE                      # If --license specified
└── README.md                    # Project documentation
```

## 🎯 Why DhruvKit?

### Before DhruvKit
```bash
# Manual setup required
mkdir myapp && cd myapp
python -m venv .venv
touch main.py settings.py .env .gitignore
# ... write boilerplate code
# ... set up MongoDB connection
# ... configure Firebase
# ... add security middleware
# ... write documentation
```

### With DhruvKit
```bash
dhruvkit new myapp --template fastapi --mongodb --firebase --secure
cd myapp && pip install -r requirements.txt
uvicorn src.main:app --reload
# 🎉 Ready to code!
```

## 🔧 Development

### Project Structure

```
dhruvkit/
├── src/
│   └── dhruvkit/
│       ├── commands/           # Command implementations
│       │   ├── new.py
│       │   ├── init.py
│       │   ├── add.py
│       │   └── docs.py
│       ├── templates/          # Project templates
│       │   ├── basic.py
│       │   ├── flask.py
│       │   └── fastapi.py
│       ├── license_templates/  # License files
│       ├── cli.py             # CLI entry point
│       ├── licenses.py        # License handler
│       └── utils.py           # Shared utilities
├── tests/
├── pyproject.toml
└── README.md
```

### Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation

## 📝 License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Uses [python-decouple](https://github.com/henriquebastos/python-decouple) for environment management

## 📬 Contact

Created by [Dhruv Garg](https://www.linkedin.com/in/dhruvgarg001/)

---

<p align="center">Made with ❤️ and Python</p>

