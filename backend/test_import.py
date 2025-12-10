#!/usr/bin/env python3
"""
Test script to import vector_store and see if it triggers the error
"""

print("About to import vector_store...")
try:
    from src.core.vector_store import vector_store
    print("Successfully imported vector_store!")
    print(f"Vector store client type: {type(vector_store.client)}")
except Exception as e:
    print(f"Error importing vector_store: {e}")
    import traceback
    traceback.print_exc()