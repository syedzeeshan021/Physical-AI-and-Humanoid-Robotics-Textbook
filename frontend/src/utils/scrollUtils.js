/**
 * Utility functions for preserving scroll position during language switching
 */

// Store scroll position by chapter ID
const scrollPositions = new Map();

/**
 * Save the current scroll position for a specific chapter
 * @param {string} chapterId - The ID of the chapter
 */
export const saveScrollPosition = (chapterId) => {
  if (typeof window !== 'undefined') {
    const scrollY = window.scrollY || window.pageYOffset;
    scrollPositions.set(chapterId, scrollY);
  }
};

/**
 * Restore the saved scroll position for a specific chapter
 * @param {string} chapterId - The ID of the chapter
 * @param {number} delay - Delay in milliseconds before restoring (default: 100ms)
 */
export const restoreScrollPosition = (chapterId, delay = 100) => {
  if (typeof window !== 'undefined') {
    setTimeout(() => {
      const savedPosition = scrollPositions.get(chapterId);
      if (savedPosition !== undefined) {
        window.scrollTo({
          top: savedPosition,
          behavior: 'smooth'
        });
      } else {
        // If no saved position, scroll to top of the element
        const element = document.getElementById(chapterId);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
          // Default to top of page if no specific element
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }
    }, delay);
  }
};

/**
 * Get the saved scroll position for a chapter
 * @param {string} chapterId - The ID of the chapter
 * @returns {number|undefined} The saved scroll position or undefined if not found
 */
export const getSavedScrollPosition = (chapterId) => {
  return scrollPositions.get(chapterId);
};

/**
 * Clear saved scroll position for a chapter
 * @param {string} chapterId - The ID of the chapter
 */
export const clearScrollPosition = (chapterId) => {
  scrollPositions.delete(chapterId);
};

/**
 * Clear all saved scroll positions
 */
export const clearAllScrollPositions = () => {
  scrollPositions.clear();
};

/**
 * Hook to use scroll position preservation functionality
 * This would typically be used in React components
 */
export const useScrollPosition = (chapterId) => {
  const savePosition = () => saveScrollPosition(chapterId);
  const restorePosition = (delay) => restoreScrollPosition(chapterId, delay);

  return {
    savePosition,
    restorePosition,
    getSavedPosition: () => getSavedScrollPosition(chapterId),
    clearPosition: () => clearScrollPosition(chapterId)
  };
};