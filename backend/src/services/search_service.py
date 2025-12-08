from typing import List, Dict, Any
from src.core.vector_store import vector_store
from sentence_transformers import SentenceTransformer


class SearchService:
    def __init__(self):
        # Initialize the sentence transformer model for embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

    async def search_similar_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for content similar to the query
        """
        # Generate embedding for the query
        query_embedding = self.encoder.encode([query])[0].tolist()

        # Search in vector store
        results = await vector_store.search_similar(query_embedding, limit)

        return results

    async def search_by_chapter(self, query: str, chapter_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for content within a specific chapter
        This would require additional filtering that's not directly supported by Qdrant
        In a real implementation, we might need to adjust our vector store approach
        """
        # For now, this is a simplified implementation that searches all content
        # and then filters by chapter ID in the application layer
        all_results = await self.search_similar_content(query, limit * 2)  # Get more results to account for filtering

        # Filter results by chapter_id
        chapter_results = [result for result in all_results if result["chapter_id"] == chapter_id]

        return chapter_results[:limit]


# Global instance
search_service = SearchService()