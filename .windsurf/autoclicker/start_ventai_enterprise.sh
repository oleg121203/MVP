#!/bin/bash

# VentAI Enterprise Autoclicker Launcher
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

# Перевіряємо віртуальне середовище або створюємо локальне
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️ Віртуальне середовище не активовано"
    if [[ ! -d "venv" ]]; then
        echo "📦 Створюю локальне віртуальне середовище..."
        python3 -m venv venv
    fi
    echo "🔄 Активую локальне віртуальне середовище..."
    source venv/bin/activate
    echo "✅ Віртуальне середовище активовано"
    
    # Встановлюємо залежності
    echo "📦 Встановлення залежностей..."
    python3 -m pip install -r requirements.txt
else
    echo "✅ Віртуальне середовище вже активовано: $VIRTUAL_ENV"
    echo "📦 Перевірка залежностей..."
    python3 -c "import pyautogui, cv2, PIL; print('✅ Всі залежності встановлені')" 2>/dev/null || {
        echo "📦 Встановлення відсутніх залежностей..."
        python3 -m pip install -r requirements.txt
    }
fi

# Перевіряємо наявність зображень
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
