# 🚀 PIAHR RAG - Setup WITHOUT Docker (Alternative Method)

**For users who don't have Docker or prefer local setup**

---

## 📋 Prerequisites

Instead of Docker, we'll run Qdrant locally. You need:

- Python 3.9+
- PostgreSQL (or Neon database - already configured)
- Qdrant (installed locally)
- Node.js 18+ (for frontend)

---

## 🔧 Option 1: Using Qdrant Cloud (Easiest - No Installation)

### Step 1: Create Free Qdrant Cloud Account
1. Visit: https://cloud.qdrant.io
2. Sign up for free account
3. Create a new cluster

### Step 2: Update Configuration
Edit `backend/.env`:
```
QDRANT_URL=https://your-cluster-url:6333
QDRANT_API_KEY=your-api-key
```

### Step 3: Run Setup
```bash
# Skip Docker, go straight to backend setup
cd backend
python scripts/populate_vector_store.py
```

**Advantage:** No local installation needed  
**Time:** 5 minutes

---

## 🔧 Option 2: Install Qdrant Locally (Linux/Mac)

### macOS
```bash
# Using Homebrew
brew install qdrant

# Start Qdrant
qdrant
```

### Linux (Ubuntu/Debian)
```bash
# Download
wget https://github.com/qdrant/qdrant/releases/download/v1.7.0/qdrant-x86_64-unknown-linux-musl

# Make executable
chmod +x qdrant-x86_64-unknown-linux-musl

# Run
./qdrant-x86_64-unknown-linux-musl
```

### Windows (Without Docker)
Download from: https://github.com/qdrant/qdrant/releases

1. Download `qdrant-x86_64-pc-windows-msvc.exe`
2. Run the executable
3. Qdrant starts on http://localhost:6333

---

## 🔧 Option 3: Use Python-Based Qdrant

If you want everything in Python without Docker:

```bash
# Install Python Qdrant package
pip install qdrant-client

# Then run
python scripts/populate_vector_store.py
```

---

## 📋 Complete Setup Without Docker

### Step 1: Prerequisites Check
```bash
python --version        # 3.9+
node --version         # 18+
```

### Step 2: Start Qdrant
Choose one:

**Option A: Qdrant Cloud**
- Sign up at https://cloud.qdrant.io
- Update `.env` with credentials

**Option B: Local Qdrant**
```bash
# Download and run locally
# See instructions above for your OS
```

### Step 3: Setup Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Populate vector store
python scripts/populate_vector_store.py
```

### Step 4: Start Backend Server
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Start Frontend
```bash
cd ../frontend
npm install
npm start
```

### Step 6: Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Qdrant Dashboard: http://localhost:6333/dashboard (if local)

---

## 📝 Configuration for No-Docker Setup

Update `backend/.env`:

```ini
# Database (already configured)
NEON_DATABASE_URL=postgresql://neondb_owner:npg_HgUqRFsf60Ki@...

# Qdrant Cloud or Local
QDRANT_URL=http://localhost:6333          # Local
# OR
QDRANT_URL=https://your-cloud-url:6333   # Cloud

QDRANT_API_KEY=your-key-if-using-cloud

# Other settings (unchanged)
OPENAI_API_KEY=sk-proj-...
SECRET_KEY=Ey7kL9mN2pQ4rT6vW8xZ1aB3...
```

---

## 🎯 Recommended: Qdrant Cloud

**Why?**
- ✓ No installation needed
- ✓ Free tier available
- ✓ Always available
- ✓ No Docker required
- ✓ Managed by Qdrant team

**How:**
1. Sign up: https://cloud.qdrant.io
2. Create cluster (free tier)
3. Copy connection details
4. Update `.env` file
5. Run: `python scripts/populate_vector_store.py`

---

## ❌ Issues & Solutions

### "Qdrant connection refused"
```
Solution:
- If using local: Start Qdrant daemon/service
- If using cloud: Verify credentials in .env
- If using cloud: Check cluster is running
```

### "Port 6333 already in use"
```
Solution:
- Find what's using it: lsof -i :6333 (Mac/Linux)
- Kill it or use different port
- Or use Qdrant Cloud instead
```

### "Can't connect to database"
```
Solution:
- Verify NEON_DATABASE_URL in .env
- Check internet connection
- Verify credentials are correct
```

### "Import errors after pip install"
```
Solution:
# Reinstall from requirements.txt
pip install --upgrade -r requirements.txt

# Or specific package
pip install qdrant-client --upgrade
```

---

## 🚀 Quick Setup (No Docker)

```bash
# 1. Go to project
cd "e:\GIAIC Q4 AGENTIC AI\PIAHR"

# 2. Use Qdrant Cloud
# - Sign up at https://cloud.qdrant.io
# - Update backend/.env with credentials

# 3. Setup backend
cd backend
pip install -r requirements.txt
python scripts/populate_vector_store.py

# 4. Start backend
python -m uvicorn src.main:app --reload

# 5. In new terminal, start frontend
cd frontend
npm install
npm start

# 6. Open http://localhost:3000
```

---

## 📊 Comparison: Setup Methods

| Method | Setup Time | Difficulty | Requirements |
|--------|-----------|-----------|--------------|
| **Docker (Recommended)** | 10 min | Easy | Docker Desktop |
| **Qdrant Cloud** | 5 min | Easy | Internet |
| **Local Qdrant** | 15 min | Medium | OS-specific |
| **Python Only** | 10 min | Medium | Python 3.9+ |

---

## ✨ My Recommendation

For the easiest setup **without Docker**:

1. **Use Qdrant Cloud** (no installation!)
2. **Follow the manual setup** steps above
3. **Done in 10 minutes**

---

## 📞 Support

- **Docker needed?** See: `DOCKER_INSTALLATION.md`
- **Cloud Setup help?** Visit: https://cloud.qdrant.io/docs
- **Qdrant Issues?** Check: https://qdrant.tech/documentation/

---

**Setup Time:** 5-15 minutes (depending on method)  
**Difficulty:** ⭐ Easy to ⭐⭐ Medium  
**Status:** Ready to start ✓
