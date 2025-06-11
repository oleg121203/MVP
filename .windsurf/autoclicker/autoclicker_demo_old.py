#!/usr/bin/env python3
"""
VentAI Enterprise Autoclicker - DEMO VERSION (швидкий тест)
Тестова версія з коротким таймаутом 10 секунд замість 60
"""

import os
import sys
import time
import signal
import pyautogui
import hashlib
from pathlib import Path
from PIL import Image
import io

# ===== DEMO НАЛАШТУВАННЯ =====
CONFIDENCE = 0.7
NORMAL_PAUSE = 5  # Коротша пауза для демо
AFTER_CLICK_PAUSE = 30  # Коротша пауза після кліків
SEQUENCE_PAUSE = 2  # Коротша пауза між кліками
VERBOSE_LOGGING = True

# DEMO параметри - ШВИДКИЙ ТЕСТ
INACTIVITY_TIMEOUT = 10  # 10 секунд замість 60 для тестування
ACTIVATION_COMMAND = "VENTAI ENTERPRISE ACTIVATE"
SCREEN_CHECK_INTERVAL = 2  # Частіша перевірка для демо

# Глобальні змінні
last_button_coordinates = {}
script_running = True
last_screen_hash = None
last_activity_time = time.time()
activation_attempted = False

# Шляхи до зображень
script_dir = Path(__file__).parent
images_dir = script_dir / "images"
ACCEPT_ALL_BUTTON = str(images_dir / "accept_all.png")
CONTINUE_BUTTON = str(images_dir / "continue.png")

def signal_handler(signum, frame):
    global script_running
    print("\n🛑 VentAI Enterprise DEMO зупинено.")
    script_running = False
    sys.exit(0)

def check_stop_flag():
    stop_flag_path = script_dir / "stop.flag"
    if stop_flag_path.exists():
        print("🛑 Знайдено файл 'stop.flag'. Зупиняю скрипт...")
        stop_flag_path.unlink()
        return True
    return False

def validate_image_files():
    missing_files = []
    if not os.path.exists(ACCEPT_ALL_BUTTON):
        missing_files.append(ACCEPT_ALL_BUTTON)
    if not os.path.exists(CONTINUE_BUTTON):
        missing_files.append(CONTINUE_BUTTON)
    
    if missing_files:
        print("❌ Відсутні файли зображень:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Файли зображень знайдено:")
    print(f"   - {ACCEPT_ALL_BUTTON}")
    print(f"   - {CONTINUE_BUTTON}")
    return True

def activate_ventai_enterprise():
    """DEMO активація VentAI Enterprise."""
    global activation_attempted
    
    if activation_attempted:
        print("⚠️ Активація вже була виконана в цій сесії")
        return False
    
    print("\n🚀 DEMO АКТИВАЦІЯ VENTAI ENTERPRISE")
    print("===================================")
    
    try:
        # 1. Натискаємо Escape
        print("1️⃣ Натискаю Escape...")
        pyautogui.press('escape')
        time.sleep(1)
        
        # 2. Шукаємо Accept All
        print("2️⃣ Шукаю кнопку Accept All...")
        try:
            accept_location = pyautogui.locateOnScreen(ACCEPT_ALL_BUTTON, confidence=CONFIDENCE)
            if accept_location:
                accept_center = pyautogui.center(accept_location)
                pyautogui.click(accept_center.x, accept_center.y, duration=0.1)
                print(f"✅ Натиснуто Accept All в {accept_center}")
                time.sleep(1)
            else:
                print("⚠️ Accept All не знайдено")
        except pyautogui.ImageNotFoundException:
            print("⚠️ Accept All не знайдено")
        
        # 3. Знаходимо поле чату та вводимо команду
        print("3️⃣ Шукаю поле вводу...")
        screen_width, screen_height = pyautogui.size()
        
        # Пробуємо центр внизу екрану
        chat_x = screen_width // 2
        chat_y = screen_height - 100
        
        print(f"4️⃣ Кліканю на поле чату ({chat_x}, {chat_y})...")
        pyautogui.click(chat_x, chat_y, duration=0.1)
        time.sleep(1)
        
        # 5. Очищаємо та вводимо команду
        print("5️⃣ Вводжу DEMO команду...")
        pyautogui.hotkey('cmd', 'a')  # Для macOS
        pyautogui.press('backspace')
        time.sleep(0.5)
        
        # Вводимо команду
        print(f"📝 Команда: {ACTIVATION_COMMAND}")
        pyautogui.typewrite(ACTIVATION_COMMAND, interval=0.1)
        time.sleep(1)
        
        # 6. Натискаємо Enter
        print("6️⃣ Відправляю команду (Enter)...")
        pyautogui.press('enter')
        
        print("✅ DEMO АКТИВАЦІЯ ЗАВЕРШЕНА!")
        activation_attempted = True
        return True
        
    except Exception as e:
        print(f"❌ Помилка DEMO активації: {e}")
        return False

