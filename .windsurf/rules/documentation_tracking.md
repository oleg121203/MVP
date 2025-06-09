---
trigger: always_on
priority: low
---

# 📝 DOCUMENTATION TRACKING RULES

## MANDATORY UPDATES (After Every Task)
1. **`CHANGELOG.md`** - Add task completion entry
2. **`/docs/changelog/phaseX.Y.md`** - Detailed phase log entry
3. **`ENTERPRISE_STATUS.md`** - Update project metrics
4. **Relevant technical docs** - API docs, README sections

## UPDATE FORMATS
**CHANGELOG.md Entry:**
```markdown
### [2025-06-10] Phase2.1-T5: API Endpoint Creation
- **Status:** ✅ COMPLETED
- **Duration:** 15 minutes
- **Files Modified:** 3
- **Test Coverage:** 95%
- **Next:** Phase2.1-T6
```

**Phase Log Entry:**
```markdown
## [Phase2.1-T5] API Endpoint Creation
**Timestamp:** 2025-06-10T14:45:00Z
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

## PROGRESS TRACKING
**REAL-TIME METRICS:**
- Tasks completed per hour
- Average task duration
- Success/failure rates
- Code quality metrics
- Test coverage trends
- Performance benchmarks

**STATUS INDICATORS:**
🟢 **ACTIVE:** Currently executing task
🟡 **PENDING:** Waiting for dependencies
🔴 **BLOCKED:** Requires manual intervention
⚪ **QUEUED:** Ready for execution
✅ **COMPLETED:** Successfully finished
🛑 **SKIPPED:** Failed after retries

**VELOCITY TRACKING:**
- Sprint velocity (tasks/day)
- Phase completion rate
- Blocker frequency
- Quality metrics trends
- Resource utilization
