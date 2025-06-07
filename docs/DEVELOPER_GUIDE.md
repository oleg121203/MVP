# VentAI Developer Guide

## Table of Contents
1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [API Architecture](#api-architecture)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)

## Development Environment Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- Docker (optional)

### Installation Steps
```bash
# Clone the repository
git clone https://github.com/ventai/ventai-app.git
cd ventai-app

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r backend/requirements.txt
pip install -r backend/requirements-test.txt

# Configure environment
cp backend/.env.example backend/.env
# Edit the .env file with your settings
```

## Project Structure

```
backend/
├── src/                  # Application source code
│   ├── app/              # FastAPI application
│   │   ├── routers/      # API endpoints
│   │   ├── schemas/      # Pydantic models
│   │   └── main.py       # App configuration
├── tests/                # Test suites
├── requirements.txt      # Production dependencies
└── requirements-test.txt # Test dependencies
```

## API Architecture

The backend follows a modular architecture:

1. **Routers**: Handle HTTP requests/responses
2. **Services**: Business logic layer
3. **Models**: Database ORM models
4. **Schemas**: Data validation and serialization

## Testing

Run the test suite:
```bash
cd backend
pytest -v --cov=./ --cov-report=html
```

## Deployment

### Docker
```bash
docker build -t ventai-backend -f backend/Dockerfile .
docker run -p 8000:8000 ventai-backend
```

### Manual Deployment
```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

**Common Issues**
- Database connection errors: Verify `.env` configuration
- Test failures: Run `pytest -x` to stop on first failure
- Dependency issues: Recreate virtual environment
