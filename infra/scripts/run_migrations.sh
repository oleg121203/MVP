#!/bin/bash
# Script to run database migrations for Vent.AI backend

# Go to the vent-ai-backend directory
cd "$(dirname "$0")/../vent-ai-backend"

# Activate the virtual environment if it exists
if [ -f "../myenv/bin/activate" ]; then
    source "../myenv/bin/activate"
    echo "Activated virtual environment"
else
    echo "Warning: Virtual environment not found at ../myenv/bin/activate"
fi

# Run the migration script
echo "Running database migrations..."
python run_migrations.py

# Check if migration was successful
if [ $? -eq 0 ]; then
    echo "✅ Database migrations completed successfully"
else
    echo "❌ Database migrations failed"
    exit 1
fi

echo "✨ Your database is now up to date with the latest schema changes"
