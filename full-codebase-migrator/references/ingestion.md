# Codebase Ingestion Reference

Detail for Step 1 (Full Codebase Ingestion) and Step 2 (Dependency Graph).

## Architecture

```
Commander
 |
 |-- Phase 1: Full Ingestion (sequential, read everything)
 |    |-- Glob: discover all source files
 |    |-- Read: ingest every file into context
 |    |-- Bash: collect metadata (line counts, git history, package.json)
 |
 |-- Phase 2: Analysis (in-context reasoning)
 |    |-- Dependency graph construction
 |    |-- Complexity scoring per file
 |    |-- Risk classification
 |    |-- Migration pattern matching
 |
 |-- Phase 3: Plan Generation (Write output)
 |    |-- migration-plan.md (the deliverable)
 |    |-- Optional: migration-plan.json (machine-readable)
```

## Glob Patterns by Migration Type

```
JS to TS:        **/*.{js,jsx,mjs,cjs}
React migration: **/*.{js,jsx,ts,tsx}
Vue migration:   **/*.{vue,js,ts}
Angular:         **/*.{ts,html,scss,css}
General:         **/*.{js,jsx,ts,tsx,vue,svelte,css,scss,json,yaml,yml,md}
```

Always exclude:

```
node_modules/**   dist/**   build/**   .next/**   coverage/**
*.min.js   *.bundle.js   package-lock.json   yarn.lock   pnpm-lock.yaml
```

## Metadata Collection (Bash)

1. Line counts -- `wc -l` on every discovered file. Drives effort estimation.
2. Package manifest -- read package.json (or equivalent) for dependencies, scripts, config.
3. Config files -- read tsconfig.json, .babelrc, webpack.config.js, vite.config.ts, .eslintrc, .prettierrc, and any others.
4. Git history -- `git log --oneline -20` for recent context; `git log --all --pretty=format:"%h %s" --diff-filter=M -- "*.js"` (adjust per migration type) to see which files change most frequently.
5. Directory structure -- `find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*'` to map the layout.

## Read Order

1. Entry points: index.js, App.js, main.js, server.js, or equivalents.
2. Config files: tsconfig, webpack, vite, eslint, babel.
3. Shared utilities, types, constants.
4. Feature files grouped by directory.
5. Test files last.

For large codebases (500+ files), use Agent sub-agents to read files in parallel batches. Each agent reads a directory subtree and returns file contents plus a brief summary.

## Context Budget Management

- Files under 1000 lines: read in full. Prioritize 500-1000 line files -- they are the riskiest to migrate.
- Files 1000+ lines: read first 500 lines + last 100 lines + any class/function declarations. Flag for manual review.
- If total source exceeds ~800K tokens, prioritize: entry points > shared code > feature code > tests > styles. Note which files were partially read or skipped.

## Dependency Graph Construction

### Import Analysis

For every file, extract:
- Static imports: `import X from './path'`, `const X = require('./path')`
- Dynamic imports: `import('./path')`, `require.resolve('./path')`
- Re-exports: `export { X } from './path'`
- Side-effect imports: `import './styles.css'`
- Type-only imports (TS): `import type { X } from './path'`

Build an adjacency list:

```json
{
  "src/App.tsx": {
    "imports": ["src/components/Header.tsx", "src/hooks/useAuth.ts", "src/utils/api.ts"],
    "importedBy": ["src/index.tsx"],
    "externalDeps": ["react", "react-router-dom"]
  }
}
```

### Layer Classification

Classify every file into one layer (top = most depended upon):

1. Foundation -- types, interfaces, constants, enums, config. Imported by many, imports few.
2. Utilities -- helpers, formatters, validators. Imported by features, imports foundation.
3. Services -- API clients, data access, state management. Imports utilities and foundation.
4. Components/Features -- UI components, route handlers, feature modules.
5. Pages/Routes -- top-level page compositions. Imports components.
6. Entry Points -- index.js, App.js, server.js. Imports pages.
7. Tests -- import everything, imported by nothing.
8. Config -- build/linter configs. Usually standalone.

### Cycles

Detect circular dependencies. A cycle means files cannot migrate independently. Flag all cycles and recommend resolution strategies.

### External Dependency Classification

- Compatible: works with both source and target (no changes).
- Needs Update: has a target-compatible version (update version).
- Needs Replacement: incompatible with target (find alternative).
- Needs Wrapper: works with an adapter/wrapper pattern.
- Must Remove: no path forward (rewrite functionality).
