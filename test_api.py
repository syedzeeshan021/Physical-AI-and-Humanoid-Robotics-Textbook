import asyncio
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from backend.src.services.rag_service import rag_service

async def test_rag_service():
    print("Testing RAG service initialization...")
    start_time = time.time()

    try:
        # Initialize the RAG service (this might take a while on first run)
        rag_service._ensure_initialized()
        init_time = time.time()
        print(f"RAG service initialized in {init_time - start_time:.2f} seconds")

        # Test a simple query
        print("Testing query...")
        result = await rag_service.process_query("hello", session_id="test")
        query_time = time.time()
        print(f"Query processed in {query_time - init_time:.2f} seconds")
        print("Result:", result)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_rag_service())