#!/bin/sh
until pg_isready -h postgres -U postgres; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done
exec "$@"
