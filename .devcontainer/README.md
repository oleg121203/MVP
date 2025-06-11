# VentAI Development Container

Этот devcontainer настроен для разработки полнофункционального приложения VentAI со всеми необходимыми зависимостями и инструментами.

## 🚀 Что включено

### Языки и Runtime
- **Python 3.11** с полным набором ML/AI библиотек
- **Node.js 18** для фронтенд разработки
- **TypeScript** поддержка

### Основные инструменты
- **FastAPI** - для backend API
- **React.js** - для frontend
- **PostgreSQL** - основная база данных
- **Redis** - кэширование и очереди
- **Docker** - контейнеризация

### VS Code Extensions
- Python разработка (PyLint, Black, Pytest)
- TypeScript/React разработка
- Jupyter Notebooks
- Git интеграция
- Thunder Client (тестирование API)
- PostgreSQL клиент

## 📦 Структура проекта

```
ventai-app/
├── .devcontainer/          # Конфигурация Dev Container
│   ├── devcontainer.json   # Основная конфигурация
│   ├── setup.sh           # Скрипт установки зависимостей
│   └── docker-compose.yml # Внешние сервисы (PostgreSQL, Redis)
├── backend/               # Python/FastAPI backend
├── frontend/              # React frontend
├── src/                   # Общий исходный код
├── tests/                 # Тесты
└── docs/                  # Документация
```

## 🛠 Начало работы

### 1. Открытие в Dev Container

1. Установите VS Code и расширение "Dev Containers"
2. Откройте папку проекта в VS Code
3. VS Code предложит "Reopen in Container" - нажмите "Reopen"
4. Дождитесь полной установки (может занять 5-10 минут при первом запуске)

### 2. Запуск сервисов

После открытия контейнера у вас есть несколько вариантов:

#### Автоматический запуск (рекомендуется)
```bash
bash start-dev.sh
```

#### Ручной запуск

**Backend (FastAPI):**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (React):**
```bash
cd frontend && npm start
```

**Внешние сервисы:**
```bash
docker-compose -f .devcontainer/docker-compose.yml up -d
```

### 3. Использование VS Code Tasks

1. Нажмите `Ctrl+Shift+P` (или `Cmd+Shift+P` на Mac)
2. Введите "Tasks: Run Task"
3. Выберите нужную задачу:
   - **Start Backend** - запуск FastAPI сервера
   - **Start Frontend** - запуск React приложения
   - **Run Tests** - запуск всех тестов
   - **Install Dependencies** - переустановка зависимостей

## 🌐 Доступные порты

После запуска контейнера будут доступны следующие сервисы:

| Сервис | Порт | URL | Описание |
|--------|------|-----|----------|
| **Frontend** | 3000 | http://localhost:3000 | React приложение |
| **Backend API** | 8000 | http://localhost:8000 | FastAPI сервер |
| **API Docs** | 8000 | http://localhost:8000/docs | Swagger UI |
| **PostgreSQL** | 5432 | localhost:5432 | База данных |
| **Redis** | 6379 | localhost:6379 | Кэш и очереди |
| **pgAdmin** | 5050 | http://localhost:5050 | PostgreSQL веб-интерфейс |
| **Redis Commander** | 8081 | http://localhost:8081 | Redis веб-интерфейс |

## 🧪 Тестирование

### Запуск тестов
```bash
# Все тесты
pytest

# Тесты с покрытием
pytest --cov=backend --cov-report=html

# Только frontend тесты
npm test

# Интеграционные тесты
pytest tests/integration/
```

### Тестирование API
- Используйте **Thunder Client** в VS Code
- Или откройте http://localhost:8000/docs для Swagger UI
- Базовый endpoint: http://localhost:8000/

## 📊 Базы данных

### PostgreSQL
- **Host:** localhost (или postgres в docker)
- **Port:** 5432
- **Database:** ventai
- **Username:** postgres
- **Password:** postgres

### Redis
- **Host:** localhost (или redis в docker)
- **Port:** 6379
- **No password** (development setup)

## 🔧 Полезные команды

```bash
# Просмотр логов сервисов
docker-compose -f .devcontainer/docker-compose.yml logs

# Перезапуск сервисов
docker-compose -f .devcontainer/docker-compose.yml restart

# Остановка всех сервисов
docker-compose -f .devcontainer/docker-compose.yml down

# Установка новых Python пакетов
pip install package_name

# Установка новых npm пакетов
cd frontend && npm install package_name

# Обновление зависимостей
bash .devcontainer/setup.sh
```

## 🐛 Troubleshooting

### Проблемы с запуском
1. **Порты заняты:** Убедитесь что порты 3000, 8000, 5432, 6379 свободны
2. **Медленный старт:** Первый запуск может занять время на скачивание образов
3. **Ошибки Python:** Проверьте `PYTHONPATH` в терминале: `echo $PYTHONPATH`

### Сброс окружения
```bash
# Полная переустановка зависимостей
bash .devcontainer/setup.sh

# Пересборка контейнера
# Ctrl+Shift+P -> "Dev Containers: Rebuild Container"
```

### Проблемы с базой данных
```bash
# Перезапуск PostgreSQL
docker-compose -f .devcontainer/docker-compose.yml restart postgres

# Создание базы данных заново
docker-compose -f .devcontainer/docker-compose.yml down -v
docker-compose -f .devcontainer/docker-compose.yml up -d
```

## 📈 Дальнейшие шаги

1. **Настройте CI/CD:** Добавьте GitHub Actions или GitLab CI
2. **Конфигурация production:** Создайте отдельные файлы для production
3. **Мониторинг:** Добавьте Prometheus/Grafana для мониторинга
4. **Безопасность:** Настройте proper secrets management

## 🤝 Поддержка

Если у вас есть вопросы или проблемы:
1. Проверьте этот README
2. Изучите логи: `docker-compose logs`
3. Создайте issue в репозитории
4. Обратитесь к команде разработки

---

**Приятной разработки! 🚀**
