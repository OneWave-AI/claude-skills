---
name: full-codebase-migrator
description: Uses 1M context window to ingest an entire codebase and output a file-by-file migration plan. Supports JS to TS, React class to hooks, framework migrations, and more. Generates migration-plan.md with file inventory, dependency graph, migration order, file-by-file changes, estimated effort, and risk assessment.
tools: Read, Glob, Grep, Write, Bash, Agent
user_invocable: true
---

# Full Codebase Migrator

A production-grade migration planning system that leverages the full 1M token context window to ingest an entire codebase, understand its architecture end-to-end, and produce a comprehensive, file-by-file migration plan. This is not a partial analysis -- it reads every file, traces every dependency, and outputs an actionable plan that a team can execute sequentially without conflicts.

## Supported Migration Types

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

## When to Use

- You are planning a major technology migration and need a complete inventory before starting
- You want to understand the full blast radius of a framework or language change
- You need to estimate effort and risk before committing to a migration
- You want a deterministic execution order that respects the dependency graph
- You need to hand off a migration plan to a team with clear, file-level instructions

## When NOT to Use

- Single-file conversions (just do them directly)
- Codebases with fewer than 5 files (overkill)
- When you want to execute the migration immediately (this skill plans; use agent-army to execute)

## Architecture

```
You (Commander)
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

## Execution Protocol

Follow these steps precisely when this skill is invoked.

### Step 0: Identify Migration Type

Before doing anything, clarify the migration scope with the user:

1. **Determine migration type** -- Ask the user (or infer from context) what the migration is. Examples: "JS to TS", "CRA to Next.js", "Redux to Zustand".
2. **Determine migration scope** -- Full repo or a specific directory? Default to full repo.
3. **Determine output location** -- Where to write migration-plan.md. Default to the repo root.
4. **Determine constraints** -- Are there files or directories to exclude? Are there deadlines or team size considerations?

If the user has already specified these in their prompt, skip the questions and proceed.

### Step 1: Full Codebase Ingestion

This is the critical step that leverages the 1M context window. Read everything.

#### 1a. Discover All Source Files

```
Use Glob to find all relevant source files. Typical patterns by migration type:

