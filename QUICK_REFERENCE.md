# PIAHR RAG System - Quick Reference

## 🚀 Quick Start Commands

```bash
# 1. Setup everything automatically
cd "e:\GIAIC Q4 AGENTIC AI\PIAHR"
python setup_rag.py

# 2. Start Backend (Terminal 1)
cd backend
python -m uvicorn src.main:app --reload

# 3. Start Frontend (Terminal 2)
cd frontend
npm start

# 4. Access the system
Frontend:    http://localhost:3000
Backend API: http://localhost:8000/api/v1
API Docs:    http://localhost:8000/docs
Qdrant:      http://localhost:6333/dashboard
```

## 🐳 Docker Commands

```bash
# Start Qdrant
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant

# Check status
docker ps

# View logs
docker logs qdrant

# Stop Qdrant
docker stop qdrant

# Remove container
docker rm qdrant
```

## 📝 Directory Structure

```
PIAHR/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── services/       # Business logic (RAG, chapters)
│   │   ├── core/           # Config, database, vector store
│   │   └── models/         # Data models
│   ├── scripts/
│   │   └── populate_vector_store.py   # Populate embeddings
│   └── .env                # Environment variables
├── frontend/               # React/Docusaurus frontend
│   ├── src/components/ChatWidget    # Chat component
│   └── .env               # Frontend config
├── setup_rag.py           # One-command setup
├── README_RAG_SETUP.md    # Full documentation
└── SETUP_COMPLETE.md      # Setup guide
```

## 🔑 Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/rag/query` | POST | Query the RAG system |
| `/api/v1/chapters` | GET | Get all chapters |
| `/api/v1/chapters/{id}` | GET | Get specific chapter |
| `/docs` | GET | Swagger API documentation |

## 📊 RAG Query Example

```bash
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is humanoid robotics?",
    "session_id": "session-123"
  }'
```

Response:
```json
{
  "response": "Humanoid robots are designed to resemble and mimic human behavior...",
  "sources": ["Basics of Humanoid Robotics"],
  "session_id": "session-123"
}
```

## 🛠️ Configuration

### Required Environment Variables (.env)

```bash
# Database (already set)
NEON_DATABASE_URL=postgresql://...
DATABASE_URL=postgresql://...

# Vector Store (already set)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=...

# OpenAI (already set)
OPENAI_API_KEY=sk-proj-...

# JWT (already set)
SECRET_KEY=Ey7kL9mN2pQ4rT6vW8xZ1aB3...
```

## 🧪 Testing Commands

```bash
# Test Qdrant health
curl http://localhost:6333/health

# Test Backend health
curl http://localhost:8000/health

# Test Chapters endpoint
curl http://localhost:8000/api/v1/chapters

# Test RAG endpoint
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query":"test query"}'
```

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 3000 in use | `netstat -ano \| findstr :3000` then kill process |
| Docker not found | Install Docker Desktop |
| .env not found | Copy from .env.example |
| Qdrant connection error | Ensure Docker container is running |
| API key invalid | Check OpenAI platform for valid key |
| Database error | Test Neon connection string |

## 📚 Key Technologies

- **Frontend:** React, TypeScript, Docusaurus
- **Backend:** FastAPI, Python
- **Database:** PostgreSQL (Neon)
- **Vector Store:** Qdrant
- **Embeddings:** sentence-transformers
- **LLM:** OpenAI GPT-3.5-turbo
- **Container:** Docker

## 🎯 Development Workflow

1. **Backend Development:**
   - Edit files in `backend/src/`
   - Changes auto-reload with `--reload` flag
   - Check logs for errors

2. **Frontend Development:**
   - Edit files in `frontend/src/`
   - Hot reload enabled
   - Test in ChatWidget component

3. **Vector Store:**
   - Modify `backend/scripts/populate_vector_store.py`
   - Rerun to update embeddings

## 📈 Performance Tips

- Use GPU for faster embeddings (requires CUDA)
- Increase worker threads for API
- Cache frequently asked questions
- Monitor Qdrant performance on dashboard

## 🔐 Security Reminders

- ✓ Never commit `.env` file
- ✓ Use different keys for production
- ✓ Rotate API keys regularly
- ✓ Use HTTPS in production
- ✓ Enable authentication for API

## 📞 Useful Links

- OpenAI: https://platform.openai.com
- Neon: https://console.neon.tech
- Qdrant: http://localhost:6333/dashboard
- FastAPI: http://localhost:8000/docs
- React: http://localhost:3000

## 🚢 Deployment Checklist

- [ ] Set DEBUG=false in production
- [ ] Use environment-specific configs
- [ ] Set up proper CORS for frontend domain
- [ ] Enable HTTPS
- [ ] Set up monitoring/logging
- [ ] Configure backup strategy
- [ ] Test failover scenarios
- [ ] Document deployment process

---

**Quick Help:** `python setup_rag.py`  
**API Docs:** http://localhost:8000/docs  
**Status:** 🟢 Ready to run
