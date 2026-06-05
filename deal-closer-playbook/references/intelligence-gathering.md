# Intelligence Gathering

Phase 1 detail: deal context intake, company research, buying-committee mapping, and risk assessment.

## Deal Context Intake

Collect the following. Ask for anything not provided. Mark unavailable items as `[UNKNOWN]` and work around them.

**Required**
- Company name
- What is sold (product/service, pricing model)
- Current deal stage (Discovery, Demo, Evaluation, Proposal, Negotiation, Verbal Commit)
- Primary contact name and title
- Deal size (ARR/TCV)
- Target close date

**Highly Valuable**
- Known objections or concerns raised
- Competitors being evaluated
- Champion (who is internally selling for the rep)
- Economic buyer (who signs the check)
- Technical evaluator (who vets the product)
- Known blockers (people, process, or technical)
- Previous interactions summary (calls, demos, emails)
- Procurement process details (legal review, security review, vendor approval)

**Nice to Have**
- Mutual connections or existing relationships
- How the opportunity originated (inbound, outbound, referral, event)
- Budget cycle timing
- Tech stack currently in use
- Decision criteria the buyer has shared
- Timeline pressures or triggering events

## Company Research

Use WebSearch to gather current intelligence on the target company. Cover:

1. **Company overview**: What they do, size, funding, revenue (if public), headquarters, key markets
2. **Recent news**: Last 90 days of press coverage -- funding rounds, product launches, partnerships, leadership changes, layoffs, acquisitions, earnings
3. **Financial signals**: Revenue growth or decline, profitability, recent fundraising, public filings, analyst sentiment
4. **Leadership and hiring**: New C-suite hires (especially CTO, CRO, CFO, COO), board changes, executive departures, job postings that signal strategic priorities
5. **Tech stack signals**: Job postings mentioning specific tools, G2 reviews left, integration partnerships, developer blog posts
6. **Industry context**: Market trends affecting their industry, regulatory changes, competitive dynamics
7. **Company culture and values**: Mission statement, about page, Glassdoor themes, LinkedIn company page

Cast a wide net with queries such as:
- `"[Company Name]" news 2025 2026`
- `"[Company Name]" funding OR acquisition OR partnership`
- `"[Company Name]" [industry] strategy`
- `"[Company Name]" hiring [relevant roles]`
- `site:linkedin.com "[Company Name]" [contact name]`
- `"[Company Name]" reviews OR complaints OR competitors`

## Buying Committee Map

Identify and profile each role in the deal.

| Role | Definition | Key Question |
|---|---|---|
| Champion | Internal advocate who actively sells on the rep's behalf | Who benefits most from this purchase and will fight for it? |
| Economic Buyer | Person with budget authority who signs off on the spend | Who controls the money and makes the final yes/no call? |
| Technical Evaluator | Person who validates the product meets technical requirements | Who will test, integrate, or architect the implementation? |
| User Buyer | End users whose daily work will be affected | Who will use this every day and what do they care about? |
| Coach | Internal informant who shares information about the process | Who is willing to reveal what is really happening behind the scenes? |
| Blocker | Person who opposes the deal or favors a competitor | Who has reasons to say no, and what are those reasons? |
| Procurement/Legal | Process gatekeepers who handle vendor approval | Who reviews the contract, security questionnaire, and terms? |
| Executive Sponsor | Senior leader whose strategic initiative this purchase supports | Which executive's OKRs or strategic goals does this serve? |

Document each identified stakeholder:

```
Name:
Title:
Role in Deal:
Disposition: (Champion / Supportive / Neutral / Skeptical / Hostile)
Key Concern:
Communication Style: (Direct / Analytical / Consensus-driven / Political)
What They Care About:
How to Win Them:
Risk If Ignored:
```

If stakeholders are unknown, flag the gap and recommend specific discovery actions to identify them.

## Deal Risk Assessment

### Deal Qualification (MEDDIC)

| Element | Status | Evidence | Gap |
|---|---|---|---|
| Metrics | What quantifiable outcomes does the buyer expect? | [Evidence] | [What is missing] |
| Economic Buyer | Identified and engaged? | [Evidence] | [What is missing] |
| Decision Criteria | What factors will they use to decide? | [Evidence] | [What is missing] |
| Decision Process | What steps remain before signature? | [Evidence] | [What is missing] |
| Identify Pain | What business pain drives the purchase? | [Evidence] | [What is missing] |
| Champion | Who is the internal advocate and how strong are they? | [Evidence] | [What is missing] |

Rate overall qualification: **STRONG / MODERATE / WEAK / UNQUALIFIED**

### Velocity Risk Factors

Check for these common deal killers:

- [ ] No confirmed budget or budget not allocated
- [ ] Economic buyer not identified or not engaged
- [ ] Single-threaded (only one contact)
- [ ] No compelling event or deadline driving urgency
- [ ] Procurement or legal review timeline unknown
- [ ] Competitor has an incumbent advantage
- [ ] Champion is too junior to influence the decision
- [ ] Technical requirements not validated
- [ ] No mutual close plan or agreed next steps
- [ ] Deal has slipped from a previous close date

Score the checked items:
- 0-2: Low velocity risk
- 3-4: Moderate velocity risk -- address before advancing
- 5-6: High velocity risk -- deal may stall without intervention
- 7+: Critical -- unlikely to close on time without major course correction
