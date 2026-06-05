# Workflow Detail: Steps 3 through 6

Expanded procedure for the analysis, ordering, risk, and effort steps of the skill.

## Step 3: Per-File Migration Assessment

Produce this assessment for every source file:

```
### [relative/path/to/file.js]

- Lines: 245
- Layer: Component
- Complexity: Medium
- Imports: 8 internal, 3 external
- Imported by: 4 files
- Migration difficulty: 3/5
- Estimated effort: 30 minutes
- Risk level: Medium

Current patterns found:
- Class component with 3 lifecycle methods (componentDidMount, componentDidUpdate, componentWillUnmount)
- Local state with this.setState (5 occurrences)
- Refs via createRef (2 occurrences)
- HOC wrapper (withRouter)

Required changes:
1. Convert class to function component
2. Replace lifecycle methods with useEffect hooks
3. Replace this.state/this.setState with useState hooks
4. Replace createRef with useRef hooks
5. Replace withRouter HOC with useRouter/useNavigate hooks
6. Add TypeScript types for props (currently PropTypes)
7. Add TypeScript types for state shape
8. Update imports from '.js' to '.ts' extensions (if applicable)

Dependencies that must migrate first:
- src/types/user.ts (needs TypeScript types defined)
- src/hooks/useAuth.ts (referenced hook must exist)

Risk factors:
- Complex componentDidUpdate with multiple conditions -- requires careful useEffect dependency array
- Ref forwarding pattern may need forwardRef wrapper

Testing impact:
- src/__tests__/UserProfile.test.js must be updated (enzyme shallow render -> testing library render)
```

## Step 4: Migration Order Calculation

### Base Order (Topological Sort)

1. Foundation (types, constants, config)
2. Utilities
3. Services
4. Components (leaf components before composite components)
5. Pages
6. Entry points
7. Tests last

### Practical Adjustments

- Quick wins first: within each layer, prioritize small/simple files. Early success builds momentum.
- High-risk files early: migrate complex files while the team is fresh.
- Batch by feature: group files so a single PR migrates a complete feature.
- Shared code before consumers: any file imported by 5+ others migrates before its consumers.
- Break cycles first: resolve circular dependencies before migrating either file in the cycle.

### Phase Grouping

Each phase should:
- Be completable in 1-3 days by one developer.
- Contain files migratable without touching files in later phases.
- Result in a buildable, testable codebase when complete.
- Map to a single PR or small set of PRs.

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
```

## Step 5: Risk Assessment

### File Risk Scores

Score each file 1-5 on:
- Complexity: lines of code, cyclomatic complexity, number of patterns to change.
- Centrality: number of dependents (high centrality = high blast radius).
- Volatility: git change frequency (high volatility = merge conflict risk).
- Test Coverage: presence of tests (no tests = higher risk).
- External Coupling: tight integration with third-party libraries needing replacement.

Overall risk = weighted average: Complexity(0.25) + Centrality(0.30) + Volatility(0.15) + TestCoverage(0.15) + ExternalCoupling(0.15).

### Migration-Level Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Build breaks during migration | Medium | High | Phase-by-phase migration with CI checks after each phase |
| Type errors cascade | High | Medium | Start with `any` types, tighten incrementally |
| Third-party lib incompatibility | Low | High | Audit all deps before starting (Step 2 external classification) |
| Team unfamiliarity with target | Medium | Medium | Pair programming on first 2 phases |
| Merge conflicts with active development | High | Medium | Feature freeze during foundation phase, or parallel branch |
| Test failures after migration | Medium | Medium | Run tests after each phase, fix immediately |
| Performance regression | Low | High | Benchmark before and after each phase |

### Rollback Strategy

- Each phase maps to a PR. Revert the PR to roll back.
- Maintain a migration branch. If the migration stalls, the main branch is untouched.
- Document the point of no return (usually after Phase 1 merges to main).

## Step 6: Effort Estimation

### Per-File Estimates

| File Size | Simple Patterns | Complex Patterns | Estimated Time |
|-----------|----------------|-----------------|----------------|
| < 50 lines | Rename + add types | N/A | 5-10 minutes |
| 50-150 lines | Add types, update imports | Lifecycle conversion, state refactor | 15-30 minutes |
| 150-300 lines | Add types, update imports | Multiple pattern changes | 30-60 minutes |
| 300-500 lines | Multiple files worth of work | Heavy refactoring | 1-2 hours |
| 500+ lines | Consider splitting first | Major risk, needs review | 2-4 hours |

### Per-Phase Estimates

- Overhead per phase: 30 minutes for PR creation, review, CI, merge.
- Integration testing: 15 minutes per phase to verify nothing broke.
- Buffer: add 20% for unexpected issues.

### Total Estimate

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
| Total | 111 | 43h | 8.6h | 51.6h |

- Calendar time (1 dev): ~7 working days
- Calendar time (2 devs): ~4 working days
- Calendar time (3 devs, parallelized): ~3 working days

Note: Phases 1-3 are sequential. Phases 4-7 can partially parallelize across developers.
```

## Effort Calibration by Migration Type

Per-file effort multipliers. Starting estimates -- adjust after ingestion.

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
