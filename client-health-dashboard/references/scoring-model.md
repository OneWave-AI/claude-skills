# Health Score Calculation

Calculate a composite health score (0-100) for each client using a weighted model. Higher scores indicate healthier accounts.

## Scoring Dimensions

Each dimension is scored 0-100, then weighted:

| Dimension | Weight | Score Criteria |
|-----------|--------|----------------|
| Product Usage | 25% | Login frequency, feature adoption, usage trend, DAU/MAU ratio |
| Support Health | 20% | Open ticket count (inverse), resolution time, escalation frequency, ticket trend |
| Engagement | 20% | Days since contact (inverse), meeting frequency, response rates, touchpoint volume |
| Financial Health | 20% | Payment timeliness, revenue trend, contract value stability |
| Relationship | 15% | Executive sponsor access, NPS/CSAT, sentiment, champion strength |

## Dimension Scoring Rules

Product Usage (0-100):
- 90-100: Daily active usage, high feature adoption (>75%), increasing trend
- 70-89: Weekly active usage, moderate feature adoption (50-75%), stable trend
- 50-69: Monthly active usage, low feature adoption (25-50%), stable/slight decline
- 25-49: Infrequent usage, minimal feature adoption (<25%), declining trend
- 0-24: Near-zero usage, single feature only, sharp decline or dormant

Support Health (0-100):
- 90-100: Zero open tickets, fast resolution (<24h avg), no escalations
- 70-89: 1-2 open tickets (low priority), good resolution (<48h), no recent escalations
- 50-69: 3-5 open tickets, moderate resolution (48-72h), 1 escalation in 90 days
- 25-49: 5-10 open tickets or 1+ critical, slow resolution (>72h), multiple escalations
- 0-24: 10+ open tickets or 3+ critical, very slow resolution (>1 week), frequent escalations

Engagement (0-100):
- 90-100: Contact within last 7 days, weekly meetings, fast response rate
- 70-89: Contact within last 14 days, biweekly meetings, good response rate
- 50-69: Contact within last 30 days, monthly meetings, moderate response rate
- 25-49: Contact 30-60 days ago, infrequent meetings, slow response rate
- 0-24: No contact in 60+ days, no scheduled meetings, unresponsive

Financial Health (0-100):
- 90-100: Payments current, revenue expanding, upsell in progress
- 70-89: Payments current, revenue stable, some expansion potential
- 50-69: Payments current, revenue flat, no expansion signals
- 25-49: Late payments, revenue contracting, discount requests
- 0-24: Severely overdue, significant contraction, cancellation signals

Relationship (0-100):
- 90-100: Strong exec sponsor, NPS 9-10, positive sentiment, active champion
- 70-89: Good exec access, NPS 7-8, neutral-positive sentiment, identified champion
- 50-69: Limited exec access, NPS 5-6, neutral sentiment, weak champion
- 25-49: No exec sponsor, NPS 3-4, negative sentiment, champion departed
- 0-24: Hostile relationship, NPS 0-2, very negative sentiment, no internal allies

## Composite Score

```
health_score = (usage * 0.25) + (support * 0.20) + (engagement * 0.20) + (financial * 0.20) + (relationship * 0.15)
```

## RAG Status Assignment

| RAG Status | Score Range | Meaning |
|------------|-------------|---------|
| RED | 0-39 | Critical risk -- immediate intervention required |
| AMBER | 40-69 | Moderate risk -- proactive attention needed |
| GREEN | 70-100 | Healthy -- maintain current engagement |

## Trend Direction

Compare current health score against the implied trajectory from available data:
- Improving: Usage increasing, tickets decreasing, engagement rising, positive signals
- Stable: Metrics holding steady, no significant changes in any dimension
- Declining: Usage dropping, tickets increasing, engagement falling, negative signals

Determine trend using: usage trend over last 90 days; ticket volume trend; contact frequency trend; revenue trajectory; recent sentiment shifts.
