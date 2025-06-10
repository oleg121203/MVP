#!/bin/zsh

# UNIVERSAL PHASE MANAGER ⚡
# Автоматичний менеджер фаз проекту з безперервним виконанням

WINDSURF_ROOT="/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf"
PROJECT_ROOT="/Users/olegkizyma/workspaces/MVP/ventai-app"
STATE_FILE="$WINDSURF_ROOT/status/current_phase.json"
LOG_FILE="$WINDSURF_ROOT/logs/phase_manager.log"

# Створити необхідні директорії
mkdir -p "$WINDSURF_ROOT/status" "$WINDSURF_ROOT/logs" "$WINDSURF_ROOT/emergency"

# Функція логування
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Функція визначення поточної фази з документів
detect_current_phase() {
    local changelog="$PROJECT_ROOT/CHANGELOG.md"
    local enterprise_plan="$PROJECT_ROOT/VENTAI_ENTERPRISE_PLAN.md"
    
    # Пошук завершених фаз в CHANGELOG
    if [[ -f "$changelog" ]]; then
        local completed_phases=$(grep -E "Phase [0-9]+\.[0-9]+" "$changelog" | grep -E "(COMPLETED|100%|✅)" | tail -1)
        if [[ -n "$completed_phases" ]]; then
            local last_completed=$(echo "$completed_phases" | grep -oE "Phase [0-9]+\.[0-9]+" | tail -1)
            echo "$last_completed"
            return 0
        fi
    fi
    
    # Якщо нічого не знайдено, повернути Phase 1.0
    echo "Phase 1.0"
}

# Функція визначення наступної фази
get_next_phase() {
    local current_phase="$1"
    
    case "$current_phase" in
        "Phase 1.0") echo "Phase 1.1" ;;
        "Phase 1.1") echo "Phase 1.2" ;;
        "Phase 1.2") echo "Phase 1.3" ;;
        "Phase 1.3") echo "Phase 1.4" ;;
        "Phase 1.4") echo "Phase 1.5" ;;
        "Phase 1.5") echo "Phase 2.0" ;;
        "Phase 2.0") echo "Phase 2.1" ;;
        "Phase 2.1") echo "Phase 2.2" ;;
        "Phase 2.2") echo "Phase 3.0" ;;
        "Phase 3.0") echo "Phase 3.1" ;;
        "Phase 3.1") echo "Phase 4.0" ;;
        "Phase 4.0") echo "Phase 4.1" ;;
        "Phase 4.1") echo "Phase 5.0" ;;
        *) echo "Phase 1.0" ;;
    esac
}

# Функція збереження стану фази
save_phase_state() {
    local phase="$1"
    local status="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    cat > "$STATE_FILE" << EOF
{
  "currentPhase": "$phase",
  "status": "$status",
  "timestamp": "$timestamp",
  "autoTransition": true,
  "lastAction": "phase_manager_update",
  "nextPhase": "$(get_next_phase "$phase")"
}
EOF
    log "Phase state saved: $phase ($status)"
}

# Функція створення активаційної команди для фази
create_phase_activation_command() {
    local phase="$1"
    local next_phase="$2"
    
    # Мапінг фаз до завдань
    case "$phase" in
        "Phase 1.1")
            echo "DECOMPOSE_AUTO: Implement Phase 1.1 Database Schema for Analytics - Create project tables, analytics schema, price analytics tables, metrics and KPI system"
            ;;
        "Phase 1.2") 
            echo "DECOMPOSE_AUTO: Implement Phase 1.2 AI Analytics Service - Extend aiService.js, create ProjectAnalyticsEngine, real-time cost analysis, AI optimization recommendations"
            ;;
        "Phase 1.3")
            echo "DECOMPOSE_AUTO: Implement Phase 1.3 Analytics Dashboard - Create ProjectAnalyticsDashboard component, real-time charts, AI Chat integration, analytics report export"
            ;;
        "Phase 1.4")
            echo "DECOMPOSE_AUTO: Implement Phase 1.4 Performance Optimizations - Request caching, virtualized lists, memory optimization, improved test coverage"
            ;;
        "Phase 1.5")
            echo "DECOMPOSE_AUTO: Implement Phase 1.5 UAT and Automation - UAT test plan, test automation, production build configuration, deployment automation"
            ;;
        "Phase 2.0")
            echo "DECOMPOSE_AUTO: Implement Phase 2.0 Price Intelligence System - Price analysis engine, supplier management, cost optimization dashboard"
            ;;
        "Phase 2.1")
            echo "DECOMPOSE_AUTO: Implement Phase 2.1 Advanced Analytics - Advanced Price Analytics Dashboard, interactive charts, real-time visualizations, predictive indicators"
            ;;
        "Phase 2.2")
            echo "DECOMPOSE_AUTO: Implement Phase 2.2 Market Intelligence - Market trend analysis, competitor analysis, pricing strategies, market reports"
            ;;
        "Phase 3.0")
            echo "DECOMPOSE_AUTO: Implement Phase 3.0 Compliance & Standards - Ukrainian DBN database, compliance verification system, automated compliance reports"
            ;;
        "Phase 3.1")
            echo "DECOMPOSE_AUTO: Implement Phase 3.1 Compliance Checker - AI project compliance analysis, violation detection, correction recommendations"
            ;;
        "Phase 4.0")
            echo "DECOMPOSE_AUTO: Implement Phase 4.0 CRM System - Client and lead database, AI client scoring, automated sales pipeline, email integration"
            ;;
        "Phase 4.1")
            echo "DECOMPOSE_AUTO: Implement Phase 4.1 Lead Generation Engine - AI client search, automated contact collection, personalized campaigns, A/B testing"
            ;;
        "Phase 5.0")
            echo "DECOMPOSE_AUTO: Implement Phase 5.0 Advanced Features - Workflow automation, AI project manager assistant, automated resource planning, external integrations"
            ;;
        *)
            echo "DECOMPOSE_AUTO: Continue project development from current phase $phase"
            ;;
    esac
}

