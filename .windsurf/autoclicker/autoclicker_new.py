#!/usr/bin/env python3
"""
Автокликер для чату Windsurf
Автоматично натискає кнопки Accept All та Continue коли AI завершує генерацію
"""

import pyautogui
import time
import os
import sys
import hashlib
from datetime import datetime

# --- Налаштування ---

# Шляхи до файлів
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
ACCEPT_ALL_BUTTON = os.path.join(IMAGE_DIR, 'accept_all.png')
CONTINUE_BUTTON = os.path.join(IMAGE_DIR, 'continue.png')
STOP_FLAG_FILE = os.path.join(BASE_DIR, 'stop.flag')

# Параметри розпізнавання
CONFIDENCE = 0.6

# Інтервали (в секундах)
SCAN_INTERVAL = 10           # Сканування кожні 10 секунд
PAUSE_AFTER_CLICK = 60       # Пауза після натискання кнопок
CLICK_DELAY = 3              # Затримка між Accept All та Continue
SCROLL_AMOUNT = 15           # Кількість скролів до низу

# Налаштування області пошуку
BOTTOM_AREA_PERCENTAGE = 0.15  # Шукаємо в нижніх 15% чату

# Глобальні змінні для відстеження
last_clicked_buttons = set()   # Зберігаємо хеші останніх нажатих кнопок
scan_counter = 0

# --- Допоміжні функції ---

def log_message(message, level="INFO"):
    """Виводить повідомлення з часовою міткою."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def check_stop_signal():
    """Перевіряє сигнал зупинки."""
    if os.path.exists(STOP_FLAG_FILE):
        log_message("Отримано сигнал зупинки через файл 'stop.flag'", "WARN")
        try:
            os.remove(STOP_FLAG_FILE)
            log_message("Файл 'stop.flag' видалено")
        except OSError as e:
            log_message(f"Не вдалося видалити 'stop.flag': {e}", "ERROR")
        return True
    return False

def get_chat_area():
    """Визначає область чату Windsurf."""
    try:
        screen_width, screen_height = pyautogui.size()
        
        # Чат Windsurf зазвичай в правій частині
        chat_area = {
            'left': int(screen_width * 0.5),
            'top': int(screen_height * 0.1),
            'width': int(screen_width * 0.5),
            'height': int(screen_height * 0.8)
        }
        
        log_message(f"Область чату: {chat_area['left']},{chat_area['top']} {chat_area['width']}x{chat_area['height']}")
        return chat_area
    except Exception as e:
        log_message(f"Помилка визначення області чату: {e}", "ERROR")
        return None

def scroll_to_bottom(chat_area):
    """Прокручує чат до самого низу."""
    try:
        # Позиціонуємось в центрі чату
        center_x = chat_area['left'] + chat_area['width'] // 2
        center_y = chat_area['top'] + chat_area['height'] // 2
        
        pyautogui.moveTo(center_x, center_y)
        
        # Агресивне прокручування до низу
        for _ in range(SCROLL_AMOUNT):
            pyautogui.scroll(-10)  # Великі скролі вниз
            time.sleep(0.05)
        
        # Додаткове прокручування клавішами
        pyautogui.press('end')  # До кінця
        time.sleep(0.2)
        
        log_message("Прокрутка до низу завершена")
        
    except Exception as e:
        log_message(f"Помилка прокрутки: {e}", "ERROR")

def get_button_hash(button_type, location):
    """Створює унікальний хеш для кнопки на основі типу та координат."""
    location_str = f"{button_type}_{location.left}_{location.top}_{location.width}_{location.height}"
    return hashlib.md5(location_str.encode()).hexdigest()

def scan_for_new_buttons(chat_area):
    """Шукає нові активні кнопки в самому низу чату."""
    global scan_counter
    scan_counter += 1
    
    try:
        # Визначаємо область самого низу
        bottom_height = int(chat_area['height'] * BOTTOM_AREA_PERCENTAGE)
        bottom_top = chat_area['top'] + chat_area['height'] - bottom_height
        search_region = (chat_area['left'], bottom_top, chat_area['width'], bottom_height)
        
        log_message(f"Сканування #{scan_counter}: область {search_region}")
        
        new_buttons = []
        
        # Шукаємо Accept All
        try:
            accept_locations = list(pyautogui.locateAllOnScreen(
                ACCEPT_ALL_BUTTON, 
                confidence=CONFIDENCE, 
                region=search_region
            ))
            
            for location in accept_locations:
                button_hash = get_button_hash('accept_all', location)
                if button_hash not in last_clicked_buttons:
                    new_buttons.append(('accept_all', location, button_hash))
                    log_message(f"Нова кнопка Accept All: {location}")
                
        except pyautogui.ImageNotFoundException:
            pass
        
        # Шукаємо Continue
        try:
            continue_locations = list(pyautogui.locateAllOnScreen(
                CONTINUE_BUTTON, 
                confidence=CONFIDENCE, 
                region=search_region
            ))
            
            for location in continue_locations:
                button_hash = get_button_hash('continue', location)
                if button_hash not in last_clicked_buttons:
                    new_buttons.append(('continue', location, button_hash))
                    log_message(f"Нова кнопка Continue: {location}")
                
        except pyautogui.ImageNotFoundException:
            pass
        
        return new_buttons
        
    except Exception as e:
        log_message(f"Помилка сканування кнопок: {e}", "ERROR")
        return []

def click_button(button_type, location, button_hash):
    """Натискає кнопку та запам'ятовує її."""
    try:
        center = pyautogui.center(location)
        pyautogui.moveTo(center)
        time.sleep(0.3)
        pyautogui.click()
        
        # Запам'ятовуємо, що натиснули цю кнопку
        last_clicked_buttons.add(button_hash)
        
        log_message(f"Натиснуто {button_type} в позиції {center}")
        return True
        
    except Exception as e:
        log_message(f"Помилка натискання {button_type}: {e}", "ERROR")
        return False

