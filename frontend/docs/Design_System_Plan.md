# VentAI Design System Plan

**Task Reference**: UI-01 - UI/UX Redesign

**Date**: 2025-06-07

This document outlines the plan for developing a consistent design system for VentAI. A design system ensures a unified visual and functional experience across the application by defining standardized colors, typography, components, and design principles. This will facilitate easier development, maintenance, and scalability of the UI.

## Objectives of the Design System
- **Consistency**: Ensure all parts of the application have a cohesive look and feel.
- **Efficiency**: Speed up design and development processes by reusing predefined elements.
- **Scalability**: Allow for easy addition of new features without redesigning core elements.
- **Accessibility**: Incorporate best practices to make the application usable by everyone.
- **Brand Identity**: Reflect VentAI’s focus on technology and engineering precision through visual design.

## Design System Components

### 1. Color Palette
- **Primary Color**: Teal (#008080) - Used for primary actions, accents, and key UI elements like buttons and links.
- **Secondary Color**: Gray (#4A5568) - For secondary text, borders, and less prominent elements.
- **Background Colors**:
  - White (#FFFFFF) - Main background for content areas.
  - Light Gray (#F7FAFC) - Subtle differentiation for sections or cards.
- **Text Colors**:
  - Dark Gray (#2D3748) - Primary text for readability.
  - Medium Gray (#718096) - Secondary text or captions.
- **Feedback Colors**:
  - Success Green (#48BB78) - For success messages or indicators.
  - Warning Yellow (#ECC94B) - For warnings or cautionary elements.
  - Error Red (#E53E3E) - For errors or critical alerts.
- **Tags/Labels**:
  - Basic Tag: Green (#48BB78).
  - Advanced Tag: Orange (#ED8936).
- **Usage Guidelines**: Ensure sufficient contrast ratios for accessibility (e.g., text on backgrounds should meet WCAG 2.1 AA standards). Use primary teal sparingly for emphasis, relying on neutral tones for most UI elements.

### 2. Typography
- **Font Family**: Roboto or Inter (both are clean, modern sans-serif fonts suitable for tech applications).
- **Hierarchy**:
  - Headlines (H1-H3): Bold, sizes ranging from 36px (H1) to 20px (H3).
  - Subheadings: Medium or Regular, sizes 18px to 16px.
  - Body Text: Regular, 16px base size for readability.
  - Captions/Labels: Regular, 14px or 12px for secondary information.
  - Button Text: Medium or Bold, 14px to 16px for clarity.
- **Line Height**: 1.5 for body text, 1.2-1.3 for headings to ensure readability.
- **Usage Guidelines**: Limit font weights to Regular, Medium, and Bold to maintain simplicity. Ensure text is legible on all device sizes, with responsive adjustments if needed.

### 3. Spacing and Layout
- **Grid System**: Use an 8px base grid for spacing and layout (e.g., margins, padding, component sizes should be multiples of 8px).
- **Container Widths**: Max-width of 1200px for desktop content, with responsive breakpoints at 1024px (tablet), 768px (mobile landscape), and 480px (mobile portrait).
- **Padding**: 
  - Cards/Containers: 16px to 24px internal padding.
  - Sections: 32px to 48px spacing between major sections.
- **Margins**: 
  - Between elements in a list or grid: 8px to 16px.
  - Between widgets or major UI blocks: 24px to 32px.
- **Usage Guidelines**: Maintain consistent spacing to create visual rhythm. Ensure layouts stack logically on mobile devices, prioritizing content hierarchy.

### 4. UI Components (Leveraging Chakra UI)
- **Buttons**:
  - Primary Button: Teal background (#008080), white text, rounded corners (4px), hover state (darken teal), sizes (small: 12px text, medium: 14px text, large: 16px text).
  - Secondary Button: Outlined teal border, teal text, white background, hover state (light teal fill).
  - Disabled State: Grayed out (opacity 50%), no interaction.
- **Cards**:
  - Background: White (#FFFFFF).
  - Border: Subtle gray (#E2E8F0) or none.
  - Shadow: Subtle drop shadow for elevation (e.g., Chakra’s `boxShadow='md'`).
  - Padding: 16px or 24px.
  - Hover: Slight lift effect (increase shadow) if interactive.
- **Inputs**:
  - Border: Light gray (#E2E8F0), focus state teal outline (#008080).
  - Placeholder Text: Medium gray (#718096).
  - Error State: Red border (#E53E3E) with error message below.
- **Navigation/Tabs**:
  - Active Tab: Teal underline or background, bold text.
  - Inactive Tab: Gray text, hover state shows teal hint.
- **Alerts/Notifications**:
  - Success: Green border or icon (#48BB78).
  - Warning: Yellow border or icon (#ECC94B).
  - Error: Red border or icon (#E53E3E).
  - Info: Teal border or icon (#008080).
- **Icons**:
  - Size: 16px to 24px for most UI elements, larger (40px) for illustrative purposes.
  - Color: Match context (teal for primary, gray for secondary, feedback colors for status).
- **Usage Guidelines**: Use Chakra UI’s built-in components for rapid development, customizing theme variables to match VentAI’s palette. Ensure all interactive elements have clear hover/focus states for accessibility.

### 5. Responsive Design Breakpoints
- **Desktop**: >1024px - Full layouts with multi-column grids.
- **Tablet**: 768px-1024px - Adjusted grids (e.g., 2 columns instead of 3), slightly reduced text sizes.
- **Mobile Landscape**: 480px-768px - Single column layouts, stack navigation elements.
- **Mobile Portrait**: <480px - Compact spacing, larger touch targets (min 44x44px for buttons).
- **Usage Guidelines**: Prioritize content visibility on smaller screens, hiding non-essential elements if needed (e.g., collapse sidebars into menus).

### 6. Accessibility Standards
- **Color Contrast**: Ensure text meets WCAG 2.1 AA contrast ratios (e.g., 4.5:1 for normal text on backgrounds).
- **Keyboard Navigation**: All interactive elements must be focusable and operable via keyboard (e.g., tab order, enter key for actions).
- **ARIA Labels**: Use ARIA attributes for screen readers on complex components (e.g., modals, accordions).
- **Alt Text**: Provide descriptive alt text for all images and icons with functional purpose.
- **Usage Guidelines**: Test with tools like axe-core during development to catch accessibility issues early.

## Integration with Development
- **Chakra UI Theme Customization**: Extend Chakra UI’s theme to include VentAI’s color palette, typography, and component styles. Create a `theme.ts` file in the frontend to centralize these customizations.
- **Design Tokens**: Export colors, spacing, and typography as reusable tokens or CSS variables for consistency across code and design files.
- **Component Library**: Document components in a shared resource (e.g., Storybook) for developers to preview and use.
- **Figma Design Files**: Maintain a master Figma file with all design system elements for designer reference and handoff.

## Next Steps
1. **Review**: Share this design system plan with stakeholders for feedback on colors, typography, and component styles.
2. **Iteration**: Refine elements based on feedback to align with brand and user needs.
3. **Documentation**: Create a comprehensive design system guide in Figma or a dedicated markdown file for team reference.
4. **Implementation**: Begin updating the frontend codebase by customizing Chakra UI themes and building reusable components as outlined.
5. **Testing**: Conduct usability and accessibility testing on implemented components to ensure compliance with standards.

This design system plan provides a foundation for a consistent and user-friendly interface for VentAI, aligning with the broader goals of the UI/UX redesign under UI-01.
