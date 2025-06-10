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

