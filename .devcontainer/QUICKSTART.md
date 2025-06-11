# 🚀 VentAI DevContainer - Быстрый старт

## Что было адаптировано

Devcontainer настроен под ваш конкретный проект VentAI со всеми особенностями:

### ✅ Автоматически настроено:
- **Python 3.11** с всеми ML/AI библиотеками
- **Node.js 18** для фронтенд разработки  
- **FastAPI + React** окружение
- **PostgreSQL + Redis** через Docker Compose
- **VS Code Extensions** для Python, TypeScript, тестирования
- **Интеграция с вашими скриптами**: `start-enterprise-services.sh`, `start-windsurf-integration.sh`, `run_tests.sh`

### 📁 Поддерживаемая структура:
```
ventai-app/
├── .devcontainer/          # ← Новая конфигурация
├── backend/               # ← Python/FastAPI код
├── frontend/              # ← React приложение  
├── src/                   # ← Общий код
├── tests/                 # ← Тесты
├── working_test.py        # ← Ваши тесты работают
├── run_tests.sh          # ← Интегрировано
├── start-enterprise-services.sh  # ← Интегрировано
└── start-windsurf-integration.sh # ← Интегрировано
```

## 🎬 Как запустить

### 1. Открыть в DevContainer
```bash
# В VS Code: 
# 1. Открыть папку проекта
# 2. VS Code предложит "Reopen in Container" 
# 3. Нажать "Reopen"
# 4. Дождаться установки (5-10 минут первый раз)
```

### 2. Быстрый старт всех сервисов
```bash
# Простой запуск (backend + frontend)
bash start-dev.sh

# С enterprise сервисами
bash start-dev.sh --enterprise

# С Windsurf интеграцией  