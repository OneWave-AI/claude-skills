# Document Structure

The generated deck MUST follow this structure. Adapt depth and emphasis based on the company stage selected. Stage-specific additions are detailed in `stage-templates.md`.

## 1. COVER

```
# [Company Name] Board of Directors Meeting
## [Quarter] [Year] Update
### [Date of Board Meeting]

**Confidential -- Board Use Only**

Prepared by: [CEO Name], CEO
```

## 2. TABLE OF CONTENTS

A numbered list linking to each major section. Include page/section references.

## 3. EXECUTIVE SUMMARY (1 page equivalent)

The single most important section. Board members who read nothing else will read this.

Structure:
- **One-paragraph narrative**: 3-5 sentences capturing the quarter's story arc. What happened, why it matters, what comes next. No jargon. No spin.
- **Quarterly Scorecard Table**:

| Metric | Q[N-1] Actual | Q[N] Target | Q[N] Actual | Delta | Status |
|--------|---------------|-------------|-------------|-------|--------|
| ARR | | | | | |
| Net New ARR | | | | | |
| Burn Rate | | | | | |
| Runway (months) | | | | | |
| Headcount | | | | | |
| Logo Retention | | | | | |
| NRR | | | | | |

Status uses text labels: ON TRACK, WATCH, OFF TRACK, EXCEEDED.

- **Top 3 Wins**: Bullet points, each one sentence with a quantified result.
- **Top 3 Challenges**: Bullet points, each one sentence with a stated mitigation.
- **Key Asks for the Board**: Numbered list of specific decisions or input needed. This list previews Section 10.

## 4. FINANCIAL REVIEW

The backbone of board credibility. Present numbers cleanly, explain variances honestly.

### 4a. Revenue & ARR

- ARR bridge: Beginning ARR + New ARR + Expansion - Contraction - Churn = Ending ARR
- ARR by segment/cohort if applicable
- Monthly or quarterly revenue trend (trailing 6-12 periods)
- Revenue vs. plan variance with written explanation for any variance exceeding 10%

### 4b. P&L Summary

| Line Item | Q[N] Actual | Q[N] Budget | Variance | Variance % | Commentary |
|-----------|-------------|-------------|----------|------------|------------|
| Revenue | | | | | |
| COGS | | | | | |
| Gross Margin | | | | | |
| S&M Expense | | | | | |
| R&D Expense | | | | | |
| G&A Expense | | | | | |
| Total OpEx | | | | | |
| EBITDA | | | | | |
| Net Burn | | | | | |

### 4c. Cash & Runway

- Cash position (beginning of quarter, end of quarter)
- Burn rate (gross and net)
- Runway in months at current burn
- Runway in months at planned burn (if different)
- Any changes to credit facilities or debt
- If runway < 18 months, include a dedicated fundraising timeline subsection

### 4d. Unit Economics

- CAC (blended and by channel)
- LTV (and LTV/CAC ratio)
- Payback period in months
- Gross margin per customer
- Magic number or burn multiple (for growth-stage and pre-IPO)

## 5. PRODUCT UPDATE

### 5a. Shipped This Quarter

Bulleted list of features/releases with:
- Feature name
- Customer impact (who it serves, what problem it solves)
- Adoption metric if available (% of users, usage volume)

### 5b. Product Roadmap

| Initiative | Priority | Status | Target Ship | Dependencies | Notes |
|-----------|----------|--------|-------------|--------------|-------|
| | | | | | |

Status: SHIPPED, IN PROGRESS, PLANNED, DEPRIORITIZED.

Include a brief written rationale for any deprioritized items, especially those previously committed to the board.

### 5c. Technical Health

- Uptime/SLA performance
- Incident summary (P1/P2 count, MTTR)
- Tech debt status (qualitative assessment: improving, stable, degrading)
- Security posture (any audits, pen tests, certifications completed or planned)

## 6. GO-TO-MARKET METRICS

### 6a. Sales Performance

| Metric | Q[N-1] | Q[N] Target | Q[N] Actual | QoQ Change |
|--------|--------|-------------|-------------|------------|
| Pipeline Generated | | | | |
| Pipeline Coverage (x) | | | | |
| Deals Closed | | | | |
| Win Rate | | | | |
| Average Deal Size | | | | |
| Sales Cycle (days) | | | | |
| Quota Attainment (avg) | | | | |

