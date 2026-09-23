# Review Checklist

Use this as a prompt for what to look for, not a form to fill. Skip categories that cannot apply to the code under review.

## Contents
- Security (OWASP Top 10:2025)
- Correctness and edge cases
- Performance
- Maintainability
- Language and framework spot checks

## Security (OWASP Top 10:2025)

| ID | Category | What to look for in code |
|----|----------|--------------------------|
| A01 | Broken Access Control | Handlers that load a record by ID without checking the caller owns it (IDOR); admin routes guarded only in the UI; missing row-level security; SSRF via user-supplied URLs |
| A02 | Security Misconfiguration | Debug mode or verbose errors in production, permissive CORS (`*` with credentials), default credentials, missing security headers |
| A03 | Software Supply Chain Failures | Unpinned or abandoned dependencies, install scripts, lockfile drift, packages pulled from untrusted registries, CI steps that run unreviewed code |
| A04 | Cryptographic Failures | MD5/SHA-1 for passwords, homemade crypto, hard-coded keys, `Math.random()` for tokens; passwords should use Argon2id, scrypt, or bcrypt |
| A05 | Injection | String-built SQL, shell commands (`exec`, `subprocess(shell=True)`), template injection, NoSQL operator injection, XSS via raw HTML sinks, prompt injection where untrusted text reaches an LLM with tool access |
| A06 | Insecure Design | No rate limiting on login or expensive endpoints, trust in client-side checks, business logic that can be replayed or reordered |
| A07 | Authentication Failures | Session tokens in URLs or localStorage without need, missing expiry or rotation, JWT `alg: none` or unverified signatures, weak password reset flows |
| A08 | Software or Data Integrity Failures | Unsafe deserialization (`pickle`, `yaml.load`, Java serialization), unsigned webhooks, auto-updates without verification |
| A09 | Security Logging and Alerting Failures | No audit trail for sensitive actions, secrets or PII written to logs |
| A10 | Mishandling of Exceptional Conditions | Swallowed exceptions, fail-open on error (auth check throws and request proceeds), error messages that leak internals |

Also check: secrets committed to the repo (keys, tokens, `.env` contents), path traversal on file operations, and CSRF on cookie-authenticated state-changing routes.

## Correctness and edge cases

- Off-by-one, inclusive/exclusive range mistakes
- Null, undefined, empty collection, and zero handling
- Async mistakes: unawaited promises, `forEach` with async callbacks, missing error handling on rejected promises
- Races on shared state, check-then-act on files or DB rows without a transaction or lock
- Time: timezone assumptions, DST, storing local time instead of UTC, comparing dates as strings
- Money and precision: floating point for currency
- Encoding: byte length vs character length, Unicode normalization
- Resource cleanup: files, DB connections, subscriptions, timers

## Performance

- N+1 queries (a query inside a loop over query results)
- Unbounded queries or responses on user-facing paths (no `LIMIT`, no pagination)
- Missing indexes for the filter and sort columns actually used
- Work repeated per request that could be cached or computed once
- Blocking I/O on an event loop or UI thread
- Algorithmic blowups: nested loops over large inputs, repeated array scans where a map/set fits
- Frontend: oversized bundles, unnecessary client components or re-renders, images without dimensions

## Maintainability

- Duplication that will drift (the same rule in two places)
- Functions doing several unrelated things; unclear ownership of state
- Names that mislead about behavior
- Magic numbers and strings that encode business rules
- Dead code and commented-out blocks
- Missing tests for the risky path the change introduces

## Language and framework spot checks

- **TypeScript**: `any` leaking through public types, non-null assertions (`!`) hiding real nulls, unchecked `as` casts on external data (validate with a schema instead).
- **React**: effects that should be derived state or event handlers, missing `key`s, state updates on unmounted components, secrets shipped to the client bundle.
- **Next.js (App Router)**: server-only code or env vars imported into client components, Server Actions without authorization checks, caching that serves one user's data to another.
- **Python**: mutable default arguments, bare `except:`, `subprocess` with `shell=True`, missing timeouts on `requests` calls.
- **Go**: ignored errors, goroutine leaks, loop variable capture in pre-1.22 code.
- **SQL**: `SELECT *` in hot paths, implicit type casts that defeat indexes, missing transaction boundaries.
