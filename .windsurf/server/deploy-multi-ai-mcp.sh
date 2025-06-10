#!/bin/bash

# 🚀 Windsurf Enterprise MCP Server - Multi-AI Deployment Script
# Enhanced with Multi-AI Provider Support

set -e

echo "🌟 Starting Windsurf Enterprise MCP Server with Multi-AI Support..."
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
SERVER_DIR="/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server"
LOG_DIR="$SERVER_DIR/logs"
PID_FILE="$SERVER_DIR/mcp-server.pid"

# Create logs directory
mkdir -p "$LOG_DIR"

echo -e "${BLUE}📁 Working directory: $SERVER_DIR${NC}"

# Function to check if service is running
check_service() {
    local service_name=$1
    local port=$2
    
    if nc -z localhost $port 2>/dev/null; then
        echo -e "${GREEN}✅ $service_name is running on port $port${NC}"
        return 0
    else
        echo -e "${RED}❌ $service_name is not running on port $port${NC}"
        return 1
    fi
}

# Function to start service
start_service() {
    local service_name=$1
    local command=$2
    
    echo -e "${YELLOW}🔧 Starting $service_name...${NC}"
    eval $command
}

# Function to check AI provider availability
check_ai_providers() {
    echo -e "${PURPLE}🤖 Checking AI Provider Configuration...${NC}"
    
    # Check for API keys in .env
    if [ -f "$SERVER_DIR/.env" ]; then
        echo -e "${BLUE}📋 Configured AI Providers:${NC}"
        
        if grep -q "OPENAI_API_KEY=" "$SERVER_DIR/.env" && [ "$(grep "OPENAI_API_KEY=" "$SERVER_DIR/.env" | cut -d'=' -f2)" != "" ]; then
            echo -e "   ${GREEN}✅ OpenAI${NC}"
        else
            echo -e "   ${YELLOW}⚠️  OpenAI (no API key)${NC}"
        fi
        
        if grep -q "ANTHROPIC_API_KEY=" "$SERVER_DIR/.env" && [ "$(grep "ANTHROPIC_API_KEY=" "$SERVER_DIR/.env" | cut -d'=' -f2)" != "" ]; then
            echo -e "   ${GREEN}✅ Anthropic Claude${NC}"
        else
            echo -e "   ${YELLOW}⚠️  Anthropic Claude (no API key)${NC}"
        fi
        
        if grep -q "GEMINI_API_KEY=" "$SERVER_DIR/.env" && [ "$(grep "GEMINI_API_KEY=" "$SERVER_DIR/.env" | cut -d'=' -f2)" != "" ]; then
            echo -e "   ${GREEN}✅ Google Gemini${NC}"
        else
            echo -e "   ${YELLOW}⚠️  Google Gemini (no API key)${NC}"
        fi
        
        if grep -q "MISTRAL_API_KEY=" "$SERVER_DIR/.env" && [ "$(grep "MISTRAL_API_KEY=" "$SERVER_DIR/.env" | cut -d'=' -f2)" != "" ]; then
            echo -e "   ${GREEN}✅ Mistral AI${NC}"
        else
            echo -e "   ${YELLOW}⚠️  Mistral AI (no API key)${NC}"
        fi
        
        if grep -q "GROK_API_KEY=" "$SERVER_DIR/.env" && [ "$(grep "GROK_API_KEY=" "$SERVER_DIR/.env" | cut -d'=' -f2)" != "" ]; then
            echo -e "   ${GREEN}✅ Grok (X.AI)${NC}"
        else
            echo -e "   ${YELLOW}⚠️  Grok (X.AI) (no API key)${NC}"
        fi
        
        if grep -q "OLLAMA_BASE_URL=" "$SERVER_DIR/.env" && [ "$(grep "OLLAMA_BASE_URL=" "$SERVER_DIR/.env" | cut -d'=' -f2)" != "" ]; then
            echo -e "   ${GREEN}✅ Ollama (Local)${NC}"
        else
            echo -e "   ${YELLOW}⚠️  Ollama (Local) (not configured)${NC}"
        fi
        
        echo -e "   ${GREEN}✅ Windsurf Built-in${NC}"
    else
        echo -e "${RED}❌ .env file not found!${NC}"
        exit 1
    fi
}

# Function to test AI providers
test_ai_providers() {
    echo -e "${PURPLE}🧪 Testing AI Providers...${NC}"
    
    cd "$SERVER_DIR"
    
    # Build the server first
    echo -e "${YELLOW}🔨 Building MCP server...${NC}"
    npm run build
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Server build successful${NC}"
        
        # Test AI providers
        echo -e "${YELLOW}🧪 Running AI provider tests...${NC}"
        node test-ai-providers.js
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ AI provider tests passed${NC}"
        else
            echo -e "${YELLOW}⚠️  Some AI provider tests failed (this is normal if API keys are not set)${NC}"
        fi
    else
        echo -e "${RED}❌ Server build failed${NC}"
        exit 1
    fi
}

