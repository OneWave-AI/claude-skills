# Tracking Directory Structure and Config

## Directory layout

Create this structure under the chosen output directory (default `./competitor-intel/`):

```
competitor-intel/
  config.yaml                    # Monitoring configuration
  competitors/
    {competitor-slug}/
      profile.yaml               # Company profile and metadata
      snapshots/
        {date}-pricing.md        # Historical pricing snapshots
        {date}-features.md       # Historical feature snapshots
        {date}-content.md        # Historical content snapshots
        {date}-jobs.md           # Historical job posting snapshots
      changes/
        {date}-changes.md        # Detected changes log
  reports/
    {date}-intel-report.md       # Generated intelligence reports
    {date}-alert.md              # Urgent change alerts
  trends/
    pricing-trends.md            # Longitudinal pricing analysis
    feature-trends.md            # Feature evolution tracking
    content-trends.md            # Content strategy analysis
    hiring-trends.md             # Hiring pattern analysis
  usage-history.json             # Run history and tracking metadata
```

## config.yaml template

```yaml
version: "1.0"
created: "2026-06-05"
company:
  name: ""
  description: ""
  website: ""

competitors:
  - slug: ""
    name: ""
    domain: ""
    pricing_url: ""
    features_url: ""
    blog_url: ""
    careers_url: ""
    social:
      twitter: ""
      linkedin: ""
    notes: ""

monitoring:
  dimensions:
    pricing: true
    features: true
    content: true
    hiring: true
    social: false
    technical: false

schedule:
  frequency: weekly
  last_run: null
  next_run: null
```

## usage-history.json template

Maintain `usage-history.json` to track runs:

```json
{
  "version": "1.0",
  "runs": [
    {
      "id": "run-001",
      "timestamp": "2026-06-05T00:00:00Z",
      "mode": "monitoring",
      "competitors_checked": ["competitor-a", "competitor-b"],
      "dimensions_checked": ["pricing", "features", "content", "hiring"],
      "changes_detected": 5,
      "critical_alerts": 1,
      "report_path": "reports/2026-06-05-intel-report.md",
      "errors": []
    }
  ],
  "stats": {
    "total_runs": 1,
    "total_changes_detected": 5,
    "total_critical_alerts": 1,
    "avg_changes_per_run": 5.0,
    "most_active_competitor": "competitor-a",
    "most_volatile_dimension": "pricing"
  }
}
```
