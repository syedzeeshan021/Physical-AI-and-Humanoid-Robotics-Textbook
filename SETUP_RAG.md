# RAG Chatbot Setup Guide

## Prerequisites
- Docker installed
- Python 3.9+
- Your `.env` file configured with API keys

## Step 1: Start Qdrant Vector Database

### Option A: Docker (Recommended)
```bash
# Windows - In cmd.exe
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant

# Verify it's running
docker logs qdrant
```

### Option B: Local Installation
If you prefer running Qdrant locally without Docker, follow: https://qdrant.tech/documentation/quick-start/

### Verify Qdrant is Running
```bash
# Test the API
curl http://localhost:6333/health
```

Expected response:
```json
{"status":"ok"}
```

---

## Step 2: Populate Vector Store with Textbook Data

### Run the Initialization Script
```bash
# Navigate to backend
cd e:\GIAIC Q4 AGENTIC AI\PIAHR\backend

# Install dependencies if needed
pip install -r requirements.txt

# Run initialization
python -m scripts.populate_vector_store
```

This will:
1. Connect to your Neon PostgreSQL database
2. Fetch all textbook chapters
3. Generate embeddings using `sentence-transformers`
4. Store embeddings in Qdrant

---

## Step 3: Start the Backend Server

```bash
# In the backend directory
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
Uvicorn running on http://0.0.0.0:8000
```

---

## Step 4: Start the Frontend

```bash
# In a new terminal, navigate to frontend
cd e:\GIAIC Q4 AGENTIC AI\PIAHR\frontend

# Install dependencies if needed
npm install

# Start development server
npm start
```

The frontend will open at `http://localhost:3000`

---

## Step 5: Test the RAG Chatbot

1. Open the chat widget in the bottom right
2. Ask a question like: "What is Physical AI?"
3. The bot should:
   - Retrieve relevant textbook sections
   - Generate an answer using GPT-3.5-turbo
   - Show sources

---

## Troubleshooting

### Qdrant Connection Failed
```bash
# Check if container is running
docker ps | grep qdrant

# If not running, restart it
docker start qdrant

# Check logs
docker logs qdrant
```

### OpenAI API Error
- Verify `OPENAI_API_KEY` in `.env`
- Check you have API credits available
- Ensure the key is valid

### No embeddings returned
- Run the population script again
- Check Qdrant is populated: `http://localhost:6333/dashboard`
- Verify database connection

### Database connection error
- Test Neon connection string
- Run: `python -c "import psycopg2; psycopg2.connect(your_connection_string)"`

---

## System Architecture

```
Frontend (React/Docusaurus)
    ↓
API Service (http://localhost:8000/api/v1)
    ↓
Backend (FastAPI)
    ├── RAG Service
    │   ├── Query Encoder (sentence-transformers)
    │   ├── Vector Search (Qdrant)
    │   └── LLM (OpenAI GPT-3.5)
    ├── Vector Store (Qdrant)
    └── Database (Neon PostgreSQL)
```

---

## Environment Variables Needed

Make sure your `.env` file has:
```
NEON_DATABASE_URL=your_connection_string
OPENAI_API_KEY=sk-your-key
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Rl11juPrzKye1MaYlAKqh7PVQKOwcF1f25VwW6xhwrQ
SECRET_KEY=your-jwt-secret
```

---

## Next Steps

Once RAG is working:
1. Add more textbook chapters to the database
2. Fine-tune embedding model for better results
3. Implement conversation memory
4. Add authentication to the chatbot
5. Deploy to production (Railway, Vercel, etc.)
