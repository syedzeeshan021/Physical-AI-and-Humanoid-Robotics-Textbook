# ADR-1: Textbook Generation System Architecture

## Status
Accepted

## Date
2025-12-07

## Context
We need to build a textbook generation system with integrated RAG chatbot for the Physical AI & Humanoid Robotics course. The system must align with project principles of simplicity, minimalism, and free-tier architecture while providing an effective educational platform.

## Decision
We will implement a distributed architecture with:

**Frontend**: Docusaurus v3 with TypeScript, deployed to GitHub Pages
- Static site generation for fast loading
- Markdown-based content management
- Custom plugin for RAG integration
- Responsive design for multiple devices

**Backend**: FastAPI with Python 3.11+, deployed to Railway/Vercel
- RESTful API design for textbook content
- RAG pipeline with semantic search
- User management and preferences
- Rate limiting and caching strategies

**Data Layer**:
- Neon (PostgreSQL) for structured data (users, preferences, chapters)
- Qdrant for vector embeddings and similarity search
- Free-tier compliant architecture

**Authentication**: Optional account creation with anonymous access
- Anonymous access for basic textbook content
- Optional accounts for personalization features
- JWT-based authentication when needed

**RAG Integration**: Custom Docusaurus plugin approach
- Select-text → Ask AI functionality
- Content-based queries from textbook only
- Caching strategies for performance

## Alternatives Considered
1. **Monolithic Architecture**: Single application handling both frontend and backend - rejected for scalability and maintenance concerns
2. **Different Frontend Frameworks**: Next.js, React with custom setup - Docusaurus chosen for built-in documentation features and static generation
3. **Different Backend**: Node.js/Express, Django - FastAPI chosen for async performance and automatic API documentation
4. **Different Databases**: MongoDB, SQLite - Neon PostgreSQL chosen for free tier and compatibility
5. **Different Vector Stores**: Pinecone, Weaviate - Qdrant chosen for free tier availability
6. **Required Authentication**: Forced account creation - rejected to reduce friction for content access

## Consequences
**Positive:**
- Fast page load times through static generation
- Cost-effective free-tier compliance
- Scalable architecture with clear separation of concerns
- Good developer experience with modern tools
- Accessible content with optional personalization

**Negative:**
- Complexity of managing multiple services
- Potential cold start issues with serverless backend
- Dependency on multiple third-party services
- More complex deployment pipeline

## References
- specs/textbook-generation/plan.md
- specs/textbook-generation/research.md
- specs/textbook-generation/data-model.md