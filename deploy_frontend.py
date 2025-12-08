#!/usr/bin/env python3
"""
Deployment script for the Physical AI & Humanoid Robotics Textbook Platform frontend
This script helps deploy the frontend to GitHub Pages
"""

import os
import subprocess
import sys
from pathlib import Path

def check_prerequisites():
    """Check if prerequisites for frontend deployment are met"""
    print("Checking prerequisites for frontend deployment...")

    # Check if we're in the right directory
    if not Path("frontend").exists():
        print("Error: 'frontend' directory not found. Make sure you're in the project root.")
        return False

    # Check if package.json exists
    if not Path("frontend/package.json").exists():
        print("Error: frontend/package.json not found.")
        return False

    # Check if docusaurus.config.ts exists
    if not Path("frontend/docusaurus.config.ts").exists():
        print("Error: frontend/docusaurus.config.ts not found.")
        return False

    print("✓ All prerequisites met for frontend deployment")
    return True

def update_config_for_production(backend_url):
    """Update the frontend configuration for production"""
    print(f"\nUpdating frontend configuration for production...")
    print(f"Backend API URL will be set to: {backend_url}")

    # Read the current docusaurus.config.ts
    config_path = Path("frontend/docusaurus.config.ts")
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update the URL and base URL for production
    updated_content = content.replace(
        "url: 'https://your-github-username.github.io',",
        f"url: 'https://your-github-username.github.io',"
    ).replace(
        "baseUrl: '/textbook-site/',",
        "baseUrl: '/Physical-AI-and-Humanoid-Robotics-Textbook/',"  # Using project name as base URL
    ).replace(
        "organizationName: 'your-github-username',",
        "organizationName: 'your-github-username',"
    ).replace(
        "projectName: 'textbook-site',",
        "projectName: 'Physical-AI-and-Humanoid-Robotics-Textbook',"
    )

    # Write the updated content back
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("✓ Frontend configuration updated for production")

def build_frontend():
    """Build the frontend for production"""
    print("\nBuilding frontend for production...")

    # Navigate to frontend directory
    original_dir = os.getcwd()
    os.chdir("frontend")

    try:
        # Install dependencies
        print("Installing frontend dependencies...")
        result = subprocess.run(["npm", "install"], check=True, capture_output=True, text=True)
        print("✓ Dependencies installed successfully")

        # Build the project
        print("Building the frontend...")
        result = subprocess.run(["npm", "run", "build"], check=True, capture_output=True, text=True)
        print("✓ Frontend built successfully")

    except subprocess.CalledProcessError as e:
        print(f"Error building frontend: {e}")
        print(f"Error output: {e.stderr}")
        return False
    finally:
        os.chdir(original_dir)

    return True

def deploy_to_github_pages():
    """Deploy the frontend to GitHub Pages"""
    print("\nDeploying frontend to GitHub Pages...")

    # Navigate to frontend directory
    original_dir = os.getcwd()
    os.chdir("frontend")

    print("Frontend deployment to GitHub Pages:")
    print("1. The GitHub Actions workflow is already configured in .github/workflows/deploy.yml")
    print("2. Push your code to the main branch of your GitHub repository")
    print("3. The workflow will automatically build and deploy to GitHub Pages")
    print("4. Make sure GitHub Pages is enabled in your repository settings")

    print("\nManual deployment (if needed):")
    print("   cd frontend")
    print("   GIT_USER=<your-username> DEPLOYMENT_BRANCH=gh-pages npm run deploy")

    print("\nAlternatively, you can set up the GitHub Actions workflow:")
    print("1. Push this repository to GitHub")
    print("2. Go to the repository Settings > Pages")
    print("3. Select GitHub Actions as the source")
    print("4. The workflow will run automatically on pushes to main branch")

    os.chdir(original_dir)
    print("✓ Frontend deployment instructions complete")

def main():
    print("Physical AI & Humanoid Robotics Textbook Platform - Frontend Deployment")
    print("=" * 70)

    if not check_prerequisites():
        sys.exit(1)

    # Get backend URL from user (or use default)
    backend_url = input("\nEnter your production backend URL (or press Enter for default): ").strip()
    if not backend_url:
        backend_url = "https://your-backend-url.onrender.com"  # Default placeholder
        print(f"Using default backend URL: {backend_url}")

    # Update configuration
    update_config_for_production(backend_url)

    # Build the frontend
    if not build_frontend():
        print("Failed to build frontend. Please fix the build errors and try again.")
        sys.exit(1)

    # Deploy to GitHub Pages
    deploy_to_github_pages()

    print("\n" + "=" * 70)
    print("Frontend deployment preparation complete!")
    print("The frontend is built and ready for deployment to GitHub Pages.")

if __name__ == "__main__":
    main()