#!/bin/bash

# VentAI Quick Development Setup (Minimal Dependencies)
# This script sets up a local development environment with minimal dependencies

set -e

echo "🚀 Quick VentAI Development Setup (Minimal)"
echo "============================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if we're in the correct directory
if [ ! -f "package.json" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the VentAI project root directory"
    exit 1
fi

print_status "Setting up backend with minimal dependencies..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install minimal dependencies
print_status "Installing minimal Python dependencies..."
pip install --upgrade pip

# Install core dependencies manually to avoid compilation issues
pip install fastapi==0.115.6
pip install "uvicorn[standard]==0.32.1"
pip install python-multipart==0.0.20
pip install python-dotenv==1.0.1
pip install httpx==0.27.0
pip install requests==2.32.3

# Try to install optional dependencies
print_status "Installing optional dependencies (skipping if failed)..."
pip install cryptography==44.0.0 || print_warning "Failed to install cryptography"
pip install passlib==1.7.4 || print_warning "Failed to install passlib"
pip install numpy==1.26.4 || print_warning "Failed to install numpy"
pip install pandas==2.2.2 || print_warning "Failed to install pandas"
pip install pytest==7.4.0 || print_warning "Failed to install pytest"

# Setup environment for minimal local development
print_status "Setting up minimal environment..."
cat > .env.minimal << EOF
# Minimal Development Environment
NODE_ENV=development
ENVIRONMENT=development

# Database (SQLite for simplicity)
DATABASE_URL=sqlite:///./ventai_minimal.db

# Application Ports
BACKEND_PORT=8000
FRONTEND_PORT=3000

# Security (development only)
SECRET_KEY=dev-secret-key-minimal
ENCRYPTION_KEY=P-K5ljoDHJvr7AU-P-gsY3wtTuXAP-3PyuR7nfQsPE8=

# AI (mock for development)
GEMINI_API_KEY=mock-development-key
ENVIRONMENT=development
PYTHONPATH=/workspaces/MVP/backend/src

# Logging
LOG_LEVEL=INFO
EOF

cd ..

print_status "Setting up frontend..."
cd frontend

# Install frontend dependencies
if [ -f "package.json" ]; then
    print_status "Installing frontend dependencies..."
    npm install --no-optional || print_warning "Some frontend packages failed to install"
fi

# Create minimal frontend environment
cat > .env.local << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
GENERATE_SOURCEMAP=false
CHOKIDAR_USEPOLLING=true
EOF

cd ..

# Create simple startup scripts
print_status "Creating startup scripts..."

# Simple backend startup
cat > start-backend-minimal.sh << 'EOF'
#!/bin/bash
echo "🔧 Starting VentAI Backend (Minimal)"
cd backend
source venv/bin/activate
export $(grep -v '^#' .env.minimal | xargs)
cd src
python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload
EOF

# Simple frontend startup
cat > start-frontend-minimal.sh << 'EOF'
#!/bin/bash
echo "📱 Starting VentAI Frontend"
cd frontend
npm start
EOF

# Combined startup
cat > start-minimal-dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting VentAI Minimal Development Environment"
echo "================================================="

cleanup() {
    echo "🛑 Stopping services..."
    jobs -p | xargs -r kill
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "🔧 Starting backend..."
./start-backend-minimal.sh &

sleep 3

echo "📱 Starting frontend..."
echo ""
echo "🎉 VentAI Development Environment Started!"
echo "========================================="
echo "📱 Frontend:     http://localhost:3000"
echo "🔧 Backend API:  http://localhost:8000"
echo "📖 API Docs:     http://localhost:8000/docs"
echo "❤️  Health:      http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

./start-frontend-minimal.sh
EOF

chmod +x start-backend-minimal.sh start-frontend-minimal.sh start-minimal-dev.sh

print_success "Minimal development environment setup complete!"
echo ""
echo "🎯 Quick Start:"
echo "  ./start-minimal-dev.sh    - Start both frontend and backend"
echo "  ./start-backend-minimal.sh  - Start only backend"
echo "  ./start-frontend-minimal.sh - Start only frontend"
echo ""
echo "🌐 Access:"
echo "  Frontend:    http://localhost:3000"
echo "  Backend:     http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo "  Health:      http://localhost:8000/health"
echo ""
print_success "Ready to develop! Run './start-minimal-dev.sh' to begin."
