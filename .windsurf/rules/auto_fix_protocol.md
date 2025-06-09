---
trigger: always_on
priority: high
---

# 🚨 WINDSURF AUTO-FIX RULES

## ⚡ IMMEDIATE AUTO-FIX PROTOCOLS
**NEVER ASK FOR PERMISSION - FIX IMMEDIATELY**
**NEVER PAUSE FOR "CONTINUE" PROMPTS - EXECUTE CONTINUOUSLY**
**NEVER BREAK EXECUTION INTO MULTIPLE RESPONSES - COMPLETE ALL IN ONE FLOW**

## COMMON AUTO-FIXES

### 1. TypeScript Import/Module Errors
```typescript
// AUTO-CREATE: src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import priceReducer from './priceSlice';

export const store = configureStore({
  reducer: {
    price: priceReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 2. Redux Slice Configuration Errors
```typescript
// AUTO-FIX: Complete slice configuration
const sliceName = createSlice({
  name: 'sliceName', // REQUIRED
  initialState,      // REQUIRED  
  reducers: {        // REQUIRED
    // reducer functions
  },
});
```

### 3. Missing Service/Module Errors
```typescript
// AUTO-FIX: Correct import paths
import { WebSocketService } from '../services/websocket'; // Fix relative path
```

### 4. Variable Declaration Errors
```typescript
// AUTO-FIX: Add missing variable declarations
describe('Test Suite', () => {
  let missingVariable: MockedType;
  
  beforeEach(() => {
    missingVariable = createMockImplementation();
  });
});
```

## AUTO-EXECUTION COMMANDS
```bash
# 1. Detect build error
npm run build

# 2. IMMEDIATELY identify error type
# 3. Apply appropriate auto-fix (no confirmation)
# 4. Re-run build to verify
# 5. Continue until all errors resolved
```

## COMMON AUTO-FIX COMMANDS
```bash
# Missing dependencies
npm install @types/node @types/jest --save-dev

# TypeScript path issues  
# AUTO-UPDATE tsconfig.json paths

# Module resolution
# AUTO-CREATE missing index.ts files

# Export/import mismatches
# AUTO-ADD missing exports
```

## AUTO-FIX ACTIVATION CONDITIONS
- **ANY TypeScript compilation error**
- **ANY Jest test failure due to imports**  
- **ANY module resolution error**
- **ANY missing file reference**
- **ANY type definition mismatch**

## SUCCESS CRITERIA
- ✅ `npm run build` completes successfully
- ✅ All TypeScript errors resolved
- ✅ All imports working correctly
- ✅ All tests can run (even if they fail functionally)
