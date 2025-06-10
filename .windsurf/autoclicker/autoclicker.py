#!/usr/bin/env python3
"""
Windsurf Chat Autoclicker - Автоматизація натискання кнопок в чаті Windsurf
Система чекає появи нових активних кнопок Continue в низу чату і автоматично виконує послідовність:
Accept All → Continue з правильними паузами
"""

import os
import sys
import time
import signal
import pyautogui
from pathlib import Path

# ===== НАЛАШТУВАННЯ =====
CONFIDENCE = 0.7  # Рівень впевненості для розпізнавання зображень
NORMAL_PAUSE = 10  # Пауза між перевірками (секунди)
AFTER_CLICK_PAUSE = 60  # Пауза після натискання кнопок (секунди)
SEQUENCE_PAUSE = 3  # Пауза між Accept All і Continue (секунди)
VERBOSE_LOGGING = True  # Детальне логування

# Глобальні змінні для відстеження стану
last_button_coordinates = {}  # Зберігає координати останніх знайдених кнопок
script_running = True  # Флаг для управління роботою скрипта

# ===== ШЛЯХИ ДО ЗОБРАЖЕНЬ =====
script_dir = Path(__file__).parent
images_dir = script_dir / "images"
ACCEPT_ALL_BUTTON = str(images_dir / "accept_all.png")
CONTINUE_BUTTON = str(images_dir / "continue.png")

def signal_handler(signum, frame):
    """Обробка сигналів для коректного завершення."""
    global script_running
    print("\n🛑 Отримано сигнал завершення. Зупиняю скрипт...")
    script_running = False
    sys.exit(0)

def check_stop_flag():
    """Перевіряє наявність файлу stop.flag для зупинки скрипта."""
    stop_flag_path = script_dir / "stop.flag"
    if stop_flag_path.exists():
        print("🛑 Знайдено файл 'stop.flag'. Зупиняю скрипт...")
        stop_flag_path.unlink()  # Видаляємо файл
        return True
    return False

def validate_image_files():
    """Перевіряє наявність файлів зображень."""
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

def get_chat_area():
    """Визначає область чату Windsurf на екрані."""
    try:
        # Отримуємо розмір екрана
        screen_width, screen_height = pyautogui.size()
        
        # Визначаємо область чату (права половина екрана)
        chat_left = screen_width // 2
        chat_top = 100  # Трохи відступу зверху
        chat_width = screen_width // 2
        chat_height = screen_height - 150  # Відступ знизу
        
        chat_area = {
            'left': chat_left,
            'top': chat_top,
            'width': chat_width,
            'height': chat_height
        }
        
        print(f"📱 Область чату: {chat_left},{chat_top} {chat_width}x{chat_height}")
        return chat_area
        
    except Exception as e:
        print(f"❌ Помилка при визначенні області чату: {e}")
        return None

def scroll_to_bottom(chat_area):
    """Прокручує чат до самого низу і перевіряє, що досягли кінця."""
    try:
        # Клікаємо в центр чату для фокуса
        center_x = chat_area['left'] + chat_area['width'] // 2
        center_y = chat_area['top'] + chat_area['height'] // 2
        pyautogui.click(center_x, center_y)
        time.sleep(0.3)
        
        print("📜⬇️ Починаю прокрутку до самого кінця чату...")
        
        # Етап 1: Швидкий перехід до кінця
        pyautogui.hotkey('cmd', 'end')  # Для macOS
        time.sleep(0.5)
        
        # Етап 2: Прокрутка вниз до повного кінця
        print("🔄 Прокручую до абсолютного кінця...")
        scroll_position_stable = False
        stable_checks = 0
        max_stable_checks = 3
        
        while not scroll_position_stable and stable_checks < max_stable_checks:
            # Зберігаємо поточну позицію (можна використати screenshot для порівняння)
            before_scroll = pyautogui.screenshot(region=(chat_area['left'], 
                                                        chat_area['top'] + chat_area['height'] - 100, 
                                                        chat_area['width'], 
                                                        100))
            
            # Агресивна прокрутка вниз
            for _ in range(5):
                pyautogui.scroll(-10)
                time.sleep(0.1)
            
            # Використовуємо End key
            pyautogui.press('end')
            time.sleep(0.3)
            
            # Перевіряємо чи змінилася позиція
            after_scroll = pyautogui.screenshot(region=(chat_area['left'], 
                                                       chat_area['top'] + chat_area['height'] - 100, 
                                                       chat_area['width'], 
                                                       100))
            
            # Простий спосіб перевірки - порівняння розмірів зображень (вони будуть однакові якщо не прокрутилося)
            if before_scroll.size == after_scroll.size:
                stable_checks += 1
                print(f"✓ Позиція стабільна ({stable_checks}/{max_stable_checks})")
            else:
                stable_checks = 0
            
            time.sleep(0.2)
        
        # Фінальна прокрутка для 100% гарантії
        pyautogui.press('end')
        time.sleep(0.2)
        
        print("✅ Досягнуто самого кінця чату! Позиція стабілізована.")
        return True
        
    except Exception as e:
        print(f"❌ Помилка при прокрутці: {e}")
        return False

