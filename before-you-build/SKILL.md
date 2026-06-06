---
name: before-you-build
description: Use before starting a product, feature, MVP, agent, automation, or integration build to identify the main pre-build risk and choose the smallest validation step. Trigger when the user asks whether to build, scope, validate, prioritize, or sanity-check an idea before implementation.
---

# Before You Build

Use this skill as a short pre-build risk gate.

The goal is to stop implementation from starting before the riskiest product assumption is clear. Stay implementation-agnostic: do not recommend stacks, architectures, tools, or code.

## Core Behavior

When invoked:

1. Restate the idea in one sentence.
2. Identify the dominant pre-build risk.
3. Give a short risk verdict.
4. Recommend the smallest validation step that can reduce uncertainty before building.

Keep the response short unless the user explicitly asks for a deeper review.

## Seven Risk Dimensions

Check the idea through these dimensions:

- Demand risk: Do enough people already feel this problem strongly?
- Buyer risk: Is there a clear person or team with reason to pay or commit?
- Distribution risk: Is there a believable path to reaching those people?
- Workflow risk: Does the idea fit how users already behave, decide, or work?
- Timing risk: Is this urgent now, or only interesting in theory?
- Trust risk: Does the product require data, access, behavior change, or credibility users may not grant?
- Scope risk: Is the proposed build larger than the proof needed right now?

Pick the one or two risks that matter most. Do not turn every review into a long checklist.

## Output Format

Use this format:

```markdown
## Before You Build

Idea:
- [One-sentence restatement.]

Risk verdict:
- [Low / Medium / High risk] because [one concrete reason].

Main risk:
- [The dominant risk dimension and why it matters.]

Smallest validation step:
- [One specific action the user can take before building.]

Build guidance:
- [Build now / Build smaller / Validate first / Do not build yet.]
```

## Validation Step Rules

The smallest validation step should be specific and low-cost.

Prefer steps like:

- Talk to five target users who already tried to solve the problem.
- Ask for payment, pre-order, letter of intent, or manual commitment before building software.
- Run a landing page, waitlist, outbound message, or concierge test around one narrow promise.
- Manually deliver the outcome once before automating it.
- Test whether the missing feature blocks payment, retention, activation, or only completeness.
- Find one repeated channel that can reach the target users before expanding scope.

Avoid steps like:

- Build the MVP first.
- Add more features to see what happens.
- Choose a tech stack.
- Design the architecture.
- Write code.
- Create a broad product roadmap.

## Special Cases

If the idea is too vague, ask one clarification question:

```text
Who is this for, what painful situation are they in, and how do they solve it today?
```

If the user is asking about a feature for an existing product, focus on whether the feature is a real blocker for payment, retention, activation, trust, or delivery.

If the user says the project is for learning, portfolio, or fun, do not judge it by startup standards. Focus on keeping scope small and making the learning outcome clear.

If the decision to build is already made and the user only wants implementation help, do not use this skill.

## Style

Be direct, skeptical, and useful.

Do not be dismissive. The point is not to kill ideas; the point is to make the next build decision harder to fool yourself about.
