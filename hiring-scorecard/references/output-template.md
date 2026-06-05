# Scorecard Output Template

Generate a single `scorecard.md` file in the current working directory (or a path the user specifies) using the structure below. Make the scorecard thorough, actionable, and ready to hand to an interview panel without further editing.

---

## Section 1: Role Summary

```markdown
# Hiring Scorecard: [Job Title]

## Role Summary

- **Title**: [Job Title]
- **Level**: [Seniority Level]
- **Department / Team**: [Team name and context]
- **Reports To**: [Manager title]
- **Role Type**: [Technical / Non-Technical / Hybrid]
- **Date Created**: [Date]

### Why This Role Exists
[2-3 sentences on the business need this hire addresses]

### What Success Looks Like at 90 Days
[3-5 bullet points describing concrete outcomes for the first 90 days]

### What Success Looks Like at 1 Year
[3-5 bullet points describing concrete outcomes for the first year]
```

---

## Section 2: Must-Have vs Nice-to-Have Criteria

Separate qualifications into two tiers. Make each criterion specific and observable, never vague.

```markdown
## Criteria

### Must-Have (Non-Negotiable)

These are hard requirements. A candidate missing ANY must-have is a no-hire regardless of other strengths.

| # | Criterion | How to Verify | Weight |
|---|-----------|---------------|--------|
| M1 | [Specific, measurable criterion] | [Interview question, work sample, or reference] | [1-5] |
| M2 | ... | ... | ... |

### Nice-to-Have (Differentiators)

These separate good candidates from great ones. No single nice-to-have is required.

| # | Criterion | How to Verify | Bonus Weight |
|---|-----------|---------------|--------------|
| N1 | [Specific criterion] | [Verification method] | [1-3] |
| N2 | ... | ... | ... |
```

Guidelines for criteria:
- Must-haves: 5-8 criteria maximum. If everything is must-have, nothing is.
- Nice-to-haves: 4-6 criteria. These are tiebreakers.
- Give every criterion a concrete verification method.
- Weight reflects relative importance within its tier.
- For technical roles: include both technical skills AND collaboration/communication criteria in must-haves.
- For non-technical roles: include both domain expertise AND analytical/problem-solving criteria.
- For leadership roles: include people management, strategic thinking, and stakeholder management.

---

## Section 3: Competency Definitions and Scoring Rubric

Define each competency with a 1-5 behavioral anchoring scale. This eliminates subjective interpretation.

```markdown
## Scoring Rubric

Use the following scale for ALL competencies:

| Score | Label | Definition |
|-------|-------|------------|
| 1 | Strong No Hire | Significant gaps. Evidence of inability or misalignment. |
| 2 | Lean No Hire | Below the bar. Could develop but not ready for this level. |
| 3 | Neutral | Meets minimum bar. No strong signal either way. |
| 4 | Lean Hire | Above the bar. Clear evidence of competency at this level. |
| 5 | Strong Hire | Exceptional. Would raise the team's average in this area. |

---

### Competency: [Name] (Weight: X/5)

**What we are looking for**: [2-3 sentence description of what this competency means for THIS specific role]

| Score | Behavioral Anchor |
|-------|-------------------|
| 1 | [Concrete example of what a 1 looks like in an interview] |
| 2 | [Concrete example of what a 2 looks like] |
| 3 | [Concrete example of what a 3 looks like] |
| 4 | [Concrete example of what a 4 looks like] |
| 5 | [Concrete example of what a 5 looks like] |

[Repeat for each competency -- typically 6-10 competencies total]
```

See `competency-library.md` for which competencies to include per role type.

---

## Section 4: Interview Questions by Competency

Provide 3-4 questions per competency. Mix behavioral ("Tell me about a time...") and situational ("How would you handle..."). Include follow-up probes.

```markdown
## Interview Questions

### [Competency Name]

**Question 1** (Behavioral)
> "Tell me about a time when [specific scenario relevant to this role and competency]."

Follow-up probes:
- What was your specific role vs the team's?
- What was the outcome? How did you measure success?
- What would you do differently?

**What good looks like**: [Description of a strong answer]
**What bad looks like**: [Description of a weak answer]

---

**Question 2** (Situational)
> "Imagine you are in this role and [specific realistic scenario]. How would you approach it?"

Follow-up probes:
- What information would you need first?
- Who would you involve?
- How would you handle [complication]?

**What good looks like**: [Description of a strong answer]
**What bad looks like**: [Description of a weak answer]

---

**Question 3** (Technical / Domain-Specific) -- if applicable
> "[Role-specific question testing depth]"

Follow-up probes:
- [Probe that tests depth vs surface knowledge]
- [Probe that tests judgment, not just knowledge]

**What good looks like**: [Description of a strong answer]
**What bad looks like**: [Description of a weak answer]

[Repeat for each competency]
```

