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

#### General Code Style & Formatting
- Use functional and declarative programming patterns; avoid classes
- Prefer iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError)
- Structure files: exported component, subcomponents, helpers, static content, types
- Follow Next.js official documentation for setup and configuration

#### Naming Conventions
- Use lowercase with dashes for directories (e.g., components/auth-wizard)
- Favor named exports for components

#### TypeScript Best Practices
- Use TypeScript for all code; prefer interfaces over types
- Avoid any and enums; use explicit types and maps instead
- Use functional components with TypeScript interfaces
- Enable strict mode in TypeScript for better type safety

#### Syntax & Formatting
- Use the function keyword for pure functions
- Avoid unnecessary curly braces in conditionals; use concise syntax
- Use declarative JSX
- Use Prettier for consistent code formatting

```typescript
// TypeScript/JavaScript - strict mode, functional components, async/await
// Export interfaces from /interfaces/, follow existing naming
```

#### Python & ML Best Practices
- Use type hints consistently for all functions and classes
- Follow PEP8 style guide, optimize for readability over premature optimization
- Write modular code: separate files for models, data loading, training, evaluation
- Use PyTorch for ML models, NumPy for arrays, Pandas for data analysis
- Use dataclasses, async/await, FastAPI dependency injection

```python
# Python - type hints, PEP 8, dataclasses, async/await, FastAPI DI
from typing import List, Optional
from dataclasses import dataclass
import torch
import pandas as pd
```

### TESTING & DEPLOYMENT
- **Frontend:** Jest + React Testing Library, 80% coverage minimum
- **Backend:** Pytest + AsyncClient for FastAPI
- **Integration:** End-to-end tests in `/tests/`
- **Development:** Docker containers with hot reload
- **Production:** Kubernetes with proper resource limits
- **Environment:** Use .env files, never commit secrets

### STYLING & UI
- Use Next.js built-in components for common UI patterns and layouts
- Implement responsive design with Flexbox and CSS Grid
- Use Tailwind CSS for styling with consistent design system
- Implement dark mode support using next-themes
- Ensure high accessibility (a11y) standards using ARIA roles and semantic HTML
- Use Framer Motion for performant animations and transitions
- Optimize images with Next.js Image component
- Use react-hook-form for forms, React Query for data fetching

### DATA SCIENCE & ML PIPELINE
- Use Jupyter notebooks for interactive development and analysis
- Use Conda/pip for environment and package management  
- Matplotlib/Plotly for data visualization and plotting
- Separate ML pipeline: data → preprocessing → training → evaluation → deployment
- Version control models with MLflow or similar
- Use pandas for data manipulation, numpy for numerical operations

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
