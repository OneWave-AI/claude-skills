---
name: static-analysis-sweep
description: Use to run real static analysis over a diff or repo before shipping — Semgrep, CodeQL, secret scanning, dependency CVEs — and triage the findings into what must be fixed now versus noise. Trigger before a release or PR merge, during a security review, or when the user asks to scan the code for vulnerabilities.
tools: Read, Write, Edit, Bash, Glob, Grep
---

# Static Analysis Sweep

Reading code for bugs finds what you thought to look for. A scanner finds the rest. This skill runs the tools, then does the part the tools cannot: deciding which findings are real.

## Core Behavior

Scan the diff first, the repo second. Triage every finding. Never hand over a raw scanner dump — an unfiltered report is how real findings get ignored.

## The Tools

**Semgrep** — fast, pattern-based, good defaults, no build required.

```bash
semgrep --config=auto --error --quiet .                    # whole repo
semgrep --config=auto --quiet --baseline-commit=origin/main # diff only
```

**Secret scanning** — the highest-value scan per second spent.

```bash
gitleaks detect --no-banner --redact
git log -p -S'BEGIN PRIVATE KEY' --oneline | head
```

**Dependency CVEs**

```bash
npm audit --audit-level=high 2>&1 | tail -40
pip-audit 2>&1 | tail -40
```

**CodeQL** — deeper, needs a build, worth it on a release branch rather than every PR.

```bash
codeql database create db --language=javascript --overwrite
codeql database analyze db --format=sarif-latest --output=results.sarif
```

If a tool is not installed, say so and run what is available rather than silently skipping the whole sweep.

## Triage

Every finding lands in one of four buckets:

**Fix now** — reachable from untrusted input and causes real damage: injection into a query or shell, authentication or authorization bypass, secrets in the repo, deserialization of user data, path traversal, SSRF against internal hosts.

**Fix soon** — real weakness, limited blast radius: missing rate limit, weak crypto choice, permissive CORS on a non-sensitive route, a dependency CVE with no exploit path.

**Won't fix, explained** — the pattern matched, the exploit does not exist here. Write the one-line reason. This is the bucket that earns trust in the report.

**Noise** — test fixtures, generated files, vendored code. Suppress with a targeted ignore, never by turning the rule off globally.

For each Fix-now item, prove reachability before claiming it: name the entry point, the path the data takes, and the sink. A finding you cannot trace is Fix-soon at best.

## Secrets

If a live credential is found in the working tree or in history, stop and tell the user immediately. Rotation comes first — scrubbing history on a key that is still valid protects nothing. Never print the secret back in full.

## Report Format

```markdown
## Scan — <scope> — <date>
Tools: <which ran, which were unavailable>

### Fix now (n)
1. **<issue>** — `file:line`
   Path: <entry point> → <sink>
   Fix: <the concrete change>

### Fix soon (n)
- <issue> — `file:line` — <why it is limited>

### Reviewed, not an issue (n)
- <finding> — <why it does not apply here>
```

Ranked by severity, not by file order. If nothing real was found, say that in one line — a clean scan is a result, and padding it with non-issues makes the next report unreadable.
