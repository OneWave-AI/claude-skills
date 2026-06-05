---
name: sub-agent-orchestrator
description: Manages parent/child agent relationships with task delegation and result aggregation. Supports sequential chains, parallel fans, conditional routing, retry logic, timeout handling, and YAML-based visual workflow definition.
tools: Read, Write, Agent, Bash
user_invocable: true
---

# Sub-Agent Orchestrator

Design and execute multi-agent pipelines where each step is a different agent that depends on the previous one. Define roles, dependencies, and handoffs in YAML, then run sequential, parallel, conditional, loop, and map-reduce workflows with retry, timeout, and validation.

Unlike Agent Army (homogeneous parallel code changes) and Agent Swarm (homogeneous parallel data processing), this orchestrator coordinates heterogeneous pipelines where the output of A feeds the input of B.

## Contents

- `references/patterns.md` -- The six workflow patterns and the comparison to Agent Army/Swarm.
- `references/workflow-schema.md` -- Full YAML workflow definition language.
- `references/examples.md` -- Complete worked workflows (research-to-proposal, lead scoring).
- `references/execution-engine.md` -- Per-step execution model, retry, timeout, validation, edge cases.
- `references/templates.md` -- Reusable workflow scaffolds.
- `references/visual-and-reporting.md` -- Text diagrams and the execution report template.

## Workflow

1. Determine the mode from the request:
   - Run a workflow file: read the YAML at the given path.
   - Define and run inline: convert the natural-language description into a workflow YAML (see `references/workflow-schema.md`), then show it for approval.
   - Dry run: parse, validate, resolve inputs, and show the execution plan without deploying agents.
   - Inspect: parse the YAML and produce a human-readable description plus a text diagram (see `references/visual-and-reporting.md`).

2. Parse and validate the workflow: confirm required fields, that agent IDs resolve, and that there are no circular dependencies. Report syntax or reference errors with the offending line. See `references/execution-engine.md`.

3. Resolve inputs: collect every required input from the user before starting; apply defaults for optional inputs.

4. Build the execution DAG and run each step in topological order using the matching execution model (sequential, parallel, conditional, loop, map). See `references/execution-engine.md`.

5. After each agent completes, validate its output against the agent's schema and rules. On failure, apply the retry/timeout/failure policy (skip, abort, or fallback).

6. On completion, present results using the execution report template in `references/visual-and-reporting.md`. For partial or failed runs, report what completed, what failed, and any collected partial output.

## Choosing a pattern

Match the task shape to a pattern, then scaffold from `references/templates.md`:

- Strict ordering of distinct steps: sequential chain.
- One input scored or analyzed from multiple angles: parallel fan-out/fan-in.
- Input routed by classification: conditional routing.
- Output must meet a quality bar: loop with a validator.
- Large input chunked and recombined: map-reduce.
- A step needs a backup approach on failure: pipeline with fallback.

See `references/patterns.md` for diagrams and examples of each.
