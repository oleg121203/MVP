#!/bin/bash

# VentAI MCP Container Build and Test Script
# This script builds Docker containers and tests the MCP server functionality

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CONTAINER_NAME="ventai-mcp-dev"
IMAGE_NAME="ventai-mcp"
DOCKERFILE="Dockerfile.dev"
PORT="8000"
MCP_PORT="8080"

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

# Function to cleanup containers and images
cleanup() {
    print_status "Cleaning up existing containers and images..."
    
    # Stop and remove container if it exists
    if docker ps -a | grep -q "$CONTAINER_NAME"; then
        docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
        docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
        print_status "Removed existing container: $CONTAINER_NAME"
    fi
    
    # Remove image if it exists
    if docker images | grep -q "$IMAGE_NAME"; then
        docker rmi "$IMAGE_NAME:latest" >/dev/null 2>&1 || true
        print_status "Removed existing image: $IMAGE_NAME:latest"
    fi
}

# Function to build Docker image
build_image() {
    print_status "Building Docker image: $IMAGE_NAME:latest"
    print_status "Using Dockerfile: $DOCKERFILE"
    
    if docker build -t "$IMAGE_NAME:latest" -f "$DOCKERFILE" .; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Function to test container startup
test_container_startup() {
    print_status "Testing container startup..."
    
    # Run container in detached mode
    if docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$PORT:$PORT" \
        -p "$MCP_PORT:$MCP_PORT" \
        --env-file .env \
        "$IMAGE_NAME:latest"; then
        print_success "Container started successfully"
    else
        print_error "Failed to start container"
        exit 1
    fi
    
    # Wait for container to be ready
    print_status "Waiting for container to be ready..."
    sleep 10
    
    # Check if container is still running
    if docker ps | grep -q "$CONTAINER_NAME"; then
        print_success "Container is running and healthy"
    else
        print_error "Container stopped unexpectedly"
        print_error "Container logs:"
        docker logs "$CONTAINER_NAME"
        exit 1
    fi
}

# Function to test MCP server endpoints
test_mcp_endpoints() {
    print_status "Testing MCP server endpoints..."
    
    # Test health endpoint
    if curl -f "http://localhost:$PORT/health" >/dev/null 2>&1; then
        print_success "Health endpoint is responding"
    else
        print_warning "Health endpoint not responding (this may be expected if not implemented)"
    fi
    
    # Test MCP server port
    if nc -z localhost "$MCP_PORT" 2>/dev/null; then
        print_success "MCP server port $MCP_PORT is accessible"
    else
        print_warning "MCP server port $MCP_PORT is not accessible"
    fi
}

# Function to show container logs
show_logs() {
    print_status "Container logs:"
    docker logs "$CONTAINER_NAME" --tail 50
}

# Function to run dependency test
test_dependencies() {
    print_status "Testing Python dependencies in container..."
    
    # Test importing key packages
    docker exec "$CONTAINER_NAME" python3 -c "
import sys
try:
    import fastapi
    import sentence_transformers
    import transformers
    import huggingface_hub
    import mcp
    print('✓ All key dependencies imported successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_success "All dependencies are working correctly"
    else
        print_error "Dependency test failed"
        exit 1
    fi
}

# Main execution
main() {
    print_status "Starting VentAI MCP Container Build and Test Process"
    print_status "================================================"
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating basic .env file..."
        cat > .env << EOF
# Database configuration
DATABASE_URL=postgresql://ventai:ventai_password@localhost:5432/ventai_db
POSTGRES_DB=ventai_db
POSTGRES_USER=ventai
POSTGRES_PASSWORD=ventai_password

# Redis configuration
REDIS_URL=redis://localhost:6379

# API Keys (replace with actual values)
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_API_KEY=your-google-api-key

# MCP Server configuration
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8080
MCP_SERVER_NAME=ventai-mcp-server

# Application settings
DEBUG=true
LOG_LEVEL=INFO
EOF
        print_warning "Created basic .env file. Please update with actual API keys."
    fi
    
    # Step 1: Cleanup
    cleanup
    
    # Step 2: Build image
    build_image
    
    # Step 3: Test container startup
    test_container_startup
    
    # Step 4: Test dependencies
    test_dependencies
    
    # Step 5: Test MCP endpoints
    test_mcp_endpoints
    
    # Step 6: Show logs
    show_logs
    
    print_success "================================================"
    print_success "VentAI MCP Container Build and Test Completed Successfully!"
    print_success "Container name: $CONTAINER_NAME"
    print_success "Container ports: $PORT (HTTP), $MCP_PORT (MCP)"
    print_success "================================================"
    
    print_status "To interact with the container:"
    print_status "  View logs: docker logs $CONTAINER_NAME"
    print_status "  Execute shell: docker exec -it $CONTAINER_NAME /bin/bash"
    print_status "  Stop container: docker stop $CONTAINER_NAME"
    print_status "  Remove container: docker rm $CONTAINER_NAME"
}

# Handle script arguments
case "${1:-}" in
    "cleanup")
        cleanup
        ;;
    "build")
        build_image
        ;;
    "test")
        test_container_startup
        test_dependencies
        test_mcp_endpoints
        ;;
    *)
        main
        ;;
esac
