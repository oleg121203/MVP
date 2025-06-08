"""
End-to-End Tests Configuration
Setup for E2E tests using Playwright
"""

import pytest
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# Test configuration
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def browser():
    """Launch browser for E2E tests"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        yield browser
        await browser.close()

@pytest.fixture
async def context(browser: Browser):
    """Create browser context"""
    context = await browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True
    )
    yield context
    await context.close()

@pytest.fixture
async def page(context: BrowserContext):
    """Create new page"""
    page = await context.new_page()
    yield page
    await page.close()

@pytest.fixture
async def authenticated_page(page: Page):
    """Create authenticated page with logged-in user"""
    # Navigate to login page
    await page.goto(f"{BASE_URL}/login")
    
    # Fill login form
    await page.fill('[data-testid="email-input"]', "e2e_test@ventai.app")
    await page.fill('[data-testid="password-input"]', "testpassword123")
    await page.click('[data-testid="login-button"]')
    
    # Wait for navigation to dashboard
    await page.wait_for_url(f"{BASE_URL}/dashboard")
    
    return page

@pytest.fixture
def test_user_credentials():
    """Test user credentials for E2E tests"""
    return {
        "email": "e2e_test@ventai.app",
        "password": "testpassword123",
        "first_name": "E2E",
        "last_name": "Test"
    }

@pytest.fixture
def sample_calculation_data():
    """Sample data for HVAC calculations"""
    return {
        "room_name": "Test Room",
        "area": "50",
        "height": "3",
        "occupancy": "10",
        "air_changes": "6"
    }

class E2ETestBase:
    """Base class for E2E tests"""
    
    async def wait_for_element(self, page: Page, selector: str, timeout: int = 5000):
        """Wait for element to be visible"""
        await page.wait_for_selector(selector, timeout=timeout)
    
    async def take_screenshot(self, page: Page, name: str):
        """Take screenshot for debugging"""
        await page.screenshot(path=f"screenshots/{name}.png", full_page=True)
    
    async def login_user(self, page: Page, email: str, password: str):
        """Helper method to login user"""
        await page.goto(f"{BASE_URL}/login")
        await page.fill('[data-testid="email-input"]', email)
        await page.fill('[data-testid="password-input"]', password)
        await page.click('[data-testid="login-button"]')
        await page.wait_for_url(f"{BASE_URL}/dashboard")
    
    async def create_project(self, page: Page, project_data: dict):
        """Helper method to create a new project"""
        await page.click('[data-testid="new-project-button"]')
        await page.fill('[data-testid="project-name-input"]', project_data["name"])
        await page.fill('[data-testid="project-description-input"]', project_data["description"])
        await page.select_option('[data-testid="building-type-select"]', project_data["building_type"])
        await page.click('[data-testid="create-project-button"]')
        await page.wait_for_selector('[data-testid="project-created-message"]')

# Pytest configuration
def pytest_configure(config):
    """Configure pytest for E2E tests"""
    import os
    os.makedirs("screenshots", exist_ok=True)

def pytest_collection_modifyitems(config, items):
    """Add E2E marker to all tests in this directory"""
    for item in items:
        item.add_marker(pytest.mark.e2e)
