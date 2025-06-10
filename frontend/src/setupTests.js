// Optional: Configure or mock libraries used in tests
import '@testing-library/jest-dom';

// Mock for MUI to work in test environment
const originalModule = jest.requireActual('@mui/material');

jest.mock('@mui/material', () => ({
  ...originalModule,
  ThemeProvider: ({ children }) => children,
  useTheme: () => ({
    palette: {
      primary: { main: '#1976d2' },
      secondary: { main: '#dc004e' }
    }
  }),
  useMediaQuery: () => false
}));

// Mock other MUI components if necessary
jest.mock('@mui/material/Box', () => ({ children, ...props }) => <div {...props}>{children}</div>);
jest.mock('@mui/material/Typography', () => ({ children, ...props }) => <span {...props}>{children}</span>);
jest.mock('@mui/material/Grid', () => ({ children, ...props }) => <div {...props}>{children}</div>);
jest.mock('@mui/material/Paper', () => ({ children, ...props }) => <div {...props}>{children}</div>);
jest.mock('@mui/material/Button', () => ({ children, ...props }) => <button {...props}>{children}</button>);
jest.mock('@mui/material/Select', () => ({ children, ...props }) => <select {...props}>{children}</select>);
jest.mock('@mui/material/MenuItem', () => ({ children, ...props }) => <option {...props}>{children}</option>);
jest.mock('@mui/material/FormControl', () => ({ children, ...props }) => <div {...props}>{children}</div>);
jest.mock('@mui/material/InputLabel', () => ({ children, ...props }) => <label {...props}>{children}</label>);
