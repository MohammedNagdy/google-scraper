from playwright.async_api import Page
import time


async def google_search(query: str, page: Page):

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
        print("Found " + str((data)) + " results")

    print(data)
    return data
