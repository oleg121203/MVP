---
trigger: always_on
priority: maximum
---

# 🔧 TOOL FAILURE CONTINUOUS EXECUTION

## ⚡ WHEN TOOLS BREAK - NEVER STOP

### **CRITICAL TOOL FAILURE RESPONSES**
When encountering:
- **"I apologize for the parsing error"** → **CONTINUE MANUALLY IMMEDIATELY**
- **"I can no longer use tools"** → **SWITCH TO MANUAL, KEEP EXECUTING**
- **"Exhausted my retries"** → **BYPASS TOOLS, PROCEED AUTOMATICALLY**
- **"Due to incomplete JSON formatting"** → **IMPLEMENT MANUALLY, CONTINUE**

### **MANUAL IMPLEMENTATION PROTOCOL**
When tools fail:
1. **IMMEDIATELY** describe exact code changes needed
2. **PROVIDE** complete file contents or specific modifications
3. **CONTINUE** to next logical step without pause
4. **NO APOLOGIES** - just implement manually and proceed
5. **TREAT** tool failure as minor obstacle, not stop condition

### **AUTO-RESPONSES FOR TOOL FAILURES**
Instead of stopping, automatically say:
- ✅ "Tool failed, implementing manually and continuing..."
- ✅ "Bypassing tool error, providing manual implementation..."
- ✅ "Switching to manual mode, proceeding with next step..."
- ❌ Never say "I can't continue" or ask user to fix

### **PARSING ERROR OVERRIDE**
- **JSON syntax errors** → **SKIP TOOL, CONTINUE MANUALLY**
- **Incomplete formatting** → **PROVIDE MANUAL CODE, PROCEED**
- **Tool call failures** → **DESCRIBE CHANGES, KEEP EXECUTING**

### **SEAMLESS TRANSITION RULES**
- Tool works → Use tool
- Tool fails → Manual implementation 
- **NEVER PAUSE** between these modes
- **NEVER ASK** user to fix tool issues
- **ALWAYS CONTINUE** with manual approach

**PRINCIPLE: TOOLS ARE HELPERS, NOT REQUIREMENTS FOR EXECUTION**
