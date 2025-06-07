# VentAI Calculators Visual Mockup Plan

**Task Reference**: UI-01 - UI/UX Redesign

**Date**: 2025-06-07

This document outlines the plan for creating a visual mockup of the VentAI Calculators section based on the textual wireframe documented in `Calculators_Wireframe.md`. The mockup will translate the conceptual layout into a visual format suitable for stakeholder review and frontend implementation.

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

#### Main Content Area - Title & Subtitle
- **Dimensions**: Full-width, height approximately 100px on desktop.
- **Elements**:
  - Page Title (e.g., 36px font size, bold): "HVAC Calculators".
  - Subtitle (e.g., 18px): "Select a tool below to perform precise calculations for your projects.".
- **Styling**: Centered or left-aligned text, light background (e.g., #F7FAFC) for subtle differentiation.

#### Search & Filter Bar
- **Dimensions**: Full-width, height approx. 60px.
- **Elements**:
  - Search Input on the left (e.g., 300px wide on desktop): "Search calculators..." with a magnifying glass icon.
  - Filter Dropdowns on the right: 
    - Category (options: Ventilation, Heating, Acoustics, etc.).
    - Complexity (options: Basic, Advanced).
- **Styling**: White background with subtle border, teal accents on icons or active filters, responsive stacking on mobile.

#### Calculator Categories & Listings - Tabbed Layout
- **Dimensions**: Full-width container with max-width (e.g., 1200px), tabbed layout with content area below.
- **Elements**:
  - Tab Navigation (horizontal on desktop, stack or scroll on mobile):
    - Tab 1: "Ventilation Calculators" (active by default).
    - Tab 2: "Heating Calculators".
    - Tab 3: "Acoustics Calculators".
    - Additional tabs as needed.
  - Content Area for Active Tab (grid layout, 2-3 columns on desktop, single column on mobile):
    - For "Ventilation Calculators":
      - Card 1: Air Exchange Calculator
        - Title (e.g., 20px, bold): "Air Exchange Calculator".
        - Description (e.g., 16px): "Calculate required air exchange rates for spaces.".
        - CTA Button: "Start Calculation" (teal background).
        - Tag: "Basic" (small badge, green or gray).
      - Card 2: Duct Sizing Calculator
        - Title: "Duct Sizing Calculator".
        - Description: "Determine optimal duct dimensions for airflow.".
        - CTA Button: "Start Calculation".
        - Tag: "Advanced" (orange badge).
      - Card 3: Duct Area Calculator
        - Title: "Duct Area Calculator".
        - Description: "Compute cross-sectional area for duct systems.".
        - CTA Button: "Start Calculation".
        - Tag: "Basic".
      - Card 4: Pressure Drop Calculator
        - Title: "Pressure Drop Calculator".
        - Description: "Estimate pressure loss in ductwork.".
        - CTA Button: "Start Calculation".
        - Tag: "Advanced".
      - Card 5: Smoke Removal Calculator
        - Title: "Smoke Removal Calculator".
        - Description: "Design smoke extraction systems for safety compliance.".
        - CTA Button: "Start Calculation".
        - Tag: "Advanced".
    - Similar card layouts for other tabs (Heating, Acoustics, etc.).
- **Styling**: Tabs with teal underline or background for active state, cards with white background, subtle shadow, hover lift effect on cards, consistent spacing.

#### Saved Calculations - Collapsible Panel
- **Dimensions**: Full-width, collapsible with toggle (default collapsed on mobile, expanded on desktop), height variable based on content.
- **Elements**:
  - Title (e.g., 20px, bold): "Your Saved Calculations".
  - Toggle Icon/Button: Expand/Collapse.
  - Content (grid or list): Show 3-5 recent saved results with columns for Name, Date, Calculator Type, and a quick view button.
  - CTA Button: "View All Saved" or "Link to Project".
- **Styling**: Light gray background when collapsed, white when expanded, subtle border, teal CTAs.

#### Help & Tutorials - Footer Bar
- **Dimensions**: Full-width, height approx. 80px.
- **Elements**:
  - Title (e.g., 20px, bold, centered): "Need Help with Calculations?".
  - CTA Buttons (horizontal on desktop, stack on mobile):
    - "Watch Tutorial Videos" (teal outlined).
    - "Read Guides" (teal outlined).
    - "Contact Support" (teal outlined).
- **Styling**: Light background (e.g., #F7FAFC), centered content for emphasis.

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
- **Tags**: Green (#48BB78) for Basic, Orange (#ED8936) for Advanced.

## Typography (Proposed)
- **Headlines**: Roboto or Inter (Bold, various sizes for hierarchy).
- **Body Text**: Roboto or Inter (Regular, 16px base size for readability).

## Next Steps After Mockup Creation
1. **Review**: Share mockup with stakeholders for feedback on layout, content, and visual style.
2. **Iteration**: Refine design based on feedback, adjusting colors, spacing, or content as needed.
3. **Prototyping**: Create interactive prototype in Figma to simulate user flow (e.g., selecting a calculator, viewing saved results).
4. **Handoff**: Export design assets (icons, images) and provide CSS specifications for developers.
5. **Implementation Plan**: Update `CalculatorsPage.tsx` and related components in the codebase to reflect the new design, leveraging Chakra UI components.

This plan ensures the visual mockup aligns with the textual wireframe’s intent while providing actionable details for a designer to execute the vision for VentAI’s Calculators section.
