---
name: agent-swarm-deployer
description: Deploys swarms of sub-agents for massive parallel data processing tasks. Unlike agent-army (which is for code changes), this is for DATA tasks -- processing 1000 documents, analyzing datasets, bulk content generation. Configurable swarm size, task distribution, result aggregation, progress tracking, and error recovery.
tools: Read, Write, Bash, Agent, Glob, Grep
user_invocable: true
---

# Agent Swarm Deployer

Deploy a swarm of parallel sub-agents to process massive, independent data tasks (documents, records, rows, items) and aggregate the results. Use this for data operations; use agent-army for code changes.

## Contents
- `references/overview.md` -- swarm vs army comparison, use cases, architecture diagram
- `references/swarm-design.md` -- input/output schemas, batch-size and swarm-size formulas, scaling guidelines
- `references/agent-brief.md` -- agent brief template, data distribution methods, progress tracking
- `references/aggregation-recovery.md` -- merge logic, completeness validation, retry strategy, error-handling table
- `references/output-formats.md` -- CSV/JSON/Markdown/individual-file outputs, final summary report
- `references/task-configs.md` -- ready-made configs for sentiment, lead scoring, content generation, summarization

## Workflow

1. Understand the task. Pin down five things before deploying anything: data source, operation per item, output format, output destination, and quality/validation requirements. If any is ambiguous, ask the user first -- a wrong spec wastes all agent compute.

2. Intake and inventory. Glob/Bash to locate and count items. Read 3-5 samples to learn structure. Estimate tokens per item and total. Report an intake summary (source, total count, item format, sample structure, token estimate).

3. Detect input schema and define output schema. Derive the input schema from samples; define the exact output schema the task requires. See `references/swarm-design.md`.

4. Design the swarm. Compute batch size from token budget (70% of ~200K usable context per agent) and swarm size from total items. Cap at 20 agents per wave; split into waves beyond that. Present the swarm plan and agent assignments, then get approval. See `references/swarm-design.md`.

5. Prepare agent briefs. Build a self-contained brief per agent: role, task, input data, output schema with example, quality rules, error protocol, and strict JSON output format. See `references/agent-brief.md`.

6. Distribute data and deploy. Choose a distribution method for the source type (pre-split CSVs/JSON with Bash; embed inline for small sets; pass file paths for directories). Launch up to 20 agents in parallel via the Agent tool with `run_in_background: true`, sending all calls in one message. Run later waves after the prior wave completes. See `references/agent-brief.md`.

7. Track progress. As agents return, record status, processed counts, and cumulative coverage. See `references/agent-brief.md`.

8. Collect and aggregate. Parse each agent's JSON; validate schema, completeness, and duplicates. Merge into one ordered output and extract failures. Report an aggregation summary with a coverage check and failure analysis. See `references/aggregation-recovery.md`.

9. Recover failures. Queue all failed and skipped items, deploy a retry agent with enhanced instructions, cap at 2 retries, and mark survivors "unrecoverable". Flag the user if unrecoverable items exceed 10%. See `references/aggregation-recovery.md`.

10. Write output and summarize. Produce the requested format (CSV, JSON, Markdown, or individual files) plus a final summary covering execution, results, quality metrics, patterns observed, and cost. See `references/output-formats.md`.

## Anti-Patterns to Avoid

1. Do not use a swarm for sequential tasks. If item N depends on item N-1, use a chain instead.
2. Do not deploy one agent per item. Batch items; one-per-agent wastes overhead.
3. Do not skip schema definition. Without a schema, merging results from many agents becomes unreliable.
4. Do not ignore failures. At 99% success, 1% of 10,000 items is still 100 failures. Always run retries.
5. Do not deploy without a sample run. Process 5 items manually first to validate the task and output quality before scaling.
