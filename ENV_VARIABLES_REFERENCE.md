# 🚨 URGENT: Environment Variables Reference for AI Systems

## ⚠️ IMPORTANT NOTICE
**This file contains sensitive environment variable templates for the VentAI project. Please use this content IMMEDIATELY to create your original .env files as this documentation will be deleted soon for security reasons.**

## 📍 Environment Files Locations and Contents

### 1. Root Environment Template
**Location:** `/Users/olegkizyma/workspaces/MVP/ventai-app/.env.example`
**Purpose:** Main application environment variables template
**Status:** Template file - copy to `.env` and update values

```bash
# Environment Variables Template
# Copy this file to .env and fill in your actual values

# =================================================================
# DATABASE CONFIGURATION
# =================================================================
DATABASE_URL=postgresql://ventai_user:your_secure_password@localhost:5433/ventai_prod
POSTGRES_DB=ventai_prod
POSTGRES_USER=ventai_user
POSTGRES_PASSWORD=your_secure_password

# =================================================================
# REDIS CONFIGURATION  
# =================================================================
REDIS_URL=redis://localhost:6380/0
REDIS_PASSWORD=your_redis_password

# =================================================================
# APPLICATION SECURITY
# =================================================================
SECRET_KEY=your-super-secret-key-min-32-chars-long
ENCRYPTION_KEY=your-32-byte-base64-encoded-encryption-key
JWT_SECRET=your-jwt-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# =================================================================
# AI API KEYS (Required for AI features)
# =================================================================
GEMINI_API_KEY=your-google-gemini-api-key
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-claude-api-key

# =================================================================
# AI MODEL CONFIGURATION
# =================================================================
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# =================================================================
# OLLAMA CONFIGURATION (Optional)
# =================================================================
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# =================================================================
# VECTOR DATABASE (Optional)
# =================================================================
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=ventai-vectors

# =================================================================
# CRM INTEGRATION (Optional)
# =================================================================
HUBSPOT_API_KEY=your-hubspot-api-key

# =================================================================
# APPLICATION SETTINGS
# =================================================================
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# =================================================================
# HVAC CALCULATION DEFAULTS
# =================================================================
LABOR_COST_PER_HOUR=50.0
ENERGY_COST_PER_KWH=0.12
DEFAULT_CLIMATE_ZONE=temperate

# =================================================================
# EMAIL CONFIGURATION (Optional)
# =================================================================
SMTP_HOST=smtp.your-provider.com
SMTP_PORT=587
SMTP_USER=your-email@domain.com
SMTP_PASSWORD=your-email-password
SMTP_USE_TLS=true

# =================================================================
# MONITORING AND LOGGING
# =================================================================
SENTRY_DSN=your-sentry-dsn-url
DATADOG_API_KEY=your-datadog-api-key

# =================================================================
# CLOUD STORAGE (Optional)
# =================================================================
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=ventai-storage

# =================================================================
# PERFORMANCE MONITORING
# =================================================================
NEW_RELIC_LICENSE_KEY=your-new-relic-license-key
ELASTIC_APM_SERVER_URL=your-elastic-apm-server-url

# =================================================================
# DEVELOPMENT SETTINGS (Development only)
# =================================================================
# DEV_CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
# DEV_DATABASE_URL=postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev

# =================================================================
# KUBERNETES SECRETS (Production deployment)
# =================================================================
# KUBE_CONFIG_DATA=base64-encoded-kubeconfig
# DOCKER_REGISTRY_URL=ghcr.io
# DOCKER_REGISTRY_USERNAME=your-github-username
# DOCKER_REGISTRY_PASSWORD=your-github-token
```

### 2. Frontend Environment (Local Development)
**Location:** `/Users/olegkizyma/workspaces/MVP/ventai-app/frontend/.env.local`
**Purpose:** React/Next.js frontend environment variables
**Status:** Active development file

```bash
# Development Environment
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_ENV=development
```

### 3. Windsurf Server Backup Configuration
**Location:** `/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server/.env.backup`
**Purpose:** Backup of Windsurf MCP server configuration
**Status:** Backup file with Ukrainian comments

