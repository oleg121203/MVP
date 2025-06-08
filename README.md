# VentAI - Professional HVAC Platform

## Огляд

VentAI - це професійна платформа для розрахунків та проектування систем вентиляції з інтеграцією AI технологій.

## Project Structure

```
ventai-app/
├── frontend/              # React frontend application
├── backend/               # Python FastAPI backend
├── services/              # Microservices
│   └── mcp/              # Model Context Protocol server
├── scripts/               # Development and management scripts
├── tools/                 # Development tools
├── infra/                 # Infrastructure configuration
│   ├── docker/           # Docker configurations
│   └── k8s/              # Kubernetes manifests
├── docs/                  # Project documentation
│   ├── architecture/     # Architecture documentation
│   ├── api/              # API documentation
│   └── deployment/       # Deployment guides
├── tests/                 # All project tests
│   ├── integration/      # Integration tests
│   ├── unit/             # Unit tests
│   └── e2e/              # End-to-end tests
├── configs/               # Configuration files
├── environments/          # Environment configurations
└── .github/              # GitHub workflows and templates
```

## Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- Docker & Docker Compose

### Installation and Setup

```bash
# Complete project setup (recommended for first time)
npm run setup:complete

# Or step by step:
npm run install:all
npm run setup:environment
npm run setup:dev
```

### Development

```bash
# Start development environment
npm run dev

# Start with Docker
npm run docker:dev

# Start specific services
npm run dev:frontend
npm run dev:backend
npm run dev:mcp
```

## Database Configuration

VentAI supports multiple database configurations:
- **SQLite** - for quick development and testing
- **PostgreSQL** - for production deployment and advanced development

### Using PostgreSQL and Redis

To run with PostgreSQL and Redis:

```bash
# Start PostgreSQL and Redis with Docker
npm run docker:db

# Start backend with PostgreSQL and Redis
npm run dev:backend:postgres

# Or use the setup script
./scripts/setup-project.sh --with-postgres
```

### Environment Management

Environment configurations are located in `environments/`:
- `.env.development` - Development settings
- `.env.production.template` - Production template
- `.env.local.template` - Local override template

## Scripts and Tools

### Project Management
```bash
npm run setup:complete      # Complete project setup
npm run validate:workflow   # Validate development workflow
npm run clean:all          # Clean all build artifacts
```

### Development Tools
```bash
npm run lint               # Run all linters
npm run format             # Format all code
npm run test:all          # Run all tests
npm run build:all         # Build all components
```

### Docker Operations
```bash
npm run docker:dev         # Start development environment
npm run docker:prod        # Start production environment
npm run docker:db          # Start database services only
npm run docker:clean       # Clean Docker resources
```

## Documentation

- [Architecture](docs/architecture/) - System architecture and design
- [API Documentation](docs/api/) - API endpoints and schemas
- [Deployment Guide](docs/deployment/) - Deployment instructions
- [PostgreSQL Integration](docs/POSTGRES_REDIS_INTEGRATION.md) - Database migration guide

## Development Workflow

1. **Setup**: Run `npm run setup:complete` for initial setup
2. **Development**: Use `npm run dev` for development server
3. **Testing**: Run `npm run test:all` before commits
4. **Validation**: Use `npm run validate:workflow` to check setup
5. **Production**: Deploy with `npm run docker:prod`

## Можливості

- **HVAC розрахунки** - Повний набір інженерних розрахунків
- **AI інтеграція** - Інтелектуальні підказки та автоматизація
- **Responsive дизайн** - Робота на всіх пристроях
- **Звітність** - Генерація професійних звітів
- **Безпека** - Сучасні методи аутентифікації

## Розробка

Детальна інформація по розробці знаходиться в [docs/development](docs/development/).

## Документація

- [API Documentation](docs/api/)
- [User Guide](docs/user-guide/)
- [Architecture](docs/architecture/)

## Troubleshooting

### Docker Build Issues
1. If seeing 'path not found' errors:
   ```bash
   docker system prune -a -f --volumes
   rm -rf deployment/docker/.cache
   ```
2. Rebuild with:
   ```bash
   docker-compose -f docker-compose.yml -f deployment/docker/docker-compose.dev.yml up --build
   ```

### Missing Frontend Files
- Ensure `src/index.js` exists with basic React render setup
- Verify all dependencies are installed (`npm install`)

---

**Версія**: 2.0.0 - Reorganized Architecture
