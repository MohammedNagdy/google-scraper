import asyncio
import grpc
import search_pb2
import search_pb2_grpc
from concurrent import futures
from playwright.async_api import async_playwright
from google_search import GoogleScraper


class SearchServicer(search_pb2_grpc.SearchServiceServicer):
    """
    gRPC service implementation for handling search requests.
    
    This class implements the Search RPC defined in the search.proto file
    and uses the GoogleScraper to perform searches and return results.
    """
    
    def __init__(self):
        """Initialize the search servicer with a GoogleScraper instance."""
        self.scraper = GoogleScraper(timeout=60)
    
    async def Search(self, request, context):
        """
        Handle search requests and return search results.
        
        Args:
            request: gRPC SearchRequest containing the search query
            context: gRPC context
            
        Returns:
            search_pb2.SearchResponse: gRPC response containing search results
        """
        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-dev-shm-usage",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-accelerated-2d-canvas",
                        "--disable-gpu"
                    ]
                )
                
                browser_context = await self.scraper.setup_browser(browser)
                page = await browser_context.new_page()
                
                try:
                    # Perform the search with a timeout
                    results = await asyncio.wait_for(
                        self.scraper.search(request.query, page),
                        timeout=self.scraper.timeout
                    )
                    print(f"Found {len(results)} results for query: {request.query}")
                except asyncio.TimeoutError:
                    await browser.close()
                    print("Search operation timed out")
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
            print(f"Error performing search: {str(e)}")
            return search_pb2.SearchResponse()


class Server:
    """
    gRPC server for handling search requests.
    
    This class encapsulates the server configuration and startup logic.
    """
    
    def __init__(self, address="[::]:50051", max_workers=10):
        """
        Initialize the server with address and worker configuration.
        
        Args:
            address (str): Server address to listen on
            max_workers (int): Maximum number of worker threads
        """
        self.address = address
        self.max_workers = max_workers
        self.server = None
    
    async def start(self):
        """
        Start the gRPC server.
        
        This method initializes the server, adds the search service,
        and starts listening for requests.
        """
        self.server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=self.max_workers))
        search_pb2_grpc.add_SearchServiceServicer_to_server(SearchServicer(), self.server)
        self.server.add_insecure_port(self.address)
        
        print(f"Starting server on {self.address}...")
        await self.server.start()
        
        print("Server started. Press Ctrl+C to stop.")
        await self.server.wait_for_termination()


async def main():
    """Initialize and start the server."""
    server = Server()
    await server.start()


if __name__ == '__main__':
    asyncio.run(main()) 