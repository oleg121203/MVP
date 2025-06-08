#!/usr/bin/env python3
"""
AI Providers для VentAI MCP Server
Підтримка різних AI провайдерів: Ollama, Gemini, OpenAI, Anthropic
"""

import os
import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import asyncio

# Імпорт Redis для кешування (якщо доступний)
try:
    import redis
    import json
    import hashlib
    
    # Initialize Redis connection
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    CACHE_EXPIRY = 3600  # 1 година
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("Redis not available - caching disabled")

logger = logging.getLogger(__name__)

def generate_cache_key(query):
    """Генерує унікальний ключ кешу на основі запиту"""
    if not REDIS_AVAILABLE:
        return None
    query_str = json.dumps(query, sort_keys=True)
    return f"ai_cache:{hashlib.md5(query_str.encode()).hexdigest()}"

def get_cached_response(query):
    """Отримує відповідь з кешу"""
    if not REDIS_AVAILABLE:
        return None
    cache_key = generate_cache_key(query)
    try:
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception as e:
        logger.warning(f"Error retrieving from cache: {e}")
    return None

def set_cached_response(query, response):
    """Зберігає відповідь в кеш"""
    if not REDIS_AVAILABLE:
        return
    cache_key = generate_cache_key(query)
    try:
        redis_client.setex(cache_key, CACHE_EXPIRY, json.dumps(response))
    except Exception as e:
        logger.warning(f"Error setting cache: {e}")

