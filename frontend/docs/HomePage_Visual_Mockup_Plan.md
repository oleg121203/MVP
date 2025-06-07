# VentAI Homepage Visual Mockup Plan

**Task Reference**: UI-01 - UI/UX Redesign

**Date**: 2025-06-07

This document outlines the plan for creating a visual mockup of the VentAI homepage based on the textual wireframe documented in `HomePage_Wireframe.md`. The mockup will be designed to translate the conceptual layout into a visual format suitable for stakeholder review and frontend implementation.

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

#### Hero Section
- **Dimensions**: Full-width, height approximately 500px on desktop.
- **Elements**:
  - Large Headline (e.g., 48px font size, bold) centered: "Revolutionize Your HVAC Engineering with VentAI".
  - Subheadline (e.g., 24px) below headline: "AI-powered tools, project management, and automation for professionals.".
  - Primary CTA Button (prominent, teal background, white text): "Get Started Now".
  - Secondary CTA Button (outlined, teal border): "Watch Demo Video".
  - Background Image/Illustration: HVAC blueprint with AI/tech overlay (semi-transparent to avoid text obstruction).
- **Styling**: Gradient or solid background if image is not used, centered text with padding for readability.

#### Capabilities Overview
- **Dimensions**: Full-width container with max-width (e.g., 1200px), 3-column grid on desktop, stack on mobile.
- **Elements (per Card)**:
  - Icon (e.g., 40x40px) at top for visual cue (Brain/AI, Calculator, Folder/Project).
  - Title (e.g., 20px, bold): "Smart Design Analysis", "Precision Tools", "Streamlined Workflow".
  - Description (e.g., 16px): Brief text explaining the feature.
- **Styling**: Card background (white), subtle shadow, equal spacing, hover effect (slight lift or color change).

#### Guided Onboarding Section
- **Dimensions**: Centered, single-column, max-width (e.g., 800px), height approx. 300px.
- **Elements**:
  - Headline (e.g., 28px, bold): "New to VentAI? Take a Quick Tour".
  - Description (e.g., 18px): "Learn how to maximize your productivity with our platform in just 2 minutes.".
  - CTA Button (teal, centered): "Start Tour".
  - Small Video Thumbnail or GIF (e.g., 200x150px) below CTA for visual preview.
- **Styling**: Light background color to differentiate from other sections, padding for breathing room.

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

## Typography (Proposed)
- **Headlines**: Roboto or Inter (Bold, various sizes for hierarchy).
- **Body Text**: Roboto or Inter (Regular, 16px base size for readability).

## Next Steps After Mockup Creation
1. **Review**: Share mockup with stakeholders for feedback on layout, content, and visual style.
2. **Iteration**: Refine design based on feedback, adjusting colors, spacing, or content as needed.
3. **Prototyping**: Create interactive prototype in Figma to simulate user flow (e.g., clicking CTAs to navigate).
4. **Handoff**: Export design assets (icons, images) and provide CSS specifications for developers.
5. **Implementation Plan**: Update `HomePage.tsx` in the codebase to reflect the new design, leveraging Chakra UI components.

This plan ensures the visual mockup aligns with the textual wireframe’s intent while providing actionable details for a designer to execute the vision for VentAI’s homepage.
