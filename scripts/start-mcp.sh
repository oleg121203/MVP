#!/bin/bash

# VentAI MCP Server Startup Script
# Налаштування для роботи з Claude 4

set -e

echo "🚀 Starting VentAI MCP Environment for Claude 4..."

PROJECT_ROOT="/Users/olegkizyma/workspaces/MVP/ventai-app"
cd "$PROJECT_ROOT"

# Функція для кольорового виводу
print_status() {
    local status=$1
    local message=$2
    case $status in
        "success") echo "✅ $message" ;;
        "warning") echo "⚠️  $message" ;;
        "error") echo "❌ $message" ;;
        "info") echo "ℹ️  $message" ;;
        *) echo "$message" ;;
    esac
}

# Перевірка наявності необхідних файлів
print_status "info" "Checking MCP configuration files..."

required_files=(
    ".vscode/mcp.json"
    ".vscode/mcp-config.json"
    "mcp_server.py"
    "test_mcp.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "success" "$file exists"
    else
        print_status "error" "$file missing"
        exit 1
    fi
done

# Завантаження змінних середовища
env_files=(".env.development" ".env.mcp" ".env")
for env_file in "${env_files[@]}"; do
    if [ -f "$env_file" ]; then
        source "$env_file"
        print_status "success" "Loaded environment from $env_file"
        break
    fi
done

# Експорт необхідних змінних
export VENTAI_PROJECT_ROOT="$PROJECT_ROOT"
export PYTHONPATH="$PROJECT_ROOT/backend/src"
export MCP_LOG_LEVEL="${MCP_LOG_LEVEL:-INFO}"
export APP_ENV="${APP_ENV:-development}"

# Функція для перевірки запущених сервісів
check_service() {
    local service_name=$1
    local port=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_status "success" "$service_name is running on port $port"
        return 0
    else
        print_status "warning" "$service_name is not running on port $port"
        return 1
    fi
}

# Функція для запуску сервісу в фоні
start_service() {
    local service_name=$1
    local command=$2
    local log_file=$3
    local port=$4
    
    if check_service "$service_name" "$port"; then
        return 0
    fi
    
    print_status "info" "Starting $service_name..."
    nohup $command > "$log_file" 2>&1 &
    
    # Очікування запуску сервісу
    local wait_time=0
    while [ $wait_time -lt 30 ]; do
        if check_service "$service_name" "$port"; then
            print_status "success" "$service_name started successfully"
            return 0
        fi
        sleep 2
        wait_time=$((wait_time + 2))
    done
    
    print_status "error" "Failed to start $service_name after 30 seconds"
    return 1
}

# Перевірка та запуск Docker сервісів
print_status "info" "Checking Docker services..."

if ! docker info >/dev/null 2>&1; then
    print_status "warning" "Docker is not running. Please start Docker Desktop."
else
    # Запуск PostgreSQL і Redis
    if [ -f "docker-compose.dev.yml" ]; then
        print_status "info" "Starting database services..."
        docker-compose -f docker-compose.dev.yml up -d postgres redis
        sleep 5
    elif [ -f "docker-compose-db.yml" ]; then
        print_status "info" "Starting database services..."
        docker-compose -f docker-compose-db.yml up -d
        sleep 5
    fi
fi

# Перевірка сервісів бази даних
check_service "PostgreSQL" 5433 || print_status "warning" "Start with: ./start-db-services.sh"
check_service "Redis" 6380 || print_status "warning" "Start with: ./start-db-services.sh"

# Запуск FastAPI сервера
cd "$PROJECT_ROOT/backend/src"
start_service "FastAPI Backend" \
    "python -m uvicorn fastapi_app.main:app --reload --host 0.0.0.0 --port 8000" \
    "/tmp/ventai-backend.log" \
    8000

# Запуск Frontend сервера
cd "$PROJECT_ROOT/frontend"
if [ -f "package.json" ]; then
    start_service "Next.js Frontend" \
        "npm run dev" \
        "/tmp/ventai-frontend.log" \
        3000
fi

cd "$PROJECT_ROOT"

# Тестування MCP конфігурації
print_status "info" "Testing MCP configuration..."
if python test_mcp.py; then
    print_status "success" "MCP configuration test passed"
else
    print_status "warning" "MCP configuration test failed (see above for details)"
fi

# Тестування MCP сервера
print_status "info" "Testing MCP server..."
timeout 10s python mcp_server.py || print_status "info" "MCP server test completed"

echo ""
echo "🎯 VentAI MCP Environment Summary"
echo "=================================="
print_status "info" "Project Root: $PROJECT_ROOT"
print_status "info" "Backend API: http://localhost:8000"
print_status "info" "Frontend: http://localhost:3000"
print_status "info" "PostgreSQL: localhost:5433"
print_status "info" "Redis: localhost:6380"

echo ""
echo "📋 MCP Servers Configured for Claude 4:"
echo "- ventai-main: Main VentAI AI services"
echo "- ventai-filesystem: File system access"

echo ""
echo "🔧 Available Tools for Claude:"
echo "- hvac_optimize: Оптимізація HVAC систем"
echo "- project_analyze: Аналіз проектів"
echo "- cost_optimize: Оптимізація вартості"
echo "- material_search: Пошук матеріалів"
echo "- procurement_analyze: Аналіз закупівель"
echo "- crm_sync: Синхронізація з CRM"
echo "- get_project_status: Статус проектів"

echo ""
echo "💡 How to use with Claude 4:"
echo "1. ✅ Environment is now ready"
echo "2. 🖥  Open Claude Desktop application"
echo "3. ⚙️  Check Settings > MCP Servers (should auto-detect from .vscode/mcp.json)"
echo "4. 🎯 Ask Claude about VentAI projects, HVAC calculations, cost optimization, etc."

echo ""
echo "🔍 Example prompts for Claude:"
echo "- 'Розрахуй вентиляцію для офісу 200м² на 50 осіб'"
echo "- 'Проаналізуй цей проект на відповідність ДБН'"
echo "- 'Знайди способи зменшити вартість проекту на 20%'"
echo "- 'Які матеріали потрібні для цієї вентиляційної системи?'"

echo ""
echo "📊 Monitoring:"
echo "- Backend logs: tail -f /tmp/ventai-backend.log"
echo "- Frontend logs: tail -f /tmp/ventai-frontend.log"
echo "- Test MCP: python test_mcp.py"
echo "- Restart services: ./start-mcp.sh"

echo ""
print_status "success" "VentAI MCP environment is ready for Claude 4! 🎉"