```bash
# 🔧 Environment Configuration для Windsurf Enterprise MCP Server

# PostgreSQL Configuration
DATABASE_URL=postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=ventai_dev
POSTGRES_USER=ventai_dev
POSTGRES_PASSWORD=ventai_dev_password

# Redis Configuration  
REDIS_URL=redis://localhost:6380
REDIS_HOST=localhost
REDIS_PORT=6380
REDIS_PASSWORD=
REDIS_DB=0

# OpenAI Configuration (Optional - для векторних embeddings)
# OPENAI_API_KEY=${OPENAI_API_KEY}
OPENAI_MODEL=text-embedding-ada-002

# Vector Store Configuration  
VECTOR_DIMENSION=1536
VECTOR_BATCH_SIZE=100
VECTOR_SYNC_INTERVAL=300000

# Feature Flags
ENABLE_VECTOR_SEARCH=true
ENABLE_GRAPH_RELATIONS=true
ENABLE_SMART_RECOMMENDATIONS=true
ENABLE_AUTO_SYNC=true
ENABLE_CACHING=true
ENABLE_OPENAI_EMBEDDINGS=false

# MCP Server Configuration
MCP_SERVER_NAME=windsurf-enterprise
MCP_SERVER_VERSION=2.0.0
MCP_LOG_LEVEL=info

# Windsurf Integration
WINDSURF_ROOT=/Users/olegkizyma/workspaces/MVP/ventai-app
WINDSURF_AUTO_SYNC=true
WINDSURF_SYNC_INTERVAL=300
WINDSURF_VECTOR_ENABLED=true

# Security Configuration
ALLOWED_DIRECTORIES=/Users/olegkizyma/workspaces/MVP/ventai-app
ACCESS_TOKEN=windsurf_enterprise_token_2024
ENABLE_AUDIT_LOG=true

# Performance Configuration
MAX_POOL_SIZE=20
CONNECTION_TIMEOUT=2000
IDLE_TIMEOUT=30000
QUERY_TIMEOUT=10000

# Feature Flags
ENABLE_VECTOR_SEARCH=true
ENABLE_GRAPH_RELATIONS=true
ENABLE_SMART_RECOMMENDATIONS=true
ENABLE_AUTO_SYNC=true
ENABLE_CACHING=true

# Development Configuration
NODE_ENV=development
DEBUG=windsurf:*
LOG_FILE=logs/windsurf-mcp.log
```

### 4. Windsurf Global Configuration
**Location:** `/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server/.env.global`
**Purpose:** Global Windsurf configuration with test API keys
**Status:** Active development file with test credentials

```bash
DATABASE_URL=postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev
REDIS_URL=redis://localhost:6380
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
DEBUG=true

# AI API Keys (замініть на справжні для production)
GEMINI_API_KEY=AIzaSyDTlDE001O_AAAgyVDgC3zPSBO3HR64M4M
OPENAI_API_KEY=test-openai-key-12345
ANTHROPIC_API_KEY=test-anthropic-key-12345
PINECONE_API_KEY=test-pinecone-key-12345
HUBSPOT_API_KEY=test-hubspot-key-12345

# Ollama Configuration (локальний сервер)
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama2

# AI Models Configuration
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Pinecone Configuration
PINECONE_ENVIRONMENT=us-west1-gcp

# Cost Configuration для розрахунків
LABOR_COST_PER_HOUR=50.0
ENERGY_COST_PER_KWH=0.12

# MCP Server Configuration
MCP_HOST=0.0.0.0
MCP_PORT=8001
MCP_LOG_LEVEL=INFO
```

### 5. Windsurf Native AI Configuration
**Location:** `/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server/.env.windsurf`
**Purpose:** Windsurf built-in AI models configuration (no external API keys needed)
**Status:** Production-ready configuration using Windsurf native AI

