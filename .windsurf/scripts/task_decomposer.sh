#!/bin/zsh

# Windsurf Task Decomposition Monitor
# Автоматично активує розбиття завдань та моніторить прогрес

WINDSURF_DIR="/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf"
PROGRESS_DIR="$WINDSURF_DIR/progress"
RULES_DIR="$WINDSURF_DIR/rules"

# Створити необхідні директорії
mkdir -p "$PROGRESS_DIR"
mkdir -p "$RULES_DIR"
mkdir -p "$WINDSURF_DIR/activation"
mkdir -p "$WINDSURF_DIR/status"

# Функція для виявлення великих завдань
detect_large_task() {
    local task_input="$1"
    
    # Ключові слова для виявлення великих завдань
    large_task_keywords=(
        "create complete"
        "full setup"
        "entire system"
        "all tests"
        "comprehensive"
        "implement complete"
        "setup all"
        "create entire"
        "build full"
        "develop complete"
    )
    
    for keyword in "${large_task_keywords[@]}"; do
        if [[ "$task_input" == *"$keyword"* ]]; then
            return 0  # Велике завдання виявлено
        fi
    done
    
    # Перевірка кількості компонентів
    component_count=$(echo "$task_input" | grep -o -E "(test|component|page|service|api|database|frontend|backend)" | wc -l)
    if [[ $component_count -gt 3 ]]; then
        return 0  # Велике завдання виявлено
    fi
    
    return 1  # Звичайне завдання
}

# Функція для створення шаблону розбиття
create_decomposition_template() {
    local original_task="$1"
    local decomposition_file="$PROGRESS_DIR/current_decomposition.json"
    
    cat > "$decomposition_file" << EOF
{
  "originalTask": "$original_task",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "active",
  "currentPhase": 1,
  "phases": [
    {
      "id": 1,
      "description": "Phase 1: Initial setup and configuration",
      "status": "pending",
      "estimatedTokens": 200
    },
    {
      "id": 2,
      "description": "Phase 2: Core implementation",
      "status": "pending",
      "estimatedTokens": 300
    },
    {
      "id": 3,
      "description": "Phase 3: Testing and validation",
      "status": "pending",
      "estimatedTokens": 250
    },
    {
      "id": 4,
      "description": "Phase 4: Integration and optimization",
      "status": "pending",
      "estimatedTokens": 200
    },
    {
      "id": 5,
      "description": "Phase 5: Documentation and cleanup",
      "status": "pending",
      "estimatedTokens": 150
    }
  ],
  "autoProgress": true,
  "totalEstimatedTokens": 1100
}
EOF

    echo "Decomposition template created: $decomposition_file"
}

# Функція для активації автоматичного режиму
activate_auto_mode() {
    local activation_file="$WINDSURF_DIR/activation/auto_decompose.active"
    
    cat > "$activation_file" << EOF
# Auto-Decomposition Activated
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
STATUS=ACTIVE
MODE=AUTO_DECOMPOSE
PRIORITY=MAXIMUM

# Commands
DECOMPOSE_LARGE_TASKS=true
AUTO_PROGRESS=true
PAUSE_OVERRIDE=true
CONTINUE_KILLER=true

# Rules Active
- task_decomposition_auto.md
- continue_response_killer.md
- cascade_error_override.md
- auto_context_loader.md
EOF

    echo "Auto-decomposition mode ACTIVATED"
}

# Функція для моніторингу статусу
monitor_status() {
    local status_file="$WINDSURF_DIR/status/decomposition_monitor.log"
    
    echo "[$(date)] Monitoring decomposition status..." >> "$status_file"
    
    # Перевірити чи є активні розбиття
    if [[ -f "$PROGRESS_DIR/current_decomposition.json" ]]; then
        local current_phase=$(jq -r '.currentPhase' "$PROGRESS_DIR/current_decomposition.json" 2>/dev/null || echo "unknown")
        local total_phases=$(jq -r '.phases | length' "$PROGRESS_DIR/current_decomposition.json" 2>/dev/null || echo "unknown")
        
        echo "[$(date)] Active decomposition: Phase $current_phase of $total_phases" >> "$status_file"
    fi
}

# Функція для створення швидких команд
create_quick_commands() {
    local commands_file="$WINDSURF_DIR/activation/quick_commands.sh"
    
    cat > "$commands_file" << 'EOF'
#!/bin/zsh

# Швидкі команди для керування розбиттям завдань

# Активувати автоматичне розбиття
alias windsurf-auto='echo "WINDSURF ACTIVATE: Load all rules, auto-decompose large tasks, continue automatically"'

# Перевірити статус
alias windsurf-status='cat ~/.windsurf/progress/current_decomposition.json 2>/dev/null | jq . || echo "No active decomposition"'

# Форсувати продовження
alias windsurf-force='echo "CRITICAL OVERRIDE: Activate maximum priority never-stop protocol. Continue automatically."'

# Розбити завдання вручну
windsurf-decompose() {
    echo "DECOMPOSE: $1"
}

# Перейти до наступної фази
alias windsurf-next='echo "PHASE_NEXT: Continue to next decomposition phase automatically"'

# Перезапустити поточну фазу
alias windsurf-retry='echo "PHASE_RESTART: Retry current phase with enhanced context"'

EOF

    chmod +x "$commands_file"
    echo "Quick commands created: $commands_file"
}

# Головна функція
main() {
    echo "🚀 Windsurf Task Decomposition System Setup"
    echo "=========================================="
    
    # Активувати автоматичний режим
    activate_auto_mode
    
    # Створити швидкі команди
    create_quick_commands
    
    # Запустити моніторинг
    monitor_status
    
    echo ""
    echo "✅ Setup completed!"
    echo ""
    echo "Available commands:"
    echo "  windsurf-auto    - Activate auto-decomposition"
    echo "  windsurf-status  - Check current status"
    echo "  windsurf-force   - Force continue override"
    echo "  windsurf-next    - Go to next phase"
    echo "  windsurf-retry   - Retry current phase"
    echo ""
    echo "To use: source $WINDSURF_DIR/activation/quick_commands.sh"
    
    # Створити приклад використання
    echo ""
    echo "Example usage:"
    echo '  windsurf-decompose "Create complete testing framework for VentAI app"'
}

# Перевірити аргументи команди
case "${1:-setup}" in
    "setup")
        main
        ;;
    "detect")
        if detect_large_task "$2"; then
            echo "Large task detected: $2"
            create_decomposition_template "$2"
        else
            echo "Regular task: $2"
        fi
        ;;
    "monitor")
        monitor_status
        ;;
    "activate")
        activate_auto_mode
        ;;
    *)
        echo "Usage: $0 {setup|detect|monitor|activate}"
        exit 1
        ;;
esac
