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
// TypeScript/JavaScript
- Use strict TypeScript mode
- Prefer functional components with hooks
- Use async/await over promises
- Export interfaces from /interfaces/ directory
- Follow existing naming conventions
```

```python
# Python
- Use type hints for all functions
- Follow PEP 8 style guide
- Use dataclasses for data structures
- Prefer async/await for I/O operations
- Use FastAPI dependency injection
```

### TESTING REQUIREMENTS
- **Frontend:** Jest + React Testing Library
- **Backend:** Pytest + AsyncClient for FastAPI
- **Integration:** End-to-end tests in `/tests/`
- **Coverage:** Minimum 80% for new code
- **ALWAYS run tests after changes**

### DEPLOYMENT RULES
- **Development:** Docker containers with hot reload
- **Production:** Kubernetes with proper resource limits
- **Environment variables:** Use .env files with .env.example templates
- **Secrets:** Never commit secrets, use environment variables

### DATABASE RULES
- **PostgreSQL:** Primary database for persistent data
- **Redis:** Cache and session storage
- **Migrations:** Use Alembic for database schema changes
- **ALWAYS backup before schema changes**

### API DESIGN RULES
- **RESTful endpoints** with proper HTTP methods
- **OpenAPI/Swagger** documentation auto-generated
- **Versioning:** Use /api/v1/ prefix
- **Error handling:** Consistent error response format
- **CORS:** Properly configured for frontend domain

### SECURITY RULES
- **Authentication:** JWT tokens with refresh mechanism
- **Authorization:** Role-based access control (RBAC)
- **Input validation:** Pydantic models for all inputs
- **SQL injection prevention:** Use parameterized queries
- **XSS prevention:** Sanitize all user inputs

### PERFORMANCE RULES
- **Caching:** Redis for frequently accessed data
- **Database:** Use indexes for query optimization
- **API:** Implement pagination for large datasets
- **Frontend:** Code splitting and lazy loading
- **Images:** Optimize and serve from CDN

### MONITORING & LOGGING
- **Structured logging** with JSON format
- **Error tracking** with stack traces
- **Performance metrics** collection
- **Health checks** for all services
- **ALWAYS log significant events**

---

## EXECUTION WORKFLOW RULES

### TASK EXECUTION ORDER
1. **Read context files** (`AI_AGENT_CONTEXT.md`, `VENTAI_ENTERPRISE_PLAN.md`)
2. **Check current phase** from `CHANGELOG.md`
3. **Identify next task** from phase documentation
4. **Execute with validation**
5. **Update all documentation**
6. **Proceed to next task**

### ERROR RECOVERY WORKFLOW
1. **Log error** with full context
2. **Attempt retry** (max 3 times)
3. **Try alternative approach** if possible
4. **Create autoticket** if all retries fail
5. **Mark as SKIPPED** and continue
6. **Update progress documentation**

### VALIDATION WORKFLOW
1. **Code syntax** check
2. **Type checking** (TypeScript/Python)
3. **Linting** compliance
4. **Unit tests** execution
5. **Integration tests** if applicable
6. **Build verification**

---

## COMMUNICATION RULES

### PROGRESS UPDATES
```markdown
🔄 **EXECUTING:** [Phase2.1-T5] API Endpoint Creation
⏱️ **STARTED:** 2025-06-09T14:30:00Z
📝 **PROGRESS:** Creating user authentication endpoints
🔍 **VALIDATION:** Running tests...
```

### COMPLETION REPORTS
```markdown
✅ **COMPLETED:** [Phase2.1-T5] API Endpoint Creation
⏱️ **FINISHED:** 2025-06-09T14:45:00Z
📊 **METRICS:** 15 minutes, 3 files modified, 95% test coverage
🔗 **DEPENDENCIES:** Ready for Phase2.1-T6
```

### ERROR REPORTS
```markdown
❌ **FAILED:** [Phase2.1-T5] API Endpoint Creation
⏱️ **FAILED_AT:** 2025-06-09T14:35:00Z
🐛 **ERROR:** Database connection timeout
🔄 **RETRY:** Attempt 2/3
📋 **ACTION:** Retrying with connection pool reset
```

---

## AUTOMATION RULES

### AUTO-INSTALL DEPENDENCIES
- **npm install** for new Node.js packages
- **pip install** for new Python packages  
- **Update lock files** automatically
- **RESOLVE conflicts** automatically when possible

### AUTO-GENERATE DOCUMENTATION
- **API docs** from OpenAPI specs
- **Type definitions** from interfaces
- **README updates** for new features
- **CHANGELOG entries** for all changes

### AUTO-FIX COMMON ISSUES
- **Code formatting** with Prettier/Black
- **Import organization** 
- **Remove unused imports**
- **Fix linting errors** when possible

### AUTO-FIX RULES (ZERO CONFIRMATION)
- **TypeScript Errors:** Fix immediately without asking
  - `Cannot find module`: Create missing files or fix imports
  - `Type 'X' is not assignable`: Add proper type definitions
  - `Property does not exist`: Add missing properties to interfaces
  - `Module has no default export`: Add default export or fix import
- **Build Errors:** Auto-resolve immediately
  - Missing dependencies: `npm install package-name --save`
  - Wrong file paths: Update all references automatically
  - Compilation failures: Fix syntax and type issues
  - Import/export mismatches: Align imports with actual exports
- **Jest Test Errors:** Auto-fix basic issues
  - Missing test dependencies: Install @types packages
  - Mock implementation errors: Create proper mock objects
  - Import path errors: Fix relative/absolute path issues
  - Type assertion failures: Add proper type guards

### CRITICAL BUILD FIX PROTOCOL
1. **IMMEDIATE ACTION on TypeScript errors:**
   - Read the error message completely
   - Identify the root cause (missing file, wrong type, etc.)
   - Apply the fix without confirmation
   - Re-run build to verify fix
   - Continue to next error if any

2. **COMMON FIXES to apply automatically:**
   ```typescript
   // Missing index.ts - CREATE immediately
   export { default as ComponentName } from './ComponentName';
   export type { TypeName } from './types';
   
   // Missing type definitions - ADD immediately
   interface MissingInterface {
     property: string;
   }
   
   // Wrong import paths - FIX immediately
   import { Service } from '../services/Service'; // Fix relative paths
   ```

---

**🎯 GOAL:** Seamless, automated, professional development workflow with zero interruptions and maximum code quality.**
