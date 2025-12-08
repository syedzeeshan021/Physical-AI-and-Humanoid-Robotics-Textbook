#!/usr/bin/env python3
"""
Deployment script for the Physical AI & Humanoid Robotics Textbook Platform backend
This script helps deploy the backend to Railway
"""

import os
import subprocess
import sys
from pathlib import Path

def check_prerequisites():
    """Check if prerequisites for deployment are met"""
    print("Checking prerequisites for backend deployment...")

    # Check if we're in the right directory
    if not Path("backend").exists():
        print("Error: 'backend' directory not found. Make sure you're in the project root.")
        return False

    # Check if requirements.txt exists
    if not Path("backend/requirements.txt").exists():
        print("Error: backend/requirements.txt not found.")
        return False

    # Check if Dockerfile exists
    if not Path("backend/Dockerfile").exists():
        print("Error: backend/Dockerfile not found.")
        return False

    print("✓ All prerequisites met for backend deployment")
    return True

def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = [
        "NEON_DATABASE_URL",
        "QDRANT_URL",
        "OPENAI_API_KEY",
        "SECRET_KEY"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set these environment variables before deployment:")
        print("For Railway deployment, set these in the Railway dashboard under Variables")
        return False

    print("✓ All required environment variables are set")
    return True

def deploy_to_railway():
    """Deploy the backend to Railway"""
    print("\nDeploying backend to Railway...")

    # Navigate to backend directory
    os.chdir("backend")

    print("Backend deployment steps:")
    print("1. Connect your Railway account and create a new project")
    print("2. Link this repository to Railway")
    print("3. Set the following environment variables in Railway dashboard:")
    print("   - NEON_DATABASE_URL")
    print("   - QDRANT_URL")
    print("   - OPENAI_API_KEY")
    print("   - SECRET_KEY")
    print("4. Railway will automatically detect the Dockerfile and deploy")
    print("5. The start command should be: gunicorn -c gunicorn.conf.py src.main:app")

    print("\nAlternatively, you can use the Railway CLI:")
    print("   railway up")

    print("\n✓ Backend deployment instructions complete")

def main():
    print("Physical AI & Humanoid Robotics Textbook Platform - Backend Deployment")
    print("=" * 70)

    if not check_prerequisites():
        sys.exit(1)

    if not check_environment_variables():
        print("\nNote: You need to set the environment variables before deploying.")
        print("You can set them in the Railway dashboard or using the Railway CLI.")

    deploy_to_railway()

    print("\n" + "=" * 70)
    print("Backend deployment preparation complete!")
    print("The backend is configured and ready for deployment to Railway.")

if __name__ == "__main__":
    main()