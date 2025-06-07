# Changelog

## [v3.0.0] - Advanced Automation and Integration - 2025-06-07
### Added
- **AUTO-01: Automated Price Verification** - Implemented automated price verification system with supplier API integration and web scraping, including scheduled tasks via Celery and API endpoints for manual verification and discrepancy resolution.
- **AUTO-02: Procurement Optimization** - Implemented procurement optimization system with supplier scoring based on price, location, and delivery time, integration with mapping services, and purchase order generation capabilities.
- **CRM-01: CRM Integration** - Implemented CRM integration with HubSpot, enabling synchronization of VentAI projects with CRM deals, real-time updates via webhooks, and API endpoints for setup and status management.

## [v2.1.0] - 2025-06-07
### Added
- **AI-01: AI Dashboard**: Implemented a new unified dashboard for all AI interactions, including chat, content generation, and project-specific analysis.
- **AI-02: Automated Project Analysis**:
  - Implemented backend service (`project_analysis_service.py`) and FastAPI endpoints for core analysis logic.
  - Added frontend components to `AIDashboard.tsx` to display simulated analysis results.
- **AI-02: Automated Project Analysis** - Completed implementation of automated project analysis feature with dynamic compliance rules loaded from a JSON configuration file for improved maintainability.
- **DB-01: Vector Database Integration** - Implemented vector database integration using Pinecone for semantic search capabilities, with backend services and API endpoints for data ingestion and querying.
- **AI-03: Cost Optimization Engine** - Implemented cost optimization engine with cost analysis, scenario comparison, and material suggestion features integrated with vector database for cost-effective solutions.

### Fixed
- **FIXME-01.4: Backend Docker Unhealthy Status**: Resolved issue causing the backend development container to report as unhealthy. Ensured `curl` is correctly installed and accessible for the healthcheck command (`curl -f http://localhost:8000/docs`) in `backend/Dockerfile.dev`.
- **FIXME-02.1: Frontend Docker Unhealthy Status**: Resolved issue causing the frontend development container to report as unhealthy. Ensured `curl` is correctly installed via `apk add --no-cache curl` and accessible for the healthcheck command (`curl -f http://localhost:3000`) in `frontend/Dockerfile.dev`.

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

## [3.1.0] - 2025-06-07
### Fixed
- **TECH-DEBT-01**: Resolved TypeScript module declaration lint errors in frontend by installing missing type declarations (`@types/axios`, `@types/react-i18next`), replacing `any` with safer types, and updating ESLint configuration for TypeScript linting.

## [0.1.0] - 2025-06-07
### Fixed
- **TECH-DEBT-02**: Resolved ESLint configuration issues for React 17+ with TypeScript and Jest, using ESLint 8.57.0's flat config system.