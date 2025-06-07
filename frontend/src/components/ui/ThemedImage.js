import React from 'react';
import { useThemedImage, usePreloadThemedImages } from '../../hooks/useThemedImage';
import './ThemedImage.css';

/**
 * Component for rendering theme-aware images
 * @param {Object} props
 * @param {string} props.src - Original image source path
 * @param {string} props.alt - Alt text for the image
 * @param {string} props.className - CSS classes
 * @param {Object} props.style - Inline styles
 * @param {boolean} props.preload - Whether to preload both theme variants
 * @param {Object} rest - Other image props (spread operator)
 */
const ThemedImage = ({ src, alt, className = '', style = {}, preload = true, ...rest }) => {
  // Get the appropriate image path for current theme
  const themedSrc = useThemedImage(src);

  // Preload both theme variants for smooth transitions
  usePreloadThemedImages(preload ? src : null);

  return (
    <img
      src={themedSrc}
      alt={alt}
      className={`themed-image ${className}`.trim()}
      style={style}
      {...rest}
    />
  );
};

export default ThemedImage;
