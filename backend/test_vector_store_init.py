#!/usr/bin/env python3
"""
Test script to replicate VectorStore initialization
"""

# Import the same way as vector_store.py
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import uuid
from src.core.config import settings
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

def test_vector_store_init():
    print("Testing VectorStore initialization...")

    # Initialize Qdrant client the exact same way as VectorStore
    if settings.QDRANT_URL and "gcp.cloud.qdrant.io" in settings.QDRANT_URL:
        # Cloud instance - use HTTPS and proper configuration
        print("Connecting to cloud instance...")
        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            https=True  # Explicitly enable HTTPS for cloud instances
        )
    else:
        # Local instance
        print("Connecting to local instance...")
        client = QdrantClient(
            url=settings.QDRANT_URL or "http://localhost:6333",
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=False
        )

    print("Qdrant client created successfully!")

    # Initialize sentence transformer for embeddings
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    print("Sentence transformer initialized!")

    # Create collection for textbook embeddings if it doesn't exist
    collection_name = "textbook_embeddings"

    try:
        # Check if collection exists
        print(f"Checking if collection {collection_name} exists...")
        client.get_collection(collection_name)
        print(f"Collection {collection_name} already exists")
    except Exception as e:
        print(f"Collection doesn't exist, creating it: {e}")
        # Create collection if it doesn't exist
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),  # Using sentence-transformers default
        )
        print(f"Collection {collection_name} created successfully!")

    print("VectorStore initialization completed successfully!")

if __name__ == "__main__":
    test_vector_store_init()