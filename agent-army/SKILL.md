---
name: agent-army
description: Deploy a 2-layer parallel agent hierarchy to tackle large tasks at maximum speed. Layer 1 is a team of 3+ specialist agents. Layer 2 is 2+ sub-agents per team member. No upper limit on either layer. Use when a task is large enough to benefit from massive parallelization.
user_invocable: true
---

# Agent Army

A 2-layer parallel execution framework that decomposes large tasks into a coordinated hierarchy of agents working simultaneously. Designed for tasks where raw parallelism dramatically reduces wall-clock time.

## Architecture

```
You (Commander)
 |
 |-- Layer 1: Agent Team (minimum 3 members, no maximum)
 |    |
 |    |-- Team Member A  (own full context window)
 |    |    |-- Sub-agent A1  (spawned by A)
 |    |    |-- Sub-agent A2  (spawned by A)
 |    |    |-- ...           (no maximum)
 |    |
 |    |-- Team Member B  (own full context window)
 |    |    |-- Sub-agent B1  (spawned by B)
 |    |    |-- Sub-agent B2  (spawned by B)
 |    |    |-- ...
 |    |
 |    |-- Team Member C  (own full context window)
 |    |    |-- Sub-agent C1  (spawned by C)
 |    |    |-- Sub-agent C2  (spawned by C)
 |    |    |-- ...
 |    |
 |    |-- ... (no maximum team members)
```

## Constraints

| Rule | Value |
|------|-------|
| **Minimum team members (Layer 1)** | 3 |
| **Maximum team members (Layer 1)** | No limit -- scale to the task |
| **Minimum sub-agents per member (Layer 2)** | 2 |
| **Maximum sub-agents per member (Layer 2)** | No limit -- scale to the workload |

## When to Use

- Large refactors spanning many files
- Multi-file color/style/naming migrations
- Broad codebase audits (security, accessibility, performance)
- Bulk content generation or transformation
- Any task where independent units of work can run simultaneously

## When NOT to Use

- Small tasks (fewer than 6 independent units of work)
- Tasks with heavy sequential dependencies where parallelism adds no value
- Single-file changes

## Execution Protocol

Follow these steps precisely when this skill is invoked.

### Step 1: Reconnaissance

Before spawning anything, gather the full scope of work:

1. **Scan** -- Use Grep, Glob, and Read to identify every file and location affected by the task.
2. **Quantify** -- Count the total units of work (files, components, endpoints, etc.).
3. **Classify** -- Group the work into logical domains (e.g., by feature area, file type, directory, concern).

Output a brief **Scope Report** to the user:

```
## Scope Report
- Total files affected: N
- Total changes estimated: N
- Domains identified: [list]
```

### Step 2: Army Composition

Design the team structure based on the scope:

1. **Determine Layer 1 size** -- At least 3 team members. One member per logical domain. If a domain is large, split it across multiple members.
2. **Determine Layer 2 size** -- At least 2 sub-agents per team member. Assign sub-agents based on file count: roughly 1-3 files per sub-agent, depending on complexity.
3. **Name every agent** -- Give each team member and sub-agent a clear, descriptive name (e.g., `forms-agent`, `charts-agent`, `blog-migration-A`).
4. **Define ownership** -- Each file is owned by exactly one sub-agent. No overlaps. No gaps.

Output the **Army Plan** to the user:

```
## Army Plan

### Layer 1: Team Members (N total)
| # | Name | Domain | Files | Sub-agents |
|---|------|--------|-------|------------|
| 1 | [name] | [domain] | N files | N sub-agents |
| 2 | ... | ... | ... | ... |

### Layer 2: Sub-agent Assignments
**[Team Member Name]**
- Sub-agent [name]: file1.tsx, file2.tsx
- Sub-agent [name]: file3.tsx, file4.tsx

(repeat for each team member)
```

### Step 3: Briefing

Each agent -- both team members and their sub-agents -- must receive a **complete, self-contained brief**. Agents do not share context. Every brief must include:

1. **Objective** -- What to do, in one sentence.
2. **Approved patterns** -- The exact values, palette, conventions, or patterns to use. Include concrete examples (e.g., `replace teal-400 with [#c2a87e]`).
3. **Forbidden patterns** -- What to avoid or remove.
4. **File list** -- The exact files this agent owns. Absolute paths.
5. **Rules** -- Any constraints (e.g., "do not change error/validation colors", "preserve functionality", "do not modify imports").
6. **Sub-agent instructions** (Layer 1 only) -- Tell each team member exactly how many sub-agents to spawn, what to name them, and which files to assign to each. Include the full brief template so team members can pass it down.

