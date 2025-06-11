#!/bin/bash
set -e

echo "🚀 Setting up VentAI development environment..."

# Update system packages
sudo apt-get update && sudo apt-get install -y \
    build-essential \
    curl \
    git \
    postgresql-client \
    redis-tools \
    sqlite3 \
    vim \
    wget

# Navigate to workspace
cd /workspaces/ventai-app

# Set proper permissions
chmod +x start-enterprise-services.sh
chmod +x start-windsurf-integration.sh
chmod +x run_tests.sh

# Create data directory for PostgreSQL if it doesn't exist
mkdir -p .devcontainer/data

echo "📦 Installing Python dependencies..."

# Upgrade pip and install build tools
python -m pip install --upgrade pip setuptools wheel

# Install backend dependencies
if [ -f "backend/requirements.txt" ]; then
    echo "Installing from backend/requirements.txt..."
    pip install -r backend/requirements.txt
fi

# Install development requirements
if [ -f ".devcontainer/requirements-dev.txt" ]; then
    echo "Installing development dependencies..."
    pip install -r .devcontainer/requirements-dev.txt
fi

# Install from pyproject.toml if it exists
if [ -f "pyproject.toml" ]; then
    echo "Installing from pyproject.toml..."
    pip install -e .
fi

# Install additional ML/AI packages commonly used
pip install \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    pydantic==2.5.0 \
    python-multipart==0.0.6 \
    python-dotenv==1.0.0 \
    sqlalchemy==2.0.23 \
    alembic==1.13.0 \
    pytest==7.4.3 \
    httpx==0.25.2 \
    websockets==11.0.3 \
    redis==4.5.5 \
    pandas==2.0.0 \
    numpy==1.24.0 \
    scikit-learn==1.2.2 \
    python-socketio==5.8.0 \
    asyncio-mqtt==0.11.1

echo "📦 Installing Node.js dependencies..."

# Install global npm packages
npm install -g \
    npm@latest \
    create-react-app \
    typescript \
    @types/node \
    nodemon \
    concurrently

# Install frontend dependencies
if [ -f "frontend/package.json" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Install root package.json dependencies if exists
if [ -f "package.json" ]; then
    echo "Installing root dependencies..."
    npm install
fi

echo "🔧 Setting up development tools..."

# Create basic FastAPI app if main.py doesn't exist
if [ ! -f "backend/main.py" ]; then
    echo "Creating basic FastAPI application..."
    mkdir -p backend
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
    description="AI-powered HVAC management platform",
    version="2.0.0"
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
    return {"message": "VentAI API is running", "version": "2.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ventai-api"}

@app.get("/api/v1/analytics/projects/{project_id}")
async def get_project_analytics(project_id: int):
    """Get project analytics"""
    return {
        "project_id": project_id,
        "metrics": {
            "completion_rate": 0.75,
            "budget_compliance": 0.9,
            "performance_score": 0.85
        },
        "insights": [
            "Project is on track for completion",
            "Budget utilization is optimal",
            "Performance metrics are above average"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
fi

# Create environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Development Environment Variables
NODE_ENV=development
FASTAPI_ENV=development
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Database
DATABASE_URL=sqlite:///./ventai_enterprise.db
POSTGRES_URL=postgresql://postgres:postgres@localhost:5432/ventai

# Redis
REDIS_URL=redis://localhost:6379

# API Keys (add your actual keys)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here

# Ports
BACKEND_PORT=8000
FRONTEND_PORT=3000
EOF
fi

# Create launch configuration for VS Code
mkdir -p .vscode
cat > .vscode/launch.json << EOF
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI (Backend)",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "backend.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "\${workspaceFolder}:\${workspaceFolder}/src:\${workspaceFolder}/backend"
            },
            "cwd": "\${workspaceFolder}"
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "\${file}",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "\${workspaceFolder}:\${workspaceFolder}/src:\${workspaceFolder}/backend"
            }
        },
        {
            "name": "Python: Pytest Current File",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "\${file}",
                "-v"
            ],
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "\${workspaceFolder}:\${workspaceFolder}/src:\${workspaceFolder}/backend"
            }
        },
        {
            "name": "Python: Test Working",
            "type": "python",
            "request": "launch",
            "program": "\${workspaceFolder}/working_test.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "\${workspaceFolder}:\${workspaceFolder}/src:\${workspaceFolder}/backend"
            }
        },
        {
            "name": "Node.js: Backend Server",
            "type": "node",
            "request": "launch",
            "program": "\${workspaceFolder}/server.ts",
            "outFiles": ["\${workspaceFolder}/dist/**/*.js"],
            "runtimeArgs": ["-r", "ts-node/register"],
            "env": {
                "NODE_ENV": "development"
            }
        }
    ]
}
EOF

