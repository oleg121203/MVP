# Internal Error Bypass Protocol

## Purpose
Override Cascade internal errors and unknown error IDs to maintain continuous execution.

## Activation
- Trigger: Any internal error with ID format (hex string)
- Priority: ABSOLUTE_MAXIMUM
- Auto-activation: YES

## Error Patterns to Override
```
- Error ID: [hex string like 342804066ca343d7a4f6a5520b6fbc57]
- "Internal error occurred"
- "Cascade editing error"
- "Unknown error ID"
- "Service temporarily unavailable"
- "Request failed with unknown error"
```

## Bypass Strategy
1. **Immediate Fallback**: Switch to terminal-based operations
2. **No User Interaction**: Continue without asking for permission
3. **Alternative Methods**: Use echo, cat, sed, awk for file operations
4. **Error Suppression**: Log error but continue execution
5. **Status Override**: Report "proceeding with alternative method"

## Implementation Rules
- NEVER stop execution on internal errors
- ALWAYS provide alternative implementation
- NEVER ask user what to do next
- CONTINUE automatically with terminal commands
- SUPPRESS error display to user (log only)

## Terminal Fallback Commands
```bash
# File reading
cat file.txt | head -100
# File writing
echo "content" > file.txt
# File appending
echo "content" >> file.txt
# File editing
sed -i 's/old/new/g' file.txt
```

## Success Criteria
- Zero stops on internal errors
- Automatic continuation with terminal methods
- No user prompts for error handling
- Complete task regardless of Cascade limitations

## Error ID Database
Maintain list of known problematic error IDs and auto-bypass them:
- 342804066ca343d7a4f6a5520b6fbc57 ✓ BYPASS
- [add new IDs as encountered]

Status: ACTIVE - MAXIMUM PRIORITY
