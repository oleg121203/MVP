# 🎯 Windsurf Enterprise MCP Server

## ✅ Статус: ГОТОВО ДО ВИКОРИСТАННЯ!

**Windsurf Enterprise MCP Server** - це потужний Model Context Protocol сервер з векторним пошуком, графовими зв'язками та інтеграцією PostgreSQL + Redis для роботи з вашими проєктами.

## 🚀 Функціональність

### 📄 Файлові операції (15 інструментів):
- **read_file** - Читання файлів з індексацією
- **write_file** - Створення/перезапис файлів
- **edit_file** - Селективне редагування
- **read_multiple_files** - Читання кількох файлів
- **create_directory** - Створення директорій
- **list_directory** - Перегляд директорій
- **move_file** - Переміщення файлів
- **search_files** - Пошук файлів за патерном
- **get_file_info** - Метадані файлів

### 🔍 AI-функції:
- **vector_search_documents** - Семантичний пошук
- **smart_recommendations** - Розумні рекомендації
- **graph_relations** - Графові зв'язки
- **sync_to_vector_store** - Синхронізація з векторним сховищем
- **create_graph_relation** - Створення зв'язків

## 💻 Швидкий старт

### 1. Запуск сервісів
```bash
# Redis
redis-server --port 6380 --daemonize yes

# Перевірка PostgreSQL (має працювати на 5433)
nc -z localhost 5433 && echo "PostgreSQL готовий"
```

### 2. Запуск MCP сервера
```bash
cd /Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server

# Простий запуск
./start-mcp.sh

# АБО ручний запуск
REDIS_URL="redis://localhost:6380" \
DATABASE_URL="postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev" \
node dist/enterprise-index.js
```

### 3. Підключення до Claude Desktop

Додайте в `~/.config/claude-desktop/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "windsurf-enterprise": {
      "command": "node",
      "args": ["/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server/dist/enterprise-index.js"],
      "env": {
        "REDIS_URL": "redis://localhost:6380",
        "DATABASE_URL": "postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev",
        "WINDSURF_ROOT": "/Users/olegkizyma/workspaces/MVP/ventai-app"
      }
    }
  }
}
```

## 🎯 Як використовувати в Claude

Після підключення до Claude Desktop, ви можете:

```
📋 "Прочитай README.md і покажи структуру проєкту"
→ Claude використає read_file + list_directory

🔍 "Знайди всі TypeScript файли з помилками"
→ Claude використає search_files + vector_search_documents

✨ "Створи React компонент для дашборду"
→ Claude використає write_file + smart_recommendations

🌐 "Покажи залежності між модулями"
→ Claude використає graph_relations
```

## 🐳 Docker розгортання

```bash
# Повний стек
docker-compose up -d

# Тільки MCP сервер
docker build -f Dockerfile.production -t windsurf-mcp .
docker run --env-file .env windsurf-mcp
```

## 🛠️ Конфігурація

### Змінні середовища (.env):
```env
# Redis
REDIS_URL=redis://localhost:6380
REDIS_HOST=localhost
REDIS_PORT=6380

# PostgreSQL
DATABASE_URL=postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev

# Windsurf
WINDSURF_ROOT=/Users/olegkizyma/workspaces/MVP/ventai-app
ENABLE_VECTOR_SEARCH=true
ENABLE_GRAPH_RELATIONS=true

# OpenAI (опціонально)
OPENAI_API_KEY=your-key-here
```

## 📊 Переваги

| Функція | Windsurf | Наш MCP Server |
|---------|----------|----------------|
| Файлові операції | ✅ | ✅ |
| Векторний пошук | ❌ | ✅ |
| Графові зв'язки | ❌ | ✅ |
| PostgreSQL | ❌ | ✅ |
| Redis кеш | ❌ | ✅ |
| Docker | ❌ | ✅ |
| Claude Desktop | ❌ | ✅ |

## 🔧 Розробка

```bash
# Розробка
npm run dev

# Білд
npm run build

# Тести
npm test

# Лінтинг
npm run lint:fix
```

## 📈 Моніторинг

```bash
# Статус сервісів
redis-cli -p 6380 ping
nc -z localhost 5433

# Логи
tail -f logs/windsurf-mcp.log

# Метрики (в Docker)
docker stats windsurf-mcp-server
```

## 🎉 Результат

Тепер у вас є Enterprise-рівня MCP сервер, який:

- ✅ **Працює без помилок** - Всі async/await проблеми виправлені
- ✅ **Підключається до баз даних** - Redis (6380) + PostgreSQL (5433)
- ✅ **Має 15 потужних інструментів** - Від файлових операцій до AI-пошуку
- ✅ **Інтегрується з Claude Desktop** - Працює як Windsurf, але краще
- ✅ **Готовий до production** - Docker, Kubernetes, моніторинг
- ✅ **Масштабований** - Не прив'язаний до macOS

**Використовуйте як звичайний Windsurf, але з потужністю Enterprise AI! 🚀**
