### Project Vision and Goals

Our primary goal is to evolve VentAI from a collection of tools into a fully integrated, intelligent platform that automates the entire HVAC engineering workflow. We will focus on creating a seamless user experience, powerful AI-driven insights, and end-to-end project management capabilities. The platform will be a one-stop solution for engineers, from initial calculations and design to procurement and project analysis.

### Execution Workflow

We will adopt a cyclical and iterative development process to ensure we stay on track, remain flexible, and continuously deliver value. This workflow is an enhanced version of the one outlined in the `REFACTOR_PLAN.md`.

1.  **Master Plan (This Document):** This document will serve as our single source of truth for the project roadmap. We will update it at the end of each phase to reflect our progress and incorporate any new insights.
2.  **Active Tasks:** We will maintain a list of active tasks, each with a unique ID, priority, and status. This will allow us to focus on the most critical items in each phase.
3.  **Implementation Sprints:** We will work in focused sprints, breaking down each task into smaller, manageable sub-tasks.
4.  **Verification and Testing:** All new features and refactoring will be accompanied by comprehensive tests to ensure quality and stability.
5.  **Changelog:** We will maintain a detailed changelog, documenting all significant changes, bug fixes, and new features. This will provide a clear history of our progress.
6.  **Cyclical Review:** At the end of each phase, we will review our progress against the master plan, update the task list, and plan the next phase. This will ensure that we remain aligned with the project's vision and can adapt to new requirements.

### Workflow Analysis (`ci-cd.yml` and `ci.yml`)

The current CI/CD setup is a solid foundation, with automated testing for both the backend and frontend. Here are my initial recommendations:

  * **Implement the Deployment Step:** The `deploy` job in `ci-cd.yml` is currently a placeholder. We need to implement a robust deployment script to automate the process of releasing new versions to production.
  * **Environment Configuration:** We should standardize the management of environment variables for different environments (development, testing, production) to ensure consistency and security.
  * **Security Scanning:** We should integrate automated security scanning into our CI/CD pipeline to identify and address potential vulnerabilities in our code and dependencies.

-----

### Master Development Plan

Here is the detailed master plan for the VentAI project, broken down into phases and tasks.

#### Phase 1: Foundation and Refactoring

This phase will focus on improving the project's structure, design, and core functionalities.

| ID | Task | Sub-tasks | Priority | Status |
| :--- | :--- | :--- | :--- | :--- |
| **CODE-01** | Backend Code Restructuring | - Complete the modular architecture design.\<br\>- Separate core modules (authentication, projects, calculators).\<br\>- Refactor database models for better scalability.\<br\>- Update all dependencies to the latest stable versions.\<br\>- Add comprehensive unit and integration tests for all modules. | High | In Progress |
| **CODE-02** | Frontend Code Restructuring | - Analyze the current frontend codebase.\<br\>- Implement a more modular and component-based architecture.\<br\>- Standardize state management with a global context or a library like Redux.\<br\>- Refactor the routing mechanism for better organization.\<br\>- Update all dependencies. | High | Pending |
| **FS-01** | File Structure Cleanup | - Remove the `@vent-ai-backend` folder and any other obsolete files.\<br\>- Organize the project into a cleaner, more intuitive structure.\<br\>- Update all relevant paths and import statements. | High | Pending |
| **UI-01** | UI/UX Redesign | - Conduct a thorough analysis of the current UI/UX.\<br\>- Create wireframes and mockups for a new, modern design.\<br\>- Develop a new, consistent design system (colors, typography, components).\<br\>- Implement a new, more intuitive navigation menu.\<br\>- Ensure the entire interface is responsive and mobile-friendly. | High | In Progress (Wireframes for Homepage, Dashboard, Calculators, Design System Plan, Homepage & Dashboard Implementation Complete) |
| **I18N-01** | Internationalization (i18n) | - Implement a robust i18n framework (e.g., `i18next`).\<br\>- Refactor all text to use translation keys.\<br\>- Create language files for English and Ukrainian.\<br\>- Implement a language switcher in the UI. | Medium | Pending |

#### Phase 2: AI-Powered Features

This phase will focus on integrating advanced AI capabilities into the platform.

| ID | Task | Sub-tasks | Priority | Status |
| :--- | :--- | :--- | :--- | :--- |
| **AI-01** | AI Dashboard | - Design a new, dedicated AI dashboard page.\<br\>- Integrate a chat interface for interacting with the AI.\<br\>- Develop widgets for displaying AI-driven insights and suggestions.\<br\>- Implement a system for tracking and managing AI tasks. | High | Pending |
| **AI-02** | Automated Project Analysis | - Develop a service for parsing various document formats (PDF, DOCX, etc.).\<br\>- Implement an OCR service for extracting text from images and scanned documents.\<br\>- Create a rules engine for automated compliance checking against Ukrainian building codes and regulations.\<br\>- Develop a system for identifying and extracting key project parameters (e.g., room dimensions, equipment specifications). | High | Pending |
| **DB-01** | Vector Database Integration | - Set up and configure a vector database (e.g., Pinecone, Weaviate).\<br\>- Develop a pipeline for converting project data and regulatory documents into vector embeddings.\<br\>- Implement a semantic search functionality to find relevant information and solutions.\<br\>- Create an API for querying the vector database. | High | Pending |
| **AI-03** | Cost Optimization Engine | - Develop an algorithm for analyzing project specifications and identifying cost-saving opportunities.\<br\>- Integrate with the vector database to find alternative materials and equipment.\<br\>- Create a feature for comparing different project scenarios and their associated costs. | High | Pending |

#### Phase 3: Advanced Automation and Integration

This phase will focus on automating procurement and other manual processes.

| ID | Task | Sub-tasks | Priority | Status |
| :--- | :--- | :--- | :--- | :--- |
| **AUTO-01**| Automated Price Verification| - Develop a system for scraping prices from supplier websites and online marketplaces.\<br\>- Implement a feature for cross-referencing prices from PDF specifications and invoices.\<br\>- Create a database for storing and tracking historical price data. | High | Pending |
| **AUTO-02**| Procurement Optimization | - Develop an algorithm for optimizing procurement based on price, location, and delivery time.\<br\>- Integrate with mapping services to calculate logistics costs.\<br\>- Create a feature for generating optimized purchase orders. | High | Pending |
| **CRM-01**| CRM Integration| - Research and select a CRM API for integration (e.g., HubSpot, Salesforce).\<br\>- Develop a system for creating and updating deals in the CRM based on project data.\<br\>- Implement a feature for syncing project status and communications with the CRM. | Medium | Pending |

I am ready to begin with **Phase 1**. I will start by completing the backend code restructuring (`CODE-01`) and then move on to the other tasks in this phase. I will keep the changelog updated with our progress and will provide regular updates. This structured approach will allow us to build a powerful and robust platform that will revolutionize the HVAC industry.
