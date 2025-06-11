#!/usr/bin/env python3
"""
VentAI Enterprise Autoclicker v2 - з реальною мишкою
Логіка:
1. Кожні 20 секунд скролінг до самого низу чату
2. Перевірка кнопки Continue внизу
3. Якщо Continue є - натискаємо Accept All + Continue
4. Якщо Continue немає - запам'ятовуємо картинку
5. Якщо 3 підряд однакові картинки - активуємо VENTAI ENTERPRISE
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

# ===== НАЛАШТУВАННЯ =====
CONFIDENCE = 0.8  # Підвищена точність
SCROLL_INTERVAL = 20  # Кожні 20 секунд
SEQUENCE_PAUSE = 5    # Більша пауза між кліками
VERBOSE_LOGGING = True

# Параметри для детекції змін
UNCHANGED_THRESHOLD = 3  # 3 однакові картинки підряд
ACTIVATION_COMMAND = "VENTAI ENTERPRISE ACTIVATE"

# Глобальні змінні
script_running = True
unchanged_count = 0
last_screen_hash = None

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

def scroll_to_bottom():
    """Скролінг до самого низу чату."""
    try:
        print("📜 Скролінг до низу чату...")
        
        # Отримуємо розміри екрану
        screen_width, screen_height = pyautogui.size()
        
        # ПРАВА ЧАСТИНА ЕКРАНУ - де знаходиться чат
        chat_x = screen_width * 3 // 4  # 3/4 від лівого краю (права сторона)
        chat_y = screen_height // 2  # Центр по висоті
        
        print(f"🖱️ Переміщую мишку в ПРАВУ частину чату ({chat_x}, {chat_y})")
        pyautogui.moveTo(chat_x, chat_y, duration=1.5)  # Повільніше
        time.sleep(1)  # Додаткова пауза
        
        # Кілька скролів вниз для гарантії
        print("📜 Виконую скролінг...")
        for i in range(15):  # Більше скролів
            pyautogui.scroll(-10)  # Більший скрол вниз
            time.sleep(0.3)  # Більша пауза між скролами
            if i % 5 == 0:  # Показуємо прогрес
                print(f"   Скрол {i+1}/15")
        
        print("✅ Скролінг завершено")
        time.sleep(2)  # Довша пауза після скролінгу
        
    except Exception as e:
        print(f"❌ Помилка скролінгу: {e}")

def get_bottom_chat_hash():
    """Отримує хеш нижньої частини чату для детекції змін."""
    try:
        screen_width, screen_height = pyautogui.size()
        
        # ПРАВА частина чату (нижня область)
        bottom_area_x = screen_width // 2  # Від половини екрану (права сторона)
        bottom_area_y = screen_height - 400  # Останні 400 пікселів
        bottom_area_width = screen_width // 2  # Права половина екрану
        bottom_area_height = 300  # Висота області
        
        # Робимо скріншот ПРАВОЇ нижньої частини
        bottom_area = pyautogui.screenshot(region=(bottom_area_x, bottom_area_y, bottom_area_width, bottom_area_height))
        
        # Конвертуємо в сірий для стабільності
        import numpy as np
        gray_array = np.array(bottom_area.convert('L'))
        
        # Робимо хеш
        img_hash = hashlib.md5(gray_array.tobytes()).hexdigest()
        
        return img_hash
    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"⚠️ Помилка при створенні хешу: {e}")
        return None

def check_for_continue_button():
    """Перевіряє наявність кнопки Continue в нижній частині екрану."""
    try:
        screen_width, screen_height = pyautogui.size()
        
        # Шукаємо Continue тільки в ПРАВІЙ нижній частині екрану
        bottom_region = (screen_width // 2, screen_height - 400, screen_width // 2, 400)  # Права половина
        
        continue_location = pyautogui.locateOnScreen(
            CONTINUE_BUTTON, 
            confidence=CONFIDENCE,
            region=bottom_region
        )
        
        if continue_location:
            continue_center = pyautogui.center(continue_location)
            print(f"✅ Знайдено 'Continue' внизу: {continue_location}")
            return {
                'location': continue_location,
                'center': continue_center
            }
        
        return None
        
    except pyautogui.ImageNotFoundException:
        return None
    except Exception as e:
        print(f"❌ Помилка пошуку Continue: {e}")
        return None

def find_accept_all_button():
    """Шукає кнопку Accept All по всьому екрану."""
    try:
        accept_location = pyautogui.locateOnScreen(ACCEPT_ALL_BUTTON, confidence=CONFIDENCE)
        if accept_location:
            accept_center = pyautogui.center(accept_location)
            print(f"✅ Знайдено 'Accept all': {accept_location}")
            return {
                'location': accept_location,
                'center': accept_center
            }
        return None
    except pyautogui.ImageNotFoundException:
        return None
    except Exception as e:
        print(f"❌ Помилка пошуку Accept All: {e}")
        return None

def click_button(button_data, button_name):
    """Клік по кнопці з реальним рухом миші."""
    try:
        center = button_data['center']
        print(f"🖱️ Переміщую мишку до '{button_name}' в {center}")
        
        # ПОВІЛЬНИЙ реальний рух миші
        pyautogui.moveTo(center.x, center.y, duration=1.5)  # Повільніше
        time.sleep(1)  # Довша пауза
        
        # Повільний клік
        print(f"👆 Виконую клік по '{button_name}'...")
        pyautogui.click(duration=0.5)  # Повільніший клік
        print(f"✅ Клік по '{button_name}' виконано")
        
        time.sleep(1)  # Пауза після кліку
        return True
    except Exception as e:
        print(f"❌ Помилка кліку {button_name}: {e}")
        return False

def find_chat_input_field():
    """Знаходить і активує поле вводу чату."""
    try:
        screen_width, screen_height = pyautogui.size()
        
        # Можливі координати поля вводу в ПРАВІЙ частині (де чат)
        possible_inputs = [
            (screen_width * 3 // 4, screen_height - 100),     # 3/4 від лівого краю (права сторона)
            (screen_width * 3 // 4, screen_height - 150),     # 3/4 від лівого краю (права сторона)
            (screen_width * 5 // 6, screen_height - 80),      # 5/6 від лівого краю (права сторона)
            (screen_width * 2 // 3, screen_height - 120),     # 2/3 від лівого краю (права сторона)
        ]
        
        for x, y in possible_inputs:
            try:
                print(f"🔍 Перевіряю поле вводу в {x}, {y}")
                
                # ПОВІЛЬНИЙ рух миші
                pyautogui.moveTo(x, y, duration=1.5)
                time.sleep(1)
                
                # Повільний клік
                pyautogui.click(duration=0.5)
                time.sleep(2)  # Довша пауза для активації
                
                # Тестуємо поле повільно
                print("✏️ Тестую поле вводу...")
                pyautogui.typewrite("GO ", interval=0.2)  # Повільніше набирання
                time.sleep(1)
                pyautogui.hotkey('cmd', 'a')  # macOS: cmd+a
                time.sleep(0.5)
                pyautogui.press('backspace')
                time.sleep(0.5)
                
                print(f"✅ Знайдено активне поле вводу в {x}, {y}")
                return (x, y)
            except Exception as inner_e:
                print(f"⚠️ Поле в {x}, {y} не працює: {inner_e}")
                continue
        
        print("❌ Не вдалося знайти поле вводу")
        return None
    except Exception as e:
        print(f"❌ Помилка пошуку поля вводу: {e}")
        return None

def activate_ventai_enterprise():
    """Активує VentAI Enterprise через поле вводу."""
    try:
        print("\n🚀 АКТИВАЦІЯ VENTAI ENTERPRISE")
        print("===============================")
        
        # 1. Натискаємо Escape
        print("1️⃣ Натискаю Escape...")
        pyautogui.press('escape')
        time.sleep(1)
        
        # 2. Шукаємо і натискаємо Accept All
        print("2️⃣ Шукаю Accept All...")
        accept_button = find_accept_all_button()
        if accept_button:
            if click_button(accept_button, 'Accept All'):
                time.sleep(2)
            else:
                print("⚠️ Не вдалося натиснути Accept All")
        else:
            print("⚠️ Accept All не знайдено")
        
        # 3. Знаходимо поле вводу
        print("3️⃣ Шукаю поле вводу чату...")
        chat_input = find_chat_input_field()
        
        if chat_input:
            x, y = chat_input
            
            # 4. Активуємо поле вводу
            print("4️⃣ Активую поле вводу...")
            pyautogui.moveTo(x, y, duration=1.5)  # Повільніше
            time.sleep(1)
            pyautogui.click(duration=0.5)  # Повільніший клік
            time.sleep(2)  # Довша пауза
            
            # 5. Очищаємо і вводимо команду
            print("5️⃣ Вводжу команду активації...")
            pyautogui.hotkey('cmd', 'a')  # macOS: cmd+a для виділення всього
            time.sleep(0.5)
            pyautogui.press('backspace')
            time.sleep(1)  # Пауза після очищення
            
            # Вводимо команду ПОВІЛЬНО
            print(f"✏️ Набираю: {ACTIVATION_COMMAND}")
            pyautogui.typewrite(ACTIVATION_COMMAND, interval=0.1)  # Повільніше набирання
            time.sleep(2)  # Пауза після введення
            
            # 6. Відправляємо командою CMD+ENTER
            print("6️⃣ Відправляю команду (CMD+ENTER)...")
            pyautogui.hotkey('cmd', 'enter')  # macOS: cmd+enter
            time.sleep(1)
            
            print("✅ VENTAI ENTERPRISE АКТИВОВАНО!")
            print(f"📝 Команда: {ACTIVATION_COMMAND}")
            return True
        else:
            print("❌ Не вдалося знайти поле вводу")
            return False
            
    except Exception as e:
        print(f"❌ Помилка активації: {e}")
        return False

def execute_continue_sequence():
    """Виконує послідовність Accept All + Continue."""
    try:
        print("\n⚡ ПОСЛІДОВНІСТЬ: Accept All + Continue")
        print("=====================================")
        
        # 1. Шукаємо Accept All
        print("1️⃣ Шукаю Accept All...")
        accept_button = find_accept_all_button()
        if not accept_button:
            print("❌ Accept All не знайдено")
            return False
        
        # 2. Клік Accept All
        print("2️⃣ Клік Accept All...")
        if not click_button(accept_button, 'Accept All'):
            return False
        
        # 3. Пауза
        print(f"⏳ Пауза {SEQUENCE_PAUSE}с...")
        time.sleep(SEQUENCE_PAUSE)
        
        # 4. Шукаємо Continue знову
        print("4️⃣ Шукаю Continue після Accept All...")
        time.sleep(1)  # Додаткова пауза
        continue_button = check_for_continue_button()
        if not continue_button:
            print("⚠️ Continue зник після Accept All (це нормально)")
            return True  # Це нормально
        
        # 5. Клік Continue
        print("5️⃣ Клік Continue...")
        if not click_button(continue_button, 'Continue'):
            return False
        
        print("✅ Послідовність виконано успішно!")
        return True
        
    except Exception as e:
        print(f"❌ Помилка виконання послідовності: {e}")
        return False

def check_screen_changes():
    """Перевіряє зміни на екрані і веде лічильник однакових картинок."""
    global last_screen_hash, unchanged_count
    
    current_hash = get_bottom_chat_hash()
    if current_hash is None:
        return False
    
    if last_screen_hash is None:
        last_screen_hash = current_hash
        unchanged_count = 1
        print(f"📸 Перша картинка збережена")
        return False
    
    if current_hash == last_screen_hash:
        unchanged_count += 1
        print(f"🔄 Картинка #{unchanged_count} - БЕЗ ЗМІН")
        
        if unchanged_count >= UNCHANGED_THRESHOLD:
            print(f"🎯 ТРИГЕР: {UNCHANGED_THRESHOLD} однакові картинки підряд!")
            return True
    else:
        unchanged_count = 1
        last_screen_hash = current_hash
        print(f"✨ Нова картинка виявлена, лічильник скинуто")
    
    return False

def main_loop():
    """Основний цикл скрипта."""
    global script_running, unchanged_count
    
    print("🚀 VENTAI ENTERPRISE v2 запущено!")
    print("🖱️ Реальна мишка")
    print("📜 Скролінг кожні 20 секунд")
    print("🎯 Автоактивація після 3 однакових картинок")
    print("💡 Для зупинки: Ctrl+C або створіть stop.flag\n")
    
    cycle = 0
    
    while script_running:
        try:
            cycle += 1
            print(f"\n🔍 Цикл #{cycle}")
            print("=" * 40)
            
            if check_stop_flag():
                break
            
            # 1. Скролінг до низу
            scroll_to_bottom()
            
            # 2. Перевірка кнопки Continue
            print("🔍 Перевіряю наявність Continue...")
            continue_button = check_for_continue_button()
            
            if continue_button:
                print("✅ Continue знайдено!")
                # Скидаємо лічильник при знаходженні Continue
                unchanged_count = 0
                last_screen_hash = None
                
                # Виконуємо послідовність
                if execute_continue_sequence():
                    print("⏰ Пауза 30 секунд після виконання послідовності...")
                    time.sleep(30)
                else:
                    time.sleep(10)
            else:
                print("❌ Continue не знайдено")
                
                # 3. Перевіряємо зміни і лічимо однакові картинки
                print("📸 Перевіряю зміни на екрані...")
                should_activate = check_screen_changes()
                
                if should_activate:
                    print("🎯 УМОВА АКТИВАЦІЇ ВИКОНАНА!")
                    if activate_ventai_enterprise():
                        # Скидаємо лічильник після активації
                        unchanged_count = 0
                        last_screen_hash = None
                        print("⏰ Пауза 60 секунд після активації...")
                        time.sleep(60)
                    else:
                        time.sleep(10)
                else:
                    print(f"⏳ Чекаю наступного циклу ({SCROLL_INTERVAL}с)...")
                    time.sleep(SCROLL_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n🛑 VentAI Enterprise зупинено (Ctrl+C)")
            break
        except Exception as e:
            print(f"❌ Помилка: {e}")
            time.sleep(10)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Налаштування PyAutoGUI для macOS
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5  # Більша глобальна пауза між командами
    
    try:
        if not validate_image_files():
            return False
        
        print("🎯 VENTAI ENTERPRISE v2 MODE:")
        print("• Реальна мишка")
        print("• Скролінг кожні 20с")
        print("• Детекція Continue")
        print("• Лічильник змін")
        print("• macOS оптимізація\n")
        
        main_loop()
        
        print("✅ VentAI Enterprise завершено.")
        return True
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
