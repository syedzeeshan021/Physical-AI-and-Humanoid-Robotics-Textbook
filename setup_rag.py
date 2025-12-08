"""
Standalone script to populate Qdrant vector store with textbook embeddings
Run from project root directory
"""
import subprocess
import sys
import time
import requests
from pathlib import Path

def check_docker():
    """Check if Docker is installed and available"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def check_qdrant():
    """Check if Qdrant is running"""
    try:
        response = requests.get("http://localhost:6333/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_qdrant():
    """Start Qdrant using Docker"""
    print("[*] Starting Qdrant vector database...")
    
    # First check if Docker is available
    if not check_docker():
        print("    ✗ Docker is not installed or not in PATH")
        print("    ℹ  Install Docker Desktop: https://www.docker.com/products/docker-desktop")
        print("    ℹ  Or install Docker manually for your OS")
        return False
    
    try:
        # Check if container already exists
        result = subprocess.run(
            ["docker", "ps", "-a"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "qdrant" in result.stdout:
            # Container exists, start it
            print("    ℹ  Qdrant container found, starting...")
            subprocess.run(["docker", "start", "qdrant"], capture_output=True, timeout=10)
            print("    ✓ Qdrant container started")
        else:
            # Create new container
            print("    ℹ  Creating new Qdrant container...")
            subprocess.run(
                ["docker", "run", "-d", "-p", "6333:6333", "-p", "6334:6334", 
                 "--name", "qdrant", "qdrant/qdrant"],
                capture_output=True,
                timeout=30
            )
            print("    ✓ Qdrant container created")
        
        # Wait for Qdrant to be ready
        print("    ⏳ Waiting for Qdrant to start (max 30 seconds)...")
        for i in range(30):
            if check_qdrant():
                print("    ✓ Qdrant is ready")
                return True
            time.sleep(1)
            if i % 5 == 0 and i > 0:
                print(f"    ⏳ Still waiting... ({i}s)")
        
        print("    ✗ Qdrant failed to start or didn't respond")
        return False
        
    except subprocess.TimeoutExpired:
        print("    ✗ Docker command timed out")
        return False
    except Exception as e:
        print(f"    ✗ Error starting Docker: {str(e)}")
        return False

def main():
    print()
    print("=" * 60)
    print("RAG Vector Store Setup")
    print("=" * 60)
    print()
    
    # Step 0: Check Docker (if Qdrant not already running)
    if not check_qdrant():
        print("[0/3] Checking Docker installation...")
        if not check_docker():
            print("\n" + "!" * 60)
            print("ERROR: Docker is not installed or not accessible")
            print("!" * 60)
            print("\nTo fix this, install Docker Desktop:")
            print("  Windows: https://www.docker.com/products/docker-desktop")
            print("\nMake sure Docker is:")
            print("  ✓ Installed and running")
            print("  ✓ Added to system PATH")
            print("  ✓ Accessible via command line")
            print("\nAfter installing Docker, try again:")
            print("  python setup_rag.py")
            print("!" * 60)
            sys.exit(1)
        print("    ✓ Docker found")
    
    # Step 1: Check Qdrant
    print("\n[1/3] Checking Qdrant...")
    if not check_qdrant():
        if not start_qdrant():
            print("\n" + "!" * 60)
            print("ERROR: Qdrant setup failed")
            print("!" * 60)
            print("\nTroubleshooting:")
            print("  1. Verify Docker is running")
            print("  2. Check Docker logs: docker logs qdrant")
            print("  3. Try manual start: docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant")
            print("!" * 60)
            sys.exit(1)
    else:
        print("    ✓ Qdrant already running")
    
    # Step 2: Setup backend environment
    print("\n[2/3] Setting up backend...")
    backend_path = Path(__file__).parent / "backend"
    
    # Install requirements
    print("    - Installing Python dependencies...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=backend_path,
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            print("    ✓ Dependencies installed")
        else:
            print("    ✗ Warning: Some dependencies may not have installed correctly")
            print("    ℹ  You can continue, but may need to install manually later")
    except subprocess.TimeoutExpired:
        print("    ✗ Dependency installation timed out")
        print("    ℹ  Continuing anyway...")
    except Exception as e:
        print(f"    ✗ Error installing dependencies: {str(e)}")
        print("    ℹ  Continuing anyway...")
    
    # Step 3: Populate vector store
    print("\n[3/3] Populating vector store...")
    print("    ⏳ Generating embeddings and storing in Qdrant...")
    print("    ⏳ This may take 2-3 minutes...")
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, "scripts/populate_vector_store.py"],
            cwd=backend_path,
            timeout=300
        )
        
        if result.returncode != 0:
            print("\n" + "!" * 60)
            print("ERROR: Vector store population failed")
            print("!" * 60)
            print("\nTroubleshooting:")
            print("  1. Check if Qdrant is running: http://localhost:6333/health")
            print("  2. Check database connection in backend/.env")
            print("  3. Try manual: cd backend && python scripts/populate_vector_store.py")
            print("!" * 60)
            sys.exit(1)
    except subprocess.TimeoutExpired:
        print("\n✗ Vector store population timed out")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("✓ Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Open a new terminal in the backend directory")
    print("  2. Run: python -m uvicorn src.main:app --reload")
    print()
    print("In another terminal:")
    print("  1. Open a new terminal in the frontend directory")
    print("  2. Run: npm start")
    print()
    print("Then access:")
    print("  - Chat: http://localhost:3000")
    print("  - API: http://localhost:8000/docs")
    print("  - Qdrant: http://localhost:6333/dashboard")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

