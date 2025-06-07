import { useMemo } from 'react';
import { useTheme } from '../context/ThemeContext';
import { getThemedImagePath, getImageVariants } from '../utils/imageUtils';

/**
 * Custom hook for getting theme-appropriate image paths
 * @param {string} imagePath - Original image path
 * @returns {string} - Theme-appropriate image path
 */
export const useThemedImage = (imagePath) => {
  const { theme } = useTheme();

  return useMemo(() => {
    return getThemedImagePath(imagePath, theme);
  }, [imagePath, theme]);
};

/**
 * Custom hook for preloading both theme variants of an image
 * @param {string|null} imagePath - Original image path or null to skip preloading
 */
export const usePreloadThemedImages = (imagePath) => {
  useMemo(() => {
    if (!imagePath) return;

    const variants = getImageVariants(imagePath);

    // Preload both variants
    Object.values(variants).forEach((path) => {
      if (path) {
        const img = new Image();
        img.src = path;
      }
    });
  }, [imagePath]);
};

export default useThemedImage;
