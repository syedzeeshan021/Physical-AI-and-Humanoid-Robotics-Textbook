/**
 * Utility functions for chapter identification and management
 */

/**
 * Extract chapter ID from URL or page context
 * @returns {string} Chapter identifier
 */
export const getCurrentChapterId = () => {
  if (typeof window === 'undefined') {
    return 'unknown';
  }

  // Try to extract from URL path
  const path = window.location.pathname;
  const pathParts = path.split('/').filter(part => part.length > 0);

  // For Docusaurus, the chapter ID is often the last part of the path
  if (pathParts.length > 0) {
    return pathParts[pathParts.length - 1];
  }

  // Fallback to page title or a default value
  return 'default-chapter';
};

/**
 * Get chapter reference based on page context
 * @param {string} fallbackId - Fallback ID if chapter cannot be determined
 * @returns {string} Chapter reference
 */
export const getChapterReference = (fallbackId = 'unknown-chapter') => {
  // In a Docusaurus context, we might get this from page metadata
  // For now, using URL-based approach
  const chapterId = getCurrentChapterId();
  return chapterId !== 'unknown' ? chapterId : fallbackId;
};

/**
 * Normalize chapter ID to a consistent format
 * @param {string} chapterId - Raw chapter ID
 * @returns {string} Normalized chapter ID
 */
export const normalizeChapterId = (chapterId) => {
  if (!chapterId) return 'unknown';

  return chapterId
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '')
    .substring(0, 100); // Limit length
};

/**
 * Check if the current page is a valid chapter page
 * @returns {boolean} True if the current page is a chapter page
 */
export const isChapterPage = () => {
  if (typeof window === 'undefined') {
    return false;
  }

  const path = window.location.pathname;

  // Common patterns for chapter pages in Docusaurus
  const chapterPatterns = [
    /^\/docs\//,      // Standard docs route
    /^\/category\//,  // Category pages
    /\.html$/,        // HTML pages
  ];

  return chapterPatterns.some(pattern => pattern.test(path));
};

/**
 * Get content from a specific element or the entire page
 * @param {string} selector - CSS selector for the content element
 * @returns {string} Extracted content
 */
export const extractChapterContent = (selector = 'article, .theme-doc-markdown') => {
  if (typeof document === 'undefined') {
    return '';
  }

  const element = document.querySelector(selector);
  if (!element) {
    return '';
  }

  // Extract text content, preserving paragraph structure
  const paragraphs = Array.from(element.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, td, th'));
  return paragraphs.map(p => p.textContent.trim()).filter(text => text.length > 0).join('\n\n');
};

/**
 * Get all chapter-related metadata
 * @returns {object} Chapter metadata
 */
export const getChapterMetadata = () => {
  if (typeof document === 'undefined') {
    return {};
  }

  // Try to get metadata from page
  const title = document.title || '';
  const description = document.querySelector('meta[name="description"]')?.content || '';
  const h1 = document.querySelector('h1')?.textContent || '';

  const chapterId = normalizeChapterId(
    getCurrentChapterId() ||
    h1 ||
    title.split(' | ')[0] // Remove site name from title
  );

  return {
    id: chapterId,
    title: h1 || title,
    description,
    isChapter: isChapterPage()
  };
};