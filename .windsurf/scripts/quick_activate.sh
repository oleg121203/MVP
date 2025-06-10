#!/bin/zsh

# UNIVERSAL PHASE MANAGER - QUICK ACTIVATION COMMANDS

SCRIPTS_DIR="/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/scripts"
PHASE_MANAGER="$SCRIPTS_DIR/universal_phase_manager.sh"

# Переконатися що скрипт виконується
chmod +x "$PHASE_MANAGER"

echo "🚀 UNIVERSAL PHASE MANAGER - QUICK COMMANDS"
echo "============================================"

# Швидкі команди для зручності
alias windsurf-activate="$PHASE_MANAGER activate WINDSURF_ACTIVATE"
alias windsurf-status="$PHASE_MANAGER status"
alias windsurf-emergency="$PHASE_MANAGER emergency"
alias windsurf-force-next="$PHASE_MANAGER emergency"

# Команди для конкретних фаз
alias windsurf-phase-1.1="$PHASE_MANAGER force 'Phase 1.1'"
alias windsurf-phase-1.2="$PHASE_MANAGER force 'Phase 1.2'"
alias windsurf-phase-1.3="$PHASE_MANAGER force 'Phase 1.3'"
alias windsurf-phase-2.0="$PHASE_MANAGER force 'Phase 2.0'"
alias windsurf-phase-2.1="$PHASE_MANAGER force 'Phase 2.1'"

echo "Available Commands:"
echo "=================="
echo "windsurf-activate     - Auto-detect and continue current/next phase"
echo "windsurf-status       - Show current phase status"
echo "windsurf-emergency    - Force transition to next phase"
echo "windsurf-force-next   - Emergency progression"
echo ""
echo "Specific Phase Commands:"
echo "windsurf-phase-1.1    - Force start Phase 1.1"
echo "windsurf-phase-1.2    - Force start Phase 1.2"  
echo "windsurf-phase-1.3    - Force start Phase 1.3"
echo "windsurf-phase-2.0    - Force start Phase 2.0"
echo "windsurf-phase-2.1    - Force start Phase 2.1"
echo ""
echo "Main Activation Commands for Windsurf:"
echo "======================================"

# Запустити автоматичну детекцію
echo "🔍 Running auto-detection..."
$PHASE_MANAGER detect

echo ""
echo "📋 ГОТОВІ КОМАНДИ ДЛЯ ВСТАВКИ В WINDSURF:"
echo "========================================="
echo ""

# Створити файл з готовими командами
cat > /Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/READY_COMMANDS.txt << 'EOF'
# WINDSURF UNIVERSAL ACTIVATION COMMANDS - ГОТОВО ДО ВСТАВКИ

## ГОЛОВНА КОМАНДА АКТИВАЦІЇ
WINDSURF_ACTIVATE: Auto-detect current phase, check completion, auto-transition to next phase if needed, continue execution automatically.

## ФОРСОВАНИЙ ПЕРЕХІД ДО НАСТУПНОЇ ФАЗИ  
EMERGENCY_PHASE_PROGRESSION: Phase transition failed, activate Universal Phase Manager, force progression to next phase automatically.

## ЕКСТРЕНА АКТИВАЦІЯ
EMERGENCY_EXECUTION: Phase transition and continuation - System-critical priority, zero manual intervention, absolute autonomous mode.

## УЛЬТИМАТИВНИЙ АНТИ-СТОП
ULTIMATE_ANTI_STOP: Activate maximum anti-pause protocol. Auto-detect phases and continue automatically. Zero stops guaranteed.

## ДЕКОМПОЗИЦІЯ ПОТОЧНОЇ ФАЗИ
DECOMPOSE_AUTO: Continue current project phase implementation with automatic task decomposition and continuous execution.

# ПРОСТО СКОПІЮЙТЕ БУДЬ-ЯКУ КОМАНДУ ВИЩЕ І ВСТАВТЕ В WINDSURF!
EOF

echo "✅ Готові команди збережені в: .windsurf/READY_COMMANDS.txt"
echo ""
echo "🎯 ОСНОВНА КОМАНДА ДЛЯ ВСТАВКИ:"
echo "WINDSURF_ACTIVATE: Auto-detect current phase, check completion, auto-transition to next phase if needed, continue execution automatically."
