# Textbook Generation Research

## Deployment Infrastructure Options

### GitHub Pages + Railway/Vercel
**Pros:**
- Free-tier compliant
- Easy setup and maintenance
- Good integration with Git workflows
- Reliable uptime

**Cons:**
- Limited customization options
- Potential cold start issues for backend

**Decision:** Selected for alignment with free-tier architecture principle

## Rate Limit Specifications

### Neon Database Free Tier
- Up to 10 database connections
- 512 MB storage
- 10M rows read/write per month

### Qdrant Cloud Free Tier
- Up to 1M vectors
- 1 GB storage
- 1M API requests per month

**Decision:** Dynamic rate limiting needed to stay within these constraints

## Authentication Flow Requirements

### Anonymous Access with Optional Account Creation
- Users can access textbook content without authentication
- Personalization features require account creation
- Progress tracking available only for authenticated users
- Optional account creation to reduce friction

**Decision:** Aligns with accessibility and user experience goals

## Docusaurus RAG Integration Approaches

### Custom Plugin Approach
- Create custom Docusaurus plugin for select-text → Ask AI
- Integrate directly with site layout
- Maintain consistent UI/UX
- Full control over functionality

**Decision:** Selected for best user experience and integration

## Embedding Model Selection

### Sentence Transformers (lightweight models)
- All-MiniLM-L6-v2: Good balance of performance and quality
- Multi-lingual support available
- Efficient for free-tier usage
- Local execution possible

**Decision:** All-MiniLM-L6-v2 for efficiency and quality balance