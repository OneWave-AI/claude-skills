# Pipeline Health Analysis Output Template

Produce the report in this structure. Replace bracketed placeholders with real values. Use plain status words (Healthy / At Risk / Critical) and plain trend words (Up / Flat / Down). Do not use emoji.

```markdown
# Pipeline Health Analysis

**Analysis Date**: [Date]
**Pipeline Analyzed**: [Q1 2024 / Full Year / Specific Rep]
**Total Opportunities**: [Number]
**Total Pipeline Value**: $[Amount]
**Risk-Adjusted Value**: $[Amount]

---

## Executive Summary

**Overall Pipeline Health**: [Healthy / At Risk / Critical]

**Key Findings**:
- [Positive finding 1 with metric]
- [Concern 1 with metric]
- [Critical issue with metric]

**Bottom Line**: [2-3 sentence summary of pipeline state and urgency]

**Forecast Confidence**: [High/Medium/Low] - [Explain reasoning]

---

## Pipeline Overview

### Pipeline by Stage

| Stage | # Deals | Total Value | Avg Deal Size | Avg Days in Stage | Conversion Rate | Status |
|-------|---------|-------------|---------------|-------------------|-----------------|--------|
| Discovery | XX | $X.XM | $XXK | XX days | XX% to Next | Healthy/At Risk/Critical |
| Demo | XX | $X.XM | $XXK | XX days | XX% to Next | Healthy/At Risk/Critical |
| Proposal | XX | $X.XM | $XXK | XX days | XX% to Next | Healthy/At Risk/Critical |
| Negotiation | XX | $X.XM | $XXK | XX days | XX% to Closed | Healthy/At Risk/Critical |
| **Total** | **XXX** | **$X.XM** | **$XXK** | **XX days avg** | **XX% overall** | |

**Stage Health Indicators**:
- Healthy: Moving at or above benchmark velocity
- At Risk: Slower than benchmark, needs attention
- Critical: Significant slowdown, immediate action required

**Benchmarks** (based on historical data):
- Discovery to Demo: [X] days average
- Demo to Proposal: [X] days average
- Proposal to Negotiation: [X] days average
- Negotiation to Closed: [X] days average

---

## Deals Requiring Immediate Attention

### Critical - High Value Stalled Deals ([N] deals)

#### Deal #1: [Company Name] - $[Amount]

**Why It's Critical**:
- Deal size: $[Amount] ([X]% of quarter)
- Stalled in [Stage] for [X] days ([X]x longer than average)
- No activity in last [X] days
- Close date slipped [X] times
- At risk of being lost to [competitor/status quo]

**Deal Details**:
- **Rep**: [Name]
- **Stage**: [Current stage]
- **Days in Stage**: [Number] (benchmark: [X] days)
- **Deal Age**: [Number] days total
- **Last Activity**: [Date] - [Type of activity]
- **Close Date**: [Date] (originally [Date])
- **Probability**: [X]% (down from [X]% last month)

**Symptoms of Stall**:
- [Symptom 1: e.g., "Champion stopped responding"]
- [Symptom 2: e.g., "Can't get meeting with economic buyer"]
- [Symptom 3: e.g., "Competitor mentioned for first time"]

**Root Cause Analysis**:
- **Primary Issue**: [What's really causing the stall]
- **Contributing Factors**: [Secondary issues]
- **Pattern**: [Have we seen this before? What happened?]

**Recommended Actions** (Prioritized):
1. **[Immediate Action]** (Do Today)
   - **What**: [Specific action to take]
   - **Why**: [Why this will help]
   - **How**: [Tactical approach]
   - **Expected Outcome**: [What you'll learn/achieve]

2. **[Short-term Action]** (This Week)
   - **What**: [Specific action]
   - **Who**: [Who should be involved]
   - **Success Metric**: [How to measure]

3. **[Backstop]** (If 1 & 2 Don't Work)
   - **What**: [Last-ditch effort or disqualification]
   - **Timing**: [When to execute]

**Re-engagement Email Template**: see references/email-templates.md

**Escalation Path**:
- If no response in 3 business days, [Manager reaches out to their executive]
- If still no response, [Consider disqualifying]

**Forecast Recommendation**:
- Move from [Current %] to [New %] probability
- Flag as "At Risk" in forecast call
- Develop backup deals to cover potential loss

---

#### Deal #2: [Company Name] - $[Amount]

[Repeat structure for each critical deal]

---

### At Risk - Deals Losing Momentum ([N] deals)

**Common Patterns**:
- [X] deals stuck in Demo stage for 30+ days
- [X] deals with decreasing engagement (less frequent contact)
- [X] deals with upcoming close dates but missing key milestones
- [X] deals where champion has gone silent

**Bulk Actions to Consider**:
1. **Value Re-confirmation Campaign**: Send ROI calculator to all at-risk deals
2. **Executive Engagement**: Get your VP to reach out to their C-level
3. **Event Invitation**: Invite to exclusive webinar/dinner to re-engage
4. **Competitive Intelligence**: Share relevant case study of competitor customer switching to you

**Individual Deal Summary**:

| Deal | Value | Stage | Days Stalled | Issue | Recommended Action |
|------|-------|-------|--------------|-------|-------------------|
| [Company 1] | $XXK | Demo | 45 | Can't get 2nd meeting | Multi-thread: Find another contact |
| [Company 2] | $XXK | Proposal | 32 | Awaiting legal review | Offer to connect legal teams directly |
| [Company 3] | $XXK | Discovery | 28 | "We're busy with X" | Create urgency: Limited time offer |

[Continue for all at-risk deals]

---

## Probability Analysis & Forecast

Insert the current forecast table, probability calibration, AI-driven re-scoring, and the three scenarios here. See references/forecasting.md for the full tables and assumptions.

---

## Stage-Specific Analysis

Insert a per-stage deep dive (Discovery, Demo, Proposal) here when stage-level data is available. See references/stage-analysis.md for the structure.

---

## Strategic Recommendations

### Immediate Actions (This Week)

1. **Address [X] Critical Stalled Deals**
   - **Owner**: [Sales Manager]
   - **Action**: Personal outreach to top [X] stalled deals
   - **Goal**: Get meetings rescheduled or disqualify
   - **Impact**: $[X]M at risk

2. **Demo Stage Intervention**
   - **Owner**: [Sales Enablement]
   - **Action**: Audit next [X] demos for "right people" attendance
   - **Goal**: Increase Demo to Proposal conversion from [X]% to [X]%
   - **Impact**: [X] more deals per month

3. **Forecast Recalibration**
   - **Owner**: [Sales Ops]
   - **Action**: Review AI probability adjustments with reps
   - **Goal**: Improve forecast accuracy by [X]%
   - **Impact**: Better planning and resource allocation

---

### Short-term Actions (This Month)

4. **Implement Stage Duration Alerts**
   - Set automatic alerts when deals exceed benchmark time in stage
   - Manager reviews all deals >30 days in any stage

5. **Multi-Threading Initiative**
   - Deals with only 1 contact have [X]% lower close rate
   - Require 3+ contacts per deal in CRM
   - Train reps on "economic buyer" access strategies

6. **Competitor Win/Loss Analysis**
   - [X] deals lost to [Competitor] in last 90 days
   - Interview lost prospects to understand why
   - Adjust competitive positioning

---

### Long-term Improvements (This Quarter)

7. **Optimize Deal Stages**
   - Current 5-stage pipeline may need adjustment
   - Consider: Discovery -> Technical Validation -> Business Case -> Proposal -> Negotiation
   - Clearer exit criteria for each stage

8. **Predictive Deal Scoring**
   - Build model on historical win/loss data
   - Auto-score deals weekly on health dimensions
   - Surface at-risk deals before reps recognize them

9. **Sales Process Consistency**
   - [X]% variation in how reps work deals
   - Document best practices from top performers
   - Create playbooks for each stage

---

## Pipeline Health Report Card

| Metric | Current | Target | Status | Trend |
|--------|---------|--------|--------|-------|
| Overall Pipeline Value | $X.XM | $X.XM | Healthy/At Risk/Critical | Up/Flat/Down |
| Weighted Pipeline | $X.XM | $X.XM | Healthy/At Risk/Critical | Up/Flat/Down |
| # Deals in Pipeline | XXX | XXX | Healthy/At Risk/Critical | Up/Flat/Down |
| Avg Deal Size | $XXK | $XXK | Healthy/At Risk/Critical | Up/Flat/Down |
| Avg Sales Cycle | XX days | XX days | Healthy/At Risk/Critical | Up/Flat/Down |
| Win Rate | XX% | XX% | Healthy/At Risk/Critical | Up/Flat/Down |
| Forecast Accuracy | XX% | XX% | Healthy/At Risk/Critical | Up/Flat/Down |
| Stage Conversion | XX% | XX% | Healthy/At Risk/Critical | Up/Flat/Down |

**Overall Grade**: [A/B/C/D/F]

---

## Next Pipeline Review

**Schedule next review for**: [Date, 1 week from now]

**Focus areas for next review**:
- Status update on [X] critical stalled deals
- Demo stage conversion rate (target: improve to [X]%)
- New deals added to top of funnel
- Forecast accuracy check

**KPIs to track week-over-week**:
- Deals moved to Commit status
- Deals closed vs. forecast
- Deals disqualified (healthy pipeline management)
- New opportunities created
```
