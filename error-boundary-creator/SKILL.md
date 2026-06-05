---
name: error-boundary-creator
description: Create error boundaries, error handling, and fallback UIs for React applications. Use when implementing error handling, creating fallback components, or setting up error reporting.
---

# Error Boundary Creator

Add resilient error handling to React and Next.js apps: error boundaries, fallback UIs, async error handling, and error reporting.

## Workflow

1. Identify error-prone areas: async operations, third-party integrations, and route-level entry points.
2. Wrap components in an error boundary. Use a class boundary or the `react-error-boundary` library. See references/class-boundaries.md.
3. For Next.js App Router, add the relevant `error.tsx`, `global-error.tsx`, and `not-found.tsx` segment files. See references/nextjs-error-handling.md.
4. Handle errors that boundaries miss (event handlers, promises) and wire up reporting. See references/async-and-reporting.md.
5. Design fallback UIs with `role="alert"` and a recovery action (reset or reload).
6. Route caught errors to a single reporting sink and test error states before shipping.

## Contents

- references/class-boundaries.md — Basic, resettable, and `react-error-boundary` patterns.
- references/nextjs-error-handling.md — App Router `error.tsx`, `global-error.tsx`, `not-found.tsx`.
- references/async-and-reporting.md — `useAsync` hook and the `reportError` integration module.

## Best Practices

1. Wrap at the route level for page-level isolation, and wrap third-party components separately.
2. Provide meaningful fallbacks with a recovery option.
3. Log every caught error to the monitoring service.
4. Do not catch errors the code cannot meaningfully handle.
5. Test error states in development.
