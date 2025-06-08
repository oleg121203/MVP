# Adding Redis caching for AI provider responses
import redis
import json
import hashlib
import os

# Initialize Redis connection
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Cache expiration time in seconds (e.g., 1 hour)
CACHE_EXPIRY = 3600

def generate_cache_key(query):
    """Generate a unique cache key based on the query."""
    query_str = json.dumps(query, sort_keys=True)
    return f"ai_cache:{hashlib.md5(query_str.encode()).hexdigest()}"

def get_cached_response(query):
    """Retrieve cached response for a given query."""
    cache_key = generate_cache_key(query)
    try:
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception as e:
        print(f"Error retrieving from cache: {e}")
    return None

def set_cached_response(query, response):
    """Cache the response for a given query."""
    cache_key = generate_cache_key(query)
    try:
        redis_client.setex(cache_key, CACHE_EXPIRY, json.dumps(response))
    except Exception as e:
        print(f"Error setting cache: {e}")

# Wrap AI provider calls with caching
# Note: This assumes there's a function or method in this file that makes AI calls
# If specific function names are different, adjust accordingly
def chat_with_ai(query):
    """Example function to wrap AI provider calls with caching."""
    # Check cache first
    cached_response = get_cached_response(query)
    if cached_response:
        print("Returning cached AI response")
        return cached_response

    # If not in cache, make the actual AI call
    # Replace this with actual AI provider call logic from the original file
    response = {"reply": f"AI analysis for: {query}", "suggestions": ["Check system efficiency"]}

    # Cache the response
    set_cached_response(query, response)
    return response