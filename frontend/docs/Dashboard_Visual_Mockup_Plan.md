# VentAI Dashboard Visual Mockup Plan

**Task Reference**: UI-01 - UI/UX Redesign

**Date**: 2025-06-07

This document outlines the plan for creating a visual mockup of the VentAI Dashboard based on the textual wireframe documented in `Dashboard_Wireframe.md`. The mockup will translate the conceptual layout into a visual format suitable for stakeholder review and frontend implementation.

## Design Tool Recommendation
- **Tool**: Figma (preferred for collaboration and prototyping) or Sketch/Adobe XD as alternatives.
- **Purpose**: Create high-fidelity mockups with precise layouts, color schemes, typography, and interactive elements for user testing.

## Visual Mockup Guidelines

### General Design Principles
- **Brand Identity**: Use a modern, professional color palette (e.g., teal, gray, white) to reflect VentAI’s focus on technology and engineering precision. Ensure the logo and branding are prominent.
- **Consistency**: Align with Chakra UI’s design system for component styling to ensure seamless transition to code.
- **Responsiveness**: Design for desktop (primary), tablet, and mobile breakpoints to ensure usability across devices.
- **Accessibility**: Follow WCAG 2.1 AA standards, ensuring sufficient color contrast and readable typography.

### Layout Specifications (Based on Wireframe)

#### Header Section
- **Dimensions**: Fixed height (e.g., 70px) with full-width layout.
- **Elements**:
  - Logo on the left (scalable, max height 50px).
  - Navigation menu in the center or right with links to Home, Calculators, Dashboard, and Login/Signup (hover effects, active states).
  - Language Switcher and Theme Toggle icons on the far right (subtle, with tooltips).
- **Styling**: Background color (e.g., white or light gray), subtle bottom shadow for elevation.

#### Main Content Area - Welcome & Quick Stats
- **Dimensions**: Full-width banner, height approximately 120px on desktop.
- **Elements**:
  - Welcome Message (e.g., 24px font size, bold) on the left: "Welcome, [User Name]! Here's your overview.".
  - Quick Stats Grid (4 mini cards on desktop, stack on mobile):
    - Card 1: Active Projects (icon + text, e.g., "5 Active").
    - Card 2: Completed Calculations (icon + text, e.g., "12 This Month").
    - Card 3: AI Alerts (icon + text, e.g., "2 New Suggestions").
    - Card 4: Team Updates (icon + text, e.g., "1 New Message", optional).
- **Styling**: Light background (e.g., #F7FAFC), cards with subtle shadows, teal accents for icons or key numbers.

#### Main Dashboard Grid - 2-Column Layout
- **Dimensions**: Full-width container with max-width (e.g., 1200px), split 70% (left) / 30% (right) on desktop, stack on mobile.
- **Left Column Elements**:
  - Widget 1: Project Overview (height approx. 300px, scrollable if needed)
    - Title (e.g., 20px, bold): "Your Projects".
    - List or Grid: Show 3-5 recent projects with name, status badge (color-coded), last updated date, and a quick link (e.g., chevron icon).
    - CTA Button (bottom or top-right): "View All Projects" or "Add New Project" (teal background).
    - Styling: White card background, subtle shadow, hover effect on list items.
  - Widget 2: Recent Calculations (height approx. 250px)
    - Title (e.g., 20px, bold): "Recent Calculations".
    - Compact Table or Cards: Show 3-4 entries with calculation type, date, result snippet, and a revisit button.
    - CTA Button: "View All Calculations".
    - Styling: Similar card design, clean table layout with alternating row colors if applicable.
- **Right Column Elements**:
  - Widget 3: AI Insights & Alerts (height approx. 300px)
    - Title (e.g., 20px, bold): "AI Insights".
    - Vertical Stack: Show 2-3 alerts with brief description, severity indicator (color dot or icon), and action button (e.g., "Review").
    - CTA Button: "See All Insights".
    - Styling: White card, color-coded severity indicators (red for critical, yellow for warning).
  - Widget 4: Quick Access Toolbar (height approx. 200px)
    - Title (e.g., 20px, bold): "Quick Tools".
    - Icon Grid: 4-6 icons linking to key calculators (e.g., Air Exchange, Duct Sizing), each with a small label.
    - CTA Button: "Go to Calculators".
    - Styling: Minimalist card, icons in teal with hover effects.

#### Customization Option - Footer Bar
- **Dimensions**: Full-width, thin bar (e.g., 50px height).
- **Elements**:
  - Button (centered or right-aligned): "Customize Dashboard" (outlined teal button, opens modal for widget management).
- **Styling**: Light gray background to differentiate from main content.

#### Footer Section
- **Dimensions**: Full-width, fixed height (e.g., 200px).
- **Elements**:
  - Links in grid or list format: About Us, Contact, Privacy Policy, Terms of Service.
  - Social Media Icons below links (small, grayscale with hover color).
  - Copyright Notice at bottom (small text).
- **Styling**: Darker background (e.g., dark gray), white text for contrast.

## Color Palette (Proposed)
- **Primary**: Teal (#008080) for CTAs and accents.
- **Secondary**: Gray (#4A5568) for text and subtle elements.
- **Background**: White (#FFFFFF) for main content, Light Gray (#F7FAFC) for differentiation.
- **Text**: Dark Gray (#2D3748) for readability.
- **Alerts**: Red (#E53E3E) for critical, Yellow (#ECC94B) for warnings.

## Typography (Proposed)
- **Headlines**: Roboto or Inter (Bold, various sizes for hierarchy).
- **Body Text**: Roboto or Inter (Regular, 16px base size for readability).

## Next Steps After Mockup Creation
1. **Review**: Share mockup with stakeholders for feedback on layout, content, and visual style.
2. **Iteration**: Refine design based on feedback, adjusting colors, spacing, or content as needed.
3. **Prototyping**: Create interactive prototype in Figma to simulate user flow (e.g., clicking widgets to view details).
4. **Handoff**: Export design assets (icons, images) and provide CSS specifications for developers.
5. **Implementation Plan**: Update `DashboardPage.tsx` in the codebase to reflect the new design, leveraging Chakra UI components and data visualization libraries like recharts.

This plan ensures the visual mockup aligns with the textual wireframe’s intent while providing actionable details for a designer to execute the vision for VentAI’s Dashboard.
