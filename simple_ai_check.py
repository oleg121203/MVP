#!/usr/bin/env python3
"""
Спрощений тест існування AI файлів
"""

import sys
from pathlib import Path

def test_files():
    """Перевіряє існування всіх AI файлів"""
    print("🔄 Перевірка AI файлів...")
    
    base_path = Path(__file__).parent
    
    # Backend файли
    backend_files = [
        "backend/mcp_ai_providers.py",
        "backend/api_routes.py", 
        "backend/main.py"
    ]
    
    # Frontend AI файли
    frontend_files = [
        "frontend/src/services/aiService.js",
        "frontend/src/components/ai/AIEnhancedCalculator.jsx",
        "frontend/src/components/ai/SimpleAIWrapper.jsx",
        "frontend/src/components/ai/AIComponents.css",
        "frontend/src/hooks/useAICalculator.js"
    ]
    
    # Калькулятори
    calculator_files = [
        "frontend/src/pages/DuctAreaCalculator.js",
        "frontend/src/pages/AirExchangeCalculator.js",
        "frontend/src/pages/DuctSizingCalculator.js", 
        "frontend/src/pages/PressureDropCalculator.js",
        "frontend/src/pages/AcousticCalculator.js",
        "frontend/src/pages/WaterHeaterCalculator.js",
        "frontend/src/pages/SmokeRemovalCalculator.js"
    ]
    
    all_files = backend_files + frontend_files + calculator_files
    
    missing_files = []
    
    for file_path in all_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return missing_files

def main():
    print("🚀 ПЕРЕВІРКА AI ІНТЕГРАЦІЇ VENTAI")
    print("=" * 40)
    
    missing = test_files()
    
    if not missing:
        print("\n🎉 Всі файли AI інтеграції присутні!")
        print("✨ VentAI система готова до використання")
        
        # Додаткова перевірка AI імпортів в калькуляторах
        print("\n🔄 Перевірка AI імпортів в калькуляторах...")
        check_ai_imports()
        
    else:
        print(f"\n❌ Відсутні файли: {len(missing)}")
        for file in missing:
            print(f"  - {file}")

def check_ai_imports():
    """Перевіряє AI імпорти в калькуляторах"""
    base_path = Path(__file__).parent
    pages_path = base_path / "frontend" / "src" / "pages"
    
    calculators = [
        "DuctAreaCalculator.js",
        "AirExchangeCalculator.js",
        "DuctSizingCalculator.js",
        "PressureDropCalculator.js", 
        "AcousticCalculator.js",
        "WaterHeaterCalculator.js",
        "SmokeRemovalCalculator.js"
    ]
    
    for calc in calculators:
        calc_path = pages_path / calc
        if calc_path.exists():
            try:
                content = calc_path.read_text(encoding='utf-8')
                has_ai = "SimpleAIWrapper" in content or "AIEnhancedCalculator" in content
                print(f"{'✅' if has_ai else '❌'} {calc} - AI інтеграція: {'Так' if has_ai else 'Ні'}")
            except Exception as e:
                print(f"⚠️  {calc} - помилка читання: {e}")

if __name__ == "__main__":
    main()
