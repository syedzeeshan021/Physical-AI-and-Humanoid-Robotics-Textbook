"""
Script to populate Qdrant vector store with textbook embeddings
"""
import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.vector_store import vector_store
from src.services.chapter_service import ChapterService
from src.core.database import init_db
from src.utils.initialize_content import initialize_textbook_content
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def populate_vector_store():
    """
    Main function to populate vector store with textbook data
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting RAG Vector Store Population")
        logger.info("=" * 60)

        # Step 1: Initialize database
        logger.info("\n[1/4] Initializing database...")
        await init_db()
        logger.info("✓ Database initialized")

        # Step 2: Initialize textbook content
        logger.info("\n[2/4] Loading textbook chapters...")
        await initialize_textbook_content()
        logger.info("✓ Textbook chapters loaded")

        # Step 3: Fetch all chapters
        logger.info("\n[3/4] Fetching chapters from database...")
        chapters = await ChapterService.get_all_chapters()
        logger.info(f"✓ Found {len(chapters)} chapters")

        if not chapters:
            logger.warning("No chapters found in database!")
            return

        # Step 4: Generate embeddings and store in Qdrant
        logger.info("\n[4/4] Generating embeddings and storing in Qdrant...")
        logger.info("This may take a minute...\n")

        total_chunks = 0
        for i, chapter in enumerate(chapters, 1):
            logger.info(f"Processing chapter {i}/{len(chapters)}: {chapter.title}")

            # Split chapter content into chunks (every 500 characters with overlap)
            chunk_size = 500
            overlap = 100
            content = chapter.content

            chunks = []
            for j in range(0, len(content), chunk_size - overlap):
                chunk = content[j : j + chunk_size]
                if chunk.strip():
                    chunks.append(chunk)

            logger.info(f"  → Split into {len(chunks)} chunks")

            # Store each chunk as an embedding
            for j, chunk in enumerate(chunks, 1):
                try:
                    point_id = await vector_store.store_embedding(
                        text=chunk,
                        chapter_id=chapter.id,
                        metadata={
                            "title": chapter.title,
                            "order": chapter.order,
                            "chunk_index": j,
                            "total_chunks": len(chunks),
                        },
                    )
                    total_chunks += 1

                    if j % 5 == 0:
                        logger.info(f"    ✓ Stored {j}/{len(chunks)} chunks")

                except Exception as e:
                    logger.error(
                        f"    ✗ Error storing chunk {j}: {str(e)}"
                    )

            logger.info(f"  ✓ Chapter {i} complete\n")

        logger.info("=" * 60)
        logger.info(f"✓ Vector Store Population Complete!")
        logger.info(f"  - Total chunks indexed: {total_chunks}")
        logger.info(f"  - Chapters processed: {len(chapters)}")
        logger.info("=" * 60)
        logger.info("\nYou can now:")
        logger.info("1. Start the backend: python -m uvicorn src.main:app --reload")
        logger.info("2. Test the RAG chatbot by asking questions")
        logger.info("\nQdrant Dashboard: http://localhost:6333/dashboard")

    except Exception as e:
        logger.error(f"✗ Error populating vector store: {str(e)}")
        logger.error("Make sure:")
        logger.error("  1. Qdrant is running on http://localhost:6333")
        logger.error("  2. PostgreSQL/Neon database is accessible")
        logger.error("  3. .env file has correct credentials")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(populate_vector_store())
    except KeyboardInterrupt:
        logger.info("\n\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"\n\nFailed to populate vector store: {str(e)}")
        sys.exit(1)
