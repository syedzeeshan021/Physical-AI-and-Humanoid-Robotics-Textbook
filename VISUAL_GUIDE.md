# PIAHR RAG System - Visual Guide

## 🎯 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                        (React Frontend)                             │
│                    http://localhost:3000                            │
├──────────────────────────┬──────────────────────────────────────────┤
│   Docusaurus Textbook    │    Chat Widget (Bottom-Right)           │
│   - Chapters             │    - User Input                          │
│   - Navigation           │    - AI Response                         │
│   - Search               │    - Source Attribution                  │
└──────────────────────────┴─────────────────┬──────────────────────┘
                                             │
                                   HTTP Request/Response
                                             │
┌──────────────────────────────────────────▼─────────────────────────┐
│                      BACKEND API (FastAPI)                          │
│                    http://localhost:8000                            │
├───────────────────────────────────────────────────────────────────┤
│  Endpoints:                                                        │
│  POST /api/v1/rag/query          ← Main RAG query endpoint       │
│  GET  /api/v1/chapters           ← List all chapters             │
│  GET  /api/v1/chapters/{id}      ← Get specific chapter          │
│  GET  /docs                      ← API documentation             │
└──────────────────────────────────────────────────────────────────┘
         │                              │                    │
         │                              │                    │
         ▼                              ▼                    ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────┐
│   RAG Service        │  │  Chapter Service     │  │ Database     │
│ (Query Processing)   │  │ (Content Management) │  │ (Neon PG)    │
├──────────────────────┤  ├──────────────────────┤  ├──────────────┤
│ 1. Encode Query      │  │ - Load chapters      │  │ Tables:      │
│ 2. Search Vector DB  │  │ - Cache content      │  │ - chapters   │
│ 3. Get Context       │  │ - Validate data      │  │ - users      │
│ 4. Call OpenAI       │  │                      │  │ - sessions   │
│ 5. Format Response   │  │                      │  │              │
└──────────┬───────────┘  └──────────────────────┘  └──────────────┘
           │
           ├─────────────────────┬─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
    ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
    │ Vector Store   │  │ Embeddings     │  │ OpenAI API     │
    │ (Qdrant)       │  │ (sentence-     │  │ (GPT-3.5)      │
    │                │  │  transformers) │  │                │
    ├────────────────┤  ├────────────────┤  ├────────────────┤
    │ Collections:   │  │ Model:         │  │ Features:      │
    │ - textbook_    │  │ all-MiniLM-    │  │ - Chat         │
    │   embeddings   │  │ L6-v2          │  │ - 4K context   │
    │                │  │                │  │ - Streaming    │
    │ Dashboard:     │  │ Output:        │  │                │
    │ localhost:6333 │  │ 384-dim        │  │ Rate Limited   │
    │               │  │ vectors        │  │                │
    └────────────────┘  └────────────────┘  └────────────────┘
```

---

## 🔄 Query Processing Flow

```
USER ASKS QUESTION
    │
    ▼
