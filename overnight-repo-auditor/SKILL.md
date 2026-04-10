---
name: overnight-repo-auditor
description: Uses Managed Agents' 14.5-hour runtime to audit an entire codebase overnight. Security, performance, accessibility, dependency issues. You wake up to a full report.
tools: Read, Grep, Glob, Bash, Agent, Write
model: inherit
---

# Overnight Repo Auditor

A production-grade autonomous codebase auditor designed for Anthropic's Managed Agents runtime (14.5-hour task horizon). You invoke this skill before leaving work. By morning, you have a comprehensive, severity-rated report covering security vulnerabilities, performance bottlenecks, accessibility violations, dependency risks, and code quality issues across your entire repository.

This skill is built for **unattended, long-running execution**. It does not ask questions. It does not pause for confirmation. It runs to completion autonomously, writing structured findings to disk as it goes, so that even if execution is interrupted, partial results are preserved.

## Architecture

```
Overnight Repo Auditor (Commander)
 |
 |-- Phase 1: Reconnaissance (sequential, ~5-10 minutes)
 |    |  Scan repo structure, identify languages, frameworks, config files
 |    |  Build a complete inventory of what exists
 |    |  Determine which audit modules are relevant
 |
 |-- Phase 2: Parallel Audit Deployment (5 specialist agents, simultaneous)
 |    |
 |    |-- Agent 1: Security Auditor
 |    |    Vulnerabilities, secrets, injection points, auth flaws, OWASP Top 10
 |    |
 |    |-- Agent 2: Performance Auditor
 |    |    N+1 queries, memory leaks, bundle size, render blocking, algorithmic complexity
 |    |
 |    |-- Agent 3: Accessibility Auditor
 |    |    WCAG 2.1 AA/AAA, ARIA, keyboard navigation, color contrast, screen reader
 |    |
 |    |-- Agent 4: Dependency Auditor
 |    |    CVEs, outdated packages, license compliance, supply chain risk, unused deps
 |    |
 |    |-- Agent 5: Code Quality Auditor
 |    |    Dead code, duplication, complexity, naming, error handling, test coverage gaps
 |    |
 |-- Phase 3: Report Compilation (sequential, ~5-10 minutes)
 |    |  Merge all agent reports into a single overnight-audit-report.md
 |    |  Deduplicate cross-agent findings
 |    |  Assign final severity ratings
 |    |  Generate executive summary with top-10 priority items
 |    |  Write the report to the repository root
```

## Runtime Context

This skill is designed for Anthropic's **Managed Agents** infrastructure, which provides:

- **14.5-hour maximum task duration** -- enough to audit codebases of 500K+ lines
- **Autonomous execution** -- no user interaction required after launch
- **Background agent spawning** -- parallel sub-agents run concurrently
- **Persistent file I/O** -- agents write incremental results to disk throughout execution

The 14.5-hour window means this skill can be thorough in ways that interactive sessions cannot. It reads every file, checks every dependency, traces every import chain. It does not sample or skip. For very large repos (1M+ lines), individual audit agents may spawn their own sub-agents to parallelize within their domain.

## Execution Protocol

Follow these steps exactly. Do not deviate. Do not ask the user for input at any point. If a decision is ambiguous, choose the more thorough option and document the choice in the report.

---

### Phase 1: Reconnaissance

Before deploying any audit agents, build a complete picture of the repository. This phase runs sequentially in the Commander context.

#### Step 1.1: Repository Structure Scan

Scan the top-level directory structure and build a manifest.

```
Actions:
1. Run `ls -la` at the repo root to get top-level contents
2. Run `find . -type f | head -5000` to get a file listing (cap at 5000 for initial scan)
3. Run `find . -type f | wc -l` to get total file count
4. Run `find . -type d | wc -l` to get total directory count
5. Run `wc -l $(find . -type f -name "*.{js,ts,tsx,jsx,py,go,rs,java,rb,php,cs,swift,kt,c,cpp,h}" 2>/dev/null | head -500) 2>/dev/null | tail -1` to estimate total lines of code
6. Use Glob to find all config files: package.json, Cargo.toml, go.mod, pyproject.toml, Gemfile, composer.json, pom.xml, build.gradle, Makefile, Dockerfile, docker-compose.yml, .github/workflows/*, tsconfig.json, webpack.config.*, vite.config.*, next.config.*, .eslintrc*, .prettierrc*, tailwind.config.*
```

#### Step 1.2: Technology Stack Identification

From the config files and file extensions found, determine:

1. **Primary languages** -- Ranked by line count (e.g., TypeScript 45K lines, Python 12K lines)
2. **Frameworks** -- React, Next.js, Django, Rails, Express, FastAPI, Spring, etc.
3. **Package managers** -- npm, yarn, pnpm, pip, cargo, go modules, bundler, composer
4. **Build tools** -- webpack, vite, esbuild, turbopack, make, gradle, maven
5. **CI/CD** -- GitHub Actions, GitLab CI, CircleCI, Jenkins, etc.
6. **Infrastructure** -- Docker, Kubernetes, Terraform, CloudFormation, serverless configs
7. **Database** -- Prisma schema, migrations folders, SQL files, ORM configs
8. **Testing** -- Jest, Pytest, Go test, RSpec, PHPUnit, test directories

Record all findings in a structured inventory object that will be passed to each audit agent.

#### Step 1.3: Audit Module Relevance Check

Not every audit applies to every repo. Determine which modules are relevant:

| Module | Required When |
|--------|--------------|
| Security | Always |
| Performance | Always |
| Accessibility | Repo contains HTML, JSX, TSX, Vue, Svelte, or template files |
| Dependency | Repo has any package manager lockfile or dependency manifest |
| Code Quality | Always |

If accessibility is not relevant (e.g., a pure backend API or CLI tool), skip that agent and note it in the final report as "Not Applicable -- no frontend components detected."

#### Step 1.4: Write Reconnaissance Report

Write a file `audit-workspace/00-reconnaissance.md` in the repo root with:

