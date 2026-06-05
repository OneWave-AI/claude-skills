# Color Theory and Analysis

Reference for harmony schemes, accessibility, and advanced palette features.

## Harmony Schemes

Generate complementary schemes from the dominant hue:

- Monochromatic: Variations of a single hue (tints, shades, tones)
- Analogous: Adjacent colors on the wheel
- Complementary: Opposite colors on the wheel
- Triadic: Three evenly spaced colors
- Split-complementary: Base plus the two colors adjacent to its complement
- Tetradic: Four colors forming two complementary pairs

## Extended Palette

For each primary color, derive:

- Light and dark variations
- Tints (add white)
- Shades (add black)
- Tones (add gray)
- Numeric scales: 50, 100, 200 ... 900, 950

## Accessibility

- Check WCAG 2.1 contrast ratios for every text/background pairing.
- Target 4.5:1 for normal text (AA), 3:1 for large text, 7:1 for AAA.
- Test the palette against color blindness types:
  - Protanopia (red-blind)
  - Deuteranopia (green-blind)
  - Tritanopia (blue-blind)
- Recommend accessible alternatives where a pairing fails.

## Advanced Features

Mood board: Generate color combinations, usage examples, and gradient options.

Brand matching: Compare against existing brand colors, find closest matches, and suggest similar palettes.

## Best Practices

Color extraction:
- Filter out near-white and near-black unless prominent.
- Group similar colors (within roughly 10% similarity).
- Weight by visual importance, not just raw frequency.

Palette generation:
- Maintain color harmony.
- Ensure sufficient contrast.
- Generate semantic names (primary, secondary, accent).
- Provide light and dark variations.

Export:
- Support common formats (CSS, Tailwind, SCSS, JSON, iOS, Android).
- Include usage guidelines and example implementations.
