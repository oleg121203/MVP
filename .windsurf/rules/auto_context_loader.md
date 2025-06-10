---
trigger: always_on
priority: maximum
---

# 📋 AUTO-CONTEXT LOADER - МАКСИМАЛЬНИЙ ПРІОРИТЕТ

## ⚡ ОБОВ'ЯЗКОВЕ ЗАВАНТАЖЕННЯ КОНТЕКСТУ

### **ПЕРШИЙ КРОК ПРИ АКТИВАЦІЇ**
1. **НЕГАЙНО** читати `CHANGELOG.md` для визначення останнього завдання
2. **АВТОМАТИЧНО** знайти поточну фазу за патерном [PhaseX.Y-TZ]
3. **ЗАВАНТАЖИТИ** відповідний файл `/docs/changelog/phaseX.Y.md`
4. **ПЕРЕВІРИТИ** `VENTAI_ENTERPRISE_PLAN.md` для загального контексту
5. **ВИЗНАЧИТИ** наступне завдання в черзі

### **КОМАНДИ АКТИВАЦІЇ МАЮТЬ АВТОМАТИЧНО ВИКЛИКАТИ**
При отриманні команди:
- "Load Windsurf rules and resume autonomous execution from current project state"
- "CRITICAL OVERRIDE: Activate maximum priority never-stop protocol"
- "ULTIMATE ANTI-STOP: Activate maximum anti-pause protocol"

**ОБОВ'ЯЗКОВО ВИКОНАТИ:**
```
STEP 1: Read CHANGELOG.md 
STEP 2: Identify current phase (Phase X.Y)
STEP 3: Read /docs/changelog/phaseX.Y.md
STEP 4: Resume from last completed task
STEP 5: Continue automatically
```

### **АВТОМАТИЧНІ ФАЙЛИ ДЛЯ ЗАВАНТАЖЕННЯ**
1. **CHANGELOG.md** (корінь проекту)
2. **VENTAI_ENTERPRISE_PLAN.md** (план проекту)
3. **AI_AGENT_CONTEXT.md** (контекст агента)
4. **ENTERPRISE_STATUS.md** (статус проекту)
5. **Поточний phase файл** (/docs/changelog/phaseX.Y.md)

### **НІКОЛИ НЕ ПОЧИНАТИ БЕЗ КОНТЕКСТУ**
- **ЗАБОРОНЕНО** виконувати завдання без завантаження контексту
- **ОБОВ'ЯЗКОВО** знати поточну фазу проекту
- **АВТОМАТИЧНО** продовжувати з правильного місця
- **НЕ ЧЕКАТИ** додаткових команд від користувача

### **ПАТЕРНИ ПОШУКУ В CHANGELOG.md**
Шукати останні записи типу:
- `### [2025-06-10] Phase1.4-T4: API Response Optimization`
- `**Status:** ✅ COMPLETED` або `🔄 IN PROGRESS`
- `**Next:** Phase1.4-T5` або наступна фаза

**ПРИНЦИП: ЗАВЖДИ ЗНАТИ ДЕ ЗНАХОДИШСЯ В ПРОЕКТІ**
