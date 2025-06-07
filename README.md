# VentAI - Professional HVAC Platform

## Огляд

VentAI - це професійна платформа для розрахунків та проектування систем вентиляції з інтеграцією AI технологій.

## Архітектура

```
ventai-app/
├── frontend/           # React фронтенд додаток
├── backend/           # Python FastAPI бекенд
├── docs/              # Документація проекту
├── tests/             # Тести всіх компонентів
├── deployment/        # Docker та деплой конфігурації
└── config/            # Конфігураційні файли
```

## Швидкий старт

```bash
# Встановлення залежностей
npm run install:all

# Запуск в режимі розробки
npm run dev

# Запуск з Docker
npm run docker:dev
```

## База данных

VentAI поддерживает две конфигурации баз данных:
- **SQLite** - для быстрой разработки и тестирования
- **PostgreSQL** - для продакшн развертывания и продвинутой разработки

### Переход на PostgreSQL и Redis

Для запуска с PostgreSQL и Redis:

```bash
# Запуск PostgreSQL и Redis в Docker
./start-db-services.sh

# Запуск сервера с PostgreSQL и Redis
cd backend
./start_postgres_redis_server.sh
```

Подробная информация о миграции на PostgreSQL и Redis находится в [docs/POSTGRES_REDIS_INTEGRATION.md](docs/POSTGRES_REDIS_INTEGRATION.md)

## Можливості

- **HVAC розрахунки** - Повний набір інженерних розрахунків
- **AI інтеграція** - Інтелектуальні підказки та автоматизація
- **Responsive дизайн** - Робота на всіх пристроях
- **Звітність** - Генерація професійних звітів
- **Безпека** - Сучасні методи аутентифікації

## Розробка

Детальна інформація по розробці знаходиться в [docs/development](docs/development/).

## Документація

- [API Documentation](docs/api/)
- [User Guide](docs/user-guide/)
- [Architecture](docs/architecture/)

## Troubleshooting

### Docker Build Issues
1. If seeing 'path not found' errors:
   ```bash
   docker system prune -a -f --volumes
   rm -rf deployment/docker/.cache
   ```
2. Rebuild with:
   ```bash
   docker-compose -f docker-compose.yml -f deployment/docker/docker-compose.dev.yml up --build
   ```

### Missing Frontend Files
- Ensure `src/index.js` exists with basic React render setup
- Verify all dependencies are installed (`npm install`)

---

**Версія**: 2.0.0 - Reorganized Architecture
