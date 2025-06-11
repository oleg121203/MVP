#!/usr/bin/env python3
"""
VentAI Enterprise Autoclicker - ДЕМО версія з коротким таймаутом
Тестування логіки активації за 20 секунд замість 60
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

# ===== ДЕМО НАЛАШТУВАННЯ =====
CONFIDENCE = 0.7
NORMAL_PAUSE = 5  # Коротша пауза для демо
AFTER_CLICK_PAUSE = 30  # Коротша пауза після кліків
SEQUENCE_PAUSE = 2
VERBOSE_LOGGING = True

# Нові параметри для VentAI Enterprise ДЕМО
INACTIVITY_TIMEOUT = 20  # 20 секунд для швидкого тестування
ACTIVATION_COMMAND = "VENTAI ENTERPRISE ACTIVATE"
SCREEN_CHECK_INTERVAL = 5  # Частіша перевірка для демо

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
    print("\n🛑 VentAI Enterprise ДЕМО зупинено.")
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
            print("🔍 ДЕМО: Hands-Free пошук...")
        
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
        pyautogui.click(center.x, center.y, duration=0.05)
        print(f"⚡ ДЕМО клік: '{button_name}' в {center}")
        return True
    except Exception as e:
        print(f"❌ Помилка кліку {button_name}: {e}")
        return False

def find_chat_input_field():
    """Знаходить поле вводу чату."""
    try:
        screen_width, screen_height = pyautogui.size()
        
        # Можливі координати поля вводу
        possible_inputs = [
            (screen_width // 2, screen_height - 100),
            (screen_width // 2, screen_height - 150),
            (screen_width // 2, screen_height - 80),
        ]
        
        for x, y in possible_inputs:
            try:
                pyautogui.click(x, y, duration=0.1)
                time.sleep(0.5)
                
                # Перевіряємо чи активне поле вводу
                pyautogui.typewrite("test")
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                
                print(f"✅ ДЕМО: Знайдено поле вводу в {x}, {y}")
                return (x, y)
            except:
                continue
        
        return None
    except Exception as e:
        print(f"❌ Помилка пошуку поля вводу: {e}")
        return None

def activate_ventai_enterprise():
    """ДЕМО: Активує VentAI Enterprise при неактивності."""
    global activation_attempted
    
    if activation_attempted:
        return False
    
    print("\n🚀 ДЕМО: АКТИВАЦІЯ VENTAI ENTERPRISE")
    print("===================================")
    
    try:
        # 1. Натискаємо Escape
        print("1️⃣ ДЕМО: Натискаю Escape...")
        pyautogui.press('escape')
        time.sleep(1)
        
        # 2. Шукаємо Accept All
        print("2️⃣ ДЕМО: Шукаю Accept All...")
        try:
            accept_location = pyautogui.locateOnScreen(ACCEPT_ALL_BUTTON, confidence=CONFIDENCE)
            if accept_location:
                accept_center = pyautogui.center(accept_location)
                pyautogui.click(accept_center.x, accept_center.y, duration=0.1)
                print(f"✅ ДЕМО: Натиснуто Accept All в {accept_center}")
                time.sleep(2)
            else:
                print("⚠️ ДЕМО: Accept All не знайдено")
        except pyautogui.ImageNotFoundException:
            print("⚠️ ДЕМО: Accept All не знайдено")
        
        # 3. Знаходимо поле чату
        print("3️⃣ ДЕМО: Шукаю поле чату...")
        chat_input = find_chat_input_field()
        
        if chat_input:
            x, y = chat_input
            
            # 4. ПЕРША активація поля
            print("4️⃣ ДЕМО: ПЕРША активація поля...")
            pyautogui.click(x, y, duration=0.1)
            time.sleep(2)  # Пауза 2 секунди
            
            # 5. ДРУГА активація поля
            print("5️⃣ ДЕМО: ДРУГА активація поля...")
            pyautogui.click(x, y, duration=0.1)
            time.sleep(1)
            
            # 6. Очищаємо та вводимо команду
            print("6️⃣ ДЕМО: Вводжу команду...")
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            time.sleep(0.5)
            
            # Вводимо команду
            pyautogui.typewrite(ACTIVATION_COMMAND, interval=0.05)
            time.sleep(1)
            
            # 7. Enter
            print("7️⃣ ДЕМО: Відправляю (Enter)...")
            pyautogui.press('enter')
            
            print("✅ ДЕМО: VENTAI ENTERPRISE АКТИВОВАНО!")
            print(f"📝 Команда: {ACTIVATION_COMMAND}")
            
            activation_attempted = True
            return True
        else:
            print("❌ ДЕМО: Поле чату не знайдено")
            return False
            
    except Exception as e:
        print(f"❌ ДЕМО помилка: {e}")
        return False

def execute_hands_free_sequence(buttons):
    """ДЕМО: Виконує швидку послідовність."""
    print("\n⚡ ДЕМО: HANDS-FREE послідовність...\n")
    
    # 1. Accept All
    print("1️⃣ ДЕМО: Клік Accept All...")
    if not click_button_hands_free(buttons['accept_all'], 'Accept All'):
        return False
    
    # 2. Пауза
    print(f"⏳ ДЕМО: Пауза {SEQUENCE_PAUSE}с...")
    time.sleep(SEQUENCE_PAUSE)
    
    # 3. Continue
    print("2️⃣ ДЕМО: Клік Continue...")
    if not click_button_hands_free(buttons['continue'], 'Continue'):
        return False
    
    # 4. Оновлюємо координати
    update_button_coordinates(buttons)
    
    print("✅ ДЕМО: Послідовність завершено!\n")
    return True

def check_inactivity():
    """ДЕМО: Перевіряє неактивність."""
    global last_activity_time, activation_attempted
    
    current_time = time.time()
    inactive_time = current_time - last_activity_time
    
    if inactive_time >= INACTIVITY_TIMEOUT and not activation_attempted:
        print(f"\n⏰ ДЕМО: НЕАКТИВНІСТЬ {inactive_time:.0f}с (>{INACTIVITY_TIMEOUT}с)")
        print("🎯 ДЕМО: Умови активації виконані!")
        return True
    
    return False

def main_demo_loop():
    """ДЕМО: Основний цикл з швидкою активацією."""
    global script_running, last_activity_time
    
    print("🚀 VENTAI ENTERPRISE АВТОКЛИКЕР - ДЕМО")
    print("=====================================")
    print("🖱️ Миша залишається ВІЛЬНОЮ")
    print("📜 БЕЗ прокрутки")
    print("⚡ Тільки швидкі кліки")
    print(f"🎯 ДЕМО: Автоактивація після {INACTIVITY_TIMEOUT}с неактивності")
    print("💡 Для зупинки: Ctrl+C або створіть stop.flag\n")
    
    cycle = 0
    
    while script_running:
        try:
            cycle += 1
            current_time = time.time()
            
            if check_stop_flag():
                break
            
            print(f"🔍 ДЕМО Цикл #{cycle}: Пошук...")
            
            # Шукаємо кнопки
            buttons = find_buttons_hands_free()
            
            if 'continue' in buttons and 'accept_all' in buttons:
                if are_buttons_new(buttons):
                    # Виконуємо послідовність
                    if execute_hands_free_sequence(buttons):
                        # ОНОВЛЮЄМО АКТИВНІСТЬ В КІНЦІ
                        last_activity_time = time.time()
                        print(f"✅ ДЕМО: Активність оновлена! Новий відлік: 0с/{INACTIVITY_TIMEOUT}с")
                        print(f"⏰ ДЕМО: Пауза {AFTER_CLICK_PAUSE}с...")
                        
                        # Коротша пауза для демо
                        for remaining in range(AFTER_CLICK_PAUSE, 0, -1):
                            if remaining % 10 == 0 or remaining <= 3:
                                print(f"⏳ ДЕМО: {remaining}с до наступного циклу...")
                            time.sleep(1)
                            
                            if check_stop_flag():
                                return
                    else:
                        time.sleep(NORMAL_PAUSE)
                else:
                    print("⏳ ДЕМО: Старі координати...")
                    time.sleep(NORMAL_PAUSE)
            else:
                # Перевіряємо неактивність
                if check_inactivity():
                    if activate_ventai_enterprise():
                        print(f"⏰ ДЕМО: Пауза {AFTER_CLICK_PAUSE}с після активації...")
                        time.sleep(AFTER_CLICK_PAUSE)
                        last_activity_time = time.time()
                    else:
                        time.sleep(NORMAL_PAUSE)
                else:
                    missing = []
                    if 'continue' not in buttons:
                        missing.append("Continue")
                    if 'accept_all' not in buttons:
                        missing.append("Accept All")
                    
                    inactive_time = current_time - last_activity_time
                    print(f"⏳ ДЕМО: Очікую: {', '.join(missing)} (неактивність: {inactive_time:.0f}с/{INACTIVITY_TIMEOUT}с)")
                    time.sleep(NORMAL_PAUSE)
                
        except KeyboardInterrupt:
            print("\n🛑 ДЕМО зупинено (Ctrl+C)")
            break
        except Exception as e:
            print(f"❌ ДЕМО помилка: {e}")
            time.sleep(NORMAL_PAUSE)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # ДЕМО налаштування PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    try:
        if not validate_image_files():
            return False
        
        print("🎯 VENTAI ENTERPRISE ДЕМО MODE:")
        print("• Швидка активація (20с)")
        print("• Без прокрутки")
        print("• Без захоплення миші")
        print("• Тільки швидкі кліки\n")
        
        main_demo_loop()
        
        print("✅ ДЕМО завершено.")
        return True
        
    except Exception as e:
        print(f"❌ ДЕМО помилка: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)