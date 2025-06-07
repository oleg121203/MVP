# VentAI Calculators Wireframe

**Task Reference**: UI-01 - UI/UX Redesign

**Date**: 2025-06-07

Below is a textual representation of the proposed wireframe for the VentAI Calculators section. This design aims to centralize all HVAC calculation tools into an intuitive hub, improving navigation and usability for professionals.

## Wireframe Layout (Textual Representation)

```
[Header Section - MainLayout Component]
  [Logo]          [Navigation Menu: Home | Calculators | Dashboard | Login/Signup]
  [Language Switcher] [Theme Toggle]

[Main Content Area - Full Width, Flexible Height]
  [Page Title: "HVAC Calculators" (Large, Bold Text)]
  [Subtitle: "Select a tool below to perform precise calculations for your projects."]
  
  [Section 1: Search & Filter Bar - Full Width]
    [Search Input: "Search calculators..." (with magnifying glass icon)]
    [Filter Dropdowns: Category (e.g., Ventilation, Heating, Acoustics) | Complexity (e.g., Basic, Advanced)]

  [Section 2: Calculator Categories & Listings - Tabbed or Accordion Layout]
    [Tab/Accordion 1: Ventilation Calculators]
      [Card 1: Air Exchange Calculator]
        [Title: "Air Exchange Calculator"]
        [Description: "Calculate required air exchange rates for spaces."]
        [CTA Button: "Start Calculation"]
        [Tag: "Basic"]
      [Card 2: Duct Sizing Calculator]
        [Title: "Duct Sizing Calculator"]
        [Description: "Determine optimal duct dimensions for airflow."]
        [CTA Button: "Start Calculation"]
        [Tag: "Advanced"]
      [Card 3: Duct Area Calculator]
        [Title: "Duct Area Calculator"]
        [Description: "Compute cross-sectional area for duct systems."]
        [CTA Button: "Start Calculation"]
        [Tag: "Basic"]
      [Card 4: Pressure Drop Calculator]
        [Title: "Pressure Drop Calculator"]
        [Description: "Estimate pressure loss in ductwork."]
        [CTA Button: "Start Calculation"]
        [Tag: "Advanced"]
      [Card 5: Smoke Removal Calculator]
        [Title: "Smoke Removal Calculator"]
        [Description: "Design smoke extraction systems for safety compliance."]
        [CTA Button: "Start Calculation"]
        [Tag: "Advanced"]
    [Tab/Accordion 2: Heating Calculators]
      [Card 1: Water Heater Calculator]
        [Title: "Water Heater Calculator"]
        [Description: "Calculate heating requirements for water systems."]
        [CTA Button: "Start Calculation"]
        [Tag: "Basic"]
    [Tab/Accordion 3: Acoustics Calculators]
      [Card 1: Acoustic Calculator]
        [Title: "Acoustic Calculator"]
        [Description: "Assess noise levels and mitigation for HVAC systems."]
        [CTA Button: "Start Calculation"]
        [Tag: "Advanced"]
    [More Tabs/Accordions as needed for additional categories]

  [Section 3: Saved Calculations - Collapsible Panel]
    [Title: "Your Saved Calculations"]
    [List or Grid: Display recent saved results with Name, Date, Calculator Type]
    [CTA: "View All Saved" or "Link to Project"]

  [Section 4: Help & Tutorials - Footer Bar]
    [Title: "Need Help with Calculations?"]
    [CTA Buttons: "Watch Tutorial Videos" | "Read Guides" | "Contact Support"]

[Footer Section - MainLayout Component]
  [Links: About Us | Contact | Privacy Policy | Terms of Service]
  [Social Media Icons]
  [Copyright Notice]
```

## Explanation of Wireframe Elements

1. **Header Section**: Consistent with `MainLayout`, providing navigation and personalization options.
2. **Search & Filter Bar**: Enables quick discovery of relevant calculators by name or category, addressing the issue of fragmented tools.
3. **Calculator Categories & Listings**: Organizes calculators into logical groups using a tabbed or accordion layout to reduce clutter and improve navigation. Each card provides a brief description and complexity tag to set user expectations.
4. **Saved Calculations**: Allows users to revisit past work, enhancing productivity by linking results to projects or reusing inputs.
5. **Help & Tutorials**: Offers resources for users unfamiliar with certain tools, improving onboarding and usability.
6. **Footer Section**: Standard branding and links for additional resources.

This wireframe serves as a conceptual foundation for the Calculators section redesign. It can be translated into visual mockups using design tools like Figma for further refinement and stakeholder feedback.

**Next Steps**:
- Review and iterate on this wireframe based on team feedback.
- Create visual mockups to finalize the design.
- Plan implementation in the frontend codebase, updating `CalculatorsPage.tsx` and related components.
- Proceed to audit the next logical section under UI-01 as per MASTER_PLAN.md.
