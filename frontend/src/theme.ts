import { extendTheme } from '@chakra-ui/react';

export default extendTheme({
  colors: {
    brand: {
      primary: '#008080', // Teal for primary actions and accents
      secondary: '#4A5568', // Gray for secondary text and elements
    },
    background: {
      main: '#FFFFFF', // White for main content areas
      light: '#F7FAFC', // Light Gray for subtle differentiation
    },
    text: {
      primary: '#2D3748', // Dark Gray for readability
      secondary: '#718096', // Medium Gray for captions or less prominent text
    },
    feedback: {
      success: '#48BB78', // Green for success messages
      warning: '#ECC94B', // Yellow for warnings
      error: '#E53E3E', // Red for errors or critical alerts
    },
    tags: {
      basic: '#48BB78', // Green for Basic level indicators
      advanced: '#ED8936', // Orange for Advanced level indicators
    },
  },
  fonts: {
    heading: 'Inter, sans-serif',
    body: 'Inter, sans-serif',
  },
  fontSizes: {
    h1: '36px',
    h2: '28px',
    h3: '20px',
    subheading: '18px',
    body: '16px',
    caption: '14px',
    button: '14px',
  },
  lineHeights: {
    heading: 1.2,
    body: 1.5,
  },
  space: {
    base: '8px', // Base grid unit for spacing
    small: '16px',
    medium: '24px',
    large: '32px',
    xlarge: '48px',
  },
  components: {
    Button: {
      variants: {
        primary: {
          bg: 'brand.primary',
          color: 'white',
          borderRadius: '4px',
          _hover: {
            bg: '#007070', // Darkened teal on hover
          },
          _disabled: {
            opacity: 0.5,
            cursor: 'not-allowed',
          },
        },
        secondary: {
          border: '1px solid',
          borderColor: 'brand.primary',
          color: 'brand.primary',
          bg: 'background.main',
          borderRadius: '4px',
          _hover: {
            bg: 'rgba(0, 128, 128, 0.1)', // Light teal fill on hover
          },
        },
      },
      sizes: {
        sm: { fontSize: '12px', px: 3, py: 2 },
        md: { fontSize: '14px', px: 4, py: 2.5 },
        lg: { fontSize: '16px', px: 5, py: 3 },
      },
    },
    Card: {
      baseStyle: {
        bg: 'background.main',
        border: '1px solid',
        borderColor: '#E2E8F0',
        boxShadow: 'md',
        p: 'medium',
        _hover: {
          boxShadow: 'lg', // Slight lift effect on hover if interactive
        },
      },
    },
    Input: {
      baseStyle: {
        field: {
          border: '1px solid',
          borderColor: '#E2E8F0',
          _focus: {
            borderColor: 'brand.primary',
            boxShadow: '0 0 0 2px rgba(0, 128, 128, 0.2)',
          },
          _invalid: {
            borderColor: 'feedback.error',
            boxShadow: '0 0 0 2px rgba(229, 62, 62, 0.2)',
          },
          placeholder: { color: 'text.secondary' },
        },
      },
    },
    Tabs: {
      variants: {
        line: {
          tab: {
            _selected: {
              color: 'brand.primary',
              borderBottom: '2px solid',
              borderColor: 'brand.primary',
              fontWeight: 'bold',
            },
            _hover: {
              color: 'brand.primary',
              borderBottom: '2px solid',
              borderColor: 'rgba(0, 128, 128, 0.5)',
            },
            color: 'text.secondary',
          },
        },
      },
    },
  },
  breakpoints: {
    sm: '30em', // 480px - Mobile Portrait
    md: '48em', // 768px - Mobile Landscape
    lg: '64em', // 1024px - Tablet
    xl: '75em', // 1200px - Desktop
  },
  config: {
    initialColorMode: 'light',
    useSystemColorMode: false,
  },
});
