# Output Template Reference (Steps 7 and 8)

Templates the skill emits as its deliverables.

## Step 7: migration-plan.md Structure

Write the final deliverable to the specified output location using this structure:

```markdown
# Migration Plan: [Source] to [Target]

Generated: [timestamp]
Codebase: [repo name / path]
Total files: [N]
Estimated effort: [Xh]
Estimated calendar time: [X days] ([N developers])

---

## Table of Contents

1. Executive Summary
2. Migration Type
3. Codebase Inventory
4. Dependency Graph
5. External Dependencies
6. Migration Phases
7. File-by-File Changes
8. Risk Assessment
9. Effort Estimation
10. Rollback Strategy
11. Pre-Migration Checklist
12. Post-Migration Verification

## Executive Summary

[2-3 paragraph overview: what is being migrated, why, key risks, estimated effort,
recommended approach (big bang vs incremental), and team recommendations]

## Migration Type

- From: [source technology/framework/pattern]
- To: [target technology/framework/pattern]
- Scope: [full repo / specific directories]
- Strategy: [incremental (recommended for 50+ files) / big bang (viable for <50 files)]

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
[Files with highest centrality -- the backbone of the codebase, must migrate cleanly]

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

[Rollback plan as defined in Step 5]

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

## Step 8: Optional migration-plan.json

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
  "phases": [],
  "dependencies": {},
  "risks": [],
  "externalDeps": []
}
```

## Edge Cases

### Codebase Too Large for Context

1. Prioritize by layer -- read foundation and utility layers in full, sample feature layers.
2. Use Agent sub-agents -- deploy agents to read and summarize subsections. Each agent reads one directory subtree and returns a structured summary (file list, import graph, patterns found).
3. Aggregate summaries -- the commander combines all sub-agent summaries into the full picture.
4. Flag gaps -- note clearly which files were summarized vs fully analyzed.

### Monorepo with Multiple Packages

1. Treat each package as a semi-independent migration.
2. Identify cross-package dependencies.
3. Generate a per-package plan plus a top-level orchestration plan.
4. Recommend migration order across packages (shared libs first, apps last).

### Mixed Codebase (Already Partially Migrated)

1. Identify which files are already in the target state.
2. Classify files as: migrated, partially migrated, not migrated.
3. Focus the plan on unmigrated files.
4. Note partially migrated files that need completion.

### No Tests Exist

1. Flag this as a HIGH risk factor.
2. Recommend adding integration tests for critical paths BEFORE migrating.
3. Include a pre-migration test authoring phase in the plan.

## Quality Checklist for the Plan

Before delivering, verify:

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
