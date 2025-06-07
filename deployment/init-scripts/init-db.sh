#!/bin/bash

# Database initialization script for PostgreSQL container
# This script runs automatically when the container starts for the first time

set -e

# Create additional database for testing if needed
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pg_trgm";

    -- Create test database
    CREATE DATABASE ${POSTGRES_DB}_test;
    GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB}_test TO $POSTGRES_USER;

    -- Create logging table for API requests
    CREATE TABLE IF NOT EXISTS api_logs (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        method VARCHAR(10),
        endpoint VARCHAR(255),
        status_code INTEGER,
        response_time FLOAT,
        user_id INTEGER,
        ip_address INET
    );

    -- Create index for performance
    CREATE INDEX IF NOT EXISTS idx_api_logs_timestamp ON api_logs(timestamp);
    CREATE INDEX IF NOT EXISTS idx_api_logs_user_id ON api_logs(user_id);
EOSQL

echo "Database initialization completed!"