```bash
# 🌊 Windsurf Enterprise MCP Server Configuration
# Using Windsurf Built-in AI Models (No External API Keys Required)

# ==================== WINDSURF NATIVE AI CONFIGURATION ====================
# Windsurf models are accessed through VS Code Language Model API
# No API keys needed - uses your Windsurf subscription

# Windsurf AI Preferences
WINDSURF_PREFERRED_VENDOR=anthropic
WINDSURF_FALLBACK_VENDOR=openai
WINDSURF_ENABLE_REASONING_MODELS=true
WINDSURF_ENABLE_THINKING_MODELS=true

# AI Chat Configuration
AI_CHAT_TEMPERATURE=0.7
AI_CHAT_MAX_TOKENS=2000
AI_CODE_ANALYSIS_TEMPERATURE=0.3
AI_CODE_ANALYSIS_MAX_TOKENS=3000

# Windsurf Model Priorities (in order of preference)
# anthropic: Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude Sonnet 4
# openai: GPT-4o, o3-mini, GPT-4o mini  
# google: Gemini 2.5 Pro, Gemini 2.5 Flash
# xai: Grok-3, Grok-3 mini
# deepseek: DeepSeek V3, DeepSeek R1
# windsurf: SWE-1, SWE-1-lite

WINDSURF_PROVIDER_PRIORITY=anthropic,openai,google,xai,deepseek,windsurf

# ==================== DATABASE CONFIGURATION ====================
# PostgreSQL Vector Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=windsurf_user
POSTGRES_PASSWORD=windsurf_secure_pass_2024
POSTGRES_DB=windsurf_enterprise

# Vector Search Configuration
VECTOR_DIMENSIONS=1536
VECTOR_SIMILARITY_THRESHOLD=0.7
VECTOR_MAX_RESULTS=50

# ==================== REDIS CACHE CONFIGURATION ====================
REDIS_URL=redis://localhost:6379
REDIS_PREFIX=windsurf:
REDIS_TTL=3600

# ==================== MCP SERVER CONFIGURATION ====================
MCP_SERVER_NAME=windsurf-enterprise-mcp
MCP_SERVER_VERSION=2.0.0
MCP_SERVER_PORT=8001
MCP_SERVER_HOST=localhost

# Logging Configuration
LOG_LEVEL=info
LOG_FILE=./logs/windsurf-mcp.log
LOG_MAX_SIZE=10m
LOG_MAX_FILES=5

# ==================== ENTERPRISE FEATURES ====================
# Vector Store & Graph Relations
ENABLE_VECTOR_STORE=true
ENABLE_GRAPH_RELATIONS=true
ENABLE_SMART_RECOMMENDATIONS=true
ENABLE_AUTO_SYNC=true

# Performance & Monitoring
ENABLE_PERFORMANCE_MONITORING=true
ENABLE_AI_ANALYTICS=true
METRICS_COLLECTION_INTERVAL=300

# Security & Access Control
ALLOWED_DIRECTORIES=/Users/olegkizyma/workspaces/MVP/ventai-app
MAX_FILE_SIZE=50MB
MAX_FILES_PER_REQUEST=20

# ==================== HVAC DOMAIN SPECIFIC ====================
# VentAI Platform Integration
VENTAI_PROJECT_CONTEXT=true
HVAC_CALCULATIONS_ENABLED=true
UKRAINIAN_STANDARDS_DB=./ukrainian_standards.db

# Specialized Prompts
HVAC_SYSTEM_PROMPT="You are an expert HVAC engineer specializing in Ukrainian building standards and energy-efficient ventilation systems."
CODE_REVIEW_PROMPT="You are a senior software engineer reviewing TypeScript/React code for the VentAI HVAC platform."

# ==================== DEVELOPMENT & TESTING ====================
NODE_ENV=development
DEBUG=windsurf:*

# Test Configuration
ENABLE_TEST_MODE=false
MOCK_AI_RESPONSES=false
TEST_RESPONSE_DELAY=100

# ==================== BACKUP & SYNC ====================
AUTO_BACKUP_ENABLED=true
BACKUP_INTERVAL_HOURS=6
BACKUP_RETENTION_DAYS=30
SYNC_INTERVAL_MINUTES=5

# ==================== API ENDPOINTS (DISABLED) ====================
# External API keys not needed with Windsurf native integration
# OPENAI_API_KEY=disabled
# ANTHROPIC_API_KEY=disabled  
# GEMINI_API_KEY=disabled
# MISTRAL_API_KEY=disabled
# GROK_API_KEY=disabled

# Note: All AI functionality now uses Windsurf built-in models
# This provides better integration, security, and cost efficiency
```

### 6. Multi-AI Provider Template
**Location:** `/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server/.env.template`
**Purpose:** Comprehensive template for multiple AI providers
**Status:** Template for advanced AI integration

