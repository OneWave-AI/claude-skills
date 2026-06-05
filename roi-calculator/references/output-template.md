# Output Template

Generate a file called `roi-analysis.md` in the current working directory using the structure below. Use proper Markdown tables. Include dollar signs and commas on all currency values and the % symbol on all percentages. No emoji anywhere in the output.

```markdown
# AI Implementation ROI Analysis

**Prepared**: [Current Date]
**Analysis Period**: [N] Months
**Organization**: [Company name if provided, otherwise "Your Organization"]

---

## Executive Summary

[3-5 sentence summary of the key findings. Lead with the headline ROI number. State the payback period. Mention the most significant benefit. Include a clear recommendation: Proceed, Proceed with Caution, or Do Not Proceed.]

### Key Metrics at a Glance

| Metric | Value |
|--------|-------|
| 12-Month ROI | [X]% |
| Payback Period | [X] months |
| Monthly Net Savings | $[X] |
| Annual Net Savings | $[X] |
| Total Hours Saved (Annual) | [X] hours |
| Net Present Value (12-month) | $[X] |
| Productivity Gain | [X]% |

---

## 1. Input Parameters

### Current State

| Parameter | Value |
|-----------|-------|
| Team Size | [X] employees |
| Average Hourly Rate (Fully Loaded) | $[X]/hr |
| Hours/Week on Manual Processes | [X] hrs/person |
| Current Monthly Tool Costs | $[X] |
| Current Monthly Error/Rework Cost | $[X] |

### Proposed AI Solution

| Parameter | Value |
|-----------|-------|
| AI Solution Monthly Cost | $[X] |
| One-Time Implementation Cost | $[X] |
| Monthly Maintenance Cost | $[X] |
| Expected Time Reduction | [X]% |
| Expected Error Reduction | [X]% |
| Ramp-Up Period | [X] months |

---

## 2. Cost-Benefit Analysis

### Monthly Savings Breakdown

| Category | Monthly Savings |
|----------|----------------|
| Labor Cost Savings | $[X] |
| Error/Rework Reduction | $[X] |
| Tool Cost Elimination | $[X] |
| Revenue Impact | $[X] |
| **Gross Monthly Savings** | **$[X]** |
| Less: AI Solution Cost | ($[X]) |
| Less: Maintenance Cost | ($[X]) |
| **Net Monthly Savings** | **$[X]** |

### Annual Cost Comparison

| Cost Category | Without AI (Annual) | With AI (Annual) | Difference |
|--------------|--------------------:|------------------:|-----------:|
| Labor (manual processes) | $[X] | $[X] | $[X] |
| Software/Tools | $[X] | $[X] | $[X] |
| Error/Rework | $[X] | $[X] | $[X] |
| AI Solution | $0 | $[X] | ($[X]) |
| Maintenance | $0 | $[X] | ($[X]) |
| **Total** | **$[X]** | **$[X]** | **$[X]** |

---

## 3. Monthly Projection

[Table showing month-by-month for the full analysis period]

| Month | Monthly Savings | Cumulative Savings | Cumulative vs. Implementation Cost |
|------:|----------------:|-------------------:|-----------------------------------:|
| 1 | $[X] | $[X] | ($[X]) or $[X] |
| 2 | $[X] | $[X] | ($[X]) or $[X] |
| ... | ... | ... | ... |
| 12 | $[X] | $[X] | $[X] |

[Mark the payback month clearly with bold formatting.]

---

## 4. Break-Even Timeline

**Break-even point: Month [X]**

[2-3 sentences explaining the break-even analysis. If break-even is not reached within the analysis period, state this clearly and explain what would need to change.]

### Cumulative Cash Flow

[Text-based chart showing cumulative cash flow over time]

```
Month  | Cumulative Net
-------|------------------
  1    | [bar representation]  ($X)
  2    | [bar representation]  ($X)
  ...
  N    | [bar representation]  $X  <-- Break-even
  ...
  12   | [bar representation]  $X
