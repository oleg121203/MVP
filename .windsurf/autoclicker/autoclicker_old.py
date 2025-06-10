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
SCROLL_INTERVAL = 5      # Як часто перевіряти чат (звичайна пауза)
SCROLL_INTERVAL_AFTER_CLICK = 30  # Пауза після натискання кнопок
CLICK_DELAY = 2         # Затримка між натисканням кнопок
VERBOSE_LOGGING = True  # Показувати детальні повідомлення
CHAT_SCROLL_AMOUNT = 3  # Кількість скролів в чаті за раз

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

def scroll_in_chat(chat_area):
    """Прокручує в області чату Windsurf."""
    try:
        # Переміщуємо курсор в центр області чату
        center_x = chat_area['left'] + chat_area['width'] // 2
        center_y = chat_area['top'] + chat_area['height'] // 2
        
        pyautogui.moveTo(center_x, center_y)
        
        # Прокручуємо вниз в області чату
        for _ in range(CHAT_SCROLL_AMOUNT):
            pyautogui.scroll(-3)  # Негативне значення для прокрутки вниз
            time.sleep(0.1)
        
        if VERBOSE_LOGGING:
            print("📜", end="", flush=True)  # Показуємо, що прокручуємо
            
    except Exception as e:
        print(f"❌ Помилка при прокрутці чату: {e}")

def check_for_buttons_in_chat(chat_area):
    """Перевіряє наявність кнопок в області чату."""
    buttons_found = []
    
    try:
        # Шукаємо кнопки тільки в області чату
        region = (chat_area['left'], chat_area['top'], chat_area['width'], chat_area['height'])
        
        # Перевіряємо кнопку "Accept all"
        try:
            accept_location = pyautogui.locateOnScreen(ACCEPT_ALL_BUTTON, confidence=CONFIDENCE, region=region)
            if accept_location:
                buttons_found.append(('accept_all', accept_location))
                if VERBOSE_LOGGING:
                    print(f"\n🔍 Знайдено 'Accept all' в позиції: {accept_location}")
        except pyautogui.ImageNotFoundException:
            pass
        
        # Перевіряємо кнопку "Continue"
        try:
            continue_location = pyautogui.locateOnScreen(CONTINUE_BUTTON, confidence=CONFIDENCE, region=region)
            if continue_location:
                buttons_found.append(('continue', continue_location))
                if VERBOSE_LOGGING:
                    print(f"\n🔍 Знайдено 'Continue' в позиції: {continue_location}")
        except pyautogui.ImageNotFoundException:
            pass
            
    except Exception as e:
        print(f"❌ Помилка при пошуку кнопок в чаті: {e}")
    
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

def wait_for_buttons_in_chat(chat_area, scroll_interval=SCROLL_INTERVAL):
    """Чекає появи кнопок в чаті, прокручуючи його."""
    print(f"🔍 Шукаю кнопки в чаті Windsurf (пауза: {scroll_interval}с)...")
    scroll_counter = 0
    
    while True:
        # Перевіряємо сигнал зупинки
        if check_for_stop_signal():
            return None
            
        # Перевіряємо наявність кнопок
        buttons_found = check_for_buttons_in_chat(chat_area)
        
        if buttons_found:
            print(f"\n🎯 Знайдено {len(buttons_found)} кнопок в чаті!")
            return buttons_found
        
        # Прокручуємо чат
        scroll_in_chat(chat_area)
        scroll_counter += 1
        
        # Показуємо прогрес кожні 10 скролів
        if scroll_counter % 10 == 0:
            print(f"\n⏳ Прокручено {scroll_counter} разів, продовжую пошук...")
        
        time.sleep(scroll_interval)

