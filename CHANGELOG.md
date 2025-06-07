### [2025-06-07] - FS-01: Foundation and Refactoring

- **Added:**
  - Standardized `src/` directories for both backend and frontend to improve code organization.
  - Clear separation of Django (`django_project/`) and FastAPI (`fastapi_app/`) components within the backend.
  - Modular frontend structure with dedicated folders for components, services, hooks, store, and pages.

- **Changed:**
  - **Completed Task FS-01:** Restructured the entire project file system for clarity and maintainability.
  - Moved all backend and frontend source code into their respective new directories.
  - Updated all configuration files (`docker-compose.yml`, `package.json`, `.github/workflows/ci-cd.yml`, etc.) to reflect the new file paths.

- **Removed:**
  - Obsolete and redundant files from the root directory.