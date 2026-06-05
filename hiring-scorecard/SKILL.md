---
name: hiring-scorecard
description: Creates structured hiring scorecards for any role. Takes job title, requirements, and team context. Generates comprehensive scorecard with weighted scoring rubric, interview questions per competency, evaluation matrix, red/green flags, and reference check questions.
tools: Read, Write, Glob, Grep
model: inherit
---

# Hiring Scorecard Generator

Build a structured, bias-reducing hiring scorecard that lets an interview panel make consistent, evidence-based decisions for any role.

## Contents

- `references/output-template.md` -- the full 9-section `scorecard.md` structure with every block, table, and per-section guideline.
- `references/competency-library.md` -- which competencies to score by role type (technical IC, non-technical IC, manager, executive).
- `references/usage-and-customization.md` -- how to use the output, focus modes, biases prevented, format adaptations, and legal/compliance reminders.

## Inputs

Job Title and Requirements are required; ask before generating if either is missing. The rest sharpen the output: Team Context, Level/Seniority, Role Type, Industry, Interview Panel, Compensation Band, Urgency/Timeline.

## Workflow

1. **Gather role context.** Confirm job title, level, team structure, reporting line, and business need. Ask for missing required inputs.
2. **Define criteria.** Separate must-have from nice-to-have qualifications, each specific and observable with a verification method. See `references/output-template.md` Section 2.
3. **Select competencies.** Choose 6-10 competencies for the role using `references/competency-library.md`.
4. **Build the scoring rubric.** Anchor each competency to the 1-5 behavioral scale. See `references/output-template.md` Section 3.
5. **Generate interview questions.** Write 3-4 behavioral/situational questions per competency with follow-up probes and "what good/bad looks like". See `references/output-template.md` Section 4.
6. **Create the evaluation matrix.** Produce the independent interviewer scoresheet. See Section 5.
7. **Identify flags.** List 8-12 concrete red flags and 8-12 green flags tied to observable behavior. See Section 6.
8. **Draft reference checks.** Produce targeted reference questions that surface real signal. See Section 7.
9. **Add debrief guide and appendix.** Include the debrief agenda, decision framework, anti-bias checklist, scoring calculator, and panel/comparison templates. See Sections 8-9.
10. **Write the file.** Output a single `scorecard.md` in the working directory (or a user-specified path), assembled from all nine sections and ready to hand to a panel without further editing.

For focus modes (technical, leadership, sales/GTM, creative, operations, culture-heavy), format adaptations, and legal/compliance reminders, see `references/usage-and-customization.md`.
