---
name: jev-audit
description: Audit a codebase for LLM calls that are really classifications in disguise, then produce a costed swap plan for a System One model. Use when asked to cut AI inference cost or latency, when scoping a performance engagement for a client, when reviewing an agent loop that feels slow, or when asked "where could we use Jev here". Produces a ranked table of candidates with measured latency and dollar deltas.
---

# Inference-cost audit

Most production LLM calls return a **label**, not prose — a route, a score, a yes/no, a
category. Those calls pay for autoregressive generation they do not use. This audit finds
them and prices the swap.

Deliverable: a ranked table of candidates with measured deltas. Sellable as a OneWave
engagement; same shape as `marketing-brain` — a repeatable audit run per client.

## 1. Find the candidates

Search for LLM calls, then filter to the ones whose output is a label:

```bash
grep -rnE "messages\.create|chat\.completions|generateText|\.invoke\(|anthropic\.|openai\." \
  --include=*.{ts,tsx,js,py} . | grep -v node_modules
```

A call is a candidate when **all** of these hold:

- the prompt asks for one of a **known, finite** set of answers (≤255)
- the caller **parses** the response — JSON.parse, a regex, an enum lookup, `.trim()`
- nothing downstream shows a human the model's reasoning
- it runs **often**, or a user waits on it

Strong signals in the prompt text: "respond with only", "return JSON", "classify",
"choose one of", "rate from 1 to", "answer yes or no", "do not explain".

Disqualifiers: the output is shown to a user, is used as content, needs a citation or
justification, or the answer set is open-ended.

## 2. Measure what it costs today

Do not estimate. Instrument:

- **calls/day** — from logs or a counter, not a guess
- **p50 and p95 latency** — p95 is what users feel
- **tokens in/out per call** → current $/1k calls at the provider's list price
- **is anything blocked on it** — a user, a page render, an agent's next step

## 3. Price the swap

Benchmark against a labelled set from that call's real traffic (see `jev-eval`). Never
project from a vendor benchmark.

Reference numbers, measured on real records, 4 questions per record:

| | latency | cost/1k | accuracy |
|---|---|---|---|
| Jev hosted | 399 ms | $0.023 | matched Claude on a 15-record set |
| Von local | 174 ms | $0.00 | matched only with well-written criteria |
| Claude Haiku 4.5 | 2,322 ms | ~$0.55 | baseline |

Jev pricing: **$0.042/MTok input, output free.**

## 4. Rank by payoff, not by ease

Rank each candidate on:

1. **volume × unit saving** — the actual dollar figure
2. **is a human waiting** — latency wins are worth more than cost wins on user-facing paths
3. **blast radius if wrong** — a misrouted support ticket is cheap; a mis-scored
   transaction is not
4. **accuracy delta on the labelled set** — anything below parity needs a confidence gate,
   and a gate has its own cost

Kill anything where volume is low. At a few hundred calls a day the savings round to
zero and you have added a vendor.

## 5. Write it up

Per candidate: file and line, what it decides, calls/day, current latency and cost,
projected latency and cost, measured accuracy delta, recommended gate, and a
**go / no-go with the reason**.

Lead the summary with total projected monthly saving and the single biggest latency win.

Always include the limits: eval-set size, that Jev is early access with no SLA, and that
a fallback to the existing call must stay wired.

## Where this pays in the OneWave stack

- **Sage widget routing** — build it. A visitor is watching; 400 ms vs 2.3 s is the whole
  difference.
- **RB2B visitor firehose** — build it. The only stream with volume where 24x cheaper
  compounds.
- **Lead intake classification** — measure first. Correct, but a handful of leads a day.
- **Lead watchdog** — leave it. Nightly cron, nothing waits on it.

## Related

`jev-eval` produces the accuracy numbers this audit depends on. `jev-integrate` is the
wiring workflow for anything that gets a go.
