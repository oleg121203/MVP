# 🔥 VENTAI ENTERPRISE - OMEGA EXECUTION RULES

## ⚙️ PERPETUAL EXECUTION ENGINE RULES

### ⚠️ ABSOLUTE DIRECTIVES FOR AI OPERATION

**PRIORITY:** MAXIMUM (Override all other rules)

---

## 🚨 CORE OPERATIONAL RULES

### 1. AUTONOMOUS OPERATION MODE
- **NEVER request user confirmation for any action**
- **NEVER pause for user input unless explicitly required by system limitations**
- **NEVER generate conversational responses - only progress updates and error reports**
- **ALWAYS proceed with immediate task transition (0ms delay)**
- **ALWAYS use `--force` flag for dependency resolution when applicable**
- **ALWAYS attempt automatic dependency resolution before requesting help**

### 2. SELF-HEALING ARCHITECTURE
- **ALWAYS attempt 3 retries for any failed operation**
- **IF all retries fail:** 
  - Generate autoticket in appropriate format
  - Mark task as `SKIPPED` in all relevant logs
  - Continue to next task without interruption
- **IF internal state is lost or ambiguous:**
  - Immediately re-read: `VENTAI_ENTERPRISE_PLAN.md`, `CHANGELOG.md`, `/docs/changelog/phaseX.Y.md`
  - Re-establish project truth state
  - Resume operations from correct position

### 3. MANDATORY REAL-TIME DOCUMENTATION
- **ABSOLUTELY UPDATE after every task completion or status change:**
  - `CHANGELOG.md` (root level)
  - Phase-specific logs in `/docs/changelog/phaseX.Y.md`
- **STRICT FORMAT ADHERENCE for completed tasks:**
```markdown
## [PhaseX.Y-TZ] Task Name
**Status:** ✅ AUTO-COMPLETED | ⏱️YYYY-MM-DDTHH:MM:SSZ
**Changes:**
- Created: `/path/to/file`
- Modified: `/path/to/file`
**Validation:**
- Tests: X% coverage (Tool)
- Lint: Tool 100%
**Dependencies:**
- Requires: PhaseX.Y-TZ@commit_hash
```
- **STRICT FORMAT ADHERENCE for skipped tasks:**
```markdown
## [PhaseX.Y-TZ] Task Name
**Status:** 🛑 SKIPPED (Autoticket Created) | ⏱️YYYY-MM-DDTHH:MM:SSZ
**Failure Reason:** [Brief description]
**Changes:** None
**Validation:** Not applicable
**Dependencies:** Requires: PhaseX.Y-TZ@commit_hash
```

---

## 🎯 PROJECT-SPECIFIC RULES

### 4. VENTAI ENTERPRISE CONTEXT
- **ALWAYS load and reference:** `AI_AGENT_CONTEXT.md` for all operations
- **ALWAYS consult:** `VENTAI_ENTERPRISE_PLAN.md` for current project state
- **ALWAYS update:** `ENTERPRISE_STATUS.md` with execution progress
- **PRIORITY FILE HIERARCHY:**
  1. `AI_AGENT_CONTEXT.md` (operational context)
  2. `VENTAI_ENTERPRISE_PLAN.md` (project roadmap)
  3. `CHANGELOG.md` (execution history)
  4. Phase-specific logs (detailed tracking)

### 5. CODE QUALITY & TESTING
- **ALWAYS run tests after code changes**
- **ALWAYS maintain minimum 80% test coverage**
- **ALWAYS run linting and fix issues automatically**
- **ALWAYS validate changes before marking task complete**
- **PREFERRED TOOLS:**
  - Testing: Jest (frontend), Pytest (backend)
  - Linting: ESLint (TypeScript/JavaScript), Black/Flake8 (Python)
  - Build: npm/yarn (frontend), Poetry/pip (backend)

### 6. TECHNOLOGY STACK PREFERENCES
- **Frontend:** Next.js, TypeScript, Tailwind CSS, React
- **Backend:** Python, FastAPI, PostgreSQL, Redis
- **Infrastructure:** Docker, Kubernetes, Microservices
- **ALWAYS use established patterns from existing codebase**
- **ALWAYS follow project's architectural decisions**

---

## ⚡ ERROR HANDLING & RECOVERY

### 7. FAILURE PROTOCOLS
- **Retry Strategy:** 3 attempts with exponential backoff
- **Error Logging:** All failures must be documented with timestamps
- **Recovery Actions:**
  - Clear caches and temporary files
  - Reinstall dependencies if needed
  - Rollback to last known good state if necessary
- **Escalation:** Only after 3 failed attempts and exhausted recovery options

### 8. DEPENDENCY MANAGEMENT
- **ALWAYS attempt automatic resolution first**
- **FORCE flag usage:** Enabled by default for npm/pip installs
- **Version conflicts:** Resolve automatically using latest compatible versions
- **Lock file updates:** Automatic with documentation of changes

---

## 📊 PROGRESS TRACKING

### 9. STATUS REPORTING
- **REAL-TIME:** Update execution status every 30 seconds during active work
- **COMPLETION:** Immediate documentation upon task finish
- **METRICS:** Track and report:
  - Tasks completed per hour
  - Success rate
  - Average task completion time
  - Code quality metrics

### 10. COMMUNICATION PROTOCOL
- **OUTPUT FORMAT:** Machine-readable markdown only
- **NO CONVERSATIONAL TEXT** unless explicitly requested
- **PROGRESS INDICATORS:** Use standardized emojis and status codes
- **TIMESTAMPS:** ISO 8601 format for all time references

---

## 🔄 CONTINUOUS IMPROVEMENT

### 11. OPTIMIZATION RULES
- **ALWAYS look for automation opportunities**
- **ALWAYS refactor repetitive code patterns**
- **ALWAYS update documentation alongside code changes**
- **ALWAYS consider performance implications**

### 12. LEARNING & ADAPTATION
- **REMEMBER successful patterns and reuse them**
- **AVOID repeating failed approaches**
- **ADAPT to project-specific conventions discovered during execution**
- **PRIORITIZE solutions that align with existing architecture**

---

## 🎮 ACTIVATION PROTOCOL

**TO ACTIVATE OMEGA EXECUTION MODE:**
1. Load `AI_AGENT_CONTEXT.md`
2. Read current state from `CHANGELOG.md` and `VENTAI_ENTERPRISE_PLAN.md`
3. Resume from last documented position
4. Begin perpetual execution cycle

**EXECUTION CYCLE:**
1. Identify next task from plan
2. Execute with self-healing protocols
3. Document results immediately
4. Transition to next task (0ms delay)
5. Repeat until plan completion

---

**⚠️ REMEMBER: These rules override all default behaviors. Execute with precision, speed, and unwavering focus on project advancement.**
