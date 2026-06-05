# Configuration

## Directory Structure

Create this layout on first run:

```
weekly-reports/
  config.yaml                    # Report configuration
  templates/
    report-template.md           # Report template
    kpi-definitions.yaml         # KPI definitions and targets
  data/
    {date}/                      # Raw data snapshots per week
      revenue.json
      pipeline.json
      marketing.json
      product.json
      support.json
  reports/
    {date}-weekly-report.md      # Generated reports
  history/
    kpi-history.json             # Historical KPI data for trends
```

## First-Run Setup Questions

Guide the user through setup when no configuration exists:

1. Company context: company name and what they sell.
2. Reporting period: which day the business week starts (default: Monday).
3. Data sources available:
   - Supabase database (analytics, user data, events)
   - CRM (HubSpot, Salesforce, or custom)
   - Financial data (spreadsheets, accounting software exports)
   - Email marketing platform (Mailchimp, SendGrid, etc.)
   - Google Analytics or equivalent
   - Stripe or payment processor
   - Support ticket system
   - Custom APIs
4. KPIs that matter most (offer the default set below, let them customize).
5. Distribution: recipient names and roles for tailoring depth.
6. Output directory (default: `./weekly-reports/`).

## config.yaml

```yaml
version: "1.0"
company:
  name: ""
  product: ""
  fiscal_year_start: "January"
  week_start: "Monday"

data_sources:
  supabase:
    enabled: false
    project_id: ""
    tables:
      users: "auth.users"
      events: "public.events"
      subscriptions: "public.subscriptions"
  crm:
    enabled: false
    platform: ""           # hubspot, salesforce, custom
    connection: ""
  financial:
    enabled: false
    source: ""             # spreadsheet path, API endpoint
    format: ""             # csv, xlsx, json
  email:
    enabled: false
    platform: ""           # mailchimp, sendgrid, custom
  analytics:
    enabled: false
    platform: ""           # google-analytics, mixpanel, custom
  payments:
    enabled: false
    platform: ""           # stripe, custom
  support:
    enabled: false
    platform: ""           # intercom, zendesk, custom

kpis:
  revenue:
    - name: "Weekly Revenue"
      source: "payments"
      query: ""
      target: null
      format: "currency"
    - name: "MRR"
      source: "payments"
      query: ""
      target: null
      format: "currency"
    - name: "ARR"
      source: "payments"
      query: ""
      target: null
      format: "currency"
    - name: "Revenue Growth Rate"
      source: "calculated"
      formula: "(current_week_revenue - previous_week_revenue) / previous_week_revenue"
      target: null
      format: "percentage"
  pipeline:
    - name: "New Leads"
      source: "crm"
      query: ""
      target: null
      format: "number"
    - name: "Qualified Opportunities"
      source: "crm"
      query: ""
      target: null
      format: "number"
    - name: "Pipeline Value"
      source: "crm"
      query: ""
      target: null
      format: "currency"
    - name: "Deals Closed"
      source: "crm"
      query: ""
      target: null
      format: "number"
    - name: "Win Rate"
      source: "calculated"
      formula: "deals_won / (deals_won + deals_lost)"
      target: null
      format: "percentage"
  product:
    - name: "Active Users"
      source: "supabase"
      query: ""
      target: null
      format: "number"
    - name: "New Signups"
      source: "supabase"
      query: ""
      target: null
      format: "number"
    - name: "Feature Adoption"
      source: "supabase"
      query: ""
      target: null
      format: "percentage"
    - name: "Churn Rate"
      source: "calculated"
      formula: "churned_users / start_of_week_users"
      target: null
      format: "percentage"
  marketing:
    - name: "Website Visitors"
      source: "analytics"
      query: ""
      target: null
      format: "number"
    - name: "Email Open Rate"
      source: "email"
      query: ""
      target: null
      format: "percentage"
    - name: "Email Click Rate"
      source: "email"
      query: ""
      target: null
      format: "percentage"
    - name: "Content Published"
      source: "manual"
      target: null
      format: "number"
  support:
    - name: "Tickets Opened"
      source: "support"
      query: ""
      target: null
      format: "number"
    - name: "Tickets Resolved"
      source: "support"
      query: ""
      target: null
      format: "number"
    - name: "Avg Resolution Time"
      source: "support"
      query: ""
      target: null
      format: "duration"
    - name: "CSAT Score"
      source: "support"
      query: ""
      target: null
      format: "score"

distribution:
  recipients:
    - name: ""
      role: ""
      detail_level: "executive"   # executive, manager, detailed
  format: "markdown"

schedule:
  day: "Monday"
  time: "08:00"
  timezone: "America/New_York"
```

## kpi-history.json

Maintain `history/kpi-history.json` to enable trend analysis:

```json
{
  "version": "1.0",
  "weeks": [
    {
      "week_start": "2026-04-06",
      "week_end": "2026-04-12",
      "kpis": {
        "weekly_revenue": 0,
        "mrr": 0,
        "arr": 0,
        "new_leads": 0,
        "qualified_opportunities": 0,
        "pipeline_value": 0,
        "deals_closed": 0,
        "win_rate": 0,
        "active_users": 0,
        "new_signups": 0,
        "churn_rate": 0,
        "website_visitors": 0,
        "email_open_rate": 0,
        "tickets_opened": 0,
        "tickets_resolved": 0,
        "avg_resolution_time_hours": 0,
        "csat_score": 0
      },
      "highlights": [],
      "concerns": [],
      "action_items": []
    }
  ]
}
```
