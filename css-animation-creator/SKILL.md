---
name: css-animation-creator
description: Create professional CSS animations, transitions, micro-interactions, and complex motion design. Use when adding animations, hover effects, loading states, page transitions, scroll animations, or any motion design work.
---

# CSS Animation Creator

Build production-grade, accessible, GPU-efficient motion for web UIs using CSS, Tailwind, and Framer Motion.

## Workflow

1. Identify the purpose of the motion: feedback, delight, guidance, or storytelling.
2. Choose the technique: CSS transitions for state changes, keyframes for looping or multi-step motion, Framer Motion or JS for orchestration and scroll-linked effects.
3. Set timing and easing to match the interaction. Apply the timing and easing tables in `references/principles-and-timing.md`.
4. Author the animation. Pull ready-made keyframes and patterns from the reference files below rather than writing from scratch.
5. Constrain animated properties to `transform` and `opacity` for GPU acceleration. Apply `references/performance.md`.
6. Honor reduced-motion preferences for every animation. Apply `references/accessibility.md`.
7. Verify on low-end devices and confirm no layout thrash before shipping.

## Contents

- `references/principles-and-timing.md` — Disney 12 principles mapped to UI, duration and easing tables.
- `references/transitions.md` — Transition syntax, easing functions, cubic-bezier presets, Tailwind transitions.
- `references/keyframe-library.md` — Keyframe syntax plus fade, scale, bounce, rotate, slide, and attention-seeker keyframes.
- `references/loading-animations.md` — Spinners, dots, skeleton loaders, shimmer, progress bars.
- `references/micro-interactions.md` — Button, hover, icon, form, and success/error interactions.
- `references/page-transitions.md` — View Transitions API, Framer Motion page and shared-layout transitions, staggered lists.
- `references/scroll-animations.md` — Intersection Observer, Framer Motion scroll hooks, native CSS scroll-driven animations.
- `references/accessibility.md` — `prefers-reduced-motion` CSS, Tailwind motion-safe/reduce, React hook.
- `references/tailwind-config.md` — Drop-in `tailwind.config.js` animation and keyframe definitions.
- `references/performance.md` — GPU-accelerated properties, `will-change`, `contain`, performance checklist.
