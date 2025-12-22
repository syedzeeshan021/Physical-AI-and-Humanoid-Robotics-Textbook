import sys
import os
from pathlib import Path

def run_server():
    # Add the project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    # Add the backend directory to Python path
    backend_dir = project_root / "backend"
    sys.path.insert(0, str(backend_dir))

    # Don't change the working directory to ensure .env from project root is loaded
    # The imports should work with the Python path modifications above

    # Now import and run the application
    try:
        import uvicorn
        from src.main import app

        print("Starting backend server...")
        print("Backend server running at: http://127.0.0.1:8000")
        print("Press Ctrl+C to stop the server")

        uvicorn.run(
            "src.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True
        )
    except Exception as e:
        print(f"Error starting backend: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_server()