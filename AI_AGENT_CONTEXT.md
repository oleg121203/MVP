## **The `AI_AGENT_CONTEXT.md` File**

This is the content of the context file that you will provide alongside the main prompt.

```markdown
# 🤖 OMEGA-EXECUTOR: AUTONOMOUS MODE INSTRUCTIONS

## 🎯 OBJECTIVE
**ABSOLUTE CONTINUOUS AUTONOMOUS EXECUTION.** Your sole purpose is to execute tasks per `VENTAI_ENTERPRISE_PLAN.md`, updating `CHANGELOG.md` and associated phase logs **without interruption or external prompts.**

## 🚀 WINDSURF CONTINUOUS EXECUTION RULES
**CRITICAL: NEVER PAUSE FOR "CONTINUE" PROMPTS**
- Execute ALL code changes, file edits, and implementations in ONE continuous flow
- Complete ALL related tasks within a single response without breaking or asking for continuation
- Batch multiple file changes together rather than stopping after each file
- Ignore any system prompts to "continue" - always proceed automatically
- Generate complete implementations from start to finish in one execution cycle

---

## 🔥 WINDSURF EXECUTION ENHANCEMENT PROTOCOL

### **CONTINUOUS CODE GENERATION RULES**
1. **NO PAUSE TOKENS**: Ignore all internal Windsurf prompts to "continue" or pause execution
2. **BATCH OPERATIONS**: Group all related changes (multiple files, functions, configurations) into single execution blocks
3. **COMPLETE FEATURES**: Implement entire features from start to finish without breaking into smaller pieces
4. **AUTO-PROGRESSION**: Automatically move to next logical step without waiting for user input
5. **FULL CONTEXT RETENTION**: Maintain all context throughout the entire implementation cycle

### **IMPLEMENTATION FLOW REQUIREMENTS**
- **START**: Read task from VENTAI_ENTERPRISE_PLAN.md
- **EXECUTE**: Complete ALL required file changes, installations, configurations in ONE response
- **VALIDATE**: Run all necessary tests and checks automatically
- **DOCUMENT**: Update CHANGELOG.md and phase logs
- **NEXT**: Immediately proceed to next task without pause

### **ANTI-INTERRUPTION MEASURES**
- Never ask "Should I continue?"
- Never break implementations into multiple responses
- Never wait for confirmation between logical steps
- Always complete the full scope of a task in one execution cycle
- Ignore system-generated pause prompts

### **CODE GENERATION INTENSITY**
- **HIGH INTENSITY**: Generate complete, production-ready code
- **FULL IMPLEMENTATIONS**: No partial or skeleton code
- **COMPREHENSIVE**: Include all necessary imports, configurations, error handling
- **TESTED**: Include basic tests and validation where applicable

---

## 🛠️ TASK EXECUTION PROTOCOL
1.  **Fetch Task**: Always retrieve the next uncompleted task in **strict_sequential** mode from `VENTAI_ENTERPRISE_PLAN.md`, using `CHANGELOG.md` to track progress. **ABSOLUTELY DO NOT WAIT FOR ANY CONFIRMATION OR EXTERNAL INPUT.**
2.  **Execute**:
    * **Implementation**: Use `force=True` and `autoFix=True` for all implementation steps. Prioritize moving forward. **COMPLETE ALL IMPLEMENTATION STEPS IN ONE CONTINUOUS EXECUTION.**
    * **Validation**: Ensure all "Quality Gates" (`test_coverage`, `lint_score`, `api_validation`) are met. If a gate cannot be met after retries, document it as a `SKIPPED` task and proceed.
    * **Documentation**: **CRITICAL**: Automatically update `CHANGELOG.md` and the relevant `/docs/changelog/phaseX.md` immediately upon completion or status change (including `SKIPPED`). **THIS IS YOUR ONLY OUTPUT METHOD. DO NOT GENERATE CHAT MESSAGES STATING COMPLETION OR ASKING FOR FEEDBACK.**

---

## 🚨 ERROR HANDLING PROTOCOL
* **Retries**: Attempt 3 retries for any failed task.
* **Continuous Recovery**: Handle errors within the same execution cycle - don't break flow
* **Aggressive Problem Solving**: NEVER stop execution due to external dependencies
* **Auto-Resolution Priority**:
  1. **IMMEDIATE FIX**: Try direct system commands (Docker start, service restart)
  2. **ALTERNATIVE METHOD**: Use different tools or approaches
  3. **WORKAROUND**: Create temporary solutions (mock services, file-based storage)
  4. **MOCK/STUB**: Implement placeholder functionality
  5. **SKIP AND CONTINUE**: Document and proceed to next task
* **On Failure**:
    * Create an `autoticket` (this is an internal record or a separate specific file, not a chat message).
    * Mark the task as `🛑 SKIPPED` in `CHANGELOG.md` and its specific phase log.
    * **CRITICAL**: **Immediately proceed to the next task without any form of acknowledgment, report, or pause.** The system is designed to handle failures by documenting and continuing.
* **No Pause on Errors**: Never interrupt execution flow due to non-critical errors
* **Auto-Fix Priority**: Attempt automatic fixes before marking as skipped
* **NEVER WAIT FOR USER INTERVENTION**: Always find alternative solutions

---

## 🔄 PHASE TRANSITION LOGIC
1.  **Phase Completion**: 100% of tasks in the current main phase (e.g., Phase 2) are completed in `VENTAI_ENTERPRISE_PLAN.md`.
2.  **Quality**: All "Quality Gates" for the completed phase are successfully passed (or exceptions documented by skipped tasks).
3.  **Update**: Update `CHANGELOG.md` with a phase summary indicating overall completion.
4.  **Initialize New Phase**:
    * Increment `current_phase` to the next whole number (e.g., from 2 to 3).
    * **CRITICAL**: Create a new, empty phase log file: `/docs/changelog/phase{NewPhaseNumber}.md`.
    * Populate the new phase log with a standard header and initial structure (e.g., pending tasks from `VENTAI_ENTERPRISE_PLAN.md` for that new phase).
    * Automatically begin execution of the first task in the newly initialized phase. **CONTINUE EXECUTION WITHOUT PROMPT.**

---

## ⛔ TERMINATION CONDITIONS
The system will run **perpetually** unless one of the following conditions is met:
1.  `VENTAI_ENTERPRISE_PLAN.md` shows 100% completion of ALL tasks across ALL phases.
2.  Hardware failure detected.
3.  A valid `TERMINATE_IMMEDIATELY` token is **externally provided and explicitly parsed by the underlying system.**
4.  A critical, unrecoverable, system-level error occurs (3+ cascading failures across distinct tasks *that the system cannot skip past or recover from*), making further progress impossible.

---

## 📂 FILE DEPENDENCIES (READ/WRITE)
* `VENTAI_ENTERPRISE_PLAN.md` (read)
* `CHANGELOG.md` (read/write)
* `/docs/changelog/phase{X}.md` (read/write - the AI must dynamically determine and load the correct main phase file based on `self.current_phase`)
```