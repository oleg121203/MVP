from fastapi import APIRouter
from ..ai.optimization_service import HVACOptimizer
from pydantic import BaseModel

router = APIRouter()
optimizer = HVACOptimizer()

# Placeholder for AI provider manager (to be properly initialized from main.py)
try:
    from ...main import get_ai_providers_status
except ImportError:
    def get_ai_providers_status():
        return [{'name': 'ollama', 'available': True, 'model': 'llama3.1'}]

# Attempt to import Ollama client for actual NLP processing
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

class ChatRequest(BaseModel):
    message: str


class OptimizationRequest(BaseModel):
    area: float
    occupancy: int
    climate_zone: str
    current_system: str


@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """Handle natural language HVAC queries"""
    # Connect to actual NLP model via MCP server's AI provider
    ai_providers = get_ai_providers_status()
    available_providers = [p for p in ai_providers if p['available']]
    
    if not available_providers:
        return {"reply": "No AI provider available for analysis.", "suggestions": []}
    
    provider = available_providers[0]
    
    # If Ollama is available, attempt to use it for real NLP processing
    if OLLAMA_AVAILABLE and provider['name'] == 'ollama':
        try:
            client = ollama.Client(host='http://host.docker.internal:11434')
            # Check available models with safer parsing and log raw response for debugging
            list_response = client.list()
            # Log the raw response to understand its structure
            raw_response_str = str(list_response)
            models = list_response.get('models', [])
            model_names = []
            full_model_names = []
            for m in models:
                # Handle different possible structures of model data
                if hasattr(m, 'model'):
                    full_name = m.model
                    full_model_names.append(full_name)
                    model_name = full_name.split(':')[0] if ':' in full_name else full_name
                    model_names.append(model_name)
                elif isinstance(m, dict):
                    if 'model' in m:
                        full_name = m['model']
                        full_model_names.append(full_name)
                        model_name = full_name.split(':')[0] if ':' in full_name else full_name
                        model_names.append(model_name)
                    elif 'name' in m:
                        full_name = m['name']
                        full_model_names.append(full_name)
                        model_name = full_name.split(':')[0] if ':' in full_name else full_name
                        model_names.append(model_name)
                    elif 'id' in m:
                        full_name = m['id']
                        full_model_names.append(full_name)
                        model_name = full_name.split(':')[0] if ':' in full_name else full_name
                        model_names.append(model_name)
                elif isinstance(m, str):
                    full_name = m
                    full_model_names.append(full_name)
                    model_name = m.split(':')[0] if ':' in m else m
                    model_names.append(model_name)
            # Check if provider model matches either normalized or full name
            matched_model = None
            for full_name in full_model_names:
                if provider['model'] == full_name or provider['model'] in full_name:
                    matched_model = full_name
                    break
            if not matched_model:
                for name in model_names:
                    if provider['model'] == name:
                        matched_model = name
                        break
            # Debug explicit check for llama3.1 in any name
            debug_info = f"Checking for {provider['model']} in models. Normalized: {', '.join(model_names) if model_names else 'None'}, Full: {', '.join(full_model_names) if full_model_names else 'None'}"
            if not matched_model:
                # Last resort: check if the provider model is a substring of any full name
                for full_name in full_model_names:
                    if provider['model'] in full_name:
                        matched_model = full_name
                        debug_info += f"; Found {provider['model']} in {full_name}"
                        break
            if not matched_model:
                return {
                    "reply": f"Model {provider['model']} not found in Ollama. {debug_info}. Raw response: {raw_response_str[:200]}...",
                    "suggestions": []
                }
            response = client.chat(model=matched_model, messages=[
                {
                    'role': 'user',
                    'content': f"Analyze this HVAC query: {request.message}"
                }
            ])
            reply = response['message']['content'] if response['message']['content'] else "No meaningful response from AI."
            return {
                "reply": reply,
                "suggestions": ["Check HVAC system efficiency", "Consider climate zone adjustments"]
            }
        except Exception as e:
            return {
                "reply": f"Failed to connect to Ollama or process request: {str(e)}",
                "suggestions": []
            }
    else:
        # Fallback to simulated response if Ollama is not installed or provider is different
        return {
            "reply": f"AI analysis from {provider['name']} for: {request.message}",
            "suggestions": ["Check HVAC system efficiency", "Consider climate zone adjustments"]
        }


@router.post("/optimize")
async def optimize_system(request: OptimizationRequest):
    """Run HVAC optimization"""
    params = {
        "area": request.area,
        "occupancy": request.occupancy,
        "climate_zone": request.climate_zone,
        "current_system_type": request.current_system,
    }
    return optimizer.optimize(params)
