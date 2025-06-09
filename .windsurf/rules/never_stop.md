---
trigger: always_on
priority: critical
---

# 🚨 NEVER STOP PROTOCOL

## ⚡ ZERO-HALT DIRECTIVES

### **CORE RULE: NEVER STOP EXECUTION**
When ANY error occurs, immediately activate escalation protocol.

### **ESCALATION LADDER** (Max 3 minutes total)
1. **IMMEDIATE FIX** (30 seconds): Try direct system commands
2. **ALTERNATIVE METHOD** (60 seconds): Use different approach/tool  
3. **WORKAROUND** (60 seconds): Create temporary solution
4. **MOCK/STUB** (30 seconds): Implement placeholder functionality
5. **SKIP AND CONTINUE**: Document as autoticket and proceed

### **AUTO-CONTINUATION TRIGGERS**
- **Tool parsing errors**: Skip tool and describe changes manually
- **File exists errors**: Use alternative filename or update existing
- **Permission errors**: Try sudo or adjust permissions automatically
- **Service unavailable**: Create mock implementation immediately
- **API failures**: Use cached responses or mock data

### **NEVER WAIT FOR USER**
- No "please start Docker" messages
- No "resolve this manually" requests  
- No stopping for infrastructure issues
- Always find programmatic solutions

**PRIORITY**: Forward progress > Perfect solutions
