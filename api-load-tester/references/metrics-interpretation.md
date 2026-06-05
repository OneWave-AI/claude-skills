# Metrics Interpretation

After all stages complete, interpret the collected metrics as follows.

## Latency

For each endpoint, compute:

- **Latency by percentile**: p50, p75, p90, p95, p99 at each concurrency level.
- **Latency trend**: How median latency changes as concurrency increases. Compute the slope.
- **Latency stability**: Standard deviation at each stage. Flag stages where stddev > 2x the median.
- **Latency threshold violations**: At which concurrency level each percentile exceeded the target.

Classify the latency profile:

- **Flat**: Latency stays within 20% of baseline up to max concurrency. Excellent.
- **Linear degradation**: Latency increases proportionally with concurrency. Acceptable up to a point.
- **Exponential degradation**: Latency increases faster than concurrency. Bottleneck detected.
- **Cliff**: Latency suddenly spikes at a specific concurrency level. Hard limit found.

## Throughput

For each endpoint, compute:

- **Peak throughput**: Maximum requests/second achieved and at which concurrency level.
- **Throughput ceiling**: The concurrency level where adding more users no longer increases throughput (saturation point).
- **Throughput curve shape**: Linear growth, logarithmic growth, or plateau.
- **Efficiency ratio**: Throughput per concurrent user at each stage.

## Errors

For each endpoint, compute:

- **Error rate by stage**: Percentage of non-success responses at each concurrency level.
- **Error onset**: The concurrency level where errors first appear above 0.1%.
- **Error types**: Categorize into timeout, connection refused, 4xx, 5xx, and other.
- **Error rate trend**: Stable, growing linearly, or growing exponentially.

## Breaking Point

The breaking point is the concurrency level where ANY of the following first occurs. State it clearly and name which condition triggered it.

1. Error rate exceeds 1%.
2. p95 latency exceeds 5x the baseline single-user p95.
3. Throughput decreases compared to the previous stage (throughput cliff).
4. More than 5% of connections are refused or reset.

## Bottleneck Classification

Classify the likely bottleneck and provide supporting evidence from the data.

- **CPU-bound**: Latency increases linearly, throughput plateaus, no connection errors.
- **Memory-bound**: Latency is stable then suddenly spikes, often with connection resets.
- **I/O-bound (database)**: Latency variance is high, throughput has a hard ceiling, errors are timeouts.
- **I/O-bound (network)**: Connection refused errors, high timeout rate, latency spikes correlate with error spikes.
- **Connection pool exhaustion**: Sudden onset of connection errors at a specific concurrency level, latency cliff.
- **Rate limiting**: Consistent 429 status codes above a threshold, latency stable but errors spike.
- **Thread/process pool exhaustion**: Throughput plateaus, latency grows linearly, no errors until a hard cliff.