### 6b. Marketing Performance

| Channel | Spend | Leads | MQLs | SQLs | Opps | Cost/Opp |
|---------|-------|-------|------|------|------|----------|
| | | | | | | |
| **Total** | | | | | | |

### 6c. Customer Success

- Logo retention rate
- Net Revenue Retention (NRR)
- Gross Revenue Retention (GRR)
- NPS or CSAT score and trend
- Expansion revenue as % of new ARR
- Top churn reasons (ranked list)
- Notable customer wins (logos, deal sizes, strategic value)
- Notable customer losses (logo, ARR lost, reason, lessons learned)

## 7. TEAM & HIRING

### 7a. Headcount Summary

| Department | Start of Q | Hires | Departures | End of Q | Plan | Delta to Plan |
|-----------|-----------|-------|------------|---------|------|---------------|
| Engineering | | | | | | |
| Product | | | | | | |
| Sales | | | | | | |
| Marketing | | | | | | |
| CS/Support | | | | | | |
| G&A | | | | | | |
| **Total** | | | | | | |

### 7b. Key Hires & Departures

- List notable hires with title and brief background
- List notable departures with title and reason category (voluntary/involuntary, performance/opportunity/personal)
- Do NOT include names for involuntary departures

### 7c. Organizational Health

- Voluntary attrition rate (annualized)
- Offer acceptance rate
- Open roles and time-to-fill
- Any organizational restructuring completed or planned
- Employee engagement score if measured

## 8. COMPETITIVE LANDSCAPE

- 2x2 or positioning matrix showing company vs. top 2-3 competitors
- Notable competitive moves this quarter (funding, launches, pricing changes, acquisitions)
- Win/loss themes against specific competitors
- Differentiation summary: what is defensible, what is at risk

Keep this section factual and evidence-based. Avoid dismissive language about competitors. Board members often have independent intelligence and will lose trust if this section reads as biased.

## 9. RISK REGISTER

| Risk | Likelihood | Impact | Mitigation | Owner | Status |
|------|-----------|--------|------------|-------|--------|
| | | | | | |

Likelihood: LOW, MEDIUM, HIGH.
Impact: LOW, MEDIUM, HIGH, CRITICAL.
Status: MONITORING, MITIGATING, ESCALATED, RESOLVED.

Include at minimum:
- Market/competitive risks
- Financial risks (runway, revenue concentration)
- Operational risks (key-person dependency, technical)
- Regulatory/compliance risks
- Reputational risks

Be honest. Boards respect transparency. The fastest way to lose board trust is to hide risks they later discover independently.

## 10. STRATEGIC DECISIONS FOR BOARD INPUT

The action section. Each item follows this template:

```
### Decision [N]: [Title]

**Context**: [2-3 sentences on background]

**Options**:
1. [Option A]: [Description, pros, cons, financial impact]
2. [Option B]: [Description, pros, cons, financial impact]
3. [Option C]: [Description, pros, cons, financial impact]

**Management Recommendation**: [Which option and why]

**What We Need From the Board**: [Specific ask -- approve, advise, connect, vote]

**Timeline**: [When decision is needed by]
```

Common decision types:
- Fundraising timing and terms
- Major strategic pivots or market expansion
- M&A opportunities
- Executive hiring (VP+ level)
- Budget reallocation exceeding threshold
- Pricing model changes
- Partnership or channel strategy shifts
- Board composition changes

See `examples.md` for a fully worked example board ask.

## 11. FORWARD LOOK

### 11a. Next Quarter Priorities

Numbered list of top 5-7 priorities with:
- Objective
- Key result / success metric
- Owner

### 11b. Updated Annual Targets

| Metric | Annual Target | YTD Actual | % of Target | On Track? |
|--------|--------------|------------|-------------|-----------|
| | | | | |

### 11c. Key Milestones Next 90 Days

| Milestone | Target Date | Owner | Dependencies |
|-----------|------------|-------|--------------|
| | | | |

## 12. APPENDIX

Include as needed:
- Detailed financial statements
- Full product roadmap
- Customer list (if appropriate for board audience)
- Org chart
- Cap table summary
- Board vote tracker (resolutions from prior meetings and status)
- Glossary of company-specific terms or metrics
