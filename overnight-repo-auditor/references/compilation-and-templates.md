# Phase 3: Compilation and Output Templates

Run sequentially in the Commander context after ALL audit agents have completed (all background agents have returned).

## Step 3.1: Read All Agent Reports

Read each report file:
- `audit-workspace/00-reconnaissance.md`
- `audit-workspace/01-security-audit.md`
- `audit-workspace/02-performance-audit.md`
- `audit-workspace/03-accessibility-audit.md` (if generated)
- `audit-workspace/04-dependency-audit.md` (if generated)
- `audit-workspace/05-code-quality-audit.md`

## Step 3.2: Deduplicate Cross-Agent Findings

Certain issues will be flagged by multiple agents. Common overlaps:

| Finding Type | Agents That May Flag It |
|--------------|------------------------|
| Known CVE in dependency | Security + Dependency |
| Missing input validation | Security + Code Quality |
| N+1 queries | Performance + Code Quality |
| Missing error handling | Security + Code Quality |
| Large bundle size | Performance + Dependency (heavy deps) |
| Missing alt text | Accessibility + Code Quality |

For each duplicate:
1. Keep the more detailed finding
2. Add a cross-reference note: "Also flagged by {other agent} -- see {section}"
3. Use the higher severity rating if they differ
4. Do not double-count in the total

## Step 3.3: Generate Executive Summary

Create a top-level summary that a CTO or engineering lead can read in 2 minutes:

1. **Overall Health Score**: Combine findings across all agents into a single assessment (A through F, with description)
2. **Top 10 Priority Items**: The 10 most impactful findings across all categories, ranked by severity and ease of fix
3. **Risk Areas**: Which parts of the codebase have the most issues?
4. **Positive Observations**: What the codebase does well (always include at least 2-3 positive notes)
5. **Recommended Sprint Plan**: Group the top priorities into an actionable sprint plan

## Step 3.4: Write the Final Report

Write the compiled report to `overnight-audit-report.md` in the repository root using this structure:

```markdown
# Overnight Codebase Audit Report

**Repository**: {repo name}
**Generated**: {date and time}
**Audit Duration**: {time from start to finish}
**Auditor**: Overnight Repo Auditor (Claude Code Skill)
**Runtime**: Anthropic Managed Agents (14.5-hour task horizon)

---

## Executive Summary

### Overall Health: {A/B/C/D/F} - {one-line description}

| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Security | {n} | {n} | {n} | {n} | {n} |
| Performance | {n} | {n} | {n} | {n} | {n} |
| Accessibility | {n} | {n} | {n} | {n} | {n} |
| Dependencies | {n} | {n} | {n} | {n} | {n} |
| Code Quality | {n} | {n} | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}** |

### Top 10 Priority Items

{numbered list with severity badge, title, category, and one-line description}

### Positive Observations

{what the codebase does well}

### Recommended Action Plan

#### Immediate (this week)
{critical and high items that are quick to fix}

#### This Sprint
{remaining high items and impactful medium items}

#### This Quarter
{medium items and strategic improvements}

#### Backlog
{low items and nice-to-haves}

---

## Detailed Findings by Category

### Security Audit
{full content from 01-security-audit.md, with deduplication notes}

### Performance Audit
{full content from 02-performance-audit.md, with deduplication notes}

### Accessibility Audit
{full content from 03-accessibility-audit.md, or "Not Applicable" note}

### Dependency Audit
{full content from 04-dependency-audit.md, or "Not Applicable" note}

### Code Quality Audit
{full content from 05-code-quality-audit.md, with deduplication notes}

---

## Repository Overview
{content from 00-reconnaissance.md}

---

## Audit Metadata

### Configuration
- Agents deployed: {count}
- Audit modules: {list of active modules}
- WCAG standard: 2.1 Level AA
- Severity rubric: 4-tier (Critical/High/Medium/Low)

### Methodology
This audit was conducted through static analysis of the source code by specialized AI agents running in parallel. Each agent independently reviewed the codebase against a comprehensive checklist specific to its domain. Findings were then compiled, deduplicated, and severity-rated by the Commander agent.

### Limitations
- This is a static analysis audit. Runtime behavior, actual performance metrics, and real-user accessibility testing are not covered.
- Dependency vulnerability data is current as of the audit date. New CVEs may be disclosed after this report.
- Code paths that require specific runtime conditions or environment variables to reach may not be fully analyzed.
- This audit does not replace professional penetration testing, performance load testing, or accessibility testing with assistive technology users.

### Files
- Reconnaissance: audit-workspace/00-reconnaissance.md
- Security audit: audit-workspace/01-security-audit.md
- Performance audit: audit-workspace/02-performance-audit.md
- Accessibility audit: audit-workspace/03-accessibility-audit.md
- Dependency audit: audit-workspace/04-dependency-audit.md
- Code quality audit: audit-workspace/05-code-quality-audit.md
- This report: overnight-audit-report.md
```

## Step 3.5: Final Summary to User

After writing the report, output a brief completion message:

```
Overnight audit complete.

Report: overnight-audit-report.md
Individual reports: audit-workspace/

Summary:
- Overall health: {grade}
- Total findings: {n} ({critical} critical, {high} high, {medium} medium, {low} low)
- Top priority: {title of #1 finding}

The full report with all findings, evidence, and recommendations is in overnight-audit-report.md.
```
