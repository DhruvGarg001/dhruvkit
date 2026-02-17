"""
Shared utilities for dhruvkit

Common functions used across different commands
"""

from pathlib import Path
from rich.console import Console
from rich.tree import Tree

console = Console()

def apply_addons_to_template(template: dict, addons: list, available_addons: dict) -> dict:
    """
    Apply add-ons to a base template
    
    Args:
        template: Base template dictionary
        addons: List of addon names to apply (e.g., ['mongodb', 'firebase', 'secure'])
        available_addons: Dictionary of available addons for this template
        
    Returns:
        New template dictionary with addons merged in
    """
    # Create a copy of the template
    merged_template = {
        "name": template["name"],
        "description": template["description"],
        "files": template["files"].copy()
    }
    
    # Detect which addons need special combination handling
    has_mongodb = 'mongodb' in addons
    has_firebase = 'firebase' in addons
    has_secure = 'secure' in addons
    
    # If any combination of mongodb/firebase/secure, handle specially
    if has_mongodb or has_firebase or has_secure:
        # Print what we're adding
        if has_mongodb:
            console.print(f"[cyan]+ Adding:[/cyan] MongoDB Atlas Integration")
        if has_firebase:
            console.print(f"[cyan]+ Adding:[/cyan] Firebase Admin SDK Integration")
        if has_secure:
            console.print(f"[cyan]+ Adding:[/cyan] Security Middleware")
        
        # If multiple addons, show combination message
        active_addons = [a for a in ['mongodb', 'firebase', 'secure'] if a in addons]
        if len(active_addons) > 1:
            combo_names = ' + '.join(active_addons)
            console.print(f"[magenta]⚡ Combining:[/magenta] {combo_names} integration")
        
        # Add non-conflicting files from each addon
        for addon_name in ['mongodb', 'firebase', 'secure']:
            if addon_name not in addons:
                continue
            
            addon = available_addons.get(addon_name, {})
            for file_path, content_func in addon.get("files", {}).items():
                # Skip main files that need to be combined
                if file_path not in ['src/main.py', 'src/settings.py', '.env', 'requirements.txt', 'README.md', '.gitignore']:
                    merged_template["files"][file_path] = content_func
        
        # Build combined main.py
        merged_template["files"]["src/main.py"] = create_combined_main(has_mongodb, has_firebase, has_secure)
        
        # Build combined settings.py
        merged_template["files"]["src/settings.py"] = create_combined_settings(has_mongodb, has_firebase, has_secure)
        
        # Build combined .env
        merged_template["files"][".env"] = create_combined_env(has_mongodb, has_firebase, has_secure)
        
        # Build combined requirements.txt
        merged_template["files"]["requirements.txt"] = create_combined_requirements(has_mongodb, has_firebase, has_secure)
        
        # Build combined README.md
        merged_template["files"]["README.md"] = create_combined_readme(has_mongodb, has_firebase, has_secure)
        
        # Build combined .gitignore (only if firebase is included)
        if has_firebase:
            merged_template["files"][".gitignore"] = lambda name: """__pycache__/
.env
.venv/
venv/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.DS_Store

# Firebase service account keys
firebase-service-account.json
*-firebase-adminsdk-*.json
"""
        
        # Remove processed addons from the list
        addons = [a for a in addons if a not in ['mongodb', 'firebase', 'secure']]
    
    # Apply any remaining addons normally
    for addon_name in addons:
        if addon_name not in available_addons:
            console.print(f"[yellow]⚠ Warning:[/yellow] Addon '{addon_name}' not found for this template. Skipping.")
            continue
        
        addon = available_addons[addon_name]
        console.print(f"[cyan]+ Adding:[/cyan] {addon['name']}")
        
        # Merge addon files into template
        for file_path, content_func in addon["files"].items():
            merged_template["files"][file_path] = content_func
    
    return merged_template