┌─────────────────────────────────────┐
│ Question received in ChatWidget     │
│ "What is Physical AI?"              │
└────────────┬────────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │ API Service Client │
    │ (Frontend)         │
    └────────┬───────────┘
             │
             │ HTTP POST
             │ /api/v1/rag/query
             │
             ▼
    ┌────────────────────────────────────────┐
    │ FastAPI Backend receives request       │
    │ - Parse query                          │
    │ - Validate input                       │
    │ - Generate user message ID             │
    └────────┬─────────────────────────────┘
             │
             ▼
    ┌────────────────────────────────────────┐
    │ RAG Service - Step 1: Encoding         │
    │ "What is Physical AI?"                 │
    │         ↓                              │
    │ sentence-transformers.encode()         │
    │         ↓                              │
    │ [0.123, -0.456, 0.789, ...] (384-dim) │
    └────────┬─────────────────────────────┘
             │
             ▼
    ┌────────────────────────────────────────┐
    │ RAG Service - Step 2: Vector Search    │
    │ Query Qdrant for similar embeddings    │
    │         ↓                              │
    │ Search Results (Top 3):                │
    │ 1. "Physical AI is..." (score: 0.95)   │
    │ 2. "Embodied cognition..." (0.89)      │
    │ 3. "Intelligence and robots..." (0.87) │
    └────────┬─────────────────────────────┘
             │
             ▼
    ┌────────────────────────────────────────┐
    │ RAG Service - Step 3: Context Assembly │
    │                                        │
    │ From Database:                         │
    │ - Chapter: "Introduction to Physical  │
    │   AI"                                  │
    │ - Content chunks                       │
    │ - Metadata                             │
    └────────┬─────────────────────────────┘
             │
             ▼
    ┌────────────────────────────────────────┐
    │ RAG Service - Step 4: Prompt Building  │
    │                                        │
    │ Prompt:                                │
    │ "You are an AI assistant for a        │
    │  textbook on Physical AI & Robotics.  │
    │                                        │
    │  Context: [Retrieved textbook content] │
    │                                        │
    │  Question: What is Physical AI?       │
    │                                        │
    │  Answer:"                              │
    └────────┬─────────────────────────────┘
             │
             │ HTTP Request
             │ (streaming)
             ▼
    ┌────────────────────────────────────────┐
    │ OpenAI GPT-3.5-turbo API                │
    │ Processing...                           │
    │ (1-3 seconds)                           │
    └────────┬─────────────────────────────┘
             │
             │ Streamed Response
             ▼
    ┌────────────────────────────────────────┐
    │ RAG Service - Step 5: Parse Response   │
    │                                        │
    │ Answer: "Physical AI is an emerging   │
    │ field that combines artificial        │
    │ intelligence with physical systems..."│
    │                                        │
    │ Sources: [                             │
    │   "Introduction to Physical AI",      │
    │   "Basics of Humanoid Robotics"       │
    │ ]                                      │
    └────────┬─────────────────────────────┘
             │
             │ JSON Response
             ▼
    ┌────────────────────────────────────────┐
    │ Frontend receives response             │
    │ ChatWidget displays answer             │
    │ Shows source attributions              │
    └────────┬─────────────────────────────┘
             │
             ▼
    ANSWER DISPLAYED TO USER
```

---

## 📁 Key File Structure

```
PIAHR/
│
├── 📄 setup_rag.py              ← START HERE (Automated setup)
├── 📄 README_RAG_SETUP.md       ← Complete guide
├── 📄 QUICK_REFERENCE.md        ← Quick commands
├── 📄 SETUP_SUMMARY.md          ← This system overview
│
├── backend/
│   ├── 📄 .env                  ← Configuration (API keys)
│   ├── 📄 requirements.txt       ← Python dependencies
│   ├── 📄 main.py               ← FastAPI app entry
│   │
│   ├── scripts/
│   │   └── 📄 populate_vector_store.py  ← Populate embeddings
│   │
│   └── src/
│       ├── api/
│       │   ├── rag.py          ← RAG endpoint
│       │   ├── chapters.py      ← Chapter endpoints
│       │   └── users.py         ← User endpoints
│       │
│       ├── services/
│       │   ├── rag_service.py   ← RAG logic (MAIN)
│       │   ├── chapter_service.py
│       │   └── search_service.py
│       │
│       ├── core/
│       │   ├── config.py        ← Settings from .env
│       │   ├── database.py      ← Database connection
│       │   ├── vector_store.py  ← Qdrant client (MODIFIED)
│       │   └── logging.py
│       │
│       ├── models/
│       │   ├── chapter.py
│       │   ├── user.py
│       │   └── chat_message.py
│       │
│       └── utils/
│           ├── initialize_content.py  ← Sample data
│           └── cache.py
│
├── frontend/
│   ├── 📄 package.json
│   ├── 📄 .env (optional)
│   │
│   └── src/
│       ├── components/
│       │   └── ChatWidget/      ← Chat interface
│       │       ├── index.tsx
│       │       └── styles.module.css
│       │
│       └── services/
│           └── api.ts           ← API client
│
└── docs/                        ← Documentation files
    ├── SETUP_COMPLETE.md
    ├── SETUP_RAG.md
    └── QUICK_START.bat