def execute_button_sequence(new_buttons):
    """Виконує послідовність натискання кнопок."""
    # Розділяємо кнопки по типах
    accept_buttons = [(btn[1], btn[2]) for btn in new_buttons if btn[0] == 'accept_all']
    continue_buttons = [(btn[1], btn[2]) for btn in new_buttons if btn[0] == 'continue']
    
    if not continue_buttons:
        log_message("Немає нових кнопок Continue - чекаємо")
        return False
    
    if not accept_buttons:
        log_message("Немає нових кнопок Accept All - чекаємо")
        return False
    
    log_message("🎯 Знайдено нові кнопки! Починаю послідовність...")
    
    # 1. Натискаємо Accept All
    log_message("1️⃣ Натискаю Accept All...")
    for location, button_hash in accept_buttons:
        if click_button('Accept All', location, button_hash):
            time.sleep(0.5)  # Коротка пауза між кнопками одного типу
    
    # 2. Чекаємо
    log_message(f"⏳ Чекаю {CLICK_DELAY} секунд...")
    time.sleep(CLICK_DELAY)
    
    # 3. Натискаємо Continue
    log_message("2️⃣ Натискаю Continue...")
    for location, button_hash in continue_buttons:
        if click_button('Continue', location, button_hash):
            time.sleep(0.5)
    
    log_message(f"✅ Послідовність завершено! Пауза {PAUSE_AFTER_CLICK} секунд")
    return True

def cleanup_old_button_history():
    """Очищає історію старих кнопок, щоб не переповнювати пам'ять."""
    global last_clicked_buttons
    
    # Кожні 50 сканувань очищаємо історію (залишаємо тільки останні 20 записів)
    if scan_counter % 50 == 0 and len(last_clicked_buttons) > 20:
        old_buttons = list(last_clicked_buttons)
        last_clicked_buttons = set(old_buttons[-20:])  # Залишаємо останні 20
        log_message(f"Очищено історію кнопок: залишено {len(last_clicked_buttons)} записів")

# --- Основна функція ---

def main():
    """Основний цикл роботи автокликера."""
    
    # Перевірка файлів зображень
    if not os.path.exists(ACCEPT_ALL_BUTTON):
        log_message(f"Файл не знайдено: {ACCEPT_ALL_BUTTON}", "ERROR")
        return 1
        
    if not os.path.exists(CONTINUE_BUTTON):
        log_message(f"Файл не знайдено: {CONTINUE_BUTTON}", "ERROR")
        return 1
    
    log_message(f"✅ Файли зображень знайдено")
    log_message(f"   - {ACCEPT_ALL_BUTTON}")
    log_message(f"   - {CONTINUE_BUTTON}")
    
    # Отримуємо область чату
    chat_area = get_chat_area()
    if not chat_area:
        log_message("Не вдалося визначити область чату", "ERROR")
        return 1
    
    log_message("🚀 Автокликер Windsurf запущено!")
    log_message(f"💡 Для зупинки створіть файл 'stop.flag' або натисніть Ctrl+C")
    log_message(f"📍 Область пошуку: {chat_area['width']}x{chat_area['height']} пікселів")
    log_message(f"🔄 Логіка: Чекаю нові Continue + Accept All → натискаю → пауза {PAUSE_AFTER_CLICK}с")
    log_message(f"⏱️ Сканування кожні {SCAN_INTERVAL} секунд")
    
    try:
        while True:
            # Перевіряємо сигнал зупинки
            if check_stop_signal():
                break
            
            # Прокручуємо до низу
            scroll_to_bottom(chat_area)
            
            # Шукаємо нові кнопки
            new_buttons = scan_for_new_buttons(chat_area)
            
            if new_buttons:
                # Виконуємо послідовність натискання
                if execute_button_sequence(new_buttons):
                    # Після успішного натискання чекаємо довше
                    time.sleep(PAUSE_AFTER_CLICK)
                else:
                    # Якщо не вдалося натиснути, чекаємо звичайний інтервал
                    time.sleep(SCAN_INTERVAL)
            else:
                # Нових кнопок немає, чекаємо звичайний інтервал
                if scan_counter % 5 == 0:
                    log_message(f"⏳ Сканування #{scan_counter}: нових кнопок не знайдено")
                time.sleep(SCAN_INTERVAL)
            
            # Періодично очищаємо історію
            cleanup_old_button_history()
                
    except KeyboardInterrupt:
        log_message("Зупинено користувачем (Ctrl+C)", "WARN")
        return 0
    except Exception as e:
        log_message(f"Критична помилка: {e}", "ERROR")
        import traceback
        log_message(f"Детальна інформація: {traceback.format_exc()}", "ERROR")
        return 1
    
    log_message("Автокликер завершив роботу")
    return 0

if __name__ == "__main__":
    sys.exit(main())
