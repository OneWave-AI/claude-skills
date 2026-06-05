# Output Template

Generate a file named `churn-autopsy.md` in the current working directory (or a user-specified location) using the following structure.

```markdown
# Churn Autopsy: [Client Name]

**Date of Analysis**: [Date]
**Analyst**: Churn Autopsy Skill
**Account Owner**: [CSM/AM Name]
**Final ARR**: [Amount]
**Lifetime Value Realized**: [Amount]
**Client Tenure**: [Duration]
**Churn Effective Date**: [Date]
**Primary Root Cause**: [Category > Subcategory]

---

## Executive Summary

[3-5 paragraph summary covering: who the client was, what happened, why it happened,
what was missed, and the single most important lesson. This should be readable by a
C-level executive in under 2 minutes.]

---

## Account Overview

### Client Profile
[Company description, size, industry, use case, original deal context]

### Contract History
| Date | Event | ARR Impact | Notes |
|------|-------|------------|-------|
| ...  | ...   | ...        | ...   |

### Stakeholder Map
| Name | Role | Relationship | Status at Churn |
|------|------|-------------|-----------------|
| ...  | ...  | ...         | ...             |

### Value Proposition
[What was sold vs what was delivered vs what was needed]

---

## Timeline of Decline

### Visual Timeline
[Month-by-month or week-by-week chronological account of key events, metrics,
and signals organized in a clear timeline format]

### Inflection Points
[Detailed analysis of each major negative shift]

### Point of No Return
[When and why the churn became inevitable]

---

## Root Cause Analysis

### Primary Cause: [Category > Subcategory]
[Detailed explanation with supporting evidence]

### Contributing Factors
| Factor | Category | Weight | Preventable | Evidence |
|--------|----------|--------|-------------|----------|
| ...    | ...      | ...    | ...         | ...      |

### Causal Chain
[How the primary cause and contributing factors interacted to produce the outcome]

---

## Missed Warning Signs

### Signal Inventory
| Signal | First Appeared | Severity | Detected | Acted Upon | Outcome |
|--------|---------------|----------|----------|------------|---------|
| ...    | ...           | ...      | ...      | ...        | ...     |

### Detection Gap Analysis
[Where the monitoring and response systems failed]

### Early Warning Assessment
[How far in advance this churn could have been predicted and what signals
should have triggered intervention]

---

## Counterfactual Analysis

### Intervention Windows
| Window | Date | What Happened | What Should Have Happened | Save Probability |
|--------|------|---------------|--------------------------|-----------------|
| ...    | ...  | ...           | ...                      | ...             |

### Save Attempt Evaluation
[Analysis of any save attempts made]

### Hindsight Playbook
[Step-by-step retention plan that should have been executed]

---

## Lessons Learned

### Process Failures
[Specific breakdowns in existing processes]

### Systemic Patterns
[Connections to broader organizational patterns]

### Recommendations
| # | Recommendation | Owner | Priority | Impact | Complexity | Timeline |
|---|---------------|-------|----------|--------|------------|----------|
| 1 | ...           | ...   | ...      | ...    | ...        | ...      |

---

## At-Risk Account Alert

### Similar Accounts
[Current accounts showing similar patterns]

### Immediate Actions Required
[Specific actions for each at-risk account]

### Monitoring Triggers to Implement
[New automated alerts and thresholds based on this autopsy]

---

## Appendix

### Data Sources Used
[List of all data sources analyzed]

### Data Gaps
[What information was unavailable and how it limited the analysis]

### Methodology Notes
[Any assumptions, estimation methods, or analytical decisions made]
```
