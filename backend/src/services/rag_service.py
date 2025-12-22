from typing import Dict, List, Any
from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from src.core.vector_store import vector_store
from src.services.chapter_service import ChapterService
from src.core.config import settings
from openai import OpenAI
import google.generativeai as genai
import asyncio
import re

# Set up logging
logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        # Initialize lazily to avoid startup issues
        self.encoder = None
        self.openai_client = None
        self.gemini_model = None
        self._initialized = False

    def _validate_api_keys(self):
        """Validate API keys are properly configured"""
        if settings.AI_PROVIDER.lower() == 'gemini':
            if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == 'your-gemini-api-key-here' or settings.GEMINI_API_KEY.startswith('your-'):
                raise ValueError("GEMINI_API_KEY is not configured in settings. Please set GEMINI_API_KEY in your .env file.")
        else:
            if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith('your-') or (settings.OPENAI_API_KEY.startswith('sk-') and len(settings.OPENAI_API_KEY) < 20):
                raise ValueError("OPENAI_API_KEY is not properly configured in settings. Please set OPENAI_API_KEY in your .env file.")

    def _ensure_initialized(self):
        """Initialize components only when first needed"""
        if not self._initialized:
            try:
                # Validate API keys before initializing
                self._validate_api_keys()

                # Initialize the sentence transformer model for embeddings
                # Using a lightweight model for efficiency
                logger.info("Loading sentence transformer model...")
                self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Sentence transformer model loaded successfully.")

                # Initialize AI provider based on configuration
                if settings.AI_PROVIDER.lower() == 'gemini':
                    genai.configure(api_key=settings.GEMINI_API_KEY)
                    self.gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)
                    logger.info("Using Google Gemini as AI provider")
                else:
                    self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                    logger.info("Using OpenAI as AI provider")

                self._initialized = True
                logger.info("RAG service initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize RAG service components: {str(e)}")
                raise e

    async def process_query(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """
        Process a query using RAG (Retrieval-Augmented Generation)
        """
        try:
            # Ensure components are initialized
            self._ensure_initialized()

            # Log the incoming query
            logger.info(f"Processing query: {query[:100]}...")

            # Generate embedding for the query
            query_embedding = self.encoder.encode([query])[0].tolist()

            # Search for similar content in the vector store
            search_results = await vector_store.search_similar(query_embedding, limit=3)

            if not search_results:
                logger.warning("No relevant results found in vector store.")
                # If no results found, return a default response
                return {
                    "response": "I couldn't find relevant information in the textbook for your query. Please try rephrasing your question or consult the textbook directly.",
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
                sources.append({
                    "title": chapter_title,
                    "text_snippet": result["text"][:200] + "..." if len(result["text"]) > 200 else result["text"]
                })

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

            Format your response in a clear and structured way, using markdown if appropriate.
            """

            try:
                if settings.AI_PROVIDER.lower() == 'gemini':
                    # Generate response using Google Gemini API
                    logger.info("Calling Google Gemini API...")
                    response = self.gemini_model.generate_content(prompt)
                    answer = response.text.strip()
                else:
                    # Generate response using OpenAI API
                    logger.info("Calling OpenAI API...")
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=500,
                        temperature=0.7
                    )
                    answer = response.choices[0].message.content.strip()

                logger.info("Successfully generated response from LLM.")

                return {
                    "response": answer,
                    "sources": sources,
                    "session_id": session_id
                }
            except Exception as e:
                # Handle any errors in the API call
                logger.error(f"Error calling {settings.AI_PROVIDER} API: {str(e)}")

                # Provide a fallback response using the context directly
                fallback_response = f"I encountered an issue generating a response. Based on the textbook content:\n\n{context[:500]}...\n\nFor a complete answer, please ensure your {settings.AI_PROVIDER} API key is properly configured."

                return {
                    "response": fallback_response,
                    "sources": sources,
                    "session_id": session_id
                }

        except ValueError as ve:
            logger.error(f"Configuration error in RAG service: {str(ve)}")
            return {
                "response": f"Configuration error: {str(ve)}",
                "sources": [],
                "session_id": session_id
            }
        except Exception as e:
            logger.error(f"Unexpected error processing RAG query: {str(e)}")
            return {
                "response": "An unexpected error occurred while processing your query. Please try again later.",
                "sources": [],
                "session_id": session_id
            }

    def _create_overlapping_chunks(self, text: str, chunk_size: int = 512, overlap: int = 100) -> List[str]:
        """
        Create overlapping chunks of text to preserve context across boundaries
        """
        # Split text into sentences to maintain semantic boundaries
        sentences = re.split(r'[.!?]+\s+', text)

        chunks = []
        current_chunk = ""
        current_length = 0

        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            if current_length + len(sentence) > chunk_size and current_chunk:
                # Save current chunk
                chunks.append(current_chunk.strip())

                # Start new chunk with overlap
                if overlap > 0:
                    # Find the last few sentences in current chunk to use as overlap
                    overlap_sentences = current_chunk.split('. ')
                    if len(overlap_sentences) > 1:
                        # Take the last few sentences as overlap
                        overlap_text = '. '.join(overlap_sentences[-2:]) + '. '
                        current_chunk = overlap_text + sentence
                        current_length = len(current_chunk)
                    else:
                        current_chunk = sentence
                        current_length = len(sentence)
                else:
                    current_chunk = sentence
                    current_length = len(sentence)
            else:
                current_chunk += " " + sentence if current_chunk else sentence
                current_length += len(sentence) + 1

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # If no sentence-based chunks were created, fall back to word-based chunks
        if not chunks:
            words = text.split()
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i + chunk_size])
                if len(chunk.strip()) > 10:  # Only process non-trivial chunks
                    chunks.append(chunk)

        return chunks

    async def process_text_for_embeddings(self, text: str, chapter_id: str, chunk_size: int = 512):
        """
        Process text into chunks and generate embeddings for each chunk
        """
        try:
            # Ensure components are initialized
            self._ensure_initialized()

            logger.info(f"Processing text for embeddings, chapter_id: {chapter_id}, length: {len(text)} chars")

            # Create overlapping chunks to preserve context
            chunks = self._create_overlapping_chunks(text, chunk_size)
            logger.info(f"Created {len(chunks)} chunks for embedding")

            # Generate embeddings for each chunk
            results = []
            for idx, chunk in enumerate(chunks):
                if len(chunk.strip()) > 10:  # Only process non-trivial chunks
                    try:
                        # Generate embedding
                        embedding = self.encoder.encode([chunk])[0].tolist()

                        # Store in vector store
                        point_id = await vector_store.store_embedding(
                            text=chunk,
                            chapter_id=chapter_id,
                            metadata={
                                "chunk_index": idx,
                                "total_chunks": len(chunks),
                                "chunk_length": len(chunk)
                            }
                        )
                        results.append(point_id)

                        logger.debug(f"Stored embedding for chunk {idx}/{len(chunks)}, point_id: {point_id}")
                    except Exception as e:
                        logger.error(f"Error processing chunk {idx}: {str(e)}")
                        continue

            logger.info(f"Successfully stored {len(results)} embeddings for chapter {chapter_id}")
            return results
        except Exception as e:
            logger.error(f"Error processing text for embeddings: {str(e)}")
            raise e


# Global instance
rag_service = RAGService()