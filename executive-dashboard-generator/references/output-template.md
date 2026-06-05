# Output Template

Use this Markdown structure for the generated dashboard. Replace bracketed placeholders with real values. Use the text status labels On Track, Monitor, and Attention Needed instead of colored indicators.

```markdown
# Executive Dashboard: [Report Title]
**Period**: [Date Range] | **Generated**: [Date] | **Status**: [Attention Needed / Monitor / On Track]

---

## Executive Summary

**Overall Performance**: [One-sentence verdict]

**Key Highlights**:
- [Positive achievement with metric]
- [Another win with specific number]
- [Area of concern with context]
- [Critical issue requiring attention]

**Bottom Line**: [Two-sentence conclusion with action needed]

---

## Critical Metrics Dashboard

### Performance Scorecard

| Metric | Current | Previous Period | Change | Target | Status |
|--------|---------|----------------|--------|--------|--------|
| Revenue | $X.XM | $X.XM | +X% | $X.XM | On Track |
| Customers | X,XXX | X,XXX | +X% | X,XXX | On Track |
| Churn Rate | X.X% | X.X% | -X% | <X% | Monitor |
| CAC | $XXX | $XXX | +X% | $XXX | Attention Needed |
| Burn Rate | $XXX K | $XXX K | -X% | $XXX K | On Track |

**Key**: On Track = On/Above Target | Monitor | Attention Needed = Below Target

---

## Trend Analysis

### Revenue Trajectory

```
visualization: line chart
x-axis: months
y-axis: revenue
data points: [detailed monthly data]
trend line: included
annotation: highlight significant events
```

**Insight**: [2-3 sentences explaining the trend, what's driving it, and projection]

**Chart Description**: Revenue has grown X% QoQ, from $X.XM in [Month] to $X.XM in [Month]. The acceleration in [specific month] was driven by [reason]. At current growth rate, we project $X.XM by [future date].

---

### Customer Acquisition & Retention

```
visualization: dual-axis chart
left y-axis: new customers (bars)
right y-axis: churn rate (line)
x-axis: months
```

**Insight**: [Analysis of acquisition vs. retention balance]

**Key Finding**: New customer acquisition is [strong/weak/steady] at XXX per month (+X% MoM), but churn increased to X.X% in [month], driven by [specific reason from data]. Net customer growth is XXX per month.

---

### Channel Performance

```
visualization: stacked bar chart or treemap
categories: [Marketing channels]
metric: revenue contribution and ROI
```

| Channel | Revenue | % of Total | Cost | ROI | Trend |
|---------|---------|-----------|------|-----|-------|
| Organic Search | $XXX K | XX% | $X K | XX:1 | Up |
| Paid Social | $XXX K | XX% | $XX K | X:1 | Down |
| Direct | $XXX K | XX% | $X K | N/A | Flat |
| Referral | $XXX K | XX% | $X K | XX:1 | Up |
| Email | $XXX K | XX% | $X K | XX:1 | Flat |

**Insight**: [Which channels are performing, which need optimization]

---

## Deep Dive: [Most Important Finding]

### The Issue/Opportunity

**What We're Seeing**: [Describe the pattern or anomaly in data]

**By The Numbers**:
- [Specific metric 1]: [Value] ([% change])
- [Specific metric 2]: [Value] ([% change])
- [Specific metric 3]: [Value] ([% change])

**Why It Matters**: [Business impact and implications]

**Root Cause Analysis**:
1. **Primary Factor**: [What data shows is the main driver]
   - Supporting data: [Specific numbers]
   - Time frame: [When it started/changed]

2. **Contributing Factors**:
   - [Factor 2 with evidence]
   - [Factor 3 with evidence]

**Projected Impact**: If trend continues, [describe future state with numbers]

---

## Strategic Recommendations

### Priority 1: [Action Item Title] (URGENT)

**Situation**: [What the data shows]
**Action**: [Specific recommendation]
**Expected Impact**: [Projected improvement with numbers]
**Timeline**: [When to implement and see results]
**Owner**: [Recommended department/role]
**Resources Required**: [Budget, people, tools needed]

**Supporting Data**:
- [Metric 1] currently at [value], target is [value]
- [Metric 2] trending [direction], showing [pattern]
- Industry benchmark is [value], we're at [value]

---

### Priority 2: [Action Item Title] (IMPORTANT)

**Situation**: [What the data shows]
**Action**: [Specific recommendation]
**Expected Impact**: [Projected improvement]
**Timeline**: [Implementation timeline]
**Owner**: [Department/role]
**Resources Required**: [What's needed]

---

### Priority 3: [Action Item Title] (OPPORTUNITY)

**Situation**: [What the data shows]
**Action**: [Specific recommendation]
**Expected Impact**: [Projected improvement]
**Timeline**: [Timeline]
**Owner**: [Department/role]

---

## Departmental Scorecards

### Sales Performance

| Metric | Current | Target | Status | Insight |
|--------|---------|--------|--------|---------|
| Pipeline Value | $X.XM | $X.XM | On Track | Up X% from last quarter |
| Win Rate | XX% | XX% | Monitor | Declined X% due to [reason] |
| Sales Cycle | XX days | XX days | On Track | Improved by X days |
| Avg Deal Size | $XX K | $XX K | Attention Needed | Down X% need pricing review |

**Overall**: [One sentence summary of sales health]

---

### Marketing Performance

| Metric | Current | Target | Status | Insight |
|--------|---------|--------|--------|---------|
| Leads Generated | X,XXX | X,XXX | On Track | X% above target |
| MQL Conversion | XX% | XX% | Monitor | Quality needs improvement |
| CAC | $XXX | $XXX | Attention Needed | Up X% from paid channels |
| Website Traffic | XXX K | XXX K | On Track | Organic growth strong |

**Overall**: [One sentence summary of marketing performance]

---

### Customer Success

| Metric | Current | Target | Status | Insight |
|--------|---------|--------|--------|---------|
| NPS Score | XX | XX | On Track | Improved X points |
| Churn Rate | X.X% | X.X% | Attention Needed | Above target, investigate |
| Support SLA | XX% | XX% | On Track | Meeting commitments |
| Expansion Revenue | $XXX K | $XXX K | Monitor | Slightly below plan |

**Overall**: [One sentence summary of CS health]

---

## Scenario Planning

### Best Case Scenario (25% probability)

**Assumptions**: [What needs to go right]
**Projected Outcomes**:
- Revenue: $X.XM (X% growth)
- Customers: X,XXX (X% growth)
- [Other key metrics]

**Triggers**: [Early indicators this is happening]

---

### Expected Scenario (50% probability)

**Assumptions**: [Current trends continue]
**Projected Outcomes**:
- Revenue: $X.XM (X% growth)
- Customers: X,XXX (X% growth)
- [Other key metrics]

**Confidence Level**: [High/Medium based on data stability]

---

### Risk Scenario (25% probability)

**Assumptions**: [What concerns materialize]
**Projected Outcomes**:
- Revenue: $X.XM (X% growth/decline)
- Customers: X,XXX (X% growth/decline)
- [Other key metrics]

**Mitigation Plans**: [What to do if this happens]

---

## Risk Flags

### High Risk

**[Risk Title]**
- **Severity**: High
- **Data Signal**: [Specific metric and threshold]
- **Impact**: [Business consequence if not addressed]
- **Recommendation**: [Immediate action required]

### Medium Risk

**[Risk Title]**
- **Severity**: Medium
- **Data Signal**: [What data is showing]
- **Impact**: [Potential consequence]
- **Recommendation**: [Action to monitor/address]

---

## Next Period Outlook

### Goals for [Next Period]

**Primary Objectives**:
1. [Objective 1] - Target: [Specific metric goal]
2. [Objective 2] - Target: [Specific metric goal]
3. [Objective 3] - Target: [Specific metric goal]

**Key Initiatives to Support Goals**:
- [Initiative 1]: [Expected impact]
- [Initiative 2]: [Expected impact]
- [Initiative 3]: [Expected impact]

**Metrics to Watch**:
- [Metric 1]: Current [value], Target [value]
- [Metric 2]: Current [value], Target [value]
- [Metric 3]: Current [value], Target [value]

---

## Appendix: Data Details

### Data Sources
- **Source 1**: [File name, date range, rows]
- **Source 2**: [File name, date range, rows]
- **Last Updated**: [Date and time]

### Methodology
- **Period Comparison**: [How periods are compared]
- **Calculations**: [Any custom formulas or aggregations]
- **Exclusions**: [Any data filtered out and why]
- **Data Quality Notes**: [Any issues or caveats]

### Glossary
- **[Term 1]**: [Definition]
- **[Term 2]**: [Definition]
- **[Term 3]**: [Definition]

---

## Report Metadata

- **Report ID**: [Unique identifier]
- **Version**: [Version number]
- **Created By**: Executive Dashboard Generator (AI)
- **Review By**: [Designated human reviewer]
- **Distribution**: [Who should receive this]
- **Next Report**: [When is next update]
- **Questions**: [Contact for clarifications]
```
