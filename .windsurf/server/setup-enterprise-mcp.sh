#!/bin/zsh

# 🚀 Windsurf Enterprise MCP Server Setup & Launch Script
# Автоматична конфігурація векторної системи з PostgreSQL і Redis

echo "🎯 WINDSURF ENTERPRISE MCP SERVER SETUP"
echo "========================================"

# Перевірка системних вимог
check_requirements() {
    echo "🔍 Перевірка системних вимог..."
    
    # Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js не встановлено. Встановіть Node.js 18+ для продовження."
        exit 1
    fi
    
    local node_version=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$node_version" -lt 18 ]; then
        echo "❌ Node.js версія $node_version < 18. Оновіть Node.js."
        exit 1
    fi
    
    # Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker не встановлено. Встановіть Docker для продовження."
        exit 1
    fi
    
    # Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo "❌ Docker Compose не встановлено."
        exit 1
    fi
    
    echo "✅ Системні вимоги виконано"
}

# Конфігурація середовища
setup_environment() {
    echo "🔧 Налаштування середовища..."
    
    # Створення .env файлу якщо не існує
    if [ ! -f .env ]; then
        echo "📝 Створення .env файлу..."
        cp .env.example .env
        
        # Генерація унікального access token
        local access_token="windsurf_$(date +%s)_$(openssl rand -hex 8)"
        sed -i "s/ACCESS_TOKEN=.*/ACCESS_TOKEN=$access_token/" .env
        
        echo "🔑 Згенеровано access token: $access_token"
    fi
    
    # Створення необхідних директорій
    mkdir -p logs data config
    mkdir -p init-db grafana/dashboards grafana/provisioning
    
    echo "✅ Середовище налаштовано"
}

# Ініціалізація бази даних
setup_database() {
    echo "🗄️ Налаштування PostgreSQL з векторним розширенням..."
    
    # Створення init script для PostgreSQL
    cat > init-db/01-init-vector.sql << 'EOF'
-- Ініціалізація векторного розширення для Windsurf
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Створення схеми для Windsurf
CREATE SCHEMA IF NOT EXISTS windsurf;

-- Надання прав користувачу
GRANT ALL PRIVILEGES ON SCHEMA windsurf TO ventai_dev;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA windsurf TO ventai_dev;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA windsurf TO ventai_dev;

-- Налаштування для українського пошуку
CREATE TEXT SEARCH CONFIGURATION ukrainian (COPY = simple);
EOF
    
    echo "✅ PostgreSQL конфігурацію створено"
}

# Конфігурація Redis
setup_redis() {
    echo "🔄 Налаштування Redis..."
    
    cat > redis.conf << 'EOF'
# Redis configuration для Windsurf Enterprise
port 6379
bind 0.0.0.0
timeout 300
keepalive 300

# Memory configuration
maxmemory 512mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Logging
loglevel notice
logfile ""

# Ukrainian locale support
# Character encoding
locale-archive /usr/lib/locale/locale-archive
EOF
    
    echo "✅ Redis конфігурацію створено"
}

# Встановлення залежностей
install_dependencies() {
    echo "📦 Встановлення Node.js залежностей..."
    
    if [ ! -d "node_modules" ]; then
        npm install
    else
        echo "✅ Залежності вже встановлені"
    fi
    
    echo "✅ Залежності встановлено"
}

# Збірка проекту
build_project() {
    echo "🔨 Збірка TypeScript проекту..."
    
    npm run build
    
    if [ $? -eq 0 ]; then
        echo "✅ Проект успішно зібрано"
    else
        echo "❌ Помилка збірки проекту"
        exit 1
    fi
}

# Запуск Docker сервісів
start_docker_services() {
    echo "🐳 Запуск Docker сервісів..."
    
    # Зупинка існуючих контейнерів
    docker-compose down 2>/dev/null || true
    
    # Запуск тільки основних сервісів
    docker-compose up -d postgres redis
    
    echo "⏳ Очікування запуску сервісів..."
    sleep 15
    
    # Перевірка статусу
    local postgres_status=$(docker-compose ps postgres | grep "Up" | wc -l)
    local redis_status=$(docker-compose ps redis | grep "Up" | wc -l)
    
    if [ "$postgres_status" -eq 1 ] && [ "$redis_status" -eq 1 ]; then
        echo "✅ Docker сервіси запущено успішно"
    else
        echo "❌ Помилка запуску Docker сервісів"
        docker-compose logs
        exit 1
    fi
}

