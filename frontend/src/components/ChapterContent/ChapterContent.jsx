import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import { useAuth } from '../Auth/AuthContext'; // Assuming we have an auth context
import TranslationButton from '../TranslationButton/TranslationButton';

const ChapterContent = ({ children, className }) => {
  const location = useLocation();
  const { user, isAuthenticated } = useAuth(); // Get user info from auth context
  const [content, setContent] = useState(children);
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [isPersonalizationAvailable, setIsPersonalizationAvailable] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);
  const [originalContent, setOriginalContent] = useState(children);

  // Extract chapter ID from the URL path
  const getChapterId = () => {
    const pathParts = location.pathname.split('/');
    // For paths like /chapters/introduction-to-physical-ai, the chapter id is the last part
    const chapterId = pathParts[pathParts.length - 1];
    return chapterId || 'unknown';
  };

  // Check if personalization is applicable
  useEffect(() => {
    setIsPersonalizationAvailable(isAuthenticated && user); // Personalization requires auth
  }, [isAuthenticated, user]);

  const handleTranslationComplete = (translatedContent) => {
    setContent(translatedContent);
    setIsTranslated(true);
  };

  const handleReset = () => {
    setContent(originalContent);
    setIsTranslated(false);
  };

  // Update original content if children change
  useEffect(() => {
    setOriginalContent(children);
    if (!isTranslated) {
      setContent(children);
    }
  }, [children]);

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

  return (
    <div className={className}>
      {/* Translation button at the start of the chapter */}
      {isAuthenticated && (
        <TranslationButton
          chapterId={getChapterId()}
          content={children}
          onTranslationComplete={handleTranslationComplete}
          onReset={handleReset}
          currentContent={content}
          originalContent={originalContent}
        />
      )}

      {/* Personalization button */}
      {isPersonalizationAvailable && (
        <div style={{ marginBottom: '1rem' }}>
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
        </div>
      )}

      {/* Render the content with proper styling for Urdu if translated */}
      <div className={isTranslated ? 'translation-content-urdu' : ''}>
        {content}
      </div>
    </div>
  );
};

export default ChapterContent;