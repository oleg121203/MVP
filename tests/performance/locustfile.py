from locust import HttpUser, task, between
import random
import json

class VentAIUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Called when a user starts"""
        # Simulate user login or initialization
        pass
    
    @task(5)
    def view_homepage(self):
        """Load the homepage"""
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Homepage failed with status {response.status_code}")
    
    @task(3)
    def view_dashboard(self):
        """Access dashboard or main app area"""
        # Adjust route based on your application
        with self.client.get("/dashboard", catch_response=True) as response:
            if response.status_code in [200, 404]:  # 404 is ok if route doesn't exist yet
                response.success()
            else:
                response.failure(f"Dashboard failed with status {response.status_code}")
    
    @task(2)
    def api_health_check(self):
        """Check API health endpoint"""
        with self.client.get("/health", catch_response=True, name="/api/health") as response:
            if response.status_code in [200, 404]:  # 404 is ok if endpoint doesn't exist yet
                response.success()
            else:
                response.failure(f"Health check failed with status {response.status_code}")
    
    @task(1)
    def static_resources(self):
        """Load static resources"""
        static_files = [
            "/static/css/main.css",
            "/static/js/main.js", 
            "/favicon.ico",
            "/logo192.png"
        ]
        
        file_to_load = random.choice(static_files)
        with self.client.get(file_to_load, catch_response=True) as response:
            if response.status_code in [200, 404]:  # 404 is ok for missing static files
                response.success()
            else:
                response.failure(f"Static file {file_to_load} failed with status {response.status_code}")

class APIUser(HttpUser):
    """Simulates API-only usage"""
    wait_time = between(0.5, 2)
    
    def on_start(self):
        # Set base URL for API testing
        self.host = "http://localhost:8000"  # Backend API
    
    @task(4)
    def api_docs(self):
        """Access API documentation"""
        with self.client.get("/docs", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"API docs failed with status {response.status_code}")
    
    @task(2)
    def api_openapi_spec(self):
        """Access OpenAPI specification"""
        with self.client.get("/openapi.json", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"OpenAPI spec failed with status {response.status_code}")
    
    @task(1)
    def api_health(self):
        """Check API health"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"API health failed with status {response.status_code}")

class HeavyUser(HttpUser):
    """Simulates heavy usage patterns"""
    wait_time = between(0.1, 1)
    weight = 1  # Lower weight means fewer of these users
    
    @task
    def rapid_requests(self):
        """Make rapid consecutive requests"""
        endpoints = ["/", "/docs", "/health"]
        
        for endpoint in endpoints:
            with self.client.get(endpoint, catch_response=True) as response:
                if response.status_code in [200, 404]:
                    response.success()
                else:
                    response.failure(f"Rapid request to {endpoint} failed with status {response.status_code}")
