---
name: client-proposal-generator
description: Generates full consulting proposals from a brief. Input client name, problem description, and rough scope. Outputs proposal.md with executive summary, problem statement, proposed approach, timeline, team, pricing tiers, and terms. Researches client company for personalization. Multiple pricing models. Professional formatting matching consulting standards.
tools: Read, Write, Bash, WebSearch, Glob
user_invocable: true
---

# Client Proposal Generator

A production-grade consulting proposal generator that transforms a brief description into a complete, professionally formatted proposal document. This skill researches the client company for personalization, structures the proposal using proven consulting frameworks, and produces a document ready to send to a prospect.

## What This Produces

A single `proposal.md` (or `proposal-{client-name}.md`) file containing:

1. Cover page with client name, your firm name, date
2. Executive summary (personalized to client's situation)
3. Understanding of the client's challenges (demonstrates you listened)
4. Proposed approach and methodology
5. Scope of work with deliverables
6. Timeline with milestones
7. Team and qualifications
8. Investment (pricing in 3 tiers)
9. Terms and conditions
10. Next steps and call to action
11. Appendix (optional: case studies, team bios, references)

## When to Use

- After a discovery call when you need to follow up with a proposal
- When a prospect asks "can you send me a proposal?"
- When responding to an RFP or RFI
- When creating proposals for internal project pitches
- When templating proposals for repeated service offerings

## Execution Protocol

### Step 0: Gather Input

Collect from the user (or extract from conversation context):

**Required inputs:**
- `client_name` -- The prospect company name
- `contact_name` -- Primary contact (who receives the proposal)
- `problem_description` -- What problem they need solved (even a vague description works)
- `your_company` -- Your company/firm name (or default to what is in the user's context)

**Optional inputs (will be inferred or defaulted if not provided):**
- `rough_scope` -- Any known scope details (timeline, budget range, team size)
- `your_services` -- Description of your service offerings
- `pricing_model` -- fixed | retainer | milestone | hourly | hybrid (default: 3-tier fixed)
- `proposal_tone` -- consultative | enterprise | startup | technical (default: consultative)
- `include_case_studies` -- boolean (default: false, since fabricated case studies are worse than none)
- `output_path` -- Where to write the file (default: current directory)
- `currency` -- USD | EUR | GBP | etc. (default: USD)

If the user gives a one-liner like "Write a proposal for Acme Corp about redesigning their data pipeline," extract what you can and infer the rest.

### Step 1: Client Research

Research the client company to personalize the proposal. This is what separates a template from a real proposal.

#### 1a. Web Research

Use WebSearch and Bash to gather:

1. **Company overview** -- What they do, industry, size, location, founding year
2. **Recent news** -- Funding, acquisitions, product launches, leadership changes (last 6 months)
3. **Technology signals** -- Job postings (indicate tech stack and pain points), GitHub repos, tech blog posts
4. **Industry context** -- Current trends and challenges in their sector
5. **Competitors** -- Who they compete with (positions your proposal in context)
6. **Company values/culture** -- From their about page, mission statement, LinkedIn

#### 1b. Structure Research Findings

Organize findings into a research brief:

```
## Client Research Brief: [Client Name]

### Company Overview
- Industry: [industry]
- Size: [employee count, revenue if public]
- Founded: [year]
- HQ: [location]
- What they do: [1-2 sentence description]

### Recent Developments
- [Event 1 -- date, significance]
- [Event 2 -- date, significance]

### Industry Context
- [Trend 1 affecting their sector]
- [Trend 2 affecting their sector]
- [Challenge specific to their industry]

### Technology Signals
- [Hiring for X suggests need for Y]
- [Using tool Z based on job postings]

### Competitive Landscape
- [Competitor 1 -- what they do differently]
- [Competitor 2 -- market positioning]

### Personalization Hooks
- [Specific detail to reference in the executive summary]
- [Pain point to mirror in the problem statement]
- [Opportunity to connect your solution to their recent news]
```

If web research is unavailable or returns limited results, note this and proceed with what is available. A slightly less personalized proposal is better than no proposal.

### Step 2: Problem Framing

Transform the user's problem description into a structured problem statement. Use the consulting standard of framing problems in terms of business impact.

#### 2a. Problem Decomposition

Break the stated problem into:

1. **Root problem** -- The fundamental issue (e.g., "legacy data pipeline cannot scale")
2. **Symptoms** -- Observable manifestations (e.g., "reports take 6 hours to generate")
3. **Business impact** -- Revenue, cost, risk, opportunity cost (e.g., "delays decision-making by 24 hours")
4. **Stakeholders affected** -- Who feels the pain (e.g., "operations team, executive leadership, customers")
5. **Urgency drivers** -- Why now (e.g., "upcoming product launch requires real-time analytics")

#### 2b. Challenge Articulation

Write 3-5 bullet points that demonstrate understanding of the client's situation. These will become the "Understanding Your Challenges" section. The tone should be: "We have listened, we understand the stakes, here is what we heard."

### Step 3: Solution Design

Design the proposed approach based on the problem and your services.

#### 3a. Methodology Selection

Choose or adapt a methodology framework:

| Problem Type | Methodology | Structure |
|-------------|-------------|-----------|
| Technology modernization | Discovery -> Design -> Build -> Migrate -> Optimize | 5-phase waterfall with agile sprints |
| Process improvement | Assess -> Map -> Redesign -> Implement -> Measure | Lean/Six Sigma influenced |
| Strategy / advisory | Research -> Analysis -> Recommendations -> Roadmap | Classic consulting engagement |
| Product development | Discovery -> Prototype -> Build -> Test -> Launch | Agile product development |
| Data / analytics | Audit -> Architecture -> Build -> Validate -> Deploy | Data engineering lifecycle |
| Organizational change | Assess -> Design -> Pilot -> Roll Out -> Sustain | Change management framework |

#### 3b. Phase Definition

For each phase, define:

```
Phase N: [Phase Name] -- [Duration]

Objective: [What this phase achieves]

Activities:
- [Activity 1]
- [Activity 2]
- [Activity 3]

Deliverables:
- [Deliverable 1 -- concrete, tangible]
- [Deliverable 2]

Milestone: [What marks the end of this phase]

Client involvement: [What you need from the client during this phase]
```

#### 3c. Deliverables Inventory

Create a master list of all deliverables across all phases:

| # | Deliverable | Phase | Format | Description |
|---|------------|-------|--------|-------------|
| D1 | Discovery Report | 1 | PDF/Presentation | Current state assessment with findings |
| D2 | Solution Architecture | 2 | Technical Document | Proposed system design |
| D3 | Implementation Plan | 2 | Project Plan | Detailed execution roadmap |
| ... | ... | ... | ... | ... |

### Step 4: Timeline Construction

Build a realistic project timeline.

#### 4a. Duration Estimation

| Project Type | Typical Duration | Notes |
|-------------|-----------------|-------|
| Quick audit / assessment | 2-4 weeks | Discovery + report |
| Strategy engagement | 4-8 weeks | Research heavy, lighter implementation |
| Technology implementation | 8-16 weeks | Build-heavy, requires testing |
| Full transformation | 12-24 weeks | Multi-phase, organizational change |
| Ongoing advisory / retainer | 3-12 months | Monthly cadence |

#### 4b. Timeline Format

```
## Timeline

### Overview
- Start date: [upon contract execution / specific date]
- End date: [estimated completion]
- Total duration: [X weeks/months]

### Phase Timeline

| Phase | Duration | Start | End | Key Milestone |
|-------|----------|-------|-----|---------------|
| 1. Discovery | 2 weeks | Week 1 | Week 2 | Discovery Report delivered |
| 2. Design | 3 weeks | Week 3 | Week 5 | Architecture approved |
| 3. Build | 6 weeks | Week 6 | Week 11 | MVP deployed to staging |
| 4. Test & Refine | 2 weeks | Week 12 | Week 13 | UAT sign-off |
| 5. Launch & Handoff | 1 week | Week 14 | Week 14 | Production deployment |

### Key Dates
- Kickoff meeting: [Week 1, Day 1]
- Mid-project review: [Week 7]
- Go/no-go decision: [Week 12]
- Final delivery: [Week 14]

### Dependencies and Assumptions
- Client provides access to systems and stakeholders within 5 business days of kickoff
- Client designates a project sponsor and day-to-day point of contact
- Feedback on deliverables provided within 3 business days
- Timeline may adjust based on discovery findings (Phase 1)
```

### Step 5: Team Composition

Present the team that will deliver the work.

#### 5a. Role Framework

Standard consulting team structure:

| Role | Responsibility | Typical Allocation |
|------|---------------|--------------------|
| **Engagement Lead** | Client relationship, strategy, quality | 10-20% |
| **Project Manager** | Timeline, coordination, status reporting | 25-50% |
| **Senior Consultant** | Analysis, recommendations, architecture | 50-100% |
| **Consultant** | Research, implementation, documentation | 100% |
| **Analyst** | Data gathering, support tasks, QA | 50-100% |
| **Subject Matter Expert** | Domain expertise, reviews | 10-25% (as needed) |

#### 5b. Team Section Format

```
## Your Team

We will staff this engagement with a focused team combining strategic vision and hands-on execution.

**[Name], Engagement Lead**
[Title at your company]. [X] years of experience in [relevant domain]. 
Previously led similar engagements for [types of companies]. 
Responsible for overall engagement quality and strategic alignment.
Allocation: [X]% throughout the engagement.

**[Name], Senior Consultant**
[Title]. Specializes in [relevant specialization].
[Brief relevant background].
Responsible for [key deliverables].
Allocation: [X]% during Phases [N-N].

[Continue for each team member]
```

Note: If the user has not provided team details, use placeholder names and roles. Never fabricate specific people or credentials.

### Step 6: Pricing

Build the pricing section with 3 tiers. The 3-tier model is a proven approach: the middle tier is the target, the lower tier makes the middle look reasonable, the upper tier captures ambitious buyers.

#### 6a. Pricing Model Selection

| Model | When to Use | Structure |
|-------|-------------|-----------|
| **Fixed Fee (3 tiers)** | Well-defined scope, predictable work | 3 packages at set prices |
| **Retainer** | Ongoing advisory, fractional roles | Monthly fee for X hours/month |
| **Milestone-Based** | Long projects, client wants to de-risk | Payments tied to deliverable acceptance |
| **Hourly/Daily Rate** | Undefined scope, staff augmentation | Blended or role-based rates |
| **Hybrid** | Mix of defined deliverables + ongoing support | Fixed for phases + retainer for support |

Default to 3-tier fixed fee unless the user specifies otherwise.

#### 6b. Three-Tier Pricing Framework

```
## Investment

We have structured three engagement options to align with your priorities and budget.

### Option A: [Tier Name -- e.g., "Foundation"]
**[Price]**

Best for: [One sentence describing who this is for]

Includes:
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

Duration: [X weeks]
Team: [Roles involved]

---

### Option B: [Tier Name -- e.g., "Accelerator"] (Recommended)
**[Price]**

Best for: [One sentence -- this should be the most compelling]

Everything in Foundation, plus:
- [Additional deliverable 1]
- [Additional deliverable 2]
- [Additional deliverable 3]
- [Additional deliverable 4]

Duration: [X weeks]
Team: [Roles involved]

---

### Option C: [Tier Name -- e.g., "Transformation"]
**[Price]**

Best for: [One sentence describing the full-scope option]

Everything in Accelerator, plus:
- [Premium deliverable 1]
- [Premium deliverable 2]
- [Premium deliverable 3]
- [Ongoing support component]

Duration: [X weeks]
Team: [Full team]
```

#### 6c. Pricing Guidelines

Consulting rate benchmarks (adjust based on market, geography, and specialization):

| Firm Size | Junior Rate | Senior Rate | Principal Rate |
|-----------|------------|-------------|----------------|
| Solo / boutique | $150-250/hr | $250-400/hr | $400-600/hr |
| Mid-market firm | $200-350/hr | $350-500/hr | $500-800/hr |
| Big 4 / enterprise | $300-500/hr | $500-800/hr | $800-1500/hr |

To calculate tier prices:
- Estimate hours per role per phase
- Apply blended rate
- Tier 1: 60-70% of full scope price
- Tier 2: 100% of target price (the one you want them to buy)
- Tier 3: 140-160% of target price

If the user provides a budget range, reverse-engineer the tiers to bracket that range.

#### 6d. Payment Terms

```
### Payment Terms

- 50% upon contract execution
- 25% at mid-project milestone ([specific milestone])
- 25% upon final delivery acceptance

OR (for retainer):
- Monthly invoicing, net 30
- 3-month minimum commitment
- 60-day cancellation notice

OR (for milestone):
- Payment upon acceptance of each phase deliverable
- Invoiced within 5 business days of milestone acceptance
- Net 30 payment terms
```

### Step 7: Terms and Conditions

Standard consulting terms to include:

```
## Terms and Conditions

### Scope
This proposal covers the scope described herein. Work outside this scope will be addressed 
through a change order process with separate estimation and approval.

### Change Orders
Changes to scope, timeline, or deliverables will be documented in a written change order 
signed by both parties before work begins on the change.

### Intellectual Property
All deliverables become the property of [Client Name] upon final payment. 
[Your Company] retains the right to use general methodologies, frameworks, 
and non-proprietary tools developed during the engagement.

### Confidentiality
Both parties agree to keep confidential all proprietary information shared during 
the engagement. A separate NDA can be executed upon request.

### Assumptions
- Client will provide timely access to stakeholders, systems, and data as needed
- Client will designate a single point of contact for day-to-day coordination
- Feedback on deliverables will be provided within [3-5] business days
- Timeline estimates assume the above; delays in client inputs may extend the timeline

### Validity
This proposal is valid for 30 days from the date of submission.

### Limitation of Liability
[Your Company]'s total liability shall not exceed the total fees paid under this engagement.
```

### Step 8: Assemble and Write the Proposal

Combine all sections into the final document. Apply professional formatting.

#### Document Structure

```markdown
# [Proposal Title]

## [Your Company] | Proposal for [Client Name]

**Prepared for**: [Contact Name], [Contact Title]
**Prepared by**: [Your Name/Team], [Your Company]
**Date**: [Current Date]
**Proposal #**: [Auto-generated: PROP-{YYYY}-{NNN}]
**Valid through**: [Date + 30 days]

---

## Table of Contents

1. Executive Summary
2. Understanding Your Challenges
3. Proposed Approach
4. Scope and Deliverables
5. Timeline
6. Your Team
7. Investment
8. Terms and Conditions
9. Next Steps
10. Appendix (if applicable)

---

## 1. Executive Summary

[2-3 paragraphs. Personalized to the client. Reference their specific situation,
recent news, or industry challenges from the research phase. State the problem,
the proposed solution at a high level, and the expected outcome. End with a 
confidence statement.]

---

## 2. Understanding Your Challenges

[This section mirrors the client's pain points back to them, demonstrating that
you have listened and understand the stakes. Use the problem framing from Step 2.
3-5 bullet points or short paragraphs, each addressing a specific challenge.]

---

## 3. Proposed Approach

[Methodology overview. Explain your approach in terms the client can understand.
Avoid jargon. Focus on the "why" behind each phase. Include a visual timeline
or phase diagram if possible.]

### Phase 1: [Phase Name]
[Description, activities, deliverables]

### Phase 2: [Phase Name]
[Description, activities, deliverables]

[Continue for all phases]

---

## 4. Scope and Deliverables

### In Scope
[Bullet list of everything included]

### Out of Scope
[Explicit list of what is NOT included -- this prevents scope creep]

### Deliverables Summary
| # | Deliverable | Phase | Format |
|---|------------|-------|--------|
[Table from Step 3c]

---

## 5. Timeline

[Timeline from Step 4]

---

## 6. Your Team

[Team section from Step 5]

---

## 7. Investment

[Pricing section from Step 6]

---

## 8. Terms and Conditions

[Terms from Step 7]

---

## 9. Next Steps

To move forward:

1. **Select your preferred option** (A, B, or C)
2. **Schedule a follow-up call** to discuss any questions or adjustments
3. **Sign the agreement** -- We will send a formal engagement letter based on your selected option
4. **Kick off** -- We can begin within [X business days] of signed agreement

We are excited about the opportunity to partner with [Client Name] on this initiative.
Please do not hesitate to reach out with questions.

**[Your Name]**
[Your Title]
[Your Email]
[Your Phone]

---

## Appendix

### A. About [Your Company]
[Brief company overview -- 1 paragraph]

### B. Relevant Experience
[2-3 brief case study summaries, IF the user has provided real ones. 
NEVER fabricate case studies -- omit this section if no real examples are available.]

### C. Glossary
[Define any technical terms used in the proposal, if the audience is non-technical]
```

### Step 9: Quality Check

Before delivering, verify:

- [ ] Client name is correct and consistent throughout
- [ ] Contact name is correct
- [ ] Company research is accurate (no hallucinated facts)
- [ ] All sections are present and complete
- [ ] Pricing tiers are internally consistent (each tier adds to the previous)
- [ ] Timeline is realistic (phases add up, dependencies make sense)
- [ ] No placeholder text remains (no `[TODO]` or `{variable}` markers)
- [ ] Tone matches the selected style (consultative, enterprise, startup, technical)
- [ ] Terms and conditions are reasonable
- [ ] Out-of-scope section is present (prevents expectation mismatch)
- [ ] Next steps are clear and actionable
- [ ] No fabricated case studies, team bios, or credentials
- [ ] Dates are current (proposal date, validity period)
- [ ] Currency is correct
- [ ] Document reads well end-to-end (no jarring transitions between sections)

### Step 10: Deliver and Summarize

1. Write the file to the specified output path
2. Present a summary to the user:

```
## Proposal Generated

**File**: proposal-acme-corp.md
**Client**: Acme Corp (attention: Jane Smith)
**Type**: Technology modernization proposal
**Pricing tiers**: 
  - Foundation: $X
  - Accelerator: $Y (recommended)
  - Transformation: $Z
**Timeline**: 14 weeks (Accelerator tier)
**Word count**: ~3,200 words

### Personalization Applied
- Referenced their recent Series B funding
- Addressed industry-specific compliance requirements
- Tailored approach to their current tech stack (Node.js + PostgreSQL)

### Review Recommendations
- Verify team member names and bios before sending
- Confirm pricing aligns with your rate card
- Consider adding a case study if you have a relevant one
- The "Out of Scope" section may need adjustment based on your discovery call notes
```

## Proposal Tone Variants

### Consultative (Default)
- Partner language ("we will work together to...")
- Questions woven in ("have you considered...?")
- Empathetic problem framing
- Moderate formality

### Enterprise
- Formal language throughout
- Risk mitigation emphasis
- Governance and compliance focus
- Reference to established methodologies by name
- Higher perceived authority

### Startup
- Direct and energetic
- Speed and iteration emphasis
- Lean methodology references
- Budget-conscious framing
- Practical over polished

### Technical
- Architecture diagrams and system design
- Technical trade-off analysis
- Detailed technology recommendations
- Less business context, more implementation detail
- Aimed at technical decision-makers

## Pricing Calibration by Engagement Type

| Engagement Type | Tier 1 Range | Tier 2 Range | Tier 3 Range |
|----------------|-------------|-------------|-------------|
| Strategy / advisory (4-8 weeks) | $15K-30K | $30K-60K | $60K-100K |
| Technology assessment (2-4 weeks) | $10K-20K | $20K-40K | $40K-75K |
| Implementation (8-16 weeks) | $50K-100K | $100K-200K | $200K-400K |
| Full transformation (12-24 weeks) | $100K-200K | $200K-500K | $500K-1M+ |
| Monthly retainer | $5K-10K/mo | $10K-20K/mo | $20K-50K/mo |

These are calibration ranges, not fixed prices. Adjust based on:
- Client company size and budget
- Geographic market
- Your firm's positioning and reputation
- Complexity of the specific engagement
- Competitive landscape for this deal

## Error Handling

| Issue | Response |
|-------|----------|
| No client name provided | Ask before proceeding -- this is the one required field |
| Minimal problem description | Generate a proposal with broader framing; flag sections that need client input |
| Web research returns nothing | Proceed without personalization, note it, suggest the user add details |
| User provides no pricing guidance | Use mid-market rates from the calibration table |
| Scope is extremely vague | Create a "Discovery Phase" as the first tier, full engagement as tiers 2-3 |
| User asks for a one-page version | Generate an executive summary version (Section 1 + pricing + next steps) |
| User wants a different format (PDF, DOCX) | Generate the markdown and suggest using a PDF/DOCX conversion skill |
| Client is a competitor | Warn the user (in case it is accidental) but proceed if confirmed |
