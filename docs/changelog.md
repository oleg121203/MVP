# Changelog

## [Unreleased]

### 2025-06-04
- Completed Task 1.1.4: Updated handleGenerateProposal in ProjectDetailPage.js to use axios blob response from generateCommercialProposalForProject, removed response.blob(), and used response.data (the blob) and Content-Disposition header for filename. This matches the new apiService.js contract per instruction.md.
- Completed Task 1.3.4: Refined Card.css and Card.js to use CSS variables for light/dark theme support. All card backgrounds, borders, and header/footer colors are now controlled by CSS variables for consistent theming.

- Completed Task 1.3.3: Refactored Modal.js to use only CSS classes from Modal.css for all modal structure and theming. Removed all inline and Tailwind classes. Modal appearance and transitions are now fully controlled by CSS and CSS variables.

- Completed Task 1.3.2: Centralized input styling logic in Input.css and refactored Input.js to use only CSS classes for all styles, removing inline and Tailwind classes. Input component now supports size and error props for styling.

- Completed Task 1.3.1: Centralized button styles in Button.css, refactored Button.js to use CSS classes and variables, removing inline/Tailwind styles. All Button instances now use variant props and CSS.

- Completed Task 1.2.3: Updated all Duct Area Calculator modules in src/components/calculators/area/ to use the 't' prop instead of 'getTranslation', and replaced all getTranslation('key') calls with t('key').

- Completed Phase 1, Section 1.2: Refactored specification CRUD UI in ProjectDetailPage.js to fully use new API service functions (getSpecificationsByProject, createSpecification, updateSpecification, deleteSpecification, searchSpecifications). All actions now update UI state, provide user feedback via useToast, and use global localization for text. Duplicate handler bugs and redeclaration errors resolved.

- Completed Phase 1, Section 1.1: Refactored `src/services/apiService.js` to use Axios for all API calls with interceptors for authentication and error handling. Updated `src/context/AuthContext.js` to use new API service functions for login, registration, and user retrieval. Updated `handleGenerateProposal` in `ProjectDetailPage.js` to handle Axios blob response for file downloads.
- Started Phase 1, Section 1.2: Began CRUD UI for specifications in `ProjectDetailPage.js` using new API service functions (`getSpecificationsByProject`, `createSpecification`, `updateSpecification`, `deleteSpecification`, `searchSpecifications`).

- Added dbn_clause_reference field to ComplianceFinding in schemas.py for DBN clause citation in compliance reports.

- Implemented ProjectAnalysisWizard.js and ProjectAnalysisWizard.css for the interactive AI-driven project analysis refinement wizard (modal Q&A for clarifying project documents).

- Added full frontend integration for Specification CRUD and semantic search in ProjectDetailPage.js, using new API service functions.
- Created SpecificationFormModal.js for modal-based create/edit of specifications.
- Standardized all frontend API calls in `src/services/apiService.js` to use Axios, with global request/response interceptors and improved error handling. (Phase 1, Section 1.1)
- Updated `src/context/AuthContext.js` to use API service functions (`apiLoginUser`, `apiRegisterUser`, `apiGetCurrentUser`) for authentication and registration logic. (Phase 1, Task 1.1.3)
- Updated `handleGenerateProposal` in `src/pages/ProjectDetailPage.js` to use the new `generateCommercialProposalForProject` API service, handle axios blob response, and update download logic. (Phase 1, Task 1.1.4)

### Added
- Added new specification service functions to `apiService.js` for CRUD and search.
- Integrated new `crud_specification` service into FastAPI endpoints in `main.py`.
- Placeholder vector embedding generation in `crud_specification.py` using `ai_services.py`.
- Standardized API service using Axios with interceptors
- Unified localization system for Duct Area Calculator
- Core setup for frontend infrastructure
- Comprehensive error handling in API service
- Request/response interceptors for centralized auth and error handling
- Centralized translation context for consistent localization
- Support for dynamic language switching across all calculator modules
- Structured data model for HVAC components with dimensions, materials, and specifications
- Vector embedding support for semantic search of specifications
- Database migration for enhanced Specification and Project models
- Support for component dimensions, materials, and performance characteristics in the database
- Advanced search and filtering for specifications with support for component types, materials, and performance metrics
- Statistics generation for specifications (counts by type, material, criticality)
- Document upload and analysis workflow in ProjectDetailPage
- Support for PDF, Word, and image file uploads with validation
- Interactive analysis wizard for refining document extraction results
- Integration with backend analysis endpoints for structured data extraction

### Changed
- Refactored all API calls to use Axios instead of fetch
- Standardized error responses across all API calls
- Improved error messages and error handling
- Updated file upload handling to work with Axios
- Streamlined API service methods with consistent return values
- Refactored Duct Area Calculator to use global localization context
- Updated all calculator modules to use the `t` function prop for translations
- Standardized translation keys across all components
- Enhanced Specification model to support structured HVAC component data
- Updated Project model to include vector embeddings for specifications
- Improved database schema for better performance and data integrity
- Updated migration scripts to handle new model structures
- Enhanced CRUD operations for Specification model with better query capabilities
- Improved update operations to only modify provided fields using exclude_unset

### Fixed
- Removed duplicate function declarations in API service
- Fixed issues with file uploads and blob responses
- Improved handling of authentication tokens
- Fixed potential memory leaks in API error handling

### Removed
- Redundant fetch-based API calls
- Duplicate code for request/response handling
- Outdated error handling logic

## [0.1.0] - 2025-06-04
### Initial Release
- Base project structure
- Core functionality implemented
