# Analysis Framework

Apply all six phases systematically. Do not skip phases.

## Phase 1: Establish the Baseline

Before analyzing what went wrong, establish what "right" looked like for this account.

1. **Account Profile Construction**
   - Reconstruct the full account timeline from first touch to final cancellation
   - Document the original value proposition sold and expected outcomes
   - Identify all stakeholders: economic buyer, champion, end users, detractors
   - Map the organizational chart as it existed at key moments
   - Calculate total lifetime value realized vs projected at time of sale

2. **Health Score Reconstruction**
   - If a health score model exists, reconstruct the score trajectory over time
   - If no health score exists, build a retrospective one using available data
   - Identify the "peak health" moment and the inflection point where decline began
   - Benchmark this account's trajectory against retained accounts of similar size/segment

3. **Expectation vs Reality Mapping**
   - Document what was promised during the sales process
   - Document what was actually delivered and when
   - Identify any gaps between promise and delivery
   - Note whether the client's business context changed in ways that affected fit

## Phase 2: Timeline of Decline

Construct a detailed chronological narrative of the account's deterioration. This is the core forensic work.

1. **Signal Detection Timeline**
   Build a month-by-month (or week-by-week for shorter accounts) timeline that includes:
   - Usage metrics with trend arrows
   - Support ticket volume and severity
   - Engagement touchpoints (meetings, emails, calls)
   - NPS/CSAT data points
   - Stakeholder changes (departures, role changes, new hires)
   - Contract events (renewals, expansions, contractions)
   - Product releases and their relevance to this account
   - Competitive mentions or evaluation signals
   - Internal team changes (CSM transitions, rep turnover)

2. **Inflection Point Identification**
   For each significant negative shift in the timeline:
   - What changed and when exactly
   - Was the change sudden or gradual
   - What was the proximate cause
   - What was the underlying cause
   - Was this signal visible at the time with existing monitoring
   - If visible, was it acted upon and how
   - If not visible, what monitoring would have caught it

3. **Point of No Return Analysis**
   Identify the moment when churn became inevitable:
   - When did the client mentally check out
   - What was the final straw vs the accumulated weight
   - Was there a window where intervention could have changed the outcome
   - How long before the actual cancellation was the decision effectively made

## Phase 3: Root Cause Classification

Every churn has a primary root cause and typically two to four contributing factors. Classify using the taxonomy in `root-cause-taxonomy.md`. A churn event may have one primary cause and multiple secondary causes.

For each contributing factor beyond the primary cause:
- How much weight did this factor carry (percentage of influence)
- Was this factor independently sufficient to cause churn
- How did this factor interact with the primary cause to accelerate the outcome
- Was this factor preventable, partially preventable, or unpreventable

## Phase 4: Missed Warning Signs Audit

This is the most operationally valuable section. For every warning sign that was present but not acted upon:

1. **Signal Inventory**
   Catalog every signal that, in retrospect, indicated risk:
   - Declining usage metrics (specify which metrics and the decline rate)
   - Increasing support ticket volume or severity
   - Decreasing engagement with CSM outreach
   - Negative NPS/CSAT trends
   - Delayed responses to emails or meeting requests
   - Reduced attendance at QBRs or trainings
   - Stakeholder departures without introductions to successors
   - Requests for data exports or API documentation for migration
   - Social media activity mentioning competitors
   - Reduction in purchased seats or licenses
   - Late or disputed invoices
   - Absence from user community or events they previously attended

2. **Detection Gap Analysis**
   For each signal:
   - Was this signal captured in any existing monitoring system
   - If captured, was it surfaced to the right person at the right time
   - If surfaced, was it triaged with appropriate urgency
   - If triaged, was the response effective
   - Where in the detection-to-response chain did the process fail

3. **Early Warning Score**
   Rate the overall early warning system performance for this account:
   - How many months before cancellation could churn have been predicted
   - What was the earliest detectable signal
   - What combination of signals should have triggered a red alert
   - Was the account flagged as at-risk at any point, and if so, when

## Phase 5: Counterfactual Analysis

What could have been done differently at each critical juncture.

1. **Intervention Windows**
   Identify each moment where a different action could have changed the outcome:
   - The specific moment in time
   - What actually happened (or did not happen)
   - What should have happened instead
   - The estimated probability that the intervention would have saved the account
   - The resources that would have been required (executive time, engineering effort, financial concessions)
   - Why the intervention did not happen (lack of awareness, resource constraints, process gaps, prioritization decisions)

2. **Save Attempt Evaluation**
   If any save attempts were made:
   - When was the save attempt initiated relative to the point of no return
   - What was offered (discounts, roadmap commitments, executive attention, additional services)
   - Why did the save attempt fail
   - Was the save attempt too little, too late, or misdirected
   - What save approach would have had the highest probability of success

3. **Hindsight Playbook**
   Write the specific playbook that, if executed from the first warning sign, would have maximized the probability of retention:
   - Step-by-step actions with timing
   - Stakeholders who needed to be involved
   - Resources that needed to be allocated
   - Escalation triggers that should have fired
   - Executive engagement that should have occurred

## Phase 6: Lessons Learned and Systemic Recommendations

Transform this individual loss into organizational improvement.

1. **Process Failures**
   Identify breakdowns in existing processes:
   - Onboarding process gaps that set a poor foundation
   - Health monitoring gaps that missed early signals
   - Escalation process gaps that delayed response
   - Handoff process gaps (sales to CS, CSM transitions)
   - QBR/EBR process gaps that missed the real conversation
   - Renewal process gaps that started engagement too late

2. **Systemic Patterns**
   Connect this churn to broader patterns:
   - Is this the same root cause as other recent churns
   - Does this represent a segment-wide risk (similar accounts at risk)
   - Does this reveal a product gap affecting multiple accounts
   - Does this reveal a competitive threat that is broader than one account
   - Are there process failures here that are likely occurring undetected elsewhere

3. **Specific Recommendations**
   For each recommendation:
   - What needs to change (process, product, people, tooling)
   - Who owns the change
   - Priority level (critical, high, medium)
   - Expected impact on retention if implemented
   - Implementation complexity and timeline
   - How to measure whether the change is working

4. **At-Risk Account Identification**
   Based on the patterns found in this autopsy:
   - List current accounts that show similar warning signs
   - Prioritize by ARR and similarity to the churned account
   - Recommend immediate actions for each identified at-risk account
   - Define the monitoring triggers that should be implemented to catch this pattern earlier
