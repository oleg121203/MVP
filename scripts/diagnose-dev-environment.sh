#!/bin/bash

# VentAI Development Environment Diagnostic Script
# This script helps diagnose common issues with the development environment

echo "🔍 VentAI Development Environment Diagnostics"
echo "=============================================="

# Check Docker
echo "📦 Docker Status:"
if docker info > /dev/null 2>&1; then
    echo "  ✅ Docker is running"
    echo "  📊 Docker version: $(docker --version)"
else
    echo "  ❌ Docker is not running"
    exit 1
fi

echo ""
echo "🐳 Container Status:"
cd "$(dirname "$0")/.."

# Check if containers exist
containers=$(docker compose -f infra/docker/docker-compose.dev.yml ps --format table)
if [ -n "$containers" ]; then
    echo "$containers"
else
    echo "  ℹ️  No containers are running"
fi

echo ""
echo "🔗 Network Connectivity:"

# Test PostgreSQL
if docker exec ventai-postgres-dev pg_isready -U ventai_dev -d ventai_dev > /dev/null 2>&1; then
    echo "  ✅ PostgreSQL is accessible"
    echo "     Database: $(docker exec ventai-postgres-dev psql -U ventai_dev -d ventai_dev -t -c "SELECT current_database();" | xargs)"
    echo "     User: $(docker exec ventai-postgres-dev psql -U ventai_dev -d ventai_dev -t -c "SELECT current_user;" | xargs)"
else
    echo "  ❌ PostgreSQL is not accessible"
fi

# Test Redis
if docker exec ventai-redis-dev redis-cli ping > /dev/null 2>&1; then
    echo "  ✅ Redis is accessible"
    echo "     Info: $(docker exec ventai-redis-dev redis-cli info server | grep redis_version | cut -d: -f2 | tr -d '\r')"
else
    echo "  ❌ Redis is not accessible"
fi

# Test Backend
if docker exec ventai-backend-dev python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" > /dev/null 2>&1; then
    echo "  ✅ Backend is accessible"
    echo "     Health: $(docker exec ventai-backend-dev python -c "import urllib.request, json; print(json.loads(urllib.request.urlopen('http://localhost:8000/health').read().decode()))" 2>/dev/null || echo "Unable to parse health response")"
else
    echo "  ❌ Backend is not accessible"
fi

echo ""
echo "📝 Recent Logs (last 10 lines):"
echo "  PostgreSQL:"
docker compose -f infra/docker/docker-compose.dev.yml logs --tail 10 db 2>/dev/null | sed 's/^/    /'

echo "  Backend:"
docker compose -f infra/docker/docker-compose.dev.yml logs --tail 10 backend 2>/dev/null | sed 's/^/    /'

echo ""
echo "🌐 External Access:"
echo "  Frontend:    http://localhost:3000"
echo "  Backend:     http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo "  PostgreSQL:  localhost:5433"
echo "  Redis:       localhost:6380"

echo ""
echo "🛠️  Troubleshooting Commands:"
echo "  View logs:   docker compose -f infra/docker/docker-compose.dev.yml logs -f [service]"
echo "  Restart:     docker compose -f infra/docker/docker-compose.dev.yml restart [service]"
echo "  Reset:       docker compose -f infra/docker/docker-compose.dev.yml down -v && ./scripts/start-dev-environment.sh"
