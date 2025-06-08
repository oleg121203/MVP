# VentAI MVP

VentAI - это инновационная платформа для управления проектами с помощью ИИ, которая помогает командам автоматизировать рутинные задачи и принимать более обоснованные решения.

## ✅ Статус проекта

🎉 **Полностью настроен и готов к разработке!**

- ✅ Universal Dev-Container настроен
- ✅ Backend (FastAPI) работает на порту 8000
- ✅ Frontend (React) работает на порту 3000
- ✅ Все зависимости установлены
- ✅ Среда разработки протестирована

## 🚀 Быстрый старт

### Предварительные требования
- Visual Studio Code с расширением Dev Containers
- Docker

### Запуск
1. Откройте проект в VS Code
2. При появлении уведомления нажмите "Reopen in Container"
3. Дождитесь настройки окружения (автоматически)
4. Запустите разработку:
   ```bash
   npm run dev
   ```

## 🔧 Доступные команды

- `npm run dev` - запуск backend и frontend в режиме разработки
- `npm run test:setup` - проверка настройки окружения
- `npm run dev:backend` - запуск только backend
- `npm run dev:frontend` - запуск только frontend

## 🌐 URL-адреса

- **Frontend**: http://localhost:3000 (React приложение)
- **Backend API**: http://localhost:8000 (FastAPI)
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

## 📁 Структура проекта

```
MVP/
├── .devcontainer/          # Настройки Dev-Container
│   ├── devcontainer.json  # Конфигурация контейнера
│   └── setup.sh          # Скрипт настройки окружения
├── backend/               # FastAPI backend
│   ├── main.py           # Основное приложение
│   ├── requirements.txt  # Python зависимости
│   └── .env             # Переменные окружения
├── frontend/             # React frontend
│   ├── src/             # Исходный код
│   ├── public/          # Статические файлы
│   └── .env.local       # Переменные окружения
├── package.json         # Node.js конфигурация
├── test-setup.py        # Тест настройки окружения
└── README.md           # Документация
```

## 🧪 Тестирование

Проверить настройку окружения:
```bash
npm run test:setup
```

Результат должен показать: **"🎉 All tests passed! Development environment is ready."**

## 🔧 Технические детали

### Backend (FastAPI)
- Python 3.12.1
- FastAPI с автоматической перезагрузкой
- Uvicorn сервер
- Swagger документация включена

### Frontend (React)
- Node.js 20.19.0
- Create React App
- Hot reload включен
- Порт 3000

### Dev-Container
- Universal контейнер Microsoft
- Автоматическая установка зависимостей
- Python и Node.js предустановлены

## 🚀 Деплой на production

Для production деплоя на Linux серверах:
1. Установите Docker и Docker Compose
2. Скопируйте проект на сервер
3. Настройте production переменные окружения
4. Используйте systemd или supervisor для управления процессами

## 🛠️ Разработка

Проект готов к разработке! Начните с:
1. Запуска `npm run dev`
2. Открытия http://localhost:3000 для frontend
3. Просмотра API документации на http://localhost:8000/docs
4. Редактирования кода - изменения применяются автоматически

---

**Последнее обновление**: Проект полностью настроен и протестирован ✅


