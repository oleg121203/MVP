#!/bin/bash
# Script to start PostgreSQL and Redis services for development

echo "Starting PostgreSQL and Redis services for VentAI development..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please start Docker and try again."
  exit 1
fi

# Start the services
docker-compose -f docker-compose-db.yml up -d

# Check if services are running
echo "Checking if services are running..."
sleep 5

# Check PostgreSQL
if docker ps | grep -q ventai-postgres-dev; then
  echo "✅ PostgreSQL is running on port 5432"
else
  echo "❌ PostgreSQL failed to start"
fi

# Check Redis
if docker ps | grep -q ventai-redis-dev; then
  echo "✅ Redis is running on port 6379"
else
  echo "❌ Redis failed to start"
fi

echo ""
echo "Database services are ready. You can now start the backend with:"
echo "cd backend/src && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "To stop the services:"
echo "docker-compose -f docker-compose-db.yml down"