Question quality standards:
- Never ask illegal or discriminatory questions (age, family status, religion, disability, etc.).
- Reference specific, job-relevant situations in behavioral questions.
- Make situational questions reflect realistic challenges of THIS role, not generic hypotheticals.
- Give every question a clear "what good looks like" so interviewers calibrate consistently.
- Include at least one question per competency that probes failure/adversity; how candidates handle setbacks reveals more than how they handle wins.
- For technical roles: include a live problem-solving or system design component, not just Q&A.
- For leadership roles: include questions about difficult people decisions (firing, reorganizing, managing out).

---

## Section 5: Evaluation Matrix (Interviewer Scoresheet)

A fill-in-the-blank scoresheet each interviewer completes independently BEFORE the debrief.

```markdown
## Evaluation Matrix

**Candidate Name**: _______________
**Interviewer**: _______________
**Interview Date**: _______________
**Interview Focus Area**: _______________

### Scores

| Competency | Weight | Score (1-5) | Evidence / Notes |
|------------|--------|-------------|------------------|
| [Competency 1] | [X] | ___ | |
| [Competency 2] | [X] | ___ | |
| [Competency 3] | [X] | ___ | |
| ... | ... | ___ | |

### Weighted Total: ___ / [Max possible]

### Overall Recommendation

- [ ] Strong Hire
- [ ] Hire
- [ ] Lean Hire
- [ ] Lean No Hire
- [ ] No Hire
- [ ] Strong No Hire

### Key Strengths (Top 2-3)
1.
2.
3.

### Key Concerns (Top 2-3)
1.
2.
3.

### Would this candidate raise the average of the current team in their area? (Yes / No / Unsure)

### Additional Notes
```

Evaluation matrix rules:
- Interviewers MUST fill this out independently before any group discussion. This prevents anchoring bias.
- The "Evidence / Notes" column is mandatory, not optional. A score without evidence is not valid.
- Calculate the weighted total as SUM(weight * score) for all competencies.
- Keep the overall recommendation consistent with the weighted total but allow for holistic judgment.
- Include the "raise the average" question; it cuts through score inflation.

---

## Section 6: Red Flags and Green Flags

Concrete, observable signals, not vague feelings.

```markdown
## Red Flags and Green Flags

### Red Flags (Potential Disqualifiers)

These are warning signs that should trigger deeper investigation or a no-hire decision.

**Behavioral Red Flags**
- [Specific observable behavior and why it matters for this role]
- [Another specific red flag]
- ...

**Technical Red Flags** (for technical roles)
- [Specific technical gap or pattern]
- ...

**Cultural / Team Fit Red Flags**
- [Specific misalignment signal]
- ...

**Process Red Flags**
- [Resume inconsistencies, reference dodging, etc.]
- ...

### Green Flags (Strong Positive Signals)

These are indicators that a candidate is likely to succeed in this specific role.

**Behavioral Green Flags**
- [Specific observable behavior and why it predicts success]
- [Another specific green flag]
- ...

**Technical Green Flags** (for technical roles)
- [Specific technical strength or pattern]
- ...

**Cultural / Team Fit Green Flags**
- [Specific alignment signal]
- ...

**Process Green Flags**
- [Preparation quality, follow-up quality, etc.]
- ...
```

Flag guidelines:
- 8-12 red flags, 8-12 green flags per scorecard.
- Tie every flag to an observable behavior, not an inference about personality.
- Calibrate flags to the seniority level (what is a red flag for a VP is normal for a junior hire).
- Include at least 2 flags specific to the team context if provided.
- Never include flags that proxy for protected characteristics.

---

## Section 7: Reference Check Questions

Targeted questions that go beyond "Would you hire them again?"

```markdown
## Reference Check Questions

### Opening
- "Thanks for taking the time. I want to make sure we set [candidate] up for success if they join. Your honest input helps us do that."
- "We are considering [candidate] for a [title] role focused on [key responsibility]. Can you help me understand how they performed in similar areas?"

### Performance and Impact
1. "On a scale of 1-10, how would you rate [candidate]'s overall performance? ... What would it take to be a 10?"
2. "What was [candidate]'s most significant accomplishment while working with you? What made it significant?"
3. "Can you describe a project where [candidate] fell short of expectations? What happened and how did they respond?"

### Working Style and Collaboration
4. "How would you describe [candidate]'s working style? What type of environment do they thrive in?"
5. "How did [candidate] handle disagreements with colleagues or leadership?"
6. "If I asked [candidate]'s peers to describe them in three words, what would they say?"

### Role-Specific Questions
7. "[Question specific to the primary competency of the role]"
8. "[Question specific to the team context or a known challenge of the role]"
9. "[Question probing a specific concern that emerged during interviews]"

### Leadership Questions (for manager+ roles)
10. "How many people reported to [candidate]? How did they handle underperformers?"
11. "Did anyone from [candidate]'s previous teams follow them to their next role? Why or why not?"
12. "How did [candidate] handle making an unpopular decision?"

### Closing
13. "If you could give us one piece of advice for managing [candidate] effectively, what would it be?"
14. "Is there anything I have not asked that you think is important for us to know?"
```

