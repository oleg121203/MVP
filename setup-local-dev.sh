#!/bin/bash

# VentAI Development Environment Setup (without Docker)
# This script sets up a local development environment for VentAI

set -e

echo "🚀 Setting up VentAI Development Environment (Local)"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the correct directory
if [ ! -f "package.json" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the VentAI project root directory"
    exit 1
fi

print_status "Checking prerequisites..."

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
else
    print_error "Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Docker is available
if command -v docker &> /dev/null && docker info &> /dev/null; then
    print_success "Docker is available"
    DOCKER_AVAILABLE=true
else
    print_warning "Docker is not available. Will setup local development environment."
    DOCKER_AVAILABLE=false
fi

# Setup backend
print_status "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
print_status "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables for local development
print_status "Setting up environment variables..."
cat > .env.local << EOF
# Local Development Environment Configuration
NODE_ENV=development
ENVIRONMENT=development

# Database Configuration (SQLite for local development)
DATABASE_URL=sqlite:///./ventai_local.db

# Application Ports
FRONTEND_PORT=3000
BACKEND_PORT=8000
MCP_PORT=8001

# Security Configuration
SECRET_KEY=dev-secret-key-change-in-production-very-long-and-secure
ENCRYPTION_KEY=P-K5ljoDHJvr7AU-P-gsY3wtTuXAP-3PyuR7nfQsPE8=
JWT_SECRET_KEY=jwt-secret-key-for-development-change-in-production

# API Keys (Development - Optional)
GEMINI_API_KEY=mock-development-key
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
PINECONE_API_KEY=
HUBSPOT_API_KEY=

# AI Provider Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# MCP Configuration
MCP_LOG_LEVEL=INFO
VENTAI_PROJECT_ROOT=.

# Business Configuration
LABOR_COST_PER_HOUR=50.0
ENERGY_COST_PER_KWH=0.12

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
EOF

# Run database migrations if needed
if [ -f "src/django_project/manage.py" ]; then
    print_status "Running Django database setup..."
    cd src/django_project
    python manage.py makemigrations --noinput || true
    python manage.py migrate --noinput || true
    cd ../..
fi

cd ..

# Setup frontend
print_status "Setting up frontend..."
cd frontend

# Install Node.js dependencies
if [ -f "package.json" ]; then
    print_status "Installing Node.js dependencies..."
    npm install
fi

# Setup frontend environment
cat > .env.local << EOF
# Frontend Local Development Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_MCP_URL=http://localhost:8001
REACT_APP_ENVIRONMENT=development

# Development settings
CHOKIDAR_USEPOLLING=true
DISABLE_ESLINT_PLUGIN=true
ESLINT_NO_DEV_ERRORS=true
GENERATE_SOURCEMAP=false
EOF

cd ..

# Create startup scripts
print_status "Creating startup scripts..."

# Backend startup script
cat > start-backend-local.sh << 'EOF'
#!/bin/bash
echo "🔧 Starting VentAI Backend (Local Development)"
cd backend
source venv/bin/activate
export $(grep -v '^#' .env.local | xargs)
cd src
python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload
EOF

# Frontend startup script
cat > start-frontend-local.sh << 'EOF'
#!/bin/bash
echo "📱 Starting VentAI Frontend (Local Development)"
cd frontend
npm start
EOF

# MCP server startup script
cat > start-mcp-local.sh << 'EOF'
#!/bin/bash
echo "🤖 Starting VentAI MCP Server (Local Development)"
cd backend
source venv/bin/activate
export $(grep -v '^#' .env.local | xargs)
python mcp_server.py
EOF

# Make scripts executable
chmod +x start-backend-local.sh start-frontend-local.sh start-mcp-local.sh

# Create a combined startup script
cat > start-local-dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting VentAI Local Development Environment"
echo "==============================================="

# Function to kill background processes on exit
cleanup() {
    echo "🛑 Stopping all services..."
    jobs -p | xargs -r kill
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend in background
echo "🔧 Starting backend..."
./start-backend-local.sh &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start MCP server in background
echo "🤖 Starting MCP server..."
./start-mcp-local.sh &
MCP_PID=$!

# Wait a bit more
sleep 2

# Start frontend
echo "📱 Starting frontend..."
echo ""
echo "🎉 VentAI Development Environment Started!"
echo "=========================================="
echo "📱 Frontend:     http://localhost:3000"
echo "🔧 Backend API:  http://localhost:8000"
echo "📖 API Docs:     http://localhost:8000/docs"
echo "🤖 MCP Server:   http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

./start-frontend-local.sh
EOF

chmod +x start-local-dev.sh

# Setup complete
print_success "Local development environment setup complete!"
echo ""
echo "🎯 Quick Start:"
echo "  1. Start all services: ./start-local-dev.sh"
echo "  2. Or start individually:"
echo "     - Backend:    ./start-backend-local.sh"
echo "     - Frontend:   ./start-frontend-local.sh"
echo "     - MCP Server: ./start-mcp-local.sh"
echo ""
echo "🌐 Access Points:"
echo "  - Frontend:     http://localhost:3000"
echo "  - Backend API:  http://localhost:8000"
echo "  - API Docs:     http://localhost:8000/docs"
echo "  - MCP Server:   http://localhost:8001"
echo ""

if [ "$DOCKER_AVAILABLE" = true ]; then
    echo "🐳 Docker is available. You can also use:"
    echo "  - Docker setup: ./scripts/start-dev-environment.sh"
    echo ""
fi

print_success "Setup complete! Run './start-local-dev.sh' to start development."
