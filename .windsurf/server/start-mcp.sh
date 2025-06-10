#!/bin/bash

# 🚀 Windsurf Enterprise MCP Server - Стартовий скрипт
# Для масштабованого розгортання без прив'язки до macOS

echo "🎯 Запуск Windsurf Enterprise MCP Server..."

# Перевірка Redis
if ! redis-cli -p 6380 ping > /dev/null 2>&1; then
    echo "⚠️  Redis не запущений на порту 6380. Запускаємо..."
    redis-server --port 6380 --daemonize yes
    sleep 2
fi

# Перевірка PostgreSQL
if ! nc -z localhost 5433 > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL не доступний на порту 5433"
    echo "   Переконайтеся, що PostgreSQL запущений з відповідними налаштуваннями"
    exit 1
fi

# Налаштування змінних середовища для масштабованого розгортання
export REDIS_URL="${REDIS_URL:-redis://localhost:6380}"
export DATABASE_URL="${DATABASE_URL:-postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev}"
export WINDSURF_ROOT="${WINDSURF_ROOT:-$(pwd)/..}"
export ENABLE_VECTOR_SEARCH="${ENABLE_VECTOR_SEARCH:-true}"
export ENABLE_GRAPH_RELATIONS="${ENABLE_GRAPH_RELATIONS:-true}"
export NODE_ENV="${NODE_ENV:-production}"

echo "✅ Redis: $REDIS_URL"
echo "✅ PostgreSQL: $DATABASE_URL"
echo "✅ Windsurf Root: $WINDSURF_ROOT"

# Запуск MCP сервера
echo "🚀 Запускаємо MCP Server..."
cd "$(dirname "$0")"
npm run build && node dist/enterprise-index.js
