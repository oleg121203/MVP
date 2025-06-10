# 🎯 Windsurf Enterprise MCP Server - Керівництво з використання

## ✅ Поточний статус
Сервер успішно виправлений і працює! Всі async/await проблеми вирішені.

## 🚀 Як запустити MCP сервер

### 1. Локальний запуск (Development)

```bash
# Перейти до директорії сервера
cd /Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server

# Запустити Redis на правильному порту
redis-server --port 6380 --daemonize yes

# Перевірити PostgreSQL (має працювати на порту 5433)
nc -z localhost 5433

# Запустити MCP сервер зі змінними середовища
REDIS_URL="redis://localhost:6380" \
DATABASE_URL="postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev" \
node dist/enterprise-index.js

# АБО використати стартовий скрипт
./start-mcp.sh
```

### 2. Підключення до Claude Desktop

Додайте в конфігурацію Claude Desktop (`~/.config/claude-desktop/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "windsurf-enterprise": {
      "command": "node",
      "args": ["/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server/dist/enterprise-index.js"],
      "env": {
        "REDIS_URL": "redis://localhost:6380",
        "DATABASE_URL": "postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev",
        "WINDSURF_ROOT": "/Users/olegkizyma/workspaces/MVP/ventai-app",
        "ENABLE_VECTOR_SEARCH": "true",
        "ENABLE_GRAPH_RELATIONS": "true"
      }
    }
  }
}
```

### 3. Docker розгортання (Production)

```bash
# Запустити повний стек
docker-compose up -d

# Перевірити статус
docker-compose ps

# Логи
docker-compose logs windsurf-mcp
```

## 🛠️ Доступні інструменти MCP

Після підключення в Claude Desktop ви матимете доступ до:

1. **Файлові операції:**
   - `read_file` - Читання файлів
   - `write_file` - Запис файлів
   - `create_directory` - Створення директорій
   - `list_directory` - Перегляд вмісту директорій

2. **Векторний пошук:**
   - `vector_search` - Пошук по змісту документів
   - `smart_recommendations` - Розумні рекомендації
   - `graph_connections` - Графові зв'язки між документами

3. **Windsurf інтеграція:**
   - `sync_windsurf_files` - Синхронізація файлів
   - `search_windsurf_docs` - Пошук в документації
   - `get_project_structure` - Структура проєкту

## 🔄 Як працює в чаті (як Windsurf)

Після підключення MCP сервера до Claude Desktop, ви можете:

```
Користувач: "Знайди всі файли TypeScript з помилками"
Claude: *використовує read_file та vector_search*

Користувач: "Створи компонент React для аналітики"
Claude: *використовує write_file та create_directory*

Користувач: "Покажи зв'язки між модулями"
Claude: *використовує graph_connections*
```

## 📊 Моніторинг

Перевірити статус сервісів:
```bash
# Redis
redis-cli -p 6380 ping

# PostgreSQL
nc -z localhost 5433

# MCP Server logs
tail -f logs/windsurf-mcp.log
```

## 🔧 Налаштування для різних середовищ

### Development
```bash
export NODE_ENV=development
export DEBUG=windsurf:*
```

### Production
```bash
export NODE_ENV=production
export MCP_LOG_LEVEL=info
```

### Kubernetes
```bash
kubectl apply -f deployment/kubernetes/
```

## 🎉 Результат

Тепер у вас є повнофункціональний Enterprise MCP сервер, який:
- ✅ Працює без async/await помилок
- ✅ Підключається до Redis (6380) та PostgreSQL (5433)
- ✅ Підтримує векторний пошук
- ✅ Має графові зв'язки між документами
- ✅ Інтегрується з Claude Desktop
- ✅ Готовий до масштабованого розгортання

## 🌟 Переваги порівняно з Windsurf

1. **Векторний пошук** - Розумний пошук по змісту
2. **Графові зв'язки** - Розуміння залежностей між файлами
3. **PostgreSQL + Redis** - Надійне зберігання та кешування
4. **Enterprise функції** - Аудит, безпека, масштабування
5. **Docker підтримка** - Легке розгортання
