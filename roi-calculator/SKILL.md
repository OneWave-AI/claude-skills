---
name: roi-calculator
description: Calculate comprehensive ROI for AI implementation projects. Takes current costs, manual process time, team size, and hourly rates. Generates detailed roi-analysis.md with executive summary, cost-benefit tables, sensitivity analysis, break-even timeline, and comparison scenarios. Use when evaluating AI investments, building business cases, or justifying automation spend.
tools: Read, Write, Edit, Bash, Glob, Grep
model: inherit
---

# AI Implementation ROI Calculator

Gather inputs about current operations and produce a comprehensive `roi-analysis.md` with data-backed financial insights and a clear recommendation.

## Contents

- `references/inputs.md` — required and optional inputs, with defaults
- `references/methodology.md` — all calculation formulas and sensitivity/comparison logic
- `references/output-template.md` — full `roi-analysis.md` structure to fill in
- `references/rules-and-protocol.md` — calculation rules, interaction protocol, quality checklist

## Workflow

1. Collect inputs. Gather every required cost, time, and labor input. If any required input is missing, ask for it in one organized message grouped by category. Do not guess. See `references/inputs.md` for the full input list and defaults.
2. Apply defaults. For optional parameters the user omits, use the conservative defaults in `references/inputs.md` and note that defaults were applied.
3. Calculate metrics. Compute time savings, cost savings, net monthly savings, ramp-up adjustment, payback period, 12-month ROI, NPV, and productivity gain using the formulas in `references/methodology.md`.
4. Run sensitivity and comparison scenarios. Produce conservative/base/optimistic cases and at least three comparison scenarios per `references/methodology.md`.
5. Generate the report. Write `roi-analysis.md` to the current working directory following `references/output-template.md`. Apply the formatting and calculation rules in `references/rules-and-protocol.md`.
6. Verify and summarize. Run the quality checklist in `references/rules-and-protocol.md`, then report the top 3 findings and the saved file path.