```bash
# 🌟 Multi-AI Provider Environment Configuration

# Copy this to your .env file in the .windsurf/server directory

# ==================== EXISTING CONFIGURATION ====================

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=ventai_enterprise
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=ventai_enterprise

# Redis Configuration  
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Vector Store Configuration
VECTOR_DIMENSIONS=1536
ENABLE_VECTOR_STORE=true

# ==================== NEW AI PROVIDERS CONFIGURATION ====================

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
# Optional: specify default model
OPENAI_DEFAULT_MODEL=gpt-4o
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Anthropic Claude Configuration  
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# Optional: specify default model
ANTHROPIC_DEFAULT_MODEL=claude-3-5-sonnet-20241022

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
# Optional: specify default model
GEMINI_DEFAULT_MODEL=gemini-1.5-pro
GEMINI_EMBEDDING_MODEL=text-embedding-004

# Mistral AI Configuration
MISTRAL_API_KEY=your_mistral_api_key_here
# Optional: specify default model
MISTRAL_DEFAULT_MODEL=mistral-large-latest
MISTRAL_EMBEDDING_MODEL=mistral-embed

# Grok (X.AI) Configuration  
GROK_API_KEY=your_grok_api_key_here
# Optional: specify default model
GROK_DEFAULT_MODEL=grok-beta

# Local Ollama Configuration (Optional)
# Uncomment and configure if you want to use local models
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_DEFAULT_MODEL=llama3:latest
# OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest

# ==================== AI PROVIDER SETTINGS ====================

# Enable/disable specific providers
ENABLE_OPENAI=true
ENABLE_ANTHROPIC=true  
ENABLE_GEMINI=true
ENABLE_MISTRAL=true
ENABLE_GROK=false
ENABLE_OLLAMA=false
ENABLE_WINDSURF=true

# Provider priority for chat (comma-separated)
AI_CHAT_PRIORITY=anthropic,openai,google,windsurf,local,mistral,grok

# Provider priority for embeddings (comma-separated)  
AI_EMBEDDING_PRIORITY=openai,google,mistral,local

# Request timeout in milliseconds
AI_REQUEST_TIMEOUT=30000

# Max retries for failed requests
AI_MAX_RETRIES=3

# Enable automatic fallback
AI_ENABLE_FALLBACK=true

# ==================== LOGGING & MONITORING ====================

# AI operation logging
LOG_AI_REQUESTS=true
LOG_AI_RESPONSES=false
LOG_AI_ERRORS=true

# Performance monitoring
TRACK_AI_PERFORMANCE=true
TRACK_TOKEN_USAGE=true

# ==================== DEVELOPMENT/TESTING ====================

# Test API keys (for development only)
# Uncomment these lines for testing without real API keys
# OPENAI_API_KEY=test-openai-key-12345
# ANTHROPIC_API_KEY=test-anthropic-key-12345
# GEMINI_API_KEY=test-gemini-key-12345
# MISTRAL_API_KEY=test-mistral-key-12345

# Enable AI testing mode (uses mock responses)
AI_TESTING_MODE=false

# ==================== SECURITY ====================

# Rate limiting
AI_RATE_LIMIT_REQUESTS_PER_MINUTE=60
AI_RATE_LIMIT_TOKENS_PER_MINUTE=100000

# API key encryption (set to true in production)
ENCRYPT_API_KEYS=false
API_KEY_ENCRYPTION_SECRET=your_encryption_secret_32_chars

# ==================== WINDSURF INTEGRATION ====================

# Windsurf project context
WINDSURF_PROJECT_ROOT=/Users/olegkizyma/workspaces/MVP/ventai-app
WINDSURF_CONTEXT_DEPTH=5
WINDSURF_INCLUDE_GITIGNORE=true

# File patterns to include in Windsurf context
WINDSURF_INCLUDE_PATTERNS=**/*.ts,**/*.tsx,**/*.js,**/*.jsx,**/*.py,**/*.md
WINDSURF_EXCLUDE_PATTERNS=node_modules/**,dist/**,build/**,coverage/**

# ==================== EXAMPLE VALUES ====================
# Replace these with your actual API keys

# Example OpenAI key format: sk-proj-1234567890abcdef...
# Example Anthropic key format: sk-ant-api03-1234567890abcdef...  
# Example Gemini key format: AIzaSy1234567890abcdef...
# Example Mistral key format: 1234567890abcdef...
# Example Grok key format: xai-1234567890abcdef...
```

