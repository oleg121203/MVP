#!/usr/bin/env python3
"""
VentAI Enterprise Autoclicker - з автоматичною активацією
Включає логіку: якщо 60 секунд немає змін - активувати VENTAI ENTERPRISE
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

# ===== VENTAI ENTERPRISE НАЛАШТУВАННЯ =====
CONFIDENCE = 0.7
NORMAL_PAUSE = 10
AFTER_CLICK_PAUSE = 60
SEQUENCE_PAUSE = 3
VERBOSE_LOGGING = True

# Нові параметри для VentAI Enterprise
INACTIVITY_TIMEOUT = 60  # 60 секунд без змін
ACTIVATION_COMMAND = "VENTAI ENTERPRISE ACTIVATE"
SCREEN_CHECK_INTERVAL = 10  # Перевіряти екран кожні 10 секунд
SCREEN_SIMILARITY_THRESHOLD = 0.95  # Поріг схожості для детекції змін

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
    print("\n🛑 VentAI Enterprise скрипт зупинено.")
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

def get_screen_hash():
    """Отримує хеш поточного екрану для детекції змін."""
    try:
        # Робимо скріншот тільки області кнопок (більш стабільна зона)
        screen_width, screen_height = pyautogui.size()
        
        # Фокусуємося на правому нижньому куті (де зазвичай кнопки)
        button_area_x = screen_width - 300  # 300px від правого краю
        button_area_y = screen_height - 200  # 200px від низу
        button_area_width = 300
        button_area_height = 200
        
        button_area = pyautogui.screenshot(region=(button_area_x, button_area_y, button_area_width, button_area_height))
        
        # Конвертуємо в сірий для стабільності
        import numpy as np
        gray_array = np.array(button_area.convert('L'))
        
        # Робимо хеш
        img_hash = hashlib.md5(gray_array.tobytes()).hexdigest()
        
        return img_hash
    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"⚠️ Помилка при створенні хешу екрану: {e}")
        return None

def has_screen_changed():
    """Перевіряє чи змінився екран."""
    global last_screen_hash
    
    current_hash = get_screen_hash()
    if current_hash is None:
        return False
    
    if last_screen_hash is None:
        last_screen_hash = current_hash
        return True
    
    if current_hash != last_screen_hash:
        last_screen_hash = current_hash
        return True
    
    return False

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
        
        return True
    except Exception as e:
        print(f"❌ Помилка кліку {button_name}: {e}")
        return False

def find_chat_input_field():
    """Знаходить поле вводу чату."""
    try:
        # Шукаємо по різних паттернах
        screen_width, screen_height = pyautogui.size()
        
        # Перевіряємо нижню частину екрану
        bottom_third = screen_height * 2 // 3
        
        # Можливі координати поля вводу (зазвичай внизу по центру)
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
                
                print(f"✅ Знайдено поле вводу чату в {x}, {y}")
                return (x, y)
            except:
                continue
        
        return None
    except Exception as e:
        print(f"❌ Помилка пошуку поля вводу: {e}")
        return None

def activate_ventai_enterprise():
    """Активує VentAI Enterprise при неактивності."""
    global activation_attempted
    
    if activation_attempted:
        return False
    
    print("\n🚀 АКТИВАЦІЯ VENTAI ENTERPRISE")
    print("===============================")
    
    try:
        # 1. Натискаємо Escape (якщо є діалоги)
        print("1️⃣ Натискаю Escape...")
        pyautogui.press('escape')
        time.sleep(1)
        
        # 2. Шукаємо кнопку Accept All (Escape All)
        print("2️⃣ Шукаю кнопку Accept All...")
        try:
            accept_location = pyautogui.locateOnScreen(ACCEPT_ALL_BUTTON, confidence=CONFIDENCE)
            if accept_location:
                accept_center = pyautogui.center(accept_location)
                pyautogui.click(accept_center.x, accept_center.y, duration=0.1)
                print(f"✅ Натиснуто Accept All в {accept_center}")
                time.sleep(2)
            else:
                print("⚠️ Accept All не знайдено, продовжую...")
        except pyautogui.ImageNotFoundException:
            print("⚠️ Accept All не знайдено, продовжую...")
        
        # 3. Знаходимо поле вводу чату
        print("3️⃣ Шукаю поле вводу чату...")
        chat_input = find_chat_input_field()
        
        if chat_input:
            x, y = chat_input
            
            # 4. Перша активація поля вводу
            print("4️⃣ Перша активація поля вводу...")
            pyautogui.click(x, y, duration=0.1)
            time.sleep(2)  # Чекаємо 2 секунди
            
            # 5. Друга активація поля вводу
            print("5️⃣ Друга активація поля вводу...")
            pyautogui.click(x, y, duration=0.1)
            time.sleep(1)
            
            # 6. Очищаємо поле та вводимо команду
            print("6️⃣ Вводжу команду активації...")
            pyautogui.hotkey('ctrl', 'a')  # Виділити все
            pyautogui.press('backspace')   # Очистити
            time.sleep(0.5)
            
            # Вводимо команду активації
            pyautogui.typewrite(ACTIVATION_COMMAND, interval=0.05)
            time.sleep(1)
            
            # 7. Натискаємо Enter
            print("7️⃣ Відправляю команду (Enter)...")
            pyautogui.press('enter')
            
            print("✅ VENTAI ENTERPRISE АКТИВОВАНО!")
            print(f"📝 Команда: {ACTIVATION_COMMAND}")
            
            activation_attempted = True
            return True
        else:
            print("❌ Не вдалося знайти поле вводу чату")
            return False
            
    except Exception as e:
        print(f"❌ Помилка активації VentAI Enterprise: {e}")
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
    
    # 4. Оновлюємо координати (БЕЗ оновлення часу активності)
    update_button_coordinates(buttons)
    
    print("✅ Hands-Free послідовність завершено!\n")
    return True

def check_inactivity():
    """Перевіряє чи настав час активації VentAI Enterprise."""
    global last_activity_time, activation_attempted
    
    current_time = time.time()
    inactive_time = current_time - last_activity_time
    
    if inactive_time >= INACTIVITY_TIMEOUT and not activation_attempted:
        print(f"\n⏰ НЕАКТИВНІСТЬ {inactive_time:.0f}с (>{INACTIVITY_TIMEOUT}с)")
        print("🎯 Умови для активації VentAI Enterprise виконані!")
        return True
    
    return False

def main_ventai_enterprise_loop():
    """Основний VentAI Enterprise цикл з автоактивацією."""
    global script_running, last_activity_time
    
    print("🚀 VENTAI ENTERPRISE AUTOCLICKER запущено!")
    print("🖱️ Миша залишається ВІЛЬНОЮ")
    print("📜 БЕЗ прокрутки")
    print("⚡ Тільки швидкі кліки")
    print(f"🎯 Автоактивація після {INACTIVITY_TIMEOUT}с неактивності")
    print("💡 Для зупинки: Ctrl+C або створіть stop.flag\n")
    
    cycle = 0
    last_screen_check = time.time()
    
    while script_running:
        try:
            cycle += 1
            current_time = time.time()
            
            if check_stop_flag():
                break
            
            print(f"🔍 Цикл #{cycle}: VentAI Enterprise пошук...")
            
            # Перевіряємо зміни екрану періодично (БЕЗ оновлення активності)
            if current_time - last_screen_check >= SCREEN_CHECK_INTERVAL:
                if has_screen_changed():
                    if VERBOSE_LOGGING:
                        print("📱 Екран змінився (моніторинг)")
                last_screen_check = current_time
            
            # Шукаємо кнопки
            buttons = find_buttons_hands_free()
            
            if 'continue' in buttons and 'accept_all' in buttons:
                if are_buttons_new(buttons):
                    # Виконуємо швидку послідовність
                    if execute_hands_free_sequence(buttons):
                        # ОНОВЛЮЄМО АКТИВНІСТЬ ТІЛЬКИ ПІСЛЯ УСПІШНИХ ДІЙН
                        last_activity_time = time.time()
                        print(f"✅ Активність оновлена! Новий відлік: 0с/{INACTIVITY_TIMEOUT}с")
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
                # Перевіряємо неактивність
                if check_inactivity():
                    if activate_ventai_enterprise():
                        # Після активації робимо довгу паузу
                        print(f"⏰ Пауза {AFTER_CLICK_PAUSE}с після активації...")
                        time.sleep(AFTER_CLICK_PAUSE)
                        last_activity_time = time.time()  # Оновлюємо час активності
                    else:
                        time.sleep(NORMAL_PAUSE)
                else:
                    missing = []
                    if 'continue' not in buttons:
                        missing.append("Continue")
                    if 'accept_all' not in buttons:
                        missing.append("Accept All")
                    
                    inactive_time = current_time - last_activity_time
                    minutes, seconds = divmod(int(inactive_time), 60)
                    time_str = f"{minutes}м {seconds}с" if minutes > 0 else f"{seconds}с"
                    
                    print(f"⏳ Очікую: {', '.join(missing)} (неактивність: {time_str}/{INACTIVITY_TIMEOUT}с)")
                    time.sleep(NORMAL_PAUSE)
                
        except KeyboardInterrupt:
            print("\n🛑 VentAI Enterprise зупинено (Ctrl+C)")
            break
        except Exception as e:
            print(f"❌ Помилка: {e}")
            time.sleep(NORMAL_PAUSE)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # VentAI Enterprise налаштування PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1  # Мінімальна пауза
    
    try:
        if not validate_image_files():
            return False
        
        print("🎯 VENTAI ENTERPRISE MODE:")
        print("• Без прокрутки")
        print("• Без захоплення миші")
        print("• Тільки швидкі кліки")
        print(f"• Автоактивація після {INACTIVITY_TIMEOUT}с\n")
        
        main_ventai_enterprise_loop()
        
        print("✅ VentAI Enterprise завершено.")
        return True
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
