# Python API Server

This directory contains the Python FastAPI server implementation for the OpenLit project.

## Directory Structure

```
python/
├── app/                    # Application code
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # Database configuration
│   ├── auth.py           # Authentication utilities
│   ├── metrics_utils.py  # Metrics calculation utilities
│   └── vault_utils.py    # Vault operations utilities
├── Dockerfile            # Docker configuration for the API server
└── requirements.txt     # Python dependencies
```

## Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Docker

To run the application using Docker:

```bash
docker-compose -f ../docker-compose-python.yaml up --build
```

The API will be available at `http://localhost:8000`.

## Features

- User authentication with JWT tokens
- User management (create, update profile)
- Database configuration management
- API key management
- SQLite database with SQLAlchemy ORM
- FastAPI for high-performance API endpoints
- Pydantic for request/response validation

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment variables file:
   ```bash
   cp .env.example .env
   ```
5. Edit the `.env` file with your configuration

## Running the Server

1. Make sure your virtual environment is activated
2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   The server will start at http://localhost:8000

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Available Endpoints

### Authentication
- POST /token - Get access token
- POST /users/ - Create new user
- GET /users/me/ - Get current user
- PUT /users/me/ - Update current user

### Database Configurations
- POST /database-configs/ - Create database config
- GET /database-configs/ - List database configs

### API Keys
- POST /api-keys/ - Create API key
- GET /api-keys/ - List API keys

## Development

The project structure is organized as follows:

```
app/
├── __init__.py
├── main.py          # FastAPI application and routes
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic schemas
├── database.py      # Database configuration
├── auth.py          # Authentication utilities
├── .env.example     # Example environment variables
└── README.md        # This file
```

## Security Notes

- Always use HTTPS in production
- Set a strong SECRET_KEY in the .env file
- Update CORS settings in main.py for production
- Never commit the .env file
- Use appropriate database backup strategies 