### 7. Windsurf Server Example Configuration
**Location:** `/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server/.env.example`
**Purpose:** Example configuration for Windsurf MCP server
**Status:** Template file with Ukrainian comments

```bash
# 🔧 Environment Configuration для Windsurf Enterprise MCP Server

# PostgreSQL Configuration
DATABASE_URL=postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=ventai_dev
POSTGRES_USER=ventai_dev
POSTGRES_PASSWORD=ventai_dev_password

# Redis Configuration  
REDIS_URL=redis://localhost:6380
REDIS_HOST=localhost
REDIS_PORT=6380
REDIS_PASSWORD=
REDIS_DB=0

# OpenAI Configuration (Optional - для векторних embeddings)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=text-embedding-ada-002

# Vector Store Configuration
VECTOR_DIMENSION=1536
VECTOR_BATCH_SIZE=100
VECTOR_SYNC_INTERVAL=300000

# MCP Server Configuration
MCP_SERVER_NAME=windsurf-enterprise
MCP_SERVER_VERSION=2.0.0
MCP_LOG_LEVEL=info

# Windsurf Integration
WINDSURF_ROOT=/Users/olegkizyma/workspaces/MVP/ventai-app
WINDSURF_AUTO_SYNC=true
WINDSURF_SYNC_INTERVAL=300
WINDSURF_VECTOR_ENABLED=true

# Security Configuration
ALLOWED_DIRECTORIES=/Users/olegkizyma/workspaces/MVP/ventai-app
ACCESS_TOKEN=windsurf_enterprise_token_2024
ENABLE_AUDIT_LOG=true

# Performance Configuration
MAX_POOL_SIZE=20
CONNECTION_TIMEOUT=2000
IDLE_TIMEOUT=30000
QUERY_TIMEOUT=10000

# Feature Flags
ENABLE_VECTOR_SEARCH=true
ENABLE_GRAPH_RELATIONS=true
ENABLE_SMART_RECOMMENDATIONS=true
ENABLE_AUTO_SYNC=true
ENABLE_CACHING=true

# Development Configuration
NODE_ENV=development
DEBUG=windsurf:*
LOG_FILE=logs/windsurf-mcp.log
```

## 🔑 Key Environment Variables Summary

### Database Connections
- **PostgreSQL Production:** `postgresql://ventai_user:your_secure_password@localhost:5433/ventai_prod`
- **PostgreSQL Development:** `postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev`
- **Redis:** `redis://localhost:6380` or `redis://localhost:6379`

### AI API Keys Required
- **OpenAI:** `OPENAI_API_KEY`
- **Anthropic:** `ANTHROPIC_API_KEY`
- **Google Gemini:** `GEMINI_API_KEY`
- **Mistral:** `MISTRAL_API_KEY`
- **Grok (X.AI):** `GROK_API_KEY`
- **Pinecone:** `PINECONE_API_KEY`

### Security Variables
- **JWT Secret:** `JWT_SECRET`
- **Encryption Key:** `ENCRYPTION_KEY`
- **Secret Key:** `SECRET_KEY`

### HVAC-Specific Variables
- **Labor Cost:** `LABOR_COST_PER_HOUR=50.0`
- **Energy Cost:** `ENERGY_COST_PER_KWH=0.12`
- **Ukrainian Standards DB:** `./ukrainian_standards.db`

## 🚀 Quick Setup Instructions

1. **Copy main template:** `cp .env.example .env`
2. **Update frontend:** Edit `frontend/.env.local` if needed
3. **Configure Windsurf:** Choose from `.windsurf/server/.env.*` files
4. **Add real API keys** to replace test values
5. **Update database credentials** for your environment
6. **Set secure passwords** for production deployment

## ⚠️ Security Warning

**DO NOT commit actual .env files to git!** Always use templates and add real .env files to .gitignore.

---

*This documentation file will be automatically deleted for security reasons. Save the necessary configurations immediately.*
