# VentAI Dashboard Wireframe

**Task Reference**: UI-01 - UI/UX Redesign

**Date**: 2025-06-07

Below is a textual representation of the proposed wireframe for the VentAI Dashboard. This design transforms the current placeholder into a functional hub for HVAC professionals, incorporating project overviews, recent calculations, AI insights, and quick access to tools.

## Wireframe Layout (Textual Representation)

```
[Header Section - MainLayout Component]
  [Logo]          [Navigation Menu: Home | Calculators | Dashboard | Login/Signup]
  [Language Switcher] [Theme Toggle]

[Main Content Area - Full Width, Flexible Height]
  [Page Title: "Dashboard" (Large, Bold Text)]
  
  [Section 1: Welcome & Quick Stats - Full Width Banner]
    [Welcome Message: "Welcome, [User Name]! Here's your overview."]
    [Quick Stats Grid: 3-4 Mini Cards]
      [Card 1: Active Projects (e.g., "5 Active")]
      [Card 2: Completed Calculations (e.g., "12 This Month")]
      [Card 3: AI Alerts (e.g., "2 New Suggestions")]
      [Card 4: (Optional) Team Updates (e.g., "1 New Message")]

  [Section 2: Main Dashboard Grid - 2-Column Layout on Desktop, Stack on Mobile]
    [Left Column - 70% Width]
      [Widget 1: Project Overview (Scrollable List or Grid)]
        [Title: "Your Projects"]
        [List Items: Project Name, Status, Last Updated, Quick Link to Details]
        [CTA: "View All Projects" or "Add New Project"]
      [Widget 2: Recent Calculations (Compact Table or Cards)]
        [Title: "Recent Calculations"]
        [Items: Calculation Type, Date, Result Summary, Revisit Button]
        [CTA: "View All Calculations"]
    [Right Column - 30% Width]
      [Widget 3: AI Insights & Alerts (Vertical Stack)]
        [Title: "AI Insights"]
        [Alerts: Brief Description, Severity Indicator, Action Button (e.g., Review)]
        [CTA: "See All Insights"]
      [Widget 4: Quick Access Toolbar (Icon Grid)]
        [Title: "Quick Tools"]
        [Icons: Links to Key Calculators (e.g., Air Exchange, Duct Sizing)]
        [CTA: "Go to Calculators"]

  [Section 3: Customization Option - Footer Bar]
    [Button: "Customize Dashboard" (Opens modal to reorder/add/remove widgets)]

[Footer Section - MainLayout Component]
  [Links: About Us | Contact | Privacy Policy | Terms of Service]
  [Social Media Icons]
  [Copyright Notice]
```

## Explanation of Wireframe Elements

1. **Header Section**: Consistent with `MainLayout`, providing navigation and personalization options.
2. **Welcome & Quick Stats**: A personalized greeting with high-level metrics to give users an immediate sense of their activity and pending actions.
3. **Main Dashboard Grid**: Divided into a primary area for project and calculation data (left) and a secondary area for insights and quick tools (right), balancing information density with accessibility. Responsive design stacks these on mobile for usability.
4. **Customization Option**: Empowers users to tailor the dashboard to their workflow, enhancing user satisfaction.
5. **Footer Section**: Standard branding and links for additional resources.

This wireframe serves as a conceptual foundation for the Dashboard redesign. It can be translated into visual mockups using design tools like Figma for further refinement and stakeholder feedback.

**Next Steps**:
- Review and iterate on this wireframe based on team feedback.
- Create visual mockups to finalize the design.
- Plan implementation in the frontend codebase, updating `DashboardPage.tsx`.
- Proceed to audit the 'Calculators' section as the next sub-task under UI-01.
