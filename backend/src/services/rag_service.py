from typing import Dict, List, Any
from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from src.core.vector_store import vector_store
from src.services.chapter_service import ChapterService
from src.core.config import settings
import openai
import asyncio

# Set up logging
logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        # Initialize the sentence transformer model for embeddings
        # Using a lightweight model for efficiency
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize OpenAI client
        openai.api_key = settings.OPENAI_API_KEY

    async def process_query(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """
        Process a query using RAG (Retrieval-Augmented Generation)
        """
        try:
            # Generate embedding for the query
            query_embedding = self.encoder.encode([query])[0].tolist()

            # Search for similar content in the vector store
            search_results = await vector_store.search_similar(query_embedding, limit=3)

            if not search_results:
                # If no results found, return a default response
                return {
                    "response": "I couldn't find relevant information in the textbook for your query.",
                    "sources": [],
                    "session_id": session_id
                }

            # Prepare context from search results
            context_parts = []
            sources = []

            for result in search_results:
                # Get the chapter title for the source reference
                chapter = await ChapterService.get_chapter_by_id(result["chapter_id"])
                chapter_title = chapter.title if chapter else "Unknown Chapter"

                context_parts.append(result["text"])
                sources.append(f"{chapter_title}")

            # Combine context
            context = "\n\n".join(context_parts)

            # Create the prompt for the LLM
            prompt = f"""
            You are an AI assistant for a textbook on Physical AI and Humanoid Robotics.
            Answer the user's question based only on the provided context from the textbook.

            Context: {context}

            Question: {query}

            Please provide a helpful and accurate answer based only on the context provided.
            If the context doesn't contain the information needed to answer the question,
            please say so explicitly.
            """

            try:
                # Generate response using OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.7
                )

                answer = response.choices[0].message.content.strip()

                return {
                    "response": answer,
                    "sources": sources,
                    "session_id": session_id
                }
            except Exception as e:
                # Handle any errors in the API call
                logger.error(f"Error calling OpenAI API: {str(e)}")
                return {
                    "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                    "sources": sources,
                    "session_id": session_id
                }

        except Exception as e:
            logger.error(f"Error processing RAG query: {str(e)}")
            raise e

    async def process_text_for_embeddings(self, text: str, chapter_id: str, chunk_size: int = 512):
        """
        Process text into chunks and generate embeddings for each chunk
        """
        # Simple chunking approach - split text into overlapping chunks
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)

        # Generate embeddings for each chunk
        results = []
        for chunk in chunks:
            if len(chunk.strip()) > 10:  # Only process non-trivial chunks
                # Generate embedding
                embedding = self.encoder.encode([chunk])[0].tolist()

                # Store in vector store
                point_id = await vector_store.store_embedding(
                    text=chunk,
                    chapter_id=chapter_id,
                    metadata={"chunk_index": chunks.index(chunk), "total_chunks": len(chunks)}
                )
                results.append(point_id)

            return results


# Global instance
rag_service = RAGService()