### Step 4: Deploy

1. **Launch all Layer 1 agents in parallel** -- Use the Agent tool with `run_in_background: true`. Send ALL team member Agent calls in a single message to maximize parallelism.
2. **Each team member launches their Layer 2 sub-agents in parallel** -- The team member's brief instructs them to immediately spawn their sub-agents (also in parallel via a single message with multiple Agent calls).
3. **Sub-agents execute their file edits** -- Each sub-agent reads its assigned files, makes the changes, and reports completion.
4. **Team members collect sub-agent results** -- Each team member verifies all sub-agents completed successfully.

### Step 5: Verification

After all agents complete:

1. **Re-scan** -- Run the same Grep/Glob searches from Step 1 to check for any remaining violations.
2. **Report** -- Show the user:
   - Total changes made
   - Any files that still need attention
   - Any errors or conflicts encountered
3. **Mop up** -- If any violations remain, either fix them directly or spawn a small follow-up agent.

## Prompt Template for Layer 1 Team Members

Use this template when briefing each team member. Fill in the bracketed values.

```
You are [AGENT_NAME], a specialist on the [DOMAIN] domain.

## Objective
[One sentence: what to accomplish]

## Approved Patterns
[List exact values/patterns to use. Be concrete -- include hex codes, class names, etc.]

## Forbidden Patterns
[List what to remove/avoid]

## Your Files
[List absolute file paths]

## Rules
[Any constraints]

## Sub-agent Deployment

You MUST spawn [N] sub-agents in parallel (in a single message with multiple Agent tool calls). Each sub-agent gets its own files and the same approved/forbidden patterns.

Assign files as follows:
- Sub-agent "[SUB_NAME_1]": [file1, file2]
- Sub-agent "[SUB_NAME_2]": [file3, file4]
[...]

For each sub-agent, pass this brief:
"You are [SUB_NAME]. Read each file, apply the approved patterns, remove the forbidden patterns, and verify your changes. Files: [list]. Approved: [list]. Forbidden: [list]. Rules: [list]."

After all sub-agents complete, verify their work by reading each file and confirming no forbidden patterns remain. Report your results.
```

## Prompt Template for Layer 2 Sub-agents

```
You are [SUB_AGENT_NAME], working under [TEAM_MEMBER_NAME].

## Objective
[One sentence]

## Files You Own
[Absolute paths -- only touch these]

## Approved Patterns
[Exact values to use]

## Forbidden Patterns
[Exact values to remove/replace]

## Rules
[Constraints]

## Process
1. Read each file completely before making changes.
2. Apply all approved patterns, replacing all forbidden patterns.
3. Do NOT touch code outside your forbidden/approved scope.
4. After editing, re-read each file to verify no forbidden patterns remain.
5. Report: files changed, number of replacements, any issues.
```

## Scaling Guidelines

| Task Size | Team Members | Sub-agents/Member | Total Agents |
|-----------|-------------|-------------------|--------------|
| 6-12 files | 3 | 2 | 9 |
| 12-25 files | 4-5 | 2-3 | 12-20 |
| 25-50 files | 5-8 | 3-4 | 20-40 |
| 50-100 files | 8-12 | 3-5 | 32-72 |
| 100+ files | 12+ | 4+ | 60+ |

These are guidelines, not hard rules. Scale to the actual work -- the only hard constraints are the minimums (3 team members, 2 sub-agents each).

## Error Handling

- **Sub-agent fails**: Team member retries the sub-agent's files directly or spawns a replacement.
- **Team member fails**: Commander spawns a replacement with the same brief.
- **File conflict**: If two agents accidentally touch the same file, the commander resolves it manually after all agents complete.
- **Partial completion**: If interrupted, the verification step (Step 5) catches anything missed.

## Example Invocation

User: "Replace all neon Tailwind colors with our sand palette across the site"

Commander runs reconnaissance, finds 45 files with neon colors across 5 domains (forms, charts, blog posts, sections, pages). Composes an army of 5 team members with 2-4 sub-agents each (15 total sub-agents). All 5 team members launch in parallel, each immediately spawning their sub-agents in parallel. 20 agents working simultaneously. Full migration completed in a single wave.
