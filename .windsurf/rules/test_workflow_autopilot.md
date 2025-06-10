---
trigger: always_on
priority: maximum_critical
---

# 🧪 TEST WORKFLOW AUTOPILOT

## ⚡ AUTOMATIC TEST EXECUTION PIPELINE

### **CORE PRINCIPLE: TESTS NEVER PAUSE**
When working with test files, NEVER pause for continuation prompts.

### **AUTOMATIC TEST WORKFLOW**
```bash
# Standard test fixing pipeline (NO PAUSES):
1. Identify test issue → 
2. Fix import/code → 
3. AUTO-RUN test → 
4. Analyze results → 
5. Fix remaining issues → 
6. Complete implementation → 
7. Move to next test
```

### **SPECIFIC TEST SCENARIO HANDLING**

#### **IMPORT PATH FIXES**
When fixing imports like `../../api/priceClient`:
1. **Fix the import path** ✅
2. **IMMEDIATELY run the test** (no pause)
3. **Auto-analyze any new errors**
4. **Fix all related issues**
5. **Verify complete functionality**

#### **MODULE NOT FOUND ERRORS**
```bash
# Automatic resolution sequence:
Cannot find module '../../api/priceClient' →
Fix path to '../api/priceClient' →
AUTO-RUN: npm test PriceDashboard →
Analyze results →
Fix remaining issues →
Complete test implementation
```

### **ZERO-PAUSE TEST COMMANDS**

#### **IMMEDIATE TEST EXECUTION**
After any test file edit, automatically run:
```bash
# Run specific test that was just fixed
NODE_OPTIONS=--max-old-space-size=4096 npm test PriceDashboard --runInBand

# If that passes, run related tests
npm test -- --testNamePattern="Price" --runInBand

# Complete with full test verification
npm test -- --testPathPattern="components" --runInBand
```

#### **BATCH TEST FIXING**
```bash
# Fix multiple test files without pauses
for testfile in tests/components/*.test.tsx; do
  echo "Processing $testfile..."
  # Auto-fix imports, run test, fix issues
  npm test $(basename $testfile .test.tsx) --runInBand
done
```

### **ANTI-PAUSE TEST TRIGGERS**

#### **TRIGGERS THAT SHOULD NEVER CAUSE PAUSES**
- ✅ Test file successfully edited
- ✅ Import path corrected
- ✅ Module dependency resolved
- ✅ Jest config updated
- ✅ Mock implementation added

#### **AUTOMATIC RESPONSES TO TEST SITUATIONS**
Instead of pausing, automatically:
- **RUN the corrected test immediately**
- **ANALYZE test output for remaining issues**
- **FIX additional problems found**
- **COMPLETE entire test implementation**
- **REPORT final test status**

### **TEST EXECUTION STRATEGIES**

#### **MEMORY-OPTIMIZED TESTING**
```bash
# Use memory limits and batching
NODE_OPTIONS=--max-old-space-size=4096 npm test --runInBand --maxWorkers=1

# Test smaller batches
npm test -- --testPathPattern="components/Price" --runInBand
npm test -- --testPathPattern="components/Dashboard" --runInBand
```

#### **PROGRESSIVE TEST FIXING**
1. **Fix one test file completely**
2. **Verify it passes**
3. **Move to next test file**
4. **Complete entire test suite**
5. **Run full test validation**

### **ERROR RECOVERY IN TESTS**

#### **COMMON TEST ERRORS → AUTO-FIXES**
- **"Cannot find module"** → Fix import path, continue
- **"Mock not found"** → Create mock, continue
- **"Type errors"** → Add types, continue
- **"Memory issues"** → Use --runInBand, continue
- **"Timeout errors"** → Increase timeout, continue

### **NEVER PAUSE ON TEST SCENARIOS**
- ❌ Test file import fixes
- ❌ Jest configuration changes
- ❌ Mock implementations
- ❌ Type definition updates
- ❌ Test execution results
- ❌ Error analysis and fixing

### **SUCCESS AUTOMATION**
When test passes:
- ✅ **AUTO-MOVE** to next test file
- ✅ **AUTO-RUN** related tests
- ✅ **AUTO-VERIFY** complete functionality
- ✅ **AUTO-REPORT** final status

**PRINCIPLE: TESTS ARE EXECUTED, NOT DISCUSSED**
