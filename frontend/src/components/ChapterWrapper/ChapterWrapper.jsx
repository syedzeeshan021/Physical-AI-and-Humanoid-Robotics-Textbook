import React from 'react';
import ChapterContent from '../ChapterContent/ChapterContent';

const ChapterWrapper = ({ children }) => {
  return (
    <ChapterContent>
      {children}
    </ChapterContent>
  );
};

export default ChapterWrapper;