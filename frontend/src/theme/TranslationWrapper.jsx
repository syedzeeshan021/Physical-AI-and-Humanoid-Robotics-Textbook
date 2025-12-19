import React from 'react';
import { ThemeClassNames } from '@docusaurus/theme-common';
import { useDoc } from '@docusaurus/useDoc';
import TranslationButton from '../components/TranslationButton';

/**
 * A wrapper component that adds translation functionality to Docusaurus docs
 */
function TranslationWrapper({ children }) {
  const { metadata } = useDoc();
  const { title, frontMatter, slug } = metadata;

  // Extract chapter ID from document metadata
  const chapterId = frontMatter?.chapter_id || slug || title.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className={ThemeClassNames.doc.docContainer}>
      {/* Translation button at the start of the chapter */}
      <div className="translation-button-container">
        <TranslationButton
          chapterId={chapterId}
          content={children?.props?.content || ''}
        >
          {children}
        </TranslationButton>
      </div>
    </div>
  );
}

export default TranslationWrapper;