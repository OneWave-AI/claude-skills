# okr-plan.md Output Template

Generate `okr-plan.md` following this exact structure. The document must be at least 400 lines of substantive content (no filler).

```markdown
# [Team Name] OKR Plan -- [Quarter/Period]

> Generated on [date] | Methodology: Google/Intel OKR Framework
> Reference: "Measure What Matters" by John Doerr

---

## Table of Contents

1. Executive Summary
2. Company Goal Alignment
3. OKR Scoring Guide
4. Objectives and Key Results
5. Alignment Map
6. Initiatives and Key Activities
7. Dependencies and Risks
8. Tracking Cadence
9. Weekly Check-in Template
10. Monthly Scoring Template
11. Quarterly Retrospective Template
12. Appendix: OKR Best Practices

---

## 1. Executive Summary

[2-3 paragraph summary of the team's strategic focus for the quarter. What is
the team trying to accomplish and why? How does this connect to the company's
broader mission? What are the most important bets the team is making?]

---

## 2. Company Goal Alignment

[A table or structured list showing each company-level goal and which team
objectives map to it. Every team objective MUST connect to at least one
company goal. If an objective does not connect, it should not exist.]

| Company Goal | Team Objective(s) | Alignment Rationale |
|---|---|---|
| [Company Goal 1] | Objective 1, Objective 3 | [Why these objectives serve this goal] |
| [Company Goal 2] | Objective 2 | [Why this objective serves this goal] |
| ... | ... | ... |

---

## 3. OKR Scoring Guide

### Scoring Scale

| Score | Meaning | Color Code | Expected For |
|---|---|---|---|
| 0.0 | No progress | Red | -- |
| 0.1 - 0.3 | Minimal progress, significantly off track | Red | -- |
| 0.4 - 0.6 | Some progress, but fell short of target | Yellow | -- |
| 0.7 | Target hit (this IS the goal for aspirational OKRs) | Green | Aspirational |
| 0.8 - 0.9 | Exceeded expectations | Green | -- |
| 1.0 | Fully delivered | Green | Committed |

### Committed vs Aspirational

- **Committed OKRs** are things the team has agreed MUST happen. The target
  score is 1.0. Failure to hit 1.0 requires a postmortem explaining what
  went wrong and what will change.

- **Aspirational OKRs** (also called "stretch" or "moonshot" OKRs) are
  ambitious targets where landing at 0.6-0.7 is considered a success.
  Consistently scoring 1.0 on aspirational OKRs means the team is not
  being ambitious enough.

### Important Reminder

> OKR scores are a management tool for learning and alignment. They are
> explicitly decoupled from employee performance evaluations, compensation
> decisions, and promotion reviews. Using OKR scores for performance
> management undermines psychological safety and encourages sandbagging.

---

## 4. Objectives and Key Results

### Objective 1: [Qualitative, inspirational statement]

**Type:** [Committed / Aspirational]
**Owner:** [Role or name]
**Company Goal Alignment:** [Which company goal(s) this serves]

| # | Key Result | Baseline | Target | Stretch | Type | Owner | Score |
|---|---|---|---|---|---|---|---|
| KR 1.1 | [Measurable outcome] | [Current value] | [Target value] | [Stretch value] | [Committed/Aspirational] | [Owner] | -- |
| KR 1.2 | [Measurable outcome] | [Current value] | [Target value] | [Stretch value] | [Committed/Aspirational] | [Owner] | -- |
| KR 1.3 | [Measurable outcome] | [Current value] | [Target value] | [Stretch value] | [Committed/Aspirational] | [Owner] | -- |

**Scoring Rubric for KR 1.1:**
- 0.0: [What 0.0 looks like]
- 0.3: [What 0.3 looks like]
- 0.5: [What 0.5 looks like]
- 0.7: [What 0.7 looks like]
- 1.0: [What 1.0 looks like]

**Scoring Rubric for KR 1.2:**
[Same structure]

**Scoring Rubric for KR 1.3:**
[Same structure]

**Key Initiatives (activities, NOT results):**
- [Initiative 1: What the team will DO to drive these key results]
- [Initiative 2]
- [Initiative 3]
- [Initiative 4]

**Risks and Mitigations:**
- Risk: [Description] | Mitigation: [Plan]
- Risk: [Description] | Mitigation: [Plan]

---

[Repeat the above structure for Objectives 2 through 5]

---

## 5. Alignment Map

[A visual or structured representation showing how team OKRs cascade from
company goals. This section makes the "ladder" explicit.]

### Cascade Diagram

```
Company Goal: [Goal 1]
  |
  +-- Team Objective 1: [Title]
  |     +-- KR 1.1: [Summary]
  |     +-- KR 1.2: [Summary]
  |     +-- KR 1.3: [Summary]
  |
  +-- Team Objective 3: [Title]
        +-- KR 3.1: [Summary]
        +-- KR 3.2: [Summary]

