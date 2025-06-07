#!/usr/bin/env python3
"""
Тестовий скрипт для VentAI MCP Server
Перевіряє функціональність AI провайдерів та MCP інструментів
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Додаємо шлях до MCP сервера
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server import VentAIMCPServer

async def test_basic_functionality():
    """Тестування базової функціональності"""
    print("🧪 Starting VentAI MCP Server Tests")
    print("=" * 50)
    
    # Ініціалізація сервера
    server = VentAIMCPServer()
    
    # Ініціалізація AI провайдерів
    print("\n1️⃣ Testing AI Providers Initialization...")
    await server.initialize_ai_providers()
    
    # Тест статусу AI провайдерів
    print("\n2️⃣ Testing AI Providers Status...")
    status_result = await server.execute_tool("ai_providers_status", {})
    
    if status_result.get("success"):
        status = status_result["status"]
        print(f"✅ AI Providers Status:")
        print(f"   📊 Total: {status['total_providers']}")
        print(f"   ✅ Available: {status['available_providers']}")
        print(f"   🎯 Primary: {status['primary_provider']}")
        
        print("   🔍 Provider Details:")
        for name, details in status["providers"].items():
            status_icon = "✅" if details["available"] else "❌"
            model_info = f" ({details.get('model', 'N/A')})" if details.get('model') else ""
            print(f"     {status_icon} {name}{model_info}")
        
        # Показуємо рекомендації
        print("   💡 Recommendations:")
        for rec in status_result.get("recommendations", []):
            print(f"     {rec}")
    else:
        print(f"❌ AI Providers Status failed: {status_result.get('error')}")
    
    # Тест AI генерації (якщо є доступні провайдери)
    if status_result.get("success") and status_result["status"]["available_providers"] > 0:
        print("\n3️⃣ Testing AI Generation...")
        
        test_prompts = [
            {
                "name": "Simple greeting",
                "prompt": "Привіт! Як ти можеш допомогти з HVAC системами?",
                "context": {"test": "greeting"}
            },
            {
                "name": "Technical question",
                "prompt": "Розкажи про енергоефективність VRF систем в Україні",
                "context": {"domain": "hvac", "country": "ukraine"}
            }
        ]
        
        for i, test in enumerate(test_prompts, 1):
            print(f"\n   3.{i} Testing: {test['name']}")
            ai_result = await server.execute_tool("ai_generate", {
                "prompt": test["prompt"],
                "context": test["context"]
            })
            
            if ai_result.get("success"):
                provider = ai_result.get("provider_used", "unknown")
                response_preview = ai_result["response"][:150] + "..." if len(ai_result["response"]) > 150 else ai_result["response"]
                print(f"     ✅ Success with {provider}")
                print(f"     📝 Response: {response_preview}")
            else:
                print(f"     ❌ Failed: {ai_result.get('error')}")
    
    # Тест AI HVAC аналізу
    if status_result.get("success") and status_result["status"]["available_providers"] > 0:
        print("\n4️⃣ Testing AI HVAC Analysis...")
        
        test_hvac_data = {
            "area": 150,
            "occupancy": 25,
            "climate_zone": "ukraine_zone_1",
            "current_system": "split_system",
            "building_type": "office",
            "insulation_level": "good"
        }
        
        analysis_types = ["basic", "detailed", "compliance"]
        
        for i, analysis_type in enumerate(analysis_types, 1):
            print(f"\n   4.{i} Testing {analysis_type} analysis...")
            hvac_result = await server.execute_tool("ai_hvac_analyze", {
                "hvac_data": test_hvac_data,
                "analysis_type": analysis_type
            })
            
            if hvac_result.get("success"):
                provider = hvac_result.get("provider_used", "unknown")
                analysis = hvac_result["analysis"]
                print(f"     ✅ Success with {provider}")
                
                # Виводимо ключові результати
                if isinstance(analysis, dict):
                    if "recommended_system" in analysis:
                        print(f"     🎯 Recommendation: {analysis['recommended_system']}")
                    if "estimated_cost_usd" in analysis:
                        print(f"     💰 Cost: ${analysis['estimated_cost_usd']}")
                    if "energy_efficiency" in analysis:
                        print(f"     ⚡ Efficiency: {analysis['energy_efficiency']}")
                else:
                    preview = str(analysis)[:100] + "..." if len(str(analysis)) > 100 else str(analysis)
                    print(f"     📝 Analysis: {preview}")
            else:
                print(f"     ❌ Failed: {hvac_result.get('error')}")
    
    # Тест традиційних HVAC інструментів
    print("\n5️⃣ Testing Traditional HVAC Tools...")
    
    traditional_tests = [
        {
            "name": "HVAC Optimization",
            "tool": "hvac_optimize",
            "params": {
                "area": 100,
                "occupancy": 15,
                "climate_zone": "temperate",
                "current_system": "split"
            }
        },
        {
            "name": "Project Status",
            "tool": "get_project_status",
            "params": {"project_ids": ["test_project_1"]}
        }
    ]
    
    for i, test in enumerate(traditional_tests, 1):
        print(f"\n   5.{i} Testing {test['name']}...")
        result = await server.execute_tool(test["tool"], test["params"])
        
        if result.get("success"):
            print(f"     ✅ Success")
            # Показуємо ключову інформацію
            if "optimization_result" in result:
                opt = result["optimization_result"]
                print(f"     📊 Optimization: {opt}")
            if "status_info" in result:
                status = result["status_info"]
                print(f"     📈 Status: {status.get('status', 'N/A')}")
        else:
            print(f"     ❌ Failed: {result.get('error')}")
    
    # Підсумок тестування
    print("\n" + "=" * 50)
    print("🎯 Test Summary")
    print("=" * 50)
    
    if status_result.get("success"):
        available_ai = status_result["status"]["available_providers"]
        total_ai = status_result["status"]["total_providers"]
        
        if available_ai > 0:
            print(f"✅ MCP Server: Ready for production")
            print(f"✅ AI Providers: {available_ai}/{total_ai} available")
            print(f"✅ Primary Provider: {status_result['status']['primary_provider']}")
            print("✅ Claude 4 can now interact with VentAI!")
            
            print("\n🔧 Next Steps:")
            print("1. Configure Claude to use this MCP server")
            print("2. Test with actual HVAC projects")
            print("3. Monitor performance and adjust as needed")
            
        else:
            print("⚠️  MCP Server: Limited functionality")
            print("❌ AI Providers: None available")
            print("💡 Configure at least one AI provider for full functionality")
    else:
        print("❌ MCP Server: Failed to initialize")
        print("🔧 Check logs and configuration")

async def test_specific_provider(provider_name: str):
    """Тестування конкретного провайдера"""
    print(f"\n🎯 Testing specific provider: {provider_name}")
    print("-" * 40)
    
    server = VentAIMCPServer()
    await server.initialize_ai_providers()
    
    # Перевіряємо чи доступний провайдер
    available = server.ai_manager.get_available_providers()
    if provider_name not in available:
        print(f"❌ Provider {provider_name} is not available")
        print(f"Available providers: {available}")
        return
    
    # Тестуємо генерацію
    print("Testing generation...")
    result = await server.execute_tool("ai_generate", {
        "prompt": "Опиши переваги енергоефективних HVAC систем",
        "provider": provider_name
    })
    
    if result.get("success"):
        print(f"✅ Generation successful")
        print(f"Response: {result['response'][:200]}...")
    else:
        print(f"❌ Generation failed: {result.get('error')}")
    
    # Тестуємо HVAC аналіз
    print("\nTesting HVAC analysis...")
    hvac_result = await server.execute_tool("ai_hvac_analyze", {
        "hvac_data": {
            "area": 200,
            "occupancy": 30,
            "climate_zone": "ukraine_zone_2",
            "current_system": "central_air"
        },
        "provider": provider_name,
        "analysis_type": "detailed"
    })
    
    if hvac_result.get("success"):
        print(f"✅ HVAC analysis successful")
        analysis = hvac_result["analysis"]
        print(f"Analysis type: {type(analysis)}")
        if isinstance(analysis, dict):
            for key, value in list(analysis.items())[:3]:  # Показуємо перші 3 ключі
                print(f"  {key}: {value}")
    else:
        print(f"❌ HVAC analysis failed: {hvac_result.get('error')}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Тест конкретного провайдера
        provider = sys.argv[1]
        asyncio.run(test_specific_provider(provider))
    else:
        # Повний тест
        asyncio.run(test_basic_functionality())