def main_workflow():
    """Основний цикл робочого процесу для чату Windsurf."""
    
    # Перевіряємо існування файлів зображень
    if not os.path.exists(ACCEPT_ALL_BUTTON):
        print(f"❌ Помилка: Файл зображення не знайдено: {ACCEPT_ALL_BUTTON}")
        return
    if not os.path.exists(CONTINUE_BUTTON):
        print(f"❌ Помилка: Файл зображення не знайдено: {CONTINUE_BUTTON}")
        return
        
    print(f"✅ Файли зображень знайдено:")
    print(f"   - {ACCEPT_ALL_BUTTON}")
    print(f"   - {CONTINUE_BUTTON}")
    
    # Визначаємо область чату Windsurf
    chat_area = find_windsurf_chat_area()
    if not chat_area:
        print("❌ Не вдалося визначити область чату Windsurf")
        return
    
    print("🚀 Моніторинг чату Windsurf запущено!")
    print(f"💡 Щоб зупинити, створіть файл 'stop.flag' у папці або натисніть Ctrl+C.")
    print(f"📍 Область пошуку: {chat_area['width']}x{chat_area['height']} пікселів")
    print("🔄 Логіка: Чекаю Continue → Accept All → Continue → пауза 30с")
    
    # Стан: чекаємо Continue як першу кнопку
    waiting_for_continue = True
    current_scroll_interval = SCROLL_INTERVAL
    
    try:
        while True:
            # Чекаємо появи кнопок в чаті
            buttons_found = wait_for_buttons_in_chat(chat_area, current_scroll_interval)
            
            if buttons_found is None:  # Сигнал зупинки
                break
                
            if buttons_found:
                # Розділяємо кнопки по типах
                accept_all_buttons = [btn for btn in buttons_found if btn[0] == 'accept_all']
                continue_buttons = [btn for btn in buttons_found if btn[0] == 'continue']
                
                if waiting_for_continue:
                    # Чекаємо Continue як першу кнопку
                    if continue_buttons:
                        print("\n🎯 Знайдено Continue! Починаю цикл: Continue → Accept All → Continue")
                        
                        # Натискаємо Continue
                        for _, location in continue_buttons:
                            click_button_at_location(location, "Continue (початок циклу)")
                            time.sleep(CLICK_DELAY)
                        
                        waiting_for_continue = False
                        current_scroll_interval = SCROLL_INTERVAL  # Звичайна пауза для пошуку Accept All
                        print("➡️ Тепер шукаю Accept All...")
                        
                    else:
                        print("⏳ Чекаю появи кнопки Continue...")
                        
                else:
                    # Після натискання Continue шукаємо Accept All
                    if accept_all_buttons:
                        print("\n✅ Знайдено Accept All! Натискаю...")
                        
                        # Натискаємо Accept All
                        for _, location in accept_all_buttons:
                            click_button_at_location(location, "Accept All")
                            time.sleep(CLICK_DELAY)
                        
                        print("➡️ Тепер шукаю Continue для завершення циклу...")
                        
                        # Чекаємо Continue для завершення циклу
                        continue_found = False
                        attempts = 0
                        max_attempts = 20  # Максимум спроб пошуку Continue
                        
                        while not continue_found and attempts < max_attempts:
                            time.sleep(2)  # Короткі паузи при пошуку Continue
                            attempts += 1
                            
                            buttons_check = check_for_buttons_in_chat(chat_area)
                            continue_check = [btn for btn in buttons_check if btn[0] == 'continue']
                            
                            if continue_check:
                                print(f"\n🎯 Знайдено Continue для завершення! (спроба {attempts})")
                                for _, location in continue_check:
                                    click_button_at_location(location, "Continue (завершення циклу)")
                                    time.sleep(CLICK_DELAY)
                                
                                continue_found = True
                                
                                # Повертаємося до очікування нового циклу
                                waiting_for_continue = True
                                current_scroll_interval = SCROLL_INTERVAL_AFTER_CLICK  # 30 секунд пауза
                                
                                print(f"✅ Цикл завершено! Пауза {SCROLL_INTERVAL_AFTER_CLICK} секунд перед наступним циклом...")
                                break
                            else:
                                print(f"⏳ Шукаю Continue... (спроба {attempts}/{max_attempts})")
                                if attempts % 5 == 0:
                                    scroll_in_chat(chat_area)  # Прокручуємо кожні 5 спроб
                        
                        if not continue_found:
                            print("⚠️ Continue не знайдено після Accept All. Повертаюся до очікування нового циклу...")
                            waiting_for_continue = True
                            current_scroll_interval = SCROLL_INTERVAL
                    else:
                        print("⏳ Чекаю появи кнопки Accept All...")

    except KeyboardInterrupt:
        print("\n🛑 Скрипт зупинено користувачем (Ctrl+C).")
    except Exception as e:
        print(f"❌ Критична помилка в основному циклі: {e}")
        import traceback
        print(f"❌ Детальна інформація: {traceback.format_exc()}")

if __name__ == "__main__":
    main_workflow()
    sys.exit(0)
