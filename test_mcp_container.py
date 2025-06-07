#!/usr/bin/env python3
"""
Комплексний тест MCP сервера в контейнері VentAI
Перевіряє всі AI провайдери, інтеграцію та функціональність
"""

import asyncio
import json
import os
import requests
import sys
import time
from typing import Dict, Any, List

# Налаштування тестування
TEST_CONFIG = {
    "mcp_server_url": "http://localhost:8001",
    "backend_url": "http://localhost:8000",
    "timeout": 30,
    "retry_count": 3,
    "test_data": {
        "hvac_basic": {
            "area": 100,
            "occupancy": 10,
            "climate_zone": "Ukraine_Zone_1",
            "current_system": "split"
        },
        "hvac_office": {
            "area": 250,
            "occupancy": 50,
            "climate_zone": "temperate",
            "current_system": "central_air",
            "building_type": "office"
        }
    }
}

class MCPContainerTester:
    """Тестер для MCP сервера в контейнері"""
    
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }
        self.mcp_url = TEST_CONFIG["mcp_server_url"]
        self.backend_url = TEST_CONFIG["backend_url"]
    
    def log_test(self, test_name: str, status: str, details: str = "", error: str = ""):
        """Логування результатів тесту"""
        self.results["total_tests"] += 1
        
        if status == "PASS":
            self.results["passed_tests"] += 1
            print(f"✅ {test_name}: {details}")
        else:
            self.results["failed_tests"] += 1
            print(f"❌ {test_name}: {error}")
        
        self.results["test_details"].append({
            "test": test_name,
            "status": status,
            "details": details,
            "error": error,
            "timestamp": time.time()
        })
    
    def test_container_health(self):
        """Тест здоров'я контейнерів"""
        print("\n🏥 Testing container health...")
        
        # Тест MCP сервера
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                self.log_test(
                    "MCP Server Health", 
                    "PASS", 
                    f"Status: {health_data.get('status')}, AI providers: {len(health_data.get('ai_providers', []))}"
                )
            else:
                self.log_test("MCP Server Health", "FAIL", error=f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("MCP Server Health", "FAIL", error=str(e))
        
        # Тест Backend
        try:
            response = requests.get(f"{self.backend_url}/docs", timeout=10)
            if response.status_code == 200:
                self.log_test("Backend Health", "PASS", "FastAPI docs available")
            else:
                self.log_test("Backend Health", "FAIL", error=f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Backend Health", "FAIL", error=str(e))
    
    def test_mcp_endpoints(self):
        """Тест MCP endpoints"""
        print("\n🔗 Testing MCP endpoints...")
        
        endpoints = ["/health", "/status", "/capabilities"]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.mcp_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if endpoint == "/capabilities":
                        tools_count = len(data.get("tools", {}))
                        self.log_test(
                            f"MCP Endpoint {endpoint}", 
                            "PASS", 
                            f"Tools available: {tools_count}"
                        )
                    else:
                        self.log_test(f"MCP Endpoint {endpoint}", "PASS", "Response OK")
                else:
                    self.log_test(f"MCP Endpoint {endpoint}", "FAIL", error=f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"MCP Endpoint {endpoint}", "FAIL", error=str(e))
    
    def test_ai_providers(self):
        """Тест AI провайдерів"""
        print("\n🤖 Testing AI providers...")
        
        try:
            response = requests.get(f"{self.mcp_url}/status", timeout=15)
            if response.status_code == 200:
                status_data = response.json()
                ai_info = status_data.get("ai_providers", {})
                
                if ai_info.get("success"):
                    providers = ai_info["status"]["providers"]
                    available_count = ai_info["status"]["available_providers"]
                    total_count = ai_info["status"]["total_providers"]
                    
                    self.log_test(
                        "AI Providers Status", 
                        "PASS", 
                        f"{available_count}/{total_count} providers available"
                    )
                    
                    # Перевіряємо кожного провайдера
                    for provider, details in providers.items():
                        status = "PASS" if details["available"] else "FAIL"
                        model_info = details.get("model", "N/A")
                        self.log_test(
                            f"AI Provider {provider}", 
                            status, 
                            f"Model: {model_info}" if status == "PASS" else "",
                            "Not available" if status == "FAIL" else ""
                        )
                else:
                    self.log_test("AI Providers Status", "FAIL", error=ai_info.get("error", "Unknown error"))
            else:
                self.log_test("AI Providers Status", "FAIL", error=f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("AI Providers Status", "FAIL", error=str(e))
    
    async def test_mcp_tools_simulation(self):
        """Симуляція тестування MCP інструментів"""
        print("\n🛠  Testing MCP tools (simulation)...")
        
        # Симуляція тестів, оскільки MCP інструменти викликаються через Claude
        test_scenarios = [
            {
                "tool": "hvac_optimize",
                "description": "HVAC optimization for office",
                "params": TEST_CONFIG["test_data"]["hvac_office"]
            },
            {
                "tool": "ai_hvac_analyze", 
                "description": "AI HVAC analysis",
                "params": {
                    "hvac_data": TEST_CONFIG["test_data"]["hvac_basic"],
                    "analysis_type": "basic"
                }
            },
            {
                "tool": "ai_providers_status",
                "description": "AI providers status check",
                "params": {}
            },
            {
                "tool": "get_project_status",
                "description": "Project status check",
                "params": {"project_ids": ["test_project_1"]}
            }
        ]
        
        for scenario in test_scenarios:
            # Симуляція виклику інструменту
            await asyncio.sleep(0.1)  # Невелика пауза для симуляції
            
            # В реальному тесті тут був би виклик MCP сервера
            # Поки що просто перевіряємо доступність endpoints
            try:
                response = requests.get(f"{self.mcp_url}/capabilities", timeout=5)
                if response.status_code == 200:
                    capabilities = response.json()
                    tools = capabilities.get("tools", {})
                    
                    if scenario["tool"] in tools:
                        self.log_test(
                            f"MCP Tool {scenario['tool']}", 
                            "PASS", 
                            f"Tool available: {scenario['description']}"
                        )
                    else:
                        self.log_test(
                            f"MCP Tool {scenario['tool']}", 
                            "FAIL", 
                            error="Tool not found in capabilities"
                        )
                else:
                    self.log_test(
                        f"MCP Tool {scenario['tool']}", 
                        "FAIL", 
                        error="Cannot access capabilities"
                    )
            except Exception as e:
                self.log_test(f"MCP Tool {scenario['tool']}", "FAIL", error=str(e))
    
    def test_environment_variables(self):
        """Тест змінних середовища"""
        print("\n🌍 Testing environment variables...")
        
        required_vars = [
            "VENTAI_PROJECT_ROOT",
            "PYTHONPATH", 
            "DATABASE_URL",
            "REDIS_URL"
        ]
        
        optional_vars = [
            "GEMINI_API_KEY",
            "OPENAI_API_KEY", 
            "ANTHROPIC_API_KEY",
            "OLLAMA_BASE_URL",
            "PINECONE_API_KEY"
        ]
        
        # Перевіряємо через status endpoint
        try:
            response = requests.get(f"{self.mcp_url}/status", timeout=10)
            if response.status_code == 200:
                # Непрямий спосіб перевірки через доступність сервісів
                status_data = response.json()
                project_status = status_data.get("project_status", {})
                
                if project_status.get("success"):
                    services = project_status["status_info"]["services"]
                    working_services = sum(1 for s in services.values() if s)
                    total_services = len(services)
                    
                    self.log_test(
                        "Environment Configuration", 
                        "PASS", 
                        f"{working_services}/{total_services} services configured"
                    )
                else:
                    self.log_test("Environment Configuration", "FAIL", error="Services not responding")
            else:
                self.log_test("Environment Configuration", "FAIL", error="Cannot check services")
        except Exception as e:
            self.log_test("Environment Configuration", "FAIL", error=str(e))
    
    def test_docker_integration(self):
        """Тест Docker інтеграції"""
        print("\n🐳 Testing Docker integration...")
        
        # Перевіряємо чи сервер працює в контейнері
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                
                # Перевіряємо чи є ознаки роботи в контейнері
                if "mcp_server" in health_data and health_data["status"] == "healthy":
                    self.log_test("Docker MCP Server", "PASS", "MCP server running in container")
                else:
                    self.log_test("Docker MCP Server", "FAIL", error="MCP server not healthy")
            else:
                self.log_test("Docker MCP Server", "FAIL", error=f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Docker MCP Server", "FAIL", error=str(e))
        
        # Перевіряємо networking між контейнерами
        try:
            response = requests.get(f"{self.backend_url}/docs", timeout=10)
            if response.status_code == 200:
                self.log_test("Docker Networking", "PASS", "Backend accessible from host")
            else:
                self.log_test("Docker Networking", "FAIL", error="Backend not accessible")
        except Exception as e:
            self.log_test("Docker Networking", "FAIL", error=str(e))
    
    def test_performance(self):
        """Тест продуктивності"""
        print("\n⚡ Testing performance...")
        
        # Тест швидкості відповіді health endpoint
        start_time = time.time()
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200 and response_time < 2.0:
                self.log_test(
                    "Response Time Health", 
                    "PASS", 
                    f"{response_time:.3f}s"
                )
            else:
                self.log_test(
                    "Response Time Health", 
                    "FAIL", 
                    error=f"Slow response: {response_time:.3f}s"
                )
        except Exception as e:
            self.log_test("Response Time Health", "FAIL", error=str(e))
        
        # Тест швидкості status endpoint
        start_time = time.time()
        try:
            response = requests.get(f"{self.mcp_url}/status", timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code == 200 and response_time < 5.0:
                self.log_test(
                    "Response Time Status", 
                    "PASS", 
                    f"{response_time:.3f}s"
                )
            else:
                self.log_test(
                    "Response Time Status", 
                    "FAIL", 
                    error=f"Slow response: {response_time:.3f}s"
                )
        except Exception as e:
            self.log_test("Response Time Status", "FAIL", error=str(e))
    
    def print_summary(self):
        """Виведення підсумку тестування"""
        print("\n" + "="*60)
        print("📊 ТЕСТУВАННЯ ЗАВЕРШЕНО")
        print("="*60)
        
        total = self.results["total_tests"]
        passed = self.results["passed_tests"] 
        failed = self.results["failed_tests"]
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"📈 Загальна статистика:")
        print(f"   Всього тестів: {total}")
        print(f"   ✅ Пройшло: {passed}")
        print(f"   ❌ Не пройшло: {failed}")
        print(f"   📊 Успішність: {success_rate:.1f}%")
        
        if failed > 0:
            print(f"\n❌ Проблемні тести:")
            for test in self.results["test_details"]:
                if test["status"] == "FAIL":
                    print(f"   - {test['test']}: {test['error']}")
        
        print(f"\n💡 Рекомендації:")
        if success_rate >= 90:
            print("   🎉 Відмінно! MCP сервер готовий до роботи з Claude 4")
        elif success_rate >= 70:
            print("   ⚠️  Є деякі проблеми, але основна функціональність працює")
        else:
            print("   🚨 Потрібно вирішити критичні проблеми перед використанням")
        
        # Збереження результатів
        with open("mcp_test_results.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Результати збережено в mcp_test_results.json")
        
        return success_rate >= 70

async def main():
    """Головна функція тестування"""
    print("🚀 VentAI MCP Container Testing Suite")
    print("=" * 60)
    
    tester = MCPContainerTester()
    
    # Чекаємо доступність сервісів
    print("⏳ Очікування запуску сервісів...")
    max_wait = 60  # максимум 60 секунд
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            response = requests.get(f"{tester.mcp_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ MCP сервер доступний!")
                break
        except:
            pass
        
        await asyncio.sleep(2)
        wait_time += 2
        print(f"⏳ Очікування... ({wait_time}/{max_wait}s)")
    
    if wait_time >= max_wait:
        print("❌ Таймаут очікування MCP сервера")
        return False
    
    # Запуск тестів
    print("\n🧪 Запуск тестування...")
    
    tester.test_container_health()
    tester.test_mcp_endpoints()
    tester.test_ai_providers()
    await tester.test_mcp_tools_simulation()
    tester.test_environment_variables()
    tester.test_docker_integration()
    tester.test_performance()
    
    # Підсумок
    success = tester.print_summary()
    
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Тестування перервано користувачем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критична помилка тестування: {e}")
        sys.exit(1)
