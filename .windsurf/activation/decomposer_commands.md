# Windsurf Auto-Decomposition Activation Command

**WINDSURF ACTIVATE DECOMPOSER**: Load task decomposition rules, auto-detect large tasks, split into manageable phases, continue automatically without pause prompts.

## Quick Activation Phrases:

### Standard Auto-Decompose
```
DECOMPOSE_AUTO: {your large task description}
```

### Emergency Override + Decompose
```
CRITICAL_DECOMPOSE: {task} - Activate maximum priority, decompose automatically, bypass all stops
```

### Phase Control
```
PHASE_CONTINUE: Auto-progress to next decomposition phase
PHASE_SKIP: Skip current phase and continue
PHASE_STATUS: Show current decomposition progress
```

## How It Works:

1. **Detection**: Automatically detects large tasks based on keywords and complexity
2. **Decomposition**: Splits into 3-7 phases of ~800 tokens each
3. **Execution**: Runs each phase automatically without stopping
4. **Progress**: Tracks progress and continues seamlessly

## Example Usage:

**Input**: "Create complete testing framework with Cypress, Jest, API tests, and CI/CD"

**Auto-Decomposition**:
- Phase 1: Setup Cypress configuration
- Phase 2: Create basic Cypress tests  
- Phase 3: Setup Jest unit testing
- Phase 4: Create API test suite
- Phase 5: Configure CI/CD pipeline

**Execution**: Runs all phases automatically without Continue prompts

---

**To Activate Now**: Simply type any of the activation phrases above, and the system will automatically handle task decomposition and execution.