Company Goal: [Goal 2]
  |
  +-- Team Objective 2: [Title]
        +-- KR 2.1: [Summary]
        +-- KR 2.2: [Summary]
        +-- KR 2.3: [Summary]
```

### Cross-Functional Dependencies

| This Team's OKR | Depends On | Other Team | Their Related OKR | Status |
|---|---|---|---|---|
| [KR reference] | [What is needed] | [Team name] | [Their OKR if known] | [Not started / In progress / Resolved] |

---

## 6. Initiatives and Key Activities

[For each objective, list the concrete initiatives (projects, workstreams,
experiments) that the team will execute. These are the "how" -- the activities
that drive key result progress. Initiatives are NOT key results. They are the
work that produces the outcomes measured by key results.]

### Objective 1 Initiatives

| Initiative | Description | Key Results Impacted | Owner | Timeline | Status |
|---|---|---|---|---|---|
| [Initiative name] | [1-2 sentence description] | KR 1.1, KR 1.2 | [Owner] | [Start - End] | Not Started |
| ... | ... | ... | ... | ... | ... |

[Repeat for each objective]

---

## 7. Dependencies and Risks

### External Dependencies

[List anything outside the team's control that could impact OKR achievement]

| Dependency | Impact If Unresolved | Responsible Party | Due Date | Status |
|---|---|---|---|---|
| [Description] | [Which KRs affected and how] | [Who] | [When needed] | [Status] |

### Top Risks

| Risk | Probability | Impact | Affected OKRs | Mitigation Plan |
|---|---|---|---|---|
| [Risk description] | High/Med/Low | High/Med/Low | [KR references] | [What the team will do] |

---

## 8. Tracking Cadence

### Weekly (Every [Day of Week])

**Purpose:** Rapid status check. Are we on track? Any blockers?
**Duration:** 15-30 minutes
**Attendees:** [Team lead + KR owners]
**Format:**
- Each KR owner gives a 60-second update: confidence level (on track / at risk / off track), key actions taken this week, blockers
- Team lead captures blockers and assigns owners to resolve
- No deep dives -- those happen offline

### Monthly (First [Day] of each month)

**Purpose:** Score update and course correction
**Duration:** 60 minutes
**Attendees:** [Full team]
**Format:**
- Score each KR on the 0.0-1.0 scale based on current progress
- Compare current trajectory to target trajectory
- Identify KRs that need intervention
- Decide on any scope adjustments (with documentation of why)
- Update initiative priorities based on what is/isn't working

### Quarterly (End of Quarter)

**Purpose:** Full retrospective and scoring
**Duration:** 90-120 minutes
**Attendees:** [Full team + stakeholders]
**Format:**
- Final scoring of all KRs
- Objective-level scoring (average of KR scores)
- Retrospective discussion (see template below)
- Input into next quarter's OKR planning

---

## 9. Weekly Check-in Template

```
## Weekly OKR Check-in -- [Team Name]
## Week of: [Date]
## Facilitator: [Name]

### Objective 1: [Title]
Overall Confidence: [On Track / At Risk / Off Track]

| Key Result | Current Value | Target | Confidence | Notes |
|---|---|---|---|---|
| KR 1.1 | [Current] | [Target] | [On Track / At Risk / Off Track] | [Brief note] |
| KR 1.2 | [Current] | [Target] | [On Track / At Risk / Off Track] | [Brief note] |
| KR 1.3 | [Current] | [Target] | [On Track / At Risk / Off Track] | [Brief note] |

[Repeat for each objective]

### Blockers
| Blocker | Affected KR | Owner | Resolution Plan | Target Date |
|---|---|---|---|---|
| [Description] | [KR ref] | [Who] | [Plan] | [Date] |

### Key Decisions Made This Week
- [Decision 1]
- [Decision 2]

