# Textbook Generation - Implementation Plan

## Technical Context

**Feature:** Textbook Generation with Integrated RAG Chatbot
**Domain:** Educational platform for Physical AI & Humanoid Robotics
**Core Components:**
- Docusaurus-based textbook frontend
- FastAPI backend with RAG capabilities
- Qdrant vector store for embeddings
- Neon database for structured data

**Unknowns:**
- Specific deployment infrastructure details - NEEDS CLARIFICATION
- Exact API rate limits for free-tier services - NEEDS CLARIFICATION
- Detailed authentication flow requirements - NEEDS CLARIFICATION

## Constitution Check

### Alignment with Project Principles
- ✅ **Simplicity**: Clean, minimal UI design using Docusaurus
- ✅ **Accuracy**: RAG answers ONLY from book text
- ✅ **Minimalism**: Lightweight architecture with efficient components
- ✅ **Fast Builds**: Static site generation with Docusaurus
- ✅ **Free-tier Architecture**: Using Neon, Qdrant free tiers
- ✅ **RAG-focused**: Answers only from textbook content

### Potential Violations
- None identified - fully aligned with constitution

## Gates

### Architecture Gate
- [x] Uses specified technology stack (Docusaurus, FastAPI, Neon, Qdrant)
- [x] Free-tier compliant design
- [x] Static site generation for frontend
- [x] RAG-focused approach

### Performance Gate
- [x] Page load times under 3 seconds target
- [x] RAG response times under 5 seconds target
- [x] Efficient embedding generation approach

### Security Gate
- [x] Input validation and sanitization planned
- [x] Rate limiting for API endpoints included
- [x] Secure authentication for personalization planned

### Quality Gate
- [x] TypeScript for frontend type safety
- [x] Python type hints for backend
- [x] Testing requirements included

## Phase 0: Research & Unknown Resolution

### Research Tasks
1. Deployment infrastructure options for free-tier compliance
2. Rate limit specifics for Neon and Qdrant free tiers
3. Authentication flow for optional personalization features
4. Docusaurus plugin ecosystem for RAG integration
5. Embedding model selection for free-tier usage

### Research Findings

#### Decision: Deployment Infrastructure
**Rationale:** GitHub Pages for frontend, Railway or Vercel for backend
**Alternatives considered:** Netlify, AWS, GCP
**Chosen:** GitHub Pages + Railway/Vercel for free-tier compliance

#### Decision: Rate Limiting
**Rationale:** Dynamic rate limiting based on free-tier constraints
**Alternatives considered:** Fixed limits, no limits with monitoring
**Chosen:** Adaptive approach with usage-based throttling

#### Decision: Authentication Flow
**Rationale:** Anonymous access with optional account creation
**Alternatives considered:** Required authentication, no authentication
**Chosen:** Optional authentication for personalization features only

#### Decision: Docusaurus RAG Integration
**Rationale:** Custom plugin for select-text → Ask AI functionality
**Alternatives considered:** External widgets, separate UI
**Chosen:** Integrated approach with custom Docusaurus plugin

#### Decision: Embedding Models
**Rationale:** Lightweight models for free-tier efficiency
**Alternatives considered:** Heavy models with quantization, API-based
**Chosen:** Sentence Transformers with efficient models

## Phase 1: Data Model

### Core Entities

#### User
- id (UUID)
- email (optional)
- preferences (JSON)
- progress (JSON)
- created_at (timestamp)
- updated_at (timestamp)

#### Chapter
- id (UUID)
- title (string)
- content (markdown text)
- order (integer)
- word_count (integer)
- created_at (timestamp)
- updated_at (timestamp)

#### Embedding
- id (UUID)
- chapter_id (UUID - foreign key)
- content (text snippet)
- embedding_vector (vector)
- token_count (integer)
- created_at (timestamp)

#### ChatSession
- id (UUID)
- user_id (UUID - optional foreign key)
- created_at (timestamp)
- updated_at (timestamp)

#### ChatMessage
- id (UUID)
- session_id (UUID - foreign key)
- role (enum: user, assistant)
- content (text)
- created_at (timestamp)

### Relationships
- User (1) → (0..*) ChatSession
- Chapter (1) → (0..*) Embedding
- ChatSession (1) → (0..*) ChatMessage

## Phase 1: API Contracts

### Authentication Endpoints

#### POST /api/auth/register
Register a new user
```json
{
  "email": "string",
  "password": "string"
}
```

#### POST /api/auth/login
Login user
```json
{
  "email": "string",
  "password": "string"
}
```

