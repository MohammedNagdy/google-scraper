from playwright.async_api import Page, Browser, BrowserContext
import asyncio
import time
from typing import List, Dict, Any, Optional


class GoogleScraper:
    """
    A class to handle Google search operations using Playwright.
    
    This class encapsulates the functionality to perform Google searches and
    extract search results in a structured format.
    """
    
    def __init__(self, timeout: int = 60):
        """
        Initialize the GoogleScraper with configurable timeout.
        
        Args:
            timeout (int): Maximum time in seconds to wait for search operations
        """
        self.timeout = timeout
    
    async def setup_browser(self, browser: Browser) -> BrowserContext:
        """
        Set up a browser context with settings to avoid detection.
        
        Args:
            browser (Browser): Playwright browser instance
            
        Returns:
            BrowserContext: Configured browser context
        """
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            timezone_id="Europe/London",
            locale="en-US",
            permissions=["geolocation"],
            geolocation={"latitude": 51.5074, "longitude": -0.1278},  # London coordinates
        )
        
        # Add extra headers to appear more like a real browser
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        return context
    
    async def search(self, query: str, page: Page) -> List[Dict[str, str]]:
        """
        Perform a Google search and extract results.
        
        Args:
            query (str): The search query
            page (Page): Playwright page object
            
        Returns:
            List[Dict[str, str]]: List of search results with title, link, and snippet
        """
        await page.goto("https://www.google.com")
        await page.fill("textarea[name='q']", query)
        await page.wait_for_timeout(1000)  # Wait 1 second
        await page.keyboard.press("Enter")
        
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector(".tF2Cxc", state="visible")
        
        # Get all the links from the result page
        results = await page.locator(".tF2Cxc").all()
        
        data = []
        for result in results[1:9]:
            try:
                title = await result.locator("h3").inner_text()
            except:
                title = ""
            try:
                link = await result.locator(".yuRUbf a").first.get_attribute("href")
            except:
                link = ""
            try:
                snippet = await result.locator(".VwiC3b").first.inner_text()
            except:
                snippet = ""
                
            data.append({"title": title, "link": link, "snippet": snippet})
            
        return data