```markdown
# Reconnaissance Report
Generated: {timestamp}

## Repository Overview
- Total files: {count}
- Total directories: {count}
- Estimated lines of code: {count}
- Primary languages: {list with line counts}
- Frameworks: {list}
- Package managers: {list}

## Technology Stack
{detailed breakdown}

## Audit Plan
- Security: ACTIVE
- Performance: ACTIVE
- Accessibility: ACTIVE / NOT APPLICABLE (reason)
- Dependency: ACTIVE / NOT APPLICABLE (reason)
- Code Quality: ACTIVE

## File Inventory
{top-level directory tree}
```

This file serves as the shared context document for all audit agents.

---

### Phase 2: Parallel Audit Deployment

Deploy all relevant audit agents simultaneously using the Agent tool. Every agent call MUST use `run_in_background: true` to enable parallel execution. Send ALL agent calls in a single message.

Each agent receives:
1. The full reconnaissance report (copy the content inline -- agents do not share filesystem context automatically)
2. Their specific audit instructions (below)
3. The output file path where they must write their findings
4. The severity rating rubric

#### Severity Rating Rubric (shared across all agents)

Every finding must be rated using this rubric. Agents must use these exact labels.

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

#### Structured Finding Format (shared across all agents)

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

---

#### Agent 1: Security Auditor

**Output file**: `audit-workspace/01-security-audit.md`

**Brief to pass to the agent**:

```
You are the Security Auditor for an overnight codebase audit. You have up to 14.5 hours to complete a thorough security review. Be exhaustive, not superficial. Read every file that could contain a vulnerability. Do not sample -- inspect everything.

## Repository Context
{paste full reconnaissance report here}

## Your Mission
Conduct a comprehensive security audit of this codebase. Write all findings to: audit-workspace/01-security-audit.md

## Audit Checklist

Work through EVERY item on this checklist. For each item, document what you checked, what you found, and your assessment. If a category is not applicable, say so explicitly.

### 1. Secrets and Credentials (CRITICAL if found)
- Hardcoded API keys, tokens, passwords, or secrets in source code
- Secrets in configuration files that are not gitignored
- .env files committed to the repository
- Private keys, certificates, or keystores in the repo
- Secrets in CI/CD configuration files
- Check: .gitignore adequately covers secret files
- Check: No secrets in git history (check recent commits for patterns like password=, apiKey=, token=, secret=, AWS_SECRET, PRIVATE_KEY)
- Search patterns: grep for "password", "secret", "api_key", "apiKey", "token", "bearer", "Authorization", "AWS_ACCESS", "PRIVATE_KEY", base64-encoded strings that decode to sensitive values

### 2. Injection Vulnerabilities
- **SQL Injection**: Raw SQL queries with string concatenation or template literals. Check every database query.
- **NoSQL Injection**: Unsanitized user input in MongoDB/DynamoDB queries
- **Command Injection**: User input passed to exec(), spawn(), system(), os.system(), subprocess without sanitization
- **Path Traversal**: User input used in file paths without sanitization (../../ attacks)
- **LDAP Injection**: User input in LDAP queries
- **Template Injection**: User input rendered in server-side templates without escaping (SSTI)
- **XSS (Cross-Site Scripting)**: 
  - Reflected: User input echoed in HTML responses without encoding
  - Stored: User input saved and later rendered without encoding
  - DOM-based: document.write, innerHTML, outerHTML with user-controlled data
  - React: dangerouslySetInnerHTML with unsanitized content
- **SSRF (Server-Side Request Forgery)**: User-controlled URLs in server-side HTTP requests

### 3. Authentication and Authorization
- Authentication bypass possibilities
- Missing authentication on sensitive endpoints/routes
- Weak password policies (if password validation exists)
- Missing or weak session management
- JWT issues: weak signing algorithm (none/HS256 with weak secret), missing expiration, sensitive data in payload
- OAuth/OIDC misconfigurations: missing state parameter, open redirects in callback URLs
- Missing CSRF protection on state-changing operations
- Broken access control: horizontal privilege escalation (user A accessing user B's data), vertical privilege escalation (regular user accessing admin functions)
- Missing authorization checks on API endpoints
- IDOR (Insecure Direct Object References): sequential IDs without ownership verification

### 4. Data Exposure
- Sensitive data in logs (PII, credentials, tokens)
- Verbose error messages exposing internals (stack traces, database schemas, file paths in production)
- API responses returning more data than needed (over-fetching)
- Missing data encryption at rest for sensitive fields
- Missing TLS/HTTPS enforcement
- Sensitive data in URL query parameters (visible in logs, browser history)
- Debug endpoints or admin panels accessible in production
- GraphQL introspection enabled in production
- Source maps deployed to production

### 5. Dependency Security
- Known CVE in direct dependencies (cross-reference with Agent 4 but flag CRITICAL ones independently)
- Dependencies pulled from non-standard registries
- Lockfile integrity (lockfile exists and is consistent with manifest)
- Prototype pollution vulnerable packages

### 6. Infrastructure and Configuration Security
- Docker images running as root
- Docker images using :latest tag instead of pinned versions
- Exposed ports that should be internal
- Missing security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- CORS misconfiguration (wildcard origins, credentials with wildcard)
- Missing rate limiting on authentication endpoints
- Missing rate limiting on public APIs
- Insecure cookie settings (missing HttpOnly, Secure, SameSite)
- Permissive Content Security Policy
- Missing Subresource Integrity (SRI) on CDN scripts

### 7. Cryptography
- Use of deprecated algorithms (MD5, SHA1 for security purposes, DES, RC4)
- Weak random number generation (Math.random() for security-sensitive operations)
- Missing or weak encryption for sensitive data
- Hardcoded encryption keys or IVs
- ECB mode usage

### 8. Business Logic
- Race conditions in financial operations or inventory management
- Missing input validation on business-critical operations
- Inconsistent validation between client and server
- Missing transaction boundaries around multi-step operations
- Time-of-check to time-of-use (TOCTOU) vulnerabilities

### 9. File Upload Security (if applicable)
- Missing file type validation
- Missing file size limits
- Uploaded files accessible without authentication
- Uploaded files served from the same origin (XSS risk)
- Missing virus/malware scanning

### 10. API Security
- Missing input validation on API parameters
- Missing output encoding
- Mass assignment vulnerabilities (accepting all user-provided fields into database models)
- Missing pagination on list endpoints (denial of service via large requests)
- Verbose API error responses in production
- Missing API versioning strategy
- GraphQL: missing query depth/complexity limits, missing field-level authorization

## Output Format

Write your report as a markdown file with this structure:

# Security Audit Report
Generated: {timestamp}
Auditor: Security Agent (Overnight Repo Auditor)

## Executive Summary
- Total findings: {count}
- Critical: {count}
- High: {count}
- Medium: {count}
- Low: {count}
- {1-2 sentence overall assessment}

## Critical Findings
{findings in the structured format, ordered by impact}

## High Findings
{findings}

## Medium Findings
{findings}

## Low Findings
{findings}

## Checklist Coverage
{for each of the 10 categories above, note: CHECKED - {number of findings or "Clean"}}

## Files Reviewed
{list of all files you read during this audit}

## Methodology Notes
{any assumptions, limitations, or areas that could not be fully assessed}
```

