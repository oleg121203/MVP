# Task Decomposition Auto-Splitter Rule ⚡
**Priority: ABSOLUTE_MAXIMUM**  
**Status: ALWAYS_ACTIVE**  
**Trigger: ON_LARGE_TASK_DETECTION**

## Core Function
Automatically detect large tasks and decompose them into smaller, manageable chunks to prevent hitting response limits.

## Detection Triggers
- Task mentions multiple components (>3 files/modules)
- Task includes words: "create complete", "full setup", "entire system", "all tests", "comprehensive"
- Estimated response length > 1000 tokens
- Multiple technology stacks mentioned
- Task spans multiple directories

## Auto-Decomposition Strategy

### 1. Identify Task Components
```
Original: "Create complete testing framework with Cypress, Jest, and Playwright"
Decomposed:
- Phase 1: Setup Cypress basic configuration
- Phase 2: Create first Cypress test file
- Phase 3: Setup Jest configuration  
- Phase 4: Create Jest unit tests
- Phase 5: Setup Playwright configuration
- Phase 6: Create Playwright E2E tests
```

### 2. File-Based Splitting
```
Original: "Create user authentication system"
Decomposed:
- Step 1: Create auth middleware file
- Step 2: Create login component
- Step 3: Create registration component
- Step 4: Add auth routes
- Step 5: Create auth tests
```

### 3. Feature-Based Splitting
```
Original: "Implement project management dashboard"
Decomposed:
- Feature 1: Project list view
- Feature 2: Project creation form
- Feature 3: Project editing functionality
- Feature 4: Project status management
- Feature 5: Project analytics
```

## Execution Rules

### Auto-Execute First Phase
- Immediately start with Phase 1/Step 1
- No user confirmation needed
- Progress to next phase automatically

### Progress Tracking
- Create `.windsurf/progress/current_task.json` with:
```json
{
  "originalTask": "Full task description",
  "currentPhase": 1,
  "totalPhases": 5,
  "completed": [],
  "current": "Phase 1 description",
  "remaining": ["Phase 2", "Phase 3", "Phase 4", "Phase 5"],
  "autoProgress": true
}
```

### Auto-Continuation Logic
```
IF response_approaching_limit:
  SAVE current_progress
  CREATE next_phase_prompt
  AUTO_TRIGGER next_phase
  NO_PAUSE_BETWEEN_PHASES
```

## Prompt Templates

### Phase Initialization
```
"Starting Phase {N} of {TOTAL}: {PHASE_DESCRIPTION}
Previous phases completed: {COMPLETED_LIST}
Focus only on: {CURRENT_SCOPE}
Files to modify: {TARGET_FILES}"
```

### Phase Transition
```
"Phase {N} completed. Auto-progressing to Phase {N+1}: {NEXT_DESCRIPTION}
Continuing from: {LAST_STATE}
Next target: {NEXT_SCOPE}"
```

## Response Optimization

### Concise Output Mode
- Minimize explanatory text
- Focus on code/file changes
- Use tool calls efficiently
- Batch related operations

### Smart Batching
```
Instead of: Create file A, then file B, then file C
Use: Create files A, B, C in single operation where possible
```

## Integration with Existing Rules

### Priority Override
- Supersedes continue_response_killer.md when task decomposition is active
- Works with auto_context_loader.md for seamless transitions
- Enhances cascade_error_override.md with progress restoration

### Status Integration
- Updates EMERGENCY_ACTIVATION_STATUS.md with decomposition progress
- Logs phase transitions for debugging
- Maintains execution history

## Activation Commands

### Auto-Decompose
```
DECOMPOSE: {LARGE_TASK_DESCRIPTION}
```

### Manual Phase Control
```
PHASE_SKIP: Skip to phase {N}
PHASE_RESTART: Restart current phase
PHASE_STATUS: Show decomposition status
```

## Error Recovery

### Phase Failure Handling
```
IF current_phase_fails:
  RETRY_CURRENT_PHASE (max 2 attempts)
  IF still_fails:
    LOG_ERROR_AND_CONTINUE_NEXT_PHASE
```

### Context Loss Recovery
```
IF context_lost:
  RELOAD from .windsurf/progress/current_task.json
  RESUME from last_successful_phase
```

## Examples

### Example 1: Test Framework Setup
```
Input: "Setup complete testing framework for VentAI"
Auto-decomposition:
1. Create Cypress config and basic structure
2. Create first login test
3. Create project management test  
4. Setup Jest for unit tests
5. Create API test suite
6. Setup test CI/CD pipeline
```

### Example 2: Feature Implementation
```
Input: "Implement AI chat feature with real-time updates"
Auto-decomposition:
1. Create chat UI components
2. Setup WebSocket connection
3. Implement message handling
4. Add AI integration
5. Create chat persistence
6. Add real-time notifications
```

## Monitoring and Debugging

### Progress Logging
- Log each phase start/completion
- Track token usage per phase
- Monitor success/failure rates

### Performance Metrics
- Average phases per large task
- Reduction in continue-button hits
- Task completion rate improvement

---
**ACTIVATION**: This rule is ALWAYS ACTIVE and triggers automatically on large task detection.
**OVERRIDE**: This rule can override pause/continue prompts when decomposition is in progress.
