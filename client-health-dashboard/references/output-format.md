# Report Output Format and Formatting

Write the final report to `client-health-report.md` in the current working directory (or a directory the user specifies).

## Report Structure

The report MUST follow this exact structure:

```markdown
# Client Health Report

**Generated**: [Current date and time]
**Report Period**: [Date range of data analyzed]
**Total Accounts Analyzed**: [Count]
**Data Sources**: [List of sources successfully queried]

---

## Executive Summary

**Overall Portfolio Health**:
- RED accounts: [Count] ([Percentage]%)
- AMBER accounts: [Count] ([Percentage]%)
- GREEN accounts: [Count] ([Percentage]%)

**Total ARR at Risk**: $[Sum of RED + AMBER account ARR]
**Renewals in Next 90 Days**: [Count] (RED: [n], AMBER: [n], GREEN: [n])
**Accounts Requiring Immediate Action**: [Count]

**Key Trends**:
- [Top 3-5 portfolio-wide observations]

**Top Priority Actions**:
1. [Most urgent action item with client name]
2. [Second most urgent]
3. [Third most urgent]
4. [Fourth most urgent]
5. [Fifth most urgent]

---

## RED Accounts -- Immediate Intervention Required

[Sorted by health score ascending (worst first)]

### [Client Name] -- Health Score: [Score]/100 [RED]

| Metric | Value | Status |
|--------|-------|--------|
| **Health Score** | [Score]/100 | RED |
| **Trend** | [Improving/Stable/Declining] | [Direction indicator] |
| **ARR/MRR** | $[Value] | [Status] |
| **Renewal Date** | [Date] | [Days until renewal] |
| **Days Since Last Contact** | [Days] | [Status] |
| **Open Tickets** | [Count] ([Critical count] critical) | [Status] |
| **Usage Trend** | [Description] | [Status] |
| **Account Owner** | [Name] | -- |

**Score Breakdown**:
| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Product Usage | [Score] | 25% | [Weighted] |
| Support Health | [Score] | 20% | [Weighted] |
| Engagement | [Score] | 20% | [Weighted] |
| Financial Health | [Score] | 20% | [Weighted] |
| Relationship | [Score] | 15% | [Weighted] |

**Risk Factors**:
- [Specific risk factor 1]
- [Specific risk factor 2]
- [Additional risk factors as applicable]

**Recommended Actions**:
1. **[Action Title]** -- [Specific description with owner and timeline]
2. **[Action Title]** -- [Specific description with owner and timeline]
3. **[Action Title]** -- [Specific description with owner and timeline]

---

## AMBER Accounts -- Proactive Attention Needed

[Same format as RED accounts, sorted by health score ascending]

---

## GREEN Accounts -- Healthy

[Same format but with expansion opportunity section added]

### [Client Name] -- Health Score: [Score]/100 [GREEN]

[Same metrics table]
[Same score breakdown]

**Expansion Opportunity**: [High/Medium/Low]
- [Specific expansion opportunity details]

**Maintenance Actions**:
1. [Action to maintain health]
2. [Action to pursue expansion]

---

## Renewal Calendar

| Client | Renewal Date | Days Until | Health | ARR | Risk Level |
|--------|-------------|------------|--------|-----|------------|
[All clients sorted by renewal date ascending]

---

## Data Quality Notes

- [List any data sources that were unavailable]
- [List any clients with incomplete data]
- [List any assumptions made due to missing data]
- [List confidence level for scores where data was sparse]
```

## Report Formatting Rules

- Do NOT use emojis anywhere in the report
- Use plain text RAG indicators: `[RED]`, `[AMBER]`, `[GREEN]`
- Format dollar amounts with commas: $1,234,567
- Use YYYY-MM-DD format for all dates
- Sort RED accounts by health score ascending (worst first)
- Sort AMBER accounts by health score ascending (worst first)
- Sort GREEN accounts by health score descending (best first)
- Include all clients even if data is sparse; note data gaps
- Round health scores to nearest integer
- Use em dashes (--) not hyphens for separators in text

## Handling Missing Data

When data is unavailable for a dimension:
- Score that dimension as 50 (neutral) with a note that data was unavailable
- Flag it in the Data Quality Notes section
- Reduce confidence level for that client's overall score
- Recommend data collection as an action item

When an entire data source is unavailable:
- Note it prominently in the Executive Summary
- Adjust all affected dimension scores to 50 (neutral)
- Add a caveat to the report header about reduced confidence
- List specific data gaps in Data Quality Notes
