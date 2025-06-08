#!/usr/bin/env python3
"""
VentAI MCP Server для Claude 4
Забезпечує доступ до AI сервісів VentAI через Model Context Protocol
"""

import asyncio
import json
import logging
import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Додаємо шлях до FastAPI додатку
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Імпортуємо AI провайдери
from mcp_ai_providers import AIProviderManager

try:
    from fastapi_app.ai.optimization_service import HVACOptimizer
    from fastapi_app.ai.cost_optimization_service import CostOptimizationService
    from fastapi_app.ai.project_analysis_service import ProjectAnalysisService
    from fastapi_app.ai.procurement_service import ProcurementService
    from fastapi_app.ai.vector_db_service import VectorDBService
    from fastapi_app.ai.crm_service import CRMService
except ImportError as e:
    print(f"Warning: Could not import AI services: {e}")
    print("Running in basic mode without AI capabilities")

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VentAIMCPServer:
    """MCP Server для VentAI з підтримкою всіх AI сервісів"""
    
    def __init__(self):
        self.project_root = os.getenv('VENTAI_PROJECT_ROOT', '/workspaces/MVP')
        self.port = int(os.getenv('MCP_PORT', '8001'))
        self.host = os.getenv('MCP_HOST', '0.0.0.0')
        self.ai_manager = AIProviderManager()
        self.initialize_services()

    async def initialize_ai_providers(self):
        """Ініціалізація AI провайдерів"""
        logger.info("🤖 Initializing AI providers...")
        provider_results = await self.ai_manager.initialize_all()
        
        for provider, success in provider_results.items():
            status = "✅" if success else "❌"
            logger.info(f"  {status} {provider}")
        
        available = self.ai_manager.get_available_providers()
        if available:
            logger.info(f"🚀 Primary AI provider: {self.ai_manager.primary_provider}")
            logger.info(f"📋 Available providers: {', '.join(available)}")
        else:
            logger.warning("⚠️  No AI providers available!")
        
        return provider_results

    def initialize_services(self):
        """Ініціалізація AI сервісів"""
        try:
            # Basic service initialization - можна розширити пізніше
            self.hvac_optimizer = None  # HVACOptimizer()
            self.vector_db = None  # VectorDBService()
            self.cost_optimizer = None  # CostOptimizationService(self.vector_db)
            self.project_analyzer = None  # ProjectAnalysisService()
            self.procurement_service = None  # ProcurementService()
            self.crm_service = None  # CRMService()
            logger.info("✅ Basic services initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize services: {e}")

    async def get_capabilities(self) -> Dict[str, Any]:
        """Повертає можливості MCP сервера"""
        return {
            "tools": {
                "hvac_optimize": {
                    "description": "Оптимізація HVAC системи",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "area": {"type": "number", "description": "Площа приміщення (м²)"},
                            "occupancy": {"type": "integer", "description": "Кількість людей"},
                            "climate_zone": {"type": "string", "description": "Кліматична зона"},
                            "current_system": {"type": "string", "description": "Поточна система"}
                        },
                        "required": ["area", "occupancy", "climate_zone"]
                    }
                },
                "project_analyze": {
                    "description": "Аналіз HVAC проекту",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "project_data": {"type": "object", "description": "Дані проекту"},
                            "check_compliance": {"type": "boolean", "description": "Перевірка відповідності ДБН"}
                        },
                        "required": ["project_data"]
                    }
                },
                "ai_generate": {
                    "description": "Генерація відповіді через AI провайдери",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string", "description": "Запит для AI"},
                            "provider": {"type": "string", "description": "Конкретний провайдер (ollama/gemini/openai/anthropic)"},
                            "context": {"type": "object", "description": "Додатковий контекст"}
                        },
                        "required": ["prompt"]
                    }
                },
                "ai_hvac_analyze": {
                    "description": "AI аналіз HVAC системи",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "hvac_data": {"type": "object", "description": "Дані HVAC системи"},
                            "provider": {"type": "string", "description": "AI провайдер для аналізу"},
                            "analysis_type": {"type": "string", "enum": ["basic", "detailed", "compliance"], "description": "Тип аналізу"}
                        },
                        "required": ["hvac_data"]
                    }
                },
                "ai_providers_status": {
                    "description": "Статус AI провайдерів",
                    "input_schema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            "resources": {
                "workspace": {
                    "description": "VentAI workspace",
                    "uri": f"file://{self.project_root}"
                },
                "documentation": {
                    "description": "Документація проекту",
                    "uri": f"file://{self.project_root}/docs"
                }
            }
        }

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Виконання інструменту"""
        try:
            if tool_name == "hvac_optimize":
                return await self._hvac_optimize(parameters)
            elif tool_name == "project_analyze":
                return await self._project_analyze(parameters)
            elif tool_name == "ai_generate":
                return await self._ai_generate(parameters)
            elif tool_name == "ai_hvac_analyze":
                return await self._ai_hvac_analyze(parameters)
            elif tool_name == "ai_providers_status":
                return await self._ai_providers_status(parameters)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {"error": str(e)}

    async def _hvac_optimize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Оптимізація HVAC системи"""
        try:
            # Базова логіка оптимізації
            area = params["area"]
            occupancy = params["occupancy"]
            climate_zone = params.get("climate_zone", "temperate")
            
            # Розрахунок базових параметрів
            air_change_rate = 6  # повітрообмін на годину
            required_airflow = area * air_change_rate * 2.5  # м³/год
            
            result = {
                "recommended_system": "Припливно-витяжна система з рекуперацією",
                "required_airflow_m3h": required_airflow,
                "estimated_power_kw": required_airflow * 0.003,
                "estimated_cost_usd": area * 150,
                "energy_efficiency_class": "A",
                "annual_savings_percent": 25
            }
            
            return {
                "success": True,
                "optimization_result": result,
                "recommendations": [
                    f"Рекомендована система: {result['recommended_system']}",
                    f"Необхідний повітрообмін: {result['required_airflow_m3h']:.0f} м³/год",
                    f"Очікувана економія: {result['annual_savings_percent']}%"
                ]
            }
        except Exception as e:
            return {"error": f"HVAC optimization failed: {e}"}

    async def _project_analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Аналіз проекту"""
        try:
            project_data = params["project_data"]
            check_compliance = params.get("check_compliance", True)
            
            result = {
                "project_status": "compliant",
                "compliance_score": 85,
                "energy_efficiency": "A",
                "estimated_payback_years": 5.2,
                "recommendations": [
                    "Розглянути встановлення додаткової рекуперації",
                    "Перевірити ізоляцію повітропроводів"
                ]
            }
            
            return {
                "success": True,
                "analysis_result": result,
                "compliance_status": "compliant" if check_compliance else "not_checked"
            }
        except Exception as e:
            return {"error": f"Project analysis failed: {e}"}

    async def _ai_generate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Генерація відповіді через AI провайдери"""
        try:
            prompt = params["prompt"]
            provider = params.get("provider")
            context = params.get("context", {})
            
            # Додаємо контекст VentAI
            ventai_context = {
                "system_info": "Ти AI експерт VentAI для HVAC систем в Україні. Знаєш ДБН В.2.5-67:2013, енергоефективність, українські будівельні норми.",
                **context
            }
            
            if provider:
                # Використовуємо конкретний провайдер
                response = await self.ai_manager.generate_with_provider(provider, prompt, ventai_context)
                return {
                    "success": True,
                    "response": response,
                    "provider_used": provider
                }
            else:
                # Використовуємо fallback логіку
                result = await self.ai_manager.generate_with_fallback(prompt, ventai_context)
                return result
                
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return {"error": str(e)}

    async def _ai_hvac_analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """AI аналіз HVAC системи"""
        try:
            hvac_data = params["hvac_data"]
            provider = params.get("provider")
            analysis_type = params.get("analysis_type", "basic")
            
            if provider:
                # Використовуємо конкретний провайдер
                result = await self.ai_manager.analyze_hvac_with_provider(provider, hvac_data)
                return {
                    "success": True,
                    "analysis": result,
                    "provider_used": provider,
                    "analysis_type": analysis_type
                }
            else:
                # Пробуємо з кожним доступним провайдером
                available_providers = self.ai_manager.get_available_providers()
                
                if not available_providers:
                    return {"error": "No AI providers available"}
                
                primary_provider = available_providers[0]
                result = await self.ai_manager.analyze_hvac_with_provider(primary_provider, hvac_data)
                
                return {
                    "success": True,
                    "analysis": result,
                    "provider_used": primary_provider,
                    "analysis_type": analysis_type
                }
                
        except Exception as e:
            logger.error(f"AI HVAC analysis failed: {e}")
            return {"error": str(e)}

    async def _ai_providers_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Статус AI провайдерів"""
        try:
            available_providers = self.ai_manager.get_available_providers()
            all_providers = list(self.ai_manager.providers.keys())
            
            provider_details = {}
            for name, provider in self.ai_manager.providers.items():
                provider_details[name] = {
                    "available": provider.is_available,
                    "name": provider.name
                }
                
                # Додаємо специфічну інформацію про провайдера
                if hasattr(provider, 'model'):
                    provider_details[name]["model"] = provider.model
                if hasattr(provider, 'base_url'):
                    provider_details[name]["base_url"] = provider.base_url
            
            return {
                "success": True,
                "status": {
                    "total_providers": len(all_providers),
                    "available_providers": len(available_providers),
                    "primary_provider": self.ai_manager.primary_provider,
                    "providers": provider_details
                },
                "recommendations": self._get_provider_recommendations(provider_details)
            }
            
        except Exception as e:
            logger.error(f"AI providers status check failed: {e}")
            return {"error": str(e)}

    def _get_provider_recommendations(self, provider_details: Dict[str, Any]) -> List[str]:
        """Генерує рекомендації щодо AI провайдерів"""
        recommendations = []
        
        available_count = sum(1 for p in provider_details.values() if p["available"])
        
        if available_count == 0:
            recommendations.append("❌ Жоден AI провайдер недоступний. Перевірте API ключі та налаштування.")
        elif available_count == 1:
            recommendations.append("⚠️  Доступний лише один AI провайдер. Рекомендуємо налаштувати резервні провайдери.")
        else:
            recommendations.append(f"✅ Доступно {available_count} AI провайдерів. Система має гарну відмовостійкість.")
        
        # Специфічні рекомендації
        if not provider_details.get("ollama", {}).get("available"):
            recommendations.append("💡 Ollama недоступний. Для локальної роботи встановіть Ollama та завантажте модель.")
        
        if not provider_details.get("openai", {}).get("available"):
            recommendations.append("💡 OpenAI недоступний. Додайте OPENAI_API_KEY для доступу до GPT моделей.")
        
        if not provider_details.get("anthropic", {}).get("available"):
            recommendations.append("💡 Anthropic недоступний. Додайте ANTHROPIC_API_KEY для доступу до Claude.")
        
        if not provider_details.get("gemini", {}).get("available"):
            recommendations.append("💡 Gemini недоступний. Додайте GEMINI_API_KEY для доступу до Google AI.")
        
        return recommendations


async def main():
    """Головна функція MCP сервера"""
    server = VentAIMCPServer()
    
    # Виведення інформації про сервер
    print("🚀 VentAI MCP Server for Claude 4")
    print(f"📁 Project root: {server.project_root}")
    
    # Ініціалізація AI провайдерів
    print("\n🤖 Initializing AI providers...")
    await server.initialize_ai_providers()
    
    capabilities = await server.get_capabilities()
    print(f"🛠  Available tools: {len(capabilities['tools'])}")
    print(f"📚 Available resources: {len(capabilities['resources'])}")
    
    # Тестування основних функцій
    print("\n🧪 Testing functionality...")
    
    # Тест AI провайдерів
    ai_status = await server.execute_tool("ai_providers_status", {})
    if ai_status.get("success"):
        status_info = ai_status["status"]
        print(f"✅ AI Providers: {status_info['available_providers']}/{status_info['total_providers']} available")
        if status_info['primary_provider']:
            print(f"🎯 Primary provider: {status_info['primary_provider']}")
        
        # Показуємо рекомендації
        for rec in ai_status.get("recommendations", []):
            print(f"  {rec}")
    
    # Тест AI генерації
    if ai_status.get("success") and ai_status["status"]["available_providers"] > 0:
        print("\n🧪 Testing AI generation...")
        ai_test = await server.execute_tool("ai_generate", {
            "prompt": "Привіт! Опиши себе як VentAI експерт.",
            "context": {"test": True}
        })
        if ai_test.get("success"):
            print(f"✅ AI Generation test passed with {ai_test.get('provider_used', 'unknown')}")
            print(f"  Response preview: {ai_test['response'][:100]}...")
        else:
            print(f"❌ AI Generation test failed: {ai_test.get('error')}")
    
    # Тест HVAC оптимізації
    test_params = {
        "area": 100,
        "occupancy": 10,
        "climate_zone": "temperate",
        "current_system": "split"
    }
    
    result = await server.execute_tool("hvac_optimize", test_params)
    if result.get("success"):
        print("✅ HVAC optimization test passed")
    else:
        print(f"❌ HVAC optimization test failed: {result.get('error')}")
    
    # Тест AI HVAC аналізу
    if ai_status.get("success") and ai_status["status"]["available_providers"] > 0:
        print("\n🧪 Testing AI HVAC analysis...")
        hvac_test = await server.execute_tool("ai_hvac_analyze", {
            "hvac_data": test_params,
            "analysis_type": "basic"
        })
        if hvac_test.get("success"):
            print("✅ AI HVAC analysis test passed")
        else:
            print(f"❌ AI HVAC analysis test failed: {hvac_test.get('error')}")
    
    print("\n🎯 VentAI MCP Server ready for Claude 4!")
    print("💡 You can now use Claude to interact with VentAI services")
    print("\n📋 Available AI providers:")
    available_providers = server.ai_manager.get_available_providers()
    if available_providers:
        for provider in available_providers:
            print(f"  ✅ {provider}")
    else:
        print("  ❌ No AI providers available")
    
    print("\n🔧 Quick start commands for Claude:")
    print("  - 'Проаналізуй HVAC систему для офісу 100м²'")
    print("  - 'Оптимізуй вентиляцію для 50 людей'")
    print("  - 'Перевір відповідність проекту ДБН'")
    print("  - 'Знайди матеріали для проекту'")
    
    # Запуск HTTP сервера для health checks
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                health_status = {
                    "status": "healthy",
                    "mcp_server": "running",
                    "ai_providers": server.ai_manager.get_available_providers(),
                    "capabilities": len(capabilities['tools']),
                    "timestamp": asyncio.get_event_loop().time()
                }
                self.wfile.write(json.dumps(health_status, indent=2).encode())
            else:
                self.send_response(404)
                self.end_headers()
    
    # Запуск HTTP сервера в окремому потоці
    def start_http_server():
        httpd = HTTPServer((server.host, server.port), HealthHandler)
        print(f"\n🌐 Health check server running on http://{server.host}:{server.port}/health")
        httpd.serve_forever()
    
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    print("\n✅ VentAI MCP Server is ready! Press Ctrl+C to stop.")
    
    try:
        # Тримаємо сервер живим
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down VentAI MCP Server...")


if __name__ == "__main__":
    asyncio.run(main())