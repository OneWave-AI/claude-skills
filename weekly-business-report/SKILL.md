---
name: weekly-business-report
description: Auto-generates weekly KPI reports from multiple data sources including Supabase analytics, CRM data, financial spreadsheets, and email metrics. Produces executive-ready reports with dashboards, trends, highlights, concerns, and action items.
tools: Read, Write, Bash, Glob, Grep, WebSearch
model: inherit
---

# Weekly Business Report Generator

Pull data from multiple business systems, synthesize it into a coherent narrative, and produce an executive-ready weekly report that turns raw numbers into strategic insight.

## Contents

- `references/configuration.md` — first-run setup questions, directory layout, full `config.yaml`, and `kpi-history.json` schema.
- `references/data-and-calculations.md` — per-source data collection, trend indicators, target comparison, rolling averages, anomaly detection, comparison modes, custom KPI groups, quality rules, and error handling.
- `references/output-template.md` — the full report markdown template and detail levels.

## Workflow

### First run (no configuration exists)

1. Run the setup questions and create the directory layout. See `references/configuration.md`.
2. Generate `config.yaml` and `templates/kpi-definitions.yaml` from the schema in `references/configuration.md`.
3. Initialize `history/kpi-history.json` using the schema in `references/configuration.md`.

### Each subsequent run

1. Read `config.yaml` and `templates/kpi-definitions.yaml`.
2. Determine the reporting period (the previous full business week).
3. Pull data from each enabled source and snapshot it to `data/{date}/`. See `references/data-and-calculations.md`.
4. Calculate every KPI: trend indicators, target comparison, rolling averages, and anomalies. See `references/data-and-calculations.md`.
5. Compare against targets and prior weeks; flag anomalies.
6. Generate the report from the template in `references/output-template.md`, tailored to each recipient's detail level.
7. Save the report to `reports/{date}-weekly-report.md` and append this week's values to `history/kpi-history.json`.

## Quick Commands

- "Generate this week's report" — full report for the most recent complete week.
- "Show me revenue trends" — revenue-specific trend analysis with 4-8 week history.
- "What are the concerns this week?" — concerns-only output.
- "Add KPI [name]" — add a new KPI to tracking (see custom KPI groups in `references/data-and-calculations.md`).
- "Update targets" — modify target values for existing KPIs.
- "Compare last 4 weeks" — side-by-side comparison of the last 4 weekly reports.
- "YTD summary" — year-to-date summary across all tracked KPIs.

Apply the report quality rules and error handling in `references/data-and-calculations.md` to every run.