def create_combined_main(has_mongodb: bool, has_firebase: bool, has_secure: bool):
    """Create combined main.py based on active addons"""
    def _generate(name: str) -> str:
        # Build imports
        imports = ["from fastapi import FastAPI"]
        if has_secure:
            imports[0] += ", HTTPException, status, Request"
            imports.append("from fastapi.middleware.cors import CORSMiddleware")
        if has_mongodb or has_firebase:
            imports.append("import settings")
        else:
            imports.append("from settings import API_KEY, DEBUG")
        
        if has_mongodb:
            imports.append("from contextlib import asynccontextmanager")
            imports.append("import dbconfig")
        
        code = "\n".join(imports) + "\n\n"
        
        # MongoDB lifespan
        if has_mongodb:
            code += """@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    dbconfig.initialize_database()
    print("✓ Database connected successfully")
"""
            if has_firebase:
                code += """    print("✓ Firebase initialized successfully")
"""
            code += """
    yield  # The app runs here
    
    # Shutdown code
    dbconfig.close_database()
    print("✓ Database disconnected successfully")


"""
        
        # App initialization
        debug_source = "settings.DEBUG" if (has_mongodb or has_firebase) else "DEBUG"
        description = []
        if has_mongodb:
            description.append("MongoDB")
        if has_firebase:
            description.append("Firebase")
        if has_secure:
            description.append("security middleware")
        
        desc_text = " and ".join(description) if description else "dhruvkit"
        
        code += f"""app = FastAPI(
    title='{name}',
    description='FastAPI application with {desc_text}',
    version='0.1.0',
    docs_url="/docs" if {debug_source} else None,
    redoc_url="/redoc" if {debug_source} else None,
    openapi_url="/openapi.json" if {debug_source} else None,
"""
        if has_mongodb:
            code += "    lifespan=lifespan\n"
        code += ")\n\n"
        
        # Firebase initialization (after app creation)
        if has_firebase:
            code += """# Firebase
import firebase_admin
from firebase_admin import credentials

FIREBASE_SERVICE_ACCOUNT_KEY_PATH = settings.FIREBASE_SERVICE_ACCOUNT_KEY_PATH

cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
firebase_admin.initialize_app(cred)

"""
        
        # Security middleware
        if has_secure:
            code += """# CORS Middleware
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "127.0.0.1:8000",
    "localhost"
]

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1:8000",
]


@app.middleware("http")
async def check_allowed_hosts(request: Request, call_next):
    host = request.headers.get("host", "")
    if not any(allowed_host in host for allowed_host in ALLOWED_HOSTS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": f"Host {host} is not allowed", "success": False}
        )
    response = await call_next(request)

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Security settings

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc"):
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data:;"
            )
    else:
        response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response


"""
        
        # API endpoints
        message_parts = []
        if has_mongodb:
            message_parts.append("MongoDB")
        if has_firebase:
            message_parts.append("Firebase")
        if has_secure:
            message_parts.append("security")
        
        message = " and ".join(message_parts) if message_parts else "FastAPI"
        
        code += f"""@app.get('/')
async def root():
    return {{'message': 'Hello from FastAPI with {message}!'}}

@app.get('/dhruvkit')
async def dhruvkit():
    return {{'message': 'I love DhruvKit!'}}

@app.get('/health')
async def health():
    return {{'status': 'healthy'"""
        
        if has_mongodb:
            code += """, 'database': 'connected'"""
        if has_firebase:
            code += """, 'firebase': 'connected'"""
        
        code += """}
"""
        
        # MongoDB endpoint
        if has_mongodb:
            code += """
# Example endpoint using MongoDB
@app.get('/db-info')
async def db_info():
    \"\"\"Get database information\"\"\"
    return {
        'database_name': dbconfig.database.dbName,
        'connected': dbconfig.database.client is not None
    }
"""
        
        return code
    
    return _generate


