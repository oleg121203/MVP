#!/bin/bash
set -e

echo "🚀 Setting up VentAI development environment..."

# Navigate to workspace
cd /workspaces/MVP

# Backend setup (globally in container, no venv)
echo "📦 Installing Python dependencies..."
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
else
    echo "Creating basic requirements.txt..."
    mkdir -p backend
    cat > backend/requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
python-dotenv==1.0.0
sqlalchemy==2.0.23
alembic==1.13.0
pytest==7.4.3
httpx==0.25.2
EOF
    pip install -r backend/requirements.txt
fi

# Create basic FastAPI app if it doesn't exist
if [ ! -f "backend/main.py" ]; then
    echo "Creating basic FastAPI application..."
    cat > backend/main.py << EOF
"""
VentAI FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="VentAI API",
    description="AI-powered event management platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "VentAI API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ventai-api"}

@app.get("/api/events")
async def get_events():
    """Get all events"""
    # Placeholder for events endpoint
    return {
        "events": [
            {
                "id": 1,
                "title": "Sample Event",
                "description": "This is a sample event",
                "date": "2025-06-15T10:00:00Z"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
fi

# Frontend setup
echo "📱 Setting up Next.js frontend..."
if [ ! -d "frontend" ]; then
    echo "Creating Next.js application..."
    npx create-next-app@latest frontend --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*" --no-git
else
    cd frontend
    if [ ! -f "package.json" ]; then
        echo "Initializing Next.js in existing frontend directory..."
        npx create-next-app@latest . --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*" --no-git
    else
        npm install
    fi
    cd ..
fi

# Create environment files
echo "📄 Creating environment files..."

# Backend env
cat > backend/.env << EOF
# Development Environment
DEBUG=true
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000
DATABASE_URL=sqlite:///./ventai.db
SECRET_KEY=dev-secret-key-change-in-production
EOF

# Frontend env
cat > frontend/.env.local << EOF
# Development Environment
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_ENV=development
EOF

# Root package.json for scripts
cat > package.json << EOF
{
  "name": "ventai-mvp",
  "version": "1.0.0",
  "description": "VentAI MVP - AI-powered event management platform",
  "scripts": {
    "dev:backend": "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000",
    "dev:frontend": "cd frontend && npm run dev",
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "test:setup": "python test-setup.py",
    "build:frontend": "cd frontend && npm run build",
    "start:prod": "concurrently \"cd backend && uvicorn main:app --host 0.0.0.0 --port 8000\" \"cd frontend && npm start\""
  },
  "devDependencies": {
    "concurrently": "^8.2.0"
  },
  "keywords": ["ai", "events", "mvp"],
  "author": "VentAI Team",
  "license": "MIT"
}
EOF

npm install

echo "✅ Development environment ready!"
echo ""
echo "Available commands:"
echo "  npm run dev          - Start both backend and frontend"
echo "  npm run dev:backend  - Start only backend"
echo "  npm run dev:frontend - Start only frontend"
echo "  npm run test:setup   - Test environment setup"
echo ""
echo "URLs:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
