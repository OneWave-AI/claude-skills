---
name: jev-integrate
description: Wire a System One model (Jev, or an open reproduction like Von) into a product feature — routing, guardrails, scoring, classification. Use when replacing an LLM call that returns a label rather than prose, when adding a typed decision to an agent loop, or when deciding between the hosted Jev API and a local open model. Covers question design, the eval-set-first workflow, threshold calibration, confidence gates, and the traps measured on real data.
---

# Wiring a System One model into a feature

A System One model answers **typed questions in one forward pass**. It generates no text.
State in, typed answers with calibrated probabilities out. It is an if-statement that can read.

Use it when the decision is **narrow, pre-specified, and repeated**. Do not use it for
anything that needs a written explanation — that is still a job for Claude.

## Before anything else: is this actually the right tool

Answer these three. If any is "no", stop and keep the LLM call.

1. **Are the possible answers known up front?** Choice caps at 255 options.
2. **Does the caller need only the label**, not the reasoning? If a human reads a
   justification downstream, you need prose and this is the wrong tool.
3. **Is it high volume, or is a person waiting?** This is a latency and cost optimisation,
   not a capability gain. It knows nothing Claude doesn't. On a nightly cron over
   fifty records it buys you a dependency and nothing else.

Measured on 150 hand-labelled records across three jobs (our Sep 20 2026 run):
Jev ties GPT-5.2 at **145/150** and costs **46x less** ($0.036 vs
$1.64 per 1k records), but end to end it is only **1.7x faster** than GPT-4.1-mini — the
published 40x-200x is against a 3-329 s multi-step frontier workflow, not one call.

**The open reproductions are not drop-in.** Same run: Von 1.0.1 (395M) **92/150 (61%)**,
Laya (421M) **62/150 (41%)**. They collapse onto one class rather than degrading — Von
predicted `exfiltration` 25 times on a 50-command set containing five. A confidence gate
does not rescue that: catching Von's errors meant escalating 92% of volume, Laya 100%,
against Jev's 8%. Use them only where you have measured them on your own labelled set.

## The three question types

```python
"lead_type":  {"type":"choice", "instructions": "...", "criteria": {"opt_a":"desc","opt_b":"desc"}}
"is_urgent":  {"type":"noul",   "instructions": "..."}                       # -> 0.0–1.0
"priority":   {"type":"score",  "instructions": "...", "criteria":["ignore","low","high"]}
```

Ask every question you need in **one call** — they all resolve in the same forward pass, so
four questions cost roughly what one does.

Response shape (both Jev and Von):

```python
r["answers"]["lead_type"]["choice"]         # the label
r["answers"]["lead_type"]["probabilities"]  # full distribution
r["answers"]["lead_type"]["confidence"]     # use this for gating
r["answers"]["is_urgent"]["noul"]           # 0.0–1.0
r["answers"]["priority"]["score"]           # position on the scale, e.g. 2.41
```

## Workflow

### 1. Build the labelled set FIRST — 50 records minimum

Non-negotiable, and the single highest-value step. Hand-label real records from the
stream you intend to point this at, **before** writing any criteria. Without it you cannot
tell a bad question from a bad model, and the failure is silent — see `jev-eval`.

### 2. Write the criteria as if explaining to a new hire

Worst-to-best spread across four wordings of the same questions, 50 records per task
(our Sep 20 2026 run):

| task | Jev | Von (395M) | Laya (421M) |
|---|---|---|---|
| agent command risk | 44-49 (10 pts) | 9-23 (**28 pts**) | 18-28 (20 pts) |
| lead triage | 47-49 (4 pts) | 22-34 (**24 pts**) | 15-24 (18 pts) |
| ticket routing | 41-47 (12 pts) | 23-41 (**36 pts**) | 22-36 (28 pts) |

Same sweep on the command task with the LLMs included: Haiku 4.5 46-48 (4 pts), GPT-4.1-mini
45-50 (10 pts), **Jev 44-49 (10 pts)**, GPT-5-mini 41-49 (16 pts).

**Jev is NOT more wording-robust than a small LLM** — it swings the same ten points, and
Haiku was the steadiest model in the test. Read the FLOOR, not the spread: every hosted
model bottoms out at 82-92% and stays shippable, while Von bottoms out at 18% and Laya at
36%. Do NOT read this as "write better criteria and the open model catches up" — an earlier
15-record test concluded exactly that and it was wrong. Richer criteria did not reliably help: on lead
triage Von scored 34/50 on the terse wording and 28/50 on the carefully written one. What
moves those numbers is sensitivity to surface form, not comprehension, so every future
criteria edit is an unannounced regression risk.

Write each option with: what it is, what it is *not*, and the edge case that tempts a
wrong answer. Name the default explicitly when one option should dominate.

### 3. Calibrate thresholds against the labelled set — never assume 0.5

A noul is a probability, not a boolean. **Jev's noul has a floor**: on records that were
plainly clean it still returned 0.2–0.5 where Claude returned 0.0. On the measured data
the useful cut was **~0.85**, not 0.5. Thresholds do not transfer between models — re-sweep
when you switch.

Don't hand-write the sweep. `jev-eval` owns calibration and ships the tool:

```bash
python ~/.claude/skills/jev-eval/scripts/sweep.py labelled.json configs.json \
    --backend jev --question <name>
```

### 4. Design the confidence gate

Gate low-confidence answers up to Claude. The same script reports both halves that matter —
what fraction of **errors** the gate catches, and what fraction of **volume** it escalates —
and labels the result. A gate catching every error while escalating 73% of traffic is scored
`saves nothing`, because it is a slow path with extra steps. If you see that, the fix is
better criteria or the hosted model, not a different threshold.

```python
a = r["answers"]["lead_type"]
if a["confidence"] < GATE:
    return escalate_to_claude(state)   # slow path
return a["choice"]                      # fast path
```

### 5. Ship behind a flag, log both paths for a week

Log the System One answer *and* what the old path would have said. Compare on real
traffic before you cut over. Never cut over on eval-set numbers alone.

## Access paths

```bash
# 1. TypeSafe direct — key in macOS Keychain, service `typesafe-api-key`
export TYPESAFE_API_KEY="$(security find-generic-password -s typesafe-api-key -w)"
curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"jev-latest","state":"...","questions":{...}}'
```

```javascript
// 2. Cloudflare Workers AI — no waitlist
await env.AI.run('typesafe/jev', { state, questions })
```

```python
# 3. Von — local, free, Apache-2.0, 395M ModernBERT
# pip install von-sdk
import von
r = von.system_one(state="...", questions={"x": von.Noul(instructions="...")})
r.answers["x"].noul
```

## Traps

- **Von's `Choice` takes `criteria=`, not `choices=`.** Pydantic error if you guess wrong.
- **Von returns `.answers[k]`**, not `.nouls[k]` / `.choices[k]`. The LangChain wrapper
  differs from the raw SDK here.
- **Von's 34 s cold start** loads weights. Warm it at boot; never measure it in latency.
- **Don't threshold a noul at 0.5.** See step 3.
- **Jev is early access, single vendor, no SLA.** Do not put a client-facing critical path
  on it without a fallback to Claude.
- **Small eval sets lie.** 15 records where both hosted models scored 100% proves almost
  nothing. Use hundreds.

## Related

`jev-eval` builds and runs the labelled set. `jev-audit` finds which existing LLM calls
in a codebase are worth converting.
