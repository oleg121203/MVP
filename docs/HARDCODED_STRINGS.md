# Hardcoded Strings in Frontend Components

This document lists files with hardcoded user-facing text in `frontend/src/components/` and `frontend/src/pages/` for extraction to translation files as part of TASK-ID-013.

## Files with Hardcoded Strings
- **frontend/src/components/common/ProtectedRoute.js**: 
  - 'Loading...'
- **frontend/src/layouts/MainLayout.tsx**: 
  - 'VentAI'
  - 'VentAI Menu'
  - '&copy; {new Date().getFullYear()} VentAI. All rights reserved.'
- **frontend/src/pages/HomePage.tsx**: 
  - Multiple hardcoded strings (e.g., 'Welcome to VentAI', 'AI-Powered Project Management', etc.)
- **frontend/src/pages/DashboardPage.tsx**: 
  - 'Dashboard'
  - 'Here you can manage your projects and view insights.'
- **frontend/src/pages/CalculatorsPage.tsx**: 
  - 'Calculators'
  - 'Use these tools to perform various calculations for your projects.'
- **frontend/src/pages/AIDashboard.tsx**: 
  - Multiple hardcoded strings related to AI features and project analysis.

## Summary of Key Files with Hardcoded Strings

After a comprehensive search of the frontend codebase, the following key files have been identified as containing hardcoded user-facing strings that need to be extracted for internationalization:

- `frontend/src/App.js`: Contains placeholder text for various pages (e.g., 'Projects Page (Placeholder)').
- `frontend/src/components/common/Navigation.tsx`: Navigation menu items and UI text.
- `frontend/src/pages/HomePage.tsx`: Homepage content with hardcoded headings and descriptions.
- `frontend/src/pages/DashboardPage.tsx`: Dashboard UI elements and titles.
- `frontend/src/pages/CalculatorsPage.tsx`: Calculator interface text.
- `frontend/src/components/auth/LoginForm.tsx`: Login form labels and messages.
- `frontend/src/components/auth/RegisterForm.tsx`: Registration form labels and messages.

## Next Steps
- **TASK-ID-013.1**: Create a comprehensive list of all hardcoded strings with their file locations.
- **TASK-ID-013.2**: Extract these strings to translation files in `frontend/src/locales/` with appropriate keys.

## Next Steps (TASK-ID-013.2)

The next action is to extract these hardcoded strings into translation files compatible with `react-i18next`. This will involve creating JSON files for each supported language and replacing the hardcoded strings with calls to the translation function `t()`.

A systematic approach will be taken, starting with the most user-visible components like Navigation and HomePage, then moving to forms and other pages.
