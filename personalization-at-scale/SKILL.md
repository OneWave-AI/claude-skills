---
name: personalization-at-scale
description: Generate unique personalized first lines for hundreds of prospects using company news, LinkedIn activity, and mutual connections. Saves 10+ hours of manual research per campaign. Use when you need personalized outreach at volume.
---

# Personalization at Scale

Generate hundreds of unique, researched first lines in minutes instead of hours, making cold outreach feel warm.

## Contents

- `references/research-sources.md` - signal sources, personalization styles, quality standards
- `references/patterns-by-type.md` - sample first lines and tables for each angle (congrats, observation, mutual connection, company news, hiring, tech stack, thought leadership, shared background)
- `references/fallbacks.md` - role/stage/industry/competitor lines for prospects with no angle
- `references/output-template.md` - full campaign deliverable structure
- `references/benchmarks.md` - expected lift, A/B reference data, pro tips (do/don't)
- `references/example-campaigns.md` - worked campaign examples by persona

## Workflow

1. Ingest the prospect list (CSV or pasted). Require First Name, Last Name, Title, Company; use LinkedIn URL, email, website, industry, size, and location when available.

2. Confirm preferences: which personalization styles to prioritize (1-3), tone (professional, casual, direct, consultative), and any exclusions (recency cutoff, personal topics, sensitive subjects).

3. Research each prospect across the sources in `references/research-sources.md`. Identify the strongest, most recent, verifiable angle per prospect.

4. Match each prospect to its angle and draft from the matching pattern in `references/patterns-by-type.md`. For prospects with no angle, draft from `references/fallbacks.md`.

5. Generate 2-3 first-line options per prospect, each with a confidence score (High/Medium/Low) and notes on alternative angles. Follow the structure in `references/output-template.md`.

6. Quality-check the first 10 manually. Confirm each line is specific, recent, relevant, natural, and verifiable before scaling the batch.

7. Export in the requested format: CSV with personalization columns, merge fields for the outreach tool (Outreach, Salesloft), individual drafts, or copy-paste blocks.

8. Track response rates by personalization type and refresh personalizations every 30 days as activity changes.

See `references/benchmarks.md` for target success rates and `references/example-campaigns.md` for persona-specific approaches.