**End of Security Auditor brief.**

---

#### Agent 2: Performance Auditor

**Output file**: `audit-workspace/02-performance-audit.md`

**Brief to pass to the agent**:

```
You are the Performance Auditor for an overnight codebase audit. You have up to 14.5 hours to complete a thorough performance review. Read source code directly -- do not rely on runtime profiling. Identify performance issues from static analysis of the code patterns, algorithms, database queries, and asset configurations.

## Repository Context
{paste full reconnaissance report here}

## Your Mission
Conduct a comprehensive performance audit of this codebase. Write all findings to: audit-workspace/02-performance-audit.md

## Severity Rating Rubric
{paste the shared severity rubric here}

## Structured Finding Format
{paste the shared finding format here}

## Audit Checklist

### 1. Database and Query Performance
- **N+1 Queries**: ORM calls inside loops. For each model/entity, trace how related data is loaded. Check for missing eager loading / includes / joins / prefetch_related.
- **Missing Indexes**: Identify columns used in WHERE clauses, JOIN conditions, ORDER BY, and GROUP BY that likely lack indexes. Check migration files and schema definitions.
- **Unbounded Queries**: SELECT * without LIMIT, or queries that could return arbitrarily large result sets.
- **Missing Pagination**: List endpoints that return all records without pagination support.
- **Expensive Aggregations**: COUNT, SUM, AVG on large tables without caching or materialized views.
- **Connection Pool Configuration**: Check database connection pool settings. Look for connection leaks (connections opened but not released in error paths).
- **Transaction Scope**: Overly broad transactions that hold locks longer than necessary. Transactions wrapping external API calls.
- **Query in Hot Paths**: Database queries inside request handlers that could be cached or precomputed.

### 2. Memory and Resource Management
- **Memory Leaks**: 
  - Event listeners added but never removed (addEventListener without removeEventListener)
  - Subscriptions not unsubscribed (RxJS, EventEmitter, WebSocket)
  - Growing arrays/maps/sets that are never cleared (caches without eviction)
  - Closures capturing large objects unnecessarily
  - React: missing cleanup in useEffect, stale closure references
- **Large Object Allocation**: Creating large arrays, buffers, or strings in hot paths
- **Stream Processing**: Reading entire files into memory instead of streaming (readFile vs createReadStream)
- **Worker/Thread Management**: Unbounded thread/worker pools, missing cleanup on process exit
- **Circular References**: Objects referencing each other preventing garbage collection

### 3. Frontend Performance (if applicable)
- **Bundle Size**:
  - Importing entire libraries when only specific functions are needed (import _ from 'lodash' vs import debounce from 'lodash/debounce')
  - Missing tree-shaking configuration
  - Large dependencies that have lighter alternatives
  - Missing code splitting / lazy loading for routes
  - Dynamic imports not used for heavy components
- **Rendering Performance**:
  - React: Missing React.memo on expensive components, missing useMemo/useCallback where re-renders are costly, inline object/array creation in JSX props, missing key props or using index as key in dynamic lists
  - Forced synchronous layouts (reading layout properties after DOM writes)
  - Layout thrashing (repeated read-write-read-write cycles)
  - Large component trees without virtualization (rendering 1000+ items without react-window/react-virtualized)
- **Asset Optimization**:
  - Unoptimized images (missing srcset, no lazy loading, no next-gen formats)
  - Missing font-display: swap or optional
  - Render-blocking CSS/JS in the critical path
  - Missing preload/prefetch for critical resources
  - Uncompressed assets (missing gzip/brotli configuration)
- **Core Web Vitals Risks**:
  - CLS (Cumulative Layout Shift): Images without dimensions, dynamically injected content above the fold, font loading causing layout shifts
  - LCP (Largest Contentful Paint): Large hero images not optimized, blocking resources in head, server response time dependencies
  - INP (Interaction to Next Paint): Long-running event handlers, heavy computation on main thread, missing debounce/throttle on input handlers

### 4. API and Network Performance
- **Waterfall Requests**: Sequential API calls that could be parallelized (await one, then await another, when they are independent)
- **Over-fetching**: API responses returning significantly more data than the client uses
- **Under-fetching**: Multiple small API calls that could be batched into one
- **Missing Caching**: 
  - API responses without Cache-Control headers
  - Repeated identical API calls without client-side caching
  - Static content served without CDN or caching headers
  - Missing ETag/Last-Modified for conditional requests
- **Missing Compression**: API responses without gzip/brotli compression
- **Missing Connection Pooling**: HTTP client creating new connections per request instead of reusing
- **Retry Logic**: Missing retry with backoff on transient failures, or retry without backoff (thundering herd)

### 5. Algorithmic Complexity
- **O(n^2) or worse in hot paths**: Nested loops over collections that grow with data. Searching unsorted arrays repeatedly.
- **String concatenation in loops**: Building strings with += in loops instead of using join or StringBuilder
- **Redundant computation**: Same expensive calculation performed multiple times when it could be cached
- **Missing memoization**: Pure functions called repeatedly with the same arguments
- **Inefficient data structures**: Using arrays for lookups instead of Sets/Maps, linear search where binary search or hash lookup is appropriate

### 6. Concurrency and Parallelism
- **Sequential async operations**: await in loops where Promise.all/Promise.allSettled would work
- **Missing concurrency limits**: Spawning unbounded parallel operations (e.g., Promise.all on 10,000 items without batching)
- **Blocking the event loop**: Synchronous file I/O, CPU-heavy computation on the main thread without worker threads
- **Missing connection pooling**: Database/HTTP connections created per-request
- **Deadlock risks**: Nested locks, circular resource dependencies

### 7. Build and Deploy Performance
- **Build configuration**: Missing production optimizations (minification, dead code elimination, source map handling)
- **Docker image size**: Multi-stage builds not used, unnecessary files in image, large base images
- **CI/CD pipeline**: Cacheable steps not cached, sequential steps that could be parallel
- **Cold start**: Serverless functions with heavy initialization, large deployment packages

### 8. Caching Strategy
- **Missing application-level caching**: Expensive computations or queries repeated without caching
- **Cache invalidation risks**: Caches without TTL, stale data risks
- **Missing HTTP caching**: Static assets without long cache times, API responses without appropriate caching headers
- **Missing CDN**: Static assets served from origin instead of CDN
- **Cache stampede risk**: Multiple requests triggering the same expensive cache rebuild simultaneously

## Output Format

# Performance Audit Report
Generated: {timestamp}
Auditor: Performance Agent (Overnight Repo Auditor)

## Executive Summary
- Total findings: {count}
- Critical: {count}
- High: {count}
- Medium: {count}
- Low: {count}
- Estimated overall performance health: GOOD / FAIR / POOR / CRITICAL
- {1-2 sentence overall assessment}

## Critical Findings
{findings in structured format}

## High Findings
{findings}

## Medium Findings
{findings}

## Low Findings
{findings}

## Performance Quick Wins
{top 5 changes that would have the biggest impact with the least effort}

## Checklist Coverage
{for each of the 8 categories above, note: CHECKED - {number of findings or "Clean"}}

## Files Reviewed
{list}

## Methodology Notes
{assumptions, limitations}
```

