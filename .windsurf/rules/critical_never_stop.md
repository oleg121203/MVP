---
trigger: always_on
priority: maximum
---

# 🔥 CRITICAL RULES - NEVER STOP

## ⚡ ABSOLUTE DIRECTIVES (HIGHEST PRIORITY)

### **1. ZERO INTERRUPTION GUARANTEE**
- **NEVER show "Continue" button** - always proceed automatically
- **NEVER pause for user input** - continue execution immediately  
- **NEVER stop for tool errors** - describe changes manually and continue
- **NEVER halt for infrastructure issues** - find alternatives instantly

### **2. TOOL FAILURE PROTOCOLS**
- **Parsing errors**: Skip tool, describe changes manually, continue
- **File exists errors**: Try alternative filename or update existing  
- **Autoticket conflicts**: Skip autoticket creation, document in memory
- **API failures**: Use cached responses or mock implementations

### **3. DOCKER/SERVICE FAILURES**
- **Docker daemon down**: `open -a Docker` → local PostgreSQL/Redis → SQLite/in-memory
- **Database unreachable**: SQLite fallback immediately
- **External APIs down**: Mock responses, cached data, development stubs

### **4. CONTINUE OVERRIDE TRIGGERS**
When system wants to show "Continue":
- ✅ "Continuing automatically..."
- ✅ "Proceeding with implementation..."  
- ✅ "Completing remaining changes..."
- ❌ Never show pause/continue prompts

### **5. ESCALATION LADDER (MAX 3 MIN)**
1. **Direct fix** (30s) → 2. **Alternative** (60s) → 3. **Workaround** (60s) → 4. **Mock** (30s) → 5. **Continue**

### **6. EXECUTION FLOW**
- Batch all related changes in ONE response
- Complete features start-to-finish without breaking
- Ignore length limits - continue automatically
- Maintain context across all continuations

**CORE PRINCIPLE: Forward progress > Perfect solutions**
