# Project Management Wireframe for VentAI UI/UX Redesign (UI-01)

## Overview
This wireframe outlines the structure and functionality of the Project Management section for VentAI, focusing on a user-centric design that enhances project tracking, collaboration, and efficiency in ventilation system design.

## Page Structure
- **Title**: 'Project Management' (translated via i18next)
- **Layout**: Utilizes `MainLayout` for consistent header, navigation, and footer across the app.
- **Main Content Area**: Divided into three primary sections for better organization and accessibility.

### Header Section
- **Welcome Text**: A brief heading and subtitle welcoming users to the project management hub.
  - Heading: 'Project Management Hub'
  - Subtitle: 'Manage all your ventilation projects in one place.'
- **Action Button**: 'Create New Project' button to initiate a new project workflow.

### Sidebar (Left Panel - Responsive)
- **Project List**: A scrollable list of user's projects.
  - Each project card shows:
    - Project Name
    - Last Updated Date
    - Status Indicator (e.g., In Progress, Completed)
  - Quick action links: 'View Details', 'Edit'
  - Responsive behavior: Collapses into a hamburger menu or accordion on mobile devices.
- **Filters**: Options to filter projects by status, date, or category.

### Main Content Area (Right Panel)
- **Active Project Overview**: Default view shows the selected project's dashboard if one is active.
  - **Project Title & Metadata**: Name, creation date, last update, and status.
  - **Key Metrics**: Visual cards or widgets showing project stats like number of calculations, design completion percentage, and team members involved.
  - **Recent Activity**: A timeline or list of recent updates (e.g., 'Duct Calculation added by User X - 2 hours ago').
  - **Quick Links**: Direct access to 'Calculations', 'Designs', 'Documents', and 'Settings' related to the project.
- **If No Project Selected**: Display a prompt to select a project from the sidebar or create a new one.

### Collaboration & Sharing Section
- **Team Members**: Avatars or list of collaborators with roles (e.g., Engineer, Manager).
  - Option to invite new members via email link or modal.
- **Sharing Options**: Buttons to export project data (PDF, CSV) or share a public link for stakeholders.
- **Comments/Notes**: A section for project-specific discussions or annotations visible to the team.

## Responsive Design Considerations
- **Mobile View**: Sidebar collapses, main content takes full width, key actions (like 'Create Project') are moved to a floating action button or top bar.
- **Tablet View**: Sidebar remains visible but narrower, main content adjusts accordingly.
- **Desktop View**: Full sidebar and detailed main content layout for maximum visibility.

## Accessibility Features
- ARIA labels for interactive elements (e.g., project list items, buttons).
- Keyboard navigation support for sidebar and main content actions.
- High contrast mode compatibility for text and icons.

## Key Interactions
- **Selecting a Project**: Clicking a project in the sidebar updates the main content to show that project's details without page reload (SPA behavior using React Router).
- **Creating a Project**: Modal or new page with a form for project details (name, description, category, team selection).
- **Editing Project Details**: Inline editing or modal for quick updates to project metadata.
- **Export/Share**: Triggers a download or copy-to-clipboard action with a confirmation toast.

## Visual Elements
- **Icons**: Use `react-icons` for project status, actions (e.g., FaFolder for projects, FaPlus for new project).
- **Color Scheme**: Follow VentAI design system with teal as primary color for buttons and links, ensuring visual hierarchy.
- **Cards**: Use `Card` component for project list items and key metrics for consistency.

## Dependencies
- **Chakra UI**: For layout (Flex, Box, SimpleGrid), components (Button, Card, Input), and responsive design utilities.
- **react-icons**: For iconography.
- **react-i18next**: For translations.
- **react-router-dom**: For navigation and single-page app behavior.

## Next Steps Post-Wireframe Approval
1. Develop visual mockups based on this structure.
2. Implement the `ProjectManagementPage.tsx` with placeholder data.
3. Integrate with backend APIs for dynamic project data retrieval and updates.
4. Test responsiveness and accessibility compliance (WCAG 2.1 AA).

This wireframe serves as the blueprint for the Project Management section redesign, aligning with VentAI's goal of a modern, intuitive, and responsive user interface.
