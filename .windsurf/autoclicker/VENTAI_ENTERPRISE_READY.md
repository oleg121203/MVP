# 🚀 VentAI Enterprise Autoclicker - Готовий до використання!

## ✅ Що доопрацьовано:

### 🎯 **Нова логіка активації:**
- **Умова:** Якщо 60 секунд немає змін у картинці (нижня частина екрану) І немає кнопки Continue
- **Дія:** Автоматично натискається Escape All + вводиться команда `VENTAI ENTERPRISE ACTIVATE`
- **Відправка:** Команда Enter для відправки

### 🔍 **Розумна детекція:**
- Моніторинг змін екрану через MD5 хешування
- Перевірка кожні 5 секунд
- Скидання таймера при будь-якій активності

### ⚡ **Hands-Free режим:**
- Без прокрутки
- Без захоплення миші  
- Тільки швидкі кліки

## 🚀 Швидкий запуск:

```bash
cd .windsurf/autoclicker
./start_ventai_enterprise.sh
```

## 📋 Логіка роботи:

```
1. Шукає кнопки Accept All + Continue
   ↓
2. Якщо ОБІ знайдені → швидка послідовність кліків
   ↓  
3. Якщо НЕ знайдені → моніторинг неактивності
   ↓
4. Якщо 60+ секунд БЕЗ змін → активація VentAI Enterprise:
   • Escape
   • Accept All (якщо є)
   • Знаходить поле чату
   • Вводить "VENTAI ENTERPRISE ACTIVATE"
   • Натискає Enter
   ↓
5. Повтор циклу
```

## 🎮 Приклад роботи:

### Нормальний режим:
```
🔍 Цикл #3: VentAI Enterprise пошук...
✅ Знайдено 'Accept all': Box(left=100, top=200, width=80, height=30)
✅ Знайдено 'Continue': Box(left=200, top=250, width=70, height=30)
⚡ HANDS-FREE: Швидка послідовність...
1️⃣ Швидкий клік Accept All...
2️⃣ Швидкий клік Continue...
✅ Hands-Free послідовність завершено!
```

### Режим активації:
```
🔍 Цикл #15: VentAI Enterprise пошук...
⏳ Очікую: Continue, Accept All (неактивність: 45с/60с)
⏳ Очікую: Continue, Accept All (неактивність: 55с/60с)

⏰ НЕАКТИВНІСТЬ 60с (>60с)
🎯 Умови для активації VentAI Enterprise виконані!

🚀 АКТИВАЦІЯ VENTAI ENTERPRISE
===============================
1️⃣ Натискаю Escape...
2️⃣ Шукаю кнопку Accept All...
✅ Натиснуто Accept All в Point(x=1816, y=958)
3️⃣ Шукаю поле вводу чату...
✅ Знайдено поле вводу чату в 960, 980
4️⃣ Активую поле вводу...
5️⃣ Вводжу команду активації...
6️⃣ Відправляю команду (Enter)...
✅ VENTAI ENTERPRISE АКТИВОВАНО!
📝 Команда: VENTAI ENTERPRISE ACTIVATE
```

## ⚙️ Налаштування:

У файлі `autoclicker_ventai_enterprise.py`:

```python
INACTIVITY_TIMEOUT = 60           # Секунд до активації
ACTIVATION_COMMAND = "VENTAI ENTERPRISE ACTIVATE"
SCREEN_CHECK_INTERVAL = 5         # Інтервал перевірки екрану
```

## 🛑 Зупинка:

- **Ctrl+C** - нормальна зупинка
- **Створити файл stop.flag** - аварійна зупинка
- **Мишу в верхній лівий кут** - PyAutoGUI failsafe

## 🧪 Тестування:

```bash
python3 test_ventai_enterprise.py
```

Результат тестування: ✅ **4/4 тести пройдено (100% успіх)**

## 📁 Файли:

```
.windsurf/autoclicker/
├── autoclicker_ventai_enterprise.py      # 🎯 Основний скрипт
├── start_ventai_enterprise.sh            # 🚀 Швидкий запуск
├── test_ventai_enterprise.py             # 🧪 Тестування
├── README_VENTAI_ENTERPRISE.md           # 📖 Повна документація
├── requirements.txt                       # 📦 Залежності
└── images/
    ├── accept_all.png                     # 🖼️ Кнопка Accept All
    └── continue.png                       # 🖼️ Кнопка Continue
```

## 🎯 Особливості:

1. **Розумна детекція неактивності** - аналізує зміни екрану
2. **Автономна активація** - не потребує втручання
3. **Захист від повторів** - активація лише один раз за сесію
4. **Безпечні кліки** - мінімальне втручання в UI
5. **Детальне логування** - повна інформація про процес

## ✅ Готово до використання!

Скрипт повністю готовий та протестований. Автоматично активує VentAI Enterprise при неактивності 60+ секунд.

**Команда запуску:**
```bash
cd .windsurf/autoclicker && ./start_ventai_enterprise.sh
```