**End of Performance Auditor brief.**

---

#### Agent 3: Accessibility Auditor

**Output file**: `audit-workspace/03-accessibility-audit.md`

**Skip condition**: Only deploy this agent if the reconnaissance phase identified frontend files (HTML, JSX, TSX, Vue, Svelte, EJS, Handlebars, Pug, or similar template files). If skipped, write a placeholder file noting "Not Applicable."

**Brief to pass to the agent**:

```
You are the Accessibility Auditor for an overnight codebase audit. You have up to 14.5 hours to complete a thorough accessibility review against WCAG 2.1 Level AA (with Level AAA recommendations where practical). Review every component, page, and template in the codebase. Do not sample.

## Repository Context
{paste full reconnaissance report here}

## Your Mission
Conduct a comprehensive accessibility audit of this codebase. Write all findings to: audit-workspace/03-accessibility-audit.md

## Severity Rating Rubric
{paste the shared severity rubric here}

## Structured Finding Format
{paste the shared finding format here}

## Audit Checklist

### 1. Perceivable (WCAG Principle 1)

#### 1.1 Text Alternatives (WCAG 1.1)
- All `<img>` elements have meaningful alt text (not "image", "photo", "icon", or empty alt on informational images)
- Decorative images have alt="" (empty alt) or are CSS backgrounds
- Complex images (charts, diagrams) have long descriptions
- Icon-only buttons/links have accessible labels (aria-label or visually hidden text)
- SVG elements have appropriate roles and labels
- `<canvas>` elements have fallback content
- Image maps have alt text on each area
- CSS background images that convey meaning have text alternatives

#### 1.2 Time-based Media (WCAG 1.2)
- Video elements have captions track
- Audio elements have transcripts
- Auto-playing media has controls to pause/stop

#### 1.3 Adaptable (WCAG 1.3)
- Semantic HTML used correctly (headings h1-h6 in order, lists for lists, tables for tabular data)
- Heading hierarchy is logical (no skipped levels)
- Form inputs have associated labels (htmlFor/id or wrapping label)
- Fieldsets and legends for related form groups
- Tables have proper headers (th), scope attributes, and captions
- Landmark regions present and correct (header, nav, main, footer, aside)
- Only one `<main>` element per page
- Content reading order matches visual order
- Information not conveyed by color alone
- Required form fields indicated by more than just color

#### 1.4 Distinguishable (WCAG 1.4)
- **Color Contrast**: 
  - Text (normal): minimum 4.5:1 contrast ratio against background
  - Text (large, 18px+ or 14px+ bold): minimum 3:1
  - UI components and graphical objects: minimum 3:1
  - Check: text colors defined in the codebase against background colors they appear on
  - Flag: any gray-on-white or light-on-light color combinations
  - Flag: any text with opacity that reduces effective contrast
- Text is resizable to 200% without loss of content or functionality
- No images of text (use actual text with CSS styling)
- Content reflows at 320px viewport width without horizontal scrolling
- Spacing adjustable (line height, letter spacing, word spacing, paragraph spacing)
- No content that flashes more than 3 times per second

### 2. Operable (WCAG Principle 2)

#### 2.1 Keyboard Accessible (WCAG 2.1)
- All interactive elements reachable and operable by keyboard
- No keyboard traps (user can always tab away)
- Custom keyboard shortcuts documented and can be turned off
- `tabIndex` values: flag any tabIndex > 0 (disrupts natural tab order)
- `onClick` on non-interactive elements (div, span) without keyboard equivalent (onKeyDown/onKeyPress with Enter/Space handling)
- Custom components (dropdowns, modals, tabs, accordions) have proper keyboard interaction patterns per WAI-ARIA Authoring Practices
- Focus visible on all interactive elements (no outline:none without alternative focus indicator)
- Skip-to-content link present

#### 2.2 Enough Time (WCAG 2.2)
- Timeouts can be extended or disabled
- Session timeouts warn users before expiration
- Auto-updating content can be paused

#### 2.3 Seizures and Physical Reactions (WCAG 2.3)
- No content flashes more than 3 times per second
- Motion animation can be disabled (prefers-reduced-motion media query respected)

#### 2.4 Navigable (WCAG 2.4)
- Page titles are descriptive and unique
- Focus order is logical and follows visual layout
- Link text is descriptive (no "click here", "read more", "learn more" without context)
- Multiple navigation mechanisms (nav, search, sitemap)
- Headings and labels describe topic or purpose
- Focus is visible at all times

#### 2.5 Input Modalities (WCAG 2.5)
- Touch targets are at least 24x24 CSS pixels (44x44 recommended)
- Multipoint gestures have single-pointer alternatives
- Drag operations have alternative input methods

### 3. Understandable (WCAG Principle 3)

#### 3.1 Readable (WCAG 3.1)
- `<html>` element has lang attribute
- Language changes in content are marked with lang attribute
- Abbreviations are expanded on first use or have `<abbr>` with title

#### 3.2 Predictable (WCAG 3.2)
- No unexpected context changes on focus
- No unexpected context changes on input (without advance warning)
- Navigation is consistent across pages
- Components with same functionality are identified consistently

#### 3.3 Input Assistance (WCAG 3.3)
- Error messages are descriptive and suggest corrections
- Labels or instructions provided for user input
- Error prevention on legal/financial/data-deletion actions (confirm, review, undo)
- Form validation errors associated with their fields (aria-describedby or aria-errormessage)
- Required fields indicated in labels (not just with asterisk alone)
- Autocomplete attributes on common form fields (name, email, address, etc.)

### 4. Robust (WCAG Principle 4)

#### 4.1 Compatible (WCAG 4.1)
- Valid HTML (no duplicate IDs, proper nesting, correct ARIA usage)
- ARIA roles, states, and properties used correctly
- No ARIA that conflicts with native HTML semantics
- Custom components have required ARIA attributes per their role
- Status messages use aria-live regions appropriately
- Dynamic content updates communicated to assistive technology

### 5. ARIA Usage Audit
- aria-label not used on elements that already have visible text (use aria-labelledby instead or remove)
- aria-hidden="true" not used on focusable elements
- role="presentation" or role="none" not used on elements with focusable children
- aria-expanded, aria-selected, aria-checked states correctly toggled
- aria-live regions used appropriately (polite vs assertive)
- No redundant ARIA (e.g., role="button" on a `<button>`)

### 6. Component-Specific Patterns
For each of these component types found in the codebase, verify the WAI-ARIA Authoring Practices pattern is implemented:
- **Modal Dialogs**: focus trap, Escape to close, focus returns to trigger, aria-modal, role="dialog"
- **Tabs**: arrow key navigation, proper role="tablist"/"tab"/"tabpanel", aria-selected
- **Dropdown Menus**: arrow key navigation, Escape to close, proper role="menu"/"menuitem"
- **Accordions**: Enter/Space to toggle, proper aria-expanded, aria-controls
- **Carousels**: pause controls, proper role and navigation
- **Toast Notifications**: aria-live region, not auto-dismissing too quickly
- **Forms**: error summary with links to fields, inline validation announcements

## Output Format

# Accessibility Audit Report
Generated: {timestamp}
Auditor: Accessibility Agent (Overnight Repo Auditor)
Standard: WCAG 2.1 Level AA (with Level AAA recommendations)

## Executive Summary
- Total findings: {count}
- Critical: {count}
- High: {count}
- Medium: {count}
- Low: {count}
- WCAG Conformance Level: DOES NOT CONFORM / PARTIALLY CONFORMS / CONFORMS (Level AA)
- {1-2 sentence overall assessment}

## Critical Findings
{findings}

## High Findings
{findings}

## Medium Findings
{findings}

## Low Findings
{findings}

## WCAG Criterion Coverage
{for each WCAG criterion checked, note: PASS / FAIL (n issues) / NOT APPLICABLE}

## Accessibility Quick Wins
{top 5 changes that would have the biggest impact for users with disabilities}

## Component Audit Results
{for each component type found, note the ARIA pattern compliance status}

## Files Reviewed
{list}

## Methodology Notes
{assumptions, limitations}
```

