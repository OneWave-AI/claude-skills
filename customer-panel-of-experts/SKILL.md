---
name: customer-panel-of-experts
description: Build a panel of your real buyer personas (from a deep scan of any tools you allow it to connect to) and have them debate any decision you bring — a marketing launch, a price increase, a new product, a positioning change, a feature cut. Returns a structured debate, the strongest objections, and a clear recommendation. Use when you want your actual customers in the room before you commit.
tools: Read, Write, Bash, Grep, Glob, WebSearch, WebFetch, Agent
model: inherit
---

# Customer Panel of Experts

Put your customers in the room before you spend money or burn trust. This skill assembles a panel of data-grounded buyer personas and runs a real debate on whatever you're deciding — then hands you the decision, the dissent, and what to test next.

It is the flagship of the panel family. It reads the persona library produced by `icp-deep-scanner` and turns it into a living, arguing room.

## When to use it
- "Should we raise prices 20%?" — and what each segment will actually do.
- "Here's the launch campaign for {product}. Will it land?"
- "We're killing {feature} and adding {feature}. Who revolts?"
- "Pick between positioning A and positioning B."
- Any high-stakes call where you'd normally guess what customers think.

## Step 0 — Get the personas

The panel is only as good as its members. In order of preference:
1. **Use an existing persona library.** Look for `personas/` and `icp-profile.md` (output of `icp-deep-scanner`). Load every persona file and `personas/index.md`.
2. **Generate one now.** If none exists and the user has connected tools, run `icp-deep-scanner` first (read-only) to build it from real data.
3. **Bootstrap from input.** If there's no data and no time, build 3–5 provisional personas from what the user tells you — and label the entire session **"PROVISIONAL — not grounded in customer data"** at the top and bottom. Never let a guessed panel masquerade as a researched one.

### Data & security rules
- Connecting tools is **read-only**. Never write to, send from, or modify a connected source. Confirm before any exception.
- Personas are archetypes. Do not surface real customer names/emails/account IDs in the debate. Quotes must be scrubbed.
- Secrets stay in env vars / the MCP connection — never printed or stored in output.

## Step 1 — Frame the decision

Restate the decision crisply and lock the variables before debating:
- **The decision:** one sentence, with the specific option(s) on the table.
- **What changes for the customer:** price, workflow, access, expectation.
- **Success metric:** what "this went well" means in numbers.
- **Reversibility:** can we walk it back, and at what cost?

If the user's ask is vague ("is this a good idea?"), tighten it into a decision with options before proceeding.

## Step 2 — Seat the panel

Select 3–6 personas relevant to THIS decision (a pricing decision needs the economic buyer and a price-sensitive segment; a feature cut needs the power users who rely on it). For each seated persona, state in one line who they are and why they're in the room. If a critical viewpoint is missing from the library, say so — don't invent a flattering one.

For a deep, parallel debate (many personas × many angles), dispatch one sub-agent per persona via `/agent-army`, then synthesize. Otherwise run it inline.

## Step 3 — Run the debate

Each persona argues **in character, from their real goals, pains, and language** — not as a generic critic. Structure:

1. **Gut reaction** — each persona's first, honest read of the decision (one paragraph, in their voice).
2. **Cross-examination** — personas challenge each other. The economic buyer and the end user often want opposite things; let that tension play out. Surface where one persona's win is another's loss.
3. **The strongest objection** — the single most dangerous reaction, stated as that customer would actually say it (and would actually act on — churn, downgrade, public complaint, silence).
4. **What would change their mind** — the concession, proof, or framing that flips a NO to a YES.

Keep personas honest: include the ones who will hate it. A panel that all agrees is a panel you rigged.

## Step 4 — Synthesize the decision

```markdown
# Customer Panel — {Decision}
Generated: {timestamp} · Panel: {persona list} · Grounding: {data-backed / PROVISIONAL}

## Recommendation: {GO / GO WITH CHANGES / NO / TEST FIRST}
One paragraph: what to do and why, in plain language.

## Vote by persona
| Persona | Verdict | Why | If it ships anyway, they will… |

## The objections that matter (ranked)
1. {Objection} — who raises it, how likely to act, blast radius, mitigation.

## What this changes about the plan
- Concrete edits to the launch / price / product before you commit.

## What to test before betting the company
- The cheapest experiment that would de-risk the biggest unknown.

## Confidence & blind spots
- Grounding strength, which personas are thin, which viewpoint is missing.
```

## Step 5 — Offer the next move
Offer to: rerun the panel against a revised plan, hand the strongest objection to `prospect-panel-simulator` to test live messaging, route a pricing decision to `pricing-change-strategist`, or escalate a full launch to `product-launch-war-room`.

## Guardrails recap
Grounded personas beat invented ones — and provisional panels say so loudly · read-only connections · no real PII in output · include the customers who'll hate it · every verdict ties to a persona's real motivation.
