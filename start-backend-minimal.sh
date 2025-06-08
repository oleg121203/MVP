#!/bin/bash
echo "🔧 Starting VentAI Backend (Minimal)"
cd backend
source venv/bin/activate
export $(grep -v '^#' .env.minimal | xargs)
cd src
python -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload
