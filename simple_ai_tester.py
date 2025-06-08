#!/usr/bin/env python3
"""
Простий тестувальник AI провайдерів без MCP
Альтернатива Claude Desktop для розробки
"""

import asyncio
import sys
import os
sys.path.append('/workspaces/MVP/backend')

from mcp_ai_providers import AIProviderManager

class SimpleAITester:
    """Простий інтерфейс для тестування AI без Claude Desktop"""
    
    def __init__(self):
        self.ai_manager = AIProviderManager()
        
    async def initialize(self):
        """Ініціалізація AI провайдерів"""
        print("🤖 Ініціалізація AI провайдерів...")
        results = await self.ai_manager.initialize_all()
        
        for provider, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {provider}")
            
        available = self.ai_manager.get_available_providers()
        if available:
            print(f"🚀 Доступні провайдери: {', '.join(available)}")
            return True
        else:
            print("❌ Жодного AI провайдера недоступно!")
            return False
    
    async def test_hvac_analysis(self):
        """Тест HVAC аналізу"""
        print("\n🏢 Тестуємо HVAC аналіз...")
        
        test_data = {
            "area": 150,
            "occupancy": 30, 
            "climate_zone": "temperate",
            "building_type": "office"
        }
        
        available = self.ai_manager.get_available_providers()
        if not available:
            print("❌ Немає доступних AI провайдерів")
            return
            
        provider = available[0]
        try:
            result = await self.ai_manager.analyze_hvac_with_provider(provider, test_data)
            print(f"✅ Результат від {provider}:")
            print(f"   {result}")
        except Exception as e:
            print(f"❌ Помилка: {e}")
    
    async def interactive_chat(self):
        """Інтерактивний чат з AI"""
        print("\n💬 Інтерактивний режим (введіть 'exit' для виходу):")
        
        while True:
            try:
                query = input("\n🧑‍💻 Ваш запит: ").strip()
                
                if query.lower() in ['exit', 'quit', 'вихід']:
                    print("👋 До побачення!")
                    break
                    
                if not query:
                    continue
                
                print("🤔 Обробляю...")
                
                context = {
                    "system_info": "Ти AI експерт VentAI для HVAC систем в Україні. Знаєш ДБН В.2.5-67:2013."
                }
                
                result = await self.ai_manager.generate_with_fallback(query, context)
                
                if result.get("success"):
                    print(f"🤖 Відповідь ({result['provider_used']}):")
                    print(f"   {result['response']}")
                else:
                    print(f"❌ Помилка: {result.get('error')}")
                    
            except KeyboardInterrupt:
                print("\n👋 До побачення!")
                break
            except Exception as e:
                print(f"❌ Системна помилка: {e}")

async def main():
    """Головна функція"""
    print("🚀 VentAI Simple AI Tester")
    print("Альтернатива Claude Desktop для розробки")
    print("=" * 50)
    
    tester = SimpleAITester()
    
    # Ініціалізація
    if not await tester.initialize():
        print("❌ Не вдалося ініціалізувати AI провайдери")
        return
    
    print("\n🎯 Що бажаєте протестувати?")
    print("1. Швидкий HVAC тест")
    print("2. Інтерактивний чат") 
    print("3. Все разом")
    
    try:
        choice = input("\nВаш вибір (1-3): ").strip()
        
        if choice == "1":
            await tester.test_hvac_analysis()
        elif choice == "2":
            await tester.interactive_chat()
        elif choice == "3":
            await tester.test_hvac_analysis()
            await tester.interactive_chat()
        else:
            print("❌ Невірний вибір")
            
    except KeyboardInterrupt:
        print("\n👋 Програма перервана користувачем")

if __name__ == "__main__":
    asyncio.run(main())
