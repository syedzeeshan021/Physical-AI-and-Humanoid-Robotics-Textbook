import React, { useState } from 'react';
import './TranslationButton.css';

interface TranslationButtonProps {
  chapterId: string;
  content: string;
  onTranslationComplete: (translatedContent: string) => void;
  onReset: () => void;
  currentContent: string;
  originalContent: string;
}

const TranslationButton: React.FC<TranslationButtonProps> = ({
  chapterId,
  content,
  onTranslationComplete,
  onReset,
  currentContent,
  originalContent
}) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showError, setShowError] = useState(false);

  const handleTranslate = async () => {
    if (isTranslating) return;

    setIsTranslating(true);
    setError(null);
    setShowError(false);

    try {
      // Get the JWT token from localStorage
      const token = localStorage.getItem('access_token');

      if (!token) {
        throw new Error('User not authenticated. Please sign in to use translation features.');
      }

      const response = await fetch(`${process.env.REACT_APP_BACKEND_API_URL || 'http://localhost:8001/api/v1'}/translation/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          content: content,
          chapter_id: chapterId,
          target_language: 'ur'
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = errorData.detail || `Translation failed with status: ${response.status}`;
        throw new Error(errorMessage);
      }

      const data = await response.json();

      // Check if the response contains a fallback message
      if (data.translated_content.includes('Translation failed:')) {
        // This indicates the backend had an error and returned the original content with error message
        throw new Error('Translation service temporarily unavailable. Please try again later.');
      }

      onTranslationComplete(data.translated_content);
      setIsTranslated(true);
    } catch (err: any) {
      console.error('Translation error:', err);
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred during translation';
      setError(errorMessage);
      setShowError(true);

      // Provide user-friendly error message
      if (errorMessage.includes('403')) {
        alert('Your account must be verified to access translation features. Please verify your account.');
      } else if (errorMessage.includes('429')) {
        alert('You have reached the translation limit. Please try again later.');
      } else {
        alert(`Translation failed: ${errorMessage}. The original content will remain displayed.`);
      }
    } finally {
      setIsTranslating(false);
    }
  };

  const handleReset = () => {
    onReset();
    setIsTranslated(false);
  };

  const handleClick = () => {
    if (isTranslated) {
      handleReset();
    } else {
      handleTranslate();
    }
  };

  const handleRetry = () => {
    setError(null);
    setShowError(false);
    handleTranslate();
  };

  return (
    <div className="translation-button-container">
      <button
        onClick={handleClick}
        disabled={isTranslating}
        className={`translation-button ${isTranslating ? 'loading' : ''} ${isTranslated ? 'translated' : ''}`}
        aria-label={isTranslated ? 'Show original content' : 'Translate to Urdu'}
        title={isTranslated ? 'Show original content' : 'Translate to Urdu'}
      >
        {isTranslating ? (
          <>
            <span className="loading-spinner">🔄</span>
            <span className="button-text">Translating...</span>
          </>
        ) : (
          <>
            <span className="translation-icon">🌐</span>
            <span className="button-text">
              {isTranslated ? 'Translate back to English' : 'Translate to Urdu'}
            </span>
          </>
        )}
      </button>
      {showError && error && (
        <div className="translation-error">
          {error}
          <button
            onClick={handleRetry}
            className="retry-button"
            style={{
              marginLeft: '8px',
              padding: '2px 6px',
              backgroundColor: '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '3px',
              fontSize: '11px',
              cursor: 'pointer'
            }}
          >
            Retry
          </button>
        </div>
      )}
    </div>
  );
};

export default TranslationButton;