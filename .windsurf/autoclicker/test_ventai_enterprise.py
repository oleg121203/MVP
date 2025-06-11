#!/usr/bin/env python3
"""
Тестовий скрипт для VentAI Enterprise Autoclicker
Демонструє активацію без очікування 60 секунд
"""

import sys
from pathlib import Path

# Додаємо шлях до основного скрипта
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

# Імпортуємо функції з основного скрипта
from autoclicker_ventai_enterprise import (
    validate_image_files,
    find_chat_input_field,
    activate_ventai_enterprise,
    get_screen_hash
)

def test_image_validation():
    """Тестує валідацію файлів зображень."""
    print("🧪 Тест 1: Валідація зображень")
    result = validate_image_files()
    print(f"   Результат: {'✅ ПРОЙДЕНО' if result else '❌ ПРОВАЛЕНО'}")
    return result

def test_screen_hash():
    """Тестує функцію хешування екрану."""
    print("\n🧪 Тест 2: Хешування екрану")
    try:
        hash1 = get_screen_hash()
        hash2 = get_screen_hash()
        
        if hash1 and hash2:
            print(f"   Хеш 1: {hash1[:8]}...")
            print(f"   Хеш 2: {hash2[:8]}...")
            print(f"   Результат: {'✅ ПРОЙДЕНО' if hash1 == hash2 else '❌ ПРОВАЛЕНО'}")
            return True
        else:
            print("   Результат: ❌ ПРОВАЛЕНО (не вдалося створити хеш)")
            return False
    except Exception as e:
        print(f"   Результат: ❌ ПРОВАЛЕНО ({e})")
        return False

def test_chat_input_detection():
    """Тестує детекцію поля вводу чату."""
    print("\n🧪 Тест 3: Детекція поля чату")
    try:
        chat_input = find_chat_input_field()
        if chat_input:
            x, y = chat_input
            print(f"   Знайдено поле в: ({x}, {y})")
            print("   Результат: ✅ ПРОЙДЕНО")
            return True
        else:
            print("   Результат: ⚠️ НЕ ЗНАЙДЕНО (можливо, чат не відкритий)")
            return False
    except Exception as e:
        print(f"   Результат: ❌ ПРОВАЛЕНО ({e})")
        return False

def test_activation_demo():
    """Демонстрація активації VentAI Enterprise."""
    print("\n🧪 Тест 4: Демо активації VentAI Enterprise")
    print("   ⚠️ УВАГА: Цей тест виконає реальну активацію!")
    
    response = input("   Продовжити? (y/N): ").lower().strip()
    if response != 'y':
        print("   Результат: ⏭️ ПРОПУЩЕНО")
        return True
    
    try:
        result = activate_ventai_enterprise()
        print(f"   Результат: {'✅ ПРОЙДЕНО' if result else '❌ ПРОВАЛЕНО'}")
        return result
    except Exception as e:
        print(f"   Результат: ❌ ПРОВАЛЕНО ({e})")
        return False

def main():
    """Запуск всіх тестів."""
    print("🚀 VENTAI ENTERPRISE AUTOCLICKER - ТЕСТУВАННЯ")
    print("=" * 50)
    
    tests = [
        test_image_validation,
        test_screen_hash,
        test_chat_input_detection,
        test_activation_demo
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ КРИТИЧНА ПОМИЛКА: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 ПІДСУМОК ТЕСТУВАННЯ:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"   Пройдено: {passed}/{total}")
    print(f"   Успішність: {passed/total*100:.1f}%")
    
    if passed == total:
        print("   Статус: ✅ ВСІ ТЕСТИ ПРОЙДЕНО")
    elif passed >= total * 0.75:
        print("   Статус: ⚠️ БІЛЬШІСТЬ ТЕСТІВ ПРОЙДЕНО")
    else:
        print("   Статус: ❌ БАГАТО ТЕСТІВ ПРОВАЛЕНО")
    
    print("\n💡 Для запуску реального автокликера:")
    print("   ./start_ventai_enterprise.sh")

if __name__ == "__main__":
    main()
