# Urdu Translation Button - Quickstart Guide

## Overview
This guide provides a quick overview of how to implement the Urdu translation functionality that allows logged users to translate textbook content by pressing a button at the start of each chapter, earning 50 bonus points.

## Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.11+ with FastAPI
- Google Cloud account with Translation API enabled
- PostgreSQL database (Neon recommended)
- Existing user authentication system

## Backend Setup

### 1. Install Dependencies
```bash
pip install fastapi google-cloud-translate python-jose[cryptography] passlib[bcrypt] psycopg2-binary
```

### 2. Environment Configuration
```bash
# .env
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_TRANSLATE_API_KEY=your-api-key
DATABASE_URL=postgresql://user:password@host:port/dbname
JWT_SECRET_KEY=your-secret-key
```

### 3. Database Models
The system requires three main database tables:
- `users` - for user accounts and bonus points
- `translation_sessions` - for caching translations
- `bonus_points_records` - for tracking earned points

## Frontend Integration

### 1. Translation Button Component
The translation button should be injected at the start of each chapter. Here's a basic implementation:

```jsx
import React, { useState } from 'react';

const TranslationButton = ({ chapterId, content }) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);

  const handleTranslate = async () => {
    setIsTranslating(true);
    try {
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          content,
          chapter_id: chapterId,
          target_language: 'ur'
        })
      });

      if (response.ok) {
        const data = await response.json();
        // Update content with translated version
        setIsTranslated(true);
        showBonusPointsNotification(data.bonus_points_awarded);
      }
    } catch (error) {
      console.error('Translation failed:', error);
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <button
      onClick={handleTranslate}
      disabled={isTranslating}
      className={`translate-btn ${isTranslating ? 'loading' : ''}`}
    >
      {isTranslating ? 'Translating...' : isTranslated ? 'Translate back to English' : 'Translate to Urdu'}
    </button>
  );
};
```

### 2. Right-to-Left Text Support
For proper Urdu rendering, ensure your CSS includes RTL support:

```css
.urdu-text {
  direction: rtl;
  text-align: right;
  font-family: 'Noto Nastaliq Urdu', 'Urdu Typesetting', serif;
}
```

## Key Implementation Steps

### 1. Backend API Implementation
1. Create the translation endpoint with authentication middleware
2. Implement caching with 24-hour TTL
3. Integrate with Google Cloud Translation API
4. Implement bonus points logic (50 points per first-time chapter translation)

### 2. Frontend Integration
1. Inject the translation button at the start of each chapter
2. Implement language switching functionality
3. Add bonus points notification system
4. Ensure proper RTL text rendering

### 3. Database Integration
1. Create the required database tables
2. Implement session-based caching
3. Track translation usage per user
4. Implement point aggregation system

## Testing

### 1. Unit Tests
- Test translation API endpoint
- Test bonus points calculation
- Test caching logic
- Test authentication middleware

### 2. Integration Tests
- Test complete translation flow
- Test bonus points awarding
- Test caching behavior
- Test error handling

### 3. End-to-End Tests
- Test user translation journey
- Test bonus points display
- Test language switching
- Test error scenarios

## Deployment

### 1. Environment Setup
- Configure Google Cloud Translation API credentials
- Set up database with required tables
- Configure caching layer
- Set up authentication system

### 2. Monitoring
- Monitor API usage and costs
- Track translation quality metrics
- Monitor user engagement with feature
- Track bonus points distribution

## Success Metrics
- Translation functionality available on all 6 textbook chapters
- 50 bonus points correctly awarded for first-time chapter translations
- Translation processing completes under 3 seconds for 95% of requests
- At least 20% of logged-in users engage with the translation feature within the first month