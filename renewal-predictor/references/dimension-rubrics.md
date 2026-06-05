# Dimension Scoring Rubrics

Score each dimension independently on a 0-100 scale, then combine with the weights in SKILL.md.

## 1. Engagement Frequency (20%)

Measures how actively the client participates in the relationship, both inside the product and with the team.

Scoring criteria:

- 90-100: Daily active usage by multiple users. Regular proactive outreach from client. Attends QBRs, participates in beta programs, provides roadmap feedback. Multiple threads of communication active simultaneously.
- 70-89: Weekly active usage. Responsive to outreach within 24 hours. Attends scheduled meetings. Engages with at least one non-support channel (community, events, feedback programs).
- 50-69: Usage several times per month. Responds to outreach within 48-72 hours. Attends most scheduled meetings but rarely initiates contact. Communication is primarily reactive.
- 30-49: Usage is sporadic or declining to once or twice per month. Slow to respond to outreach (3-5 business days). Cancels or reschedules meetings. No engagement outside of required touchpoints.
- 0-29: Usage has dropped to near-zero or is confined to a single user. Outreach goes unanswered for a week or more. Meetings are declined. No response to escalation attempts.

Data sources to check:

- Product analytics: DAU/WAU/MAU per account, session duration, login frequency
- CRM activity logs: emails, calls, meetings logged against the account
- Meeting attendance records: QBRs, check-ins, training sessions
- Community participation: forum posts, event registrations, beta enrollments
- Response latency: average time to reply to CSM outreach

Red flags:

- Login frequency dropped more than 40% over trailing 30 days
- No response to last two outreach attempts
- Primary contact has not logged in for 14+ days
- Declined last QBR or annual review

Green flags:

- Client proactively requests meetings or feature discussions
- Multiple departments or teams now using the product
- Client volunteered for case study, referral, or advisory board

## 2. Support Ticket Volume and Sentiment (15%)

Measures the health of the support relationship: trajectory, severity, and emotional tone, not just volume.

Scoring criteria:

- 90-100: Minimal ticket volume (below cohort average). Tickets are feature requests or minor questions, not bugs or outages. Sentiment in tickets is neutral to positive. CSAT on resolved tickets is consistently 4.5+/5.
- 70-89: Ticket volume is at or slightly below cohort average. Most tickets are low to medium severity. Sentiment is neutral. Resolution times meet SLA. No escalations in the trailing 90 days.
- 50-69: Ticket volume is above cohort average or trending upward. Mix of medium and high severity tickets. Some negative sentiment detected. One or two escalations in the trailing 90 days. Resolution satisfaction is inconsistent.
- 30-49: Ticket volume is significantly above average or has spiked sharply. Multiple high-severity or critical tickets. Negative sentiment is dominant. Escalations to management have occurred. Client has expressed frustration with support quality or speed.
- 0-29: Critical outage tickets or data loss incidents. Client has threatened to cancel or referenced competitors in support threads. Executive escalation has occurred. Sentiment is hostile or resigned. Open tickets are aging without resolution.

Data sources to check:

- Support platform: ticket count by severity, open vs closed, age of open tickets
- Sentiment analysis on ticket text and follow-up communications
- CSAT scores on resolved tickets (trailing 90 days)
- Escalation log: any tickets escalated beyond Tier 1
- SLA adherence: percentage of tickets resolved within SLA

Red flags:

- Ticket volume increased more than 50% month-over-month
- Any P0/P1 (critical/high) ticket open for more than 5 business days
- Client used words like "unacceptable," "considering alternatives," "escalate," "cancel"
- CSAT on support interactions dropped below 3.0/5

Green flags:

- Ticket volume is stable or declining while usage grows (indicates product maturity)
- Client submits feature requests rather than bug reports
- Support interactions end with positive feedback or thanks

## 3. Feature Adoption (20%)

Measures how much of the product the client is actually using relative to what they purchased and what is available.

Scoring criteria:

