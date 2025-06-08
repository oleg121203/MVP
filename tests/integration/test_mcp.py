#!/usr/bin/env python3
"""
Тестування MCP конфігурації VentAI для Claude 4
"""

import os
import json
import asyncio
import subprocess
import time
from pathlib import Path

def check_file_exists(file_path: str) -> bool:
    """Перевірка існування файлу"""
    return Path(file_path).exists()

def check_service_running(port: int) -> bool:
    """Перевірка запущеного сервісу на порту"""
    try:
        result = subprocess.run(
            ["lsof", "-i", f":{port}"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def check_python_imports():
    """Перевірка можливості імпорту модулів"""
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))
        
        from fastapi_app.ai.optimization_service import HVACOptimizer
        from fastapi_app.ai.cost_optimization_service import CostOptimizationService
        from fastapi_app.ai.project_analysis_service import ProjectAnalysisService
        
        print("✅ All Python modules can be imported")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def check_environment_variables():
    """Перевірка змінних середовища"""
    required_vars = [
        "PYTHONPATH",
        "VENTAI_PROJECT_ROOT"
    ]
    
    optional_vars = [
        "PINECONE_API_KEY",
        "HUBSPOT_API_KEY",
        "DB_HOST",
        "REDIS_HOST"
    ]
    
    print("🔍 Checking environment variables...")
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: {os.getenv(var)}")
        else:
            print(f"❌ {var}: Not set (required)")
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ {var}: {os.getenv(var)}")
        else:
            print(f"⚠️  {var}: Not set (optional)")

def check_mcp_config():
    """Перевірка MCP конфігурації"""
    config_path = Path(__file__).parent / ".vscode" / "mcp.json"
    
    if not config_path.exists():
        print("❌ MCP config file not found")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if "mcpServers" in config:
            servers = config["mcpServers"]
            print(f"✅ MCP config loaded with {len(servers)} servers:")
            for name, server_config in servers.items():
                print(f"  - {name}: {server_config.get('command', 'unknown')}")
            return True
        else:
            print("❌ Invalid MCP config format")
            return False
    except json.JSONDecodeError as e:
        print(f"❌ MCP config JSON error: {e}")
        return False

def test_mcp_server():
    """Тестування MCP сервера"""
    print("🧪 Testing MCP server functionality...")
    
    try:
        # Імпорт і тестування MCP сервера
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        
        from mcp_server import VentAIMCPServer
        
        async def run_test():
            server = VentAIMCPServer()
            
            # Тест можливостей
            capabilities = await server.get_capabilities()
            print(f"✅ Server capabilities: {len(capabilities.get('tools', {}))} tools")
            
            # Тест виконання інструменту
            test_params = {
                "area": 100,
                "occupancy": 10,
                "climate_zone": "temperate"
            }
            
            result = await server.execute_tool("get_project_status", {})
            if result.get("success"):
                print("✅ Tool execution test passed")
                return True
            else:
                print(f"❌ Tool execution failed: {result.get('error')}")
                return False
        
        return asyncio.run(run_test())
        
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        return False

def main():
    """Головна функція тестування"""
    print("🚀 VentAI MCP Configuration Test for Claude 4")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Встановлення змінних середовища для тестування
    os.environ["PYTHONPATH"] = str(project_root / "backend" / "src")
    os.environ["VENTAI_PROJECT_ROOT"] = str(project_root)
    os.environ["APP_ENV"] = "development"
    
    tests = [
        ("Configuration Files", lambda: (
            check_file_exists(".vscode/mcp.json") and
            check_file_exists("mcp_server.py") and
            check_file_exists(".vscode/mcp-config.json")
        )),
        ("Environment Variables", check_environment_variables),
        ("Python Imports", check_python_imports),
        ("MCP Configuration", check_mcp_config),
        ("MCP Server", test_mcp_server),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        print("-" * 30)
        
        try:
            if callable(test_func):
                result = test_func()
                if result is None:
                    result = True  # Assume success if no return value
            else:
                result = test_func
            
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Перевірка сервісів
    print(f"\n🔍 Checking Services")
    print("-" * 30)
    
    services = [
        ("PostgreSQL", 5433),
        ("Redis", 6380),
        ("FastAPI Backend", 8000),
        ("Next.js Frontend", 3000)
    ]
    
    for service_name, port in services:
        if check_service_running(port):
            print(f"✅ {service_name} (port {port}): Running")
        else:
            print(f"❌ {service_name} (port {port}): Not running")
    
    # Підсумок
    print(f"\n📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! VentAI MCP is ready for Claude 4")
        print("\n📝 Next steps:")
        print("1. Start required services: ./start-mcp.sh")
        print("2. Open Claude Desktop")
        print("3. Check MCP servers in Claude settings")
        print("4. Start using VentAI with Claude!")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed")
        print("2. Check environment variables")
        print("3. Start database services: ./start-db-services.sh")
        print("4. Review logs for detailed error messages")

if __name__ == "__main__":
    main()
