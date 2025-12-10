#!/usr/bin/env python3
"""
Test script to isolate Qdrant connection issue
"""

from qdrant_client import QdrantClient
from src.core.config import settings

print("Testing Qdrant connection...")
print(f"QDRANT_URL: {settings.QDRANT_URL}")
print(f"QDRANT_API_KEY: {'***' if settings.QDRANT_API_KEY else 'None'}")

try:
    if settings.QDRANT_URL and "gcp.cloud.qdrant.io" in settings.QDRANT_URL:
        print("Attempting to connect to cloud instance...")
        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            https=True
        )
    else:
        print("Attempting to connect to local instance...")
        client = QdrantClient(
            url=settings.QDRANT_URL or "http://localhost:6333",
            api_key=settings.QDRANT_API_KEY
        )

    print("Qdrant client created successfully!")
    print(f"Client type: {type(client)}")

    # Try to list collections to test the connection
    collections = client.get_collections()
    print(f"Available collections: {collections}")

    # Test collection creation like in VectorStore
    from qdrant_client.http import models
    collection_name = "test_collection"

    try:
        # Check if collection exists
        client.get_collection(collection_name)
        print(f"Collection {collection_name} already exists")
    except:
        # Create collection if it doesn't exist
        print(f"Creating collection {collection_name}...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )
        print(f"Collection {collection_name} created successfully")

    print("All operations completed successfully!")

except Exception as e:
    print(f"Error creating Qdrant client: {e}")
    import traceback
    traceback.print_exc()