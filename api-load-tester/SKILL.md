---
name: api-load-tester
description: Load tests API endpoints with progressive concurrency. Measures response times, error rates, throughput, and identifies breaking points. Generates a detailed report with latency percentiles, throughput curves, bottleneck analysis, and optimization recommendations.
tools: Bash, Read, Write, Glob, Grep
model: inherit
---

# API Load Tester

Stress-test HTTP endpoints under increasing load, identify breaking points, and produce a report with actionable recommendations.

## Contents

- `references/tool-commands.md` -- tool invocations (hey/wrk/ab/curl), default concurrency stages, per-stage data to capture.
- `references/metrics-interpretation.md` -- latency, throughput, error, breaking-point, and bottleneck classification.
- `references/output-template.md` -- exact structure for `api-load-report.md`, including ASCII charts and scaling table.
- `references/rules-and-examples.md` -- safety rules, error handling, and example invocations.

## Inputs

Collect from the user. Ask before proceeding if a required input is missing.

**Required**: endpoint URL(s) (with method, headers, body as needed); expected latency thresholds. Default thresholds if unspecified: p50 < 100ms, p95 < 300ms, p99 < 1000ms.

**Optional**: concurrent users or range (default ramp 1 to 100); authentication; request payloads; custom headers; test duration (default 10s per stage); ramp pattern (default step ramp, doubling each stage); success criteria (default 2xx); known rate limits; environment label (prod/staging/dev).

## Workflow

Follow these steps in order.

1. **Select a tool.** Check in priority order: `which hey`, `which wrk`, `which ab`, `which curl`. If none of hey/wrk/ab exist, install hey (`brew install hey` on macOS, `go install github.com/rakyll/hey@latest` on Linux with Go) or fall back to curl with bash background processes and `wait`. Verify with a single trivial request against a provided endpoint; diagnose connectivity or auth before continuing.

2. **Validate endpoints.** Send one request per endpoint with the specified method, headers, auth, and body. Confirm the status matches the success criteria and record baseline single-request latency. On failure, surface the error and ask whether to skip or fix.

3. **Design the test plan.** Build progressive concurrency stages (see `references/tool-commands.md` for the default progression), trimming or extending to the user's concurrency range. Define per-endpoint method, URL, headers, body, success codes, and timeout (default 30s). Print the plan for review before executing.

4. **Execute stages.** For each endpoint, run every concurrency stage sequentially with the selected tool, waiting 2 seconds between stages. Capture and store the per-stage metrics. See `references/tool-commands.md` for commands, request-count formula, and the metrics list.

5. **Interpret metrics.** Compute latency percentiles and profile, throughput curve and ceiling, error rates and onset, the breaking point, and the bottleneck classification. See `references/metrics-interpretation.md`.

6. **Generate the report.** Write `api-load-report.md` to the current working directory following `references/output-template.md` exactly, including ASCII throughput and latency charts.

7. **Post-report actions.** Print a 3-5 line summary to the console, state the report path, explicitly highlight any critical issues, and offer to re-run specific stages with different parameters.

## Rules

Apply the safety rules, error handling, and example invocations in `references/rules-and-examples.md`. Key constraints: never load-test production without explicit confirmation, only test GET by default, mask auth tokens, respect 429 rate limits, count timeouts as failures, and never extrapolate beyond tested ranges.
