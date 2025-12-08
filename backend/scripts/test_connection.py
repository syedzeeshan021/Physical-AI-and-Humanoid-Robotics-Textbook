"""
Diagnostic script to test Qdrant Cloud connection
Run this BEFORE running populate_vector_store.py
"""
import sys
from pathlib import Path
import os

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("\n" + "=" * 70)
print("QDRANT CLOUD CONNECTION DIAGNOSTIC")
print("=" * 70 + "\n")

# Step 1: Check .env file
print("[1/5] Checking .env file...")
env_path = Path(__file__).parent.parent / ".env"
if not env_path.exists():
    print("  ✗ .env file not found at:", env_path)
    print("  ℹ  Create backend/.env with your Qdrant Cloud credentials")
    sys.exit(1)
print("  ✓ .env file found")

# Step 2: Load environment variables
print("\n[2/5] Loading environment variables...")
from dotenv import load_dotenv
load_dotenv(env_path)

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
neon_url = os.getenv("NEON_DATABASE_URL")

print(f"  QDRANT_URL: {qdrant_url}")
print(f"  QDRANT_API_KEY: {qdrant_api_key[:20]}..." if qdrant_api_key else "  QDRANT_API_KEY: NOT SET")
print(f"  DATABASE_URL: {neon_url[:50]}..." if neon_url else "  DATABASE_URL: NOT SET")

# Check for placeholder values
if "your-cluster-url" in (qdrant_url or ""):
    print("\n  ✗ ERROR: QDRANT_URL contains placeholder 'your-cluster-url'")
    print("  ℹ  Update QDRANT_URL with your actual Qdrant Cloud URL")
    sys.exit(1)

if "your-api-key" in (qdrant_api_key or ""):
    print("\n  ✗ ERROR: QDRANT_API_KEY contains placeholder 'your-api-key'")
    print("  ℹ  Update QDRANT_API_KEY with your actual API key")
    sys.exit(1)

print("  ✓ Environment variables loaded")

# Step 3: Test Qdrant connection
print("\n[3/5] Testing Qdrant Cloud connection...")
try:
    import requests
    response = requests.get(f"{qdrant_url}/health", timeout=5, verify=False)
    if response.status_code == 200:
        print("  ✓ Qdrant Cloud is reachable")
        print(f"  Response: {response.json()}")
    else:
        print(f"  ✗ Qdrant Cloud returned status: {response.status_code}")
        print(f"  Response: {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ Connection failed: {str(e)}")
    print("\n  Troubleshooting:")
    print("  1. Verify QDRANT_URL is correct (should start with https://)")
    print("  2. Check internet connection")
    print("  3. Verify Qdrant Cloud cluster is running")
    print("  4. Try accessing URL in browser: " + qdrant_url + "/health")
    sys.exit(1)

# Step 4: Test Qdrant client
print("\n[4/5] Testing Qdrant Python client...")
try:
    from qdrant_client import QdrantClient
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=False  # Use HTTP for cloud
    )
    print("  ✓ Qdrant client created successfully")
except Exception as e:
    print(f"  ✗ Failed to create Qdrant client: {str(e)}")
    sys.exit(1)

# Step 5: Test Database connection
print("\n[5/5] Testing PostgreSQL/Neon connection...")
try:
    import asyncio
    from src.core.database import AsyncSessionLocal, init_db
    
    async def test_db():
        try:
            await init_db()
            async with AsyncSessionLocal() as session:
                result = await session.execute("SELECT 1")
                print("  ✓ Database connection successful")
        except Exception as e:
            print(f"  ✗ Database connection failed: {str(e)}")
            print("\n  Troubleshooting:")
            print("  1. Check NEON_DATABASE_URL is correct")
            print("  2. Verify database credentials")
            print("  3. Check internet connection to Neon")
            sys.exit(1)
    
    asyncio.run(test_db())
except Exception as e:
    print(f"  ⚠  Could not test database: {str(e)}")
    print("  ℹ  This is okay, will test during population")

# Success!
print("\n" + "=" * 70)
print("✓ ALL DIAGNOSTICS PASSED!")
print("=" * 70)
print("\nYou can now run:")
print("  python scripts/populate_vector_store.py")
print()
