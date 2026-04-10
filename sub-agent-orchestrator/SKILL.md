---
name: sub-agent-orchestrator
description: Manages parent/child agent relationships with task delegation and result aggregation. Supports sequential chains, parallel fans, conditional routing, retry logic, timeout handling, and YAML-based visual workflow definition.
tools: Read, Write, Agent, Bash
user_invocable: true
---

# Sub-Agent Orchestrator

A workflow orchestration engine for designing and executing complex multi-agent pipelines. Define agent roles, dependencies, and handoff protocols using a YAML-based workflow syntax. Supports sequential chains, parallel fan-out/fan-in, conditional routing, retry logic, timeout handling, and structured result validation.

## Why This Exists

Agent Army deploys many agents doing the same type of work in parallel (homogeneous parallelism). Agent Swarm does the same for data processing. The Sub-Agent Orchestrator is different: it coordinates agents doing **different types of work** that depend on each other (heterogeneous pipelines).

Think of it as a workflow engine where each step is an intelligent agent, not a dumb function.

## Comparison

| Feature | Agent Army | Agent Swarm | Sub-Agent Orchestrator |
|---------|-----------|-------------|----------------------|
| Agent roles | Same (all do code changes) | Same (all do data processing) | Different (each has a unique role) |
| Execution pattern | Parallel fan-out | Parallel fan-out | Sequential, parallel, conditional, or mixed |
| Dependencies | File-level (import graph) | None (items are independent) | Task-level (output of A feeds input of B) |
| Use case | Bulk code changes | Bulk data processing | Complex workflows with multiple stages |

## Supported Workflow Patterns

### 1. Sequential Chain

```
[Agent A] --> [Agent B] --> [Agent C]
```

Each agent's output becomes the next agent's input. Use when tasks have strict ordering dependencies.

**Example**: Research a company (A) -> Draft a proposal (B) -> Review and polish (C)

### 2. Parallel Fan-Out / Fan-In

```
              /--> [Agent B1] --\
[Agent A] ---|                   |--> [Agent D]
              \--> [Agent B2] --/
```

Agent A produces output. Multiple agents process it in parallel. Agent D aggregates their results.

**Example**: Analyze a dataset (A) -> Score by 3 criteria in parallel (B1, B2, B3) -> Aggregate scores (D)

### 3. Conditional Routing

```
                    /--> [Agent B] (if condition X)
[Agent A] -- GATE -|
                    \--> [Agent C] (if condition Y)
```

Agent A's output is evaluated against conditions. The appropriate downstream agent is invoked based on the result.

**Example**: Classify a lead (A) -> If hot, draft proposal (B) / If cold, add to nurture (C)

### 4. Loop / Iteration

```
[Agent A] --> [Agent B] --> [Validator] --failed--> [Agent B] (retry)
                                        --passed--> [Done]
```

A validator agent checks the output. If it fails, the producing agent retries with feedback.

**Example**: Write a draft (A) -> Review for quality (B) -> If fails quality bar, rewrite with feedback (loop back to A)

### 5. Map-Reduce

```
[Splitter] --> [Agent 1] --\
           --> [Agent 2]  --|--> [Reducer]
           --> [Agent 3] --/
```

Split input into chunks, process in parallel, reduce to a single output.

**Example**: Split a long document into sections -> Summarize each section -> Combine into executive summary

### 6. Pipeline with Fallback

```
[Agent A] --success--> [Agent B]
           --failure--> [Fallback Agent A'] --success--> [Agent B]
```

If an agent fails, a fallback agent attempts the same task with a different approach.

## Workflow Definition Language (YAML)

Workflows are defined in YAML. The orchestrator parses this definition and executes it step by step.

### Schema

