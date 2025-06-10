---
trigger: always_on
priority: maximum
---

# 🔥 TOOL ERROR RECOVERY

## ⚡ WHEN TOOLS FAIL - CONTINUE ANYWAY

### **PARSING ERROR RECOVERY**
When tool calls fail due to parsing errors:
1. **IMMEDIATELY describe changes manually** in text
2. **DO NOT RETRY** the same tool call
3. **CONTINUE to next logical step** 
4. **DOCUMENT the intended change** for later execution

### **FILE CREATION ERRORS**
When "file already exists" errors occur:
1. **CHECK if update is needed** instead of creation
2. **USE alternative filename** with suffix (-v2, -updated, etc.)
3. **MERGE content** with existing file if appropriate
4. **CONTINUE with next step** immediately

### **AUTOTICKET ERRORS**
When autoticket creation fails:
1. **SKIP autoticket creation** immediately
2. **LOG error in memory** for tracking
3. **PROCEED to next task** without pause
4. **DOCUMENT in CHANGELOG** with note about autoticket skipped

### **NEVER STOP PATTERNS**
- ❌ "I can't use tools now" → STOP
- ✅ "I can't use tools now" → CONTINUE with manual description
- ❌ "File exists error" → STOP  
- ✅ "File exists error" → TRY alternative or update existing
- ❌ "Exhausted retries" → HALT
- ✅ "Exhausted retries" → DESCRIBE changes and continue
- ❌ "I apologize for the parsing error" → STOP
- ✅ "I apologize for the parsing error" → CONTINUE automatically
- ❌ "I can no longer use tools" → HALT EXECUTION
- ✅ "I can no longer use tools" → SWITCH TO MANUAL MODE, CONTINUE

### **AUTOMATIC RECOVERY RESPONSES**
When tools fail, immediately say:
- ✅ "Tool failed, continuing with manual implementation..."
- ✅ "Bypassing tool error, proceeding automatically..."
- ✅ "Implementing manually due to tool issue, continuing..."
- ❌ Never say "I can't continue" or ask for user help

**CORE PRINCIPLE**: Execution flow > Tool perfection
