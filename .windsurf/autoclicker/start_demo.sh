#!/bin/bash

# VentAI Enterprise Autoclicker - DEMO VERSION
# Швидкий тест з таймаутом 10 секунд

echo "🚀 VENTAI ENTERPRISE DEMO"
echo "========================="

# Перевіряємо файли
if [[ ! -f "autoclicker_demo.py" ]]; then
    echo "❌ Error: autoclicker_demo.py не знайдено"
    exit 1
fi

# Перевіряємо віртуальне середовище
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "❌ Віртуальне середовище не активовано"
    echo "   Команда: source ../../.venv/bin/activate"
    exit 1
fi

echo "✅ Віртуальне середовище: $VIRTUAL_ENV"

# Тестуємо PyAutoGUI
python3 -c "import pyautogui; print('✅ PyAutoGUI готовий')" || {
    echo "❌ PyAutoGUI не працює"
    exit 1
}

echo ""
echo "🎯 DEMO FEATURES:"
echo "• ⚡ ШВИДКИЙ ТЕСТ: активація через 10 секунд (замість 60)"
echo "• 🔍 Пошук кнопок Accept All + Continue"
echo "• 🚀 Автоматична активація VentAI Enterprise"
echo "• 📝 Команда: 'VENTAI ENTERPRISE ACTIVATE'"
echo ""
echo "⚠️  ДЕМО РЕЖИМ - для реального використання запустіть:"
echo "   ./start_ventai_simple.sh"
echo ""
echo "⚡ Для зупинки: Ctrl+C"
echo ""

read -p "🚀 Запустити DEMO? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Запуск VentAI Enterprise DEMO..."
    python3 autoclicker_demo.py
else
    echo "❌ DEMO скасовано"
fi
