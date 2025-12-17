from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import uuid
from src.core.config import settings
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        # Initialize Qdrant client
        # Handle both cloud and local Qdrant instances
        if settings.QDRANT_URL and "gcp.cloud.qdrant.io" in settings.QDRANT_URL:
            # Cloud instance - construct URL properly for Qdrant client
            # Qdrant client expects URL without protocol prefix when using https=True
            clean_url = settings.QDRANT_URL.replace("https://", "")
            self.client = QdrantClient(
                host=clean_url,
                api_key=settings.QDRANT_API_KEY,
                https=True  # Explicitly enable HTTPS for cloud instances
            )
        else:
            # Local instance
            self.client = QdrantClient(
                url=settings.QDRANT_URL or "http://localhost:6333",
                api_key=settings.QDRANT_API_KEY,
                prefer_grpc=False
            )

        # Initialize sentence transformer for embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

        # Create collection for textbook embeddings if it doesn't exist
        self.collection_name = "textbook_embeddings"
        self._create_collection()

    def _create_collection(self):
        """Create the embeddings collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),  # Using sentence-transformers default
            )

    async def store_embedding(self, text: str, chapter_id: str, metadata: Dict[str, Any] = None) -> str:
        """Store an embedding in Qdrant"""
        try:
            point_id = str(uuid.uuid4())

            # Generate real embedding using sentence-transformers
            embedding = self.encoder.encode(text).tolist()

            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "text": text,
                            "chapter_id": chapter_id,
                            "metadata": metadata or {}
                        }
                    )
                ]
            )

            return point_id
        except Exception as e:
            logger.error(f"Error storing embedding: {str(e)}")
            raise

    async def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar embeddings"""
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit
        )

        return [
            {
                "id": str(result.id),
                "text": result.payload.get("text", ""),
                "chapter_id": result.payload.get("chapter_id", ""),
                "metadata": result.payload.get("metadata", {}),
                "score": result.score
            }
            for result in results.points
        ]

    async def delete_by_chapter_id(self, chapter_id: str):
        """Delete all embeddings associated with a chapter"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FieldCondition(
                key="payload.chapter_id",
                match=models.MatchValue(value=chapter_id)
            )
        )


# Global instance
vector_store = VectorStore()