def create_combined_settings(has_mongodb: bool, has_firebase: bool, has_secure: bool):
    """Create combined settings.py based on active addons"""
    def _generate(name: str) -> str:
        code = """from decouple import config

# API Configuration
API_KEY = config('API_KEY', default='')
DEBUG = config('DEBUG', default=False, cast=bool)
"""
        
        if has_mongodb:
            code += """
# MongoDB Configuration
MONGODB_URI = config('MONGODB_URI', cast=str)
MONGODB_DB_NAME = config('MONGODB_DB_NAME', cast=str)
"""
        
        if has_firebase:
            code += """
# Firebase Configuration
FIREBASE_SERVICE_ACCOUNT_KEY_PATH = config('FIREBASE_SERVICE_ACCOUNT_KEY_PATH', cast=str)
"""
        
        return code
    
    return _generate


def create_combined_env(has_mongodb: bool, has_firebase: bool, has_secure: bool):
    """Create combined .env based on active addons"""
    def _generate(name: str) -> str:
        code = """# API Configuration
API_KEY=your_api_key_here
DEBUG=True
"""
        
        if has_mongodb:
            code += f"""
# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME={name.lower()}_db
"""
        
        if has_firebase:
            code += """
# Firebase Configuration
# Path to your Firebase service account key JSON file
# Can be a file path: ./firebase-service-account.json
# Or the JSON content as a string
FIREBASE_SERVICE_ACCOUNT_KEY_PATH=./firebase-service-account.json
"""
        
        return code
    
    return _generate


def create_combined_requirements(has_mongodb: bool, has_firebase: bool, has_secure: bool):
    """Create combined requirements.txt based on active addons"""
    def _generate(name: str) -> str:
        code = """fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-decouple>=3.8
"""
        
        if has_mongodb:
            code += """pymongo>=4.13.2
"""
        
        if has_firebase:
            code += """firebase-admin>=6.4.0
"""
        
        return code
    
    return _generate


def create_combined_readme(has_mongodb: bool, has_firebase: bool, has_secure: bool):
    """Create combined README.md based on active addons"""
    def _generate(name: str) -> str:
        # Build feature list
        features = []
        if has_mongodb:
            features.append("MongoDB Atlas")
        if has_firebase:
            features.append("Firebase Admin SDK")
        if has_secure:
            features.append("security middleware")
        
        features_text = ", ".join(features[:-1]) + " and " + features[-1] if len(features) > 1 else features[0] if features else "dhruvkit"
        
        code = f"""# {name}

FastAPI application with {features_text}, created with dhruvkit.

## Getting Started

"""
        
        # Setup instructions
        if has_mongodb or has_firebase:
            if has_mongodb:
                code += """1. Set up MongoDB Atlas:
   - Create a MongoDB Atlas account
   - Get your connection string

"""
            if has_firebase:
                num = "1" if not has_mongodb else "2"
                code += f"""{num}. Set up Firebase:
   - Get your Firebase service account key from [Firebase Console](https://console.firebase.google.com/)
   - Place the JSON file in your project root as `firebase-service-account.json`

"""
            num = "3" if (has_mongodb and has_firebase) else "2"
            code += f"""{num}. Install dependencies and run:

```bash
"""
        else:
            code += """```bash
"""
        
        code += f"""python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Project Structure

```
{name}/
├── src/
"""
        
        if has_mongodb:
            code += """│   ├── database_functions/   # MongoDB connection utilities
│   │   ├── __init__.py
│   │   └── MongoDBConfig.py
"""
        
        code += """│   ├── main.py       # FastAPI application"""
        if has_mongodb or has_firebase or has_secure:
            descriptors = []
            if has_mongodb and has_firebase:
                descriptors.append("with MongoDB and Firebase")
            elif has_mongodb:
                descriptors.append("with MongoDB integration")
            elif has_firebase:
                descriptors.append("with Firebase integration")
            if has_secure:
                descriptors.append("security middleware")
            code += " " + ", ".join(descriptors)
        code += "\n"
        
        if has_mongodb:
            code += """│   ├── dbconfig.py   # Database initialization
"""
        
        code += """│   └── settings.py   # Configuration
"""
        
        if has_mongodb or has_firebase or has_secure:
            code += """├── docs/
"""
            if has_mongodb:
                code += """│   ├── mongodb_usage.md     # MongoDB usage guide
"""
            if has_firebase:
                code += """│   ├── firebase_usage.md    # Firebase usage guide
"""
            if has_secure:
                code += """│   └── security_guide.md    # Security configuration guide
"""
        
        code += """├── .env              # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Features

- FastAPI framework with async support
"""
        
        if has_mongodb:
            code += """- MongoDB Atlas integration with connection management
- Database lifecycle management (startup/shutdown)
- Collection index management
"""
        
        if has_firebase:
            code += """- Firebase Admin SDK integration
"""
        
        if has_secure:
            code += """- CORS middleware with configurable origins
- Host checking middleware
- Security headers (CSP, X-Frame-Options, X-Content-Type-Options)
"""
        
        code += """- Auto-generated interactive API docs at `/docs`
- Environment variable configuration
"""
        
        # Documentation section
        if has_mongodb or has_firebase or has_secure:
            code += """
## Documentation

"""
            if has_mongodb:
                code += """- See [docs/mongodb_usage.md](docs/mongodb_usage.md) for MongoDB integration guide
"""
            if has_firebase:
                code += """- See [docs/firebase_usage.md](docs/firebase_usage.md) for Firebase integration guide
"""
            if has_secure:
                code += """- See [docs/security_guide.md](docs/security_guide.md) for security configuration and best practices
"""
        
        code += """
## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
"""
        
        return code
    
    return _generate