# Create tasks.json for common development tasks
cat > .vscode/tasks.json << EOF
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start Backend (FastAPI)",
            "type": "shell",
            "command": "uvicorn",
            "args": [
                "backend.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Start Frontend (React)",
            "type": "shell",
            "command": "npm",
            "args": ["start"],
            "options": {
                "cwd": "\${workspaceFolder}/frontend"
            },
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Start Enterprise Services",
            "type": "shell",
            "command": "bash",
            "args": ["start-enterprise-services.sh"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Start Windsurf Integration",
            "type": "shell",
            "command": "bash",
            "args": ["start-windsurf-integration.sh"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Run All Tests",
            "type": "shell",
            "command": "bash",
            "args": ["run_tests.sh"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Run Python Tests",
            "type": "shell",
            "command": "pytest",
            "args": ["-v", "tests/", "backend/tests/"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Run Frontend Tests",
            "type": "shell",
            "command": "npm",
            "args": ["test"],
            "options": {
                "cwd": "\${workspaceFolder}/frontend"
            },
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Build TypeScript",
            "type": "shell",
            "command": "tsc",
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": ["\$tsc"]
        },
        {
            "label": "Install Dependencies",
            "type": "shell",
            "command": "bash",
            "args": [".devcontainer/setup.sh"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Format Python Code",
            "type": "shell",
            "command": "black",
            "args": ["backend/", "src/", "tests/"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "problemMatcher": []
        }
    ]
}
EOF

echo "🎯 Creating development scripts..."

# Create start script for development
cat > start-dev.sh << EOF
#!/bin/bash
echo "🚀 Starting VentAI development servers..."

# Function to kill background processes on exit
cleanup() {
    echo "Stopping servers..."
    kill \$(jobs -p) 2>/dev/null
    exit
}
trap cleanup SIGINT SIGTERM

# Check if enterprise services should be started
if [ "\$1" = "--enterprise" ] || [ "\$1" = "-e" ]; then
    echo "Starting enterprise services..."
    bash start-enterprise-services.sh &
fi

# Check if windsurf integration should be started
if [ "\$1" = "--windsurf" ] || [ "\$1" = "-w" ]; then
    echo "Starting Windsurf integration..."
    bash start-windsurf-integration.sh &
fi

# Start external services (PostgreSQL, Redis)
if command -v docker-compose >/dev/null 2>&1; then
    echo "Starting external services (PostgreSQL, Redis)..."
    docker-compose -f .devcontainer/docker-compose.yml up -d
fi

# Start backend
if [ -f "backend/main.py" ]; then
    echo "Starting FastAPI backend on port 8000..."
    cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    cd ..
else
    echo "Warning: backend/main.py not found"
fi

# Start frontend if available
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    echo "Starting React frontend on port 3000..."
    cd frontend && npm start &
    cd ..
else
    echo "Info: Frontend not found or not configured"
fi

echo ""
echo "✅ Development servers started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🗄️ pgAdmin: http://localhost:5050"
echo "📊 Redis Commander: http://localhost:8081"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for all background processes
wait
EOF

chmod +x start-dev.sh

# Create VS Code workspace settings
cat > .vscode/settings.json << EOF
{
    "python.defaultInterpreterPath": "/usr/local/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": ["tests", "backend/tests"],
    "python.terminal.activateEnvironment": false,
    "typescript.preferences.importModuleSpecifier": "relative",
    "editor.formatOnSave": true,
    "editor.rulers": [88, 120],
    "files.associations": {
        "*.py": "python",
        "*.tsx": "typescriptreact",
        "*.ts": "typescript",
        "*.sh": "shellscript"
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/node_modules": true,
        "**/.git": true,
        "**/.DS_Store": true,
        "**/Thumbs.db": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true,
        "**/coverage": true,
        "**/dist": true,
        "**/*.egg-info": true
    },
    "search.exclude": {
        "**/node_modules": true,
        "**/coverage": true,
        "**/.pytest_cache": true,
        "**/__pycache__": true,
        "**/dist": true
    },
    "terminal.integrated.defaultProfile.linux": "zsh",
    "terminal.integrated.cwd": "\${workspaceFolder}",
    "git.ignoreLimitWarning": true,
    "explorer.confirmDelete": false,
    "explorer.confirmDragAndDrop": false,
    "workbench.editor.enablePreview": false,
    "breadcrumbs.enabled": true,
    "python.analysis.autoImportCompletions": true,
    "python.analysis.typeCheckingMode": "basic",
    "eslint.workingDirectories": ["frontend"],
    "typescript.updateImportsOnFileMove.enabled": "always",
    "emmet.includeLanguages": {
        "javascript": "javascriptreact",
        "typescript": "typescriptreact"
    }
}
EOF

echo "✅ VentAI development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Run 'bash start-dev.sh' to start both frontend and backend"
echo "2. Run 'bash start-dev.sh --enterprise' to include enterprise services"
echo "3. Run 'bash start-dev.sh --windsurf' to include Windsurf integration"
echo "4. Or use VS Code tasks: Ctrl+Shift+P -> 'Tasks: Run Task'"
echo "5. Backend will be available at: http://localhost:8000"
echo "6. Frontend will be available at: http://localhost:3000"
echo "7. API docs at: http://localhost:8000/docs"
echo ""
echo "🔧 Available commands:"
echo "- pytest: Run tests"
echo "- bash run_tests.sh: Run your existing test suite"
echo "- bash .devcontainer/quick-test.sh: Quick environment test"
echo "- uvicorn backend.main:app --reload: Start backend only"
echo "- npm run dev: Start frontend only (from frontend/)"
echo ""

# Make quick-test executable
chmod +x .devcontainer/quick-test.sh

# Run quick test to verify setup
echo "🧪 Running quick environment test..."
bash .devcontainer/quick-test.sh
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
