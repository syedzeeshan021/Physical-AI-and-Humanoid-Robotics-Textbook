# Textbook Generation API Contracts

## Authentication API

### POST /api/auth/register
Register a new user

#### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

#### Response (201 Created)
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2025-12-07T10:00:00Z"
}
```

#### Response (400 Bad Request)
```json
{
  "error": "Invalid email format or password too short"
}
```

### POST /api/auth/login
Login user

#### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

#### Response (200 OK)
```json
{
  "token": "jwt-token-string",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  }
}
```

#### Response (401 Unauthorized)
```json
{
  "error": "Invalid credentials"
}
```

## Chapter API

### GET /api/chapters
Get all textbook chapters

#### Response (200 OK)
```json
[
  {
    "id": "uuid-string",
    "title": "Introduction to Physical AI",
    "order": 1,
    "word_count": 1500
  },
  {
    "id": "uuid-string",
    "title": "Basics of Humanoid Robotics",
    "order": 2,
    "word_count": 1800
  }
]
```

### GET /api/chapters/{id}
Get specific chapter content

#### Response (200 OK)
```json
{
  "id": "uuid-string",
  "title": "Introduction to Physical AI",
  "content": "# Introduction to Physical AI\n\nPhysical AI...",
  "order": 1
}
```

#### Response (404 Not Found)
```json
{
  "error": "Chapter not found"
}
```

## RAG API

### POST /api/rag/query
Query textbook content with RAG

#### Request
```json
{
  "query": "What is Physical AI?",
  "session_id": "optional-session-id"
}
```

#### Response (200 OK)
```json
{
  "response": "Physical AI is a field that combines...",
  "sources": [
    "Introduction to Physical AI",
    "Chapter 1: Definitions"
  ],
  "session_id": "session-id-string"
}
```

#### Response (429 Too Many Requests)
```json
{
  "error": "Rate limit exceeded, please try again later"
}
```

## User Preferences API

### GET /api/user/preferences
Get user preferences

#### Response (200 OK)
```json
{
  "language": "en",
  "theme": "light",
  "personalization_enabled": true
}
```

#### Response (401 Unauthorized)
```json
{
  "error": "Authentication required"
}
```

### PUT /api/user/preferences
Update user preferences

#### Request
```json
{
  "language": "ur",
  "theme": "dark",
  "personalization_enabled": true
}
```

#### Response (200 OK)
```json
{
  "language": "ur",
  "theme": "dark",
  "personalization_enabled": true
}
```