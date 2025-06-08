#!/usr/bin/env python3
"""
VentAI Development Environment Test
Tests if the development setup is working correctly in Universal dev-container.
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
    
    # Test FastAPI import (globally installed)
    try:
        import fastapi
        print("✅ FastAPI available")
        return True
    except ImportError:
        print("❌ FastAPI not available - run setup")
        return False

def test_node_env():
    """Test Node.js environment"""
    print("\n📱 Node.js Environment Test")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
        else:
            print("❌ Node.js not available")
            return False
            
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ NPM version: {result.stdout.strip()}")
            return True
        else:
            print("❌ NPM not available")
            return False
    except FileNotFoundError:
        print("❌ Node.js/NPM not found")
        return False

def test_frontend_deps():
    """Test frontend dependencies"""
    print("\n📦 Frontend Dependencies Test")
    
    if not Path("frontend").exists():
        print("❌ Frontend directory not found")
        return False
        
    node_modules = Path("frontend/node_modules")
    if node_modules.exists():
        print("✅ node_modules exists")
        
        # Check for key packages (React app, not Next.js)
        key_packages = ["react", "react-dom", "react-scripts"]
        for package in key_packages:
            package_path = node_modules / package
            if package_path.exists():
                print(f"✅ {package} installed")
            else:
                print(f"❌ {package} missing")
                return False
        return True
    else:
        print("❌ node_modules not found")
        return False

def test_env_files():
    """Test environment files"""
    print("\n📄 Environment Files Test")
    
    backend_env = Path("backend/.env")
    if backend_env.exists():
        print("✅ Backend .env exists")
    else:
        print("❌ Backend .env missing")
        return False
    
    frontend_env = Path("frontend/.env.local")
    if frontend_env.exists():
        print("✅ Frontend .env.local exists")
    else:
        print("❌ Frontend .env.local missing")
        return False
    
    return True

def test_backend_structure():
    """Test backend structure"""
    print("\n🔧 Backend Structure Test")
    
    if not Path("backend").exists():
        print("❌ Backend directory not found")
        return False
        
    required_files = [
        "backend/requirements.txt"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    # Check if main.py exists
    main_py = Path("backend/main.py")
    if main_py.exists():
        print("✅ backend/main.py exists")
    else:
        print("⚠️  backend/main.py missing (will be created)")
    
    return True

def main():
    """Run all tests"""
    print("🔍 VentAI Universal Dev-Container Environment Test")
    print("=================================================")
    
    # Change to project root
    os.chdir(Path(__file__).parent)
    
    tests = [
        test_python_env,
        test_node_env,
        test_backend_structure,
        test_frontend_deps,
        test_env_files
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
        print("1. Run: npm run dev")
        print("2. Open: http://localhost:3000 (Frontend)")
        print("3. Check API: http://localhost:8000/docs (Backend)")
    else:
        print("❌ Some tests failed. Please run setup.")
        print("\nSetup commands:")
        print("1. Run: bash .devcontainer/setup.sh")
        print("2. Or rebuild dev-container")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
