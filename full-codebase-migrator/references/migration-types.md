# Supported Migration Types

| Migration | From | To |
|-----------|------|----|
| Language | JavaScript (.js/.jsx) | TypeScript (.ts/.tsx) |
| Component Model | React Class Components | React Functional + Hooks |
| Framework | Create React App | Next.js / Vite |
| Framework | Express.js | Fastify / Hono / Elysia |
| Framework | Vue 2 (Options API) | Vue 3 (Composition API) |
| Framework | Angular.js | Angular (modern) |
| Styling | CSS / SCSS / CSS Modules | Tailwind CSS |
| Styling | Styled Components | CSS Modules / Tailwind |
| State | Redux (classic) | Redux Toolkit / Zustand / Jotai |
| Testing | Jest + Enzyme | Vitest + Testing Library |
| Build | Webpack | Vite / Turbopack / esbuild |
| Monorepo | Single repo | Turborepo / Nx workspace |
| ORM | Sequelize / TypeORM | Prisma / Drizzle |
| Runtime | Node.js (CommonJS) | Node.js (ESM) / Bun / Deno |
| Package Manager | npm | pnpm / yarn (berry) |
| Custom | Any | Any (user-defined rules) |

## When to Use This Skill

- Planning a major technology migration that needs a complete inventory before starting.
- Understanding the full blast radius of a framework or language change.
- Estimating effort and risk before committing to a migration.
- Producing a deterministic execution order that respects the dependency graph.
- Handing off a migration plan to a team with clear, file-level instructions.

## When NOT to Use This Skill

- Single-file conversions (do them directly).
- Codebases with fewer than 5 files (overkill).
- When the migration should execute immediately (this skill plans; use agent-army to execute).
