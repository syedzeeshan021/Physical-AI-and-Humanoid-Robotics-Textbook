import { useState, useCallback } from 'react';

const useLanguageSwitch = (initialContent, chapterId) => {
  const [currentLanguage, setCurrentLanguage] = useState('en'); // Default to English
  const [translatedContent, setTranslatedContent] = useState('');
  const [isTranslating, setIsTranslating] = useState(false);
  const [translationError, setTranslationError] = useState(null);

  const switchLanguage = useCallback(async () => {
    if (currentLanguage === 'en') {
      // Switch to Urdu - need to translate
      setIsTranslating(true);
      setTranslationError(null);

      try {
        const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');

        if (!token) {
          throw new Error('User not authenticated');
        }

        const response = await fetch('/api/translate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            content: initialContent,
            chapter_id: chapterId,
            target_language: 'ur'
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Translation failed');
        }

        const data = await response.json();
        setTranslatedContent(data.translated_content);
        setCurrentLanguage('ur');
      } catch (error) {
        console.error('Translation error:', error);
        setTranslationError(error.message);
        // Optionally show user-friendly message
        alert(`Translation failed: ${error.message}`);
      } finally {
        setIsTranslating(false);
      }
    } else {
      // Switch back to English
      setCurrentLanguage('en');
    }
  }, [currentLanguage, initialContent, chapterId]);

  const toggleLanguage = useCallback(() => {
    switchLanguage();
  }, [switchLanguage]);

  const resetLanguage = useCallback(() => {
    setCurrentLanguage('en');
    setTranslatedContent('');
    setTranslationError(null);
  }, []);

  return {
    currentLanguage,
    isTranslating,
    translationError,
    translatedContent,
    toggleLanguage,
    resetLanguage,
    isUrdu: currentLanguage === 'ur',
    isEnglish: currentLanguage === 'en'
  };
};

export default useLanguageSwitch;