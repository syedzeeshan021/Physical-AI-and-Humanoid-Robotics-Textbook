import React, { useState, useEffect } from 'react';
import './button-styles.css';

const TranslationButton = ({ chapterId, content, children }) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);
  const [translatedContent, setTranslatedContent] = useState('');
  const [originalContent, setOriginalContent] = useState(children);

  // Check if user is logged in by checking for auth token
  const isLoggedIn = () => {
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    return !!token;
  };

  // Only show the button if user is logged in
  if (!isLoggedIn()) {
    return null;
  }

  const handleTranslate = async () => {
    if (isTranslated) {
      // Switch back to original content
      setIsTranslated(false);
      return;
    }

    setIsTranslating(true);
    try {
      const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');

      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          content: typeof children === 'string' ? children : content || '',
          chapter_id: chapterId,
          target_language: 'ur'
        })
      });

      if (response.ok) {
        const data = await response.json();
        setTranslatedContent(data.translated_content);
        setIsTranslated(true);
      } else {
        console.error('Translation failed:', response.status);
        // Show error to user
        alert('Translation failed. Please try again.');
      }
    } catch (error) {
      console.error('Translation error:', error);
      alert('Translation failed. Please try again.');
    } finally {
      setIsTranslating(false);
    }
  };

  const buttonText = isTranslated ? 'Translate back to English' : 'Translate to Urdu';
  const buttonClass = `translation-btn ${isTranslating ? 'loading' : ''} ${isTranslated ? 'translated' : ''}`;

  return (
    <div className="translation-container">
      <button
        onClick={handleTranslate}
        disabled={isTranslating}
        className={buttonClass}
        aria-label={isTranslated ? 'Switch back to English' : 'Translate to Urdu'}
      >
        {isTranslating ? (
          <>
            <span className="spinner"></span>
            Translating...
          </>
        ) : (
          buttonText
        )}
      </button>

      <div className={`translation-content ${isTranslated ? 'urdu-text' : ''}`}>
        {isTranslated ? (
          <div className="urdu-content">{translatedContent}</div>
        ) : (
          <div className="original-content">{children}</div>
        )}
      </div>
    </div>
  );
};

export default TranslationButton;