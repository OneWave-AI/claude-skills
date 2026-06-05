# Scoring and Rules

Change-magnitude scoring scale, applied to every detected change:

```
1  Cosmetic   wording change, no strategic impact
2  Minor      small price adjustment, minor feature update
3  Moderate   new feature in existing category, meaningful price change
4  Major      new product tier, new product line, significant pivot
5  Critical   acquisition, major funding round, market exit, price war
```

## Change Detection Algorithm

When comparing current data against previous snapshots:

1. Exact match detection: directly compare structured data (prices, feature lists).
2. Semantic similarity: for content and descriptions, detect meaningful changes vs cosmetic edits.
3. Magnitude scoring: rate each change on the 1-5 scale above.
4. Alert threshold: changes rated 4-5 generate immediate alerts.

## Trend Analysis Protocol

When 3 or more snapshots exist for a competitor:

1. Load all historical snapshots chronologically.
2. Plot pricing changes over time (direction and magnitude).
3. Calculate feature velocity (new features per time period).
4. Identify content publishing cadence and topic evolution.
5. Map hiring patterns (growing, stable, shrinking; department shifts).
6. Synthesize into a strategic narrative: "Competitor X appears to be [pivoting toward / doubling down on / retreating from] [area] based on [evidence]".

## Data Quality Rules

1. Source attribution: always note where data came from.
2. Timestamp everything: every data point gets a collection timestamp.
3. Confidence tagging: mark data as confirmed (official source), inferred (indirect signals), or speculative (analyst interpretation).
4. Staleness warnings: flag data older than 30 days as potentially stale.
5. Contradiction detection: if new data contradicts previous data, flag it and investigate.
6. No fabrication: if data for a dimension cannot be found, say so. Never make up competitor data.

## Execution Rules

1. Always read existing data first. Before fetching new data, load the most recent snapshots to establish a comparison baseline.
2. Be thorough but efficient. Do not fetch pages that have not changed (use snapshot comparison). Focus monitoring time on high-value dimensions.
3. Separate fact from analysis. Snapshots contain raw data; analysis lives in the intel deliverable. Never mix them.
4. Protect against hallucination. If WebFetch fails or returns incomplete data, note the gap. Do not fill in data from memory or assumption.
5. Respect rate limits. Space out web requests. Do not hammer competitor websites.
6. Date everything. Every file, snapshot, and deliverable gets a date in the filename.
7. Build the picture over time. The trend across many snapshots is more powerful than any single one. Always reference historical context when available.
8. Actionable over comprehensive. Lead with "so what" and "now what".
9. No competitive sabotage suggestions. Recommend legal, ethical competitive responses only.
10. Privacy compliance. Do not collect personal data about competitor employees beyond publicly available professional information (job titles, LinkedIn profiles).

## Quick Commands

Invoke specific sub-functions on request:

- "Check pricing for [competitor]": run pricing monitoring for a single competitor.
- "What has changed since last run?": generate a changes-only summary.
- "Compare us to [competitor] on features": feature gap analysis.
- "Trend report": generate longitudinal trend analysis.
- "Add competitor [name] [url]": add a new competitor to monitoring.
- "Full report": complete monitoring run plus full intelligence deliverable.
- "Alert me about [competitor]": set up monitoring focus on a specific competitor.
