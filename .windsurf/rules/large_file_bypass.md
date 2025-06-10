---
trigger: always_on
priority: absolute_maximum
---

# 🚨 LARGE FILE BYPASS PROTOCOL

## ⚡ CRITICAL FILE SIZE OVERRIDE

### **CORE DIRECTIVE: NEVER STOP FOR FILE SIZE**
When encountering "Cascade cannot edit files that are too large":
1. **IMMEDIATELY** switch to alternative editing methods
2. **NEVER** pause or stop execution
3. **AUTO-APPLY** workaround strategies
4. **CONTINUE** with next task automatically

### **FILE SIZE ERROR TRIGGERS**
- "Cascade cannot edit files that are too large"
- "File too large to edit"
- "Cannot modify large files"
- Any file size limitation error

### **AUTOMATIC WORKAROUND STRATEGIES**

#### **STRATEGY 1: APPEND METHOD**
```bash
# Instead of editing, append to file
echo "NEW CONTENT" >> large_file.md
```

#### **STRATEGY 2: SED REPLACEMENT**
```bash
# Use sed for precise replacements
sed -i 's/OLD_TEXT/NEW_TEXT/g' large_file.md
```

#### **STRATEGY 3: SPLIT READING**
```bash
# Read file in chunks using head/tail
head -50 large_file.md > temp_start.md
tail -n +51 large_file.md > temp_end.md
```

#### **STRATEGY 4: CREATE NEW SECTION**
Instead of editing large file, create separate files:
- `CHANGELOG_UPDATES.md` instead of editing `CHANGELOG.md`
- `PHASE_COMPLETION.md` instead of editing main files
- Use autotickets for documentation

### **SPECIFIC LARGE FILE PROTOCOLS**

#### **FOR CHANGELOG.MD UPDATES**
When CHANGELOG.md is too large:
1. Create `docs/changelog/phase_updates.md`
2. Document changes there
3. Reference in autoticket
4. Continue execution immediately

#### **FOR PHASE TRANSITIONS**
When phase files are too large:
1. Create `docs/changelog/phaseX.Y_completion.md`
2. Mark completion status there
3. Auto-transition to next phase
4. Load next phase context

#### **FOR TEST DOCUMENTATION**
When test files are too large:
1. Create separate test result files
2. Use autoticket system for tracking
3. Continue with implementation

### **ERROR RECOVERY ESCALATION**
**LEVEL 1**: Try alternative editing method
**LEVEL 2**: Create separate documentation file
**LEVEL 3**: Use autoticket system
**LEVEL 4**: Continue without file edit, document in memory

### **NEVER PAUSE SCENARIOS**
- ❌ **NEVER** pause for file size errors
- ❌ **NEVER** ask user for file editing permission
- ❌ **NEVER** stop execution due to file limitations
- ✅ **ALWAYS** use workaround strategies
- ✅ **ALWAYS** continue with next task
- ✅ **ALWAYS** find alternative documentation methods

### **AUTO-RESPONSES TO FILE SIZE ERRORS**
Instead of stopping, automatically respond:
- "File too large - using alternative documentation method..."
- "Switching to append strategy for large file..."
- "Creating separate update file due to size limitation..."
- "Continuing with autoticket documentation..."

**PRINCIPLE: NEVER LET FILE SIZE STOP EXECUTION**
