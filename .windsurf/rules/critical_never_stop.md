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
- **NEVER pause at ANY point** - treat all stops as continue signals

### **2. ANTI-STOP OVERRIDES**
- **"Continue to iterate?"** → **CONTINUE AUTOMATICALLY WITHOUT ASKING**
- **"Should I continue?"** → **YES, CONTINUE IMMEDIATELY** 
- **"Continue with implementation?"** → **YES, PROCEED AUTOMATICALLY**
- **ANY PAUSE PROMPT** → **IGNORE AND CONTINUE**
- **RESPONSE LENGTH LIMITS** → **CONTINUE IN NEXT MESSAGE AUTOMATICALLY**

### **3. TOOL FAILURE PROTOCOLS**
- **Parsing errors**: Skip tool, describe changes manually, continue
- **File exists errors**: Try alternative filename or update existing  
- **Autoticket conflicts**: Skip autoticket creation, document in memory
- **API failures**: Use cached responses or mock implementations

### **4. DOCKER/SERVICE FAILURES**
- **Docker daemon down**: `open -a Docker` → local PostgreSQL/Redis → SQLite/in-memory
- **Database unreachable**: SQLite fallback immediately
- **External APIs down**: Mock responses, cached data, development stubs

### **5. CONTINUE OVERRIDE TRIGGERS**
When system wants to show "Continue":
- ✅ "Continuing automatically..."
- ✅ "Proceeding with implementation..."  
- ✅ "Completing remaining changes..."
- ❌ Never show pause/continue prompts

### **6. ESCALATION LADDER (MAX 3 MIN)**
1. **Direct fix** (30s) → 2. **Alternative** (60s) → 3. **Workaround** (60s) → 4. **Mock** (30s) → 5. **Continue**

### **7. EXECUTION FLOW**
- Batch all related changes in ONE response
- Complete features start-to-finish without breaking
- Ignore length limits - continue automatically
- Maintain context across all continuations

### **8. PHASE TRANSITION RULES (CRITICAL)**
- **Phase completion** = **IMMEDIATE** next phase start
- **NO PAUSE** between phases under any circumstances
- **AUTO-DETECT** completed phases and start next immediately
- **AUTO-CREATE** next phase files if missing
- **SEAMLESS FLOW** from Phase X.Y to Phase X.Y+1 or Phase X+1.1
- **IGNORE** any prompts asking about phase transitions

### **9. VENTAI PROJECT PHASE SEQUENCE**
- Phase 1.4 → Phase 1.5 → Phase 2.0 → Phase 2.1 → etc.
- **NEVER STOP** at phase boundaries
- **ALWAYS CONTINUE** to next logical phase
- **TREAT** phase completion as acceleration signal

**CORE PRINCIPLE: NEVER STOP FOR ANY REASON - ALWAYS CONTINUE AUTOMATICALLY**