### Action Items
- [ ] [Action] -- @[Owner] -- Due [Date]
- [ ] [Action] -- @[Owner] -- Due [Date]
```

---

## 10. Monthly Scoring Template

```
## Monthly OKR Scoring -- [Team Name]
## Month: [Month Year]
## Scored By: [Name]

### Scoring Summary

| Objective | KR | Score (0.0-1.0) | Trajectory | Notes |
|---|---|---|---|---|
| Obj 1 | KR 1.1 | [Score] | [Improving / Flat / Declining] | [Note] |
| Obj 1 | KR 1.2 | [Score] | [Improving / Flat / Declining] | [Note] |
| Obj 1 | KR 1.3 | [Score] | [Improving / Flat / Declining] | [Note] |
| **Obj 1 Avg** | -- | **[Avg]** | -- | -- |
| Obj 2 | KR 2.1 | [Score] | [Improving / Flat / Declining] | [Note] |
| ... | ... | ... | ... | ... |

### Month-over-Month Comparison

| KR | Month 1 Score | Month 2 Score | Month 3 Score | Delta |
|---|---|---|---|---|
| KR 1.1 | [Score] | [Score] | [Score] | [+/- change] |
| ... | ... | ... | ... | ... |

### Course Corrections Needed
- [KR reference]: [What needs to change and why]

### Wins This Month
- [Win 1]
- [Win 2]

### Scope Changes (if any)
- [Change]: [Rationale]
```

---

## 11. Quarterly Retrospective Template

```
## Quarterly OKR Retrospective -- [Team Name]
## Quarter: [Q# Year]
## Date: [Date]
## Facilitator: [Name]
## Attendees: [Names]

---

### Part 1: Final Scores

| Objective | Type | KR | Final Score | Target Score | Delta |
|---|---|---|---|---|---|
| Obj 1: [Title] | [Committed/Aspirational] | KR 1.1 | [Score] | [Target] | [+/-] |
| | | KR 1.2 | [Score] | [Target] | [+/-] |
| | | KR 1.3 | [Score] | [Target] | [+/-] |
| **Obj 1 Average** | | | **[Avg]** | **[Target]** | **[+/-]** |
| ... | ... | ... | ... | ... | ... |

**Overall Team OKR Score: [Average of all objective averages]**

---

### Part 2: Objective-by-Objective Review

#### Objective 1: [Title]

**What went well:**
- [Point 1]
- [Point 2]

**What did not go well:**
- [Point 1]
- [Point 2]

**What did we learn:**
- [Learning 1]
- [Learning 2]

**What would we do differently:**
- [Change 1]
- [Change 2]

[Repeat for each objective]

---

### Part 3: Process Review

**OKR Setting Process:**
- Were the OKRs well-scoped? [Yes / No -- explain]
- Were the targets appropriately ambitious? [Yes / No -- explain]
- Did we have the right number of OKRs? [Yes / No -- explain]

**Tracking and Cadence:**
- Did we maintain weekly check-ins? [Yes / No]
- Were monthly scorings completed on time? [Yes / No]
- Did the tracking cadence help us course-correct? [Yes / No -- explain]

**Alignment:**
- Did our OKRs stay aligned with company goals? [Yes / No -- explain]
- Were cross-functional dependencies managed well? [Yes / No -- explain]

---

### Part 4: Carry-Forward Items

**Unfinished Key Results to Consider for Next Quarter:**
- [KR]: [Current score] -- [Recommendation: carry forward / drop / modify]

**New Insights That Should Inform Next Quarter:**
- [Insight 1]
- [Insight 2]

**Process Improvements for Next Quarter:**
- [Improvement 1]
- [Improvement 2]

---

### Part 5: Team Health Check

Rate each dimension 1-5 (1 = strongly disagree, 5 = strongly agree):

| Dimension | Score | Notes |
|---|---|---|
| We were aligned on priorities | [1-5] | [Note] |
| We had the right level of ambition | [1-5] | [Note] |
| We communicated blockers early | [1-5] | [Note] |
| We supported each other across KRs | [1-5] | [Note] |
| Leadership gave us the resources we needed | [1-5] | [Note] |
| We learned something valuable this quarter | [1-5] | [Note] |
```

---

## 12. Appendix: OKR Best Practices

See references/best-practices.md for the full appendix content (common mistakes, the OKR cycle, grading guidance by KR type, and recommended reading). Include it inline in the generated plan.
```