def create_project_structure(root: Path, project_name: str, template: dict, license_name: str = None):
    """
    Create project structure from template
    
    Args:
        root: Root directory for the project
        project_name: Name of the project
        template: Template dictionary with file definitions
        license_name: Optional license name (e.g., 'mit', 'apache', 'gpl')
        
    Returns:
        List of created file paths (sorted)
    """
    created_items = []
    
    for file_path, content_func in template["files"].items():
        full_path = root / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content_func(project_name), encoding='utf-8')
        created_items.append(file_path)
    
    # Add LICENSE file if license_name is provided
    if license_name:
        from dhruvkit.licenses import get_license
        license_path = root / "LICENSE"
        license_content = get_license(license_name, project_name)
        license_path.write_text(license_content, encoding='utf-8')
        created_items.append("LICENSE")
    
    return sorted(created_items)

def display_created_files(project_name: str, items: list, is_new: bool = True):
    """
    Display beautiful output of created files using rich tree
    
    Args:
        project_name: Name of the project
        items: List of created file paths
        is_new: Whether this is a new project (in new folder) or init (current dir)
    """
    tree = Tree(
        f"[bold blue]📁 {project_name}[/bold blue]" if is_new else "[bold blue]📁 . (current directory)[/bold blue]",
        guide_style="bright_blue"
    )
    
    # Group files by directory
    dirs = {}
    root_files = []
    
    for item in items:
        if "/" in item:
            parts = item.split("/")
            dir_name = parts[0]
            file_name = parts[1]
            if dir_name not in dirs:
                dirs[dir_name] = []
            dirs[dir_name].append(file_name)
        else:
            root_files.append(item)
    
    # Add root files
    for file in root_files:
        tree.add(f"[green]📄 {file}[/green]")
    
    # Add directories and their files
    for dir_name, files in sorted(dirs.items()):
        dir_branch = tree.add(f"[blue]📁 {dir_name}/[/blue]")
        for file in sorted(files):
            dir_branch.add(f"[green]📄 {file}[/green]")
    
    console.print()
    console.print(tree)
    console.print()