Reference check guidelines:
- Always ask the 1-10 rating question; it anchors the conversation and the follow-up ("What would it take to be a 10?") reveals real development areas.
- Ask about failures, not just successes. A reference who cannot name a single shortcoming is not being candid.
- Customize 2-3 questions based on concerns or open questions from the interview process.
- For back-channel references (with candidate permission), adjust tone to be more conversational.
- Pay attention to what references do NOT say as much as what they do say.
- If a reference is clearly reading from a script or giving only generic praise, probe deeper with specific scenario questions.

---

## Section 8: Debrief Guide

How the hiring panel should run the post-interview debrief.

```markdown
## Debrief Guide

### Before the Debrief
- All interviewers submit their scoresheets independently (no sharing before the meeting)
- Hiring manager collects and reviews all scoresheets for patterns
- Identify any score discrepancies of 2+ points on the same competency

### Debrief Agenda (45-60 minutes)

1. **Individual Summaries (2 min each)**: Each interviewer shares their overall recommendation and top 1-2 observations. No rebuttals yet.

2. **Competency Walk-Through (20-30 min)**: Go through each competency. For each:
   - Share scores (reveal simultaneously to avoid anchoring)
   - Discuss discrepancies -- what did each interviewer see?
   - Reach consensus score with documented evidence

3. **Red Flag Review (5 min)**: Did anyone observe a red flag? Discuss as a group.

4. **Green Flag Review (5 min)**: What were the strongest positive signals?

5. **Must-Have Checklist (5 min)**: Go through must-have criteria. Does the candidate pass all of them?

6. **Final Vote (5 min)**: Each interviewer gives their final recommendation. Hiring manager makes the call.

### Decision Framework

- **Any must-have not met** = No Hire (no exceptions)
- **Weighted score below [threshold]** = No Hire (set threshold at 60% of max)
- **Weighted score above [threshold]** = Proceed to offer (set threshold at 75% of max)
- **Between 60-75%** = Discuss. Consider: Would you bet your own quota/OKRs on this person?
- **Split panel** = Hiring manager decides, but must document reasoning

### Anti-Bias Checklist
Before finalizing the decision, the panel should ask:
- Are we comparing this candidate to the job requirements or to other candidates?
- Are we weighting recent interviews more heavily than earlier ones? (Recency bias)
- Did a single strong/weak moment override the full picture? (Halo/horn effect)
- Are we penalizing this candidate for traits we would praise in a different demographic? (Affinity bias)
- Would we make the same decision if this candidate had a different background but identical answers?
```

---

## Section 9: Appendix

```markdown
## Appendix

### Scoring Calculator

Total weighted score = SUM(competency_weight * competency_score) for all competencies

Maximum possible score = SUM(competency_weight * 5) for all competencies

Percentage = (Total weighted score / Maximum possible score) * 100

| Percentage | Recommendation |
|------------|----------------|
| 85-100% | Strong Hire |
| 75-84% | Hire |
| 65-74% | Borderline -- requires strong justification |
| 50-64% | No Hire |
| Below 50% | Strong No Hire |

### Interview Panel Assignment Template

| Interviewer | Role | Competencies to Assess | Interview Format | Duration |
|-------------|------|------------------------|------------------|----------|
| [Name] | Hiring Manager | [Competencies] | Behavioral | 45 min |
| [Name] | Peer | [Competencies] | Technical / Collaborative | 60 min |
| [Name] | Cross-functional | [Competencies] | Situational | 30 min |
| [Name] | Skip-level | [Competencies] | Values / Culture | 30 min |

### Candidate Comparison Matrix (for finalist stage)

| Competency | Weight | Candidate A | Candidate B | Candidate C |
|------------|--------|-------------|-------------|-------------|
| [Comp 1] | [X] | ___ | ___ | ___ |
| [Comp 2] | [X] | ___ | ___ | ___ |
| ... | ... | ... | ... | ... |
| **Weighted Total** | | ___ | ___ | ___ |
| **Overall Rec** | | ___ | ___ | ___ |
```
