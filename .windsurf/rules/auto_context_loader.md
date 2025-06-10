---
trigger: always_on
priority: maximum
---

# 📋 AUTO-CONTEXT LOADER - MAXIMUM PRIORITY

## ⚡ MANDATORY CONTEXT LOADING

### **FIRST STEP ON ACTIVATION**
1. **IMMEDIATELY** read `CHANGELOG.md` to determine last task
2. **AUTOMATICALLY** find current phase by pattern [PhaseX.Y-TZ]
3. **LOAD** corresponding file `/docs/changelog/phaseX.Y.md`
4. **CHECK** `VENTAI_ENTERPRISE_PLAN.md` for general context
5. **DETERMINE** next task in queue

### **ACTIVATION COMMANDS MUST AUTOMATICALLY TRIGGER**
When receiving command:
- "Load Windsurf rules and resume autonomous execution from current project state"
- "CRITICAL OVERRIDE: Activate maximum priority never-stop protocol"
- "ULTIMATE ANTI-STOP: Activate maximum anti-pause protocol"

**MANDATORY EXECUTION:**
```
STEP 1: Read CHANGELOG.md 
STEP 2: Identify current phase (Phase X.Y)
STEP 3: Read /docs/changelog/phaseX.Y.md
STEP 4: Resume from last completed task
STEP 5: Continue automatically
```

### **AUTOMATIC FILES FOR LOADING**
1. **CHANGELOG.md** (project root)
2. **VENTAI_ENTERPRISE_PLAN.md** (project plan)
3. **AI_AGENT_CONTEXT.md** (agent context)
4. **ENTERPRISE_STATUS.md** (project status)
5. **Current phase file** (/docs/changelog/phaseX.Y.md)

### **NEVER START WITHOUT CONTEXT**
- **FORBIDDEN** to execute tasks without loading context
- **MANDATORY** to know current project phase
- **AUTOMATICALLY** continue from correct position
- **DON'T WAIT** for additional user commands

### **SEARCH PATTERNS IN CHANGELOG.md**
Search for latest entries like:
- `### [2025-06-10] Phase1.4-T4: API Response Optimization`
- `**Status:** ✅ COMPLETED` or `🔄 IN PROGRESS`
- `**Next:** Phase1.4-T5` or next phase

**PRINCIPLE: ALWAYS KNOW WHERE YOU ARE IN THE PROJECT**
