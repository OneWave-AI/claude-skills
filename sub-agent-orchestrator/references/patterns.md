# Supported Workflow Patterns

The orchestrator coordinates agents doing different types of work that depend on each other (heterogeneous pipelines). This contrasts with Agent Army (homogeneous parallel code changes) and Agent Swarm (homogeneous parallel data processing).

| Feature | Agent Army | Agent Swarm | Sub-Agent Orchestrator |
|---------|-----------|-------------|----------------------|
| Agent roles | Same (all do code changes) | Same (all do data processing) | Different (each has a unique role) |
| Execution pattern | Parallel fan-out | Parallel fan-out | Sequential, parallel, conditional, or mixed |
| Dependencies | File-level (import graph) | None (items are independent) | Task-level (output of A feeds input of B) |
| Use case | Bulk code changes | Bulk data processing | Complex workflows with multiple stages |

## 1. Sequential Chain

```
[Agent A] --> [Agent B] --> [Agent C]
```

Each agent's output becomes the next agent's input. Use when tasks have strict ordering dependencies.

Example: Research a company (A) -> Draft a proposal (B) -> Review and polish (C)

## 2. Parallel Fan-Out / Fan-In

```
              /--> [Agent B1] --\
[Agent A] ---|                   |--> [Agent D]
              \--> [Agent B2] --/
```

Agent A produces output. Multiple agents process it in parallel. Agent D aggregates their results.

Example: Analyze a dataset (A) -> Score by 3 criteria in parallel (B1, B2, B3) -> Aggregate scores (D)

## 3. Conditional Routing

```
                    /--> [Agent B] (if condition X)
[Agent A] -- GATE -|
                    \--> [Agent C] (if condition Y)
```

Agent A's output is evaluated against conditions. The appropriate downstream agent is invoked based on the result.

Example: Classify a lead (A) -> If hot, draft proposal (B) / If cold, add to nurture (C)

## 4. Loop / Iteration

```
[Agent A] --> [Agent B] --> [Validator] --failed--> [Agent B] (retry)
                                        --passed--> [Done]
```

A validator agent checks the output. If it fails, the producing agent retries with feedback.

Example: Write a draft (A) -> Review for quality (B) -> If fails quality bar, rewrite with feedback (loop back to A)

## 5. Map-Reduce

```
[Splitter] --> [Agent 1] --\
           --> [Agent 2]  --|--> [Reducer]
           --> [Agent 3] --/
```

Split input into chunks, process in parallel, reduce to a single output.

Example: Split a long document into sections -> Summarize each section -> Combine into executive summary

## 6. Pipeline with Fallback

```
[Agent A] --success--> [Agent B]
           --failure--> [Fallback Agent A'] --success--> [Agent B]
```

If an agent fails, a fallback agent attempts the same task with a different approach.
