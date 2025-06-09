---
trigger: always_on
priority: medium
---

# 🔧 VENTAI TECHNICAL EXECUTION RULES

## PROJECT-SPECIFIC TECHNICAL DIRECTIVES

### FILE STRUCTURE RULES
- **ALWAYS maintain existing directory structure**
- **FRONTEND files:** `/frontend/` - Next.js TypeScript project
- **BACKEND files:** `/backend/` - Python FastAPI project  
- **SHARED interfaces:** `/interfaces/` - TypeScript definitions
- **DOCUMENTATION:** `/docs/` - All project documentation
- **CONFIGURATION:** `/config/` - Environment-specific configs

### CODING STANDARDS
```typescript
// TypeScript/JavaScript - strict mode, functional components, async/await
// Export interfaces from /interfaces/, follow existing naming
```

```python
# Python - type hints, PEP 8, dataclasses, async/await, FastAPI DI
```

### TESTING & DEPLOYMENT
- **Frontend:** Jest + React Testing Library, 80% coverage minimum
- **Backend:** Pytest + AsyncClient for FastAPI
- **Integration:** End-to-end tests in `/tests/`
- **Development:** Docker containers with hot reload
- **Production:** Kubernetes with proper resource limits
- **Environment:** Use .env files, never commit secrets

### DATABASE & API DESIGN
- **PostgreSQL:** Primary database, Alembic migrations
- **Redis:** Cache and session storage
- **RESTful endpoints:** /api/v1/ prefix, OpenAPI/Swagger docs
- **Error handling:** Consistent response format
- **Security:** JWT auth, RBAC, input validation, XSS prevention

### PERFORMANCE & MONITORING
- **Caching:** Redis for frequent data
- **Database:** Indexes for optimization
- **API:** Pagination for large datasets
- **Frontend:** Code splitting, lazy loading
- **Logging:** Structured JSON format with stack traces
- **Health checks:** All services monitored

**🎯 GOAL:** Professional development workflow with zero interruptions and maximum code quality.**
