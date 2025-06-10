#!/usr/bin/env python3
import pyautogui
import time
import os
import sys

# --- Налаштування ---

# Шляхи до файлів (відносно поточного скрипта)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')

# Зображення кнопок
ACCEPT_ALL_BUTTON = os.path.join(IMAGE_DIR, 'accept_all.png')
CONTINUE_BUTTON = os.path.join(IMAGE_DIR, 'continue.png')

# Файл-прапор для зупинки
STOP_FLAG_FILE = os.path.join(BASE_DIR, 'stop.flag')

# Рівень впевненості для розпізнавання зображень (від 0.0 до 1.0)
CONFIDENCE = 0.6  # Знижено з 0.85 для кращої сумісності

# Інтервали (в секундах)
SCROLL_INTERVAL = 10     # Як часто перевіряти чат (звичайна пауза)
SCROLL_INTERVAL_AFTER_CLICK = 60  # Пауза після натискання кнопок
CLICK_DELAY = 3         # Затримка між натисканням кнопок
VERBOSE_LOGGING = True  # Показувати детальні повідомлення
CHAT_SCROLL_AMOUNT = 10  # Кількість скролів в чаті за раз до самого низу

# --- Функції ---

def check_for_stop_signal():
    """Перевіряє, чи існує файл 'stop.flag' для зупинки скрипта."""
    if os.path.exists(STOP_FLAG_FILE):
        print("\n🟡 Отримано сигнал зупинки через файл 'stop.flag'. Завершую роботу...")
        try:
            os.remove(STOP_FLAG_FILE) # Видаляємо прапор, щоб не спрацював наступного разу
            print("ℹ️ Файл 'stop.flag' видалено.")
        except OSError as e:
            print(f"⚠️ Не вдалося видалити 'stop.flag': {e}")
        return True
    return False

def find_windsurf_chat_area():
    """Знаходить область чату Windsurf на екрані."""
    try:
        # Отримуємо розмір екрану
        screen_width, screen_height = pyautogui.size()
        
        # Припускаємо, що чат Windsurf знаходиться в правій частині екрану
        # Ці координати можуть потребувати налаштування залежно від вашого інтерфейсу
        chat_area = {
            'left': int(screen_width * 0.5),    # Права половина екрану
            'top': int(screen_height * 0.1),    # Верхня частина
            'width': int(screen_width * 0.5),   # 50% ширини екрану
            'height': int(screen_height * 0.8)  # 80% висоти екрану
        }
        
        print(f"📱 Область чату: {chat_area['left']},{chat_area['top']} {chat_area['width']}x{chat_area['height']}")
        return chat_area
    except Exception as e:
        print(f"❌ Помилка при визначенні області чату: {e}")
        return None

def scroll_to_bottom_of_chat(chat_area):
    """Прокручує чат до самого низу для пошуку нових активних кнопок."""
    try:
        # Переміщуємо курсор в центр області чату
        center_x = chat_area['left'] + chat_area['width'] // 2
        center_y = chat_area['top'] + chat_area['height'] // 2
        
        pyautogui.moveTo(center_x, center_y)
        
        # Прокручуємо до самого низу
        for _ in range(CHAT_SCROLL_AMOUNT):
            pyautogui.scroll(-5)  # Великі скролі вниз
            time.sleep(0.1)
        
        if VERBOSE_LOGGING:
            print("📜⬇️ Прокрутка до низу чату", end="", flush=True)
            
    except Exception as e:
        print(f"❌ Помилка при прокрутці до низу чату: {e}")

def check_for_active_buttons_at_bottom(chat_area):
    """Перевіряє наявність активних кнопок в самому низу чату."""
    buttons_found = []
    
    try:
        # Шукаємо кнопки тільки в нижній частині чату (останні 20% висоти)
        bottom_height = int(chat_area['height'] * 0.2)  # Нижні 20%
        bottom_top = chat_area['top'] + chat_area['height'] - bottom_height
        
        region = (chat_area['left'], bottom_top, chat_area['width'], bottom_height)
        
        if VERBOSE_LOGGING:
            print(f"\n🔍 Шукаю активні кнопки в низу чату: область {region}")
        
        # Перевіряємо кнопку "Accept all"
        try:
            accept_location = pyautogui.locateOnScreen(ACCEPT_ALL_BUTTON, confidence=CONFIDENCE, region=region)
            if accept_location:
                buttons_found.append(('accept_all', accept_location))
                if VERBOSE_LOGGING:
                    print(f"🔍 Знайдено активну 'Accept all' в низу: {accept_location}")
        except pyautogui.ImageNotFoundException:
            pass
        
        # Перевіряємо кнопку "Continue"
        try:
            continue_location = pyautogui.locateOnScreen(CONTINUE_BUTTON, confidence=CONFIDENCE, region=region)
            if continue_location:
                buttons_found.append(('continue', continue_location))
                if VERBOSE_LOGGING:
                    print(f"🔍 Знайдено активну 'Continue' в низу: {continue_location}")
        except pyautogui.ImageNotFoundException:
            pass
            
    except Exception as e:
        print(f"❌ Помилка при пошуку активних кнопок в низу: {e}")
    
    return buttons_found

