---
name: lookalike-customer-finder
description: Input your best customers and find 100+ companies that match the profile. Uses firmographic data, tech stack, growth signals, and similarity scoring to identify ideal prospects. Use when building target account lists or expanding to new markets.
---

# Lookalike Customer Finder

Analyze a company's best customers and find similar companies that match the same profile, producing a high-quality, ranked target account list.

## Contents

- `references/scoring-model.md` - Profile dimensions, weighted scoring model, and score bands.
- `references/output-template.md` - Full Markdown report structure (ICP, ranked lookalikes, market insights, targeting strategy, action plan).
- `references/data-sources.md` - Recommended enrichment tools and data points to gather.
- `references/examples.md` - Best practices, trigger phrases, and an example request.

## Workflow

1. Collect the best customers provided. If none are given, ask for the top 5-10 accounts.
2. Analyze common characteristics across them. See `references/scoring-model.md` for the five profile dimensions.
3. Build the Ideal Customer Profile (ICP) from those shared traits.
4. Search the market for companies matching the ICP. Pull firmographics, tech stack, growth signals, and contacts from the tools in `references/data-sources.md`.
5. Score each candidate 0-100 using the weighted scoring model in `references/scoring-model.md`.
6. Rank and tier the companies by score (Tier 1: top 10, Tier 2: next 40, Tier 3: next 50).
7. Produce the report following `references/output-template.md`, including market insights, a tiered targeting strategy, and a quick-start action plan.
8. Apply the best practices in `references/examples.md` throughout: favor quality over quantity, weight growth signals, and enrich contacts before recommending outreach.
