from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create a simplified app that doesn't rely on SQLAlchemy models initially
app = FastAPI(
    title="Physical AI & Humanoid Robotics - Textbook API",
    version="1.0.0",
    description="Textbook Generation API with RAG Chatbot (Simplified Version)"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Physical AI & Humanoid Robotics Textbook API",
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

# Include basic API routes that don't require SQLAlchemy
from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_status():
    return {"status": "running", "component": "api"}

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "src.main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )