import asyncio
from playwright.async_api import async_playwright, Playwright
from google_search import GoogleScraper


async def run(playwright: Playwright, query: str = "python programming"):
    """
    Run a standalone Google search demonstration.
    
    Args:
        playwright (Playwright): Playwright instance
        query (str): Search query to use
    """
    # Initialize the scraper
    scraper = GoogleScraper()
    
    # Launch browser with anti-detection features
    browser = await playwright.chromium.launch(
        headless=False, 
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    # Set up the browser context
    context = await scraper.setup_browser(browser)
    
    # Create a new page
    page = await context.new_page()
    
    print(f"Searching for: {query}")
    
    try:
        # Perform the search
        results = await scraper.search(query, page)
        
        # Print the results
        print("\nSearch Results:")
        print("===============")
        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}")
            print("-" * 50)
            
        print(f"\nTotal results: {len(results)}")
    finally:
        # Close the browser
        await browser.close()


async def main():
    """Entry point for the standalone search demonstration."""
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(main())