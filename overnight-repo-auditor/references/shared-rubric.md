# Shared Rubric and Finding Format

Pass both of these blocks verbatim to every audit agent brief, alongside the reconnaissance report.

## Severity Rating Rubric

Rate every finding using this rubric. Use these exact labels.

```
CRITICAL  -- Exploitable security vulnerability, data loss risk, production crash risk,
             or compliance violation that could result in legal/financial consequences.
             Requires immediate remediation before next deploy.
             Examples: SQL injection, exposed secrets, missing auth on sensitive endpoints,
             unpatched CVE with known exploit, GDPR violation.

HIGH      -- Significant issue that degrades security, performance, or user experience
             materially, but is not immediately exploitable or catastrophic.
             Should be addressed within the current sprint.
             Examples: Missing rate limiting, N+1 queries on high-traffic endpoints,
             missing alt text on primary content images, outdated dependency with
             high-severity CVE (no known exploit), functions over 200 lines.

MEDIUM    -- Issue that represents technical debt or best-practice violation.
             Does not cause immediate harm but will compound over time.
             Should be addressed within the current quarter.
             Examples: Missing error boundaries, console.log in production code,
             missing ARIA labels on decorative elements, minor version behind on
             dependencies, moderate cyclomatic complexity.

LOW       -- Minor improvement opportunity. Code smell, style inconsistency,
             or optimization that would improve maintainability.
             Address when touching the relevant code.
             Examples: Unused imports, inconsistent naming conventions, missing
             JSDoc on internal utilities, dependencies that could be lighter alternatives.
```

## Structured Finding Format

Every individual finding must follow this format:

```markdown
### [SEVERITY] Finding Title
- **File**: path/to/file.ts (lines 45-67)
- **Category**: {agent-specific category, e.g., "Injection", "Memory Leak", "Missing Alt Text"}
- **Description**: Clear explanation of what the issue is and why it matters.
- **Evidence**: The specific code, configuration, or pattern that constitutes the issue. Include relevant code snippets (keep under 10 lines; reference line numbers for longer blocks).
- **Impact**: What happens if this is not fixed. Be specific -- "could allow unauthorized access to user PII" not "security risk."
- **Recommendation**: Specific, actionable fix. Include code examples when helpful.
- **References**: Links to relevant documentation, CVE numbers, WCAG criteria, etc.
```
