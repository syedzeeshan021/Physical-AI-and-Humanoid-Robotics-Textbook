"""
Simple server to test basic functionality without SQLAlchemy dependencies
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Physical AI & Humanoid Robotics - Textbook API",
    version="1.0.0",
    description="Textbook Generation API with RAG Chatbot (Minimal Server)"
)

@app.get("/")
def read_root():
    return {
        "message": "Textbook Generation API is running!",
        "status": "operational",
        "features": [
            "Docusaurus-based textbook frontend",
            "RAG chatbot integration",
            "User authentication",
            "Chapter management"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "textbook-generation-api",
        "version": "1.0.0",
        "checks": {
            "basic_api": "ok",
            "database": "not checked (due to Python 3.13/SQLAlchemy compatibility)",
            "vector_store": "not checked",
            "external_apis": "not checked"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )