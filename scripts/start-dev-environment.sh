#!/bin/bash

# VentAI Development Environment Startup Script
# This script starts the complete development environment with PostgreSQL and Redis

set -e

echo "🚀 Starting VentAI Development Environment..."
echo "================================================"

# Change to the project root
cd "$(dirname "$0")/.."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker compose -f infra/docker/docker-compose.dev.yml down -v

# Pull base images only (postgres, redis)
echo "📥 Pulling base images..."
docker compose -f infra/docker/docker-compose.dev.yml pull db redis || echo "⚠️  Some base images couldn't be pulled, continuing..."

# Build development images
echo "🔨 Building development images..."
docker compose -f infra/docker/docker-compose.dev.yml build

# Start services in order
echo "🔧 Starting database services..."
docker compose -f infra/docker/docker-compose.dev.yml up -d db redis

# Wait for database to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
timeout=60
counter=0
while ! docker exec ventai-postgres-dev pg_isready -U ventai_dev -d ventai_dev > /dev/null 2>&1; do
    if [ $counter -ge $timeout ]; then
        echo "❌ Timeout waiting for PostgreSQL"
        docker compose -f infra/docker/docker-compose.dev.yml logs db
        exit 1
    fi
    echo "  Waiting... ($counter/${timeout}s)"
    sleep 2
    counter=$((counter + 2))
done

echo "✅ PostgreSQL is ready"

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."
timeout=30
counter=0
while ! docker exec ventai-redis-dev redis-cli ping > /dev/null 2>&1; do
    if [ $counter -ge $timeout ]; then
        echo "❌ Timeout waiting for Redis"
        docker compose -f infra/docker/docker-compose.dev.yml logs redis
        exit 1
    fi
    echo "  Waiting... ($counter/${timeout}s)"
    sleep 1
    counter=$((counter + 1))
done

echo "✅ Redis is ready"

# Start backend
echo "🔧 Starting backend service..."
docker compose -f infra/docker/docker-compose.dev.yml up -d backend

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
timeout=120
counter=0
while ! docker exec ventai-backend-dev python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" > /dev/null 2>&1; do
    if [ $counter -ge $timeout ]; then
        echo "❌ Timeout waiting for backend"
        echo "Backend logs:"
        docker compose -f infra/docker/docker-compose.dev.yml logs backend
        exit 1
    fi
    echo "  Waiting... ($counter/${timeout}s)"
    sleep 3
    counter=$((counter + 3))
done

echo "✅ Backend is ready"

# Start frontend
echo "🔧 Starting frontend service..."
docker compose -f infra/docker/docker-compose.dev.yml up -d frontend

# Start MCP server
echo "🔧 Starting MCP server..."
docker compose -f infra/docker/docker-compose.dev.yml up -d mcp-server

echo ""
echo "🎉 VentAI Development Environment is ready!"
echo "================================================"
echo "📱 Frontend:     http://localhost:3000"
echo "🔧 Backend API:  http://localhost:8000"
echo "📖 API Docs:     http://localhost:8000/docs"
echo "🤖 MCP Server:   http://localhost:8001"
echo "🗃️  PostgreSQL:   localhost:5433"
echo "🔴 Redis:        localhost:6380"
echo ""
echo "🔍 To view logs: docker compose -f infra/docker/docker-compose.dev.yml logs -f [service]"
echo "🛑 To stop:      docker compose -f infra/docker/docker-compose.dev.yml down"
echo ""

# Show service status
echo "📊 Service Status:"
docker compose -f infra/docker/docker-compose.dev.yml ps
