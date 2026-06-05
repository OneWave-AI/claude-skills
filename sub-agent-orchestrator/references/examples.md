# Example Workflows

## Research-to-Proposal Pipeline (sequential with review loop)

```yaml
workflow:
  name: research-to-proposal
  description: Research a prospect company and generate a personalized consulting proposal
  version: "1.0.0"
  timeout: "15m"

  inputs:
    - name: company_name
      type: string
      required: true
      description: Target company name
    - name: contact_name
      type: string
      required: true
      description: Primary contact at the company
    - name: our_services
      type: string
      required: true
      description: Description of our service offerings
    - name: rough_scope
      type: string
      required: false
      default: ""
      description: Any known scope details

  agents:
    researcher:
      name: Company Researcher
      role: Gather intelligence about the target company
      prompt: |
        You are a business research analyst. Research {{inputs.company_name}} and compile:
        1. Company overview (size, industry, recent news)
        2. Key challenges in their industry
        3. Technology stack (if detectable)
        4. Recent hiring patterns (signals growth areas)
        5. Competitor landscape

        Use web search and any available tools. Return structured JSON.
      tools: [Read, Bash, WebSearch]
      timeout: "3m"
      retry:
        max_attempts: 2
        on_failure: skip
      validation:
        rules:
          - "Output must include company_overview field"
          - "Output must include key_challenges array"

    pain_identifier:
      name: Pain Point Identifier
      role: Identify specific pain points we can solve
      prompt: |
        Given this research about {{inputs.company_name}}:
        {{steps.research.output}}

        And our services:
        {{inputs.our_services}}

        Identify the top 3 pain points where our services align with their needs.
        For each pain point, explain:
        1. The problem (from their perspective)
        2. The business impact (cost, time, risk)
        3. How our service addresses it

        Return as structured JSON array.
      tools: [Read]
      timeout: "2m"
      validation:
        rules:
          - "Must identify exactly 3 pain points"
          - "Each pain point must have problem, impact, and solution fields"

    pricing_analyst:
      name: Pricing Analyst
      role: Develop pricing tiers based on scope
      prompt: |
        Given these pain points for {{inputs.company_name}}:
        {{steps.identify_pains.output}}

        Scope details: {{inputs.rough_scope}}

        Create 3 pricing tiers:
        1. Starter: Addresses the primary pain point only
        2. Growth: Addresses top 2 pain points with deeper engagement
        3. Enterprise: Full scope, all 3 pain points, ongoing support

        For each tier, provide:
        - Name and tagline
        - Scope description
        - Deliverables list
        - Timeline
        - Price range (provide realistic consulting rates)
        - ROI justification

        Return as structured JSON.
      tools: [Read]
      timeout: "2m"

    proposal_writer:
      name: Proposal Writer
      role: Draft the full proposal document
      prompt: |
        Write a professional consulting proposal for {{inputs.company_name}},
        contact: {{inputs.contact_name}}.

        Research data: {{steps.research.output}}
        Pain points: {{steps.identify_pains.output}}
        Pricing tiers: {{steps.pricing.output}}

        Structure:
        1. Executive Summary (personalized to their situation)
        2. Understanding of Your Challenges (mirror their pain points)
        3. Proposed Approach (our methodology)
        4. Scope and Deliverables (3 tiers)
        5. Timeline
        6. Investment (pricing tiers)
        7. Why Us (differentiators)
        8. Next Steps

        Tone: Professional, confident, consultative. Not salesy.
        Length: 2000-3000 words.
        Format: Markdown.
      tools: [Read, Write]
      timeout: "4m"

    reviewer:
      name: Quality Reviewer
      role: Review proposal for quality and accuracy
      prompt: |
        Review this proposal for {{inputs.company_name}}:
        {{steps.draft.output}}

        Check for:
        1. Factual accuracy (does it match the research data?)
        2. Personalization (does it feel generic or tailored?)
        3. Pricing reasonableness (are the tiers realistic?)
        4. Professional tone (no typos, no overselling)
        5. Completeness (all 8 sections present?)

        Return a review with:
        - overall_score (1-10)
        - passed (boolean, true if score >= 7)
        - feedback (array of specific improvements)
        - critical_issues (array, empty if none)
      tools: [Read]
      timeout: "2m"
      validation:
        rules:
          - "Must include overall_score field"
          - "Must include passed boolean"

  steps:
    - id: research
      agent: researcher
      type: sequential
      input: "{{inputs.company_name}}"
      output:
        store_as: research_data
        format: json

    - id: identify_pains
      agent: pain_identifier
      type: sequential
      input: "{{steps.research.output}}"
      output:
        store_as: pain_points
        format: json

    - id: pricing
      agent: pricing_analyst
      type: sequential
      input: "{{steps.identify_pains.output}}"
      output:
        store_as: pricing_tiers
        format: json

    - id: draft
      agent: proposal_writer
      type: sequential
      input: "all prior context"
      output:
        store_as: proposal_draft
        format: markdown

    - id: review
      type: loop
      loop:
        agent: proposal_writer
        validator: reviewer
        max_iterations: 2
        feedback_path: "{{steps.review.output.feedback}}"
      output:
        store_as: final_proposal
        format: markdown
```

