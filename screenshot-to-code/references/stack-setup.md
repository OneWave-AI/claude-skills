# Stack Setup

Minimal setup for each target. Skip this entirely when working inside an existing project.

## Contents
- Single-file HTML with Tailwind
- React + TypeScript + Tailwind v4 (Vite)
- Next.js App Router
- Vue 3
- Plain HTML/CSS

## Single-file HTML with Tailwind

For prototypes and one-off screens. The browser build compiles Tailwind in the page, so it is not for production.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Page</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <style type="text/tailwindcss">
    @theme {
      --color-brand: #3b82f6;
      --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
    }
  </style>
</head>
<body class="bg-white text-slate-900 font-sans">
  <!-- markup -->
</body>
</html>
```

## React + TypeScript + Tailwind v4 (Vite)

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install tailwindcss @tailwindcss/vite
npm install lucide-react   # icons, if the design has them
```

`vite.config.ts`:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({ plugins: [react(), tailwindcss()] });
```

`src/index.css` (replace its contents):

```css
@import "tailwindcss";

@theme {
  --color-brand: #3b82f6;
  --color-surface: #111a2e;
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
}
```

Run with `npm run dev`.

Component shape:

```tsx
type PlanCardProps = {
  name: string;
  price: string;
  features: string[];
  highlighted?: boolean;
};

export function PlanCard({ name, price, features, highlighted = false }: PlanCardProps) {
  return (
    <article className={`rounded-xl bg-surface p-6 ${highlighted ? "ring-2 ring-brand" : ""}`}>
      <h3 className="text-lg font-semibold">{name}</h3>
      <p className="mt-2 text-4xl font-bold">{price}</p>
      <ul className="mt-6 space-y-2">
        {features.map((f) => <li key={f}>{f}</li>)}
      </ul>
    </article>
  );
}
```

## Next.js App Router

```bash
npx create-next-app@latest my-app --typescript --tailwind --app --eslint --yes
```

This scaffolds Tailwind v4 already wired through PostCSS with `@import "tailwindcss";` in `app/globals.css`; add tokens in an `@theme` block there. Put the page in `app/page.tsx`. Keep components as Server Components unless they need state or event handlers, then add `"use client"` at the top of that file only. Use `next/image` for images with explicit `width` and `height`.

## Vue 3

```bash
npm create vite@latest my-app -- --template vue-ts
cd my-app
npm install tailwindcss @tailwindcss/vite
```

Add the same `tailwindcss()` plugin to `vite.config.ts` and `@import "tailwindcss";` to the main CSS file. Use `<script setup lang="ts">` with `defineProps<{ ... }>()`.

## Plain HTML/CSS

Put tokens in custom properties and use grid/flex:

```css
:root {
  --color-brand: #3b82f6;
  --radius: 12px;
  --space: 8px;
}
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: calc(var(--space) * 3); }
```