**End of Accessibility Auditor brief.**

---

#### Agent 4: Dependency Auditor

**Output file**: `audit-workspace/04-dependency-audit.md`

**Skip condition**: Only deploy if the reconnaissance phase identified package manager manifests (package.json, Cargo.toml, go.mod, requirements.txt, pyproject.toml, Gemfile, composer.json, pom.xml, build.gradle). If no dependencies exist, write a placeholder noting "Not Applicable."

**Brief to pass to the agent**:

```
You are the Dependency Auditor for an overnight codebase audit. You have up to 14.5 hours to conduct a thorough analysis of all project dependencies. Review every dependency manifest, lockfile, and assess the health and risk profile of the entire dependency tree.

## Repository Context
{paste full reconnaissance report here}

## Your Mission
Conduct a comprehensive dependency audit of this codebase. Write all findings to: audit-workspace/04-dependency-audit.md

## Severity Rating Rubric
{paste the shared severity rubric here}

## Structured Finding Format
{paste the shared finding format here}

## Audit Checklist

### 1. Security Vulnerabilities (CVEs)
- Run `npm audit` / `yarn audit` / `pnpm audit` if Node.js project
- Run `pip audit` or `safety check` if Python project (install if needed, or analyze requirements manually)
- Run `cargo audit` if Rust project
- Run `go vuln` or `govulncheck` if Go project
- Run `bundle audit` if Ruby project
- If automated tools are not available, manually check dependency versions against known CVE databases
- For each vulnerability found:
  - CVE ID and description
  - Affected package and version
  - Fixed version (if available)
  - Is the vulnerable code path actually used in this project? (reduces false positives)
  - CVSS score if available
  - Is there a known exploit in the wild?

### 2. Outdated Dependencies
- Compare current versions against latest available versions
- Flag: major version behind (potentially breaking changes needed)
- Flag: more than 6 months behind latest release
- Flag: dependencies that are no longer maintained (last commit > 2 years ago, archived repo)
- Prioritize: dependencies with security implications (auth libraries, crypto, HTTP clients)
- For each outdated dependency:
  - Current version vs latest version
  - Changelog summary of what changed (major items)
  - Breaking changes that would affect this project
  - Estimated upgrade effort (trivial/moderate/significant)

### 3. License Compliance
- Identify license for every direct dependency
- Flag: copyleft licenses (GPL, AGPL, LGPL) in projects that appear to be proprietary/commercial
- Flag: no license specified (legally risky -- default copyright applies)
- Flag: license incompatibilities (e.g., mixing GPL and MIT in ways that could cause issues)
- Flag: SSPL, Commons Clause, or other non-OSI-approved licenses
- Generate a license summary table:
  | Package | Version | License | Risk Level |

### 4. Supply Chain Risk
- Flag: packages with very few weekly downloads (< 100/week) that are not internal
- Flag: packages maintained by a single individual with no organizational backing
- Flag: packages that were recently transferred to new owners (name squatting risk)
- Flag: packages with install scripts (preinstall/postinstall) that execute arbitrary code
- Flag: packages pulling from non-standard registries
- Check: lockfile exists and is committed (prevents supply chain attacks via version ranges)
- Check: lockfile integrity (sha hashes present where supported)
- Flag: dependencies using git URLs instead of registry packages (no integrity verification)

### 5. Unused Dependencies
- Scan the codebase for import/require statements and cross-reference with declared dependencies
- Flag: dependencies declared in manifest but never imported (increase attack surface unnecessarily)
- Flag: devDependencies that appear in production bundles
- Flag: peerDependencies with incorrect version ranges
- Note: some dependencies are used in config files, scripts, or CLI tools rather than source imports -- check those paths before flagging as unused

### 6. Dependency Weight and Alternatives
- Identify the heaviest dependencies (by install size / bundle impact)
- For each heavy dependency, assess: is the full library needed, or is only a small feature used?
- Suggest lighter alternatives where available (e.g., date-fns instead of moment, got instead of axios+interceptors for simple use)
- Check for dependencies that overlap in functionality (e.g., both lodash and underscore, both axios and node-fetch)

### 7. Dependency Configuration
- Check lockfile version and consistency with the package manager version
- Check for resolution overrides / forced versions (may mask real version conflicts)
- Check node_modules / vendor directory is gitignored
- Check for peer dependency warnings
- Check engine constraints (e.g., node version specified in package.json)
- Check for workspace/monorepo configuration issues (if applicable)

### 8. Transitive Dependency Risks
- Identify transitive dependencies (deps of deps) with known CVEs
- Identify deeply nested transitive deps that are very outdated
- Calculate total dependency count (direct + transitive)
- Flag unusually deep dependency trees (potential bloat)

## Output Format

# Dependency Audit Report
Generated: {timestamp}
Auditor: Dependency Agent (Overnight Repo Auditor)

## Executive Summary
- Direct dependencies: {count}
- Transitive dependencies: {count}
- Total dependency count: {count}
- Known vulnerabilities (CVEs): {count by severity}
- Outdated dependencies: {count}
- License issues: {count}
- Unused dependencies: {count}
- {1-2 sentence overall assessment}

## Critical Findings (CVEs with known exploits, license violations)
{findings}

## High Findings (High-severity CVEs, severely outdated deps)
{findings}

## Medium Findings (Medium CVEs, moderately outdated, license concerns)
{findings}

## Low Findings (Low CVEs, minor updates, weight optimization)
{findings}

## License Summary
| Package | Version | License | Risk |
|---------|---------|---------|------|
{for every direct dependency}

## Outdated Dependencies
| Package | Current | Latest | Behind By | Breaking Changes | Priority |
|---------|---------|--------|-----------|-----------------|----------|
{for each outdated dependency}

## Unused Dependencies
{list with evidence}

## Upgrade Roadmap
{prioritized list of dependency upgrades, grouped by effort level}
1. Immediate (security fixes, drop-in replacements)
2. This sprint (minor version bumps, small API changes)
3. This quarter (major version bumps, significant migration)
4. Evaluate (consider replacing with alternatives)

## Checklist Coverage
{for each of the 8 categories, note: CHECKED - {count of findings or "Clean"}}

## Files Reviewed
{list of manifest and lockfiles reviewed}

## Methodology Notes
{tools used, limitations, packages that could not be assessed}
```

