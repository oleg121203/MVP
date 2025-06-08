#!/usr/bin/env python3
"""
VentAI API Routes - трансформація MCP функціональності у веб-API
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
from mcp_ai_providers import AIProviderManager

# Ініціалізуємо AI провайдери (ті самі, що й в MCP)
ai_manager = AIProviderManager()

router = APIRouter(prefix="/api/v1", tags=["HVAC AI"])

# Pydantic моделі для API
class HVACAnalysisRequest(BaseModel):
    area: float
    occupancy: int
    climate_zone: str
    current_system: Optional[str] = None
    building_type: Optional[str] = "office"

class HVACAnalysisResponse(BaseModel):
    success: bool
    analysis: Dict[str, Any]
    provider_used: str
    recommendations: List[str]
    error: Optional[str] = None

class AIPromptRequest(BaseModel):
    prompt: str
    context: Optional[Dict[str, Any]] = None
    preferred_provider: Optional[str] = None

@router.on_event("startup")
async def initialize_ai_providers():
    """Ініціалізація AI провайдерів при старті сервера"""
    print("🤖 Initializing AI providers for production...")
    results = await ai_manager.initialize_all()
    
    available = ai_manager.get_available_providers()
    print(f"✅ Available AI providers: {available}")
    
    if not available:
        print("⚠️  Warning: No AI providers available!")

@router.post("/hvac/analyze", response_model=HVACAnalysisResponse)
async def analyze_hvac_system(request: HVACAnalysisRequest):
    """
    Аналіз HVAC системи - та сама логіка, що була в MCP
    """
    try:
        # Перетворюємо запит у формат для AI провайдера
        hvac_data = {
            "area": request.area,
            "occupancy": request.occupancy,
            "climate_zone": request.climate_zone,
            "current_system": request.current_system,
            "building_type": request.building_type
        }
        
        # Використовуємо ту саму логіку, що й в MCP сервері
        available_providers = ai_manager.get_available_providers()
        if not available_providers:
            raise HTTPException(status_code=503, detail="No AI providers available")
        
        # Беремо перший доступний провайдер
        provider_name = available_providers[0]
        result = await ai_manager.analyze_hvac_with_provider(provider_name, hvac_data)
        
        return HVACAnalysisResponse(
            success=True,
            analysis=result,
            provider_used=provider_name,
            recommendations=result.get("recommendations", [])
        )
        
    except Exception as e:
        return HVACAnalysisResponse(
            success=False,
            analysis={},
            provider_used="none",
            recommendations=[],
            error=str(e)
        )

@router.post("/ai/generate")
async def ai_generate(request: AIPromptRequest):
    """
    Генерація AI відповіді - еквівалент MCP ai_generate
    """
    try:
        # Додаємо VentAI контекст
        ventai_context = {
            "system_info": "Ти AI експерт VentAI для HVAC систем в Україні. Знаєш ДБН В.2.5-67:2013.",
            **(request.context or {})
        }
        
        # Використовуємо fallback логіку
        if request.preferred_provider:
            response = await ai_manager.generate_with_provider(
                request.preferred_provider, 
                request.prompt, 
                ventai_context
            )
            return {
                "success": True,
                "response": response,
                "provider_used": request.preferred_provider
            }
        else:
            return await ai_manager.generate_with_fallback(
                request.prompt, 
                ventai_context
            )
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": ""
        }

@router.get("/ai/providers/status")
async def ai_providers_status():
    """
    Статус AI провайдерів - еквівалент MCP ai_providers_status
    """
    try:
        available_providers = ai_manager.get_available_providers()
        all_providers = list(ai_manager.providers.keys())
        
        provider_details = {}
        for name, provider in ai_manager.providers.items():
            provider_details[name] = {
                "available": provider.is_available,
                "name": provider.name
            }
            
            if hasattr(provider, 'model'):
                provider_details[name]["model"] = provider.model
                
        return {
            "success": True,
            "status": {
                "total_providers": len(all_providers),
                "available_providers": len(available_providers),
                "primary_provider": ai_manager.primary_provider,
                "providers": provider_details
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/ai/providers")
async def get_available_providers():
    """Список доступних AI провайдерів"""
    return {
        "providers": ai_manager.get_available_providers(),
        "primary": ai_manager.primary_provider
    }

# Для зворотної сумісності з існуючим кодом
@router.post("/chat")
async def chat_with_ai_endpoint(prompt: str):
    """
    Простий чат endpoint для сумісності
    """
    try:
        result = await ai_manager.generate_with_fallback(
            prompt,
            {"system_info": "Ти AI експерт VentAI для HVAC систем в Україні."}
        )
        
        if result.get("success"):
            return {
                "reply": result["response"],
                "suggestions": ["Перевірте енергоефективність системи"],
                "provider": result.get("provider_used")
            }
        else:
            return {
                "reply": f"Помилка AI: {result.get('error')}",
                "suggestions": ["Спробуйте пізніше"],
                "provider": "none"
            }
            
    except Exception as e:
        return {
            "reply": f"Системна помилка: {str(e)}",
            "suggestions": ["Зверніться до адміністратора"],
            "provider": "none"
        }
