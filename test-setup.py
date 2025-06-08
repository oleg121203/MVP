#!/usr/bin/env python3
"""
VentAI Development Environment Test
Tests if the minimal development setup is working correctly.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def test_python_env():
    """Test Python environment"""
    print("🐍 Python Environment Test")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    return True

def test_backend_venv():
    """Test backend virtual environment"""
    print("\n🔧 Backend Virtual Environment Test")
    venv_path = Path("backend/venv")
    if venv_path.exists():
        print("✅ Virtual environment exists")
        
        # Check if we can activate and run basic imports
        activate_script = venv_path / "bin" / "activate"
        if activate_script.exists():
            print("✅ Activation script exists")
        else:
            print("❌ Activation script missing")
            return False
            
        # Try to test basic imports
        python_path = venv_path / "bin" / "python"
        if python_path.exists():
            print("✅ Python interpreter in venv exists")
            try:
                result = subprocess.run([str(python_path), "-c", "import fastapi; print('FastAPI available')"], 
                                     capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print("✅ FastAPI available in venv")
                else:
                    print(f"❌ FastAPI import failed: {result.stderr}")
                    return False
            except Exception as e:
                print(f"❌ Error testing FastAPI: {e}")
                return False
        else:
            print("❌ Python interpreter not found in venv")
            return False
    else:
        print("❌ Virtual environment not found")
        return False
    
    return True

def test_frontend_deps():
    """Test frontend dependencies"""
    print("\n📱 Frontend Dependencies Test")
    node_modules = Path("frontend/node_modules")
    if node_modules.exists():
        print("✅ node_modules exists")
        
        # Check for key packages
        key_packages = ["react", "next", "@types/react"]
        for package in key_packages:
            package_path = node_modules / package
            if package_path.exists():
                print(f"✅ {package} installed")
            else:
                print(f"❌ {package} missing")
                return False
    else:
        print("❌ node_modules not found")
        return False
    
    return True

def test_env_files():
    """Test environment files"""
    print("\n📄 Environment Files Test")
    
    backend_env = Path("backend/.env.minimal")
    if backend_env.exists():
        print("✅ Backend .env.minimal exists")
    else:
        print("❌ Backend .env.minimal missing")
        return False
    
    frontend_env = Path("frontend/.env.local")
    if frontend_env.exists():
        print("✅ Frontend .env.local exists")
    else:
        print("❌ Frontend .env.local missing")
        return False
    
    return True

def test_docker_config():
    """Test Docker configuration"""
    print("\n🐳 Docker Configuration Test")
    
    docker_compose = Path("infra/docker/docker-compose.dev.yml")
    if docker_compose.exists():
        print("✅ Docker Compose file exists")
    else:
        print("❌ Docker Compose file missing")
        return False
    
    docker_env = Path("infra/docker/.env")
    if docker_env.exists():
        print("✅ Docker .env file exists")
    else:
        print("❌ Docker .env file missing")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🔍 VentAI Development Environment Test")
    print("=====================================")
    
    # Change to project root
    os.chdir(Path(__file__).parent)
    
    tests = [
        test_python_env,
        test_backend_venv,
        test_frontend_deps,
        test_env_files,
        test_docker_config
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n📊 Test Results Summary")
    print("======================")
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Development environment is ready.")
        print("\nNext steps:")
        print("1. Run: ./start-minimal-dev.sh")
        print("2. Open: http://localhost:3000")
        print("3. Check API: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the setup.")
        print("\nTroubleshooting:")
        print("1. Run: ./setup-minimal-dev.sh")
        print("2. Check logs for any error messages")
        print("3. Try Docker alternative: ./scripts/start-dev-environment.sh")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
