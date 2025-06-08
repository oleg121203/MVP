#!/bin/bash

# VentAI Local Development Diagnostics
# This script helps diagnose issues with the local development environment

echo "🔍 VentAI Local Development Diagnostics"
echo "======================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✅]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌]${NC} $1"
}

# Check if we're in the correct directory
if [ ! -f "package.json" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the VentAI project root directory"
    exit 1
fi

print_status "System Requirements Check"
echo "=========================="

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js: $NODE_VERSION"
else
    print_error "Node.js not found"
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_success "npm: $NPM_VERSION"
else
    print_error "npm not found"
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python: $PYTHON_VERSION"
else
    print_error "Python 3 not found"
fi

# Check pip
if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version)
    else
        PIP_VERSION=$(pip --version)
    fi
    print_success "pip: $PIP_VERSION"
else
    print_error "pip not found"
fi

echo ""
print_status "Project Structure Check"
echo "======================"

# Check backend structure
if [ -d "backend" ]; then
    print_success "Backend directory exists"
    
    if [ -f "backend/requirements.txt" ]; then
        print_success "Backend requirements.txt found"
    else
        print_error "Backend requirements.txt missing"
    fi
    
    if [ -d "backend/venv" ]; then
        print_success "Backend virtual environment exists"
    else
        print_warning "Backend virtual environment not found (run setup-local-dev.sh)"
    fi
    
    if [ -f "backend/.env.local" ]; then
        print_success "Backend .env.local exists"
    else
        print_warning "Backend .env.local missing (run setup-local-dev.sh)"
    fi
else
    print_error "Backend directory missing"
fi

# Check frontend structure
if [ -d "frontend" ]; then
    print_success "Frontend directory exists"
    
    if [ -f "frontend/package.json" ]; then
        print_success "Frontend package.json found"
    else
        print_error "Frontend package.json missing"
    fi
    
    if [ -d "frontend/node_modules" ]; then
        print_success "Frontend node_modules exists"
    else
        print_warning "Frontend node_modules missing (run npm install in frontend/)"
    fi
    
    if [ -f "frontend/.env.local" ]; then
        print_success "Frontend .env.local exists"
    else
        print_warning "Frontend .env.local missing (run setup-local-dev.sh)"
    fi
else
    print_error "Frontend directory missing"
fi

echo ""
print_status "Service Status Check"
echo "==================="

# Check if services are running
if pgrep -f "uvicorn.*fastapi_app.main:app" > /dev/null; then
    print_success "Backend service is running"
    
    # Test backend health
    if command -v curl &> /dev/null; then
        if curl -s http://localhost:8000/health > /dev/null; then
            print_success "Backend health check passed"
        else
            print_warning "Backend health check failed"
        fi
    fi
else
    print_warning "Backend service not running"
fi

if pgrep -f "npm.*start" > /dev/null || pgrep -f "react-scripts start" > /dev/null; then
    print_success "Frontend service is running"
else
    print_warning "Frontend service not running"
fi

if pgrep -f "mcp_server.py" > /dev/null; then
    print_success "MCP server is running"
else
    print_warning "MCP server not running"
fi

echo ""
print_status "Port Check"
echo "=========="

# Check if ports are in use
if netstat -tuln 2>/dev/null | grep -q ":3000 "; then
    print_success "Port 3000 (Frontend) is in use"
else
    print_warning "Port 3000 (Frontend) is free"
fi

if netstat -tuln 2>/dev/null | grep -q ":8000 "; then
    print_success "Port 8000 (Backend) is in use"
else
    print_warning "Port 8000 (Backend) is free"
fi

if netstat -tuln 2>/dev/null | grep -q ":8001 "; then
    print_success "Port 8001 (MCP) is in use"
else
    print_warning "Port 8001 (MCP) is free"
fi

echo ""
print_status "Database Check"
echo "============="

if [ -f "backend/.env.local" ]; then
    DATABASE_URL=$(grep "DATABASE_URL" backend/.env.local | cut -d'=' -f2)
    if [[ "$DATABASE_URL" == *"sqlite"* ]]; then
        print_success "Database configured: SQLite"
        
        # Check if database file exists
        if [[ "$DATABASE_URL" == *"sqlite:///"* ]]; then
            DB_PATH=$(echo "$DATABASE_URL" | sed 's|sqlite:///||')
            if [ -f "$DB_PATH" ] || [ -f "backend/$DB_PATH" ]; then
                print_success "SQLite database file exists"
            else
                print_warning "SQLite database file not found (will be created on first run)"
            fi
        fi
    else
        print_success "Database configured: $DATABASE_URL"
    fi
else
    print_warning "Database configuration not found"
fi

echo ""
print_status "Recommendations"
echo "=============="

if [ ! -d "backend/venv" ] || [ ! -f "backend/.env.local" ]; then
    echo "🔧 Run: ./setup-local-dev.sh"
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Run: cd frontend && npm install"
fi

if ! pgrep -f "uvicorn.*fastapi_app.main:app" > /dev/null; then
    echo "🚀 Start backend: ./start-backend-local.sh"
fi

if ! pgrep -f "npm.*start" > /dev/null; then
    echo "📱 Start frontend: ./start-frontend-local.sh"
fi

echo "🎯 Start all services: ./start-local-dev.sh"

echo ""
print_status "Access URLs"
echo "==========="
echo "📱 Frontend:     http://localhost:3000"
echo "🔧 Backend API:  http://localhost:8000"
echo "📖 API Docs:     http://localhost:8000/docs"
echo "🤖 MCP Server:   http://localhost:8001"
echo "❤️  Health Check: http://localhost:8000/health"
