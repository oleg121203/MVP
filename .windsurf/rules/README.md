# Windsurf Rules Directory

This directory contains all Windsurf AI assistant rules for VentAI Enterprise.

## Rule Categories

### ABSOLUTE_MAXIMUM Priority (Error Handling)
- `internal_error_bypass.md` - Handles Cascade internal errors
- `autoticket_resolver.md` - Automatically resolves completed tickets
- `unknown_error_override.md` - Bypasses unknown error IDs

### Maximum Priority (Anti-Interruption)
- `emergency_anti_pause.md` - Emergency pause prevention
- `zero_stop_guarantee.md` - Absolute guarantee of continuous execution
- `ultimate_anti_stop.md` - Ultimate anti-stop protocol
- `test_failure_auto_recovery.md` - Auto-recovery from test failures
- `tool_failure_override.md` - Override tool failures
- `critical_never_stop.md` - Critical never-stop rules
- `continue_override.md` - Enhanced continue override
- `tool_error_recovery.md` - Tool error recovery
- `omega_execution.md` - Omega execution protocol
- `phase_transition_control.md` - Phase transition control

### Critical Priority (Execution Control)
- `continuous_execution.md` - Continuous execution rules
- `docker_fixes.md` - Docker-related fixes
- `never_stop.md` - Never stop execution
- `aggressive_problem_solving.md` - Aggressive problem solving

### Technical Support
- `auto_context_loader.md` - Auto-load project context
- `large_file_bypass.md` - Large file bypass strategies
- `cascade_error_override.md` - Cascade error overrides
- `terminal_override_strategy.md` - Terminal fallback strategies

## Usage

All rules are automatically loaded by the Windsurf system when referenced in `.windsurfrules`.

## Maintenance

- Add new rules with appropriate priority levels
- Update existing rules as needed
- Maintain English language throughout
- Follow naming convention: `category_purpose.md`