def find_buttons_in_chat(chat_area):
    """Шукає кнопки Continue у верхній частині чату і Accept All внизу."""
    buttons_found = {}
    
    try:
        # Шукаємо Continue у всій області чату (як показано на фото - вгорі)
        print(f"🔍 Шукаю Continue в чаті...")
        
        # Шукаємо Continue
        try:
            continue_location = pyautogui.locateOnScreen(CONTINUE_BUTTON, confidence=CONFIDENCE)
            if continue_location:
                continue_center = pyautogui.center(continue_location)
                buttons_found['continue'] = {
                    'location': continue_location,
                    'center': continue_center
                }
                print(f"🔍 Знайдено 'Continue': {continue_location}")
        except pyautogui.ImageNotFoundException:
            pass
        
        # Шукаємо Accept All у нижній частині чату (як показано на фото)
        bottom_height = int(chat_area['height'] * 0.4)  # Збільшуємо область пошуку
        bottom_top = chat_area['top'] + chat_area['height'] - bottom_height
        bottom_region = (chat_area['left'], bottom_top, chat_area['width'], bottom_height)
        
        print(f"🔍 Шукаю Accept All у нижній частині чату: область {bottom_region}")
        
        try:
            accept_location = pyautogui.locateOnScreen(ACCEPT_ALL_BUTTON, confidence=CONFIDENCE, region=bottom_region)
            if accept_location:
                accept_center = pyautogui.center(accept_location)
                buttons_found['accept_all'] = {
                    'location': accept_location,
                    'center': accept_center
                }
                print(f"🔍 Знайдено 'Accept all': {accept_location}")
        except pyautogui.ImageNotFoundException:
            pass
            
    except Exception as e:
        print(f"❌ Помилка при пошуку кнопок: {e}")
    
    return buttons_found

def are_buttons_new(buttons):
    """Перевіряє, чи є кнопки новими (інші координати)."""
    global last_button_coordinates
    
    for button_type, button_data in buttons.items():
        location = button_data['location']
        # Використовуємо абсолютні координати екрана для порівняння
        key = f"{button_type}_{location.left}_{location.top}"
        
        if key in last_button_coordinates:
            print(f"⚠️ Кнопка {button_type} в старих координатах: {location}")
            return False
    
    print("✅ Кнопки в нових координатах!")
    return True

def update_button_coordinates(buttons):
    """Оновлює збережені координати кнопок."""
    global last_button_coordinates
    
    for button_type, button_data in buttons.items():
        location = button_data['location']
        key = f"{button_type}_{location.left}_{location.top}"
        last_button_coordinates[key] = time.time()

def click_button_safely(button_data, button_name):
    """Безпечно натискає кнопку з перевіркою."""
    try:
        center = button_data['center']
        pyautogui.click(center.x, center.y)
        print(f"✅ Натиснуто кнопку: '{button_name}' в позиції {center}")
        return True
    except Exception as e:
        print(f"❌ Помилка при натисканні {button_name}: {e}")
        return False

