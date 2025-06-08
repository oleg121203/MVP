#!/bin/bash

# VentAI Project Setup Script
# This script sets up the complete development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if command exists
check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        success "$1 is installed"
        return 0
    else
        error "$1 is not installed"
        return 1
    fi
}

# Setup environment
setup_environment() {
    log "Setting up environment files..."
    
    # Copy development environment if .env doesn't exist
    if [ ! -f ".env" ]; then
        cp environments/.env.development .env
        success "Created .env from development template"
    else
        warning ".env already exists, skipping"
    fi
    
    # Create logs directories
    mkdir -p backend/logs services/mcp/logs
    success "Created log directories"
}

# Install dependencies
install_dependencies() {
    log "Installing project dependencies..."
    
    # Install root dependencies
    npm install
    success "Installed root dependencies"
    
    # Install frontend dependencies
    log "Installing frontend dependencies..."
    cd frontend
    npm install --legacy-peer-deps
    cd ..
    success "Installed frontend dependencies"
    
    # Setup Python virtual environment and install backend dependencies
    log "Setting up Python environment..."
    cd backend
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        success "Created Python virtual environment"
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
    success "Installed backend dependencies"
    
    # Install MCP service dependencies
    log "Installing MCP service dependencies..."
    cd services/mcp
    if [ ! -f "requirements.txt" ]; then
        cp ../../backend/requirements.txt .
    fi
    pip install -r requirements.txt
    cd ../..
    success "Installed MCP service dependencies"
}

# Setup database
setup_database() {
    log "Setting up database..."
    
    # Start database services
    docker-compose -f infra/docker/docker-compose-db.yml up -d
    
    # Wait for database to be ready
    log "Waiting for database to be ready..."
    sleep 10
    
    # Run migrations
    cd backend
    source venv/bin/activate
    if [ -f "alembic.ini" ]; then
        python -m alembic upgrade head
        success "Database migrations completed"
    else
        warning "No alembic.ini found, skipping migrations"
    fi
    cd ..
}

# Main setup function
main() {
    log "Starting VentAI project setup..."
    
    # Check prerequisites
    log "Checking prerequisites..."
    check_command "node" || exit 1
    check_command "npm" || exit 1
    check_command "python3" || exit 1
    check_command "docker" || exit 1
    check_command "docker-compose" || exit 1
    
    # Run setup steps
    setup_environment
    install_dependencies
    
    # Ask if user wants to setup database
    read -p "Do you want to setup the database? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_database
    fi
    
    log "Setup completed successfully!"
    success "Your VentAI development environment is ready!"
    
    echo ""
    echo "Next steps:"
    echo "1. Configure your API keys in .env file"
    echo "2. Run: npm run dev (for Docker development)"
    echo "3. Or run: npm run dev:local (for local development)"
    echo "4. Access frontend at: http://localhost:3000"
    echo "5. Access backend API at: http://localhost:8000/docs"
}

# Run main function
main "$@"
