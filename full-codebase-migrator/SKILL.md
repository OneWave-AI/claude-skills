---
name: full-codebase-migrator
description: Uses 1M context window to ingest an entire codebase and output a file-by-file migration plan. Supports JS to TS, React class to hooks, framework migrations, and more. Generates migration-plan.md with file inventory, dependency graph, migration order, file-by-file changes, estimated effort, and risk assessment.
tools: Read, Glob, Grep, Write, Bash, Agent
user_invocable: true
---

# Full Codebase Migrator

Leverage the full 1M token context window to ingest an entire codebase, understand its architecture end-to-end, and produce a comprehensive, file-by-file migration plan that a team can execute sequentially without conflicts.

## Contents

- `references/migration-types.md` -- supported migration types; when to use and when not to use this skill.
- `references/ingestion.md` -- architecture, glob patterns, metadata collection, read order, context budgeting, and dependency graph construction (Steps 0-2).
- `references/workflow-detail.md` -- per-file assessment, migration order, risk scoring, and effort estimation templates (Steps 3-6).
- `references/output-template.md` -- migration-plan.md and migration-plan.json templates, edge cases, and the final quality checklist (Steps 7-8).

## Workflow

1. Identify scope. Determine migration type, scope (full repo or directory), output location for migration-plan.md, and any exclusions or constraints. Infer from the user's prompt when already specified. See `references/migration-types.md` for supported types and fit.
2. Ingest the codebase. Glob all source files, collect metadata with Bash (line counts, package manifest, configs, git history, directory tree), then Read every source file. For 500+ file codebases, dispatch Agent sub-agents to read directory subtrees in parallel. See `references/ingestion.md`.
3. Build the dependency graph. Extract every import, build an adjacency list, classify each file into layers, detect circular dependencies, and classify external dependencies. See `references/ingestion.md`.
4. Assess each file. Produce a per-file migration assessment covering layer, complexity, patterns found, required changes, prerequisite dependencies, risk factors, and testing impact. See `references/workflow-detail.md`.
5. Calculate migration order. Run a topological sort by layer, apply practical adjustments (quick wins, high-risk-early, break cycles first), and group files into buildable, PR-sized phases. See `references/workflow-detail.md`.
6. Assess risk. Score each file 1-5 on complexity, centrality, volatility, test coverage, and external coupling. Build the migration-level risk matrix and rollback strategy. See `references/workflow-detail.md`.
7. Estimate effort. Derive per-file, per-phase, and total estimates with overhead and a 20% buffer, then translate into calendar time by team size. See `references/workflow-detail.md` and the effort calibration table in `references/migration-types.md`.
8. Generate the deliverable. Write migration-plan.md to the output location, and migration-plan.json when machine-readability helps. Verify against the quality checklist before delivering. See `references/output-template.md`.

## Edge Cases

Codebases too large for context, monorepos, partially migrated codebases, and codebases without tests each need adjusted handling. See `references/output-template.md`.
