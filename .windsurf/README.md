# 🌊 Windsurf AI Integration для VentAI Enterprise

## 🎯 **ГОТОВО ДО ВИКОРИСТАННЯ** ✅

**Статус**: Повністю інтегровано та протестовано  
**Моделей**: 11 через 6 провайдерів  
**Безкоштовних**: 3 моделі  
**Версія**: Точна відповідність Windsurf API 2025-06-11

---

## ⚡ **ШВИДКИЙ СТАРТ**

### **1. Автоматичний запуск (рекомендовано)**
```bash
cd /Users/olegkizyma/workspaces/MVP/ventai-app
./start-windsurf-integration.sh
```

### **2. Ручний запуск**
```bash
cd .windsurf/server
npm install
npm run build
npm run start:http
```

### **3. Перевірка роботи**
```bash
curl http://localhost:8001/health
```

---

## 🤖 **ДОСТУПНІ AI МОДЕЛІ**

### **🆓 Безкоштовні моделі (3)**
- **windsurf-swe-1** - Спеціалізована для розробки ПЗ
- **windsurf-swe-1-lite** - Швидка допомога з кодом
- **deepseek-v3** - Потужна китайська модель

### **💰 Економічні моделі (0.1x кредитів)**
- **gpt-4o-mini** - Мінімальна версія GPT-4o
- **gemini-2.5-flash** - Швидкий Gemini

### **🧠 Reasoning моделі (2)**
- **o3-mini-reasoning** - OpenAI reasoning
- **claude-3.7-sonnet-thinking** - Claude з thinking

### **💪 Повні моделі**
- **gpt-4o** - Найкращий GPT-4
- **claude-3.5-sonnet** - Класичний Claude
- **gemini-2.5-pro** - Промо Gemini
- **grok-3** - Найновіший xAI

---

## 📋 **API ПРИКЛАДИ**

### **Список всіх провайдерів**
```bash
curl -X POST http://localhost:8001/mcp/call-tool \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_ai_providers", "params": {}}'
```

### **AI чат з безкоштовною моделлю**
```bash
curl -X POST http://localhost:8001/mcp/call-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "ai_chat_completion",
    "params": {
      "messages": [{"role": "user", "content": "Розрахуй вентиляцію для 100м²"}],
      "provider": "windsurf",
      "model": "windsurf-swe-1"
    }
  }'
```

**🎯 Windsurf AI повністю інтегровано з VentAI та готове до використання!**

*Останнє оновлення: 11 червня 2025*