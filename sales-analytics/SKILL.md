---
name: sales-analytics
description: Use this skill when the user wants to analyze sales pipeline, review win rates, investigate
  sales velocity or cycle length, build a sales report, evaluate rep performance, look at lead source
  quality, or answer questions about their CRM data. Triggers include 'how is the pipeline', 'win rate
  by segment', 'sales cycle', 'pipeline coverage', 'rep performance', 'forecast accuracy', 'why are deals
  stalling', 'lead source quality', 'stage conversion', 'pull my Salesforce numbers', 'HubSpot deals report',
  'sales report'. Reads live data from your Coupler.io workspace via the Coupler.io MCP connector.
---

# Sales Analytics

Analyze sales performance using data from Coupler.io dataflows (Salesforce, HubSpot, Pipedrive, Close, Zoho, custom CRMs). This skill guides you through retrieving opportunity/deal data, computing pipeline and conversion metrics, investigating velocity and rep performance, detecting anomalies, and presenting actionable insights a sales leader can act on.

## Step 0: Context Check (Pre-requisite)

Before starting any analysis, the **Data Context Check** skill (`generate-data-set-context`) runs as a gate. It calls `get-schema` on each target dataset to determine whether meaningful context is attached — particularly stage definitions, segment mappings (SMB/MM/Enterprise), team/territory structure, lead source taxonomy, and how 'closed-lost no decision' is distinguished from 'closed-lost competitive'.

- If context exists → proceed to Step 1.
- If context is missing → the user is offered the option to generate it first.

Do not duplicate this check in Step 1d.

## Step 1: Discover and Select Data Sources

### 1a. Discover available data

Default to `search-datasets` with sales-flavored keywords — `salesforce`, `hubspot`, `pipedrive`, `close`, `zoho`, `opportunities`, `deals`, `pipeline`, `leads`, `activities`, or whatever CRM the user named. Search keeps the response small and lands on the right dataflow when the domain is known.

Fall back to `list-datasets` only when the user is genuinely browsing or hasn't given any source/keyword to anchor on. Each dataflow represents a CRM data pipeline (e.g. "Salesforce Opportunities", "HubSpot Deals", "Pipedrive Pipeline", "Salesforce Activities", "Lead Sources").

### 1b. Select relevant datasets

**Unambiguous match (1 dataflow)** → use it; mention which one.

**Obvious candidates (2–3)** → state your selection with one-line reasoning, proceed but invite corrections.

**Ambiguous (5+, or unclear)** → present best candidates (up to 5–7) grouped by source/scope, with reasoning, and wait for confirmation:

```
I found 4 dataflows likely relevant to your win-rate question:
  1. salesforce_opportunities — full pipeline with stage history
  2. hubspot_deals — older deals not migrated to SF
  3. salesforce_activities — calls/emails per opportunity
  4. closed_lost_reasons — categorized loss reasons
Should I focus on 1 alone, or include 4 to break down the loss reasons?
```

**Hard gate only when ambiguous.**

### 1c. Get dataflow details

Call `get-dataflow` for each candidate. Note `schedule`, source health, and last successful run — CRM extracts can lag, and pipeline snapshots become misleading fast.

### 1d. Understand the data structure

Call `get-schema` on each target dataset. If context was generated in Step 0, use the enriched schema directly.

For sales/CRM schemas, watch for: opportunity_id, account_id, owner_id, stage, stage_history (rare; often requires snapshots), amount/expected_amount, close_date, created_date, won/lost flags, lead_source, segment, territory, probability. Stage history is the load-bearing one for cycle/conversion analysis — if it's missing, flag that some metrics will be approximations.

### 1e. Sample the data

Sample each dataset. Watch for: deals stuck in legacy stages, missing close_date on open deals, amount in mixed currencies, deals tagged closed-won but with empty amount (services or trials), duplicate deal records across systems.

## Step 2: Compute Metrics via SQL

Always compute via SQL in `get-data`.

### Working with multiple datasets

**Date alignment:** created_date, last_modified, close_date, stage_change_date — confirm which the user wants. 'Pipeline as of date X' typically uses close_date filtered by stage status as of X (requires snapshot history).

**Currency normalization:** Multi-currency CRMs need conversion (most have a currency field per opportunity). State your conversion approach.

**Open vs. closed:** Be explicit which population you're analyzing. 'Pipeline' usually means open deals. 'Win rate' usually means closed (won + lost) deals — open deals don't count yet.

**Snapshot vs. live:** Live CRM data is point-in-time current. To compute 'pipeline as of last quarter', you need historical snapshots (often via daily extracts). Without snapshots, you can only approximate using created_date and close_date.

## Step 3: Draft Findings and Get User Feedback

Before generating a full analysis, present a brief summary — top 3–5 findings, anomalies, direction. Wait for user response.

## Step 4: Build the Analysis

### Pipeline Review

Snapshot the current open pipeline:

