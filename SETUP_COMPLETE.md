# PIAHR RAG Chatbot - Complete Setup Guide

This guide will help you set up and run the RAG (Retrieval-Augmented Generation) chatbot system.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              http://localhost:3000                       │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│            Backend API (FastAPI)                        │
│         http://localhost:8000/api/v1                    │
├──────────────────────────────────────────────────────────┤
│  RAG Service                                            │
│  ├─ Query Processing                                   │
│  ├─ Embedding Generation (sentence-transformers)       │
│  ├─ Vector Search (Qdrant)                            │
│  └─ LLM Response (OpenAI GPT-3.5)                      │
├──────────────────────────────────────────────────────────┤
│  Supporting Services                                    │
│  ├─ PostgreSQL/Neon Database                           │
│  ├─ Qdrant Vector Store                               │
│  └─ Chapter Management                                 │
└──────────────────────────────────────────────────────────┘
```

## Prerequisites

### Required Software
- **Docker Desktop** - For running Qdrant
  - Download: https://www.docker.com/products/docker-desktop
  - Required for Windows: WSL 2 Backend
  
- **Python 3.9+**
  - Download: https://www.python.org/downloads/
  
- **Node.js 18+** (for frontend only)
  - Download: https://nodejs.org/

### Required Accounts
- **OpenAI API** with credits
  - Get your API key: https://platform.openai.com/api-keys
  
- **Neon Database** (PostgreSQL hosting)
  - Already set up at: https://console.neon.tech

## Quick Start (3 Steps)

### Step 1: Prepare Environment Variables

Create `.env` file in `backend/` directory with:
```bash
# Database (already configured)
NEON_DATABASE_URL=postgresql://neondb_owner:npg_HgUqRFsf60Ki@ep-patient-mud-ahcxg3t7-pooler.c-3.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require
DATABASE_URL=postgresql://neondb_owner:npg_HgUqRFsf60Ki@ep-patient-mud-ahcxg3t7-pooler.c-3.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require

# Vector Store
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# OpenAI (already configured)
OPENAI_API_KEY=your_openai_api_key_here

# JWT (already configured)
SECRET_KEY=your_secure_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Settings
DEBUG=true
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=["*"]
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

### Step 2: Run Setup Script

**On Windows (CMD):**
```bash
cd e:\GIAIC Q4 AGENTIC AI\PIAHR
python setup_rag.py
```

**On Mac/Linux:**
```bash
cd "e:/GIAIC Q4 AGENTIC AI/PIAHR"
python setup_rag.py
```

This will automatically:
- ✓ Start Qdrant in Docker
- ✓ Initialize textbook content in database
- ✓ Generate embeddings for all chapters
- ✓ Store embeddings in Qdrant vector store

**Expected Duration:** 2-3 minutes

### Step 3: Start Services

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # Only needed first time
npm start
```

You should see:
```
Compiled successfully!
Local: http://localhost:3000
```

## Accessing the System

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | http://localhost:3000 | Chat interface & textbook |
| Backend API | http://localhost:8000/api/v1 | API endpoints |
| API Docs | http://localhost:8000/docs | Interactive Swagger UI |
| Qdrant Dashboard | http://localhost:6333/dashboard | Vector store management |

## Using the Chatbot

1. **Open Frontend:** http://localhost:3000
2. **Look for Chat Widget** in the bottom-right corner
3. **Ask Questions:** "What is Physical AI?" or "Explain humanoid robotics"
4. **View Sources:** The bot shows which textbook chapters it retrieved from

## Testing RAG Functionality

### Test 1: Check Vector Store
```bash
curl http://localhost:6333/health
```

Expected: `{"status":"ok"}`

### Test 2: Check Backend API
```bash
curl http://localhost:8000/api/v1/chapters
```

Expected: JSON array of chapters

### Test 3: Query RAG Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?", "session_id": "test-123"}'
```

Expected: RAG response with sources

## Troubleshooting

### Docker Issues

**Qdrant won't start:**
```bash
# Check Docker status
docker ps

# Check logs
docker logs qdrant

# Kill and restart
docker stop qdrant
docker rm qdrant
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant
```

### Database Connection

**PostgreSQL/Neon error:**
```bash
# Test connection
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://neondb_owner:npg_HgUqRFsf60Ki@...')
print('Connected!')
"
```

### API/OpenAI Issues

**OpenAI API error:**
- Verify `OPENAI_API_KEY` is correct
- Check you have API credits: https://platform.openai.com/account/billing/overview
- Ensure key has correct permissions

**No embeddings returned:**
- Run setup script again: `python setup_rag.py`
- Check Qdrant dashboard for collections
- Verify database has chapter content

### Frontend Issues

**Port 3000 in use:**
```bash
# Find process using port 3000 (Windows)
netstat -ano | findstr :3000

# Kill process
taskkill /PID <PID> /F

# Or use different port
PORT=3001 npm start
```

## Advanced Operations

### Manually Populate Vector Store
```bash
cd backend
python scripts/populate_vector_store.py
```

### Add More Chapters
Edit `backend/src/utils/initialize_content.py` and add chapter content, then re-run setup.

### Monitor Vector Store
Visit: http://localhost:6333/dashboard

### View API Documentation
Visit: http://localhost:8000/docs

### Check Backend Logs
Look for files in `backend/logs/` directory

## Performance Optimization

### For Faster Embeddings
Reduce chunk size in `populate_vector_store.py`:
```python
chunk_size = 250  # Instead of 500
```

### For Better RAG Accuracy
- Add more textbook content
- Use a larger embedding model:
  ```python
  self.encoder = SentenceTransformer('all-mpnet-base-v2')  # Better but slower
  ```

### For Production
- Use GPU for embeddings
- Set up async workers: `--workers 4`
- Add authentication to API
- Use HTTPS
- Set `DEBUG=false`

## Deployment

### To Railway (recommended for full stack)
1. Create Railway account: https://railway.app
2. Create new project
3. Deploy backend from `railway.toml`
4. Deploy frontend to Vercel

### To Docker Compose
See `docker-compose.yml` (coming soon)

## Support

For issues:
1. Check logs in `backend/logs/`
2. Verify `.env` configuration
3. Ensure all services are running
4. Check internet connection for API calls

## Next Steps

After successful setup:
1. Add user authentication
2. Implement conversation memory
3. Fine-tune RAG with feedback
4. Deploy to production
5. Monitor performance and costs

---

**Last Updated:** December 8, 2025  
**System Status:** ✓ Ready for deployment