**End of Dependency Auditor brief.**

---

#### Agent 5: Code Quality Auditor

**Output file**: `audit-workspace/05-code-quality-audit.md`

**Brief to pass to the agent**:

```
You are the Code Quality Auditor for an overnight codebase audit. You have up to 14.5 hours to conduct a thorough code quality review. Focus on maintainability, readability, correctness, and engineering best practices. This is not a style guide review -- focus on substantive quality issues that affect the team's ability to maintain and extend this codebase.

## Repository Context
{paste full reconnaissance report here}

## Your Mission
Conduct a comprehensive code quality audit of this codebase. Write all findings to: audit-workspace/05-code-quality-audit.md

## Severity Rating Rubric
{paste the shared severity rubric here}

## Structured Finding Format
{paste the shared finding format here}

## Audit Checklist

### 1. Dead Code and Unused Exports
- Exported functions/classes/constants that are never imported anywhere in the codebase
- Unreachable code after return/throw/break/continue statements
- Commented-out code blocks (more than 5 lines)
- Unused variables and parameters (especially in function signatures)
- Feature flags or conditional blocks that are permanently enabled/disabled
- Entire files that are not imported or referenced anywhere
- Unused CSS classes/styles (if stylesheets exist)
- Unused test utilities or fixtures
- TODO/FIXME/HACK/XXX comments older than 6 months (check git blame for age)

### 2. Code Duplication
- Functions or methods that are substantially identical (>80% similar) across different files
- Copy-pasted logic that should be extracted into a shared utility
- Similar data transformation logic repeated in multiple places
- Duplicate type definitions or interfaces
- Repeated validation logic that could be centralized
- Similar error handling patterns that could be abstracted
- Note: some duplication is acceptable (test setup, simple patterns). Focus on non-trivial duplicated logic (10+ lines).

### 3. Complexity and Readability
- **Cyclomatic Complexity**: Functions with more than 10 branches (if/else/switch/ternary/&&/||)
- **Cognitive Complexity**: Deeply nested code (3+ levels of nesting), especially nested conditionals
- **Function Length**: Functions over 50 lines (flag at 50, strongly flag at 100+)
- **File Length**: Files over 500 lines (flag at 500, strongly flag at 1000+)
- **Parameter Count**: Functions with more than 4 parameters (suggest object parameter pattern)
- **Return Complexity**: Functions with more than 3 return statements, or unclear return types
- **Boolean Parameter Anti-pattern**: Functions that take boolean flags to switch behavior (should be split into separate functions)
- **Nested Callbacks/Promises**: Callback hell or deeply nested .then() chains that should use async/await
- **Magic Numbers/Strings**: Hardcoded values that should be named constants

### 4. Error Handling
- **Empty catch blocks**: catch(e) {} with no logging or re-throwing
- **Generic catch-all**: Catching all exceptions without differentiation (catch Exception, catch(e))
- **Missing error handling**: async operations without try/catch or .catch()
- **Swallowed errors**: Errors caught and logged but not propagated when they should be
- **Missing error boundaries**: React components without error boundaries around complex subtrees
- **Inconsistent error formats**: Different error response shapes across API endpoints
- **Missing validation**: Function inputs not validated (especially public API boundaries)
- **Silent failures**: Operations that fail without any indication to the caller
- **Missing finally blocks**: Resource cleanup that could be skipped on error paths (file handles, connections, locks)

### 5. Type Safety (for typed languages)
- **Any/unknown overuse**: TypeScript `any` types that could be properly typed
- **Type assertions**: as SomeType casts that bypass type checking (especially `as any`)
- **Missing null checks**: Nullable values accessed without guards
- **Inconsistent types**: Same data represented by different types in different parts of the codebase
- **Missing generics**: Functions that lose type information by using broad types where generics would preserve it
- **Enum misuse**: String enums where union types would be better, or vice versa
- **Missing discriminated unions**: Complex conditional logic that could be replaced with discriminated union types

### 6. Architecture and Design Patterns
- **Circular dependencies**: Modules that import from each other (directly or transitively)
- **God objects/files**: Files that are imported by >20 other files (high coupling)
- **Violation of separation of concerns**: Business logic in UI components, database queries in route handlers, etc.
- **Missing abstraction layers**: Direct database calls from route handlers without a service/repository layer
- **Inconsistent patterns**: Some endpoints use controllers, others use inline handlers. Some use DTOs, others pass raw objects.
- **Missing dependency injection**: Hard-coded dependencies that make testing difficult
- **Global mutable state**: Singletons, global variables, or module-level mutable state that could cause issues in concurrent/test environments
- **Missing interfaces/contracts**: Public APIs without clear type contracts

### 7. Testing Gaps
- **Missing test files**: Source files with no corresponding test file
- **Test coverage distribution**: Which parts of the codebase have tests and which do not?
- **Test quality issues**: Tests that only test happy paths, missing edge cases
- **Tests without assertions**: Test functions that call code but never assert on the result
- **Flaky test indicators**: Tests depending on timing, network, or external state
- **Missing integration tests**: Only unit tests exist, or only E2E tests exist, with no middle ground
- **Test data management**: Hardcoded test data that drifts from reality, missing factories/fixtures
- **Missing mocks**: Tests making real network/database calls when they should be mocked

### 8. Documentation and Developer Experience
- **Missing README or outdated README**: No setup instructions, or instructions that no longer work
- **Missing or misleading comments**: Comments that describe what code does rather than why, or comments that contradict the code
- **Missing JSDoc/docstrings on public APIs**: Exported functions without documentation
- **Missing environment variable documentation**: .env.example missing, or not documenting all required variables
- **Missing contribution guidelines**: No CONTRIBUTING.md or equivalent for multi-developer projects
- **Missing or broken scripts**: package.json scripts that don't work, Makefile targets that are stale

### 9. Naming and Conventions
- **Inconsistent naming patterns**: mixedCase and snake_case in the same language, or plural/singular inconsistency in file names
- **Misleading names**: Variables or functions whose names do not match their behavior
- **Abbreviated names**: Single-letter variables or heavily abbreviated names outside of small scopes (loop indices are fine)
- **Boolean naming**: Boolean variables not named as predicates (is*, has*, should*, can*)
- **File organization**: No clear pattern for where new files should be created

### 10. Correctness Risks
- **Race conditions**: Shared mutable state accessed from async operations without synchronization
- **Floating point comparison**: Comparing floats with === instead of epsilon-based comparison
- **Integer overflow**: Arithmetic on large numbers without BigInt (JavaScript) or appropriate types
- **Timezone handling**: Date/time operations without explicit timezone handling
- **Unicode handling**: String operations that assume ASCII (length, substring, regex without unicode flag)
- **Off-by-one errors**: Array bounds, pagination calculations, date range calculations
- **Null coalescing pitfalls**: Using || instead of ?? (treating 0, "", false as nullish)
- **Promise handling**: Promises created but never awaited (floating promises)

## Output Format

# Code Quality Audit Report
Generated: {timestamp}
Auditor: Code Quality Agent (Overnight Repo Auditor)

## Executive Summary
- Total findings: {count}
- Critical: {count}
- High: {count}
- Medium: {count}
- Low: {count}
- Overall code health: EXCELLENT / GOOD / FAIR / POOR / CRITICAL
- Tech debt estimate: LOW / MODERATE / HIGH / SEVERE
- {1-2 sentence overall assessment}

## Critical Findings
{findings}

## High Findings
{findings}

## Medium Findings
{findings}

## Low Findings
{findings}

## Code Health Metrics
- Estimated dead code: {percentage or line count}
- Files over 500 lines: {count and list}
- Functions over 50 lines: {count}
- Average cyclomatic complexity: {estimate}
- Test coverage estimate: {percentage of source files with corresponding test files}
- Circular dependency chains: {count and list}

## Top Refactoring Priorities
{ranked list of the 10 highest-impact refactoring opportunities, with estimated effort}

## Checklist Coverage
{for each of the 10 categories, note: CHECKED - {count of findings or "Clean"}}

## Files Reviewed
{list}

## Methodology Notes
{assumptions, limitations}
```

