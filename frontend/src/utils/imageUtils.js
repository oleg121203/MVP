/**
 * Utility functions for handling theme-based images in the Duct Area Calculator
 *
 * Note: Currently, dark theme versions use the same images as light theme.
 * CSS filters are applied automatically to darken images in dark theme.
 * Future enhancement: Create dedicated dark theme image variants.
 */

// Mapping from old image names to new corrected ones
const IMAGE_MAPPING = {
  // Straight ducts
  'straight_round_duct.svg': {
    light: '/images/ductwork_round_correction.png',
    dark: '/images/ductwork_round_correction.png', // CSS фільтри затемнять автоматично
  },
  'straight_rectangular_duct.svg': {
    light: '/images/ductwork_rectangular_correction.png',
    dark: '/images/ductwork_rectangular_correction.png', // CSS фільтри затемнять автоматично
  },

  // Bends
  'bend_round_duct.svg': {
    light: '/images/ductwork_round_correction.png', // використовуємо основну картинку
    dark: '/images/ductwork_round_correction.png',
  },
  'bend_rectangular_duct.svg': {
    light: '/images/ductwork_rectangular_correction.png',
    dark: '/images/ductwork_rectangular_correction.png',
  },

  // Transitions
  'transition_round_to_round.svg': {
    light: '/images/transition_round_round_correction.png',
    dark: '/images/transition_round_round_correction.png',
  },
  'transition_rect_to_round.svg': {
    light: '/images/transition_round_rectangular_correction.png',
    dark: '/images/transition_round_rectangular_correction.png',
  },
  'transition_rect_to_rect.svg': {
    light: '/images/transition_rectangular_rectangular.png',
    dark: '/images/transition_rectangular_rectangular.png',
  },

  // Tees
  'tee_round_duct.svg': {
    light: '/images/tee_output_round_round_correction.png',
    dark: '/images/tee_output_round_round_correction.png',
  },
  'tee_rectangular_duct.svg': {
    light: '/images/tee_output_rectangular_rectangular_correction.png',
    dark: '/images/tee_output_rectangular_rectangular_correction.png',
  },

  // Caps
  'cap_round_duct.svg': {
    light: '/images/cap_round_correction.png',
    dark: '/images/cap_round_correction.png',
  },
  'cap_rectangular_duct.svg': {
    light: '/images/cap_rectangular_correction.png',
    dark: '/images/cap_rectangular_correction.png',
  },

  // Cut-ins
  'cutin_round_duct.svg': {
    light: '/images/incut_straight_round_correction.png',
    dark: '/images/incut_straight_round_correction.png',
  },
  'cutin_rectangular_duct.svg': {
    light: '/images/incut_straight_rectangular_correction.png',
    dark: '/images/incut_straight_rectangular_correction.png',
  },

  // Offsets
  'offset_round_duct.svg': {
    light: '/images/duck_one_correction.png', // найближча за змістом
    dark: '/images/duck_one_correction.png',
  },
  'offset_rectangular_duct.svg': {
    light: '/images/duck_two_correction.png',
    dark: '/images/duck_two_correction.png',
  },

  // Hoods
  'hood_round_duct.svg': {
    light: '/images/canopy_blunt_correction.png',
    dark: '/images/canopy_blunt_correction.png',
  },
  'hood_rectangular_duct.svg': {
    light: '/images/canopy_sharp_correction.png',
    dark: '/images/canopy_sharp_correction.png',
  },
};

/**
 * Get the appropriate image path based on current theme
 * @param {string} originalPath - Original image path (e.g., '/images/straight_round_duct.svg')
 * @param {string} theme - Current theme ('light' or 'dark')
 * @returns {string} - Appropriate image path for the theme
 */
export const getThemedImagePath = (originalPath, theme = 'light') => {
  // Extract filename from path
  const filename = originalPath.split('/').pop();

  // Get mapping for this image
  const mapping = IMAGE_MAPPING[filename];

  if (mapping) {
    return mapping[theme] || mapping.light;
  }

  // Fallback to original path if no mapping found
  return originalPath;
};

/**
 * Check if an image has theme-specific versions
 * @param {string} originalPath - Original image path
 * @returns {boolean} - Whether the image has theme variants
 */
export const hasThemeVariants = (originalPath) => {
  const filename = originalPath.split('/').pop();
  return IMAGE_MAPPING.hasOwnProperty(filename);
};

/**
 * Get all available theme variants for an image
 * @param {string} originalPath - Original image path
 * @returns {Object} - Object with light and dark paths
 */
export const getImageVariants = (originalPath) => {
  const filename = originalPath.split('/').pop();
  const mapping = IMAGE_MAPPING[filename];

  if (mapping) {
    return mapping;
  }

  // Return original path for both themes if no mapping
  return {
    light: originalPath,
    dark: originalPath,
  };
};

const imageUtils = {
  getThemedImagePath,
  hasThemeVariants,
  getImageVariants,
  IMAGE_MAPPING,
};

export default imageUtils;