```

---

## 5. Sensitivity Analysis

### Scenario Comparison

| Metric | Conservative | Base Case | Optimistic |
|--------|------------:|----------:|-----------:|
| Monthly Net Savings | $[X] | $[X] | $[X] |
| Annual Net Savings | $[X] | $[X] | $[X] |
| Payback Period | [X] mo | [X] mo | [X] mo |
| 12-Month ROI | [X]% | [X]% | [X]% |
| NPV (12-month) | $[X] | $[X] | $[X] |

### Variable Impact Analysis

[Show how changing each key variable by +/-20% affects the 12-month ROI]

| Variable | -20% Change | Base | +20% Change | Impact Rating |
|----------|------------:|-----:|------------:|:-------------:|
| Time Reduction % | [X]% ROI | [X]% ROI | [X]% ROI | [High/Med/Low] |
| Team Size | [X]% ROI | [X]% ROI | [X]% ROI | [High/Med/Low] |
| Hourly Rate | [X]% ROI | [X]% ROI | [X]% ROI | [High/Med/Low] |
| AI Solution Cost | [X]% ROI | [X]% ROI | [X]% ROI | [High/Med/Low] |
| Ramp-Up Period | [X]% ROI | [X]% ROI | [X]% ROI | [High/Med/Low] |

---

## 6. Comparison Scenarios

### Scenario 1: Do Nothing (Status Quo)

| Metric | Year 1 | Year 2 | Year 3 |
|--------|-------:|-------:|-------:|
| Manual Labor Cost | $[X] | $[X] | $[X] |
| Tool Costs | $[X] | $[X] | $[X] |
| Error/Rework Cost | $[X] | $[X] | $[X] |
| **Total Cost** | **$[X]** | **$[X]** | **$[X]** |

[2-3 sentences on the risk of inaction: growing costs, competitive disadvantage, scaling limitations]

### Scenario 2: Partial Implementation

[Assume 50% of team, primary use case only]

| Metric | Value |
|--------|------:|
| Implementation Cost | $[X] |
| Monthly Net Savings | $[X] |
| Payback Period | [X] months |
| 12-Month ROI | [X]% |

[When partial implementation makes sense vs. full rollout]

### Scenario 3: Full Implementation (Recommended)

| Metric | Value |
|--------|------:|
| Implementation Cost | $[X] |
| Monthly Net Savings | $[X] |
| Payback Period | [X] months |
| 12-Month ROI | [X]% |

[Why full implementation is or is not recommended]

### Scenario 4: Phased Rollout

[Only include if team_size > 10. Show 3-phase approach.]

| Phase | Team | Timeline | Cumulative Savings |
|-------|-----:|:--------:|-----------------:|
| Phase 1: Pilot | [X] people | Months 1-3 | $[X] |
| Phase 2: Expansion | [X] people | Months 4-6 | $[X] |
| Phase 3: Full Rollout | [X] people | Months 7+ | $[X] |

---

## 7. Risk Factors and Assumptions

### Key Assumptions

1. [List each major assumption made in the analysis]
2. [Time reduction percentages are estimates and may vary]
3. [Hourly rates include overhead at standard 1.3x multiplier if estimated]
4. [Ramp-up follows linear progression]
5. [No major organizational changes during implementation]

### Risk Factors

| Risk | Probability | Impact | Mitigation |
|------|:-----------:|:------:|:-----------|
| Adoption resistance | [H/M/L] | [H/M/L] | [Strategy] |
| Integration complexity | [H/M/L] | [H/M/L] | [Strategy] |
| Actual savings below estimate | [H/M/L] | [H/M/L] | [Strategy] |
| Vendor reliability | [H/M/L] | [H/M/L] | [Strategy] |
| Data quality issues | [H/M/L] | [H/M/L] | [Strategy] |
| Scope creep | [H/M/L] | [H/M/L] | [Strategy] |

### What Could Go Wrong

[Honest assessment of 2-3 scenarios where the investment underperforms, and what the financial impact would be in each case]

---

## 8. Recommendations

### Verdict: [PROCEED / PROCEED WITH CAUTION / DO NOT PROCEED]

[3-5 sentences with the final recommendation, supported by the numbers above]

### Recommended Next Steps

1. [Specific action item with timeline]
2. [Specific action item with timeline]
3. [Specific action item with timeline]
4. [Specific action item with timeline]
5. [Specific action item with timeline]

### Success Metrics to Track

| Metric | Baseline | Target (Month 3) | Target (Month 6) | Target (Month 12) |
|--------|:--------:|:-----------------:|:-----------------:|:------------------:|
| Hours on manual tasks/week | [X] | [X] | [X] | [X] |
| Error rate | [X] | [X] | [X] | [X] |
| Monthly cost | $[X] | $[X] | $[X] | $[X] |
| Team satisfaction | Baseline | +[X]% | +[X]% | +[X]% |

---

## Appendix: Calculation Details

### Formulas Used

- **Monthly Labor Savings**: (hours_saved_per_person * 4.33 * team_size) * hourly_rate
- **Net Monthly Savings**: gross_savings - ai_cost - maintenance + tool_cost_elimination
- **Payback Period**: implementation_cost / average_monthly_net_savings (adjusted for ramp)
- **12-Month ROI**: ((total_benefits - total_costs) / total_costs) * 100
- **NPV**: -implementation_cost + SUM(monthly_savings / (1 + r)^month) where r = monthly discount rate
- **Productivity Gain**: (hours_reclaimed / previous_productive_hours) * 100

### Raw Input Values

[List every input value used, including defaults, so the analysis is fully reproducible]
```
