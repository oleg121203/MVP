#!/bin/bash

# VentAI Workflow Validation Script
# This script validates the entire development workflow

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
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

# Function to check if command exists
check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        success "$1 is installed"
        return 0
    else
        error "$1 is not installed"
        return 1
    fi
}

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        success "File exists: $1"
        return 0
    else
        error "File missing: $1"
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        success "Directory exists: $1"
        return 0
    else
        error "Directory missing: $1"
        return 1
    fi
}

# Main validation function
main() {
    log "Starting VentAI Workflow Validation..."
    
    # Check prerequisites
    log "Checking prerequisites..."
    check_command "node" || exit 1
    check_command "npm" || exit 1
    check_command "python3" || exit 1
    check_command "docker" || exit 1
    check_command "docker-compose" || exit 1
    
    # Check project structure
    log "Checking project structure..."
    check_file "package.json" || exit 1
    check_file "infra/docker/docker-compose.dev.yml" || exit 1
    check_file "infra/docker/docker-compose.yml" || exit 1
    check_dir "frontend" || exit 1
    check_dir "backend" || exit 1
    check_dir "services/mcp" || exit 1
    check_file "frontend/package.json" || exit 1
    check_file "backend/requirements.txt" || exit 1
    check_file "services/mcp/requirements.txt" || exit 1
    check_file "frontend/Dockerfile.dev" || exit 1
    check_file "backend/Dockerfile.dev" || exit 1
    check_file "services/mcp/Dockerfile" || exit 1
    
    # Validate package.json scripts
    log "Validating package.json scripts..."
    if npm run 2>/dev/null | grep -q "install:all"; then
        success "install:all script exists"
    else
        error "install:all script missing"
        exit 1
    fi
    
    if npm run 2>/dev/null | grep -q "docker:dev"; then
        success "docker:dev script exists"
    else
        error "docker:dev script missing"
        exit 1
    fi
    
    # Check Docker Compose syntax
    log "Validating Docker Compose files..."
    if docker-compose -f infra/docker/docker-compose.dev.yml config >/dev/null 2>&1; then
        success "docker-compose.dev.yml syntax is valid"
    else
        error "docker-compose.dev.yml syntax is invalid"
        exit 1
    fi
    
    if docker-compose -f infra/docker/docker-compose.yml config >/dev/null 2>&1; then
        success "docker-compose.yml syntax is valid"
    else
        error "docker-compose.yml syntax is invalid"
        exit 1
    fi
    
    # Check Dockerfile syntax
    log "Validating Dockerfiles..."
    if docker build -f frontend/Dockerfile.dev -t test-frontend-dev frontend --dry-run >/dev/null 2>&1; then
        success "frontend/Dockerfile.dev syntax is valid"
    else
        warning "frontend/Dockerfile.dev may have issues (dry-run not supported on all Docker versions)"
    fi
    
    if docker build -f backend/Dockerfile.dev -t test-backend-dev backend --dry-run >/dev/null 2>&1; then
        success "backend/Dockerfile.dev syntax is valid"
    else
        warning "backend/Dockerfile.dev may have issues (dry-run not supported on all Docker versions)"
    fi
    
    # Check Python requirements
    log "Checking Python requirements..."
    if python3 -m pip check >/dev/null 2>&1; then
        success "Python requirements are compatible"
    else
        warning "Python requirements may have conflicts"
    fi
    
    # Check Node.js dependencies
    log "Checking Node.js frontend dependencies..."
    cd frontend
    if npm ls >/dev/null 2>&1; then
        success "Frontend Node.js dependencies are compatible"
    else
        warning "Frontend Node.js dependencies may have conflicts"
    fi
    cd ..
    
    # Port availability check
    log "Checking port availability..."
    ports=(3000 8000 8001 5433 6380)
    for port in "${ports[@]}"; do
        if netstat -tuln 2>/dev/null | grep -q ":$port "; then
            warning "Port $port is already in use"
        else
            success "Port $port is available"
        fi
    done
    
    # Environment variables check
    log "Checking environment configuration..."
    if [ -f ".env" ]; then
        success ".env file exists"
    else
        warning ".env file not found - using defaults"
    fi
    
    # Check disk space
    log "Checking disk space..."
    available_space=$(df . | awk 'NR==2 {print $4}')
    if [ "$available_space" -gt 1048576 ]; then  # 1GB in KB
        success "Sufficient disk space available"
    else
        warning "Low disk space - may affect Docker builds"
    fi
    
    # Final summary
    log "Validation completed successfully!"
    success "Your VentAI workflow is ready to run"
    
    echo ""
    echo "Next steps:"
    echo "1. Run: npm run install:all"
    echo "2. Run: npm run docker:dev"
    echo "3. Access frontend at: http://localhost:3000"
    echo "4. Access backend API at: http://localhost:8000/docs"
    echo "5. Access MCP server at: http://localhost:8001"
}

# Run main function
main "$@"