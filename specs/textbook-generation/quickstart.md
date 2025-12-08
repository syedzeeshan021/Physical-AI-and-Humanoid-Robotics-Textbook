# Textbook Generation Quickstart Guide

## Development Setup

### Prerequisites
- Node.js 18+ (for Docusaurus)
- Python 3.11+ (for FastAPI backend)
- Git
- npm or yarn

### Clone Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Environment Variables
Create `.env` file in backend directory:
```env
NEON_DATABASE_URL=your_neon_db_url
QDRANT_URL=your_qdrant_url
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_secret_key
```

### Run Applications
```bash
# Terminal 1: Frontend
cd frontend && npm run start

# Terminal 2: Backend
cd backend && python -m uvicorn main:app --reload
```

## Key Technologies

### Frontend (Docusaurus)
- Static site generation
- Markdown-based content
- Auto sidebar generation
- Custom plugin for RAG integration

### Backend (FastAPI)
- Async Python framework
- Type hints and validation
- Automatic API documentation
- RAG pipeline implementation

### Database (Neon)
- PostgreSQL-compatible
- Serverless with auto-scaling
- Free tier available
- Connection pooling

### Vector Store (Qdrant)
- Vector similarity search
- Efficient embedding storage
- Free tier available
- High performance

## Project Structure
```
project/
├── frontend/                 # Docusaurus application
│   ├── docs/                 # Textbook content (markdown)
│   ├── src/                  # Custom components
│   ├── static/               # Static assets
│   └── docusaurus.config.js  # Configuration
├── backend/                  # FastAPI application
│   ├── src/
│   │   ├── api/              # API endpoints
│   │   ├── models/           # Data models
│   │   ├── services/         # Business logic
│   │   └── main.py           # Application entry point
│   └── requirements.txt      # Dependencies
├── specs/                    # Specifications and plans
└── README.md                 # Project overview
```

## Common Commands

### Frontend Commands
```bash
npm run start          # Start development server
npm run build          # Build for production
npm run serve          # Serve built site locally
npm run docusaurus     # Docusaurus CLI commands
```

### Backend Commands
```bash
python -m uvicorn main:app --reload    # Development server
python -m pytest                       # Run tests
python -m mypy .                       # Type checking
```

## Configuration Files

### Docusaurus Configuration
Located at `frontend/docusaurus.config.js`:
- Site metadata (title, description)
- Theme configuration
- Plugin settings
- Sidebar generation

### Backend Configuration
Located at `backend/src/config.py`:
- Database connection settings
- API keys and secrets
- RAG pipeline configuration
- Rate limiting settings

## API Endpoints

### Frontend API
- `/api/chapters` - Get textbook chapters
- `/api/chapters/:id` - Get specific chapter
- `/api/rag/query` - RAG query endpoint

### Backend API
- `/docs` - Interactive API documentation
- `/redoc` - Alternative API documentation
- `/api/v1/` - Versioned API endpoints

## Testing

### Frontend Tests
```bash
npm run test
```

### Backend Tests
```bash
python -m pytest
```

### End-to-End Tests
```bash
# Run both frontend and backend, then:
npm run test:e2e
```

## Deployment

### Frontend Deployment
1. Build: `npm run build`
2. Deploy to GitHub Pages, Netlify, or Vercel
3. Configure custom domain if needed

### Backend Deployment
1. Deploy to Railway, Vercel, or similar platform
2. Configure environment variables
3. Set up Neon and Qdrant connections
4. Verify API endpoints are accessible

## Troubleshooting

### Common Issues
1. **Environment Variables**: Ensure all required environment variables are set
2. **Port Conflicts**: Check if ports 3000 (frontend) and 8000 (backend) are available
3. **Database Connection**: Verify Neon connection string format
4. **API Keys**: Confirm all API keys are valid and have necessary permissions

### Development Tips
1. Use `npm run start` for hot-reloading during development
2. Check browser console for frontend errors
3. Use `python -m uvicorn main:app --reload --log-level debug` for detailed backend logs
4. Monitor rate limits when testing RAG functionality