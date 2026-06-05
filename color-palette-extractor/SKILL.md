---
name: color-palette-extractor
description: Extract color palettes from images, websites, or designs. Identifies dominant colors, generates complementary schemes, and exports in multiple formats (HEX, RGB, HSL, Tailwind, CSS variables). Use when users need color schemes from images, brand colors, or design system palettes.
---

# Color Palette Extractor

Extract and generate accessible color palettes from images, websites, and designs.

## Contents

- `references/output-template.md` — full report structure for presenting a palette
- `references/export-formats.md` — CSS, Tailwind, SCSS, JSON, iOS, Android snippets
- `references/color-theory.md` — harmony schemes, accessibility, extraction best practices

## Workflow

1. Identify the source: image file (PNG, JPG, SVG), website URL, screenshot, design mockup, or an existing color code to build from.

2. Extract colors.
   - From an image: analyze pixel data, identify dominant colors, group similar shades, calculate frequency, and sort by prominence.
   - From a website: fetch and parse the CSS, extract color values, and identify brand, accent, text, and background colors.
   - Cluster with K-means; extract 5-10 dominant colors. Ignore near-white and near-black unless significant.

3. Build the primary palette (5-10 colors): most dominant color, 2-3 supporting colors, 1-2 accents, a background, and a text color. Generate an extended palette with tints, shades, tones, and 50-950 numeric scales. See `references/color-theory.md`.

4. Run color harmony analysis to produce complementary, analogous, triadic, split-complementary, tetradic, and monochromatic schemes. See `references/color-theory.md`.

5. Check accessibility: compute WCAG 2.1 contrast ratios for each text/background pairing and test against protanopia, deuteranopia, and tritanopia. Recommend accessible alternatives where a pairing fails. See `references/color-theory.md`.

6. Format the report following `references/output-template.md`, and export to the requested formats using `references/export-formats.md`.

## Output Requirements

Deliver palettes that have clear dominant colors, sufficient variations, semantic naming, harmony schemes, contrast ratios that pass accessibility checks, usage guidelines, and exports in multiple formats. Produce professional, accessible palettes ready for immediate use in design systems.

## Example Triggers

- "Extract colors from this screenshot"
- "Get color palette from this website"
- "Generate a color scheme from this image"
- "Create Tailwind config from these colors"
- "Find dominant colors in this logo"
- "Build a palette from this hex code"
