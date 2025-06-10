#!/bin/bash

# VentAI Enterprise Quick Start
# Запускає всі необхідні сервіси для enterprise платформи

echo "🚀 VENTAI ENTERPRISE QUICK START"
echo "================================="

# Перевіряємо наявність Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не встановлено. Встановіть Docker для продовження."
    exit 1
fi

echo "🔄 Запуск PostgreSQL..."
docker run -d \
  --name ventai-postgres \
  -e POSTGRES_DB=ventai_dev \
  -e POSTGRES_USER=ventai_dev \
  -e POSTGRES_PASSWORD=ventai_dev_password \
  -p 5433:5432 \
  postgres:14

echo "🔄 Запуск Redis..."
docker run -d \
  --name ventai-redis \
  -p 6380:6379 \
  redis:7-alpine

echo "⏳ Чекаємо запуску сервісів..."
sleep 10

echo "🔍 Перевірка статусу сервісів..."
if docker ps | grep -q ventai-postgres; then
    echo "✅ PostgreSQL запущено"
else
    echo "❌ Помилка запуску PostgreSQL"
    exit 1
fi

if docker ps | grep -q ventai-redis; then
    echo "✅ Redis запущено"
else
    echo "❌ Помилка запуску Redis"
    exit 1
fi

echo ""
echo "🎉 Всі сервіси запущено успішно!"
echo "📊 PostgreSQL: localhost:5433"
echo "🔄 Redis: localhost:6380"
echo ""
echo "🔄 Тепер можна запустити міграцію бази даних:"
echo "   cd backend && python enterprise_migration.py"
echo ""
echo "🛑 Для зупинки сервісів:"
echo "   docker stop ventai-postgres ventai-redis"
echo "   docker rm ventai-postgres ventai-redis"
