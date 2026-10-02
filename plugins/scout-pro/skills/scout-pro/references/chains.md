# Chain Design and Library

A chain is a sequence of skills where each skill's output feeds into the next skill's input.

## Design Principles

1. **Minimize manual handoffs**: Each step should produce output the next step can directly consume.
2. **Include validation steps**: Add review/check steps for quality assurance.
3. **Parallel when possible**: Identify steps that can run simultaneously.
4. **Graceful degradation**: If one step fails, the chain should still produce partial value.
5. **Clear data contracts**: Define what data flows between steps.

## Chain Notation

```
Chain: [Chain Name]
Purpose: [What this chain accomplishes end-to-end]
Estimated Time: [Total time for all steps]

Step 1: /skill-name
  Input: [What goes in]
  Output: [What comes out]
  Duration: ~[X] minutes
  |
  v
Step 2: /skill-name
  Input: [Output from Step 1]
  Output: [What comes out]
  Duration: ~[X] minutes
  |
  v
Step 3: /skill-name
  Input: [Output from Step 2]
  Output: [Final deliverable]
  Duration: ~[X] minutes

Total: ~[X] minutes
Dependencies: [Any external requirements]
```

## Common Chain Patterns

### Research-to-Content Chain
```
/expert-panel -> /content-repurposer -> /seo-optimizer -> /social-repurposer
```
Use when the user needs to create authoritative content on a topic they are not expert in.

### Competitive Intelligence Chain
```
/competitor-content-analyzer -> /competitor-price-tracker -> /weak-signal-synthesizer -> /executive-dashboard-generator
```
Use when the user needs a comprehensive competitive landscape analysis.

### Sales Campaign Chain
```
/lookalike-customer-finder -> /contact-hunter -> /prospect-research-compiler -> /personalization-at-scale -> /cold-email-sequence-generator
```
Use when the user needs to build and execute an outbound sales campaign from scratch.

### Product Launch Chain
```
/landing-page-copywriter -> /seo-optimizer -> /email-template-generator -> /social-selling-content-generator -> /utm-parameter-generator
```
Use when the user is launching a new product or feature and needs full marketing collateral.

### Code Quality Chain
```
/code-review-pro -> /test-coverage-improver -> /performance-profiler -> /dependency-auditor -> /docker-debugger
```
Use when the user wants a comprehensive code quality audit and improvement.

### Documentation Chain
```
/api-documentation-writer -> /technical-writer -> /knowledge-base-builder -> /flashcard-generator
```
Use when the user needs complete documentation for a product or API.

### Deal Strategy Chain
```
/sales-call-prep-assistant -> /deal-momentum-analyzer -> /objection-pattern-detector -> /proposal-writer
```
Use when the user is preparing for an important sales meeting or deal.

### Content Repurposing Chain
```
/meeting-intelligence -> /content-repurposer -> /linkedin-post-optimizer -> /email-template-generator
```
Use when the user has meeting notes or transcripts to turn into marketing content.

## Custom Chain Builder Protocol

When the user asks to build a custom chain:

1. **Understand the end goal**: What is the final deliverable?
2. **Decompose into steps**: What intermediate outputs are needed?
3. **Match skills to steps**: Which skill produces each intermediate output?
4. **Identify gaps**: Where no skill exists, flag for manual intervention or suggest creating a new skill.
5. **Optimize ordering**: Determine which steps run in parallel and which can be skipped for a minimum viable result.
6. **Estimate timing**: How long will the full chain take?
7. **Define checkpoints**: Where should the user review progress before continuing?

Output the chain in the standard notation above, plus a `chain-config.yaml` file:

```yaml
chain:
  name: string
  description: string
  created: datetime
  estimated_minutes: integer
  steps:
    - order: integer
      skill: string
      description: string
      input_source: enum[user, previous_step, file, api]
      input_path: string
      output_format: string
      output_path: string
      checkpoint: boolean    # Should user review before next step?
      parallel_with: array[integer]  # Step numbers that can run simultaneously
      on_failure: enum[stop, skip, retry, manual]
      timeout_minutes: integer
  data_flow:
    - from_step: integer
      to_step: integer
      data_key: string
      transformation: string  # Any data transformation needed between steps
```