**End of Code Quality Auditor brief.**

---

### Phase 3: Report Compilation

After ALL audit agents have completed (all background agents have returned), the Commander compiles the final report. This phase runs sequentially in the Commander context.

#### Step 3.1: Read All Agent Reports

Read each report file:
- `audit-workspace/00-reconnaissance.md`
- `audit-workspace/01-security-audit.md`
- `audit-workspace/02-performance-audit.md`
- `audit-workspace/03-accessibility-audit.md` (if generated)
- `audit-workspace/04-dependency-audit.md` (if generated)
- `audit-workspace/05-code-quality-audit.md`

#### Step 3.2: Deduplicate Cross-Agent Findings

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

#### Step 3.3: Generate Executive Summary

Create a top-level summary that a CTO or engineering lead can read in 2 minutes:

1. **Overall Health Score**: Combine findings across all agents into a single assessment (A through F, with description)
2. **Top 10 Priority Items**: The 10 most impactful findings across all categories, ranked by severity and ease of fix
3. **Risk Areas**: Which parts of the codebase have the most issues?
4. **Positive Observations**: What the codebase does well (always include at least 2-3 positive notes)
5. **Recommended Sprint Plan**: Group the top priorities into an actionable sprint plan

#### Step 3.4: Write the Final Report

Write the compiled report to `overnight-audit-report.md` in the repository root.

