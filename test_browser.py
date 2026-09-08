import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(color_scheme="dark")
        
        await page.goto("http://localhost:3001/alerts/12345", wait_until="networkidle")
        await asyncio.sleep(2)  # wait for any loading animations
        
        # Take a screenshot
        await page.screenshot(path="dashboard_screenshot.png")
        await browser.close()

asyncio.run(main())
