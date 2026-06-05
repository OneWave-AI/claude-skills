---
name: product-launch-war-room
description: Run a go-to-market war room for a launch, repositioning, price change, or new product. Convenes opposing expert and customer-persona viewpoints to debate the plan, surfaces the risks that kill launches, and returns a go/no-go call plus a phased rollout plan with owners, sequencing, and kill criteria. Use before any launch you can't easily walk back.
tools: Read, Write, Bash, Grep, Glob, WebSearch, WebFetch, Agent
model: inherit
---

# Product Launch War Room

A launch fails for boring reasons: nobody owned the objection, the price change leaked, the segment that mattered wasn't in the room. This skill runs the war room that catches those reasons before launch day — adversarial by design, decision-oriented, and grounded in your real customers when data is available.

It composes the panel skills (`customer-panel-of-experts`, `prospect-panel-simulator`) into a single GTM decision and a rollout plan you can execute.

## What it's for
- New product / feature launch
- Repositioning or rebrand
- Price increase or packaging change (hand the rollout to `pricing-change-strategist`)
- Market or segment expansion
- Sunsetting something customers depend on

## Step 1 — Define the launch

Lock these before any debate:
- **What's launching** and what specifically changes for the customer.
- **Audience** — existing customers, prospects, a specific segment, the market.
- **Goal + metric** — the number that defines success and the window to hit it.
- **Constraints** — timeline, budget, team, dependencies, hard commitments already made.
- **Reversibility** — fully reversible / costly / one-way door. This sets how much rigor the war room applies.

## Step 2 — Convene the room

Seat both sides. Use `icp-deep-scanner` personas where the call is customer-facing; add functional experts for execution risk:
- **Customer voice** — relevant buyer personas (load from `personas/`; if absent and tools are connected, run `icp-deep-scanner` read-only; otherwise mark PROVISIONAL).
- **The skeptic / pre-mortem lead** — assumes the launch already failed and explains why.
- **Functional experts** as the launch demands — GTM/demand-gen, sales, product, support/CS, finance, brand. Each owns the risks in their lane.

For a thorough war room, dispatch parallel sub-agents (one per role) via `/agent-army`, then synthesize. Connections are read-only; no external sends; no real PII; secrets in env vars only.

## Step 3 — Pre-mortem and debate

1. **Pre-mortem** — "It's 90 days post-launch and it flopped. What happened?" Each role writes the most likely failure in their lane.
2. **Customer reaction** — run the plan/messaging through the customer or prospect panel. Who's delighted, who churns, who shrugs.
3. **Cross-fire** — finance vs. growth, sales vs. product, brand vs. speed. Force the real trade-offs into the open.
4. **Risk register** — every surfaced risk scored by likelihood × blast radius, with an owner and a mitigation.

## Step 4 — Decide and sequence

```markdown
# Launch War Room — {Launch}
Generated: {timestamp} · Room: {roles/personas} · Reversibility: {…} · Grounding: {data / PROVISIONAL}

## Call: {GO / GO WITH CHANGES / DELAY / NO-GO}
The reasoning in one paragraph.

## Top risks (ranked)
| Risk | Likelihood | Blast radius | Owner | Mitigation | Pre-launch or live? |

## Required changes before launch
- The non-negotiables surfaced by the room.

## Phased rollout
- Phase 0 — prep & internal enablement (sales, support scripts, FAQ)
- Phase 1 — soft launch / segment / beta + what we watch
- Phase 2 — full launch + channels + sequencing
- Phase 3 — post-launch monitoring window

## Kill criteria & rollback
- The specific metric thresholds that trigger pause or rollback, and how to walk it back.

## Owners & timeline
| Workstream | Owner | Deadline | Dependency |

## Comms kit to produce next
- Customer email, sales talk track, support FAQ, objection handling, public page.
```

## Step 5 — Hand off the artifacts
Offer to generate the comms kit (`cold-email-sequence-generator`, `landing-page-copywriter`, `company-announcement-writer`), route a price change to `pricing-change-strategist`, build the launch video with `hyperframes-ad-director`, or re-run the room against the revised plan.

## Guardrails recap
Adversarial by default — the room's job is to find the failure, not bless the plan · rigor scales with reversibility · kill criteria are mandatory, not optional · read-only connections, no sends, no real PII · provisional grounding is labeled.
