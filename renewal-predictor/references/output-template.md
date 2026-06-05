# Output Template: renewal-forecast.md

Generate a file called `renewal-forecast.md` in the working directory following this exact structure. Every claim must be supported by evidence. Every recommendation must be actionable and specific.

```
# Renewal Forecast

Generated: [YYYY-MM-DD]
Accounts Analyzed: [N]
Data Sources: [list of sources consulted]

## Executive Summary

[3-5 sentences summarizing the overall portfolio health. Include: number of accounts in each category, total ARR at risk, top systemic themes, and the single most urgent action item.]

## Portfolio Overview

| Account | Health Score | Prediction | Confidence | ARR | Renewal Date | Top Risk Signal | Recommended Action |
|---|---|---|---|---|---|---|---|
| [Account 1] | [0-100] | [Likely to Renew / At Risk / Likely to Churn] | [High/Medium/Low] | [$X] | [YYYY-MM-DD] | [Signal] | [Action] |
| [Account 2] | ... | ... | ... | ... | ... | ... | ... |

## Detailed Assessments

### [Account Name] -- [Prediction Category]

**Health Score: [X]/100 | Confidence: [High/Medium/Low] | ARR: [$X] | Renewal: [YYYY-MM-DD]**

#### Dimension Scores

| Dimension | Score | Weight | Weighted Score | Trend |
|---|---|---|---|---|
| Engagement Frequency | [X] | 20% | [X] | [Up/Stable/Down] |
| Support Ticket Volume/Sentiment | [X] | 15% | [X] | [Up/Stable/Down] |
| Feature Adoption | [X] | 20% | [X] | [Up/Stable/Down] |
| NPS/CSAT | [X] | 10% | [X] | [Up/Stable/Down] |
| Billing History | [X] | 10% | [X] | [Up/Stable/Down] |
| Stakeholder Continuity | [X] | 10% | [X] | [Up/Stable/Down] |
| Usage Trends | [X] | 15% | [X] | [Up/Stable/Down] |
| **Total** | | **100%** | **[X]** | |

#### Active Signals

**Churn Signals:**
- [Signal 1]: [Description with specific data points]
- [Signal 2]: [Description with specific data points]

**Expansion Signals:**
- [Signal 1]: [Description with specific data points]

#### Evidence

[Specific data points, quotes from communications, metrics with dates. Every claim in the assessment must be traceable to evidence listed here.]

#### Recommended Action

**Priority**: [Critical / High / Medium / Low]
**Action**: [Specific intervention with clear next step]
**Owner**: [Role responsible -- CSM, CS Leader, Executive Sponsor, Support Engineering]
**Deadline**: [Date by which the action must be completed]
**Expected Outcome**: [What success looks like if the action is executed]

[Repeat the Detailed Assessment block for every account analyzed.]

## Priority Action List

Ranked list of interventions sorted by urgency and impact. This is the operational output that the CS team should execute against.

| Priority | Account | Action | Owner | Deadline | Risk if Delayed |
|---|---|---|---|---|---|
| 1 | [Account] | [Action] | [Owner] | [Date] | [What happens if this is not done] |
| 2 | [Account] | [Action] | [Owner] | [Date] | [Risk] |
| ... | ... | ... | ... | ... | ... |

## Early Warning Watchlist

Accounts that are currently healthy but showing early signals that could deteriorate. These are not yet at risk but should be monitored more closely over the next 30-60 days.

| Account | Health Score | Warning Signal | Monitoring Cadence | Trigger for Escalation |
|---|---|---|---|---|
| [Account] | [X] | [Signal] | [Weekly/Biweekly] | [What would cause this to move to At Risk] |

## Data Gaps

Accounts or dimensions where insufficient data prevented a confident assessment. These gaps should be filled to improve future forecast accuracy.

| Account | Missing Data | Impact on Assessment | Recommended Collection Method |
|---|---|---|---|
| [Account] | [What is missing] | [How it affected the score] | [How to get this data] |

## Methodology Notes

- Health Score model version: 1.0
- Weights last calibrated: [Date]
- Data coverage period: [Start date] to [End date]
- Known limitations: [Any caveats about data quality, missing sources, or model assumptions]
```
