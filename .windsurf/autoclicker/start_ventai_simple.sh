#!/bin/bash

# VentAI Enterprise Autoclicker Launcher - Simplified
# Запуск автокликера з автоматичною активацією VentAI Enterprise

echo "🚀 VENTAI ENTERPRISE AUTOCLICKER"
echo "================================="

# Перевіряємо поточну директорію
if [[ ! -f "autoclicker_ventai_enterprise.py" ]]; then
    echo "❌ Error: autoclicker_ventai_enterprise.py не знайдено"
    echo "   Запустіть скрипт з директорії .windsurf/autoclicker/"
    exit 1
fi

# Перевіряємо Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 не встановлено"
    exit 1
fi

# Перевіряємо віртуальне середовище
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "✅ Віртуальне середовище активовано: $VIRTUAL_ENV"
else
    echo "❌ Віртуальне середовище не активовано"
    echo "   Активуйте його командою: source ../../.venv/bin/activate"
    echo "   Або запустіть з корня проекту: cd ../.. && source .venv/bin/activate && cd .windsurf/autoclicker"
    exit 1
fi

# Тестуємо залежності
echo "📦 Перевірка залежностей..."
python3 -c "import pyautogui; print('✅ PyAutoGUI доступний')" 2>/dev/null || {
    echo "❌ PyAutoGUI не встановлено"
    echo "   Встановіть командою: pip install pyautogui pillow opencv-python"
    exit 1
}

# Перевіряємо зображення
echo "🖼️ Перевірка зображень..."
if [[ ! -f "images/accept_all.png" ]]; then
    echo "⚠️ Warning: images/accept_all.png не знайдено"
fi

if [[ ! -f "images/continue.png" ]]; then
    echo "⚠️ Warning: images/continue.png не знайдено"
fi

echo ""
echo "🎯 VENTAI ENTERPRISE FEATURES:"
echo "• Автоматичне натискання Accept All + Continue"
echo "• Hands-Free режим (без захоплення миші)"
echo "• Автоактивація VentAI Enterprise після 60с неактивності"
echo "• Команда активації: 'VENTAI ENTERPRISE ACTIVATE'"
echo ""
echo "⚡ Для зупинки: Ctrl+C або створіть файл stop.flag"
echo ""

# Запускаємо VentAI Enterprise Autoclicker
echo "🚀 Запуск VentAI Enterprise Autoclicker..."
python3 autoclicker_ventai_enterprise.py