JS to TS:        **/*.{js,jsx,mjs,cjs}
React migration:  **/*.{js,jsx,ts,tsx}
Vue migration:    **/*.{vue,js,ts}
Angular:          **/*.{ts,html,scss,css}
General:          **/*.{js,jsx,ts,tsx,vue,svelte,css,scss,json,yaml,yml,md}

Always exclude:
- node_modules/**
- dist/**
- build/**
- .next/**
- coverage/**
- *.min.js
- *.bundle.js
- package-lock.json
- yarn.lock
- pnpm-lock.yaml
```

#### 1b. Collect Metadata

Run these Bash commands to gather structural information:

1. **Line counts** -- `wc -l` on every discovered file. This drives effort estimation.
2. **Package manifest** -- Read package.json (or equivalent) for dependencies, scripts, and config.
3. **Config files** -- Read tsconfig.json, .babelrc, webpack.config.js, vite.config.ts, .eslintrc, .prettierrc, and any other config files.
4. **Git history** -- `git log --oneline -20` for recent context. `git log --all --pretty=format:"%h %s" --diff-filter=M -- "*.js"` (adjusted per migration type) to see which files change most frequently.
5. **Directory structure** -- `find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*'` to map the project layout.

#### 1c. Read Every Source File

This is the key differentiator. Read EVERY source file discovered in 1a. Use the Read tool systematically:

1. Start with entry points: `index.js`, `App.js`, `main.js`, `server.js`, or equivalents.
2. Read config files next: tsconfig, webpack, vite, eslint, babel configs.
3. Read shared utilities, types, and constants.
4. Read feature files grouped by directory.
5. Read test files last.

For large codebases (500+ files), use Agent sub-agents to read files in parallel batches. Each agent reads a directory subtree and returns file contents plus a brief summary.

**Context budget management:**
- Files under 100 lines: read in full
- Files 100-500 lines: read in full
- Files 500-1000 lines: read in full (prioritize these -- they are the riskiest to migrate)
- Files 1000+ lines: read first 500 lines + last 100 lines + any class/function declarations. Flag for manual review.
- If the total codebase exceeds ~800K tokens of source, prioritize: entry points > shared code > feature code > tests > styles. Note which files were partially read or skipped.

### Step 2: Dependency Graph Construction

With the full codebase in context, build the dependency graph:

#### 2a. Import Analysis

For every file, extract:
- **Static imports**: `import X from './path'`, `const X = require('./path')`
- **Dynamic imports**: `import('./path')`, `require.resolve('./path')`
- **Re-exports**: `export { X } from './path'`
- **Side-effect imports**: `import './styles.css'`
- **Type-only imports** (TS): `import type { X } from './path'`

Build an adjacency list:
```
{
  "src/App.tsx": {
    "imports": ["src/components/Header.tsx", "src/hooks/useAuth.ts", "src/utils/api.ts"],
    "importedBy": ["src/index.tsx"],
    "externalDeps": ["react", "react-router-dom"]
  }
}
```

#### 2b. Identify Layers

Classify every file into one of these layers (top = most depended upon):

1. **Foundation** -- Types, interfaces, constants, enums, config. Imported by many, imports few.
2. **Utilities** -- Helper functions, formatters, validators. Imported by features, imports foundation.
3. **Services** -- API clients, data access, state management. Imports utilities and foundation.
4. **Components/Features** -- UI components, route handlers, feature modules. Imports services, utilities, foundation.
5. **Pages/Routes** -- Top-level page compositions. Imports components.
6. **Entry Points** -- index.js, App.js, server.js. Imports pages.
7. **Tests** -- Test files. Import everything, imported by nothing.
8. **Config** -- Build configs, linter configs. Usually standalone.

#### 2c. Identify Cycles

Detect circular dependencies. These are migration hazards -- a cycle means you cannot migrate files independently. Flag all cycles and recommend resolution strategies.

#### 2d. Identify External Dependencies

List all third-party packages and classify them:
- **Compatible**: Works with both source and target (no changes needed)
- **Needs Update**: Has a version compatible with the target (update version)
- **Needs Replacement**: Incompatible with target (find alternative)
- **Needs Wrapper**: Can work with an adapter/wrapper pattern
- **Must Remove**: No path forward (rewrite functionality)

### Step 3: File-by-File Analysis

For every source file, produce a migration assessment:

```
### [relative/path/to/file.js]

- **Lines**: 245
- **Layer**: Component
- **Complexity**: Medium
- **Imports**: 8 internal, 3 external
- **Imported by**: 4 files
- **Migration difficulty**: 3/5
- **Estimated effort**: 30 minutes
- **Risk level**: Medium

**Current patterns found:**
- Class component with 3 lifecycle methods (componentDidMount, componentDidUpdate, componentWillUnmount)
- Local state with this.setState (5 occurrences)
- Refs via createRef (2 occurrences)
- HOC wrapper (withRouter)

**Required changes:**
1. Convert class to function component
2. Replace lifecycle methods with useEffect hooks
3. Replace this.state/this.setState with useState hooks
4. Replace createRef with useRef hooks
5. Replace withRouter HOC with useRouter/useNavigate hooks
6. Add TypeScript types for props (currently PropTypes)
7. Add TypeScript types for state shape
8. Update imports from '.js' to '.ts' extensions (if applicable)

**Dependencies that must migrate first:**
- src/types/user.ts (needs TypeScript types defined)
- src/hooks/useAuth.ts (referenced hook must exist)

**Risk factors:**
- Complex componentDidUpdate with multiple conditions -- requires careful useEffect dependency array
- Ref forwarding pattern may need forwardRef wrapper

**Testing impact:**
- src/__tests__/UserProfile.test.js must be updated (enzyme shallow render -> testing library render)
```

### Step 4: Migration Order Calculation

Using the dependency graph, calculate the optimal migration order. This is a topological sort with practical adjustments:

#### 4a. Base Order (Topological Sort)

1. Foundation layer first (types, constants, config)
2. Utilities second
3. Services third
4. Components fourth (leaf components before composite components)
5. Pages fifth
6. Entry points sixth
7. Tests last

#### 4b. Practical Adjustments

Adjust the base order for real-world concerns:

- **Quick wins first**: Within each layer, prioritize small/simple files. Early success builds momentum.
- **High-risk files early**: Migrate complex files while the team is fresh, not at the end when fatigue sets in.
- **Batch by feature**: When possible, group files by feature so a single PR migrates a complete feature.
- **Shared code before consumers**: Any file imported by 5+ other files should migrate before its consumers.
- **Break cycles first**: If circular dependencies exist, resolve them before migrating either file in the cycle.

#### 4c. Phase Grouping

Organize files into migration phases. Each phase should:

- Be completable in 1-3 days by one developer
- Contain files that can all be migrated without touching files in later phases
- Result in a buildable, testable codebase when complete
- Map to a single PR or small set of PRs

```
## Phase 1: Foundation (Day 1)
- Estimated effort: 4 hours
- Files: 12
- Risk: Low
| # | File | Lines | Effort | Notes |
|---|------|-------|--------|-------|
| 1 | src/types/index.ts | 45 | 15m | Already TS, just verify |
| 2 | src/constants/config.ts | 30 | 10m | Rename .js to .ts, add types |
| ... | ... | ... | ... | ... |

## Phase 2: Utilities (Day 1-2)
...

## Phase 3: Services (Day 2-3)
...
```

### Step 5: Risk Assessment

Produce a risk matrix for the overall migration:

#### 5a. File Risk Scores

Score each file 1-5 on these dimensions:
- **Complexity**: Lines of code, cyclomatic complexity, number of patterns to change
- **Centrality**: Number of files that depend on it (high centrality = high blast radius)
- **Volatility**: How often the file changes in git history (high volatility = merge conflict risk)
- **Test Coverage**: Does this file have tests? (no tests = higher risk)
- **External Coupling**: Does it tightly integrate with third-party libraries that need replacement?

Overall risk = weighted average: Complexity(0.25) + Centrality(0.30) + Volatility(0.15) + TestCoverage(0.15) + ExternalCoupling(0.15)

#### 5b. Migration-Level Risks

Assess these macro risks:

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Build breaks during migration | Medium | High | Phase-by-phase migration with CI checks after each phase |
| Type errors cascade | High | Medium | Start with `any` types, tighten incrementally |
| Third-party lib incompatibility | Low | High | Audit all deps before starting (Step 2d) |
| Team unfamiliarity with target | Medium | Medium | Pair programming on first 2 phases |
| Merge conflicts with active development | High | Medium | Feature freeze during foundation phase, or parallel branch |
| Test failures after migration | Medium | Medium | Run tests after each phase, fix immediately |
| Performance regression | Low | High | Benchmark before and after each phase |

#### 5c. Rollback Strategy

Define the rollback plan:
- Each phase maps to a PR. Revert the PR to roll back.
- Maintain a migration branch. If the migration stalls, the main branch is untouched.
- Document the point of no return (usually after Phase 1 merges to main).

### Step 6: Effort Estimation

Produce effort estimates at multiple granularities:

#### 6a. Per-File Estimates

Based on file size and migration patterns:

| File Size | Simple Patterns | Complex Patterns | Estimated Time |
|-----------|----------------|-----------------|----------------|
| < 50 lines | Rename + add types | N/A | 5-10 minutes |
| 50-150 lines | Add types, update imports | Lifecycle conversion, state refactor | 15-30 minutes |
| 150-300 lines | Add types, update imports | Multiple pattern changes | 30-60 minutes |
| 300-500 lines | Multiple files worth of work | Heavy refactoring | 1-2 hours |
| 500+ lines | Consider splitting first | Major risk, needs review | 2-4 hours |

#### 6b. Per-Phase Estimates

Sum file estimates plus overhead:
- **Overhead per phase**: 30 minutes for PR creation, review, CI, merge
- **Integration testing**: 15 minutes per phase to verify nothing broke
- **Buffer**: Add 20% buffer for unexpected issues

#### 6c. Total Estimate

```
## Effort Summary

| Phase | Files | Raw Effort | Buffer (20%) | Total |
|-------|-------|-----------|-------------|-------|
| 1. Foundation | 12 | 3h | 0.6h | 3.6h |
| 2. Utilities | 18 | 6h | 1.2h | 7.2h |
| 3. Services | 8 | 4h | 0.8h | 4.8h |
| 4. Components | 35 | 16h | 3.2h | 19.2h |
| 5. Pages | 10 | 5h | 1h | 6h |
| 6. Entry Points | 3 | 1h | 0.2h | 1.2h |
| 7. Tests | 25 | 8h | 1.6h | 9.6h |
| **Total** | **111** | **43h** | **8.6h** | **51.6h** |

- Calendar time (1 dev): ~7 working days
- Calendar time (2 devs): ~4 working days
- Calendar time (3 devs, parallelized): ~3 working days

Note: Phases 1-3 are sequential. Phases 4-7 can partially parallelize across developers.
```

### Step 7: Generate migration-plan.md

Write the final deliverable to the specified output location. The document structure:

```markdown
# Migration Plan: [Source] to [Target]

**Generated**: [timestamp]
**Codebase**: [repo name / path]
**Total files**: [N]
**Estimated effort**: [Xh]
**Estimated calendar time**: [X days] ([N developers])

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Migration Type](#migration-type)
3. [Codebase Inventory](#codebase-inventory)
4. [Dependency Graph](#dependency-graph)
5. [External Dependencies](#external-dependencies)
6. [Migration Phases](#migration-phases)
7. [File-by-File Changes](#file-by-file-changes)
8. [Risk Assessment](#risk-assessment)
9. [Effort Estimation](#effort-estimation)
10. [Rollback Strategy](#rollback-strategy)
11. [Pre-Migration Checklist](#pre-migration-checklist)
12. [Post-Migration Verification](#post-migration-verification)

## Executive Summary

[2-3 paragraph overview: what is being migrated, why, key risks, estimated effort,
recommended approach (big bang vs incremental), and team recommendations]

## Migration Type

- **From**: [source technology/framework/pattern]
- **To**: [target technology/framework/pattern]
- **Scope**: [full repo / specific directories]
- **Strategy**: [incremental (recommended for 50+ files) / big bang (viable for <50 files)]

## Codebase Inventory

### File Distribution by Type
| File Type | Count | Total Lines | % of Codebase |
|-----------|-------|-------------|---------------|
| .js | N | N | N% |
| .jsx | N | N | N% |
| ... | ... | ... | ... |

### Directory Structure
[tree output, annotated with migration notes]

### File Size Distribution
| Range | Count | Notes |
|-------|-------|-------|
| < 50 lines | N | Quick migrations |
| 50-150 lines | N | Standard effort |
| 150-300 lines | N | Moderate effort |
| 300-500 lines | N | Significant effort |
| 500+ lines | N | Consider splitting before migrating |

## Dependency Graph

### Layer Classification
[Table of all files classified into Foundation / Utilities / Services / Components / Pages / Entry Points / Tests / Config]

### Critical Path
[Files with highest centrality -- these are the backbone of the codebase and must migrate cleanly]

### Circular Dependencies
[List of cycles with recommended resolution]

## External Dependencies

| Package | Current | Status | Action | Replacement |
|---------|---------|--------|--------|-------------|
| react | 18.2.0 | Compatible | None | -- |
| lodash | 4.17.21 | Compatible | None | -- |
| moment | 2.29.4 | Needs Replacement | Replace | dayjs or date-fns |
| ... | ... | ... | ... | ... |

## Migration Phases

[Phase-by-phase breakdown as defined in Step 4]

## File-by-File Changes

[Every file's migration assessment as defined in Step 3, organized by phase]

## Risk Assessment

[Risk matrix and macro risks as defined in Step 5]

## Effort Estimation

[Effort tables as defined in Step 6]

## Rollback Strategy

[Rollback plan as defined in Step 5c]

## Pre-Migration Checklist

- [ ] All team members have read this plan
- [ ] Target framework/library versions agreed upon
- [ ] CI pipeline updated to support target (e.g., TypeScript compiler added)
- [ ] Branch strategy agreed (migration branch vs feature flags)
- [ ] Code freeze scheduled for foundation phase (if applicable)
- [ ] Rollback procedure tested
- [ ] Performance benchmarks captured (before state)
- [ ] Test suite passing at 100% before migration starts

## Post-Migration Verification

- [ ] All files migrated per plan
- [ ] Zero source-pattern files remaining (e.g., no .js files if migrating to TS)
- [ ] Build passes with zero errors
- [ ] Test suite passes at 100%
- [ ] No `any` types remaining (or documented exceptions)
- [ ] Performance benchmarks comparable to pre-migration
- [ ] Documentation updated
- [ ] Team trained on new patterns
```

### Step 8: Optional JSON Output

If the user requests it (or for large migrations where machine-readability helps), also generate `migration-plan.json`:

```json
{
  "metadata": {
    "generated": "ISO timestamp",
    "migrationFrom": "JavaScript",
    "migrationTo": "TypeScript",
    "totalFiles": 111,
    "estimatedHours": 51.6
  },
  "files": [
    {
      "path": "src/utils/helpers.js",
      "targetPath": "src/utils/helpers.ts",
      "lines": 145,
      "layer": "utility",
      "phase": 2,
      "phaseOrder": 3,
      "difficulty": 2,
      "estimatedMinutes": 20,
      "riskScore": 1.8,
      "dependencies": ["src/types/index.ts"],
      "dependedOnBy": ["src/services/api.ts", "src/components/Form.tsx"],
      "patterns": ["add-types", "update-imports"],
      "notes": "Pure functions, straightforward typing"
    }
  ],
  "phases": [...],
  "dependencies": {...},
  "risks": [...],
  "externalDeps": [...]
}
```

## Handling Edge Cases

### Codebase Too Large for Context

If the codebase exceeds the context window capacity:

1. **Prioritize by layer** -- Read foundation and utility layers in full, sample feature layers.
2. **Use Agent sub-agents** -- Deploy agents to read and summarize subsections of the codebase. Each agent reads one directory subtree and returns a structured summary (file list, import graph, patterns found).
3. **Aggregate summaries** -- The commander combines all sub-agent summaries into the full picture.
4. **Flag gaps** -- Clearly note in the migration plan which files were summarized vs fully analyzed.

### Monorepo with Multiple Packages

1. Treat each package as a semi-independent migration.
2. Identify cross-package dependencies.
3. Generate a per-package migration plan plus a top-level orchestration plan.
4. Recommend migration order across packages (shared libs first, apps last).

### Mixed Codebase (Already Partially Migrated)

1. Identify which files are already in the target state.
2. Classify files as: migrated, partially migrated, not migrated.
3. Focus the plan on unmigrated files.
4. Note any partially migrated files that need completion.

### No Tests Exist

1. Flag this as a HIGH risk factor.
2. Recommend adding integration tests for critical paths BEFORE migrating.
3. Include a "pre-migration test authoring" phase in the plan.

## Effort Calibration by Migration Type

Different migration types have different per-file effort multipliers:

| Migration Type | Simple File | Medium File | Complex File |
|---------------|------------|-------------|-------------|
| JS to TS (strict) | 10 min | 30 min | 2h |
| JS to TS (loose/any) | 5 min | 15 min | 45 min |
| Class to Hooks | 15 min | 45 min | 2.5h |
| CRA to Next.js | 10 min | 30 min | 1.5h |
| Redux to Zustand | 20 min | 1h | 3h |
| Vue 2 to Vue 3 | 15 min | 45 min | 2h |
| CSS to Tailwind | 10 min | 30 min | 1.5h |
| Jest to Vitest | 5 min | 15 min | 45 min |
| CommonJS to ESM | 5 min | 10 min | 30 min |

These are starting estimates. Adjust based on the specific codebase after ingestion.

## Quality Checklist for the Migration Plan

Before delivering the plan, verify:

- [ ] Every source file is accounted for (inventory matches glob results)
- [ ] Every file has a phase assignment
- [ ] No file depends on an unmigrated file in a later phase (topological order holds)
- [ ] All external dependencies are classified
- [ ] Effort estimates sum correctly
- [ ] Risk scores are calculated and documented
- [ ] Circular dependencies are identified and have resolution strategies
- [ ] The plan is actionable -- a developer can pick up Phase 1 and start immediately
- [ ] Rollback strategy is defined
- [ ] Pre-migration and post-migration checklists are included
