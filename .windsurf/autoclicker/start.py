#!/usr/bin/env python3

import sys
import subprocess
import importlib.util

# Словник, де ключ - назва пакета для pip, а значення - назва модуля для перевірки
REQUIRED_PACKAGES = {
    'Pillow': 'PIL',
    'opencv-python': 'cv2',
    'PyAutoGUI': 'pyautogui'
}

def check_and_install_packages():
    """
    Перевіряє, чи встановлені необхідні пакети. Якщо ні - встановлює їх.
    """
    print("Перевірка наявності необхідних бібліотек...")
    all_packages_installed = True
    
    for package_name, module_name in REQUIRED_PACKAGES.items():
        # Перевіряємо, чи можна знайти специфікацію модуля. Якщо ні - він не встановлений.
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            all_packages_installed = False
            print(f"🟡 Бібліотека '{package_name}' не знайдена. Спроба встановити...")
            try:
                # Використовуємо той самий інтерпретатор Python для виклику pip
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                print(f"✅ Бібліотеку '{package_name}' успішно встановлено.")
            except subprocess.CalledProcessError:
                print(f"❌ Помилка під час встановлення '{package_name}'.")
                print("Будь ласка, спробуйте встановити її вручну, виконавши команду:")
                print(f"   pip install {package_name}")
                return False
    
    if all_packages_installed:
        print("✅ Усі необхідні бібліотеки вже встановлено.")
        
    return True

def run_main_script():
    """
    Запускає основний скрипт автоматизації.
    """
    import os
    # Отримуємо директорію, де знаходиться поточний скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "autoclicker.py")
    print(f"\n🚀 Запуск основного скрипта: {script_path}")
    try:
        # Запускаємо autoclicker.py як дочірній процес
        subprocess.run([sys.executable, script_path], check=True)
    except FileNotFoundError:
        print(f"❌ Помилка: Основний скрипт '{script_path}' не знайдено.")
        print("Переконайтесь, що 'start.py' та 'autoclicker.py' знаходяться в одній папці.")
    except subprocess.CalledProcessError as e:
        # Ця помилка може виникнути, якщо скрипт завершився з ненульовим кодом,
        # але це не завжди означає проблему (наприклад, зупинка через Ctrl+C).
        print(f"\nℹ️ Скрипт 'autoclicker.py' завершив роботу з кодом виходу {e.returncode}.")

if __name__ == "__main__":
    if check_and_install_packages():
        run_main_script()
    else:
        print("\n🛑 Не вдалося підготувати середовище для запуску. Виправте помилки вище та спробуйте знову.")
        # Затримка, щоб користувач встиг прочитати повідомлення про помилку
        input("Натисніть Enter для виходу...")