def main_demo_loop():
    """DEMO цикл з швидким тестуванням."""
    global script_running, last_activity_time
    
    print("🚀 VENTAI ENTERPRISE DEMO запущено!")
    print("🎯 ШВИДКИЙ ТЕСТ - активація через 10 секунд!")
    print("🖱️ Миша залишається ВІЛЬНОЮ")
    print("💡 Для зупинки: Ctrl+C\n")
    
    cycle = 0
    
    while script_running:
        try:
            cycle += 1
            current_time = time.time()
            
            if check_stop_flag():
                break
            
            print(f"🔍 DEMO Цикл #{cycle}...")
            
            # Шукаємо кнопки
            try:
                accept_location = pyautogui.locateOnScreen(ACCEPT_ALL_BUTTON, confidence=CONFIDENCE)
                continue_location = pyautogui.locateOnScreen(CONTINUE_BUTTON, confidence=CONFIDENCE)
                
                if accept_location and continue_location:
                    print("✅ Знайдено ОБІ кнопки - виконую кліки...")
                    
                    # Accept All
                    accept_center = pyautogui.center(accept_location)
                    pyautogui.click(accept_center.x, accept_center.y, duration=0.1)
                    print(f"⚡ Клік Accept All: {accept_center}")
                    time.sleep(SEQUENCE_PAUSE)
                    
                    # Continue
                    continue_center = pyautogui.center(continue_location)
                    pyautogui.click(continue_center.x, continue_center.y, duration=0.1)
                    print(f"⚡ Клік Continue: {continue_center}")
                    
                    last_activity_time = current_time
                    print(f"⏰ Пауза {AFTER_CLICK_PAUSE}с після кліків...")
                    time.sleep(AFTER_CLICK_PAUSE)
                    
                else:
                    # Перевіряємо неактивність
                    inactive_time = current_time - last_activity_time
                    
                    if inactive_time >= INACTIVITY_TIMEOUT and not activation_attempted:
                        print(f"\n⏰ DEMO НЕАКТИВНІСТЬ {inactive_time:.0f}с (>{INACTIVITY_TIMEOUT}с)")
                        print("🎯 ДЕМО умови виконані - активую VentAI Enterprise!")
                        
                        if activate_ventai_enterprise():
                            print(f"⏰ Пауза {AFTER_CLICK_PAUSE}с після активації...")
                            time.sleep(AFTER_CLICK_PAUSE)
                            last_activity_time = current_time
                        else:
                            time.sleep(NORMAL_PAUSE)
                    else:
                        missing = []
                        if not accept_location:
                            missing.append("Accept All")
                        if not continue_location:
                            missing.append("Continue")
                        
                        print(f"⏳ DEMO очікую: {', '.join(missing)} (неактивність: {inactive_time:.0f}с/{INACTIVITY_TIMEOUT}с)")
                        time.sleep(NORMAL_PAUSE)
                        
            except Exception as e:
                print(f"❌ Помилка пошуку: {e}")
                time.sleep(NORMAL_PAUSE)
                
        except KeyboardInterrupt:
            print("\n🛑 DEMO зупинено (Ctrl+C)")
            break
        except Exception as e:
            print(f"❌ DEMO помилка: {e}")
            time.sleep(NORMAL_PAUSE)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # DEMO налаштування PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    try:
        if not validate_image_files():
            return False
        
        print("🎯 VENTAI ENTERPRISE DEMO MODE:")
        print("• Швидкий тест (10с замість 60с)")
        print("• Без прокрутки")
        print("• Тільки швидкі кліки")
        print("• Демо активація VentAI Enterprise\n")
        
        main_demo_loop()
        
        print("✅ VentAI Enterprise DEMO завершено.")
        return True
        
    except Exception as e:
        print(f"❌ DEMO помилка: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
