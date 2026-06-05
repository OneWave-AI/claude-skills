---
name: ai-readiness-assessment
description: Assesses how ready a business is for AI adoption across six dimensions. Evaluates data maturity, tech stack, team skills, process documentation, budget, and culture. Generates a comprehensive ai-readiness-report.md with scores, gap analysis, and recommended starting points. Aligned with OneWave AI's audit methodology.
tools: Read, Write, Glob, Grep, Bash, WebSearch, WebFetch
model: inherit
---

# AI Readiness Assessment Skill

Conduct a structured, evidence-based evaluation of a business's readiness for AI adoption across six dimensions, then produce a detailed `ai-readiness-report.md` covering scores, gap analysis, and prioritized next steps. Aligned with OneWave AI's pragmatic, ROI-driven audit methodology.

## Contents

- `references/dimensions.md` — The six dimensions, full 1-5 scoring rubric, and key questions per dimension.
- `references/methodology.md` — Information-gathering, scoring math and interpretation table, gap analysis, recommendation priorities, company-size and industry tailoring, and conversation flow.
- `references/output-template.md` — The complete `ai-readiness-report.md` structure to fill in.

## Workflow

1. Gather context. Collect information through conversation, document review, and codebase analysis. See `references/methodology.md` (Phase 1) for channels and the question set in `references/dimensions.md`.
2. Score the six dimensions. Rate each from 1 to 5 against the rubric in `references/dimensions.md`. Be honest and conservative, use half-points for nuance, and record the evidence behind every score.
3. Calculate the overall score. Apply the weighted formula and map it to a readiness level using the table in `references/methodology.md` (Phase 2).
4. Run the gap analysis. For each dimension below 4.0, document current state, target state, the gap, its impact, and the effort to close it (Phase 3).
5. Build recommendations. Produce prioritized actions across the five OneWave priority tiers, tailoring for company size and industry (Phase 4 and tailoring section).
6. Generate the report. Write `ai-readiness-report.md` following `references/output-template.md`, then highlight the top 3 immediate actions.

## The Six Dimensions

| Dimension | Weight |
|-----------|--------|
| Data Maturity | 25% |
| Technology Stack | 20% |
| Team Skills and Capacity | 20% |
| Process Documentation | 15% |
| Budget and Resources | 10% |
| Organizational Culture | 10% |

See `references/dimensions.md` for the full rubric and questions.

## Core Rules

1. Never inflate scores. A business that scores 2.0 needs to hear that honestly; false optimism wastes money and time.
2. Always provide evidence. Back every score with specific observations, not assumptions.
3. Be actionable. Pair every identified gap with a concrete recommendation.
4. Respect budget realities. Include cost-appropriate options; not every organization needs enterprise-grade solutions.
5. Use no jargon without explanation. The report is read by business leaders, not only technologists.
6. Flag deal-breakers. When a dimension scores 1.0, state explicitly that AI initiatives should not begin until it is addressed.
7. Consider the full cost. Include ongoing costs (maintenance, retraining, monitoring), not just implementation.
8. Recommend the right AI. Match recommendations to actual readiness; do not recommend deep learning to a company that has not consolidated its data.
9. Maintain OneWave AI alignment. Frame all recommendations within pragmatic, ROI-driven AI adoption. Avoid hype; focus on business value.
10. Use no emojis. Keep all output professional and text-based.
