# Переход на PostgreSQL и Redis в VentAI

Эта документация описывает интеграцию PostgreSQL и Redis в систему VentAI и необходимые шаги для настройки системы.

## Обзор изменений

1. **PostgreSQL интеграция**
   - Обновлена конфигурация базы данных для использования PostgreSQL
   - Добавлены оптимизированные настройки для соединения с PostgreSQL
   - Создан скрипт миграции для переноса данных из SQLite в PostgreSQL

2. **Redis интеграция**
   - Добавлена библиотека для работы с Redis
   - Создан модуль redis_handler.py для работы с Redis
   - Добавлено кэширование API-запросов с использованием fastapi-cache
   - Интегрирован мониторинг состояния Redis в health-check

## Необходимые зависимости

Добавлены следующие зависимости:
- `psycopg2-binary==2.9.9` - драйвер PostgreSQL
- `redis==5.0.1` - клиент Redis
- `fastapi-cache2[redis]==0.2.1` - кэширование для FastAPI
- `psutil==7.0.0` - для демонстрационного API кэширования

## Конфигурация

### PostgreSQL

Для конфигурации PostgreSQL необходимо установить переменную окружения `DATABASE_URL` или изменить значение в файле `.env`:

```env
DATABASE_URL=postgresql://ventai_user:ventai_password@postgres:5432/ventai_db
```

### Redis

Для конфигурации Redis необходимо установить переменную окружения `REDIS_URL` или изменить значение в файле `.env`:

```env
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=ваш_пароль  # Опционально
```

## Миграция данных

Для переноса данных из SQLite в PostgreSQL используйте скрипт миграции:

```bash
cd /workspace/ventai-app/backend/src
python simple_migrate.py
```

Для более сложных случаев можно использовать:

```bash
python migrate_to_postgres.py --sqlite-db ./ventai.db --reset-postgres
```

## Docker-конфигурация

В режиме разработки Docker Compose уже настроен для запуска PostgreSQL и Redis. Для запуска всего окружения:

```bash
docker-compose up -d postgres redis backend
```

## Запуск сервера с новой конфигурацией

Для запуска сервера с новой конфигурацией можно использовать скрипт:

```bash
cd /workspace/ventai-app/backend
./start_postgres_redis_server.sh
```

Или запустить сервер вручную:

```bash
cd /workspace/ventai-app/backend/src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Проверка работоспособности

После запуска системы можно проверить статус компонентов:

- API Health Check: http://localhost:8000/health
- Redis Status: http://localhost:8000/api/redis-status
- Cached Statistics (пример кэширования): http://localhost:8000/api/cached-statistics

## Использование Redis в коде

Пример использования Redis для кэширования:

```python
from fastapi_cache.decorator import cache

@app.get("/api/example")
@cache(expire=60)  # Кэшировать на 60 секунд
async def cached_endpoint():
    # Дорогостоящая операция
    return result
```

Пример прямого использования Redis:

```python
from redis_handler import redis_handler

# Сохранение в кэш
redis_handler.set_cache("my_key", data, expiration=3600)

# Получение из кэша
data = redis_handler.get_cache("my_key")
```

## Работа с сессиями через Redis

Для работы с сессиями можно использовать методы Redis Handler:

```python
from redis_handler import redis_handler

# Сохранение сессии
session_id = str(uuid.uuid4())
session_data = {"user_id": user_id, "timestamp": datetime.now().isoformat()}
redis_handler.store_session(session_id, session_data, expiration=3600)

# Получение сессии
session = redis_handler.get_session(session_id)
if session:
    user_id = session.get("user_id")
```

## Мониторинг Redis

Для мониторинга состояния Redis можно использовать:

```bash
curl http://localhost:8000/api/redis-status
```

Ответ будет содержать информацию о состоянии Redis:

```json
{
  "status": "available",
  "connected": true,
  "version": "7.4.4",
  "memory_usage": "1007.41K",
  "clients_connected": 2
}
```

## Дополнительная информация

- Redis использует базу данных 0 по умолчанию
- Все кэши имеют префикс "ventai-cache:"
- Время жизни кэша по умолчанию: 3600 секунд (1 час)
- При запросе к cached API Redis автоматически кэширует ответ на указанное время
- Система проверки здоровья (health check) теперь включает проверку состояния Redis
