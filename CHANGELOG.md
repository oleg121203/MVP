# Changelog

## [v2.1.0] - 2025-06-07
### Added
- **AI-01: AI Dashboard**: Implemented a new unified dashboard for all AI interactions, including chat, content generation, and project-specific analysis.
- **AI-02: Automated Project Analysis**:
  - Implemented backend service (`project_analysis_service.py`) and FastAPI endpoints for core analysis logic.
  - Added frontend components to `AIDashboard.tsx` to display simulated analysis results.

### Changed
- **UI-01: UI/UX Redesign**:
  - Implemented a complete redesign of the user interface, including a new navigation menu, color scheme, and typography.
  - **Homepage**: Rebuilt with an enhanced hero section, capabilities overview, testimonials, and clear calls-to-action.
  - **Project Management**: Implemented a new, dedicated page for managing projects.
  - **Responsiveness**: Updated all key pages to be fully responsive across mobile, tablet, and desktop devices.
- **Infrastructure**:
  - Updated `Navigation.tsx` and `App.tsx` to include routes for all new pages and features.
  - Updated `MASTER_PLAN.md` to reflect the completion of Phase 1 and progress on Phase 2.

## [v2.0.0] - 2025-06-07
### Added
- Standardized `src/` directories for both backend and frontend to improve code organization.
- Clear separation of Django (`django_project/`) and FastAPI (`fastapi_app/`) components within the backend.
- Modular frontend structure with dedicated folders for components, services, hooks, store, and pages.

### Changed
- **FS-01: File Structure Cleanup**: Completed a full restructuring of the project file system for clarity and maintainability.
- Updated all configuration files (`docker-compose.yml`, `package.json`, `.github/workflows/ci-cd.yml`, etc.) to reflect the new file paths.

### Removed
- Obsolete and redundant files from the root directory.