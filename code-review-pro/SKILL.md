---
name: code-review-pro
description: Performs a deep code review of files, modules, a diff, or a branch - finding security vulnerabilities (mapped to OWASP Top 10:2025), correctness bugs, performance problems, and maintainability issues - and returns severity-ranked findings with evidence and concrete fixes. Use when the user asks to review, audit, or sanity-check code, asks "is this safe", "what's wrong with this", "find bugs", or wants a security or performance pass before shipping. For posting line comments on a GitHub pull request, use git-pr-reviewer.
---

# Code Review Pro

Find the problems that matter, prove each one, and show the fix. A short list of real issues beats a long list of maybes.

## Workflow

1. **Set the scope.** Decide what is under review: a pasted snippet, specific files, the working-tree diff (`git diff`, `git diff --staged`), or a branch against its base (`git diff main...HEAD`). For a diff, review the changed lines but read enough surrounding code to know how they are called.

2. **Learn the context before judging.** Identify language, framework and version (check `package.json`, `pyproject.toml`, `go.mod`, and so on), how the code is reached (HTTP handler, job, CLI, library), what input is untrusted, and any repo conventions (linters, `CLAUDE.md`, existing patterns). A pattern that is a bug in one framework can be safe in another; for example, React escapes JSX text, so XSS lives in `dangerouslySetInnerHTML`, `href` values, and raw HTML sinks.

3. **Review in priority order**, using [references/checklist.md](references/checklist.md):
   1. Security
   2. Correctness and edge cases
   3. Performance
   4. Maintainability and conventions

4. **Verify every finding before reporting it.** For each candidate, trace the data flow: where does the input come from, can an attacker or real user control it, and does anything upstream already validate or escape it? Check whether a test covers it. If you can run code, reproduce the bug with a small test or script. Drop findings you cannot support; mark the rest with a confidence level.

5. **Rank and write the report** in the format below. Lead with the highest severity. Group repeated instances of one problem into a single finding with all locations.

## Severity

- **Critical** - exploitable now or causes data loss/corruption: injection with user input, auth bypass, secrets in code, broken access control on real data.
- **High** - likely bug or vulnerability under realistic conditions: race on shared state, missing authorization check, unbounded query on a user-facing path, swallowed errors that hide failures.
- **Medium** - correct today but fragile: missing input validation behind a trusted caller, N+1 queries on small data, confusing ownership of state.
- **Low** - style, naming, small simplifications. Report at most a handful; skip anything a linter or formatter already enforces.

## Output format

````markdown
# Code Review: [scope]

**Verdict**: [Ship / Ship after fixes / Do not ship] - [one sentence why]
**Findings**: [n] critical, [n] high, [n] medium, [n] low

## Critical

### 1. SQL injection in user search (`src/api/users.ts:42`)
**Category**: A05:2025 Injection | **Confidence**: High
**Evidence**: `q` comes from `req.query` and is interpolated into the SQL string; no validation upstream.
**Impact**: Any caller can read or modify arbitrary tables.

Current:
```ts
const rows = await db.query(`SELECT * FROM users WHERE name LIKE '%${q}%'`);
```

Fix:
```ts
const rows = await db.query("SELECT * FROM users WHERE name LIKE $1", [`%${q}%`]);
```

## High
...

## Medium
...

## Low
- `utils/date.ts:10` - [one line]

## What is solid
[Two or three specific things done well, so the author knows what to keep.]

## Not reviewed
[Files, paths, or concerns outside scope or that could not be verified.]
````

## Traps that cause bad reviews

- **Reporting without reading the caller.** "Missing validation" is often validated one layer up. Look before flagging.
- **Generic advice.** "Consider adding error handling" is not a finding. Name the failure: which call throws, what the user sees, what state is left behind.
- **Style as severity.** Line length, bracket placement, or personal preference never rank above Low.
- **Outdated rules.** Check against the version in use: `useMemo`/`useCallback` advice changes when the React Compiler is enabled, and many Node APIs now ship built-ins (`fetch`, `crypto.randomUUID`, `node:test`).
- **Fixes that do not compile.** Every "Fix" block must be valid for the language and version in the repo. If unsure, say so.
- **Flooding.** More than about 15 findings buries the critical ones. Summarize the long tail in one line.
