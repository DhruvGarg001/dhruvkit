"""
FastAPI Application Template

Basic FastAPI application with modern async structure

Add-ons:
- --mongodb: Add MongoDB Atlas integration
- --firebase: Add Firebase Admin SDK integration
- --secure: Add CORS middleware and security headers
"""

TEMPLATE = {
    "name": "FastAPI Application",
    "description": "FastAPI application with modern async structure",
    "files": {
        "README.md": lambda name: f"""# {name}

FastAPI application created with dhruvkit.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Project Structure

```
{name}/
├── src/
│   ├── main.py       # FastAPI application
│   └── settings.py   # Configuration
├── .env              # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Features

- FastAPI framework with async support
- Auto-generated interactive API docs at `/docs`
- Pydantic for data validation
- Environment variable configuration
""",
        ".env": lambda name: """API_KEY=your_api_key_here
DEBUG=True
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
.DS_Store
""",
        "requirements.txt": lambda name: """fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-decouple>=3.8
""",
        "src/main.py": lambda name: f"""from fastapi import FastAPI
from settings import API_KEY, DEBUG

app = FastAPI(
    title='{name}',
    description='FastAPI application created with dhruvkit',
    version='0.1.0',
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None,
)

@app.get('/')
async def root():
    return {{'message': 'Hello from FastAPI!'}}

@app.get('/dhruvkit')
async def dhruvkit():
    return {{'message': 'I love DhruvKit!'}}

@app.get('/health')
async def health():
    return {{'status': 'healthy'}}
""",
        "src/settings.py": lambda name: """from decouple import config

API_KEY = config('API_KEY', default='')
DEBUG = config('DEBUG', default=False, cast=bool)
"""
    }
}