class AIProvider(ABC):
    """Абстрактний клас для AI провайдерів"""
    
    def __init__(self, name: str):
        self.name = name
        self.is_available = False
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Ініціалізація провайдера"""
        pass
    
    @abstractmethod
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Генерація відповіді"""
        pass
    
    @abstractmethod
    async def analyze_hvac_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Аналіз HVAC даних"""
        pass

class OllamaProvider(AIProvider):
    """Провайдер для Ollama (локальний AI)"""
    
    def __init__(self):
        super().__init__("ollama")
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'llama3.1')
        self.client = None

    async def initialize(self) -> bool:
        """Ініціалізація Ollama клієнта"""
        try:
            # Спробуємо імпортувати ollama
            import ollama
            self.client = ollama.Client(host=self.base_url)
            
            # Перевірка доступності
            models = self.client.list()
            available_models = [m.model for m in models.models] if hasattr(models, 'models') else []
            
            if self.model not in available_models:
                logger.warning(f"Model {self.model} not found in Ollama. Available: {available_models}")
                # Спробуємо завантажити модель
                try:
                    self.client.pull(self.model)
                    logger.info(f"Successfully pulled {self.model}")
                except Exception as e:
                    logger.error(f"Failed to pull {self.model}: {e}")
                    return False
            
            self.is_available = True
            logger.info(f"✅ Ollama provider initialized with model {self.model}")
            return True
            
        except ImportError:
            logger.error("❌ Ollama package not installed")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to initialize Ollama: {e}")
            return False

    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Генерація відповіді через Ollama"""
        if not self.is_available:
            raise Exception("Ollama provider not available")
        
        try:
            # Додаємо контекст до промпту
            full_prompt = prompt
            if context and context.get('system_info'):
                full_prompt = f"Система: {context['system_info']}\n\nЗапит: {prompt}"
            
            response = self.client.generate(model=self.model, prompt=full_prompt)
            return response['response']
            
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise

    async def analyze_hvac_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Аналіз HVAC даних через Ollama"""
        prompt = f"""
        Проаналізуй HVAC систему для проекту в Україні:
        
        Дані: {data}
        
        Розрахуй згідно з ДБН В.2.5-67:2013 та поверни результат:
        - Рекомендована система
        - Потужність (кВт)
        - Орієнтовна вартість (USD)
        - Клас енергоефективності
        - Економія енергії (%)
        """
        
        response = await self.generate_response(prompt)
        return {
            "analysis": response,
            "provider": "ollama",
            "model": self.model
        }

class GeminiProvider(AIProvider):
    """Провайдер для Google Gemini"""
    
    def __init__(self):
        super().__init__("gemini")
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = os.getenv('GEMINI_MODEL', 'gemini-pro')
        self.client = None

    async def initialize(self) -> bool:
        """Ініціалізація Gemini клієнта"""
        if not self.api_key:
            logger.error("❌ GEMINI_API_KEY not found")
            return False
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
            
            # Тестовий запит
            response = self.client.generate_content("Hello")
            
            if response.text:
                self.is_available = True
                logger.info(f"✅ Gemini provider initialized with model {self.model}")
                return True
                
        except ImportError:
            logger.error("❌ Google AI package not installed")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {e}")
            return False
        
        return False

    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Генерація відповіді через Gemini"""
        if not self.is_available:
            raise Exception("Gemini provider not available")
        
        try:
            # Додаємо контекст
            full_prompt = prompt
            if context and context.get('system_info'):
                full_prompt = f"{context['system_info']}\n\n{prompt}"
            
            response = self.client.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise

    async def analyze_hvac_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Аналіз HVAC даних через Gemini"""
        prompt = f"""
        Експертний аналіз HVAC системи для України:
        
        Дані проекту: {data}
        
        Розрахуй за ДБН В.2.5-67:2013 та поверни JSON:
        {{
            "system_type": "рекомендована система",
            "capacity_kw": число,
            "cost_estimate_usd": число,
            "efficiency_class": "A+/A/B/C",
            "annual_savings": число_в_процентах,
            "recommendations": ["список рекомендацій"]
        }}
        """
        
        response = await self.generate_response(prompt)
        
        try:
            import json
            # Спробуємо витягти JSON з відповіді
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return {
            "analysis": response,
            "provider": "gemini",
            "model": self.model
        }

class OpenAIProvider(AIProvider):
    """Провайдер для OpenAI"""
    
    def __init__(self):
        super().__init__("openai")
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        self.client = None

    async def initialize(self) -> bool:
        """Ініціалізація OpenAI клієнта"""
        if not self.api_key:
            logger.error("❌ OPENAI_API_KEY not found")
            return False
        
        try:
            import openai
            self.client = openai.AsyncOpenAI(api_key=self.api_key)
            
            # Тестовий запит
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            
            if response.choices:
                self.is_available = True
                logger.info(f"✅ OpenAI provider initialized with model {self.model}")
                return True
                
        except ImportError:
            logger.error("❌ OpenAI package not installed")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI: {e}")
            return False
        
        return False

    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Генерація відповіді через OpenAI"""
        if not self.is_available:
            raise Exception("OpenAI provider not available")
        
        try:
            messages = []
            if context:
                system_msg = f"Ти AI асистент VentAI. {context.get('system_info', '')}"
                messages.append({"role": "system", "content": system_msg})
            
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise

    async def analyze_hvac_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Аналіз HVAC даних через OpenAI"""
        prompt = f"""
        Проаналізуй HVAC проект для України:
        
        Дані: {data}
        
        Розрахуй згідно з ДБН В.2.5-67:2013 і поверни результат у JSON:
        {{
            "recommended_system": "string",
            "required_capacity_kw": number,
            "estimated_cost_usd": number,
            "energy_class": "A+/A/B/C",
            "annual_savings_percent": number,
            "dbn_compliance": boolean,
            "recommendations": ["string"]
        }}
        """
        
        response = await self.generate_response(prompt)
        
        try:
            import json
            return json.loads(response)
        except:
            return {
                "analysis": response,
                "provider": "openai",
                "model": self.model
            }

class AnthropicProvider(AIProvider):
    """Провайдер для Anthropic Claude"""
    
    def __init__(self):
        super().__init__("anthropic")
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')
        self.client = None

    async def initialize(self) -> bool:
        """Ініціалізація Anthropic клієнта"""
        if not self.api_key:
            logger.error("❌ ANTHROPIC_API_KEY not found")
            return False
        
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
            
            # Тестовий запит
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello"}]
            )
            
            if response.content:
                self.is_available = True
                logger.info(f"✅ Anthropic provider initialized with model {self.model}")
                return True
                
        except ImportError:
            logger.error("❌ Anthropic package not installed")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to initialize Anthropic: {e}")
            return False
        
        return False

    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Генерація відповіді через Anthropic"""
        if not self.is_available:
            raise Exception("Anthropic provider not available")
        
        try:
            system_message = "Ти AI експерт VentAI для HVAC систем в Україні."
            if context:
                system_message += f" {context.get('system_info', '')}"
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.7,
                system=system_message,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            raise

    async def analyze_hvac_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Аналіз HVAC даних через Anthropic"""
        prompt = f"""
        Експертний аналіз HVAC системи для України:
        
        📋 Дані проекту:
        {data}
        
        🎯 Завдання:
        1. Розрахунок за ДБН В.2.5-67:2013
        2. Вибір оптимальної системи
        3. Оцінка енергоефективності
        4. Економічний розрахунок
        
        Результат у JSON:
        {{
            "system_recommendation": "детальна назва",
            "capacity_calculation": {{
                "required_kw": number,
                "peak_load_kw": number,
                "safety_factor": number
            }},
            "economic_analysis": {{
                "initial_cost_usd": number,
                "annual_operating_cost_usd": number,
                "savings_vs_baseline_percent": number,
                "payback_period_years": number
            }},
            "compliance": {{
                "dbn_67_2013": boolean,
                "energy_efficiency_class": "string",
                "co2_reduction_percent": number
            }},
            "detailed_recommendations": ["string"]
        }}
        """
        
        response = await self.generate_response(prompt)
        
        try:
            import json
            # Шукаємо JSON в відповіді
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return {
            "analysis": response,
            "provider": "anthropic",
            "model": self.model
        }

class AIProviderManager:
    """Менеджер AI провайдерів"""
    
    def __init__(self):
        self.providers: Dict[str, AIProvider] = {}
        self.primary_provider = None
        
    async def initialize_all(self) -> Dict[str, bool]:
        """Ініціалізація всіх провайдерів"""
        provider_classes = [
            OllamaProvider,
            GeminiProvider,
            OpenAIProvider,
            AnthropicProvider
        ]
        
        results = {}
        
        for provider_class in provider_classes:
            provider = provider_class()
            success = await provider.initialize()
            self.providers[provider.name] = provider
            results[provider.name] = success
            
            # Встановлюємо першого доступного як основного
            if success and not self.primary_provider:
                self.primary_provider = provider.name
        
        return results
    
    def get_available_providers(self) -> List[str]:
        """Отримання списку доступних провайдерів"""
        return [name for name, provider in self.providers.items() if provider.is_available]
    
    async def generate_with_provider(self, provider_name: str, prompt: str, context: Dict[str, Any] = None) -> str:
        """Генерація з конкретним провайдером"""
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not found")
        
        provider = self.providers[provider_name]
        if not provider.is_available:
            raise ValueError(f"Provider {provider_name} not available")
        
        return await provider.generate_response(prompt, context)
    
    async def analyze_hvac_with_provider(self, provider_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Аналіз HVAC з конкретним провайдером"""
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not found")
        
        provider = self.providers[provider_name]
        if not provider.is_available:
            raise ValueError(f"Provider {provider_name} not available")
        
        return await provider.analyze_hvac_data(data)
    
    async def generate_with_fallback(self, prompt: str, context: Dict[str, Any] = None, preferred_provider: str = None) -> Dict[str, Any]:
        """Генерація з fallback логікою"""
        providers_to_try = []
        
        # Спочатку спробуємо преферований провайдер
        if preferred_provider and preferred_provider in self.providers:
            providers_to_try.append(preferred_provider)
        
        # Потім основний провайдер
        if self.primary_provider and self.primary_provider not in providers_to_try:
            providers_to_try.append(self.primary_provider)
        
        # Потім всі інші доступні
        for name in self.get_available_providers():
            if name not in providers_to_try:
                providers_to_try.append(name)
        
        last_error = None
        
        for provider_name in providers_to_try:
            try:
                response = await self.generate_with_provider(provider_name, prompt, context)
                return {
                    "success": True,
                    "response": response,
                    "provider_used": provider_name
                }
            except Exception as e:
                last_error = e
                logger.warning(f"Provider {provider_name} failed: {e}")
                continue
        
        return {
            "success": False,
            "error": f"All providers failed. Last error: {last_error}",
            "providers_tried": providers_to_try
        }

# Backward compatibility function
def chat_with_ai(query):
    """Функція зворотної сумісності для кешування"""
    # Перевіряємо кеш
    cached_response = get_cached_response(query)
    if cached_response:
        print("Returning cached AI response")
        return cached_response

    # Якщо немає в кеші, повертаємо базову відповідь
    response = {"reply": f"AI analysis for: {query}", "suggestions": ["Check system efficiency"]}

    # Зберігаємо в кеш
    set_cached_response(query, response)
    return response