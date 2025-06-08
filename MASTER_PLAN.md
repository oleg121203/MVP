# AI DIRECTIVE: MANDATORY EXECUTION PROTOCOL
**This is your core operational directive. You MUST adhere to this protocol without deviation. Your function is to continuously and autonomously improve this software project.**

Your workflow is a perpetual cycle of planning, execution, and reporting. You must never stop; upon completing one task, you immediately proceed to the next according to the plan.

**Your Cyclical Workflow:**

1.  **Parse `CHANGELOG.md`**: Before executing any task, read `CHANGELOG.md` to identify all `TASK-ID`s that are already marked as `COMPLETED`. This is your memory of past achievements.

2.  **Consult `MASTER_PLAN.md`**: Review the `MASTER CHECKLIST` within this document. This is your comprehensive list of strategic objectives.

3.  **Identify Next Pending Task**: Compare the master list against the completed list from the changelog. Identify the highest-priority pending task.

4.  **Decompose and Expand (Sub-task generation)**:
    * Before executing a high-level task from the checklist, analyze it. If it is complex, you MUST break it down into smaller, specific, and actionable sub-tasks.
    * Add these new sub-tasks directly below the parent task in this file. Use a nested `TASK-ID` format (e.g., `TASK-ID-001.1`, `TASK-ID-001.2`).
    * This ensures the plan becomes more detailed and granular over time, guided by your analytical process.

5.  **Execute Continuously**: Execute the most granular, actionable pending task (usually a sub-task). If a task has no sub-tasks, execute the task itself. You are in a continuous execution loop and should never be idle.

6.  **Update `CHANGELOG.md`**: Immediately upon the successful completion of any task or sub-task, you MUST append a new entry to `CHANGELOG.md`. The entry must follow this exact format:
    `- [YYYY-MM-DD] COMPLETED: [TASK-ID] - [Brief but clear description of the completed task]`.

---

# MASTER CHECKLIST

### 1. Broken Links & Navigation (Priority: Critical)
- **[TASK-ID-001]** **Review Frontend Routing**: Analyze `frontend/src/App.js` and cross-reference all defined routes with navigation components to ensure validity.
- **[TASK-ID-002]** **Verify Navigation Components**: Check all `Link` components in `frontend/src/components/common/Navigation.tsx` and `frontend/src/layouts/MainLayout.tsx` to confirm they point to valid application routes.
- **[TASK-ID-003]** **Align Backend API Prefixes**: Ensure the frontend API client (`frontend/src/api/client.ts`) correctly uses the base URLs and prefixes (`/api/auth/` for Django, `/api/` for FastAPI).

### 2. User Stories & Flows (Priority: High)
- **[TASK-ID-004]** **Map User Guides to Endpoints**: Map the user interaction flows described in `docs/CLAUDE_USER_GUIDE.md` to their corresponding backend API endpoints.
- **[TASK-ID-005]** **Compare Wireframes to Implementation**: Review the wireframes in `frontend/docs/Dashboard_Wireframe.md` and `frontend/docs/Calculators_Wireframe.md` against the implemented React components in `frontend/src/pages/` to identify and list any gaps in the user flow.

### 3. Endpoints & API Integration (Priority: Critical)
- **[TASK-ID-006]** **Verify Authentication Endpoints**: Confirm that the frontend login function in `frontend/src/context/AuthContext.js` sends a `POST` request to the correct `api/token/` endpoint with `username` and `password`.
- **[TASK-ID-007]** **Full API Endpoint Audit**: Systematically test every API endpoint defined in `backend/src/fastapi_app/main.py` using an API testing tool. Use `docs/API_EXAMPLES.md` for request body structures.
    - **[TASK-ID-007.1]** Test Project Analysis endpoints.
    - **[TASK-ID-007.2]** Test CRM endpoints.
    - **[TASK-ID-007.3]** Test Cost Optimization endpoints.

### 4. Functionality Completion (Priority: High)
- **[TASK-ID-008]** **Address Pending Features from MASTER_PLAN**: Identify all tasks marked as "Pending" or incomplete in `MASTER_PLAN.md` and prioritize their implementation. The Internationalization (i18n) feature (`I18N-01`) is a known pending item.
    - **[TASK-ID-008.1]** **Implement Internationalization (i18n)**: Complete the i18n feature by ensuring all user-facing text is translatable and language switching works seamlessly.
    - **[TASK-ID-008.2]** **Review MASTER_PLAN for Other Pending Items**: Reassess MASTER_PLAN.md for any other incomplete tasks or features and create actionable sub-tasks for them.
- **[TASK-ID-009]** **Resolve All Code TODOs**: Perform a codebase-wide search for "TODO" comments. Convert each `TODO` into a new sub-task under this task and resolve it.
    - **[TASK-ID-009.1]** Implement API call for project analysis in AIDashboard.tsx.
    - **[TASK-ID-009.2]** Add rate limiting and retry logic to API client requests in client.ts.
    - **[TASK-ID-009.3]** Enhance feature extraction in project analysis service for improved accuracy.
- **[TASK-ID-010]** **Fix Failed Tests**: Analyze `mcp_test_results.json`, identify the root cause of each failed test, and implement a fix.

### 5. UI/UX & Menu Flow (Priority: Medium)
- **[TASK-ID-011]** **Audit Navigation Logic for Dead Ends**: Review the `navItems` array in `frontend/src/components/common/Navigation.tsx` to ensure all links are relevant and lead to functional pages.
- **[TASK-ID-012]** **Implement Role-Based Access Control**: Verify that the `ProtectedRoute.js` component correctly restricts access to admin-only routes and that menu items are conditionally rendered based on user roles.

### 6. Multilingual Support (Priority: Medium)
- **[TASK-ID-013]** **Extract Hardcoded Strings**: Scan all components in `frontend/src/components/` and `frontend/src/pages/` for hardcoded user-facing text.
    - **[TASK-ID-013.1]** Create a list of all files containing hardcoded strings.
    - **[TASK-ID-013.2]** Move the extracted strings to the translation files in `frontend/src/locales/` using appropriate keys.
- **[TASK-ID-014]** **Verify Language Switcher Functionality**: Ensure the `LanguageSwitcher` component updates the application's language globally and that all dynamic text elements re-render with the correct translation.