### Chapter Endpoints

#### GET /api/chapters
Get all textbook chapters
```json
[
  {
    "id": "string",
    "title": "string",
    "order": 0,
    "word_count": 0
  }
]
```

#### GET /api/chapters/{id}
Get specific chapter content
```json
{
  "id": "string",
  "title": "string",
  "content": "string",
  "order": 0
}
```

### RAG Endpoints

#### POST /api/rag/query
Query textbook content with RAG
```json
{
  "query": "string",
  "session_id": "string (optional)"
}
```
Response:
```json
{
  "response": "string",
  "sources": ["string"],
  "session_id": "string"
}
```

### User Preference Endpoints

#### GET /api/user/preferences
Get user preferences
```json
{
  "language": "string",
  "theme": "string",
  "personalization_enabled": "boolean"
}
```

#### PUT /api/user/preferences
Update user preferences
```json
{
  "language": "string",
  "theme": "string",
  "personalization_enabled": "boolean"
}
```

## Phase 1: Quickstart Guide

### Development Setup

1. **Prerequisites**
   - Node.js 18+ (for Docusaurus)
   - Python 3.11+ (for FastAPI backend)
   - Git

2. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Environment Variables**
   Create `.env` file in backend directory:
   ```env
   NEON_DATABASE_URL=your_neon_db_url
   QDRANT_URL=your_qdrant_url
   OPENAI_API_KEY=your_openai_key
   ```

6. **Run Applications**
   ```bash
   # Frontend
   cd frontend && npm run start

   # Backend
   cd backend && python -m uvicorn main:app --reload
   ```

### Deployment

1. **Frontend Deployment**
   - Build: `npm run build`
   - Deploy to GitHub Pages or Netlify

2. **Backend Deployment**
   - Deploy to Railway or Vercel
   - Configure environment variables
   - Set up Neon and Qdrant connections

## Phase 2: Implementation Tasks

### Sprint 1: Core Infrastructure
- [ ] Set up Docusaurus project with basic layout
- [ ] Create chapter content in markdown format
- [ ] Implement auto sidebar generation
- [ ] Set up FastAPI backend with basic endpoints
- [ ] Connect to Neon database

### Sprint 2: RAG System
- [ ] Implement embedding generation for textbook content
- [ ] Set up Qdrant vector store
- [ ] Create RAG query functionality
- [ ] Implement similarity search
- [ ] Connect RAG to Docusaurus frontend

### Sprint 3: User Features
- [ ] Implement user authentication system
- [ ] Add personalization features
- [ ] Create progress tracking
- [ ] Add Urdu translation capability
- [ ] Implement select-text → Ask AI functionality

### Sprint 4: Polish & Deploy
- [ ] Add error handling and fallback strategies
- [ ] Implement rate limiting
- [ ] Add caching mechanisms
- [ ] Performance optimization
- [ ] Deploy to production

## Risk Assessment & Mitigation

### High-Risk Areas
1. **Rate Limiting**: Implement adaptive throttling to stay within free-tier limits
2. **Performance**: Use caching and efficient embedding models
3. **Data Consistency**: Implement proper transaction handling between Neon and Qdrant

### Mitigation Strategies
- Comprehensive monitoring and alerting
- Graceful degradation when services are unavailable
- Circuit breaker patterns for external API calls
- Regular backup of content and user data

## Success Criteria

### Functional Requirements
- [ ] Complete textbook with 6 chapters rendered in Docusaurus
- [ ] Auto-generated sidebar navigation working correctly
- [ ] RAG chatbot responding to queries based on textbook content
- [ ] Text selection triggering AI assistant functionality
- [ ] All content accessible and properly formatted
- [ ] Search functionality working across all chapters

### Non-Functional Requirements
- [ ] Page load times under 3 seconds
- [ ] RAG responses under 5 seconds
- [ ] Free-tier resource usage compliance
- [ ] Mobile-responsive design
- [ ] Accessibility compliance (WCAG 2.1 AA)
- [ ] Cross-browser compatibility

## Post-Implementation Review

### Re-evaluation of Constitution Alignment
- [ ] Verify all principles maintained after implementation
- [ ] Confirm free-tier compliance
- [ ] Validate RAG-focused approach (no external data sources)
- [ ] Ensure minimalism and simplicity preserved

### Performance Benchmarks
- [ ] Measure actual page load times
- [ ] Test RAG response times under load
- [ ] Validate embedding efficiency
- [ ] Verify rate limiting effectiveness