# Тестування підключень
test_connections() {
    echo "🔌 Тестування підключень..."
    
    # Тест PostgreSQL
    local pg_test=$(docker exec windsurf-postgres pg_isready -U ventai_dev -d ventai_dev)
    if [[ $pg_test == *"accepting connections"* ]]; then
        echo "✅ PostgreSQL підключення успішне"
    else
        echo "❌ PostgreSQL підключення невдале"
        exit 1
    fi
    
    # Тест Redis
    local redis_test=$(docker exec windsurf-redis redis-cli ping)
    if [[ $redis_test == "PONG" ]]; then
        echo "✅ Redis підключення успішне"
    else
        echo "❌ Redis підключення невдале"
        exit 1
    fi
}

# Запуск MCP сервера
start_mcp_server() {
    echo "🚀 Запуск Windsurf Enterprise MCP Server..."
    
    # Завантаження змінних середовища
    source .env
    
    # Перевірка наявності OpenAI ключа
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
        echo "⚠️ OpenAI API ключ не налаштовано. Векторний пошук буде обмежений."
        echo "💡 Додайте OPENAI_API_KEY в .env файл для повної функціональності."
    fi
    
    # Запуск у режимі розробки або продакшн
    if [ "$1" = "dev" ]; then
        echo "🔧 Запуск у режимі розробки..."
        npm run dev
    else
        echo "🏭 Запуск у продакшн режимі..."
        npm start
    fi
}

# Створення початкової документації
create_documentation() {
    echo "📚 Створення документації..."
    
    cat > README.md << 'EOF'
# 🚀 Windsurf Enterprise MCP Server

## Векторна система з PostgreSQL + Redis інтеграцією

### Можливості
- 🔍 **Векторний пошук** документів з AI embeddings
- 🕸️ **Графові зв'язки** між завданнями та документами  
- 📊 **Розумні рекомендації** на основі контексту
- 🔄 **Автоматична синхронізація** з файловою системою
- 📈 **Аналітика та моніторинг** операцій

### Швидкий старт
```bash
# Запуск всіх сервісів
./setup-enterprise-mcp.sh

# Запуск у режимі розробки
./setup-enterprise-mcp.sh dev
```

### Архітектура
- **PostgreSQL** з pgvector для векторного пошуку
- **Redis** для кешування та швидкого доступу
- **OpenAI** для генерації embeddings (опціонально)
- **MCP Protocol** для інтеграції з AI асистентами

### Інструменти
- `vector_search_documents` - Семантичний пошук
- `smart_recommendations` - AI рекомендації
- `graph_relations` - Дослідження зв'язків
- `sync_to_vector_store` - Синхронізація файлів

### Моніторинг
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Logs: `./logs/windsurf-mcp.log`
EOF
    
    echo "✅ Документацію створено"
}

# Виведення статусу
show_status() {
    echo ""
    echo "🎉 WINDSURF ENTERPRISE MCP SERVER ГОТОВИЙ!"
    echo "=========================================="
    echo ""
    echo "🔗 Підключення:"
    echo "  PostgreSQL: localhost:5433"
    echo "  Redis: localhost:6380"
    echo "  MCP Server: stdio protocol"
    echo ""
    echo "📊 Моніторинг:"
    echo "  Grafana: http://localhost:3000 (admin/windsurf_admin)"
    echo "  Prometheus: http://localhost:9090"
    echo ""
    echo "📁 Файли:"
    echo "  Конфігурація: .env"
    echo "  Логи: ./logs/"
    echo "  Дані: ./data/"
    echo ""
    echo "🛠️ Керування:"
    echo "  Зупинка: docker-compose down"
    echo "  Логи: docker-compose logs -f"
    echo "  Перезапуск: docker-compose restart"
    echo ""
    echo "🚀 Тепер можна інтегрувати з Claude Desktop або VS Code!"
}

# Основна функція
main() {
    echo "Початок налаштування Windsurf Enterprise MCP Server..."
    
    check_requirements
    setup_environment  
    setup_database
    setup_redis
    install_dependencies
    build_project
    start_docker_services
    test_connections
    create_documentation
    
    # Запуск MCP сервера
    if [ "$1" = "setup-only" ]; then
        echo "✅ Налаштування завершено. Запустіть сервер: npm start"
    else
        start_mcp_server "$1"
    fi
    
    show_status
}

# Обробка аргументів командного рядка
case "$1" in
    "dev")
        main "dev"
        ;;
    "setup-only")
        main "setup-only"
        ;;
    "help"|"-h"|"--help")
        echo "Використання: $0 [dev|setup-only|help]"
        echo "  dev        - Запуск у режимі розробки"
        echo "  setup-only - Тільки налаштування без запуску"
        echo "  help       - Показати це повідомлення"
        ;;
    *)
        main
        ;;
esac