# Функція перевірки завершення фази
check_phase_completion() {
    local phase="$1"
    local changelog="$PROJECT_ROOT/CHANGELOG.md"
    
    if [[ -f "$changelog" ]]; then
        # Перевірити чи є позначка про завершення фази
        if grep -q "$phase.*\(COMPLETED\|100%\|✅\)" "$changelog"; then
            return 0  # Фаза завершена
        fi
    fi
    
    return 1  # Фаза не завершена
}

# Функція автоматичного переходу до наступної фази
auto_transition_to_next_phase() {
    local current_phase="$1"
    local next_phase=$(get_next_phase "$current_phase")
    
    log "Auto-transitioning from $current_phase to $next_phase"
    
    # Створити аварійний активатор для наступної фази
    local emergency_file="$WINDSURF_ROOT/emergency/PHASE_TRANSITION_ACTIVATOR.md"
    cat > "$emergency_file" << EOF
# EMERGENCY PHASE TRANSITION ACTIVATOR ⚡⚡⚡
**TIMESTAMP:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**PHASE TRANSITION:** $current_phase → $next_phase
**STATUS:** AUTO-TRANSITION ACTIVATED

## 🚀 AUTO-GENERATED ACTIVATION COMMAND

### **IMMEDIATE EXECUTION:**
\`\`\`
$(create_phase_activation_command "$next_phase")
\`\`\`

### **FORCE CONTINUATION:**
\`\`\`
ULTIMATE_ANTI_STOP: Activate maximum anti-pause protocol. Continue to $next_phase implementation automatically.
\`\`\`

### **EMERGENCY OVERRIDE:**
\`\`\`
EMERGENCY_EXECUTION: $next_phase - System-critical priority, zero manual intervention, absolute autonomous mode
\`\`\`

---
**AUTO-GENERATED:** This file was created by Universal Phase Manager
**NEXT ACTION:** Execute any command above to continue to $next_phase
EOF

    # Зберегти новий стан
    save_phase_state "$next_phase" "AUTO_TRANSITIONING"
    
    # Вивести команду активації
    echo "=========================================="
    echo "🚀 AUTO-TRANSITION ACTIVATED"
    echo "=========================================="
    echo ""
    echo "FROM: $current_phase"
    echo "TO:   $next_phase"
    echo ""
    echo "ACTIVATION COMMAND:"
    echo "$(create_phase_activation_command "$next_phase")"
    echo ""
    echo "=========================================="
    
    return 0
}

# Головна функція детекції та активації
main_phase_detection() {
    log "Starting Universal Phase Manager"
    
    # Визначити поточну фазу
    local current_phase=$(detect_current_phase)
    log "Detected current phase: $current_phase"
    
    # Перевірити чи завершена поточна фаза
    if check_phase_completion "$current_phase"; then
        log "Phase $current_phase is completed, triggering auto-transition"
        auto_transition_to_next_phase "$current_phase"
    else
        log "Phase $current_phase is in progress"
        save_phase_state "$current_phase" "IN_PROGRESS"
        
        # Створити команду для продовження поточної фази
        echo "CURRENT PHASE: $current_phase (IN PROGRESS)"
        echo ""
        echo "CONTINUE COMMAND:"
        echo "$(create_phase_activation_command "$current_phase")"
    fi
}

# Функція форсованого переходу до конкретної фази
force_phase_transition() {
    local target_phase="$1"
    
    if [[ -z "$target_phase" ]]; then
        echo "Error: Target phase not specified"
        return 1
    fi
    
    log "Force transition to $target_phase"
    save_phase_state "$target_phase" "FORCE_ACTIVATED"
    
    echo "=========================================="
    echo "🔥 FORCE PHASE TRANSITION"
    echo "=========================================="
    echo ""
    echo "TARGET: $target_phase"
    echo ""
    echo "ACTIVATION COMMAND:"
    echo "$(create_phase_activation_command "$target_phase")"
    echo ""
    echo "=========================================="
}

# Функція активації головної команди
activate_main_command() {
    local command="$1"
    
    case "$command" in
        "WINDSURF_ACTIVATE"|"windsurf-activate"|"activate")
            log "Main activation command received"
            main_phase_detection
            ;;
        "FORCE_PHASE_"*)
            local phase=$(echo "$command" | sed 's/FORCE_PHASE_//')
            force_phase_transition "$phase"
            ;;
        "EMERGENCY_TRANSITION")
            log "Emergency transition activated"
            auto_transition_to_next_phase "$(detect_current_phase)"
            ;;
        "STATUS"|"status")
            if [[ -f "$STATE_FILE" ]]; then
                echo "Current Phase Status:"
                cat "$STATE_FILE" | jq . 2>/dev/null || cat "$STATE_FILE"
            else
                echo "No phase state found"
            fi
            ;;
        *)
            main_phase_detection
            ;;
    esac
}

# Обробка аргументів командного рядка
case "${1:-auto}" in
    "detect"|"auto"|"")
        main_phase_detection
        ;;
    "force")
        force_phase_transition "$2"
        ;;
    "activate")
        activate_main_command "$2"
        ;;
    "status")
        activate_main_command "status"
        ;;
    "emergency")
        activate_main_command "EMERGENCY_TRANSITION"
        ;;
    *)
        activate_main_command "$1"
        ;;
esac
