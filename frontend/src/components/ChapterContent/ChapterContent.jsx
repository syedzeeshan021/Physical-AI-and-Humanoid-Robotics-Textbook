import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import { useAuth } from '../Auth/AuthContext'; // Assuming we have an auth context

const ChapterContent = ({ children, className }) => {
  const location = useLocation();
  const { user, isAuthenticated } = useAuth(); // Get user info from auth context
  const [content, setContent] = useState(children);
  const [isTranslating, setIsTranslating] = useState(false);
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [isTranslationAvailable, setIsTranslationAvailable] = useState(false);
  const [isPersonalizationAvailable, setIsPersonalizationAvailable] = useState(false);

  // Check if translation/personalization is applicable
  useEffect(() => {
    setIsTranslationAvailable(true); // Translation is always available
    setIsPersonalizationAvailable(isAuthenticated && user); // Personalization requires auth
  }, [isAuthenticated, user]);

  const handleTranslate = async () => {
    if (!isAuthenticated) {
      alert('Please sign in to use translation features');
      return;
    }

    setIsTranslating(true);
    try {
      const response = await fetch('/api/v1/content/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Assuming JWT token
        },
        body: JSON.stringify({
          content: children,
          target_language: 'ur' // Urdu
        })
      });

      if (response.ok) {
        const data = await response.json();
        setContent(data.translated_content);
      } else {
        alert('Translation failed. Using original content.');
      }
    } catch (error) {
      console.error('Translation error:', error);
      alert('Translation failed. Using original content.');
    } finally {
      setIsTranslating(false);
    }
  };

  const handlePersonalize = async () => {
    if (!isAuthenticated || !user) {
      alert('Please sign in to use personalization features');
      return;
    }

    setIsPersonalizing(true);
    try {
      const response = await fetch('/api/v1/content/personalize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          content: children,
          user_preferences: user.preferences || {}
        })
      });

      if (response.ok) {
        const data = await response.json();
        setContent(data.personalized_content);
      } else {
        alert('Personalization failed. Using original content.');
      }
    } catch (error) {
      console.error('Personalization error:', error);
      alert('Personalization failed. Using original content.');
    } finally {
      setIsPersonalizing(false);
    }
  };

  const handleReset = () => {
    setContent(children); // Reset to original content
  };

  return (
    <div className={className}>
      {/* Action buttons for translation and personalization */}
      <div style={{
        display: 'flex',
        gap: '10px',
        marginBottom: '20px',
        flexWrap: 'wrap'
      }}>
        {isTranslationAvailable && (
          <button
            onClick={handleTranslate}
            disabled={isTranslating}
            style={{
              padding: '8px 16px',
              backgroundColor: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: isTranslating ? 'not-allowed' : 'pointer',
              opacity: isTranslating ? 0.6 : 1
            }}
          >
            {isTranslating ? 'Translating...' : 'Translate to Urdu'}
          </button>
        )}

        {isPersonalizationAvailable && (
          <button
            onClick={handlePersonalize}
            disabled={isPersonalizing}
            style={{
              padding: '8px 16px',
              backgroundColor: '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: isPersonalizing ? 'not-allowed' : 'pointer',
              opacity: isPersonalizing ? 0.6 : 1
            }}
          >
            {isPersonalizing ? 'Personalizing...' : 'Personalize Content'}
          </button>
        )}

        {/* Reset button to show original content */}
        {content !== children && (
          <button
            onClick={handleReset}
            style={{
              padding: '8px 16px',
              backgroundColor: '#f44336',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Show Original
          </button>
        )}
      </div>

      {/* Render the content */}
      <div>
        {content}
      </div>
    </div>
  );
};

export default ChapterContent;