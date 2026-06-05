# Daily Pipeline Report

After processing all emails, generate a daily pipeline report and save it as a local Markdown file.

**Report File:** Save to the current working directory as `lead-pipeline-report.md`.

## Report Structure

```markdown
# Lead Pipeline Report
**Generated:** [Current date and time]
**Period:** [Start date] to [End date]
**Processed by:** Gmail-to-CRM Pipeline Skill

---

## Executive Summary

- **New leads today:** [count]
- **Total pipeline value:** [count of active leads across all stages]
- **Hot leads (P1):** [count] -- RESPOND IMMEDIATELY
- **Warm leads (P2):** [count] -- respond today
- **Cool leads (P3):** [count] -- respond within 48h
- **Unqualified (P4):** [count]
- **Average lead score:** [avg] / 100
- **Drafts ready for review:** [count]

---

## Hot Leads -- Immediate Action Required

### 1. [Contact Name] -- [Company Name] (Score: [X]/100)
- **What they need:** [1-sentence summary]
- **Role:** [Title] | **Company size:** [size] | **Industry:** [industry]
- **Urgency:** [timeline/urgency details]
- **Key quote:** "[Most important sentence from their email]"
- **Draft status:** Ready for review in Gmail Drafts
- **Recommended action:** [specific next step]

[Repeat for each hot lead]

---

## Warm Leads -- Same-Day Response

### 1. [Contact Name] -- [Company Name] (Score: [X]/100)
- **What they need:** [summary]
- **Key qualifying questions to ask:** [2-3 questions]
- **Draft status:** Ready for review
- **Recommended action:** [next step]

[Repeat for each warm lead]

---

## Cool Leads -- Nurture Track

| # | Contact | Company | Score | Type | Next Action |
|---|---------|---------|-------|------|-------------|
| 1 | [name]  | [co]    | [X]   | [type] | [action]  |

---

## Unqualified / Not Leads

| # | Sender | Subject | Reason |
|---|--------|---------|--------|
| 1 | [name] | [subj]  | [why not qualified] |

---

## Pipeline Snapshot (All Active Leads)

| Stage | Count | Avg Score | Oldest Lead |
|-------|-------|-----------|-------------|
| New | [n] | [avg] | [date] |
| Contacted | [n] | [avg] | [date] |
| Qualifying | [n] | [avg] | [date] |
| Proposal | [n] | [avg] | [date] |
| Negotiation | [n] | [avg] | [date] |

**Leads at risk (no activity in 7+ days):**
- [Lead name] -- [company] -- last activity [date] -- [stage]

---

## Score Distribution

- 90-100: [count] leads (exceptional fit)
- 75-89:  [count] leads (strong fit)
- 50-74:  [count] leads (moderate fit)
- 25-49:  [count] leads (low fit)
- 0-24:   [count] leads (not qualified)

---

## Recommendations

1. [Specific actionable recommendation based on today's leads]
2. [Pattern observed -- e.g., "3 leads from fintech this week -- consider targeted content"]
3. [Follow-up reminder -- e.g., "2 warm leads from Monday still unanswered"]
```

## Report Data Sources

To populate the pipeline snapshot and historical data, query Supabase:

```sql
-- Pipeline snapshot by stage
SELECT stage, COUNT(*) as count, AVG(score_total) as avg_score,
       MIN(created_at) as oldest
FROM leads
WHERE stage NOT IN ('won', 'lost')
GROUP BY stage;

-- Leads at risk (no recent activity)
SELECT l.contact_name, l.company_name, l.stage,
       MAX(a.created_at) as last_activity
FROM leads l
LEFT JOIN lead_activity_log a ON a.lead_id = l.id
WHERE l.stage NOT IN ('won', 'lost', 'nurture')
GROUP BY l.id, l.contact_name, l.company_name, l.stage
HAVING MAX(a.created_at) < now() - interval '7 days'
   OR MAX(a.created_at) IS NULL;

-- Score distribution
SELECT
  CASE
    WHEN score_total >= 90 THEN '90-100'
    WHEN score_total >= 75 THEN '75-89'
    WHEN score_total >= 50 THEN '50-74'
    WHEN score_total >= 25 THEN '25-49'
    ELSE '0-24'
  END as range,
  COUNT(*) as count
FROM leads
WHERE created_at > now() - interval '30 days'
GROUP BY range
ORDER BY range DESC;
```
