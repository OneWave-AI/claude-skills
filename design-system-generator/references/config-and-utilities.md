# Config and Utilities

Wiring that binds tokens and components into the build: the Tailwind config and the `cn` class-merge helper.

## Tailwind Config

```javascript
// tailwind.config.js
const { colors, typography, spacing, shadows, radii } = require('./tokens');

module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: colors.primary,
        gray: colors.gray,
        success: colors.success,
        warning: colors.warning,
        error: colors.error,
      },
      fontFamily: typography.fontFamily,
      fontSize: typography.fontSize,
      spacing: spacing,
      boxShadow: shadows,
      borderRadius: radii,
    },
  },
  plugins: [],
};
```

## Utility Function

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```
