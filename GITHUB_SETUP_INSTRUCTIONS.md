# GitHub Repository Setup Instructions

## Create a New Repository on GitHub

1. Go to https://github.com/new
2. Create a new repository with the name `Physical-AI-and-Humanoid-Robotics-Textbook`
3. Add a description: "A comprehensive textbook platform with integrated RAG chatbot for Physical AI and Humanoid Robotics education"
4. Choose Public visibility
5. Do NOT initialize with a README, .gitignore, or license (we already have these)

## Push the Code to GitHub

After creating the repository, run these commands in your terminal:

```bash
# Change directory to your project
cd "E:\GIAIC Q4 AGENTIC AI\PIAHR"

# Add the remote origin (replace <your-username> with your GitHub username)
git remote add origin https://github.com/<your-username>/Physical-AI-and-Humanoid-Robotics-Textbook.git

# Push the code to GitHub
git branch -M main
git push -u origin main
```

## Alternative: Using SSH (if you have SSH keys set up)

```bash
# Add the remote origin using SSH
git remote add origin git@github.com:<your-username>/Physical-AI-and-Humanoid-Robotics-Textbook.git

# Push the code to GitHub
git branch -M main
git push -u origin main
```

## Repository Details

- **Name**: Physical-AI-and-Humanoid-Robotics-Textbook
- **Description**: A comprehensive textbook platform with integrated RAG chatbot for Physical AI and Humanoid Robotics education
- **Language**: Python, TypeScript
- **Features**:
  - 6-Chapter textbook on Physical AI & Humanoid Robotics
  - RAG Chatbot with textbook content knowledge
  - Text selection → Ask AI functionality
  - User authentication and personalization
  - Responsive Docusaurus frontend
  - FastAPI backend with Neon DB and Qdrant vector store

## After Creating the Repository

Once pushed to GitHub, you can:

1. **Enable GitHub Pages** for the frontend:
   - Go to Settings > Pages
   - Select source as "GitHub Actions"

2. **Set up backend deployment on Railway**:
   - Connect your GitHub repository to Railway
   - Add the required environment variables:
     - NEON_DATABASE_URL
     - QDRANT_URL
     - OPENAI_API_KEY
     - SECRET_KEY

3. **Update frontend configuration**:
   - Update docusaurus.config.ts with your GitHub username and repo name
   - Update backend API URL in frontend/src/services/api.ts to point to your deployed backend