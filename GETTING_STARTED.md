# 🚀 GETTING STARTED - 5 Minute Quick Start

**Welcome to PIAHR RAG Chatbot!** This file will get you running in 5 minutes.

---

## ⚡ Start Here (Choose One)

### Option 1: Automated Setup (Easiest) ⭐ RECOMMENDED
```bash
cd "e:\GIAIC Q4 AGENTIC AI\PIAHR"
python setup_rag.py
```
**Time:** 2-3 minutes  
**Difficulty:** ⭐ Super Easy

### Option 2: Windows Quick Launcher
```bash
# Double-click this file
QUICK_START.bat
```
**Time:** 2-3 minutes  
**Difficulty:** ⭐ Super Easy

### Option 3: Manual Commands
```bash
# Terminal 1 - Qdrant
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant

# Terminal 2 - Backend
cd backend
python -m uvicorn src.main:app --reload

# Terminal 3 - Frontend
cd frontend
npm install
npm start
```
**Time:** 5-10 minutes  
**Difficulty:** ⭐⭐ Medium

---

## ✅ Prerequisites Check

Before starting, verify you have:
```bash
docker --version       # Should show version
python --version       # Should show 3.9+
node --version         # Should show 18+
```

If any are missing, install:
- Docker: https://www.docker.com/products/docker-desktop
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

---

## 🎯 What Happens When You Run Setup

```
Step 1: Start Qdrant in Docker
        ✓ Vector database ready

Step 2: Initialize Database
        ✓ Chapters loaded
        ✓ Users table ready

Step 3: Generate Embeddings
        ✓ All textbook content indexed
        ✓ Vector store populated

Step 4: Ready to Launch!
        ✓ Backend configured
        ✓ Frontend configured
```

**Total time:** 2-3 minutes

---

## 🚀 After Setup - Start the Services

### Terminal 1: Start Backend
```bash
cd backend
python -m uvicorn src.main:app --reload
```

Expected output:
```
Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm start
```

Expected output:
```
Compiled successfully!
Local:  http://localhost:3000
```

---

## 🎯 Access Points

Once running, you have access to:

| What | URL |
|------|-----|
| Chat Interface | http://localhost:3000 |
| API Docs | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

## 💬 Using the Chatbot

1. Open http://localhost:3000
2. Look for the chat bubble in the **bottom-right corner**
3. Type a question like:
   - "What is Physical AI?"
   - "Explain humanoid robotics"
   - "What is ROS 2?"
4. Get AI-generated answers with sources!

---

## ✨ Example Interaction

```
You:  "What is Physical AI?"

Bot:  "Physical AI is an emerging field that combines 
       artificial intelligence with physical systems and 
       robotics. It represents the intersection of machine 
       learning, robotics, and embodied intelligence..."

Sources: [Introduction to Physical AI]
```

---

## 🔧 Troubleshooting (Quick Fixes)

### Docker not found
```bash
# Install Docker Desktop
# https://www.docker.com/products/docker-desktop
```

### Port already in use
```bash
# Change port
PORT=3001 npm start    # Frontend on 3001
```

### .env file not found
```bash
# Copy the example
copy backend\.env.example backend\.env
```

### OpenAI API error
```bash
# Check you have credits
# https://platform.openai.com/account/billing/overview
```

### Qdrant connection failed
```bash
# Check if running
docker ps | findstr qdrant

# If not, restart
docker start qdrant
```

---

## 📚 Documentation

Need more info? Read these:

| Document | Purpose |
|----------|---------|
| INDEX.md | Navigation hub |
| README_RAG_SETUP.md | Complete guide |
| QUICK_REFERENCE.md | Command reference |
| SETUP_COMPLETE.md | Troubleshooting |

---

## ✅ Success Checklist

Your system is working when:

- [ ] `setup_rag.py` completes without errors
- [ ] Backend shows "Uvicorn running"
- [ ] Frontend loads at localhost:3000
- [ ] Chat widget appears (bottom-right)
- [ ] You can type a question
- [ ] Bot responds with an answer
- [ ] Answer includes source attribution

---

## 🎓 What You Can Do Now

- ✓ Ask questions about Physical AI & Robotics
- ✓ Get AI-powered answers
- ✓ See where information comes from
- ✓ Handle multiple questions
- ✓ Test the vector search

---

## 📊 Architecture in 30 Seconds

```
You ask a question
    ↓
Frontend sends to backend
    ↓
Backend searches vector database
    ↓
Retrieves relevant textbook sections
    ↓
Sends to OpenAI for answer generation
    ↓
Returns answer + sources
    ↓
You see the response with references
```

---

## 💾 File Locations

Important files:
```
e:\GIAIC Q4 AGENTIC AI\PIAHR\
├── setup_rag.py              ← Run this
├── QUICK_START.bat           ← Or this (Windows)
├── backend\.env              ← Config file
├── backend\src\main.py       ← Backend entry
└── frontend\src\index.tsx    ← Frontend entry
```

---

## 🎯 Common Questions

**Q: How long does setup take?**  
A: 2-3 minutes first time, 10 seconds after

**Q: Does it work offline?**  
A: No, needs internet for OpenAI API

**Q: How much does it cost?**  
A: ~$0.01 per question (OpenAI API costs)

**Q: Can I add more chapters?**  
A: Yes, edit `backend/src/utils/initialize_content.py`

**Q: Is it secure?**  
A: Yes, JWT auth + rate limiting + API key protection

---

## 🚀 Ready? Let's Go!

Run this now:
```bash
python setup_rag.py
```

Then open: http://localhost:3000

---

## 📞 Quick Help

| Need | Action |
|------|--------|
| System overview | Read: INDEX.md |
| Full setup guide | Read: README_RAG_SETUP.md |
| Command reference | Read: QUICK_REFERENCE.md |
| Fix something | Read: SETUP_COMPLETE.md |
| See diagrams | Read: VISUAL_GUIDE.md |

---

## ✨ Special Features

- 🤖 AI-powered answers
- 🔍 Semantic search  
- 📚 Source attribution
- ⚡ Fast responses
- 🔒 Secure API
- 📈 Scalable
- 🎯 Production-ready

---

## 🎯 Next Steps After Starting

1. ✓ Test with a few questions
2. ✓ Check answer quality
3. ✓ Review source attribution
4. ✓ Monitor performance
5. ✓ Plan deployment

---

## 🏁 You're Ready!

Everything is configured. Pick your start method above and begin!

**Easiest:** `python setup_rag.py`

**Have fun! 🚀**

---

**Questions?** Check the documentation files listed above.

**Status:** 🟢 Ready to Run

**Time to First Chat:** 5 minutes
