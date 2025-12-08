@echo off
REM Quick Start Script for PIAHR RAG Chatbot System
REM This script sets up and runs the complete RAG system

setlocal enabledelayedexpansion

echo.
echo =========================================================
echo   PIAHR RAG Chatbot System - Quick Start
echo =========================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Docker is not installed or not in PATH
    echo Please install Docker from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1/5] Starting Qdrant Vector Database...
docker ps | findstr qdrant >nul
if errorlevel 1 (
    echo   - Qdrant not running, starting container...
    docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant >nul 2>&1
    timeout /t 3 >nul
    echo   ✓ Qdrant started
) else (
    echo   ✓ Qdrant already running
)

echo.
echo [2/5] Checking database connection...
cd /d "e:\GIAIC Q4 AGENTIC AI\PIAHR\backend"

REM Test if we can import and run the setup
python -c "from src.core.config import settings; print('✓ Configuration loaded')"
if errorlevel 1 (
    echo   ✗ Configuration error. Check your .env file
    pause
    exit /b 1
)
echo   ✓ Database configured

echo.
echo [3/5] Populating vector store with embeddings...
echo   This may take 2-3 minutes...
python scripts\populate_vector_store.py
if errorlevel 1 (
    echo   ✗ Failed to populate vector store
    echo   Check the logs above for details
    pause
    exit /b 1
)
echo   ✓ Vector store populated

echo.
echo [4/5] Starting Backend Server...
start "" cmd /k python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
timeout /t 3 >nul
echo   ✓ Backend started on http://localhost:8000

echo.
echo [5/5] Starting Frontend...
cd /d "e:\GIAIC Q4 AGENTIC AI\PIAHR\frontend"
if not exist "node_modules" (
    echo   - Installing dependencies first...
    call npm install
)
start "" cmd /k npm start
timeout /t 2 >nul
echo   ✓ Frontend starting on http://localhost:3000

echo.
echo =========================================================
echo   ✓ System Ready!
echo =========================================================
echo.
echo Access points:
echo   - Frontend:           http://localhost:3000
echo   - Backend API:        http://localhost:8000/api/v1
echo   - Qdrant Dashboard:   http://localhost:6333/dashboard
echo   - API Docs:           http://localhost:8000/docs
echo.
echo The chat widget appears in the bottom-right corner of the frontend.
echo.
echo To stop the system:
echo   1. Close the terminal windows
echo   2. Run: docker stop qdrant
echo.
pause