## Multi-Criteria Lead Scoring (parallel fan-out/fan-in)

```yaml
workflow:
  name: multi-criteria-lead-scoring
  description: Score a lead from 3 different angles in parallel, then aggregate
  version: "1.0.0"
  timeout: "5m"

  inputs:
    - name: lead_data
      type: json
      required: true
      description: Lead data object with name, company, title, etc.
    - name: icp_criteria
      type: json
      required: true
      description: Ideal Customer Profile criteria

  agents:
    firmographic_scorer:
      name: Firmographic Scorer
      role: Score based on company attributes
      prompt: |
        Score this lead on firmographic fit (0-100):
        Lead: {{inputs.lead_data}}
        ICP: {{inputs.icp_criteria}}

        Evaluate: company size, industry, geography, revenue range.
        Return: { score: number, breakdown: object, reasoning: string }
      tools: [Read]
      timeout: "1m"

    technographic_scorer:
      name: Technographic Scorer
      role: Score based on tech stack alignment
      prompt: |
        Score this lead on technographic fit (0-100):
        Lead: {{inputs.lead_data}}
        ICP: {{inputs.icp_criteria}}

        Evaluate: current tech stack, tools they use, technical maturity.
        Return: { score: number, breakdown: object, reasoning: string }
      tools: [Read]
      timeout: "1m"

    intent_scorer:
      name: Intent Scorer
      role: Score based on buying signals
      prompt: |
        Score this lead on buying intent (0-100):
        Lead: {{inputs.lead_data}}

        Evaluate: recent job postings, funding rounds, tech changes, content consumption.
        Return: { score: number, signals: string[], reasoning: string }
      tools: [Read, Bash]
      timeout: "1m"

    aggregator:
      name: Score Aggregator
      role: Combine scores into final recommendation
      prompt: |
        Aggregate these parallel scoring results for lead {{inputs.lead_data.name}}:

        Firmographic: {{steps.parallel_scoring.outputs.firmographic}}
        Technographic: {{steps.parallel_scoring.outputs.technographic}}
        Intent: {{steps.parallel_scoring.outputs.intent}}

        Calculate weighted final score:
        - Firmographic: 40% weight
        - Technographic: 30% weight
        - Intent: 30% weight

        Return:
        {
          final_score: number,
          category: "hot" | "warm" | "cold" | "disqualify",
          recommended_action: string,
          summary: string,
          breakdown: { firmographic, technographic, intent }
        }
      tools: [Read]
      timeout: "1m"

  steps:
    - id: parallel_scoring
      type: parallel
      parallel:
        - agent: firmographic_scorer
          input: "{{inputs.lead_data}}"
          output_key: firmographic
        - agent: technographic_scorer
          input: "{{inputs.lead_data}}"
          output_key: technographic
        - agent: intent_scorer
          input: "{{inputs.lead_data}}"
          output_key: intent
      wait: all
      output:
        store_as: parallel_scores
        format: json

    - id: aggregate
      agent: aggregator
      type: sequential
      input: "{{steps.parallel_scoring.outputs}}"
      output:
        store_as: final_score
        format: json
```
