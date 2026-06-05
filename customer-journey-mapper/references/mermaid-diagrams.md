# Mermaid Diagram Requirements

Generate TWO Mermaid diagrams in the document. All diagrams must use valid syntax that renders correctly.

## 1. Journey Overview Diagram (near the top)
A simplified `journey` diagram showing the high-level flow:

```mermaid
journey
    title Customer Journey: [Product Name]
    section Awareness
      Discovers problem: 3: Prospect
      Finds brand via search: 3: Prospect
      Reads blog content: 4: Prospect
    section Consideration
      Requests demo: 4: Prospect
      Attends webinar: 4: Prospect, Sales
      Compares alternatives: 3: Prospect
    section Decision
      Negotiates pricing: 3: Prospect, Sales
      Signs contract: 5: Customer, Sales
    section Onboarding
      Completes setup: 4: Customer, Support
      First value moment: 5: Customer
    section Retention
      Regular usage: 5: Customer
      Contacts support: 3: Customer, Support
    section Expansion
      Upgrades plan: 4: Customer, Sales
      Adds team members: 5: Customer
    section Advocacy
      Writes review: 5: Advocate
      Refers colleague: 5: Advocate
```

## 2. Full Detail Diagram (in the dedicated section)
A more comprehensive diagram with granular touchpoints and accurate satisfaction scores (1-5) based on the analysis. Each touchpoint must have a realistic satisfaction score reflecting the emotional state described in the stage analysis.

## Satisfaction Scoring Guide

Use this scale consistently across all diagrams and analysis:

| Score | Meaning | Emotional State |
|---|---|---|
| 1 | Extremely frustrated | Angry, considering abandoning |
| 2 | Dissatisfied | Annoyed, experiencing significant friction |
| 3 | Neutral | Neither positive nor negative, functional |
| 4 | Satisfied | Positive experience, expectations met |
| 5 | Delighted | Exceeded expectations, memorable positive moment |