# Add-ons that can be applied to the base template
ADDONS = {
    "mongodb": {
        "name": "MongoDB Atlas Integration",
        "description": "Add MongoDB Atlas database support with connection management",
        "files": {
            "src/database_functions/__init__.py": lambda name: """from .MongoDBConfig import MongoDBConfig

__all__ = ['MongoDBConfig']
""",
            "src/database_functions/MongoDBConfig.py": lambda name: """from fastapi import HTTPException, status

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class MongoDBConfig:
    def __init__(self, dbName: str, dbURI: str):
        self.client = None
        self.db = None
        self.dbName = dbName
        self.dbURI = dbURI

    def connect(self):
        \"\"\"
        Connect to the MongoDB database using the provided URI and database name.

        Returns:
            MongoClient: The MongoDB client connected to the specified database.
        \"\"\"
        try:
            # Create a MongoDB client with the provided URI
            self.client = MongoClient(self.dbURI, server_api=ServerApi('1'))
        
            # Access the database
            self.db = self.client[self.dbName]

            self.client.admin.command('ping')  # Test the connection
            return self.client
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": f"Database connection failed: {str(e)}", "success": False}
            )
    
    def disconnect(self):
        \"\"\"
        Disconnect from the MongoDB database.

        Returns:
            str: A message indicating successful disconnection.
        \"\"\"
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            return "Disconnected from MongoDB successfully."
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "No active database connection to disconnect.", "success": False}
            )
        
    def get_collection(self, collection_name: str):
        \"\"\"
        Get a collection from the connected database.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The MongoDB collection object.
        \"\"\"

        if self.db is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Database connection not established.", "success": False}
            )
        
        return self.db[collection_name]
    
    def create_collection_index_unique(self, collection_name: str, index: str, unique: bool = True):
        \"\"\"
        Create a unique index on a specified collection.

        Args:
            collection_name (str): The name of the collection.
            index (str): The field name to index.
            unique (bool): Whether the index should be unique.

        Returns:
            The collection object with the index created.
        \"\"\"
        if self.db is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Database connection not established.", "success": False}
            )
        
        self.db[collection_name].create_index(index, unique=unique)

        return self.db[collection_name]
""",
            "src/dbconfig.py": lambda name: f"""from database_functions import MongoDBConfig
import settings

# MongoDB Configuration
database = MongoDBConfig(settings.MONGODB_DB_NAME, settings.MONGODB_URI)

def initialize_database():
    \"\"\"
    Initialize the MongoDB database connection.
    \"\"\"
    database.connect()

    # Create collections and indexes
    # Example: Create a unique index on 'users' collection for 'user_id' field
    database.create_collection_index_unique("users", "user_id", unique=True)
    
    # Add more collection indexes as needed:
    # database.create_collection_index_unique("posts", "post_id", unique=True)
    # database.create_collection_index_unique("comments", "comment_id", unique=True)

def close_database():
    \"\"\"
    Close the MongoDB database connection.
    \"\"\"
    database.disconnect()
""",
            "src/main.py": lambda name: f"""from fastapi import FastAPI
from contextlib import asynccontextmanager
import dbconfig
from settings import API_KEY, DEBUG

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    dbconfig.initialize_database()
    print("✓ Database connected successfully")

    yield  # The app runs here
    
    # Shutdown code
    dbconfig.close_database()
    print("✓ Database disconnected successfully")


app = FastAPI(
    title='{name}',
    description='FastAPI application with MongoDB Atlas integration',
    version='0.1.0',
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None,
    lifespan=lifespan
)

@app.get('/')
async def root():
    return {{'message': 'Hello from FastAPI with MongoDB!'}}

@app.get('/dhruvkit')
async def dhruvkit():
    return {{'message': 'I love DhruvKit!'}}

@app.get('/health')
async def health():
    return {{'status': 'healthy', 'database': 'connected'}}

# Example endpoint using MongoDB
@app.get('/db-info')
async def db_info():
    \"\"\"Get database information\"\"\"
    return {{
        'database_name': dbconfig.database.dbName,
        'connected': dbconfig.database.client is not None
    }}
""",
            "src/settings.py": lambda name: """from decouple import config

# API Configuration
API_KEY = config('API_KEY', default='')
DEBUG = config('DEBUG', default=False, cast=bool)

# MongoDB Configuration
MONGODB_URI = config('MONGODB_URI', cast=str)
MONGODB_DB_NAME = config('MONGODB_DB_NAME', cast=str)
""",
            ".env": lambda name: f"""# API Configuration
API_KEY=your_api_key_here
DEBUG=True

# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME={name.lower()}_db
""",
            "requirements.txt": lambda name: """fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-decouple>=3.8
pymongo>=4.13.2
""",
            "README.md": lambda name: f"""# {name}

FastAPI application with MongoDB Atlas integration, created with dhruvkit.

## Getting Started

1. Set up your environment variables in `.env`:
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `MONGODB_DB_NAME`: Your database name

2. Install dependencies and run:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Project Structure

```
{name}/
├── src/
│   ├── database_functions/   # MongoDB connection utilities
│   │   ├── __init__.py
│   │   └── MongoDBConfig.py
│   ├── main.py              # FastAPI application with lifespan
│   ├── dbconfig.py          # Database initialization
│   └── settings.py          # Configuration
├── docs/
│   └── mongodb_usage.md     # MongoDB usage guide
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Features

- FastAPI framework with async support
- MongoDB Atlas integration with connection management
- Database lifecycle management (startup/shutdown)
- Auto-generated interactive API docs at `/docs`
- Collection index management
- Environment variable configuration
- Comprehensive MongoDB usage documentation

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## MongoDB Documentation

See [docs/mongodb_usage.md](docs/mongodb_usage.md) for detailed MongoDB integration guide, including:
- Accessing collections in endpoints
- Common CRUD operations
- Adding new collections with indexes
- Error handling
- Best practices
""",
            "docs/mongodb_usage.md": lambda name: f"""# MongoDB Usage Guide for {name}

This guide explains how to use MongoDB in your FastAPI application.

## Database Configuration

The database is configured in `src/dbconfig.py`. The main components are:

1. **MongoDBConfig**: A class that manages MongoDB connections
2. **database**: A global instance of MongoDBConfig
3. **initialize_database()**: Called on app startup to connect and set up indexes
4. **close_database()**: Called on app shutdown to disconnect

## Accessing Collections

### In Your Endpoints

To access MongoDB collections in your FastAPI endpoints:

```python
from fastapi import APIRouter
import dbconfig

router = APIRouter()

@router.get('/users')
async def get_users():
    # Get the users collection
    users_collection = dbconfig.database.get_collection("users")
    
    # Query the collection
    users = list(users_collection.find({{}}, {{'_id': 0}}))
    
    return {{'users': users}}

@router.post('/users')
async def create_user(user_id: str, name: str):
    users_collection = dbconfig.database.get_collection("users")
    
    # Insert a document
    result = users_collection.insert_one({{
        'user_id': user_id,
        'name': name
    }})
    
    return {{'message': 'User created', 'id': str(result.inserted_id)}}
```

## Common Operations

### Insert Documents

```python
collection = dbconfig.database.get_collection("collection_name")

# Insert one
collection.insert_one({{'field': 'value'}})

# Insert many
collection.insert_many([
    {{'field': 'value1'}},
    {{'field': 'value2'}}
])
```

### Query Documents

```python
collection = dbconfig.database.get_collection("collection_name")

# Find one
doc = collection.find_one({{'field': 'value'}})

# Find many
docs = list(collection.find({{'field': 'value'}}))

# Find with projection (exclude _id)
docs = list(collection.find({{}}, {{'_id': 0}}))
```

### Update Documents

```python
collection = dbconfig.database.get_collection("collection_name")

# Update one
collection.update_one(
    {{'field': 'value'}},  # filter
    {{'$set': {{'new_field': 'new_value'}}}}  # update
)

# Update many
collection.update_many(
    {{'status': 'active'}},
    {{'$set': {{'updated': True}}}}
)
```

### Delete Documents

```python
collection = dbconfig.database.get_collection("collection_name")

# Delete one
collection.delete_one({{'field': 'value'}})

# Delete many
collection.delete_many({{'status': 'inactive'}})
```

## Adding New Collections

To add a new collection with indexes:

1. Open `src/dbconfig.py`
2. Add index creation in `initialize_database()`:

```python
def initialize_database():
    database.connect()
    
    # Existing indexes
    database.create_collection_index_unique("users", "user_id", unique=True)
    
    # Add your new collection index
    database.create_collection_index_unique("posts", "post_id", unique=True)
    database.create_collection_index_unique("comments", "comment_id", unique=False)
```

## Error Handling

The MongoDBConfig class raises HTTPException for database errors:

```python
from fastapi import HTTPException

try:
    collection = dbconfig.database.get_collection("users")
    users = list(collection.find({{}}))
except HTTPException as e:
    # Handle the error
    print(f"Database error: {{e.detail}}")
```

## Environment Variables

Configure your MongoDB connection in `.env`:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME={name.lower()}_db
```

## Best Practices

1. **Always use indexes**: Create indexes for fields you frequently query
2. **Use projections**: Exclude `_id` or unnecessary fields to reduce data transfer
3. **Handle errors**: Always handle potential database errors
4. **Close connections**: The lifespan manager handles this automatically
5. **Use connection pooling**: PyMongo handles this by default

## Testing Database Connection

Run your app and visit:
- http://localhost:8000/db-info - Check database connection status
- http://localhost:8000/docs - Interactive API documentation

## Additional Resources

- [MongoDB Python Driver Documentation](https://pymongo.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
"""
        }
    },
    "firebase": {
        "name": "Firebase Admin SDK Integration",
        "description": "Add Firebase Admin SDK support for authentication and services",
        "files": {
            "README.md": lambda name: f"""# {name}

FastAPI application with Firebase Admin SDK integration, created with dhruvkit.

## Getting Started

1. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set up Firebase:
   - Get your Firebase service account key from [Firebase Console](https://console.firebase.google.com/)
   - Place the JSON file in your project root as `firebase-service-account.json`
   - Or set the JSON content in `.env` as `FIREBASE_SERVICE_ACCOUNT_KEY_PATH`

3. Run the application:

```bash
uvicorn src.main:app --reload
```

## Project Structure

```
{name}/
├── src/
│   ├── main.py       # FastAPI application with Firebase
│   └── settings.py   # Configuration
├── docs/
│   └── firebase_usage.md  # Firebase usage guide
├── .env              # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Features

- FastAPI framework with async support
- Firebase Admin SDK integration
- Auto-generated interactive API docs at `/docs`
- Environment variable configuration
- Comprehensive Firebase usage documentation

## Firebase Services Available

- **Authentication**: User management and token verification
- **Firestore**: NoSQL document database
- **Realtime Database**: Real-time data synchronization
- **Cloud Storage**: File storage and retrieval
- **Cloud Messaging**: Push notifications

## Documentation

See [docs/firebase_usage.md](docs/firebase_usage.md) for detailed Firebase integration guide.

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
""",
            "src/main.py": lambda name: f"""from fastapi import FastAPI
import settings

app = FastAPI(
    title='{name}',
    description='FastAPI application with Firebase integration',
    version='0.1.0',
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)

# Firebase
import firebase_admin
from firebase_admin import credentials

FIREBASE_SERVICE_ACCOUNT_KEY_PATH = settings.FIREBASE_SERVICE_ACCOUNT_KEY_PATH

cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
firebase_admin.initialize_app(cred)

@app.get('/')
async def root():
    return {{'message': 'Hello from FastAPI with Firebase!'}}

@app.get('/dhruvkit')
async def dhruvkit():
    return {{'message': 'I love DhruvKit!'}}

@app.get('/health')
async def health():
    return {{'status': 'healthy', 'firebase': 'connected'}}
""",
            "src/settings.py": lambda name: """from decouple import config

# API Configuration
API_KEY = config('API_KEY', default='')
DEBUG = config('DEBUG', default=False, cast=bool)

# Firebase Configuration
FIREBASE_SERVICE_ACCOUNT_KEY_PATH = config('FIREBASE_SERVICE_ACCOUNT_KEY_PATH', cast=str)
""",
            ".env": lambda name: """# API Configuration
API_KEY=your_api_key_here
DEBUG=True

# Firebase Configuration
# Path to your Firebase service account key JSON file
# Can be a file path: ./firebase-service-account.json
# Or the JSON content as a string
FIREBASE_SERVICE_ACCOUNT_KEY_PATH=./firebase-service-account.json
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
.DS_Store

# Firebase service account keys
firebase-service-account.json
*-firebase-adminsdk-*.json
""",
            "requirements.txt": lambda name: """fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-decouple>=3.8
firebase-admin>=6.4.0
""",
            "docs/firebase_usage.md": lambda name: f"""# Firebase Usage Guide for {name}

This guide explains how to use Firebase Admin SDK in your FastAPI application.

## Firebase Configuration

The Firebase Admin SDK is initialized in `src/main.py` using a service account key.

### Getting Your Service Account Key

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to Project Settings (gear icon) → Service Accounts
4. Click "Generate New Private Key"
5. Save the JSON file securely

### Configuration Options

You can configure Firebase in two ways:

#### Option 1: File Path (Recommended)

1. Place your `firebase-service-account.json` in your project root
2. Update `.env`:

```env
FIREBASE_SERVICE_ACCOUNT_KEY_PATH=./firebase-service-account.json
```

#### Option 2: JSON Content

You can also pass the JSON content directly (useful for deployment):

```env
FIREBASE_SERVICE_ACCOUNT_KEY_PATH={{"type": "service_account", "project_id": "your-project",...}}
```

**Important**: Add `firebase-service-account.json` to your `.gitignore` to avoid committing secrets!

## Using Firebase Services

The Firebase Admin SDK provides access to various Firebase services:

### Firebase Authentication

```python
from firebase_admin import auth
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/users/{{user_id}}')
async def get_user(user_id: str):
    try:
        user = auth.get_user(user_id)
        return {{
            'uid': user.uid,
            'email': user.email,
            'display_name': user.display_name
        }}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post('/users')
async def create_user(email: str, password: str):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {{'uid': user.uid, 'email': user.email}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Firebase Firestore

```python
from firebase_admin import firestore
from fastapi import APIRouter

router = APIRouter()
db = firestore.client()

@router.get('/items')
async def get_items():
    items_ref = db.collection('items')
    docs = items_ref.stream()
    
    items = []
    for doc in docs:
        item = doc.to_dict()
        item['id'] = doc.id
        items.append(item)
    
    return {{'items': items}}

@router.post('/items')
async def create_item(name: str, description: str):
    doc_ref = db.collection('items').document()
    doc_ref.set({{
        'name': name,
        'description': description
    }})
    
    return {{'id': doc_ref.id, 'name': name}}
```

### Firebase Realtime Database

```python
from firebase_admin import db
from fastapi import APIRouter

router = APIRouter()

# Initialize with database URL in main.py:
# firebase_admin.initialize_app(cred, {{
#     'databaseURL': 'https://your-project.firebaseio.com'
# }})

@router.get('/data/{{path}}')
async def get_data(path: str):
    ref = db.reference(path)
    return ref.get()

@router.post('/data/{{path}}')
async def set_data(path: str, data: dict):
    ref = db.reference(path)
    ref.set(data)
    return {{'success': True}}
```

### Verify ID Tokens (Authentication Middleware)

```python
from firebase_admin import auth
from fastapi import Header, HTTPException

async def verify_firebase_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Missing or invalid authorization header')
    
    token = authorization.split('Bearer ')[1]
    
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token')

# Use in endpoints:
@app.get('/protected')
async def protected_route(user = Depends(verify_firebase_token)):
    return {{'message': f'Hello {{user["email"]}}'}}
```

## Common Use Cases

### User Registration and Login Flow

1. Client registers/logs in using Firebase Authentication (client-side)
2. Client receives an ID token
3. Client sends token in Authorization header: `Bearer <token>`
4. Server verifies token using `auth.verify_id_token()`
5. Server performs authorized actions

### Custom Claims

```python
from firebase_admin import auth

# Set custom claims (e.g., admin role)
auth.set_custom_user_claims(uid, {{'admin': True}})

# Verify claims in token
decoded_token = auth.verify_id_token(token)
if decoded_token.get('admin'):
    # User is admin
    pass
```

## Error Handling

```python
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

try:
    user = auth.get_user(uid)
except auth.UserNotFoundError:
    # User doesn't exist
    pass
except FirebaseError as e:
    # Handle Firebase errors
    print(f"Firebase error: {{e}}")
```

## Security Best Practices

1. **Never commit service account keys**: Add `*.json` to `.gitignore`
2. **Use environment variables**: Store sensitive config in `.env`
3. **Verify tokens**: Always verify ID tokens on the server side
4. **Use custom claims**: Implement role-based access control
5. **Rotate keys**: Regularly rotate service account keys
6. **Limit permissions**: Use service accounts with minimal required permissions

## Environment Variables for Production

For deployment (e.g., Docker, Cloud):

```env
# Use environment variable with JSON content
FIREBASE_SERVICE_ACCOUNT_KEY_PATH={{"type":"service_account","project_id":"...",...}}
```

Or use platform-specific secrets management:
- **Heroku**: Use Config Vars
- **AWS**: Use Secrets Manager or Parameter Store
- **Google Cloud**: Use Secret Manager
- **Docker**: Use secrets or environment files

## Testing

For testing, you can use Firebase Emulator Suite:

```bash
npm install -g firebase-tools
firebase emulators:start --only auth,firestore
```

Update your code to use emulators:

```python
import os

if os.getenv('FIREBASE_EMULATOR'):
    os.environ['FIREBASE_AUTH_EMULATOR_HOST'] = 'localhost:9099'
    os.environ['FIRESTORE_EMULATOR_HOST'] = 'localhost:8080'
```

## Additional Resources

- [Firebase Admin Python SDK Documentation](https://firebase.google.com/docs/admin/setup)
- [Firebase Authentication](https://firebase.google.com/docs/auth)
- [Cloud Firestore](https://firebase.google.com/docs/firestore)
- [Realtime Database](https://firebase.google.com/docs/database)
"""
        }
    },
    "secure": {
        "name": "Security Middleware",
        "description": "Add CORS middleware, host checking, and security headers",
        "files": {
            "src/main.py": lambda name: f"""from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from settings import API_KEY, DEBUG

app = FastAPI(
    title='{name}',
    description='FastAPI application with security middleware',
    version='0.1.0',
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None,
)

# CORS Middleware
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
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
            detail={{"error": f"Host {{host}} is not allowed", "success": False}}
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


@app.get('/')
async def root():
    return {{'message': 'Hello from FastAPI with security!'}}

@app.get('/dhruvkit')
async def dhruvkit():
    return {{'message': 'I love DhruvKit!'}}

@app.get('/health')
async def health():
    return {{'status': 'healthy'}}
""",
            "README.md": lambda name: f"""# {name}

FastAPI application with security middleware (CORS, host checking, security headers), created with dhruvkit.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Project Structure

```
{name}/
├── src/
│   ├── main.py       # FastAPI application with security middleware
│   └── settings.py   # Configuration
├── docs/
│   └── security_guide.md  # Security configuration guide
├── .env              # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Security Features

- **CORS Middleware**: Configurable allowed origins for cross-origin requests
- **Host Checking**: Validates incoming request hosts against allowed list
- **Security Headers**: 
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Content-Security-Policy` with special handling for API docs

## Configuration

### Allowed Origins (CORS)

Edit `CORS_ALLOWED_ORIGINS` in `src/main.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    # Add your frontend origins here
]
```

### Allowed Hosts

Edit `ALLOWED_HOSTS` in `src/main.py`:

```python
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1:8000",
    # Add your production domains here
]
```

## Documentation

See [docs/security_guide.md](docs/security_guide.md) for detailed security configuration and best practices.

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Note**: Security headers are automatically relaxed for `/docs` and `/redoc` endpoints to ensure proper rendering.
""",
            "docs/security_guide.md": lambda name: f"""# Security Guide for {name}

This guide explains the security features implemented in your FastAPI application.

## Security Features Overview

### 1. CORS (Cross-Origin Resource Sharing)

CORS middleware controls which origins can make requests to your API.

#### Configuration

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "127.0.0.1:8000",
    "localhost"
]
```

#### Settings

- `allow_credentials=True`: Allows cookies and authorization headers
- `allow_methods=["*"]`: Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
- `allow_headers=["*"]`: Allows all headers

#### Production Best Practices

For production, be specific with allowed origins:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
    "https://app.yourdomain.com",
]
```

### 2. Host Checking Middleware

Validates that incoming requests are from allowed hosts, preventing host header injection attacks.

#### Configuration

```python
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1:8000",
]
```

#### How It Works

- Checks the `Host` header of every incoming request
- Returns 403 Forbidden if host is not in the allowed list
- Partial matching: "localhost" matches "localhost:8000"

#### Production Configuration

```python
ALLOWED_HOSTS = [
    "yourdomain.com",
    "www.yourdomain.com",
    "api.yourdomain.com",
]
```

### 3. Security Headers

Adds security headers to all responses to protect against common web vulnerabilities.

#### Headers Added

**X-Content-Type-Options: nosniff**
- Prevents MIME type sniffing
- Forces browsers to respect declared content types

**X-Frame-Options: DENY**
- Prevents clickjacking attacks
- Stops your site from being embedded in iframes

**Content-Security-Policy**
- Controls resources the browser can load
- Two modes:
  - Strict for API endpoints: `default-src 'self'`
  - Relaxed for docs: Allows CDN resources for Swagger UI/ReDoc

#### Custom CSP for API Docs

```python
if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc"):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data:;"
    )
```

This ensures API documentation renders properly while maintaining security elsewhere.

## Testing Security Features

### Test CORS

```bash
# From another domain, should succeed if origin is allowed
curl -X GET http://localhost:8000/ \\
  -H "Origin: http://localhost:3000" \\
  -v
```

Look for `Access-Control-Allow-Origin` in response headers.

### Test Host Checking

```bash
# Should succeed (localhost is allowed)
curl -X GET http://localhost:8000/ \\
  -H "Host: localhost:8000"

# Should return 403 (malicious.com not allowed)
curl -X GET http://localhost:8000/ \\
  -H "Host: malicious.com"
```

### Test Security Headers

```bash
curl -X GET http://localhost:8000/ -v
```

Check response headers for:
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Content-Security-Policy`

## Common Issues

### CORS Errors in Browser

**Symptom**: Console errors like "blocked by CORS policy"

**Solution**: 
1. Check that your frontend origin is in `CORS_ALLOWED_ORIGINS`
2. Include the protocol: `http://localhost:3000` not `localhost:3000`
3. Match exactly: `http://localhost:3000` ≠ `http://localhost:3000/`

### 403 Forbidden on Valid Requests

**Symptom**: All requests return 403

**Solution**:
1. Add your host to `ALLOWED_HOSTS`
2. Check the `Host` header your client is sending
3. Remember port numbers: `localhost:8000` vs `localhost`

### API Docs Not Loading

**Symptom**: Swagger UI/ReDoc shows blank page or errors

**Solution**:
- The CSP should already be relaxed for `/docs` and `/redoc`
- Check browser console for CSP violations
- Adjust CSP if using custom docs paths

## Production Deployment

### Environment-Based Configuration

```python
import os

if os.getenv('ENVIRONMENT') == 'production':
    CORS_ALLOWED_ORIGINS = [
        "https://yourdomain.com",
    ]
    ALLOWED_HOSTS = [
        "yourdomain.com",
        "api.yourdomain.com",
    ]
else:
    # Development settings
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
    ]
    ALLOWED_HOSTS = [
        "localhost",
    ]
```

### Additional Production Recommendations

1. **HTTPS Only**: Use HTTPS in production
2. **Rate Limiting**: Add rate limiting middleware
3. **Authentication**: Implement proper authentication (JWT, OAuth)
4. **API Keys**: Secure sensitive endpoints
5. **Logging**: Log security-related events

## Additional Security Middleware

### Rate Limiting (Optional)

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/endpoint")
@limiter.limit("5/minute")
async def rate_limited_endpoint():
    return {{"message": "This endpoint is rate limited"}}
```

### HTTPS Redirect (Production)

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if os.getenv('ENVIRONMENT') == 'production':
    app.add_middleware(HTTPSRedirectMiddleware)
```

## Resources

- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [CORS MDN Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
"""
        }
    }
}
