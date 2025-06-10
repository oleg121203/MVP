#!/bin/bash

# 🚀 Windsurf AI Integration Quick Start
# Швидкий запуск повної інтеграції Windsurf AI для VentAI

set -e

echo "🌊 === WINDSURF AI INTEGRATION QUICK START ==="
echo ""

# Кольори для виводу
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Перевірка поточної директорії
if [[ ! -d ".windsurf/server" ]]; then
    echo -e "${RED}❌ Error: Please run from VentAI root directory${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 Step 1: Checking Windsurf server...${NC}"
cd .windsurf/server

# Перевірка залежностей
if [[ ! -d "node_modules" ]]; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    npm install
fi

# Збірка проекту
echo -e "${BLUE}🔨 Step 2: Building Windsurf server...${NC}"
npm run build

# Перевірка чи запущений HTTP сервер
echo -e "${BLUE}🌐 Step 3: Checking HTTP server status...${NC}"
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ HTTP server is already running${NC}"
else
    echo -e "${YELLOW}🚀 Starting HTTP MCP server...${NC}"
    npm run start:http &
    sleep 3
    
    # Перевірка запуску
    if curl -s http://localhost:8001/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ HTTP server started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start HTTP server${NC}"
        exit 1
    fi
fi

# Тестування інтеграції
echo -e "${BLUE}🧪 Step 4: Testing Windsurf integration...${NC}"

# Test 1: Health check
echo -n "   Health check: "
if curl -s http://localhost:8001/health | jq -r '.status' | grep -q "ok"; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
    exit 1
fi

# Test 2: Providers check
echo -n "   Providers count: "
PROVIDERS_COUNT=$(curl -s -X POST http://localhost:8001/mcp/call-tool \
    -H "Content-Type: application/json" \
    -d '{"tool": "list_ai_providers", "params": {}}' | \
    jq -r '.content[0].text' | jq -r '.total')

if [[ "$PROVIDERS_COUNT" == "6" ]]; then
    echo -e "${GREEN}✅ 6/6 providers${NC}"
else
    echo -e "${RED}❌ Expected 6, got $PROVIDERS_COUNT${NC}"
    exit 1
fi

# Test 3: Models count  
echo -n "   Models count: "
MODELS_COUNT=$(curl -s -X POST http://localhost:8001/mcp/call-tool \
    -H "Content-Type: application/json" \
    -d '{"tool": "list_ai_providers", "params": {}}' | \
    jq -r '.content[0].text' | jq -r '.total_models')

if [[ "$MODELS_COUNT" == "11" ]]; then
    echo -e "${GREEN}✅ 11/11 models${NC}"
else
    echo -e "${RED}❌ Expected 11, got $MODELS_COUNT${NC}"
    exit 1
fi

# Test 4: AI Chat
echo -n "   AI Chat test: "
AI_RESPONSE=$(curl -s -X POST http://localhost:8001/mcp/call-tool \
    -H "Content-Type: application/json" \
    -d '{
        "tool": "ai_chat_completion",
        "params": {
            "messages": [{"role": "user", "content": "Test"}],
            "provider": "windsurf",
            "model": "windsurf-swe-1"
        }
    }' | jq -r '.content[0].text' | jq -r '.response' | wc -c)

if [[ $AI_RESPONSE -gt 10 ]]; then
    echo -e "${GREEN}✅ WORKING${NC}"
else
    echo -e "${RED}❌ NO RESPONSE${NC}"
    exit 1
fi

# Фінальна інформація
echo ""
echo -e "${BOLD}🎉 === WINDSURF AI INTEGRATION READY ===${NC}"
echo ""
echo -e "${GREEN}✅ HTTP Server:${NC} http://localhost:8001"
echo -e "${GREEN}✅ Providers:${NC} 6 (windsurf, openai, anthropic, google, xai, deepseek)"
echo -e "${GREEN}✅ Models:${NC} 11 total (3 free, 2 reasoning, 9 chat)"
echo -e "${GREEN}✅ Status:${NC} Production Ready"
echo ""

echo -e "${BOLD}📋 Quick API Examples:${NC}"
echo ""
echo -e "${BLUE}# List all providers:${NC}"
echo "curl -X POST http://localhost:8001/mcp/call-tool \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"tool\": \"list_ai_providers\", \"params\": {}}'"
echo ""

echo -e "${BLUE}# Chat with free Windsurf model:${NC}"
echo "curl -X POST http://localhost:8001/mcp/call-tool \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{"
echo "    \"tool\": \"ai_chat_completion\","
echo "    \"params\": {"
echo "      \"messages\": [{\"role\": \"user\", \"content\": \"Hello!\"}],"
echo "      \"provider\": \"windsurf\","
echo "      \"model\": \"windsurf-swe-1\""
echo "    }"
echo "  }'"
echo ""

echo -e "${BOLD}📁 Integration Files:${NC}"
echo -e "${YELLOW}Backend:${NC} .windsurf/server/src/windsurf-ai-provider.ts"
echo -e "${YELLOW}Frontend:${NC} frontend/src/services/windsurfExactModels.js"
echo -e "${YELLOW}React:${NC} frontend/src/components/WindsurfModelsShowcase.jsx"
echo -e "${YELLOW}Demo:${NC} .windsurf/server/final-exact-verification.js"
echo ""

echo -e "${BOLD}🚀 Ready for VentAI integration!${NC}"
echo ""
