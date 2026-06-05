---
name: customer-journey-mapper
description: Maps the full customer journey from first touch to advocacy. Generates a comprehensive customer-journey.md with all stages, touchpoints, emotions, pain points, opportunities, Mermaid diagrams, and metrics. Use when mapping customer experience, designing onboarding flows, identifying churn risks, or optimizing conversion funnels.
tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
model: inherit
---

# Customer Journey Mapper

Produce a comprehensive, actionable customer journey map spanning every stage from initial awareness through long-term advocacy.

## Contents
- `references/journey-stages.md` — the seven stages and the dimensions to analyze for each
- `references/output-template.md` — exact structure for the generated `customer-journey.md`
- `references/mermaid-diagrams.md` — both required Mermaid diagrams and the satisfaction scoring guide
- `references/examples.md` — invocation examples, research protocol, and ambiguity handling

## Workflow

1. **Collect inputs.** Gather Product/Service, Target Persona, Touchpoints (optional), and Channels. When any are missing, infer reasonable values and document the assumptions at the top of the output. Ask one clarifying question only when the product type is genuinely unclear.

2. **Research context.** Use WebSearch to ground the map in real reviews, complaints, competitor comparisons, and industry patterns. See `references/examples.md` for the research protocol.

3. **Map all seven stages.** Build a detailed stage-by-stage analysis covering Awareness, Consideration, Decision, Onboarding, Retention, Expansion, and Advocacy. See `references/journey-stages.md` for the dimensions to cover per stage.

4. **Identify opportunities.** Surface pain points, emotional states, and improvement opportunities at every stage. Include honest friction even in generally positive stages, and cross-reference how one stage's issues create downstream effects.

5. **Generate the deliverable.** Write `customer-journey.md` to the current working directory following `references/output-template.md`. Include both Mermaid diagrams per `references/mermaid-diagrams.md`.

## Required Inputs

| Input | Description | Example |
|---|---|---|
| **Product/Service** | What is being sold or offered | "B2B SaaS project management tool" |
| **Target Persona** | Who the primary customer is | "VP of Engineering at mid-market companies, 200-1000 employees" |
| **Touchpoints** | Known interaction points (optional) | "Google search, blog, demo request, sales call, onboarding email sequence" |
| **Channels** | Active marketing/sales/support channels | "Website, email, LinkedIn, phone, in-app, Slack community" |

## Quality Requirements

1. **Minimum 400 lines** of substantive content, not padded whitespace.
2. **Specificity**: Tie every touchpoint, pain point, and opportunity to the given product and persona — no generic filler.
3. **Actionability**: Make recommendations concrete enough to begin implementation immediately.
4. **Measurable metrics**: State how each metric is actually measured, not just what to measure.
5. **Emotional realism**: Reflect genuine customer psychology, not idealized happy paths.
6. **Honest pain points**: Include real friction even in positive stages.
7. **No emojis** anywhere in the output document.
8. **Mermaid validity**: Use valid syntax that renders correctly.
9. **Consistent voice**: Keep professional, strategic language throughout — a working document for product and marketing teams.
10. **Cross-references**: Connect each stage's issues to their downstream effects.
