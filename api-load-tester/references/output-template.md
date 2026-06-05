# Output Template

Create the file `api-load-report.md` in the current working directory using this exact structure.

```markdown
# API Load Test Report

**Date**: <YYYY-MM-DD HH:MM:SS timezone>
**Environment**: <prod/staging/dev or as specified>
**Tool**: <hey/wrk/ab/curl>
**Test Duration**: <total wall-clock time>

---

## Executive Summary

<2-3 sentences summarizing the overall findings. State the key throughput number, the breaking point, and the most critical recommendation.>

---

## Endpoints Tested

| # | Method | URL | Auth | Payload |
|---|--------|-----|------|---------|
| 1 | GET | https://... | Bearer | N/A |
| 2 | POST | https://... | Bearer | JSON (245 bytes) |

---

## Test Configuration

- **Concurrency stages**: <list of concurrency levels>
- **Duration per stage**: <seconds>
- **Total requests per stage**: <number>
- **Request timeout**: <seconds>
- **Success criteria**: <status codes>
- **Ramp pattern**: <step/linear/spike>

---

## Results by Endpoint

### Endpoint 1: <METHOD> <URL>

#### Latency Percentiles (ms)

| Concurrency | p50 | p75 | p90 | p95 | p99 | Max |
|-------------|-----|-----|-----|-----|-----|-----|
| 1 | ... | ... | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... |

#### Throughput

| Concurrency | Req/sec | Transfer (KB/s) | Avg Latency (ms) | Error Rate (%) |
|-------------|---------|------------------|-------------------|----------------|
| 1 | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

#### Error Breakdown

| Concurrency | 2xx | 4xx | 5xx | Timeout | Conn Error | Total Errors |
|-------------|-----|-----|-----|---------|------------|-------------|
| 1 | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... |

#### Latency Profile

<Classify as Flat / Linear / Exponential / Cliff with supporting data>

#### Breaking Point

<State the breaking point concurrency, which condition triggered it, and the specific metric values>

---

<Repeat for each endpoint>

---

## Comparative Analysis

<If multiple endpoints were tested, compare their performance profiles. Identify which endpoints are the weakest links.>

| Endpoint | Peak RPS | Breaking Point | Bottleneck Type | p95 at Peak |
|----------|----------|---------------|-----------------|-------------|
| GET /health | ... | ... | ... | ... |
| POST /search | ... | ... | ... | ... |

---

## Throughput Curves (ASCII)

<For each endpoint, render an ASCII chart showing throughput vs concurrency>

```
Throughput (req/s)
    ^
800 |          *----*----*
    |        *
600 |      *
    |    *
400 |   *
    |  *
200 | *
    |*
  0 +--+--+--+--+--+--+--> Concurrency
    1  5  10 25 50 100 200
```

---

## Latency Distribution (ASCII)

<For each endpoint, render an ASCII chart showing p50/p95/p99 vs concurrency>

```
Latency (ms)
     ^
1000 |                        * p99
     |                  *
 500 |            *           o p95
     |      o           o
 200 |o  o        .  .  .  . . p50
 100 |.  .  .
   0 +--+--+--+--+--+--+--+--> Concurrency
     1  5  10 25 50 100 200 500
```

---

## Bottleneck Analysis

### Primary Bottleneck

<Classification (CPU/Memory/IO/Connection Pool/Rate Limit/Thread Pool) with 3-5 bullet points of supporting evidence from the test data>

### Secondary Observations

<Any additional patterns observed, such as:>
- Garbage collection pauses (periodic latency spikes)
- DNS resolution overhead
- TLS handshake cost at high concurrency
- Keep-alive vs connection-per-request behavior
- Response body size variation under load

---

## Recommendations

### Critical (Address Immediately)

1. **<Recommendation title>**: <Detailed explanation with specific numbers from the test. E.g., "Add connection pooling -- connection errors begin at 50 concurrent users, suggesting the server is opening a new database connection per request. A pool of 20-30 connections should handle up to 200 concurrent users based on the observed throughput ceiling.">

2. **<Recommendation title>**: <...>

### Important (Address Before Scaling)

3. **<Recommendation title>**: <...>

4. **<Recommendation title>**: <...>

### Nice to Have (Optimization)

5. **<Recommendation title>**: <...>

6. **<Recommendation title>**: <...>

---

## Capacity Estimate

Based on the observed performance profile:

- **Current safe operating capacity**: <X concurrent users> (<Y req/sec>)
- **Maximum tested capacity**: <X concurrent users> (<Y req/sec, Z% error rate>)
- **Estimated capacity with recommended fixes**: <X concurrent users> (projected)

### Scaling Projections

| Target Users | Current Status | After Fixes | Additional Infra Needed |
|-------------|---------------|-------------|------------------------|
| 50 | OK | OK | None |
| 100 | Degraded (p95 > target) | OK (projected) | None |
| 500 | Breaking point | OK (projected) | Add replica |
| 1000 | Not viable | Marginal | Load balancer + 3 replicas |

---

## Methodology Notes

- Tool: <name and version>
- Each concurrency stage ran for <N> seconds with a <N>-second cooldown between stages
- Latency measurements include full round-trip time (DNS + connect + TLS + TTFB + transfer)
- All tests were run from <location/machine description>
- Results may vary based on network conditions, server load, and time of day
- For production capacity planning, repeat tests at different times and from multiple geographic locations

---

## Raw Data Reference

Raw output files are stored in: `<temp_directory_path>`

<List the files with brief descriptions>
```
