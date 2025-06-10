#!/usr/bin/env python3
"""
Windsurf Chat Autoclicker - HANDS-FREE MODE
БЕЗ прокрутки, БЕЗ захоплення миші, тільки спостереження і швидкі кліки
"""

import os
import sys
import time
import signal
import pyautogui
from pathlib import Path

# ===== HANDS-FREE НАЛАШТУВАННЯ =====
CONFIDENCE = 0.7
NORMAL_PAUSE = 10
AFTER_CLICK_PAUSE = 60
SEQUENCE_PAUSE = 3
VERBOSE_LOGGING = True

# Глобальні змінні
last_button_coordinates = {}
script_running = True

# Шляхи до зображень
script_dir = Path(__file__).parent
images_dir = script_dir / "images"
ACCEPT_ALL_BUTTON = str(images_dir / "accept_all.png")
CONTINUE_BUTTON = str(images_dir / "continue.png")

def signal_handler(signum, frame):
    global script_running
    print("\n🛑 Hands-Free скрипт зупинено.")
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

def find_buttons_hands_free():
    """Шукає кнопки БЕЗ будь-якої прокрутки або рухів миші."""
    buttons_found = {}
    
    try:
        if VERBOSE_LOGGING:
            print("🔍 Hands-Free пошук (БЕЗ прокрутки)...")
        
        # Шукаємо Continue по всьому екрану
        try:
            continue_location = pyautogui.locateOnScreen(CONTINUE_BUTTON, confidence=CONFIDENCE)
            if continue_location:
                continue_center = pyautogui.center(continue_location)
                buttons_found['continue'] = {
                    'location': continue_location,
                    'center': continue_center
                }
                print(f"✅ Знайдено 'Continue': {continue_location}")
        except pyautogui.ImageNotFoundException:
            pass
        
        # Шукаємо Accept All по всьому екрану
        try:
            accept_location = pyautogui.locateOnScreen(ACCEPT_ALL_BUTTON, confidence=CONFIDENCE)
            if accept_location:
                accept_center = pyautogui.center(accept_location)
                buttons_found['accept_all'] = {
                    'location': accept_location,
                    'center': accept_center
                }
                print(f"✅ Знайдено 'Accept all': {accept_location}")
        except pyautogui.ImageNotFoundException:
            pass
            
    except Exception as e:
        print(f"❌ Помилка при пошуку: {e}")
    
    return buttons_found

def are_buttons_new(buttons):
    global last_button_coordinates
    
    for button_type, button_data in buttons.items():
        location = button_data['location']
        key = f"{button_type}_{location.left}_{location.top}"
        
        if key in last_button_coordinates:
            if VERBOSE_LOGGING:
                print(f"⚠️ Кнопка {button_type} в старих координатах")
            return False
    
    print("✅ Знайдено нові кнопки!")
    return True

def update_button_coordinates(buttons):
    global last_button_coordinates
    
    for button_type, button_data in buttons.items():
        location = button_data['location']
        key = f"{button_type}_{location.left}_{location.top}"
        last_button_coordinates[key] = time.time()

def click_button_hands_free(button_data, button_name):
    """Швидкий клік БЕЗ захоплення миші."""
    try:
        center = button_data['center']
        # Зберігаємо поточну позицію миші
        original_pos = pyautogui.position()
        
        # Швидкий клік
        pyautogui.click(center.x, center.y, duration=0.05)
        print(f"⚡ Hands-Free клік: '{button_name}' в {center}")
        
        # НЕ повертаємо мишу для мінімального втручання
        
        return True
    except Exception as e:
        print(f"❌ Помилка кліку {button_name}: {e}")
        return False

def execute_hands_free_sequence(buttons):
    """Виконує швидку послідовність БЕЗ захоплення миші."""
    print("\n⚡ HANDS-FREE: Швидка послідовність...\n")
    
    # 1. Accept All
    print("1️⃣ Швидкий клік Accept All...")
    if not click_button_hands_free(buttons['accept_all'], 'Accept All'):
        return False
    
    # 2. Пауза
    print(f"⏳ Пауза {SEQUENCE_PAUSE}с...")
    time.sleep(SEQUENCE_PAUSE)
    
    # 3. Continue
    print("2️⃣ Швидкий клік Continue...")
    if not click_button_hands_free(buttons['continue'], 'Continue'):
        return False
    
    # 4. Оновлюємо координати
    update_button_coordinates(buttons)
    
    print("✅ Hands-Free послідовність завершено!\n")
    return True

def main_hands_free_loop():
    """Основний Hands-Free цикл БЕЗ прокрутки."""
    global script_running
    
    print("🚀 HANDS-FREE MODE запущено!")
    print("🖱️ Миша залишається ВІЛЬНОЮ")
    print("📜 БЕЗ прокрутки")
    print("⚡ Тільки швидкі кліки")
    print("💡 Для зупинки: Ctrl+C або створіть stop.flag\n")
    
    cycle = 0
    
    while script_running:
        try:
            cycle += 1
            
            if check_stop_flag():
                break
            
            print(f"🔍 Цикл #{cycle}: Hands-Free пошук...")
            
            # Шукаємо БЕЗ прокрутки
            buttons = find_buttons_hands_free()
            
            if 'continue' in buttons and 'accept_all' in buttons:
                if are_buttons_new(buttons):
                    # Виконуємо швидку послідовність
                    if execute_hands_free_sequence(buttons):
                        print(f"⏰ Пауза {AFTER_CLICK_PAUSE}с...")
                        
                        # Довга пауза з рідкими повідомленнями
                        for remaining in range(AFTER_CLICK_PAUSE, 0, -1):
                            if remaining % 15 == 0 or remaining <= 5:
                                print(f"⏳ {remaining}с до наступного циклу...")
                            time.sleep(1)
                            
                            if check_stop_flag():
                                return
                    else:
                        time.sleep(NORMAL_PAUSE)
                else:
                    print("⏳ Старі координати, чекаю нові...")
                    time.sleep(NORMAL_PAUSE)
            else:
                missing = []
                if 'continue' not in buttons:
                    missing.append("Continue")
                if 'accept_all' not in buttons:
                    missing.append("Accept All")
                
                print(f"⏳ Очікую: {', '.join(missing)}")
                time.sleep(NORMAL_PAUSE)
                
        except KeyboardInterrupt:
            print("\n🛑 Hands-Free зупинено (Ctrl+C)")
            break
        except Exception as e:
            print(f"❌ Помилка: {e}")
            time.sleep(NORMAL_PAUSE)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Hands-Free налаштування PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1  # Мінімальна пауза
    
    try:
        if not validate_image_files():
            return False
        
        print("🎯 HANDS-FREE MODE:")
        print("• Без прокрутки")
        print("• Без захоплення миші")
        print("• Тільки швидкі кліки\n")
        
        main_hands_free_loop()
        
        print("✅ Hands-Free завершено.")
        return True
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)