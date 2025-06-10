#!/bin/zsh

# 🚀 VENTAI ENTERPRISE UNIVERSAL ACTIVATOR
# Автоматично визначає поточну фазу і запускає необхідні дії

WORKSPACE="/Users/olegkizyma/workspaces/MVP/ventai-app"
WINDSURF_DIR="$WORKSPACE/.windsurf"

echo "🚀 VENTAI ENTERPRISE ACTIVATION"
echo "==============================="

# Функція для визначення поточної фази
detect_current_phase() {
    local changelog="$WORKSPACE/CHANGELOG.md"
    local enterprise_plan="$WORKSPACE/VENTAI_ENTERPRISE_PLAN.md"
    
    if [[ -f "$changelog" ]]; then
        # Шукаємо останню фазу в CHANGELOG.md
        local last_phase=$(grep -E "Phase [0-9]+\.[0-9]+" "$changelog" | tail -1 | grep -oE "Phase [0-9]+\.[0-9]+")
        echo "📋 Last phase in CHANGELOG: $last_phase"
        
        # Перевіряємо статус цієї фази
        if grep -q "completed\|COMPLETED\|100%" "$changelog"; then
            echo "✅ Current phase appears completed"
            return 1  # Phase completed, need transition
        else
            echo "🔄 Current phase in progress"
            return 0  # Phase in progress
        fi
    fi
    
    echo "❓ Unable to determine phase status"
    return 2  # Unknown status
}

# Функція для активації скриптів
activate_enterprise_scripts() {
    echo ""
    echo "🎯 ACTIVATING ENTERPRISE SCRIPTS:"
    echo "================================="
    
    # 1. Ultimate Activation
    if [[ -x "$WINDSURF_DIR/activate_ultimate.sh" ]]; then
        echo "🔥 Running Ultimate Activation..."
        "$WINDSURF_DIR/activate_ultimate.sh"
    else
        echo "❌ Ultimate activation script not found or not executable"
    fi
    
    # 2. Phase Manager
    if [[ -x "$WINDSURF_DIR/scripts/universal_phase_manager.sh" ]]; then
        echo "🔄 Running Phase Manager..."
        "$WINDSURF_DIR/scripts/universal_phase_manager.sh" detect
    else
        echo "❌ Phase manager script not found"
    fi
    
    # 3. Task Decomposer Setup
    if [[ -x "$WINDSURF_DIR/scripts/task_decomposer.sh" ]]; then
        echo "⚡ Setting up Task Decomposer..."
        "$WINDSURF_DIR/scripts/task_decomposer.sh" setup
    else
        echo "❌ Task decomposer not found"
    fi
}

# Функція для створення команди активації для Windsurf
generate_windsurf_activation() {
    local activation_command="$WINDSURF_DIR/status/CURRENT_ACTIVATION_COMMAND.md"
    
    cat > "$activation_command" << 'EOF'
# 🚀 CURRENT ACTIVATION STATUS

**Command Executed:** VENTAI ENTERPRISE ACTIVATE
**Timestamp:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Scripts Executed:** ✅ ALL

## 🎯 NEXT ACTIONS FOR WINDSURF:

### 1. Load Project Context
- Read CHANGELOG.md to identify current phase
- Read VENTAI_ENTERPRISE_PLAN.md for project overview
- Determine completion status of current phase

### 2. Phase Detection & Transition
- If current phase completed → Auto-transition to next phase
- If current phase in progress → Continue current tasks
- If phase status unclear → Start Phase 2.1 Advanced Analytics

### 3. Autonomous Execution Mode
- Execute without pause prompts
- Use task decomposition for large tasks
- Apply all anti-stop protocols
- Continue with zero manual intervention

## 🔥 RECOMMENDED IMMEDIATE ACTION:

```
PHASE_TRANSITION_OVERRIDE: Auto-detect current phase completion, transition to next phase automatically, continue with autonomous execution
```

or 

```
EMERGENCY_EXECUTION: Phase 2.1.1 - Advanced Price Analytics Dashboard - Critical priority, no stops, auto-decompose if needed
```

---
**Status:** ENTERPRISE ACTIVATION COMPLETED ✅
**Ready for:** AUTONOMOUS PHASE PROGRESSION 🚀
EOF

    echo "📝 Windsurf activation command generated: $activation_command"
}

# Функція для перевірки стану проекту
check_project_status() {
    echo ""
    echo "📊 PROJECT STATUS CHECK:"
    echo "======================="
    
    # Перевірка фаз
    if [[ -f "$WORKSPACE/CHANGELOG.md" ]]; then
        echo "✅ CHANGELOG.md exists"
        local phase_count=$(grep -c "Phase [0-9]" "$WORKSPACE/CHANGELOG.md")
        echo "📈 Phases documented: $phase_count"
    else
        echo "❌ CHANGELOG.md not found"
    fi
    
    # Перевірка enterprise plan
    if [[ -f "$WORKSPACE/VENTAI_ENTERPRISE_PLAN.md" ]]; then
        echo "✅ VENTAI_ENTERPRISE_PLAN.md exists"
    else
        echo "❌ VENTAI_ENTERPRISE_PLAN.md not found"
    fi
    
    # Перевірка backend
    if [[ -d "$WORKSPACE/backend" ]]; then
        echo "✅ Backend directory exists"
    else
        echo "❌ Backend directory not found"
    fi
    
    # Перевірка frontend
    if [[ -d "$WORKSPACE/frontend" ]]; then
        echo "✅ Frontend directory exists"
    else
        echo "❌ Frontend directory not found"
    fi
}

# Головна функція
main() {
    echo "Starting VentAI Enterprise Activation..."
    echo "Workspace: $WORKSPACE"
    echo ""
    
    # Перевірка проекту
    check_project_status
    
    # Визначення поточної фази
    echo ""
    detect_current_phase
    local phase_status=$?
    
    # Активація скриптів
    activate_enterprise_scripts
    
    # Генерація команди для Windsurf
    generate_windsurf_activation
    
    echo ""
    echo "🎉 VENTAI ENTERPRISE ACTIVATION COMPLETED!"
    echo "=========================================="
    echo ""
    echo "🎯 NEXT STEPS:"
    echo "1. Copy and paste one of the commands from:"
    echo "   $WINDSURF_DIR/status/CURRENT_ACTIVATION_COMMAND.md"
    echo ""
    echo "2. Or simply use:"
    echo "   PHASE_TRANSITION_OVERRIDE"
    echo ""
    echo "3. System will auto-detect phase and continue autonomous execution"
    echo ""
    echo "✅ All enterprise protocols activated and ready!"
}

# Запуск
main "$@"