```

---

## 🚀 Execution Timeline

### First Time Setup (2-3 minutes)
```
0:00  $ python setup_rag.py
      ↓
0:10  ✓ Docker check passed
      ✓ Qdrant starting...
      ↓
0:45  ✓ Qdrant ready
      ✓ Database initialized
      ↓
1:15  ✓ Generating embeddings... (Processing chapters)
      ✓ Chunk 1/142... 2/142... 3/142... (progress)
      ↓
2:30  ✓ Vector store populated (142 chunks indexed)
      ✓ Ready to start services
      
Next: Start backend and frontend in separate terminals
```

### Subsequent Runs (10 seconds)
```
0:00  $ python setup_rag.py
0:05  ✓ Qdrant already running
0:08  ✓ Database already initialized
0:10  Ready to start!
```

---

## 🧠 Data Flow Summary

```
Components:                  Communication:
┌──────────────┐            HTTP/REST
│   Frontend   │ ◄──────► ┌──────────────┐
│   (React)    │          │   Backend    │
└──────────────┘          │   (FastAPI)  │
                          └──┬───────┬──┘
                             │       │
                          Python Client (asyncio)
                             │       │
                    ┌────────▼┐    ┌▼─────────┐
                    │ Qdrant  │    │ OpenAI   │
                    │(Vectors)│    │  (LLM)   │
                    └─────────┘    └──────────┘
                             ▲
                             │
                       PostgreSQL
                       Connection
                             │
                    ┌────────▼────────┐
                    │ Neon Database   │
                    │  (Chapters &    │
                    │   Users)        │
                    └─────────────────┘
```

---

## 📊 Query Latency Breakdown

```
User Question
    ↓ (< 10ms)
ChatWidget sends request via HTTP
    ↓ (< 50ms)
FastAPI receives and routes to RAG endpoint
    ↓ (< 20ms)
Encode query with sentence-transformers
    ↓ (< 100ms)
Search Qdrant for similar vectors
    ↓ (< 50ms)
Retrieve context from database
    ↓ (< 50ms)
Build prompt and send to OpenAI
    ↓ (1000-3000ms)
OpenAI processes and returns response
    ↓ (< 50ms)
Parse and format response
    ↓ (< 10ms)
Send JSON response to frontend
    ↓ (< 50ms)
ChatWidget displays answer with sources

TOTAL: 2-5 seconds
```

---

## 🔑 Key Decisions Made

| Decision | Why |
|----------|-----|
| HTTP (not gRPC) | Better compatibility with Windows/local |
| sentence-transformers | Lightweight, fast, good quality |
| all-MiniLM-L6-v2 | Balance speed/accuracy (384-dim) |
| GPT-3.5-turbo | Cost-effective, good quality |
| Docusaurus | Built-in textbook capabilities |
| FastAPI | Modern, async, fast |
| Neon | Serverless PostgreSQL, low cost |
| Docker for Qdrant | Easy to manage, no installation |

---

## ✅ System Ready Checklist

```
Infrastructure:
  ✓ PostgreSQL database available
  ✓ OpenAI API key with credits
  ✓ Qdrant vector database configured
  ✓ All environment variables set

Backend:
  ✓ FastAPI service configured
  ✓ RAG service with real embeddings
  ✓ Database connections working
  ✓ API endpoints defined

Frontend:
  ✓ React application ready
  ✓ ChatWidget component integrated
  ✓ API client configured
  ✓ Styling complete

Automation:
  ✓ setup_rag.py script ready
  ✓ populate_vector_store.py script ready
  ✓ Error handling implemented

Documentation:
  ✓ Setup guides written
  ✓ Quick reference created
  ✓ Troubleshooting guide provided
  ✓ Visual diagrams included
```

---

## 🎯 You Are Ready!

Everything is configured and ready to run. Choose one:

1. **Automated:** `python setup_rag.py`
2. **Manual:** Follow `QUICK_REFERENCE.md`
3. **Windows:** Double-click `QUICK_START.bat`

---

**Status:** 🟢 Production Ready  
**Last Updated:** December 8, 2025
