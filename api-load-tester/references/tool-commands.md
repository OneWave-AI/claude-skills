# Tool Commands

Run each concurrency stage with the best available tool. Wait 2 seconds between stages so the server stabilizes and carryover effects are avoided.

## hey (preferred)

```bash
hey -n <total_requests> -c <concurrency> -t <timeout> \
    -m <METHOD> \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '<body>' \
    <url>
```

Calculate total requests as `concurrency * (duration / estimated_response_time)`, with a minimum of `concurrency * 10` requests per stage.

## wrk

```bash
wrk -t <threads> -c <concurrency> -d <duration>s \
    -s <lua_script> \
    <url>
```

Generate a Lua script when custom methods, headers, or bodies are needed.

## ab (Apache Bench)

```bash
ab -n <total_requests> -c <concurrency> -t <timeout> \
    -H "Authorization: Bearer <token>" \
    -T "application/json" \
    -p <body_file> \
    <url>
```

## curl fallback

```bash
for i in $(seq 1 $CONCURRENCY); do
  (for j in $(seq 1 $REQUESTS_PER_USER); do
    curl -o /dev/null -s -w "%{http_code} %{time_total}\n" \
      -X <METHOD> \
      -H "Authorization: Bearer <token>" \
      -H "Content-Type: application/json" \
      -d '<body>' \
      <url>
  done) &
done
wait
```

## Default concurrency stages

Adjust to the user-specified concurrency range. If the user specifies a max of 50, stop there. If they specify a max of 1000, add stages beyond 500.

| Stage | Concurrent Users | Duration | Purpose |
|-------|-----------------|----------|---------|
| 1 | 1 | 10s | Baseline single-user latency |
| 2 | 5 | 10s | Light load behavior |
| 3 | 10 | 10s | Moderate load |
| 4 | 25 | 10s | Medium load |
| 5 | 50 | 10s | Heavy load |
| 6 | 100 | 10s | Stress test |
| 7 | 200 | 10s | Breaking point search |
| 8 | 500 | 10s | Extreme stress (optional) |

## Per-stage data to capture

- Total requests sent
- Successful responses (by status code)
- Failed responses (by status code or error type)
- Latency: min, max, mean, median (p50), p90, p95, p99
- Requests per second (throughput)
- Transfer rate (bytes/sec if available)
- Connection errors, timeouts, and resets
- Stage start and end timestamps

Store raw results in a temp directory like `/tmp/api-load-test-<timestamp>/`, one file per stage:
`raw_<endpoint_name>_c<concurrency>.txt`.