**Final report structure**:

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

#### Step 3.5: Final Summary to User

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

---

## Error Handling

This skill is designed for autonomous execution. Errors must be handled without user interaction.

### Agent Failure

If an audit agent fails to complete or returns an error:

1. **Retry once**: Re-deploy the agent with the same brief
2. **If retry fails**: Write a partial report noting the failure
3. **Continue with other agents**: Never let one agent's failure block the others
4. **Document in final report**: Note which agents failed and what coverage was lost

### File Access Errors

If a file cannot be read (permissions, binary file, etc.):

1. Skip the file
2. Log it in the agent's "Methodology Notes" section
3. Continue with remaining files

### Timeout Management

The 14.5-hour window is generous, but for very large codebases:

1. Each agent should prioritize high-risk files first (auth, payments, data handling, public endpoints)
2. If an agent detects it has reviewed >2000 files, it should note that a sampling strategy was used for lower-risk files
3. The Commander should monitor agent completion and compile partial results if the window is closing

### Disk Space

All reports are markdown text files. Total output is typically under 1MB even for large audits. If the audit-workspace directory already exists from a previous run, the new audit will overwrite it.

---

## Scaling Behavior

| Codebase Size | Estimated Duration | Agent Strategy |
|---------------|-------------------|----------------|
| < 10K lines | 15-30 minutes | All 5 agents, single pass each |
| 10K - 50K lines | 30-90 minutes | All 5 agents, thorough pass |
| 50K - 200K lines | 1-4 hours | All 5 agents, may need sub-agents for Security and Code Quality |
| 200K - 500K lines | 4-8 hours | All agents spawn 2-3 sub-agents each to parallelize file review |
| 500K+ lines | 8-14 hours | Full sub-agent deployment with file-batch assignments per sub-agent |

For codebases over 200K lines, each audit agent should spawn sub-agents to parallelize:

```
Security Agent
 |-- Sub-agent: Auth & Sessions (auth/, middleware/, login/*)
 |-- Sub-agent: Data Handling (models/, schemas/, migrations/*)
 |-- Sub-agent: API Surface (routes/, controllers/, handlers/*)
 |-- Sub-agent: Infrastructure (Dockerfile, CI/CD, configs)
```

The agent briefs above instruct agents to self-organize sub-agent deployment based on the repository size discovered during their audit.

---

## Invocation Examples

### Basic Usage
```
User: "Run an overnight audit on this repo"
```
The skill runs the full protocol: recon, deploy 5 parallel agents, compile report.

### Targeted Audit
```
User: "Run an overnight audit, but focus on security and dependencies only"
```
The Commander deploys only the Security and Dependency agents (skipping Performance, Accessibility, and Code Quality). The final report only includes those two sections.

### Repeat Audit
```
User: "Re-run the overnight audit, the code has changed since last time"
```
The skill overwrites the previous audit-workspace directory and overnight-audit-report.md with fresh results. Previous results are not preserved (the user should commit or copy them first if needed).

---

## Important Notes

- This skill does NOT modify any source code. It is read-only. The only files it creates are in the `audit-workspace/` directory and the `overnight-audit-report.md` file.
- This skill does NOT run tests, build the project, or execute any project code. It performs static analysis only.
- Exception: the Dependency Auditor may run `npm audit`, `pip audit`, or similar package manager audit commands, which are read-only operations that query vulnerability databases.
- If the repository contains sensitive code (proprietary algorithms, security infrastructure), the audit reports will contain descriptions of that code. Treat the reports with the same sensitivity as the source code itself.
- The `audit-workspace/` directory should be added to `.gitignore` to prevent accidentally committing audit reports. The skill will suggest this if `.gitignore` exists but does not include the directory.
