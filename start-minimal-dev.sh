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
