# Physical AI & Humanoid Robotics Textbook Platform

A comprehensive textbook platform with integrated RAG chatbot for Physical AI and Humanoid Robotics education.

## Features

- **6-Chapter Textbook**: Complete coverage of Physical AI and Humanoid Robotics topics
- **RAG Chatbot**: AI-powered assistant that answers questions based on textbook content
- **Text Selection**: Select text and ask AI about specific content
- **User Authentication**: Optional account creation for personalization
- **Progress Tracking**: Track learning progress
- **Urdu Translation**: Optional Urdu language support
- **Responsive Design**: Works on all device sizes

## Architecture

### Frontend
- **Framework**: Docusaurus v3 with TypeScript
- **Components**: React-based components for chat and text selection
- **Deployment**: GitHub Pages

### Backend
- **Framework**: FastAPI with Python 3.11+
- **Database**: Neon PostgreSQL (free tier)
- **Vector Store**: Qdrant Cloud (free tier)
- **AI Integration**: OpenAI API for RAG responses
- **Deployment**: Railway or Vercel

## Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:
```env
NEON_DATABASE_URL=your_neon_db_url
QDRANT_URL=your_qdrant_url
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_secret_key
```

Run the backend:
```bash
cd backend
python -m uvicorn src.main:app --reload
```

## API Endpoints

### Textbook Content
- `GET /api/v1/chapters` - Get all chapters
- `GET /api/v1/chapters/{id}` - Get specific chapter

### RAG Chatbot
- `POST /api/v1/rag/query` - Query textbook content with RAG
- `POST /api/v1/rag/index-chapter/{chapter_id}` - Index chapter for RAG search

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### User Preferences
- `GET /api/v1/users/preferences` - Get user preferences
- `PUT /api/v1/users/preferences` - Update user preferences

## Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production
```bash
# Frontend
cd frontend
npm run build

# Backend documentation
http://localhost:8000/docs
```

## Deployment

### Frontend (GitHub Pages)
```bash
cd frontend
GIT_USER=<your-username> DEPLOYMENT_BRANCH=gh-pages npm run deploy
```

### Backend (Railway/Vercel)
Follow the platform-specific deployment instructions with the environment variables configured.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the GitHub repository.