- 90-100: Client uses 80%+ of purchased features. Has adopted features released in the last two quarters. Uses advanced/power-user features. Multiple workflows configured. API integrations active. Self-service capabilities fully leveraged.
- 70-89: Client uses 60-79% of purchased features. Has tried at least one feature released in the last two quarters. Core workflows are well-established. Some advanced features in use.
- 50-69: Client uses 40-59% of purchased features. Adoption of new features is slow or absent. Usage is concentrated in one or two core workflows. Advanced features are untouched. Training opportunities have been offered but not taken.
- 30-49: Client uses less than 40% of purchased features. Multiple purchased modules are inactive. No adoption of new features in the last two quarters. Usage pattern suggests the client may not understand the full value of what they bought.
- 0-29: Client uses a single feature or module only. Most of the product is unexplored. No integrations configured. Usage pattern is indistinguishable from a free trial despite being on a paid plan.

Data sources to check:

- Feature usage matrix: which features are active per account
- Module activation rates: percentage of purchased modules in active use
- New feature adoption: time-to-first-use for features released in the last 6 months
- Integration status: API connections, webhooks, SSO, third-party integrations
- Training completion: onboarding milestones, certification progress

Red flags:

- Purchased module has zero usage for 60+ days after activation
- No adoption of any feature released in the last 6 months
- Client declined training or enablement sessions
- Usage is limited to a single user on a multi-seat license

Green flags:

- Client adopted a new feature within 30 days of release
- API usage indicates deep integration into client workflows
- Client requests features that indicate long-term investment in the platform
- Multiple roles/personas active in the product

## 4. NPS/CSAT Scores (10%)

Measures explicit satisfaction signals from surveys and structured feedback.

Scoring criteria:

- 90-100: NPS response is Promoter (9-10). CSAT consistently above 4.5/5. Client has provided testimonial or referral. Positive trend across last three survey cycles.
- 70-89: NPS response is Promoter (9-10) or high Passive (7-8). CSAT between 4.0-4.5/5. Scores are stable or improving.
- 50-69: NPS response is Passive (7-8). CSAT between 3.5-4.0/5. Scores are flat. Comments are neutral with no strong positive or negative signals.
- 30-49: NPS response is low Passive (7) or Detractor (0-6). CSAT between 2.5-3.5/5. Scores are declining. Comments reference specific pain points or unmet expectations.
- 0-29: NPS response is Detractor (0-6). CSAT below 2.5/5. Scores have dropped sharply. Comments reference intent to leave, competitor evaluation, or fundamental dissatisfaction.

Data sources to check:

- NPS survey results: score, verbatim comments, response rate
- CSAT surveys: transactional (post-support) and relational (quarterly/annual)
- In-app feedback: thumbs up/down, feature ratings, feedback widgets
- Third-party review sites: G2, Capterra, TrustRadius (if client has posted)

Red flags:

- NPS dropped 3+ points between survey cycles
- Client declined to respond to last survey (non-response is a signal)
- Verbatim comments mention competitor names or "looking for alternatives"
- CSAT trend is negative across three consecutive measurements

Green flags:

- Client is a Promoter and has provided a referral or review
- NPS improved by 2+ points between cycles
- Unsolicited positive feedback received outside of surveys

## 5. Billing History (10%)

Measures the financial health of the relationship and the client's commitment signals expressed through purchasing behavior.

Scoring criteria:

- 90-100: All invoices paid on time or early. No disputes in the last 12 months. Client has expanded contract (upsell, additional seats, upgraded tier). Multi-year agreement in place. No discount dependency.
- 70-89: Invoices paid within terms (net 30/45/60 as agreed). Rare minor disputes resolved quickly. Contract is stable with no downgrades. Renewal at same or higher value expected.
- 50-69: Occasional late payments (1-2 in the last 6 months). One invoice dispute in the last 12 months. Client requested pricing review or discount at last renewal. Contract value is flat.
- 30-49: Multiple late payments. Active invoice disputes. Client has downgraded seats, modules, or tier in the last 12 months. Heavy discount dependency (renewal contingent on discount). Budget review or procurement audit in progress.
- 0-29: Invoices are significantly overdue (60+ days). Client has requested early termination terms or referenced cancellation clauses. Chargeback or payment failure occurred. Finance team has flagged the account for collections risk.

Data sources to check:

- Billing platform: payment history, days sales outstanding (DSO) per account
- Invoice dispute log: frequency, severity, resolution
- Contract modifications: upsells, downgrades, tier changes, add-ons
- Discount history: percentage of contract value attributed to discounts
- Renewal terms: auto-renew status, opt-out window, multi-year vs annual

Red flags:

- Payment is 30+ days past due with no communication
- Client requested contract termination terms or asked about cancellation process
- Downgraded from a higher tier or reduced seat count
- Discount has increased at each renewal cycle

Green flags:

- Client expanded contract mid-cycle without being asked
- Multi-year renewal signed
- Client paying above list price due to custom SLA or premium support
- No discount requests at renewal

## 6. Stakeholder Continuity (10%)

Measures the stability of the human relationships that sustain the account, because products do not renew themselves -- people do.

Scoring criteria:

- 90-100: Executive sponsor is engaged and accessible. Primary champion is active, enthusiastic, and has organizational influence. Multiple stakeholders across departments are invested. No key personnel changes in the last 6 months. Succession plan exists if champion leaves.
- 70-89: Executive sponsor is aware of the relationship and available when needed. Champion is active and supportive. At least two stakeholders are familiar with the product. No disruptive personnel changes in the last 6 months.
- 50-69: Executive sponsor is disengaged or unknown. Champion is present but their influence may be limited. Only one or two people at the client know the product well. A key stakeholder changed roles in the last 6 months but a replacement was identified.
- 30-49: Champion has left the organization or changed roles with no clear successor. Executive sponsor is unknown or has changed. New stakeholders are unfamiliar with the product and have not been onboarded. Organizational restructuring is underway.
- 0-29: All known champions have departed. No executive sponsor. New decision-makers have no prior relationship with the team. Acquisition, merger, or leadership overhaul is in progress. New stakeholders are evaluating competitive alternatives.

Data sources to check:

- CRM contact records: role changes, departure flags, last activity dates
- LinkedIn monitoring: job changes for key contacts (champion, sponsor, admin)
- Meeting attendance: who is showing up vs who used to show up
- Org chart changes: restructuring announcements, new leadership, M&A news
- Onboarding status of new contacts: have replacements been introduced and enabled

Red flags:

- Champion changed jobs (LinkedIn update, email bounce, CRM flag)
- Executive sponsor was replaced and new sponsor has not been briefed
- New procurement or IT leadership with no prior relationship
- Client company announced layoffs, restructuring, or acquisition
- Decision-maker mentioned "evaluating options" or "conducting a review"

Green flags:

- Champion got promoted (more influence, deeper investment)
- New executive sponsor proactively reached out to learn about the partnership
- Client introduced additional stakeholders to expand the relationship
- Multi-threaded relationship: 5+ contacts actively engaged

## 7. Usage Trends (15%)

Measures the directional momentum of product usage. This is distinct from feature adoption -- it captures whether usage is accelerating, stable, or decelerating.

Scoring criteria:

- 90-100: Usage is growing across all key metrics (sessions, active users, data volume, API calls) over trailing 30/60/90-day windows. Growth rate is accelerating or steady. New use cases are emerging. Usage exceeds contracted entitlements.
- 70-89: Usage is stable or growing slightly. Key metrics are flat to positive over trailing 90 days. No significant declines in any dimension. Seasonal patterns are consistent with prior years.
- 50-69: Usage is flat overall with some metrics declining. Active user count may have dipped. Session duration or frequency is trending down slightly. No new use cases have emerged in the last quarter.
- 30-49: Usage is declining across multiple metrics. Active user count has dropped by 20%+ over trailing 90 days. Core workflows are being used less frequently. Data volume or API calls have decreased.
- 0-29: Usage has collapsed. Active users have dropped by 50%+ or to a single user. Core workflows are abandoned. The client appears to be migrating away or has stopped using the product entirely.

Data sources to check:

- Product analytics: trailing 30/60/90-day trends for sessions, users, actions, data volume
- API call logs: volume trends, new endpoints being called, error rates
- Storage/compute consumption: growing or shrinking footprint
- Feature-level usage trends: are core features stable while peripheral features decline, or vice versa
- Cohort comparison: how does this client's usage trajectory compare to similar accounts

Red flags:

- Active users declined 20%+ in the last 30 days without a known seasonal cause
- Core feature usage dropped while overall login count remained stable (indicates disengagement from value-driving workflows)
- Data exports increased (potential sign of migration)
- API call volume dropped or shifted to read-only patterns (extracting data, not writing)

Green flags:

- Usage is growing faster than seat count (organic adoption)
- New API endpoints being called (indicates expanding integration)
- Usage survived a slow season without significant decline
- Client hit or exceeded usage entitlements (expansion opportunity)
