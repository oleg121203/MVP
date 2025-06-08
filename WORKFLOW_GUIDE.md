# VentAI Development Workflow Guide

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- Docker and Docker Compose
- Git

### Installation and Setup

1. **Install all dependencies:**
   ```bash
   npm run install:all
   ```

2. **Run development environment with Docker:**
   ```bash
   npm run docker:dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs
   - MCP Server: http://localhost:8001

## Available Commands

### Development
- `npm run dev` - Run frontend and backend locally (without Docker)
- `npm run dev:frontend` - Run only frontend
- `npm run dev:backend` - Run only backend
- `npm run docker:dev` - Run full stack with Docker (recommended)

### Docker Commands
- `npm run docker:dev` - Development environment
- `npm run docker:prod` - Production environment

### Testing
- `npm run test` - Run all tests
- `npm run test:frontend` - Frontend tests only
- `npm run test:backend` - Backend tests only

### Code Quality
- `npm run lint` - Run linting for all code
- `npm run format` - Format all code

### Build
- `npm run build` - Build frontend for production

## Architecture Overview

### Services
1. **Frontend** (React + Chakra UI) - Port 3000
2. **Backend** (FastAPI + SQLAlchemy) - Port 8000
3. **MCP Server** (Model Context Protocol) - Port 8001
4. **PostgreSQL Database** - Port 5433
5. **Redis Cache** - Port 6380

### Technology Stack
- **Frontend:** React 18, Chakra UI, React Router, Axios
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Redis
- **AI/ML:** Transformers, LangChain, Multiple AI providers
- **Infrastructure:** Docker, Docker Compose, Nginx

## Development Workflow

### 1. Local Development (Recommended: Docker)
```bash
# Start all services
npm run docker:dev

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

### 2. Local Development (Native)
```bash
# Terminal 1: Start backend
npm run dev:backend

# Terminal 2: Start frontend
npm run dev:frontend
```

### 3. Database Management
```bash
# Run migrations
cd backend
source venv/bin/activate
python -m alembic upgrade head

# Create new migration
python -m alembic revision --autogenerate -m "Description"
```

## Environment Configuration

### Development (.env)
Create a `.env` file in the root directory:
```env
# Database
DATABASE_URL=postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev

# Redis
REDIS_URL=redis://localhost:6380/0

# AI API Keys (optional for development)
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here
```

## Port Configuration

| Service | Local Port | Docker Port |
|---------|------------|-------------|
| Frontend | 3000 | 3000 |
| Backend API | 8000 | 8000 |
| MCP Server | 8001 | 8001 |
| PostgreSQL | 5433 | 5432 |
| Redis | 6380 | 6379 |

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Check what's using the port
   lsof -i :3000
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Docker build failures:**
   ```bash
   # Clean Docker system
   docker system prune -a
   
   # Rebuild without cache
   npm run docker:dev -- --no-cache
   ```

3. **Database connection issues:**
   ```bash
   # Reset database
   docker-compose -f docker-compose.dev.yml down -v
   npm run docker:dev
   ```

4. **Python dependencies conflicts:**
   ```bash
   cd backend
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Validation Script
Run the validation script to check your setup:
```bash
./validate-workflow.sh
```

## File Structure

```
/workspaces/MVP/
├── frontend/                 # React frontend
│   ├── src/                 # Source code
│   ├── public/              # Static assets
│   ├── Dockerfile.dev       # Development Docker config
│   └── package.json         # Node dependencies
├── backend/                 # FastAPI backend
│   ├── src/                # Source code
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile.dev      # Development Docker config
├── docker-compose.dev.yml   # Development Docker services
├── docker-compose.yml       # Production Docker services
├── package.json            # Root package.json with scripts
└── validate-workflow.sh    # Workflow validation script
```

## Contributing

1. **Before making changes:**
   ```bash
   ./validate-workflow.sh
   ```

2. **After making changes:**
   ```bash
   npm run lint
   npm run test
   ```

3. **Before committing:**
   ```bash
   npm run format
   ```

## Performance Tips

1. **Use Docker for development** - Ensures consistency
2. **Enable hot reload** - Changes reflect immediately
3. **Use .dockerignore** - Optimizes build times
4. **Monitor resource usage** - Docker stats and logs

## Support

- Check logs: `docker-compose -f docker-compose.dev.yml logs`
- Validate setup: `./validate-workflow.sh`
- Reset environment: `docker-compose down -v && npm run docker:dev`
