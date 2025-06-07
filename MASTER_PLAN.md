### Project Vision and Goals

Our primary goal is to evolve VentAI from a collection of tools into a fully integrated, intelligent platform that automates the entire HVAC engineering workflow. We will focus on creating a seamless user experience, powerful AI-driven insights, and end-to-end project management capabilities. The platform will be a one-stop solution for engineers, from initial calculations and design to procurement and project analysis.

### Execution Workflow

We will adopt a cyclical and iterative development process to ensure we stay on track, remain flexible, and continuously deliver value.

1.  **Master Plan (This Document):** Serves as our single source of truth for the project roadmap.
2.  **Active Tasks:** We will maintain a list of active tasks with unique IDs, priorities, and statuses.
3.  **Implementation Sprints:** We will work in focused sprints, breaking down tasks into smaller sub-tasks.
4.  **Verification and Testing:** All new features and refactoring will be accompanied by comprehensive tests.
5.  **Changelog:** We will maintain a detailed changelog for all significant changes.
6.  **Cyclical Review:** We will review our progress against the master plan at the end of each phase.
7.  **Critical Bug Fix Mode:** If a critical bug arises that blocks core functionality (e.g., server startup), all other tasks are suspended. The entire focus shifts to resolving the critical bug.

### Workflow Analysis (`ci-cd.yml` and `ci.yml`)

The current CI/CD setup is a solid foundation. Recommendations remain:
  * Implement the Deployment Step.
  * Standardize Environment Configuration.
  * Integrate Security Scanning.

-----

### Master Development Plan

#### Phase 1: Foundation and Refactoring

| ID | Task | Sub-tasks | Priority | Status |
| :--- | :--- | :--- | :--- | :--- |
| **CODE-01** | Backend Code Restructuring | - Complete modular architecture, separate modules, refactor models, update dependencies, add tests. | High | **Completed** |
| **CODE-02** | Frontend Code Restructuring| - Implement modular architecture, standardize state management, refactor routing, update dependencies. | High | **Completed** |
| **FS-01** | File Structure Cleanup | - Remove obsolete files, organize project structure, update all relevant paths. | High | **Completed** |
| **UI-01** | UI/UX Redesign | - Conduct analysis, create wireframes, develop design system, implement navigation, ensure responsiveness. | High | **Completed** |
| **I18N-01** | Internationalization (i18n)| - Implement i18n framework, refactor text to use translation keys, create language files, implement switcher. | Medium | Pending |

#### Phase 2: AI-Powered Features

| ID | Task | Sub-tasks | Priority | Status |
| :--- | :--- | :--- | :--- | :--- |
| **AI-01** | AI Dashboard | - Audit components, create unified dashboard, implement project-specific insights. | High | **Completed** |
| **AI-02** | Automated Project Analysis | - Develop analysis algorithms, integrate with project management, provide insights and compliance checks. | High | **In Progress (Implementation Blocked by `FIXME-01`, `FIXME-02`)** |
| **DB-01** | Vector Database Integration | - Setup vector DB, create data pipeline, implement semantic search, create query API. | High | Pending |
| **AI-03** | Cost Optimization Engine | - Develop cost analysis algorithm, integrate with vector DB for material search, create scenario comparison feature. | High | Pending |

#### Phase 3: Advanced Automation and Integration

| ID | Task | Sub-tasks | Priority | Status |
| :--- | :--- | :--- | :--- | :--- |
| **AUTO-01**| Automated Price Verification| - Develop price scraping system, cross-reference prices from PDFs, create historical price database. | High | Pending |
| **AUTO-02**| Procurement Optimization | - Develop procurement algorithm based on price/location/time, integrate with mapping services, generate purchase orders. | High | Pending |
| **CRM-01**| CRM Integration| - Research and select CRM API, develop deal creation system, sync project status with CRM. | Medium | Pending |

---
### Technical Debt and Known Issues

| ID | Task | Priority | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **FIXME-01**| Backend Server Startup Issue | **CRITICAL** | **Active** | `python` command not found in Docker environment. Blocks all backend functionality. |
| **FIXME-02**| Frontend Server Startup Issue| **CRITICAL** | **Active** | Missing `index.js` file, preventing frontend server start. |
| **TECH-DEBT-01**| Resolve TypeScript module declarations | Low | Pending | Address lint errors in `App.tsx` and other files related to missing module declarations. |