# Lead Scoring Model

Apply a multi-dimensional scoring model to each lead. Total score (0-100) determines qualification status and priority.

## A. ICP Fit Score (0-40 points)

Measures how well the lead matches the firm's target customer.

```
Company Size Alignment:
  Enterprise (1000+ employees)      = 15 points
  Mid-market (100-999 employees)    = 12 points
  SMB (10-99 employees)             = 8 points
  Startup/Micro (1-9 employees)     = 4 points
  Unknown                           = 5 points (neutral)

Industry Alignment (configure per firm):
  Primary target industries         = 15 points
  Secondary/adjacent industries     = 10 points
  Neutral industries                = 5 points
  Misaligned industries             = 2 points
  Unknown                           = 5 points (neutral)

Role/Authority:
  C-suite, VP, Director (decision maker)        = 10 points
  Manager, Head of (influencer)                 = 7 points
  Individual contributor                        = 4 points
  Unknown role                                  = 3 points
```

**Default Target Industries for Consulting Firm:**
- Primary: Technology, SaaS, Financial Services, Healthcare Tech, Professional Services
- Secondary: E-commerce, Manufacturing, Education, Real Estate Tech, Media

Users can customize these by providing their ICP definition. Ask on first run if no ICP config exists.

## B. Intent Score (0-35 points)

Measures the strength of buying intent based on language analysis.

```
Inquiry Type:
  RFP / Formal proposal request     = 12 points
  Demo / Trial request               = 10 points
  Pricing inquiry                    = 9 points
  Referral / Introduction            = 8 points
  Partnership inquiry                = 6 points
  General inquiry                    = 4 points
  Support question (not a lead)      = 0 points

Language Signals (cumulative, max 15 points):
  Mentions specific services by name          = +4
  Describes a concrete problem/pain point     = +4
  Asks about process, timeline, or next steps = +3
  References competitor or current vendor     = +3
  Mentions team/stakeholder involvement       = +2
  Uses vague/exploratory language only        = +1

Engagement Depth:
  Long, detailed email (200+ words)    = 8 points
  Medium email (50-200 words)          = 5 points
  Short email (under 50 words)         = 2 points
```

## C. Urgency Score (0-25 points)

Measures how time-sensitive the opportunity is.

```
Explicit Timeline:
  Deadline within 2 weeks            = 12 points
  Deadline within 1 month            = 9 points
  Deadline within 1 quarter          = 6 points
  Vague future timeline              = 3 points
  No timeline mentioned              = 1 point

Urgency Language (cumulative, max 8 points):
  "ASAP" / "urgent" / "immediately"          = +4
  "This week" / "this month"                 = +3
  "Soon" / "in the near future"              = +2
  "Exploring" / "researching"                = +1

Contextual Urgency (max 5 points):
  Regulatory deadline mentioned       = +5
  Board/executive mandate             = +4
  Competitive pressure                = +3
  Budget expiring                     = +5
  Seasonal/event driven               = +3
```

## Score Interpretation and Qualification

```
Total Score Range: 0-100 points

HOT LEAD (75-100):
  - Qualification: Sales-Qualified Lead (SQL)
  - Action: Respond within 2 hours, book a call
  - Priority: P1 -- immediate attention
  - Draft: Eager, specific, offer calendar link

WARM LEAD (50-74):
  - Qualification: Marketing-Qualified Lead (MQL)
  - Action: Respond within 24 hours, ask qualifying questions
  - Priority: P2 -- same-day response
  - Draft: Warm, curious, ask 2-3 discovery questions

COOL LEAD (25-49):
  - Qualification: Information-Qualified Lead (IQL)
  - Action: Respond within 48 hours, nurture
  - Priority: P3 -- respond when time allows
  - Draft: Helpful, educational, offer resources

COLD / NOT A LEAD (0-24):
  - Qualification: Unqualified
  - Action: Polite response or no action
  - Priority: P4 -- low priority
  - Draft: Brief acknowledgment, redirect if needed
```

## Score Adjustment Rules

Apply these modifiers after initial scoring:

1. **Referral Bonus:** Warm introduction from a known contact -- add +10 points.
2. **Multi-stakeholder Bonus:** Multiple people CC'd from the same company -- add +5 points.
3. **Repeat Inquiry Bonus:** This person/company has emailed before (check CRM) -- add +8 points.
4. **Generic Domain Penalty:** Sender uses gmail/yahoo/outlook AND no company identified -- subtract -5 points.
5. **Auto-generated Penalty:** Email appears auto-generated (newsletter, notification) -- subtract -15 points.
6. **Spam Signals Penalty:** Email contains spam signals (ALL CAPS subject, excessive exclamation marks, too-good-to-be-true language) -- subtract -20 points.
