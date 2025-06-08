import { test, expect } from '@playwright/test';

test.describe('VentAI Application', () => {
  test('homepage loads successfully', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page loads
    await expect(page).toHaveTitle(/VentAI/);
    
    // Check for main elements
    await expect(page.locator('h1')).toBeVisible();
  });

  test('navigation works correctly', async ({ page }) => {
    await page.goto('/');
    
    // Test navigation to different sections
    // Adjust selectors based on your actual application
    const navLinks = page.locator('nav a');
    const count = await navLinks.count();
    
    expect(count).toBeGreaterThan(0);
  });

  test('API connectivity', async ({ page }) => {
    await page.goto('/');
    
    // Check if backend API is accessible
    const response = await page.request.get(process.env.BACKEND_URL + '/docs' || 'http://localhost:8000/docs');
    expect(response.status()).toBe(200);
  });

  test('responsive design', async ({ page }) => {
    await page.goto('/');
    
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('body')).toBeVisible();
    
    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page.locator('body')).toBeVisible();
  });
});
