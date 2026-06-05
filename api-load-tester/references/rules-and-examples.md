# Rules, Error Handling, and Examples

## Safety and Conduct Rules

1. **Never test production endpoints without explicit user confirmation.** If the environment is "prod" or the URL contains "prod", "production", or appears to be a production domain, warn the user and ask for confirmation before proceeding.
2. **Respect rate limits.** If 429 responses are detected, reduce concurrency and note the rate limit. Do not continue hammering an endpoint that is returning 429s.
3. **Handle authentication carefully.** Never log or include full auth tokens. Mask them (e.g., "Bearer eyJ...****").
4. **No destructive testing by default.** Only test GET endpoints by default. For POST/PUT/DELETE, confirm the endpoint is safe to call repeatedly (idempotent, uses a test database, or has no side effects).
5. **Clean up temporary files.** Store raw results in a clearly named temp directory but do not delete them automatically; the user may want to inspect them.
6. **Report in consistent units.** Use milliseconds for latency, requests/second for throughput, and percentages for error rates. Always label units.
7. **ASCII charts are mandatory in the output.** Even though approximate, they give immediate visual understanding without external tools.
8. **Test from the same machine consistently.** Do not distribute load across machines unless the user specifically asks for distributed testing.
9. **Timeouts count as failures.** A timed-out request is a failed request, not excluded from the data.
10. **Do not extrapolate beyond tested ranges.** The scaling projections table must clearly mark projected values vs observed values.

## Error Handling

- If a tool installation fails, fall back to the next tool in the priority list. If all preferred tools fail, use the curl fallback.
- If an endpoint becomes completely unresponsive during testing (100% timeout for 30+ seconds), stop testing that endpoint at that concurrency level and move to the next stage or endpoint. Note this in the output as "endpoint became unresponsive."
- If the machine runs out of file descriptors or hits OS-level connection limits, detect the error message, surface it, and suggest increasing `ulimit -n` before retrying.
- If the run is interrupted (Ctrl+C or timeout), save whatever data has been collected so far and generate a partial output clearly marked as incomplete.

## Example Invocations

**Simple single endpoint**:
```
Load test https://api.example.com/health
Expected response time: p95 < 200ms
Concurrent users: up to 100
```

**Multiple endpoints with auth**:
```
Endpoints:
  - GET https://api.example.com/users (Bearer token: abc123)
  - POST https://api.example.com/search (Bearer token: abc123, body: {"query": "test"})
Expected: p95 < 300ms
Concurrency: 10 to 500
Environment: staging
```

**Quick smoke test**:
```
Quick load test https://api.example.com/health with 50 concurrent users
```

For quick/smoke tests, reduce to 3 stages: baseline (1), target concurrency (50), and 2x target (100). Shorten duration to 5 seconds per stage.
