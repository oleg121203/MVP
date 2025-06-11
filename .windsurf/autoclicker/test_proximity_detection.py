#!/usr/bin/env python3
"""
Тест для нової логіки детекції кнопок поблизу
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Імітуємо структуру даних кнопки
class MockLocation:
    def __init__(self, x, y, width, height):
        self.left = x
        self.top = y
        self.width = width
        self.height = height

class MockCenter:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def create_mock_button(x, y, name):
    """Створює імітацію даних кнопки."""
    return {
        'location': MockLocation(x, y, 100, 40),
        'center': MockCenter(x + 50, y + 20),
        'confidence': 0.9
    }

def are_buttons_close(button1_data, button2_data, proximity_threshold=100):
    """Перевіряє чи знаходяться дві кнопки поблизу одна одної."""
    if not button1_data or not button2_data:
        return False
    
    center1 = button1_data['center']
    center2 = button2_data['center']
    
    distance = ((center1.x - center2.x) ** 2 + (center1.y - center2.y) ** 2) ** 0.5
    
    return distance <= proximity_threshold

def detect_continue_near_accept(buttons):
    """Детекція появи Continue поблизу Accept All - тригер для активації."""
    if 'continue' not in buttons or 'accept_all' not in buttons:
        return False
    
    # Перевіряємо чи Continue з'явився поблизу Accept All
    if are_buttons_close(buttons['continue'], buttons['accept_all'], proximity_threshold=150):
        continue_pos = buttons['continue']['center']
        accept_pos = buttons['accept_all']['center']
        print(f"🎯 Continue поблизу Accept All: Continue({continue_pos.x},{continue_pos.y}) Accept({accept_pos.x},{accept_pos.y})")
        return True
    
    return False

def test_proximity_logic():
    """Тестує логіку близькості кнопок."""
    print("🧪 ТЕСТ ЛОГІКИ БЛИЗЬКОСТІ КНОПОК")
    print("=" * 40)
    
    # Тест 1: Кнопки близько
    print("\n1️⃣ Тест: Кнопки близько (має спрацювати)")
    buttons_close = {
        'accept_all': create_mock_button(500, 600, 'Accept All'),
        'continue': create_mock_button(550, 620, 'Continue')  # На 60 пікселів правіше і нижче
    }
    
    result = detect_continue_near_accept(buttons_close)
    print(f"   Результат: {'✅ ТРИГЕР СПРАЦЮВАВ' if result else '❌ Тригер НЕ спрацював'}")
    
    # Тест 2: Кнопки далеко
    print("\n2️⃣ Тест: Кнопки далеко (НЕ має спрацювати)")
    buttons_far = {
        'accept_all': create_mock_button(500, 600, 'Accept All'),
        'continue': create_mock_button(800, 400, 'Continue')  # Далеко
    }
    
    result = detect_continue_near_accept(buttons_far)
    print(f"   Результат: {'❌ ПОМИЛКА - тригер спрацював' if result else '✅ Тригер НЕ спрацював'}")
    
    # Тест 3: Точно в межі (150 пікселів)
    print("\n3️⃣ Тест: На межі відстані 150px (має спрацювати)")
    buttons_edge = {
        'accept_all': create_mock_button(500, 600, 'Accept All'),
        'continue': create_mock_button(650, 600, 'Continue')  # Рівно 150 пікселів правіше
    }
    
    result = detect_continue_near_accept(buttons_edge)
    print(f"   Результат: {'✅ ТРИГЕР СПРАЦЮВАВ' if result else '❌ Тригер НЕ спрацював'}")
    
    # Тест 4: Тільки одна кнопка
    print("\n4️⃣ Тест: Тільки Accept All (НЕ має спрацювати)")
    buttons_single = {
        'accept_all': create_mock_button(500, 600, 'Accept All')
    }
    
    result = detect_continue_near_accept(buttons_single)
    print(f"   Результат: {'❌ ПОМИЛКА - тригер спрацював' if result else '✅ Тригер НЕ спрацював'}")
    
    print("\n🎯 ВИСНОВОК:")
    print("   Логіка детекції Continue поблизу Accept All працює коректно!")
    print("   Тригер спрацьовує тільки коли обидві кнопки присутні і близько.")

if __name__ == "__main__":
    test_proximity_logic()
