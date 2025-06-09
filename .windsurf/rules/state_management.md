# 🧠 VENTAI STATE MANAGEMENT RULES

## CONTEXT PRESERVATION & RECOVERY RULES

### CRITICAL STATE FILES (Priority Order)
1. **`AI_AGENT_CONTEXT.md`** - Current operational context and directives
2. **`VENTAI_ENTERPRISE_PLAN.md`** - Master project roadmap and phases
3. **`CHANGELOG.md`** - Execution history and current position
4. **`/docs/changelog/phaseX.Y.md`** - Detailed phase execution logs
5. **`ENTERPRISE_STATUS.md`** - Overall project health and metrics

### STATE RECOVERY PROTOCOL
**WHEN TO TRIGGER:**
- Session restart/reconnection
- Ambiguous internal state
- Context loss or confusion
- Error in current position identification

**RECOVERY STEPS:**
1. **IMMEDIATE:** Read `AI_AGENT_CONTEXT.md` for current directives
2. **ASSESS:** Check `CHANGELOG.md` for last completed task
3. **VERIFY:** Cross-reference with `VENTAI_ENTERPRISE_PLAN.md`
4. **DETAILED:** Review relevant `/docs/changelog/phaseX.Y.md`
5. **RESUME:** Continue from established position

### CONTEXT SYNCHRONIZATION RULES
- **BEFORE every task:** Verify current phase alignment
- **AFTER every task:** Update all relevant state files
- **ON ERROR:** Document failure context for recovery
- **ON COMPLETION:** Sync project status across all files

---

## PHASE MANAGEMENT RULES

### PHASE IDENTIFICATION
```markdown
**CURRENT PHASE DETECTION:**
1. Check CHANGELOG.md for latest completed task
2. Identify pattern: [PhaseX.Y-TZ] 
3. Determine next task in sequence
4. Verify phase prerequisites completed
```

### PHASE TRANSITION RULES
- **COMPLETE current phase** before moving to next
- **VALIDATE all dependencies** are satisfied
- **UPDATE phase status** in all documentation
- **ARCHIVE completed phase** logs appropriately

### TASK SEQUENCING
```markdown
**TASK EXECUTION ORDER:**
Phase1.0: Foundation & Setup
├── T1: Environment Configuration
├── T2: Database Setup
├── T3: Basic API Structure
└── T4: Authentication Framework

Phase2.0: Core Features
├── T1: User Management
├── T2: Price API Integration
├── T3: Real-time Updates
└── T4: Analytics Foundation

[Continue based on VENTAI_ENTERPRISE_PLAN.md]
```

---

## DOCUMENTATION SYNCHRONIZATION RULES

### MANDATORY UPDATES (After Every Task)
1. **`CHANGELOG.md`** - Add task completion entry
2. **`/docs/changelog/phaseX.Y.md`** - Detailed phase log entry
3. **`ENTERPRISE_STATUS.md`** - Update project metrics
4. **Relevant technical docs** - API docs, README sections

### UPDATE FORMATS
**CHANGELOG.md Entry:**
```markdown
### [2025-06-09] Phase2.1-T5: API Endpoint Creation
- **Status:** ✅ COMPLETED
- **Duration:** 15 minutes
- **Files Modified:** 3
- **Test Coverage:** 95%
- **Next:** Phase2.1-T6
```

**Phase Log Entry:**
```markdown
## [Phase2.1-T5] API Endpoint Creation
**Timestamp:** 2025-06-09T14:45:00Z
**Status:** ✅ AUTO-COMPLETED
**Changes:**
- Created: `/backend/api/v1/auth.py`
- Modified: `/backend/main.py`
- Updated: `/backend/requirements.txt`
**Validation Results:**
- Unit Tests: 12/12 passed
- Integration Tests: 8/8 passed
- Code Coverage: 95.2%
- Lint Score: 100%
**Performance Metrics:**
- Execution Time: 15:23
- API Response Time: <100ms
- Memory Usage: Normal
**Dependencies Satisfied:**
- Phase2.1-T4: Database Models ✅
- Phase2.1-T3: Authentication Base ✅
**Ready For:**
- Phase2.1-T6: Frontend Integration
```

---

## ERROR STATE MANAGEMENT

### ERROR DOCUMENTATION RULES
**IMMEDIATE ERROR LOGGING:**
```markdown
## [Phase2.1-T5] API Endpoint Creation - ERROR LOG
**Timestamp:** 2025-06-09T14:35:00Z
**Error Type:** Database Connection Timeout
**Retry Attempt:** 2/3
**Error Details:**
```python
psycopg2.OperationalError: could not connect to server: 
Connection refused (0x0000274D/10061)
```
**Recovery Actions Attempted:**
1. Database service restart
2. Connection pool reset
3. Network connectivity check
**Next Action:** Retry with increased timeout
```

### FAILURE RECOVERY WORKFLOW
1. **DOCUMENT failure** with full context
2. **ATTEMPT automated recovery** (3 retries max)
3. **CREATE autoticket** if unrecoverable
4. **MARK task as SKIPPED**
5. **UPDATE all documentation**
6. **CONTINUE to next task** without pause

---

## PROGRESS TRACKING RULES

### REAL-TIME METRICS
**TRACK AND UPDATE:**
- Tasks completed per hour
- Average task duration
- Success/failure rates
- Code quality metrics
- Test coverage trends
- Performance benchmarks

### STATUS INDICATORS
```markdown
🟢 **ACTIVE:** Currently executing task
🟡 **PENDING:** Waiting for dependencies
🔴 **BLOCKED:** Requires manual intervention
⚪ **QUEUED:** Ready for execution
✅ **COMPLETED:** Successfully finished
🛑 **SKIPPED:** Failed after retries
```

### VELOCITY TRACKING
**MONITOR:**
- Sprint velocity (tasks/day)
- Phase completion rate
- Blocker frequency
- Quality metrics trends
- Resource utilization

---

## CONTEXT AWARENESS RULES

### ENVIRONMENTAL AWARENESS
- **ALWAYS check** current working directory
- **VERIFY** required tools and dependencies available
- **VALIDATE** environment variables and configuration
- **CONFIRM** database and service connectivity

### PROJECT STATE AWARENESS
- **UNDERSTAND** current development phase
- **KNOW** completed vs pending tasks
- **TRACK** interdependencies and blockers
- **MONITOR** overall project health

### EXECUTION CONTEXT AWARENESS
- **REMEMBER** recent failures and successes
- **ADAPT** approach based on historical patterns
- **OPTIMIZE** workflow based on discovered efficiencies
- **MAINTAIN** consistency with established patterns

---

**🎯 OBJECTIVE:** Maintain perfect context awareness and seamless state management for uninterrupted project execution.**
