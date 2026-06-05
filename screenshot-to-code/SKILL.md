---
name: screenshot-to-code
description: Convert UI screenshots into working HTML/CSS/React/Vue code. Detects design patterns, components, and generates responsive layouts. Use this when users provide screenshots of websites, apps, or UI designs and want code implementation.
---

# Screenshot to Code

Convert UI screenshots into production-ready code with accurate styling and structure.

## How This Works

Given a screenshot of a UI design:
1. Analyze the visual design thoroughly
2. Generate clean, modern code that recreates it
3. Provide complete, runnable implementation

## Instructions

### 1. Analyze the Screenshot

Examine the image carefully and identify:
- **Layout structure**: Grid, flexbox, or custom positioning
- **Components**: Buttons, inputs, cards, navigation, modals, etc.
- **Visual details**: Colors, fonts, spacing, borders, shadows, borders-radius
- **Responsive considerations**: Mobile vs. desktop layout cues

### 2. Determine the Framework

Ask which framework is preferred:
- React (with Tailwind CSS or styled-components)
- Vue.js
- Plain HTML/CSS
- Next.js

**Default**: If not specified, use **React with Tailwind CSS** for modern designs, or **plain HTML/CSS** for simple pages.

### 3. Generate Complete Code

Create the implementation:

**For React/Vue:**
- Build component hierarchy (break into logical components)
- Use semantic HTML elements
- Implement modern CSS (flexbox, grid, custom properties)
- Include prop types and sensible defaults

**For HTML/CSS:**
- Use semantic HTML5 structure
- Write clean, organized CSS (consider using BEM naming)
- Make it responsive by default

**Critical requirements:**
- Match colors EXACTLY (extract hex codes from screenshot)
- Match spacing and proportions as closely as possible
- Use appropriate semantic elements (header, nav, main, section, etc.)
- Include accessibility attributes (alt text, ARIA labels where needed)

### 4. Make It Responsive

- Use responsive units (rem, em, %, vw/vh) rather than fixed pixels
- Add breakpoints for mobile, tablet, desktop if the design suggests it
- Use `min()`, `max()`, `clamp()` for fluid typography where appropriate

### 5. Deliver Complete Implementation

Provide:
1. **Complete code** (all files needed, fully functional)
2. **File structure** (explain what each file does)
3. **Usage instructions** (how to run/use the code)
4. **Notes on design decisions** (any assumptions or interpretations)

## Output Format

Structure React + Tailwind output like this:

```jsx
import React from 'react';

export default function ComponentName() {
  return (
    <div className="...">
      {/* Component structure */}
    </div>
  );
}
```

Always include:
- All necessary imports
- Any required dependencies
- Clear comments for complex sections
- Suggestions for improvements or next steps

## Best Practices

- **Accuracy**: Match the design as closely as possible
- **Modern CSS**: Prefer Grid/Flexbox over floats or tables
- **Accessibility**: Include ARIA labels, alt text, semantic HTML
- **Performance**: Optimize images, use efficient selectors
- **Maintainability**: Write clean, well-organized code with comments
- **Responsiveness**: Design mobile-first when possible

## Common Patterns

**Navigation Bars**: Flexbox with space-between, sticky positioning
**Card Grids**: CSS Grid with auto-fit/auto-fill for responsiveness
**Hero Sections**: Full-height with centered content, background images
**Forms**: Proper labels, validation states, accessible inputs
**Modals**: Fixed positioning, backdrop, focus management

## Handling Unclear Screenshots

When the screenshot is unclear or ambiguous:
- Make reasonable assumptions based on common UI patterns
- Note the chosen interpretation in comments
- Suggest alternatives that might be preferred
- Ask for clarification on critical decisions

## Example Workflow

**Input**: Screenshot of a landing page with hero section, feature cards, and footer

**Response**:
1. Analyze: Hero with large headline, 3-column feature grid, simple footer
2. Ask: "Would you like this in React with Tailwind or plain HTML/CSS?"
3. Generate: Complete implementation with responsive design
4. Deliver: All code files with clear structure and usage instructions

---

Aim to produce code so clean and accurate that it could be deployed immediately with minimal modifications.