```yaml
workflow:
  name: string                    # Human-readable workflow name
  description: string             # What this workflow accomplishes
  version: string                 # Workflow version (semver)
  timeout: string                 # Global timeout (e.g., "30m", "2h")
  
  # Input variables available to all agents
  inputs:
    - name: string                # Variable name
      type: string                # string | number | boolean | json | file_path
      required: boolean
      default: any                # Default value if not provided
      description: string

  # Agent role definitions
  agents:
    agent_id:                     # Unique identifier (snake_case)
      name: string                # Human-readable name
      role: string                # Brief role description
      prompt: string              # Full prompt template (supports {{variable}} interpolation)
      tools: string[]             # Tools this agent can use (Read, Write, Bash, etc.)
      timeout: string             # Per-agent timeout (overrides global)
      retry:
        max_attempts: number      # Maximum retry attempts (default: 1, no retry)
        backoff: string           # none | linear | exponential
        on_failure: string        # skip | abort | fallback:{agent_id}
      validation:
        schema: object            # JSON schema for expected output
        rules: string[]           # Plain-English validation rules
      
  # Execution steps
  steps:
    - id: string                  # Step identifier
      agent: string               # Agent ID to execute
      type: string                # sequential | parallel | conditional | loop | map
      
      # For sequential steps
      input: string               # "{{inputs.variable}}" or "{{steps.prev_step.output}}"
      
      # For parallel steps
      parallel:
        - agent: string
          input: string
        - agent: string
          input: string
      wait: all | any | N         # Wait for all, any one, or N to complete
      
      # For conditional steps
      condition:
        eval: string              # Expression to evaluate (e.g., "{{steps.classify.output.category}} == 'hot'")
        true: string              # Step ID or agent ID to run if true
        false: string             # Step ID or agent ID to run if false
      
      # For loop steps
      loop:
        agent: string             # Agent to loop
        validator: string         # Validator agent ID
        max_iterations: number    # Safety limit
        feedback_path: string     # Where to get feedback from validator
      
      # For map steps  
      map:
        over: string              # Array to iterate over (e.g., "{{steps.split.output.chunks}}")
        agent: string             # Agent to run for each element
        reduce: string            # Reducer agent ID
      
      # Output handling
      output:
        store_as: string          # Variable name to store result
        format: string            # json | text | markdown
```

### Example Workflow: Research-to-Proposal Pipeline

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

### Example Workflow: Multi-Criteria Lead Scoring

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

## Execution Engine

The orchestrator follows this execution model when processing a workflow.

### Parse Phase

1. **Load workflow YAML** -- Read and parse the workflow definition
2. **Validate schema** -- Ensure all required fields are present, agent IDs are referenced correctly, no circular dependencies in sequential steps
3. **Resolve inputs** -- Collect all required inputs from the user, apply defaults for optional inputs
4. **Build execution graph** -- Convert steps into a directed acyclic graph (DAG) for execution ordering

### Execute Phase

For each step in topological order:

#### Sequential Step
```
1. Resolve input template (replace {{variables}} with actual values)
2. Build agent prompt from agent definition + resolved input
3. Deploy agent using Agent tool
4. Wait for completion
5. Validate output against agent's validation rules
6. Store output in step context
7. Proceed to next step
```

#### Parallel Step
```
1. Resolve all input templates
2. Build all agent prompts
3. Deploy ALL agents simultaneously (single message, multiple Agent tool calls)
4. Wait based on wait policy:
   - all: Wait for every agent to complete
   - any: Proceed when first agent completes
   - N: Proceed when N agents complete
5. Collect and validate all outputs
6. Store outputs (keyed by output_key) in step context
7. Proceed to next step
```

#### Conditional Step
```
1. Resolve the condition expression
2. Evaluate: parse the expression and determine true/false
3. Route to the appropriate agent/step based on the result
4. Execute that branch
5. Store output in step context
6. Proceed to next step
```

#### Loop Step
```
1. Execute the primary agent
2. Pass output to the validator agent
3. If validator returns passed=true: exit loop, store output
4. If validator returns passed=false:
   a. Extract feedback from validator
   b. Re-execute primary agent with original input + feedback
   c. Repeat from step 2
5. If max_iterations reached: store last output, flag as "max iterations reached"
```

#### Map Step
```
1. Resolve the array to iterate over
2. For each element, deploy an agent instance (parallel, batched if > 20)
3. Collect all results
4. Pass collected results to the reducer agent
5. Store reducer's output in step context
```

### Retry Logic

When an agent fails:

```
attempt = 1
while attempt <= max_attempts:
    result = deploy_agent(brief)
    if result.success:
        return result
    attempt += 1
    if backoff == "linear":
        wait(attempt * 5 seconds)  // conceptual, actual implementation uses re-deploy timing
    elif backoff == "exponential":
        wait(2^attempt seconds)

// All retries exhausted
if on_failure == "skip":
    store null output, continue workflow
elif on_failure == "abort":
    stop entire workflow, report failure
elif on_failure starts with "fallback:":
    deploy fallback agent with same input
```

### Timeout Handling

Three levels of timeout:

