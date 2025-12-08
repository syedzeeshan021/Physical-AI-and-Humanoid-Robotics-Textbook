import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';
import ApiService from '../../services/api';

interface TextSelectionPopupProps {
  onQuerySubmit?: (query: string) => void;
}

const TextSelectionPopup: React.FC<TextSelectionPopupProps> = ({ onQuerySubmit }) => {
  const [selectedText, setSelectedText] = useState<string>('');
  const [showPopup, setShowPopup] = useState<boolean>(false);
  const [position, setPosition] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const popupRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim() || '';

      if (text.length > 0 && selection?.anchorOffset !== selection?.focusOffset) {
        const range = selection?.getRangeAt(0);
        const rect = range?.getBoundingClientRect();

        if (rect) {
          setPosition({
            x: rect.left + window.scrollX,
            y: rect.top + window.scrollY - 40, // Position above the selected text
          });
          setSelectedText(text);
          setShowPopup(true);
        }
      } else {
        setShowPopup(false);
      }
    };

    const handleClick = (event: MouseEvent) => {
      // Check if click is outside the popup
      if (popupRef.current && !popupRef.current.contains(event.target as Node)) {
        setShowPopup(false);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('click', handleClick);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('click', handleClick);
    };
  }, []);

  const handleAskAI = async () => {
    if (selectedText) {
      setIsLoading(true);
      try {
        if (onQuerySubmit) {
          // Use the callback if provided (for backward compatibility)
          onQuerySubmit(selectedText);
        } else {
          // Directly call the API service if no callback provided
          const response = await ApiService.queryRag(selectedText);
          // Optionally display the response in a chat widget or notification
          console.log('RAG Response:', response);
        }
      } catch (error) {
        console.error('Error querying RAG:', error);
      } finally {
        setShowPopup(false);
        setIsLoading(false);
      }
    }
  };

  if (!showPopup || !selectedText) {
    return null;
  }

  return (
    <div
      ref={popupRef}
      className={styles.popup}
      style={{ left: position.x, top: position.y }}
    >
      <button
        className={styles.askButton}
        onClick={handleAskAI}
        disabled={isLoading}
      >
        {isLoading ? 'Asking...' : 'Ask AI about this'}
      </button>
    </div>
  );
};

export default TextSelectionPopup;