- **Total pipeline value** — sum of open deal amounts, weighted (× probability) and unweighted.
- **Stage distribution** — count and value by stage. Healthy pipeline shows progression; bunched-at-stage-1 signals a stalled top-of-funnel.
- **Pipeline coverage** = (open pipeline closing in period) / (target for period). Healthy: 3x for the current quarter.
- **Aging** — days in current stage. Deals stuck >2x average stage time are at risk.
- **Top 10 deals** — biggest open deals with stage, age, owner, expected close. Always show the leaderboard, even if the user didn't ask.

### Win Rate Investigation

- **Overall win rate** = closed-won / (closed-won + closed-lost) for the period.
- **By segment** — SMB/MM/Enterprise rates often differ 2–3x; report separately.
- **By source** — inbound vs. outbound vs. partner can differ wildly.
- **By rep** — flag outliers (best, worst), but caveat with sample size — a rep with 4 deals doesn't have a meaningful rate.
- **Loss reason analysis** — if loss reasons are tagged, group them: price, product fit, no-decision, competitive, timing. No-decision losses signal qualification issues; competitive losses signal product/positioning issues.

### Velocity & Cycle Analysis

- **Sales velocity** = (# open opportunities × avg deal size × win rate) / sales cycle length (days). Quarterly velocity in $/day is a leading indicator.
- **Sales cycle (median days)** — created_date to close_date for closed-won deals. Use median, not mean — a few mega-deals skew the mean.
- **Stage cycle** — median days per stage. Identifies the bottleneck stage.
- **Stage conversion** — share of deals that progress from stage N to stage N+1 (vs. dying in stage N). Requires stage history; without it, approximate using created→won transitions.

### Rep Performance

- **Quota attainment** — actual / quota for the period. Distribution across the team matters more than the average.
- **Activity metrics** — calls, emails, meetings per rep (if activity data is connected). Correlate to outcomes; high activity / low conversion signals quality issues.
- **Win rate, avg deal size, cycle length** per rep, with sample size caveat.
- **Pipeline-built per rep** — leading indicator for next period's bookings.

Never single out a rep negatively without enough data (n>10 closed deals minimum). Frame development opportunities, not failures.

### Anomaly Detection and Metric Investigations

Apply this framework whenever investigating a change, drop, or spike (e.g., 'why did our win rate drop'):

**Severity classification:**
- **Informational** — within 1 SD of trailing-quarter average, or <5pp change in rate metrics. Note it.
- **Warning** — 1–2 SD, or 5–10pp change. Investigate, present hypotheses.
- **Critical** — >2 SD, >10pp change, or pipeline coverage dropping below 2x. Lead with this finding.

**Baseline comparison:** Same quarter prior year (sales has annual cycles), trailing 4-quarter average, target/budget.

**Root cause investigation steps:**
1. **Isolate the scope** — one segment, one source, one team, one product line, or everything?
2. **Check data freshness** — are recent stage changes recorded? CRM hygiene gaps make 'metric drops' that are really data gaps.
3. **Check upstream changes** — territory realignment, comp plan changes, pricing updates, product launches/sunsets, marketing source mix shifts.
4. **Check for data issues** — bulk-edited deals, duplicates, deals reassigned mid-cycle, stage definitions changed.
5. **Present hypotheses ranked by likelihood** — "Most likely: enterprise segment win rate dropped 12pp, accounts for 80% of the overall drop. Less likely: rep churn — only 2 reps left this quarter."

## Step 5: Present Results

Lead with the headline. Plain language. Every finding gets a 'So what?' and 'Now what?'

**Abbreviation expansion:** First use of CRM, ACV, ARR, MQL, SQL (sales-qualified lead, NOT structured query language — disambiguate if both meanings could apply), CAC, NRR — expand.

**Sample size caveats:** When breaking down by rep/source/segment, state n. "Inbound has a 28% win rate (n=42) vs outbound's 14% (n=8)."

## Rules & Edge Cases

- Always state data freshness (when the dataflow last ran) and whether the period is in-progress or closed.
- Open vs. closed populations: never silently mix them. 'Pipeline win rate' is almost always nonsense — open deals don't have outcomes yet.
- Probability fields: confirm whether they're rep-set or stage-derived. Rep-set probabilities are often inflated.
- Stage definitions: stage names like 'Discovery' or 'Negotiation' mean different things at different companies — defer to the user's stage glossary if context exists.
- Multi-currency: state your normalization. Don't sum amounts across currencies without conversion.
- Snapshots: if doing historical analysis without snapshot data, say so. "This 'pipeline as of Q1' is approximated from created_date and stage; without daily snapshots, deals that moved stage mid-quarter are counted at their final stage, not their Q1-end stage."
- Channel/source double-counting: deals with both inbound and outbound activity may be tagged inconsistently. Pick one source-of-truth field per analysis and stick to it.
- Rep attribution: if territory or owner changed mid-deal, state how you're attributing the win/loss.
- Sample-size minimums: per-rep stats with n<10 closed deals are noise — use them to spot patterns, not for performance reviews.
- If a dataflow's last execution failed or is stale (>1 day for daily-refresh CRM data), warn the user.