def click_button_at_location(location, description):
    """Клікає на кнопку за заданою локацією."""
    try:
        button_center = pyautogui.center(location)
        pyautogui.moveTo(button_center)
        time.sleep(0.5)  # Коротка затримка для переміщення
        pyautogui.click()
        print(f"✅ Натиснуто кнопку: '{description}' в позиції {button_center}")
        return True
    except Exception as e:
        print(f"❌ Помилка при кліку на '{description}': {e}")
        return False

def wait_for_continue_at_bottom(chat_area, scroll_interval=SCROLL_INTERVAL):
    """Чекає появи активної кнопки Continue в низу чату."""
    print(f"🔍 Чекаю активну кнопку Continue в низу чату (пауза: {scroll_interval}с)...")
    scroll_counter = 0
    
    while True:
        # Перевіряємо сигнал зупинки
        if check_for_stop_signal():
            return None
            
        # Прокручуємо до низу чату
        scroll_to_bottom_of_chat(chat_area)
        
        # Перевіряємо наявність активних кнопок в низу
        buttons_found = check_for_active_buttons_at_bottom(chat_area)
        
        # Шукаємо Continue
        continue_buttons = [btn for btn in buttons_found if btn[0] == 'continue']
        
        if continue_buttons:
            print(f"\n🎯 Знайдено активну Continue в низу чату!")
            return buttons_found
        
        scroll_counter += 1
        
        # Показуємо прогрес кожні 5 спроб
        if scroll_counter % 5 == 0:
            print(f"\n⏳ Перевірено {scroll_counter} разів, продовжую чекати Continue в низу...")
        
        time.sleep(scroll_interval)

def main_workflow():
    """Основний цикл робочого процесу для чату Windsurf."""
    
    # Перевіряємо існування файлів зображень
    if not os.path.exists(ACCEPT_ALL_BUTTON):
        print(f"❌ Помилка: Файл зображення не знайдено: {ACCEPT_ALL_BUTTON}")
        return 1
    if not os.path.exists(CONTINUE_BUTTON):
        print(f"❌ Помилка: Файл зображення не знайдено: {CONTINUE_BUTTON}")
        return 1
        
    print(f"✅ Файли зображень знайдено:")
    print(f"   - {ACCEPT_ALL_BUTTON}")
    print(f"   - {CONTINUE_BUTTON}")
    
    # Визначаємо область чату Windsurf
    chat_area = find_windsurf_chat_area()
    if not chat_area:
        print("❌ Не вдалося визначити область чату Windsurf")
        return 1
    
    print("🚀 Моніторинг чату Windsurf запущено!")
    print(f"💡 Щоб зупинити, створіть файл 'stop.flag' у папці або натисніть Ctrl+C.")
    print(f"📍 Область пошуку: {chat_area['width']}x{chat_area['height']} пікселів")
    print("🔄 Нова логіка: Чекаю Continue в низу → Accept All → Continue → пауза 60с")
    
    try:
        while True:
            # Чекаємо появи Continue в низу чату
            buttons_found = wait_for_continue_at_bottom(chat_area, SCROLL_INTERVAL)
            
            if buttons_found is None:  # Сигнал зупинки
                break
                
            if buttons_found:
                # Розділяємо кнопки по типах
                accept_all_buttons = [btn for btn in buttons_found if btn[0] == 'accept_all']
                continue_buttons = [btn for btn in buttons_found if btn[0] == 'continue']
                
                if continue_buttons and accept_all_buttons:
                    print("\n🎯 Знайдено Continue і Accept All в низу! Починаю послідовність...")
                    
                    # 1. Спочатку натискаємо Accept All
                    print("1️⃣ Натискаю Accept All...")
                    for _, location in accept_all_buttons:
                        click_button_at_location(location, "Accept All")
                        time.sleep(1)
                    
                    # 2. Чекаємо 3 секунди
                    print(f"⏳ Чекаю {CLICK_DELAY} секунд...")
                    time.sleep(CLICK_DELAY)
                    
                    # 3. Потім натискаємо Continue
                    print("2️⃣ Натискаю Continue...")
                    for _, location in continue_buttons:
                        click_button_at_location(location, "Continue")
                        time.sleep(1)
                    
                    print(f"✅ Послідовність завершено! Пауза {SCROLL_INTERVAL_AFTER_CLICK} секунд перед наступним циклом...")
                    time.sleep(SCROLL_INTERVAL_AFTER_CLICK)
                    
                elif continue_buttons:
                    print("⚠️ Знайдено тільки Continue без Accept All. Чекаю повний набір...")
                else:
                    print("⚠️ Continue не знайдено в низу. Продовжую чекати...")

    except KeyboardInterrupt:
        print("\n🛑 Скрипт зупинено користувачем (Ctrl+C).")
        return 0  # Код успішного завершення
    except Exception as e:
        print(f"❌ Критична помилка в основному циклі: {e}")
        import traceback
        print(f"❌ Детальна інформація: {traceback.format_exc()}")
        return 1  # Код помилки

if __name__ == "__main__":
    exit_code = main_workflow()
    sys.exit(exit_code if exit_code is not None else 0)
