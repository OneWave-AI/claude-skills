---
name: executive-dashboard-generator
description: Transform raw data from CSVs, Google Sheets, or databases into executive-ready reports with visualizations, key metrics, trend analysis, and actionable recommendations. Creates data-driven narratives for leadership. Use when users need to turn spreadsheets into executive summaries or board reports.
---

# Executive Dashboard Generator

Turn raw data into executive-ready insights with visualizations and recommendations.

## Contents

- `references/analysis-coverage.md` — supported data inputs and analysis types per domain (financial, sales/marketing, operations, customer).
- `references/output-template.md` — the full Markdown dashboard template to populate.
- `references/best-practices.md` — reporting principles, visualization do/don't, trigger phrases, example request.

## Workflow

1. Clarify business context and collect the data sources (files, Sheets links, query output). See `references/analysis-coverage.md` for accepted inputs and the analysis types to run per domain.
2. Discover the data: identify structure, date ranges, granularity, key metrics and dimensions, and any data quality issues. Map relationships across datasets.
3. Analyze: calculate period-over-period changes, identify trends and patterns, flag outliers and anomalies, run cohort analysis, and set benchmarks and targets.
4. Generate insights: synthesize findings into key messages, prioritize by business impact, connect each metric to a business outcome, and develop concrete action recommendations and risk/opportunity flags.
5. Choose visualizations: select chart types built for executive readability and maintain a clear visual hierarchy. See `references/best-practices.md` for the visualization do/don't list.
6. Assemble the report using the structure in `references/output-template.md`. Replace every placeholder with real values; never ship a template with bracketed placeholders left in.
7. Prioritize recommendations and include scenario planning and a risk assessment, then deliver the dashboard.

Lead with insights over raw numbers, and answer "So what?" and "What should we do?" Apply the reporting principles in `references/best-practices.md`.
