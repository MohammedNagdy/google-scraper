import asyncio
import grpc
import search_pb2
import search_pb2_grpc
from concurrent import futures
from playwright.async_api import async_playwright
from google_search import google_search

class SearchService(search_pb2_grpc.SearchServiceServicer):
    async def Search(self, request, context):
        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(
                    headless=True,  # Changed to headless mode
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-dev-shm-usage",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-accelerated-2d-canvas",
                        "--disable-gpu"
                    ]
                )
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
                
                page = await context.new_page()
                
                try:
                    # Perform the search with a longer timeout
                    results = await asyncio.wait_for(
                        google_search(request.query, page),
                        timeout=60.0  # Increased timeout to 60 seconds
                    )
                    print("Results: " + str(results))
                except asyncio.TimeoutError:
                    await browser.close()
                    print("Timeout error")
                    return search_pb2.SearchResponse()
                
                await browser.close()
                
                # Convert results to gRPC response
                response = search_pb2.SearchResponse()
                for result in results:
                    search_result = response.results.add()
                    search_result.title = result['title']
                    search_result.link = result['link']
                    search_result.snippet = result['snippet']
                
                return response
                
        except Exception as e:
            print("Error: " + str(e))
            return search_pb2.SearchResponse()

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    search_pb2_grpc.add_SearchServiceServicer_to_server(SearchService(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting server on port 50051...")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve()) 