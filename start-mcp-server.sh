#!/bin/bash
"""
Скрипт запуску VentAI MCP Server для Claude 4
"""

set -e

echo "🚀 Starting VentAI MCP Server..."

# Перевірка робочої директорії
if [ ! -d "/workspaces/MVP" ]; then
    echo "❌ VentAI workspace not found at /workspaces/MVP"
    exit 1
fi

cd /workspaces/MVP

# Налаштування змінних середовища
export VENTAI_PROJECT_ROOT="/workspaces/MVP"
export MCP_PORT=8001
export MCP_HOST="0.0.0.0"

# Встановлення Python залежностей
echo "📦 Installing Python dependencies..."
pip install -r backend/requirements.txt

# Перевірка наявності AI API ключів
echo "🔑 Checking AI API keys..."
if [ ! -z "$OPENAI_API_KEY" ]; then
    echo "  ✅ OpenAI API key found"
else
    echo "  ⚠️  OpenAI API key not found (OPENAI_API_KEY)"
fi

if [ ! -z "$ANTHROPIC_API_KEY" ]; then
    echo "  ✅ Anthropic API key found"
else
    echo "  ⚠️  Anthropic API key not found (ANTHROPIC_API_KEY)"
fi

if [ ! -z "$GEMINI_API_KEY" ]; then
    echo "  ✅ Gemini API key found"
else
    echo "  ⚠️  Gemini API key not found (GEMINI_API_KEY)"
fi

# Перевірка Ollama
echo "🤖 Checking Ollama availability..."
if command -v ollama &> /dev/null; then
    if ollama list &> /dev/null; then
        echo "  ✅ Ollama is running and available"
        export OLLAMA_BASE_URL="http://localhost:11434"
    else
        echo "  ⚠️  Ollama installed but not running"
    fi
else
    echo "  ⚠️  Ollama not installed"
fi

# Перевірка Redis
echo "💾 Checking Redis availability..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo "  ✅ Redis is running and available"
        export REDIS_URL="redis://localhost:6379/0"
    else
        echo "  ⚠️  Redis installed but not running"
        echo "  💡 Starting Redis in background..."
        redis-server --daemonize yes --port 6379 || echo "  ❌ Failed to start Redis"
    fi
else
    echo "  ⚠️  Redis not installed - caching will be disabled"
fi

echo ""
echo "🔧 MCP Configuration Summary:"
echo "  - Project Root: $VENTAI_PROJECT_ROOT"
echo "  - Server Port: $MCP_PORT"
echo "  - Server Host: $MCP_HOST"
echo ""

# Створення MCP конфігурації для Claude Desktop
echo "📋 Creating Claude Desktop MCP configuration..."
MCP_CONFIG_DIR="$HOME/.config/claude-desktop"
mkdir -p "$MCP_CONFIG_DIR"

cat > "$MCP_CONFIG_DIR/claude_desktop_config.json" << EOF
{
  "mcpServers": {
    "ventai-main": {
      "command": "python",
      "args": ["/workspaces/MVP/backend/mcp_server.py"],
      "env": {
        "VENTAI_PROJECT_ROOT": "/workspaces/MVP",
        "MCP_PORT": "8001",
        "MCP_HOST": "0.0.0.0"
      }
    }
  }
}
EOF

echo "✅ Claude Desktop configuration created at: $MCP_CONFIG_DIR/claude_desktop_config.json"

echo ""
echo "🎯 Starting VentAI MCP Server..."
echo "📡 Server will be available at: http://$MCP_HOST:$MCP_PORT/health"
echo ""

# Запуск MCP сервера
cd /workspaces/MVP/backend
python mcp_server.py
