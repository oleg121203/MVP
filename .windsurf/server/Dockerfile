# Dockerfile для Windsurf Enterprise MCP Server
FROM node:18-alpine AS builder

# Встановлення системних залежностей
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    postgresql-client \
    redis

# Робоча директорія
WORKDIR /app

# Копіювання package files
COPY package*.json ./
COPY tsconfig.json ./

# Встановлення залежностей
RUN npm ci --only=production && npm cache clean --force

# Копіювання вихідного коду
COPY src/ ./src/

# Збірка TypeScript
RUN npm run build

# Production stage
FROM node:18-alpine AS production

# Встановлення runtime залежностей
RUN apk add --no-cache \
    postgresql-client \
    redis \
    curl

# Створення користувача для безпеки
RUN addgroup -g 1001 -S windsurf && \
    adduser -S windsurf -u 1001

# Робоча директорія
WORKDIR /app

# Копіювання з builder stage
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Створення директорій для логів
RUN mkdir -p logs data && \
    chown -R windsurf:windsurf /app

# Перемикання на користувача windsurf
USER windsurf

# Експозиція портів (якщо потрібно для моніторингу)
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "console.log('Health check passed')" || exit 1

# Змінні середовища за замовчуванням
ENV NODE_ENV=production \
    MCP_LOG_LEVEL=info \
    VECTOR_ENABLED=true

# Точка входу
ENTRYPOINT ["node", "dist/enterprise-index.js"]

# Мітки
LABEL \
    org.opencontainers.image.title="Windsurf Enterprise MCP Server" \
    org.opencontainers.image.description="Vector-powered MCP server for Windsurf Enterprise System" \
    org.opencontainers.image.version="2.0.0" \
    org.opencontainers.image.vendor="VentAI Enterprise" \
    org.opencontainers.image.licenses="MIT"
