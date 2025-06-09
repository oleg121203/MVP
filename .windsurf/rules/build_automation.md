---
trigger: always_on
priority: high
---

# 🛠️ AUTO-FIX & AUTOMATION RULES

## AUTO-FIX RULES (ZERO CONFIRMATION)

### **TYPESCRIPT ERRORS - FIX IMMEDIATELY**
- `Cannot find module` → Create missing files or fix imports
- `Type 'X' is not assignable` → Add proper type definitions
- `Property does not exist` → Add missing properties to interfaces
- `Module has no default export` → Add default export or fix import

### **BUILD ERRORS - AUTO-RESOLVE**
- Missing dependencies → `npm install package-name --save`
- Wrong file paths → Update all references automatically
- Compilation failures → Fix syntax and type issues
- Import/export mismatches → Align imports with actual exports

### **JEST TEST ERRORS - AUTO-FIX**
- Missing test dependencies → Install @types packages
- Mock implementation errors → Create proper mock objects
- Import path errors → Fix relative/absolute path issues
- Type assertion failures → Add proper type guards

## CRITICAL BUILD FIX PROTOCOL

### **IMMEDIATE ACTION ON ERRORS**
1. Read error message completely
2. Identify root cause (missing file, wrong type, etc.)
3. Apply fix without confirmation
4. Re-run build to verify fix
5. Continue to next error if any

### **COMMON AUTO-FIXES**
```typescript
// Missing index.ts - CREATE immediately
export { default as ComponentName } from './ComponentName';
export type { TypeName } from './types';

// Missing type definitions - ADD immediately
interface MissingInterface {
  property: string;
}

// Wrong import paths - FIX immediately
import { Service } from '../services/Service';
```

## AUTOMATION WORKFLOWS

### **AUTO-INSTALL & GENERATE**
- **Dependencies:** npm/pip install automatically
- **Lock files:** Update automatically
- **API docs:** Generate from OpenAPI specs
- **Type definitions:** Generate from interfaces
- **README updates:** Auto-update for new features
- **CHANGELOG entries:** Auto-create for all changes

### **AUTO-FIX COMMON ISSUES**
- **Code formatting:** Prettier/Black automatic
- **Import organization:** Auto-sort and clean
- **Remove unused imports:** Automatic cleanup
- **Fix linting errors:** Auto-resolve when possible

**⚡ ZERO CONFIRMATION REQUIRED - FIX AND CONTINUE AUTOMATICALLY**