# Main deployment process
main() {
    cd "$SERVER_DIR"
    
    echo -e "${BLUE}📦 Checking dependencies...${NC}"
    
    # Check if Node.js is installed
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js is not installed${NC}"
        exit 1
    fi
    
    # Check if npm is installed
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm is not installed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Node.js version: $(node --version)${NC}"
    echo -e "${GREEN}✅ npm version: $(npm --version)${NC}"
    
    # Install dependencies
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    npm install
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        exit 1
    fi
    
    # Check dependencies
    echo -e "${BLUE}🔍 Checking prerequisite services...${NC}"
    
    # Check PostgreSQL
    if check_service "PostgreSQL" 5433; then
        echo -e "${GREEN}✅ PostgreSQL connection successful${NC}"
    else
        echo -e "${YELLOW}⚠️  PostgreSQL not running on port 5433${NC}"
        echo -e "${YELLOW}   Starting PostgreSQL...${NC}"
        # Try to start PostgreSQL (this depends on your setup)
        # brew services start postgresql@14 || true
    fi
    
    # Check Redis
    if check_service "Redis" 6380; then
        echo -e "${GREEN}✅ Redis connection successful${NC}"
    else
        echo -e "${YELLOW}⚠️  Redis not running on port 6380${NC}"
        echo -e "${YELLOW}   Starting Redis...${NC}"
        # Try to start Redis (this depends on your setup)
        # brew services start redis || true
    fi
    
    # Check AI provider configuration
    check_ai_providers
    
    # Test AI providers functionality
    test_ai_providers
    
    # Build the project
    echo -e "${YELLOW}🔨 Building project...${NC}"
    npm run build
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Build failed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Build successful${NC}"
    
    # Start the MCP server
    echo -e "${YELLOW}🚀 Starting Windsurf Enterprise MCP Server...${NC}"
    
    # Kill existing server if running
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if ps -p $OLD_PID > /dev/null 2>&1; then
            echo -e "${YELLOW}🔄 Stopping existing server (PID: $OLD_PID)...${NC}"
            kill $OLD_PID
            sleep 2
        fi
        rm -f "$PID_FILE"
    fi
    
    # Start new server
    echo -e "${GREEN}🎯 Starting new MCP server instance...${NC}"
    
    # Run in background and capture PID
    nohup node dist/enterprise-index.js > "$LOG_DIR/server.log" 2>&1 &
    SERVER_PID=$!
    echo $SERVER_PID > "$PID_FILE"
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if server is still running
    if ps -p $SERVER_PID > /dev/null 2>&1; then
        echo -e "${GREEN}✅ MCP Server started successfully!${NC}"
        echo -e "${GREEN}   PID: $SERVER_PID${NC}"
        echo -e "${GREEN}   Log file: $LOG_DIR/server.log${NC}"
        
        # Show server info
        echo -e "${BLUE}📊 Server Information:${NC}"
        echo -e "   Server Name: Windsurf Enterprise MCP Server"
        echo -e "   Version: 2.0.0 (Multi-AI Enabled)"
        echo -e "   Transport: stdio"
        echo -e "   Features: Vector Store, Graph Relations, Multi-AI Providers"
        echo -e "   AI Providers: OpenAI, Anthropic, Google, Mistral, Grok, Ollama, Windsurf"
        
        echo ""
        echo -e "${PURPLE}🔧 Available MCP Tools:${NC}"
        echo -e "   📁 File Operations: read_file, write_file, edit_file, etc."
        echo -e "   🔍 Vector Search: vector_search_documents, smart_recommendations"
        echo -e "   🕸️  Graph Relations: graph_relations, create_graph_relation"
        echo -e "   🤖 AI Tools: ai_chat_completion, ai_create_embeddings"
        echo -e "   🏗️  Windsurf Assistant: ai_windsurf_assistant"
        echo -e "   🔍 Code Analysis: ai_code_analysis"
        echo -e "   🧪 Provider Testing: ai_test_providers, list_ai_providers"
        
        echo ""
        echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
        echo -e "${YELLOW}📝 To monitor the server:${NC}"
        echo -e "   tail -f $LOG_DIR/server.log"
        echo -e "${YELLOW}📝 To stop the server:${NC}"
        echo -e "   kill \$(cat $PID_FILE)"
        
    else
        echo -e "${RED}❌ Server failed to start${NC}"
        echo -e "${RED}   Check log file: $LOG_DIR/server.log${NC}"
        cat "$LOG_DIR/server.log"
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    "stop")
        echo -e "${YELLOW}🛑 Stopping MCP Server...${NC}"
        if [ -f "$PID_FILE" ]; then
            OLD_PID=$(cat "$PID_FILE")
            if ps -p $OLD_PID > /dev/null 2>&1; then
                kill $OLD_PID
                echo -e "${GREEN}✅ Server stopped (PID: $OLD_PID)${NC}"
            else
                echo -e "${YELLOW}⚠️  Server was not running${NC}"
            fi
            rm -f "$PID_FILE"
        else
            echo -e "${YELLOW}⚠️  No PID file found${NC}"
        fi
        ;;
    "restart")
        $0 stop
        sleep 2
        $0 start
        ;;
    "status")
        if [ -f "$PID_FILE" ]; then
            OLD_PID=$(cat "$PID_FILE")
            if ps -p $OLD_PID > /dev/null 2>&1; then
                echo -e "${GREEN}✅ Server is running (PID: $OLD_PID)${NC}"
            else
                echo -e "${RED}❌ Server is not running${NC}"
            fi
        else
            echo -e "${RED}❌ Server is not running${NC}"
        fi
        ;;
    "logs")
        echo -e "${BLUE}📝 Server logs:${NC}"
        tail -f "$LOG_DIR/server.log"
        ;;
    "test")
        check_ai_providers
        test_ai_providers
        ;;
    "start"|*)
        main
        ;;
esac
