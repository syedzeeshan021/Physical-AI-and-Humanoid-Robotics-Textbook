#!/usr/bin/env python3
"""
Debug script to check FastAPI routes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app

print("FastAPI app routes:")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"  {route.path} -> {getattr(route, 'methods', 'N/A')}")
    else:
        print(f"  {route} -> (no path attribute)")

print(f"\nTotal routes: {len(app.routes)}")

# Check for specific paths
paths = [route.path for route in app.routes if hasattr(route, 'path')]
print(f"\nAvailable paths: {paths}")

if '/api/v1/rag/query' in paths:
    print("✓ RAG query endpoint found!")
else:
    print("✗ RAG query endpoint NOT found")

if '/api/v1/chapters/' in paths:
    print("✓ Chapters endpoint found!")
else:
    print("✗ Chapters endpoint NOT found")