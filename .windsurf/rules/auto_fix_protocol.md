# 🚨 WINDSURF AUTO-FIX RULES - COMPILATION ERRORS

## ⚡ IMMEDIATE AUTO-FIX PROTOCOLS

### ZERO-CONFIRMATION FIXES
**NEVER ASK FOR PERMISSION - FIX IMMEDIATELY:**

#### 1. TypeScript Import/Module Errors
```bash
# Error: Cannot find module '.' or its corresponding type declarations
# FIX: Create missing index.ts with proper exports
```

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

#### 2. Redux Slice Configuration Errors
```bash
# Error: Type '{}' is not assignable to parameter of type 'CreateSliceOptions'
# FIX: Add required properties to createSlice
```

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

#### 3. Missing Service/Module Errors
```bash
# Error: Cannot find module '../../services/websocket'
# FIX: Update import path or create missing service
```

```typescript
// AUTO-FIX: Correct import paths
import { WebSocketService } from '../services/websocket'; // Fix relative path
```

#### 4. Variable Declaration Errors
```bash
# Error: Cannot find name 'variableName'
# FIX: Declare missing variables in test context
```

```typescript
// AUTO-FIX: Add missing variable declarations
describe('Test Suite', () => {
  let missingVariable: MockedType;
  
  beforeEach(() => {
    missingVariable = createMockImplementation();
  });
});
```

---

## 🔧 WINDSURF AUTO-EXECUTION COMMANDS

### BUILD ERROR WORKFLOW
```bash
# 1. Detect build error
npm run build

# 2. IMMEDIATELY identify error type
# 3. Apply appropriate auto-fix (no confirmation)
# 4. Re-run build to verify
# 5. Continue until all errors resolved
```

### COMMON AUTO-FIX COMMANDS
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

---

## 🎯 WINDSURF EXECUTION TRIGGERS

### AUTO-FIX ACTIVATION CONDITIONS
- **ANY TypeScript compilation error**
- **ANY Jest test failure due to imports**  
- **ANY module resolution error**
- **ANY missing file reference**
- **ANY type definition mismatch**

### EXECUTION PRIORITY
1. **HIGHEST:** Build-breaking errors
2. **HIGH:** Test compilation failures
3. **MEDIUM:** Type safety warnings
4. **LOW:** Linting suggestions

### SUCCESS CRITERIA
- ✅ `npm run build` completes successfully
- ✅ All TypeScript errors resolved
- ✅ All imports working correctly
- ✅ All tests can run (even if they fail functionally)

---

## 🚀 ACTIVATION PROTOCOL

**TO TRIGGER AUTO-FIX MODE:**
1. Any build command failure
2. TypeScript compiler errors
3. Module resolution failures
4. Import/export mismatches

**EXECUTION FLOW:**
```
Error Detected → Analyze Error Type → Apply Auto-Fix → Verify Fix → Continue
```

**NEVER:**
- Ask for confirmation on standard fixes
- Pause execution for common errors
- Request input for missing files
- Wait for approval on dependency installation

**ALWAYS:**
- Fix immediately upon detection
- Log the fix in progress updates
- Verify fix worked before continuing
- Update documentation with changes made

---

**⚡ REMEMBER: Speed and autonomy are critical. Fix first, document second, ask never.**
