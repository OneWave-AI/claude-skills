---
name: pipeline-health-analyzer
description: Analyze pipeline health, identify stalled deals, predict close probability, and suggest actions to move deals forward. Improves forecast accuracy and prevents revenue leakage. Use when deals get stuck or forecast accuracy is poor.
---

# Pipeline Health Analyzer

Identify pipeline risks, predict deal outcomes, and prescribe specific actions to accelerate stalled opportunities.

## Contents

- references/output-template.md - Full report skeleton to populate.
- references/stage-analysis.md - Per-stage deep-dive patterns (Discovery, Demo, Proposal) and why deals stall.
- references/forecasting.md - Forecast tables, probability calibration, AI re-scoring, scenario planning.
- references/email-templates.md - Re-engagement email templates for stalled and dark deals.
- references/examples.md - Trigger phrases, a worked example request, and best practices.

## Workflow

1. Obtain the pipeline data. Request a CSV export with deal name, stage, value, rep, deal age, days in current stage, last activity date, close date, and probability if not provided.
2. Compute pipeline-by-stage metrics: deal count, total value, average deal size, average days in stage, and stage-to-stage conversion rates. Compare each against historical benchmarks.
3. Score each deal across six health dimensions: stage velocity, engagement level, qualification depth, stakeholder coverage, competitive position, and 30-day momentum.
4. Identify stalled and at-risk deals. Flag deals exceeding benchmark time in stage, with no recent activity, with slipped close dates, or with single-threaded contacts.
5. For each critical deal, determine the root cause and prescribe prioritized actions (immediate, this-week, backstop). Pull re-engagement copy from references/email-templates.md.
6. Build the forecast: categorize deals (Commit/Best Case/Pipeline/Upside), calculate weighted and risk-adjusted value, check probability calibration against actual close rates, and re-score outliers. Follow references/forecasting.md.
7. Model best-case, expected, and worst-case scenarios against quota, with a mitigation plan for the downside.
8. Produce strategic recommendations across immediate, short-term, and long-term horizons.
9. Assemble the report using references/output-template.md. Use plain status words (Healthy / At Risk / Critical) and trend words (Up / Flat / Down); never use emoji.
10. Close with the report card, next-review date, and week-over-week KPIs to track.

## Operating Principles

- Run weekly, not monthly; pipeline health degrades fast.
- Base assessments on activity metrics, not rep intuition.
- Disqualify dead deals early; a flowing pipeline is healthy.
- Always end with concrete next steps, not just analysis.
- Coach with the insights; do not weaponize them against reps.

See references/examples.md for trigger phrases, a worked example, and the full best-practices list.
