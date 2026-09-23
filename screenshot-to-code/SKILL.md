---
name: screenshot-to-code
description: Turns a screenshot, mockup, Figma export, or photo of a UI into working front-end code - React + Tailwind CSS v4 by default, or Next.js, Vue, or plain HTML/CSS - matching layout, spacing, colors, and typography, then renders the result and compares it against the image to close visual gaps. Use whenever the user shares an image of a website, app screen, dashboard, component, or wireframe and wants it built, cloned, recreated, or "made real", or says "code this up", "build this design", or "match this screenshot".
---

# Screenshot to Code

Recreate the UI in the image as clean, responsive, accessible code, then check the render against the image.

## Workflow

1. **Pick the target stack.** If the user is inside a project, match it: read `package.json` for React/Next/Vue and the Tailwind version, and reuse existing components, tokens, and icon libraries. Do not ask when the repo already answers it. With no project:
   - Single screen or quick prototype: one self-contained `index.html` (Tailwind via the browser build, see [references/stack-setup.md](references/stack-setup.md)).
   - App or multi-screen: React + TypeScript + Tailwind v4 on Vite.
   - User mentions Next.js, SSR, or routing: Next.js App Router.

2. **Write a short spec before coding.** Looking at the image, note:
   - Layout regions top to bottom (nav, hero, sidebar, grid, footer) and the grid or flex structure of each
   - Design tokens: 3-6 colors as hex, font family guess and the type scale, spacing rhythm (usually multiples of 4px), corner radius, shadow style
   - Repeated components (cards, list rows, buttons) that should be one component with props
   - What the image cannot show: hover and focus states, mobile layout, real data, content below the fold

   Estimate sizes from the image resolution. If the screenshot is 2x (a Retina capture 2880px wide is a 1440px layout), halve the pixel measurements.

3. **Build.** Use semantic elements (`header`, `nav`, `main`, `section`, `button`, `a`), extract repeated pieces into components, and put tokens in one place (Tailwind v4 `@theme` or CSS custom properties) rather than scattering hex codes. Use real text from the image, not lorem ipsum. For images and logos you cannot extract, use sized placeholders with descriptive `alt` text. Use an icon library the project already has (default: `lucide-react`), not hand-drawn SVGs or emoji.

4. **Make it responsive.** Build for the screenshot's viewport first, then define how it collapses: multi-column grids stack, navs become a menu button, and type scales down with `clamp()` or responsive utilities. If the screenshot is mobile, go the other direction.

5. **Render and compare.** If you can run a browser (Playwright, a headless browser, or a browser tool), screenshot the result at the source image's viewport width and compare side by side. See [references/visual-check.md](references/visual-check.md). Fix the largest differences first: layout and alignment, then spacing, then type size and weight, then color. Two or three passes is usually enough; stop when remaining differences are at the level of font rendering.

6. **Deliver.** Provide the files, how to run them, and a short list of assumptions (fonts guessed, states invented, content inferred). Name anything that needs real assets.

## Stack notes

- **React 19**: function components with TypeScript prop types. `propTypes` checks were removed from React 19; do not add them. `forwardRef` is not needed for passing `ref` to function components.
- **Tailwind CSS v4**: configuration lives in CSS. Use `@import "tailwindcss";` and `@theme { --color-brand: #...; }`, not a `tailwind.config.js` and not the v3 `@tailwind base/components/utilities` directives. Custom tokens become utilities automatically (`bg-brand`).
- **Next.js (App Router)**: pages in `app/`, components are Server Components by default. Add `"use client"` only to components that use state, effects, or event handlers.
- **Create React App** is deprecated. Use Vite for plain React.

Setup commands for each stack are in [references/stack-setup.md](references/stack-setup.md).

## Worked example

Input: a 1440px-wide screenshot of a pricing section - centered heading, three plan cards with the middle one highlighted, feature checklists, and a button per card.

Spec:
- Regions: heading block, then a 3-column card grid, max width about 1100px, 24px gap
- Tokens: background `#0B1220`, card `#111A2E`, accent `#3B82F6`, text `#E5E7EB`, muted `#94A3B8`; Inter-like sans; radius 12px
- Components: `PlanCard` with `name`, `price`, `features[]`, `highlighted`, `cta`
- Unknowns: hover states, monthly/annual toggle behavior, mobile layout

Build: `PricingSection.tsx` mapping a `plans` array into `PlanCard`; `highlighted` adds an accent border and a "Most popular" label; `grid-cols-1 md:grid-cols-3`. Check icons from `lucide-react`.

Compare: the first render has cards 40px too tall because of button padding, and the heading weight is 600 against a 700 in the image. Fix both, re-render, and deliver with an assumptions list: toggle not built, font assumed Inter.

## Failure modes

- **Guessing the stack** when the repo already defines it, or mixing Tailwind v3 config into a v4 project.
- **Absolute positioning to force a pixel match.** It breaks on the first resize. Use flex and grid, and accept small differences.
- **One giant component.** Anything that repeats three times is a component with props.
- **Invisible states.** Buttons and links need hover and `focus-visible` styles even though the screenshot cannot show them. Inputs need labels.
- **Color drift.** Sample colors from flat areas of the image, not anti-aliased edges or gradients, and check text contrast meets WCAG AA (4.5:1 for body text).
- **Claiming a match without looking.** If you could not render the result, say the comparison was not done.
