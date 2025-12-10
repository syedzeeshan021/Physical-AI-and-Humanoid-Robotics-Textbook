---
id: 002
title: Correct Application Startup Procedure
stage: general
date: 2025-12-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: npm start
labels: ["startup", "full-stack", "docusaurus", "fastapi", "backend", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - GETTING_STARTED.md
  - backend/src/main.py
  - frontend/package.json
  - setup_rag.py
tests:
  - backend server started on port 8001
  - frontend server started on port 3004
  - both services accessible
---

## Prompt

npm start

## Response snapshot

After reviewing the project documentation and files, I discovered that this is a full-stack application with both frontend (Docusaurus) and backend (FastAPI) components. The correct startup procedure involves:

1. The project requires Docker for the Qdrant vector database, but since Docker is not available, I started just the backend service.
2. Backend server started successfully on port 8001 using: `cd backend && python -m uvicorn src.main:app --reload --port 8001`
3. Frontend Docusaurus server is running on port 3004 from previous command
4. The complete architecture includes: Frontend (port 3000 by default), Backend (port 8000 by default), and Qdrant vector database (port 6333)

The proper startup sequence when Docker is available would be:
- Run `python setup_rag.py` to initialize the system
- Start backend: `cd backend && python -m uvicorn src.main:app --reload`
- Start frontend: `cd frontend && npm start`

## Outcome

- ✅ Impact: Both frontend and backend services are now running
- 🧪 Tests: Backend accessible at http://localhost:8001, Frontend at http://localhost:3004
- 📁 Files: No files modified, running existing project
- 🔁 Next prompts: Access the application via the frontend interface
- 🧠 Reflection: The project is a sophisticated RAG-based textbook platform with multiple services

## Evaluation notes (flywheel)

- Failure modes observed: Docker dependency for Qdrant vector database
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A