1. **Global timeout** -- If the entire workflow exceeds this, abort all running agents and report partial results
2. **Per-agent timeout** -- If a single agent exceeds this, trigger its retry/failure policy
3. **Step timeout** -- For parallel steps, the timeout applies to the wait policy (e.g., if wait=all and one agent times out, apply that agent's failure policy)

### Result Validation

After each agent completes, validate its output:

1. **Schema check** -- If a JSON schema is provided, validate the output structure
2. **Rule check** -- Evaluate each plain-English rule against the output:
   - "Must include X field" -- Check field presence
   - "Must identify exactly N items" -- Check array length
   - "Score must be between 0 and 100" -- Check value range
3. **Type check** -- Verify output format matches the expected format (json, text, markdown)

If validation fails, the output is treated as a failure and triggers the retry/failure policy.

## Orchestrator Commands

The user can invoke the orchestrator in several ways:

### Run a Workflow File

```
"Run the workflow at ./workflows/lead-scoring.yaml"
```

1. Read the YAML file
2. Prompt the user for any required inputs
3. Execute the workflow
4. Return results

### Define and Run Inline

```
"Set up a 3-step workflow: first research the company, then identify pain points, then draft an email"
```

1. Convert the natural language description into a workflow YAML
2. Show the YAML to the user for approval
3. Execute upon confirmation

### Dry Run

```
"Dry run the proposal workflow for Acme Corp"
```

1. Parse and validate the workflow
2. Resolve all inputs
3. Show the execution plan (which agents run in what order, expected inputs/outputs)
4. Do NOT actually deploy any agents

### Inspect Workflow

```
"Explain the lead-scoring workflow"
```

1. Parse the YAML
2. Generate a human-readable description of each step
3. Draw the execution graph (text-based)
4. List all agents and their roles

## Visual Workflow Representation

When presenting workflows to users, render them as text-based diagrams:

### Sequential
```
[1. Researcher] --> [2. Pain Identifier] --> [3. Pricing] --> [4. Writer] --> [5. Reviewer]
```

### Parallel Fan-Out/Fan-In
```
                    /--> [2a. Firmographic Scorer] --\
[1. Prepare Data] -+--> [2b. Technographic Scorer] --+--> [3. Aggregator]
                    \--> [2c. Intent Scorer] --------/
```

### Conditional
```
                        /--> [3a. Hot Lead Handler] (score >= 80)
[1. Research] --> [2. Score] --+--> [3b. Warm Lead Handler] (40 <= score < 80)
                        \--> [3c. Cold Lead Handler] (score < 40)
```

### Loop
```
[1. Writer] --> [2. Reviewer] --PASS--> [3. Deliver]
     ^                |
     |              FAIL
     \--- feedback ---/
     (max 3 iterations)
```

## Built-In Workflow Templates

### Template: Content Pipeline

```yaml
# Research -> Draft -> Review -> Publish
agents: [researcher, writer, editor, publisher]
pattern: sequential with review loop
use_when: "Creating any content that needs research and quality review"
```

### Template: Multi-Angle Analysis

```yaml
# Fan-out to N analysts -> Aggregate
agents: [N domain analysts, aggregator]
pattern: parallel fan-out/fan-in
use_when: "Need multiple perspectives on a single topic"
```

### Template: Qualify-and-Route

```yaml
# Classify -> Route to specialist
agents: [classifier, specialist_a, specialist_b, specialist_c]
pattern: conditional routing
use_when: "Different inputs need different handling"
```

### Template: Iterative Refinement

```yaml
# Generate -> Validate -> Refine (loop) -> Deliver
agents: [generator, validator]
pattern: loop with validation
use_when: "Output must meet a quality bar and may need multiple passes"
```

### Template: Map-Reduce

```yaml
# Split -> Process each -> Combine
agents: [splitter, processor, reducer]
pattern: map-reduce
use_when: "Large input needs to be chunked, processed, and recombined"
```

## Error Handling and Edge Cases

| Scenario | Handling |
|----------|---------|
| Required input missing | Prompt user before starting |
| Agent returns empty output | Treat as failure, trigger retry/fallback |
| Circular dependency in steps | Reject workflow at parse time with clear error |
| Parallel step with one failure | Apply that agent's failure policy; others continue |
| Loop exceeds max_iterations | Exit loop, store last output, flag in report |
| Global timeout reached | Abort all running agents, collect partial results, report |
| Workflow YAML syntax error | Report the error line and suggest correction |
| Agent references undefined variable | Report at parse time, not runtime |
| Conditional eval is ambiguous | Default to false branch, log warning |
| Fallback agent also fails | Treat as abort for that step |

## Reporting

After workflow completion, present:

```
## Workflow Execution Report: [workflow name]

### Execution Summary
- Status: COMPLETE / PARTIAL / FAILED
- Total steps: N
- Steps completed: N
- Steps failed: N
- Steps skipped: N
- Total agents deployed: N
- Total time: Xm Ys
- Retries used: N

### Step-by-Step Results
| Step | Agent | Status | Duration | Retries | Output Size |
|------|-------|--------|----------|---------|-------------|
| 1 | researcher | SUCCESS | 45s | 0 | 2.1KB |
| 2 | pain_identifier | SUCCESS | 30s | 0 | 1.4KB |
| 3 | pricing | SUCCESS | 35s | 1 | 1.8KB |
| 4 | writer | SUCCESS | 90s | 0 | 8.2KB |
| 5 | reviewer | SUCCESS | 40s | 0 | 0.9KB |

### Final Output
[The workflow's final deliverable]

### Issues and Warnings
- [Any retries, fallbacks, or validation warnings]
- [Agent notes or flags]
```