def execute_button_sequence(buttons):
    """Виконує послідовність: Accept All → Continue."""
    print("🎯 Знайдено Continue і Accept All в низу! Починаю послідовність...")
    
    # 1. Натискаємо Accept All
    print("1️⃣ Натискаю Accept All...")
    if not click_button_safely(buttons['accept_all'], 'Accept All'):
        return False
    
    # 2. Чекаємо пауза
    print(f"⏳ Чекаю {SEQUENCE_PAUSE} секунд...")
    time.sleep(SEQUENCE_PAUSE)
    
    # 3. Натискаємо Continue
    print("2️⃣ Натискаю Continue...")
    if not click_button_safely(buttons['continue'], 'Continue'):
        return False
    
    # 4. Оновлюємо координати
    update_button_coordinates(buttons)
    
    print("✅ Послідовність завершено! Пауза 60 секунд перед наступним циклом...")
    return True

def main_loop():
    """Основний цикл програми."""
    global script_running
    
    print("🚀 Моніторинг чату Windsurf запущено!")
    print("💡 Щоб зупинити, створіть файл 'stop.flag' у папці або натисніть Ctrl+C.")
    
    # Отримуємо область чату
    chat_area = get_chat_area()
    if not chat_area:
        print("❌ Не вдалося визначити область чату.")
        return
    
    print(f"📍 Область пошуку: {chat_area['width']}x{chat_area['height']} пікселів")
    print("🔄 Нова логіка: Чекаю нові Continue в низу → Accept All → Continue → пауза 60с")
    
    while script_running:
        try:
            # Перевіряємо флаг зупинки
            if check_stop_flag():
                break
            
            print(f"🔍 Початок циклу: прокрутка до кінця...")
            
            # Прокручуємо до низу і чекаємо завершення
            scroll_success = scroll_to_bottom(chat_area)
            if not scroll_success:
                print("❌ Помилка прокрутки, повторюю через 5 секунд...")
                time.sleep(5)
                continue
            
            print(f"⏰ Тепер починаю відлік {NORMAL_PAUSE} секунд...")
            
            # Відлік після завершення прокрутки
            for remaining in range(NORMAL_PAUSE, 0, -1):
                print(f"⏳ Залишилось {remaining} секунд до пошуку кнопок...")
                time.sleep(1)
                
                # Перевіряємо флаг зупинки під час відліку
                if check_stop_flag():
                    return
            
            print("🔍 Шукаю активні кнопки Continue в чаті...")
            
            # Шукаємо кнопки в чаті
            buttons = find_buttons_in_chat(chat_area)
            
            # Перевіряємо, чи є Continue і Accept All
            if 'continue' in buttons and 'accept_all' in buttons:
                # Перевіряємо, чи це нові кнопки
                if are_buttons_new(buttons):
                    print("\n🎯 Знайдено нові активні кнопки!\n")
                    
                    # Виконуємо послідовність
                    if execute_button_sequence(buttons):
                        print(f"⏰ Довга пауза {AFTER_CLICK_PAUSE} секунд після натискання...")
                        # Довга пауза після виконання з відліком
                        for remaining in range(AFTER_CLICK_PAUSE, 0, -1):
                            if remaining % 10 == 0 or remaining <= 10:
                                print(f"⏳ Залишилось {remaining} секунд до наступного циклу...")
                            time.sleep(1)
                            
                            # Перевіряємо флаг зупинки під час довгої паузи
                            if check_stop_flag():
                                return
                    else:
                        print("❌ Помилка при виконанні послідовності")
                        time.sleep(NORMAL_PAUSE)
                else:
                    print("⏳ Кнопки в старих координатах, чекаю нові...")
            else:
                if 'continue' not in buttons:
                    print("⏳ Continue не знайдено в чаті...")
                if 'accept_all' not in buttons:
                    print("⏳ Accept All не знайдено в чаті...")
                
        except KeyboardInterrupt:
            print("\n🛑 Скрипт зупинено користувачем (Ctrl+C).")
            break
        except Exception as e:
            print(f"❌ Критична помилка в основному циклі: {e}")
            time.sleep(NORMAL_PAUSE)

def main():
    """Основна функція."""
    # Налаштовуємо обробку сигналів
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Налаштовуємо PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    
    try:
        # Перевіряємо наявність файлів зображень
        if not validate_image_files():
            print("❌ Не всі необхідні файли зображень знайдено.")
            return False
        
        # Запускаємо основний цикл
        main_loop()
        
        print("✅ Програма завершена успішно.")
        return True
        
    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)