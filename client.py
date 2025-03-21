import asyncio
import grpc
import search_pb2
import search_pb2_grpc

async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = search_pb2_grpc.SearchServiceStub(channel)
        
        # Create a search request
        request = search_pb2.SearchRequest(query="python programming")
        
        try:
            # Call the Search RPC
            response = await stub.Search(request)
            
            print("\nSearch Results:")
            print("==============")
            for result in response.results:
                print(f"\nTitle: {result.title}")
                print(f"Link: {result.link}")
                print(f"Snippet: {result.snippet}")
                print("-" * 80)
                
        except grpc.RpcError as e:
            print(f"RPC failed: {e}")

if __name__ == '__main__':
    asyncio.run(run()) 