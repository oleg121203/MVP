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

# Додаємо шлях до FastAPI додатку
sys.path.insert(0, str(Path(__file__).parent.parent / "backend" / "src"))

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
        self.project_root = os.getenv('VENTAI_PROJECT_ROOT', '/app')
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
            self.hvac_optimizer = HVACOptimizer()
            self.vector_db = VectorDBService()
            self.cost_optimizer = CostOptimizationService(self.vector_db)
            self.project_analyzer = ProjectAnalysisService()
            self.procurement_service = ProcurementService()
            self.crm_service = CRMService()
            logger.info("✅ All AI services initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize AI services: {e}")
            self.hvac_optimizer = None
            self.vector_db = None
            self.cost_optimizer = None
            self.project_analyzer = None
            self.procurement_service = None
            self.crm_service = None

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
                "cost_optimize": {
                    "description": "Оптимізація вартості проекту",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "project_data": {"type": "object", "description": "Дані проекту"},
                            "target_savings": {"type": "number", "description": "Цільова економія (%)"}
                        },
                        "required": ["project_data"]
                    }
                },
                "material_search": {
                    "description": "Пошук матеріалів у векторній базі",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Пошуковий запит"},
                            "max_cost": {"type": "number", "description": "Максимальна вартість"},
                            "top_k": {"type": "integer", "description": "Кількість результатів"}
                        },
                        "required": ["query"]
                    }
                },
                "procurement_analyze": {
                    "description": "Аналіз закупівель",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "project_data": {"type": "object", "description": "Дані проекту"},
                            "criteria": {"type": "object", "description": "Критерії оцінки"}
                        },
                        "required": ["project_data"]
                    }
                },
                "crm_sync": {
                    "description": "Синхронізація з CRM",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "direction": {"type": "string", "enum": ["push", "pull"], "description": "Напрямок синхронізації"},
                            "projects": {"type": "array", "description": "Список проектів"}
                        },
                        "required": ["direction"]
                    }
                },
                "get_project_status": {
                    "description": "Отримання статусу проектів",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "project_ids": {"type": "array", "description": "ID проектів"}
                        }
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
                },
                "api_examples": {
                    "description": "Приклади API",
                    "uri": f"file://{self.project_root}/docs/API_EXAMPLES.md"
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
            elif tool_name == "cost_optimize":
                return await self._cost_optimize(parameters)
            elif tool_name == "material_search":
                return await self._material_search(parameters)
            elif tool_name == "procurement_analyze":
                return await self._procurement_analyze(parameters)
            elif tool_name == "crm_sync":
                return await self._crm_sync(parameters)
            elif tool_name == "get_project_status":
                return await self._get_project_status(parameters)
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
        if not self.hvac_optimizer:
            return {"error": "HVAC optimizer not available"}
        
        try:
            result = self.hvac_optimizer.optimize(params)
            return {
                "success": True,
                "optimization_result": result,
                "recommendations": [
                    f"Рекомендована система: {result.get('recommended_system', 'N/A')}",
                    f"Очікувана економія: {result.get('estimated_savings', 0):.2f}%",
                    f"Термін окупності: {result.get('payback_period', 'N/A')} років"
                ]
            }
        except Exception as e:
            return {"error": f"HVAC optimization failed: {e}"}

    async def _project_analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Аналіз проекту"""
        if not self.project_analyzer:
            return {"error": "Project analyzer not available"}
        
        try:
            result = self.project_analyzer.analyze_project(params["project_data"])
            return {
                "success": True,
                "analysis_result": result,
                "compliance_status": result.get("compliance_status", "unknown"),
                "recommendations": result.get("recommendations", [])
            }
        except Exception as e:
            return {"error": f"Project analysis failed: {e}"}

    async def _cost_optimize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Оптимізація вартості"""
        if not self.cost_optimizer:
            return {"error": "Cost optimizer not available"}
        
        try:
            result = self.cost_optimizer.analyze_costs(params["project_data"])
            return {
                "success": True,
                "cost_analysis": result,
                "total_cost": result.get("total_cost_usd", 0),
                "potential_savings": result.get("potential_savings_usd", 0),
                "suggestions": result.get("suggestions", [])
            }
        except Exception as e:
            return {"error": f"Cost optimization failed: {e}"}

    async def _material_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Пошук матеріалів"""
        if not self.vector_db:
            return {"error": "Vector database not available"}
        
        try:
            query = params["query"]
            max_cost = params.get("max_cost")
            top_k = params.get("top_k", 5)
            
            results = self.vector_db.search(query, top_k=top_k)
            
            # Фільтрація за ціною якщо вказано
            if max_cost:
                filtered_results = []
                for result in results:
                    cost = result.get("metadata", {}).get("cost_usd", 0)
                    if cost <= max_cost:
                        filtered_results.append(result)
                results = filtered_results
            
            return {
                "success": True,
                "search_results": results,
                "total_found": len(results)
            }
        except Exception as e:
            return {"error": f"Material search failed: {e}"}

    async def _procurement_analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Аналіз закупівель"""
        if not self.procurement_service:
            return {"error": "Procurement service not available"}
        
        try:
            result = await self.procurement_service.analyze_procurement(params["project_data"])
            return {
                "success": True,
                "procurement_analysis": result,
                "supplier_options": result
            }
        except Exception as e:
            return {"error": f"Procurement analysis failed: {e}"}

    async def _crm_sync(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Синхронізація з CRM"""
        if not self.crm_service:
            return {"error": "CRM service not available"}
        
        try:
            direction = params["direction"]
            if direction == "push":
                projects = params.get("projects", [])
                result = self.crm_service.sync_projects_push(projects)
            else:
                project_ids = params.get("project_ids")
                result = self.crm_service.sync_projects_pull(project_ids)
            
            return {
                "success": True,
                "sync_result": result
            }
        except Exception as e:
            return {"error": f"CRM sync failed: {e}"}

    async def _get_project_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Отримання статусу проектів"""
        try:
            # Тут можна додати логіку отримання статусу з бази даних
            project_ids = params.get("project_ids", [])
            
            # Заглушка для демонстрації
            status_info = {
                "projects_checked": len(project_ids),
                "status": "All systems operational",
                "services": {
                    "hvac_optimizer": self.hvac_optimizer is not None,
                    "vector_db": self.vector_db is not None,
                    "cost_optimizer": self.cost_optimizer is not None,
                    "project_analyzer": self.project_analyzer is not None,
                    "procurement_service": self.procurement_service is not None,
                    "crm_service": self.crm_service is not None
                }
            }
            
            return {
                "success": True,
                "status_info": status_info
            }
        except Exception as e:
            return {"error": f"Status check failed: {e}"}

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
            
            # Розширюємо дані залежно від типу аналізу
            if analysis_type == "detailed":
                hvac_data["analysis_depth"] = "detailed"
                hvac_data["include_economics"] = True
                hvac_data["include_compliance"] = True
            elif analysis_type == "compliance":
                hvac_data["analysis_depth"] = "compliance"
                hvac_data["focus_on_dbn"] = True
            
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
                
                # Використовуємо перший доступний
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
        hvac_ai_test = await server.execute_tool("ai_hvac_analyze", {
            "hvac_data": test_params,
            "analysis_type": "basic"
        })
        if hvac_ai_test.get("success"):
            print(f"✅ AI HVAC analysis test passed with {hvac_ai_test.get('provider_used', 'unknown')}")
        else:
            print(f"❌ AI HVAC analysis test failed: {hvac_ai_test.get('error')}")
    
    # Тест статусу
    status_result = await server.execute_tool("get_project_status", {})
    if status_result.get("success"):
        print("✅ Status check test passed")
        services = status_result["status_info"]["services"]
        for service, available in services.items():
            status = "✅" if available else "❌"
            print(f"  {status} {service}")
    
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
    
    # Додавання HTTP сервера для health checks та статусу
    print(f"\n🌐 Starting HTTP server on {server.host}:{server.port}")
    
    # Простий HTTP сервер для health checks
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading
    import json
    
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Get capabilities from server
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                caps = loop.run_until_complete(server.get_capabilities())
                loop.close()
                
                health_status = {
                    "status": "healthy",
                    "mcp_server": "running",
                    "ai_providers": server.ai_manager.get_available_providers(),
                    "capabilities": len(caps['tools']),
                    "timestamp": asyncio.get_event_loop().time()
                }
                self.wfile.write(json.dumps(health_status, indent=2).encode())
            elif self.path == '/status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                # Запускаємо асинхронний метод в синхронному контексті
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                status_info = loop.run_until_complete(server.execute_tool("get_project_status", {}))
                ai_info = loop.run_until_complete(server.execute_tool("ai_providers_status", {}))
                loop.close()
                
                combined_status = {
                    "project_status": status_info,
                    "ai_providers": ai_info,
                    "server_info": {
                        "host": server.host,
                        "port": server.port,
                        "project_root": server.project_root
                    }
                }
                self.wfile.write(json.dumps(combined_status, indent=2).encode())
            elif self.path == '/capabilities':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Get capabilities from server
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                caps = loop.run_until_complete(server.get_capabilities())
                loop.close()
                
                self.wfile.write(json.dumps(caps, indent=2).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {"error": "Not found", "available_endpoints": ["/health", "/status", "/capabilities"]}
                self.wfile.write(json.dumps(error_response).encode())
        
        def log_message(self, format, *args):
            # Логуємо тільки важливі запити
            if "health" not in self.path:
                logger.info(f"HTTP {self.command} {self.path}")
    
    # Запуск HTTP сервера в окремому потоці
    try:
        httpd = HTTPServer((server.host, server.port), HealthHandler)
        http_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        http_thread.start()
        
        print(f"🔗 Health endpoint: http://{server.host}:{server.port}/health")
        print(f"📊 Status endpoint: http://{server.host}:{server.port}/status")
        print(f"🛠  Capabilities endpoint: http://{server.host}:{server.port}/capabilities")
        
    except Exception as e:
        logger.error(f"Failed to start HTTP server: {e}")
        print("⚠️  HTTP server not available, but MCP functionality remains active")

    # Очікування (у реальному MCP сервері тут був би основний цикл)
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 VentAI MCP Server shutting down...")
        try:
            httpd.shutdown()
            print("🔌 HTTP server stopped")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())
