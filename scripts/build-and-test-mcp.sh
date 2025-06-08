#!/bin/bash
# Скрипт для перебудови контейнерів та тестування MCP сервера

set -e

# Кольори для виводу
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функції для логування
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Функція очистки при помилці
cleanup() {
    log_warning "Очистка ресурсів..."
    docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans || true
}

# Trap для cleanup
trap cleanup ERR INT TERM

echo "🚀 VentAI MCP Container Build & Test Script"
echo "=============================================="

# Перевірка наявності необхідних файлів
log_info "Перевірка файлів проекту..."

required_files=(
    "docker-compose.dev.yml"
    "mcp_server.py"
    "mcp_ai_providers.py"
    "backend/requirements.txt"
    "backend/Dockerfile.dev"
    "test_mcp_container.py"
)

for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        log_error "Відсутній файл: $file"
        exit 1
    fi
done

log_success "Всі необхідні файли знайдено"

# Перевірка змінних середовища
log_info "Перевірка змінних середовища..."

# Створюємо .env файл якщо його немає
if [[ ! -f ".env" ]]; then
    log_warning ".env файл не знайдено, створюємо базовий..."
    cat > .env << EOF
# AI API Keys (додайте справжні ключі)
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
PINECONE_API_KEY=your-pinecone-api-key-here
HUBSPOT_API_KEY=your-hubspot-api-key-here

# Ollama Configuration
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1

# AI Models
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Pinecone
PINECONE_ENVIRONMENT=us-west1-gcp

# Costs
LABOR_COST_PER_HOUR=50.0
ENERGY_COST_PER_KWH=0.12
EOF
    log_warning "Створено .env файл з заглушками. Додайте справжні API ключі!"
fi

# Зупинка існуючих контейнерів
log_info "Зупинка існуючих контейнерів..."
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans || true

# Очистка старих образів
log_info "Очистка старих образів..."
docker images | grep ventai | grep dev | awk '{print $3}' | xargs -r docker rmi -f || true

# Перебудова контейнерів
log_info "Перебудова контейнерів..."
if ! docker-compose -f docker-compose.dev.yml build --no-cache; then
    log_error "Помилка перебудови контейнерів"
    exit 1
fi

log_success "Контейнери перебудовано"

# Запуск контейнерів
log_info "Запуск контейнерів..."
if ! docker-compose -f docker-compose.dev.yml up -d; then
    log_error "Помилка запуску контейнерів"
    exit 1
fi

log_success "Контейнери запущено"

# Очікування готовності сервісів
log_info "Очікування готовності сервісів..."

max_wait=120
wait_time=0

while [ $wait_time -lt $max_wait ]; do
    # Перевіряємо PostgreSQL
    if docker-compose -f docker-compose.dev.yml exec -T db pg_isready -U ventai_dev -d ventai_dev >/dev/null 2>&1; then
        log_success "PostgreSQL готовий"
        break
    fi
    
    sleep 2
    wait_time=$((wait_time + 2))
    echo -n "."
done

if [ $wait_time -ge $max_wait ]; then
    log_error "Таймаут очікування PostgreSQL"
    docker-compose -f docker-compose.dev.yml logs db
    exit 1
fi

# Очікування Backend
log_info "Очікування Backend сервісу..."
max_wait=60
wait_time=0

while [ $wait_time -lt $max_wait ]; do
    if curl -f http://localhost:8000/docs >/dev/null 2>&1; then
        log_success "Backend готовий"
        break
    fi
    
    sleep 2
    wait_time=$((wait_time + 2))
    echo -n "."
done

if [ $wait_time -ge $max_wait ]; then
    log_warning "Backend не відповідає, але продовжуємо..."
fi

# Очікування MCP сервера
log_info "Очікування MCP сервера..."
max_wait=60
wait_time=0

while [ $wait_time -lt $max_wait ]; do
    if curl -f http://localhost:8001/health >/dev/null 2>&1; then
        log_success "MCP сервер готовий"
        break
    fi
    
    sleep 2
    wait_time=$((wait_time + 2))
    echo -n "."
done

if [ $wait_time -ge $max_wait ]; then
    log_error "MCP сервер не відповідає"
    log_info "Перевіряємо логи MCP сервера..."
    docker-compose -f docker-compose.dev.yml logs mcp-server
    exit 1
fi

# Показуємо статус контейнерів
log_info "Статус контейнерів:"
docker-compose -f docker-compose.dev.yml ps

# Запуск тестування
log_info "Запуск тестування MCP сервера..."

if python3 test_mcp_container.py; then
    log_success "Тестування пройшло успішно!"
    
    echo ""
    echo "🎉 VentAI MCP сервер готовий до роботи!"
    echo "=============================================="
    echo "📋 Доступні сервіси:"
    echo "   🔗 MCP Server Health: http://localhost:8001/health"
    echo "   📊 MCP Server Status: http://localhost:8001/status"
    echo "   🛠  MCP Capabilities: http://localhost:8001/capabilities"
    echo "   🌐 Backend API: http://localhost:8000/docs"
    echo "   🖥  Frontend: http://localhost:3000"
    echo ""
    echo "🤖 Для роботи з Claude 4:"
    echo "   1. Використовуйте конфігурацію з .vscode/mcp.json"
    echo "   2. Переконайтеся що Claude 4 має доступ до MCP серверів"
    echo "   3. Тестуйте запити типу 'Проаналізуй HVAC систему для офісу 100м²'"
    echo ""
    echo "📖 Документація: .vscode/MCP_README.md"
    echo "🔧 Налаштування: .vscode/MCP_ROLE_EXPLANATION.md"
    
else
    log_error "Тестування не пройшло"
    
    echo ""
    echo "🔍 Діагностика проблем:"
    echo "=============================================="
    
    # Показуємо логи проблемних сервісів
    log_info "Логи MCP сервера:"
    docker-compose -f docker-compose.dev.yml logs --tail=20 mcp-server
    
    echo ""
    log_info "Логи Backend:"
    docker-compose -f docker-compose.dev.yml logs --tail=20 backend
    
    echo ""
    log_info "Статус контейнерів:"
    docker-compose -f docker-compose.dev.yml ps
    
    echo ""
    log_warning "Для діагностики використовуйте:"
    echo "   docker-compose -f docker-compose.dev.yml logs [service_name]"
    echo "   docker-compose -f docker-compose.dev.yml exec [service_name] bash"
    
    exit 1
fi

# Опції для користувача
echo ""
echo "🎛  Управління:"
echo "   🔄 Перезапуск: docker-compose -f docker-compose.dev.yml restart"
echo "   🛑 Зупинка: docker-compose -f docker-compose.dev.yml down"
echo "   📜 Логи: docker-compose -f docker-compose.dev.yml logs -f [service]"
echo "   🧪 Повторне тестування: python3 test_mcp_container.py"

log_success "Скрипт завершено успішно!"
