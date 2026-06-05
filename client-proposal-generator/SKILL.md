---
name: client-proposal-generator
description: Generates full consulting proposals from a brief. Input client name, problem description, and rough scope. Outputs proposal.md with executive summary, problem statement, proposed approach, timeline, team, pricing tiers, and terms. Researches client company for personalization. Multiple pricing models. Professional formatting matching consulting standards.
tools: Read, Write, Bash, WebSearch, Glob
user_invocable: true
---

# Client Proposal Generator

Transform a brief description into a complete, professionally formatted consulting proposal (`proposal.md`), researching the client company for personalization and structuring the document with proven consulting frameworks.

## Contents

- `references/inputs.md` -- Required and optional inputs, defaults, one-liner extraction
- `references/research.md` -- Client web research checklist and research brief template
- `references/problem-and-solution.md` -- Problem decomposition, methodology selection, phase and deliverable templates
- `references/timeline.md` -- Duration estimation and timeline format
- `references/team.md` -- Role framework and team section format
- `references/pricing.md` -- Pricing models, 3-tier framework, rate benchmarks, calibration, payment terms
- `references/terms.md` -- Standard terms and conditions block
- `references/output-template.md` -- Full proposal document structure and delivery summary
- `references/tone-and-quality.md` -- Tone variants, pre-delivery quality checklist, error handling

## Workflow

1. Gather input. Collect required fields (client name, contact, problem, firm name) and optional fields; infer the rest from context. See `references/inputs.md`.
2. Research the client. Pull company overview, recent news, tech signals, industry context, and competitors; organize into a research brief. See `references/research.md`.
3. Frame the problem and design the solution. Decompose into root problem, symptoms, business impact, stakeholders, and urgency; select a methodology and define phases and deliverables. See `references/problem-and-solution.md`.
4. Construct the timeline. Estimate duration, lay out phases with milestones, and state dependencies and assumptions. See `references/timeline.md`.
5. Compose the team. Map roles and allocations; use placeholder names if none provided and never fabricate credentials. See `references/team.md`.
6. Build pricing. Select a model (default: 3-tier fixed), set tier prices from rate benchmarks or a supplied budget, and add payment terms. See `references/pricing.md`.
7. Add terms and conditions. Insert the standard block, adjusting scope, IP, and assumptions to the engagement. See `references/terms.md`.
8. Assemble and write the proposal. Combine all sections into the output structure and write the file. See `references/output-template.md`.
9. Run the quality check. Verify accuracy, consistency, no placeholders, and no fabricated facts; match the selected tone. See `references/tone-and-quality.md`.
10. Deliver and summarize. Write to the output path and present the delivery summary with personalization applied and review recommendations. See `references/output-template.md`.

## Guardrails

- Never fabricate case studies, team bios, credentials, or client facts. Omit rather than invent.
- If web research yields nothing, proceed without personalization and flag it.
- Leave no placeholder markers in the delivered document.
