# Data Collection and KPI Calculations

## Data Collection by Source

### Supabase
1. Use the Supabase connection details from config.
2. Query the specified tables for the reporting period.
3. Common queries:
   - New user signups: `SELECT COUNT(*) FROM auth.users WHERE created_at >= [start] AND created_at < [end]`
   - Active users: `SELECT COUNT(DISTINCT user_id) FROM events WHERE created_at >= [start] AND created_at < [end]`
   - Subscriptions: `SELECT plan, COUNT(*), SUM(amount) FROM subscriptions WHERE status = 'active'`
4. Store raw query results in `data/{date}/`.

### Spreadsheets (Financial)
1. Read the spreadsheet file (CSV, XLSX).
2. Parse relevant columns and rows for the reporting period.
3. Extract revenue figures, expense categories, and financial metrics.
4. Store parsed data in `data/{date}/financial.json`.

### CRM
1. Query the CRM for the reporting period.
2. Extract pipeline data: new leads, qualified opportunities, closed deals.
3. Calculate conversion rates between pipeline stages.
4. Store in `data/{date}/pipeline.json`.

### Manual Data Entry
1. Present the user with the list of manual KPIs needing values.
2. Accept input as `KPI Name: Value`.
3. Store in `data/{date}/manual.json`.
4. Track which KPIs are manual vs automated for future automation recommendations.

## Trend Indicators

For each KPI, compute and display a trend indicator:

- `[UP]` Value increased week-over-week (include % change)
- `[DOWN]` Value decreased week-over-week (include % change)
- `[FLAT]` Value changed less than 2% week-over-week
- `[NEW]` First week tracking this KPI (no comparison available)

## Target Comparison

For KPIs with targets:

- `[ON TRACK]` Within 10% of target pace
- `[AHEAD]` More than 10% above target pace
- `[BEHIND]` More than 10% below target pace
- `[AT RISK]` More than 25% below target pace

## Rolling Averages and Aggregates

Compute and display:

- 4-week rolling average (smooths weekly volatility)
- Week-over-week change (absolute and percentage)
- Month-to-date total (for cumulative metrics like revenue)
- Quarter-to-date total
- Year-to-date total (where applicable)

## Anomaly Detection

Flag KPIs showing unusual behavior:

- Value more than 2 standard deviations from the 4-week average
- Sudden reversal of a multi-week trend
- New all-time high or low
- Missing data (source unavailable)

## Comparison Modes

- Week-over-Week: default comparison
- Month-over-Month: for monthly metrics
- Year-over-Year: for seasonal businesses
- vs Plan: compare actual to planned/budgeted numbers
- vs Cohort: compare against a reference cohort (e.g., same week last year)

## Custom KPI Groups

To define a custom KPI group beyond the defaults, collect:

1. KPI name and description
2. Data source and query/formula
3. Target value and measurement unit
4. Trend direction preference (higher is better vs lower is better)
5. Alert thresholds

## Report Quality Rules

1. Numbers are king. Back every claim with specific data. State "revenue increased 12% to $47,500", not "revenue improved".
2. Context over data. Always include comparison (WoW, vs target, vs 4-week average).
3. Lead with insight. The executive summary tells the story, not just the dashboard. State what the data means for the business.
4. Honest assessment. Do not sugarcoat bad numbers. Frame concerns constructively but do not hide them.
5. Actionable recommendations. Every concern gets a suggested action. Every trend gets an implication.
6. Consistent format. Use the same structure every week.
7. Brevity for executives. Executive summary and dashboard read in under 2 minutes. Details go below.
8. Source transparency. Note where data came from and flag any gaps.

## Error Handling

- Data source unavailable: note it in the report, use most recent available data with a staleness warning.
- Missing KPIs: generate the report with available data, list missing KPIs in the appendix.
- Calculation errors: flag the affected KPI, show raw data, note the error.
- No historical data: generate the report without trend analysis, note it is the first report in the series.
- Partial data: generate the report with what is available, clearly mark sections based on partial data.
