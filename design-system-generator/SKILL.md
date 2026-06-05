---
name: design-system-generator
description: Create design systems with tokens, components, and documentation. Use when building design systems, creating component libraries, or establishing design tokens.
---

# Design System Generator

Generate a token-driven design system: tokens, base components, build config, and documentation.

## Contents

- `references/design-tokens.md` — color, typography, spacing, shadow, and radius token files plus CSS variable setup.
- `references/components.md` — Button, Input, Card implementations and the component barrel index.
- `references/config-and-utilities.md` — Tailwind config and the `cn` class-merge helper.

## Workflow

1. Define design tokens. Create `tokens/` with colors, typography, spacing, and effects (shadows, radii) per `references/design-tokens.md`. Replace the reference values with the project brand palette.
2. Add CSS variables. Set up `:root` and `.dark` custom properties in `globals.css` using the variable block in `references/design-tokens.md`.
3. Wire the build. Add the `cn` helper and extend the Tailwind theme from the token files following `references/config-and-utilities.md`.
4. Build base components. Implement Button, Input, and Card from `references/components.md`, then extend the set as the product requires.
5. Export a barrel. Re-export every shipped component from `components/ui/index.ts` (see `references/components.md`).
6. Document usage and variants. For each component, note its variants, sizes, props, and accessibility behavior so consumers apply it consistently.
