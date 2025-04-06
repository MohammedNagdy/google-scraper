import asyncio
import grpc
import search_pb2
import search_pb2_grpc
from typing import List, Optional


class SearchClient:
    """
    Client for interacting with the Google Search gRPC service.
    
    This class encapsulates the functionality to connect to the search service,
    send search queries, and process search results.
    """
    
    def __init__(self, server_address: str = 'localhost:50051'):
        """
        Initialize the client with the server address.
        
        Args:
            server_address (str): Address of the gRPC server
        """
        self.server_address = server_address
        self.channel = None
        self.stub = None
    
    async def connect(self):
        """
        Connect to the gRPC server.
        
        Returns:
            bool: True if connected successfully, False otherwise
        """
        self.channel = grpc.aio.insecure_channel(self.server_address)
        self.stub = search_pb2_grpc.SearchServiceStub(self.channel)
        return True
    
    async def search(self, query: str) -> List[dict]:
        """
        Send a search query to the server and return results.
        
        Args:
            query (str): Search query string
            
        Returns:
            List[dict]: List of search results, each containing title, link, and snippet
            
        Raises:
            ConnectionError: If not connected to the server
            grpc.RpcError: If the RPC call fails
        """
        if not self.stub:
            raise ConnectionError("Not connected to server. Call connect() first.")
        
        # Create a search request
        request = search_pb2.SearchRequest(query=query)
        
        # Call the Search RPC
        response = await self.stub.Search(request)
        
        # Convert the response to a list of dictionaries
        results = []
        for result in response.results:
            results.append({
                'title': result.title,
                'link': result.link,
                'snippet': result.snippet
            })
        
        return results
    
    async def close(self):
        """Close the gRPC channel."""
        if self.channel:
            await self.channel.close()
    
    def print_results(self, results: List[dict]):
        """
        Print search results in a formatted way.
        
        Args:
            results (List[dict]): List of search results to print
        """
        print("\nSearch Results:")
        print("==============")
        
        if not results:
            print("No results found.")
            return
            
        for result in results:
            print(f"\nTitle: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}")
            print("-" * 80)


async def main():
    """
    Main function to demonstrate client usage.
    
    This function connects to the search service, performs a search,
    and displays the results.
    """
    client = SearchClient()
    
    try:
        # Connect to the server
        await client.connect()
        
        # Perform a search
        query = "python programming"
        print(f"Searching for: {query}")
        
        results = await client.search(query)
        
        # Print the results
        client.print_results(results)
        
    except grpc.RpcError as e:
        print(f"RPC failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        await client.close()


if __name__ == '__main__':
    asyncio.run(main()) 