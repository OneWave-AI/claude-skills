---
name: agent-army
description: Deploy a 2-layer parallel agent hierarchy to tackle large tasks at maximum speed. Layer 1 is a team of 3-50+ agents, each with their own independent context window. Layer 2 is 2+ sub-agents per team member, each with their own context seeded by the parent's brief. No upper limit on either layer.
user_invocable: true
---

# Agent Army

A 2-layer parallel execution framework. Each Layer 1 agent gets its own independent context window (currently 1M tokens). Each spawns Layer 2 sub-agents that also get their own context, seeded with the parent's brief. Every agent reasons independently. Not one brain divided -- many brains deployed.

## Architecture

```
You (Commander)
 |
 |-- Layer 1: Agent Team (minimum 3 members, no maximum)
 |    |  Each member = own full context window (1M tokens)
 |    |
 |    |-- Team Member A  (1M context)
 |    |    |-- Sub-agent A1  (own context)
 |    |    |-- Sub-agent A2  (own context)
 |    |    |-- ...           (no maximum)
 |    |
 |    |-- Team Member B  (1M context)
 |    |    |-- Sub-agent B1  (own context)
 |    |    |-- Sub-agent B2  (own context)
 |    |    |-- ...
 |    |
 |    |-- Team Member C  (1M context)
 |    |    |-- Sub-agent C1  (own context)
 |    |    |-- Sub-agent C2  (own context)
 |    |    |-- ...
 |    |
 |    |-- ... (no maximum team members)
```

**Key distinction:** Traditional agent "swarms" share one context window -- one brain, divided. Agent Army deploys independent agents, each with its own full context window. Sub-agents also get their own context, seeded with their parent's brief. Every instance reasons independently.

## NON-NEGOTIABLE RULES

These rules are MANDATORY. Violating any of them is a failure state. Do not rationalize skipping them.

1. **EVERY Layer 1 agent MUST spawn 2+ sub-agents.** No exceptions. No "this task is simple enough for one agent." If you are about to deploy a Layer 1 agent without sub-agents, STOP and restructure. The user chose this skill because they want the full hierarchy.

2. **NEVER silently reduce the army size.** If the user chose Aggressive tier, deploy Aggressive. Do not quietly drop to 3 agents because "it seemed sufficient." Match the tier or explain why you can't.

3. **Report progress as agents complete.** Do not go silent after deploying. Every time an agent finishes, immediately tell the user: "[Agent N/M complete] name: X files modified, Y flags." This is not optional.

4. **Show the army plan before deploying (Full Mode).** Do not skip the plan. The user needs to see which agents own which files before you launch. In Quick Mode, you may skip the plan confirmation but you MUST still compose one internally.

5. **Sub-agent briefs go INSIDE the Layer 1 prompt.** Each team member must receive explicit instructions to spawn their sub-agents. If you forget to include sub-agent deployment instructions in the Layer 1 brief, the sub-agents will not exist.

6. **Build check after every wave.** Run the project's build command. If it fails, that's a new wave trigger. Do not skip the build check.

7. **If the user says "keep going" or "don't stop", enter continuous mode.** Launch new agents as each completes. Do not wait for all to finish. Do not ask permission for each new launch.

Failure to follow these rules means the skill was not executed correctly. The user will notice and will call it out.

## Army Size Selection

Before composing the army, ask the user what concurrency level they want. Present this table:

```
How many parallel agents should I deploy?

| Tier | Team Members | Total Agents | Speed | Estimated Token Cost |
|------|-------------|--------------|-------|---------------------|
| Conservative | 3 | 9 | Methodical | ~$2-5 |
| Standard | 5-10 | 15-30 | Good balance | ~$5-15 |
| Aggressive | 10-20 | 30-60 | Fast, heavy parallel | ~$15-40 |
| Maximum | 20+ | 60+ | Full speed | ~$40+ |
| Custom | You pick | You pick | You decide | Varies |

Each agent is an independent Claude instance with its own full context window.
More agents = faster completion, but more API token usage.
Your machine just orchestrates -- all compute runs on Anthropic's servers.
Token costs are rough estimates and vary by task complexity.

Pick a tier (or enter a custom number):
```

If the user picks a tier, scale the army composition to match. If they skip or say "just do it", default to Standard (5-10 team members). Never silently reduce below the user's chosen tier.

## Constraints

| Rule | Value |
|------|-------|
| **Minimum team members (Layer 1)** | 3 (or user's chosen tier minimum) |
| **Maximum team members (Layer 1)** | No limit -- scale to the task and user's tier |
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

## Progress Updates (MANDATORY)

You MUST report each agent's completion the moment it finishes. Do NOT batch updates. Do NOT wait for all agents. The user should never wonder "is anything happening?"

Format: `[Agent N/M complete] agent-name: X files modified, Y flags`

If an agent fails: `[Agent N/M FAILED] agent-name: error description -- spawning replacement`

## Continuous Deployment Mode

If the user says "keep going", "burn tokens", or "don't stop" -- enter continuous mode:
- As each agent completes, immediately launch a new agent for the next batch of work
- Don't wait for all agents to finish before starting more
- Keep deploying until the task is fully complete or the user says stop
- Report completions as they come in

## Sub-agent Enforcement (MANDATORY)

BEFORE deploying ANY Layer 1 agent, run this checklist. Do NOT proceed until all boxes are checked:

```
DEPLOYMENT GATE -- all must pass:
[x] Every Layer 1 agent brief contains "You MUST spawn N sub-agents"
[x] Every sub-agent is named and has specific files assigned
[x] Every file in the scope is owned by exactly one sub-agent
[x] Zero files are unassigned
[x] The Layer 1 brief includes the full sub-agent deployment instructions
```

If ANY check fails: STOP. Fix the plan. Then deploy.

There is ONE exception: if the total task has fewer than 6 independent units of work, sub-agents add overhead without value. In that case, explicitly tell the user: "This task has N units of work. Sub-agents would add overhead. Deploying N single agents instead. OK?" Wait for confirmation.

## Execution Protocol

Follow these steps precisely when this skill is invoked.

**Mode decision:** If scope is clear and specific (file paths, exact changes), skip to Step 3 (Quick Mode). Otherwise, start at Step 1 (Full Mode).

### Step 1: Intake Questions (Full Mode only)

Ask the user before starting recon:

1. **What's the goal?** (one sentence)
2. **What's the scope?** (specific files, directories, or "the whole site")
3. **Any constraints?** (don't touch X, preserve Y, match Z style)
4. **Which tier?** (show the Army Size Selection table)

If the user already provided this context in their request, don't re-ask. Just confirm: "I see you want [goal] across [scope]. Deploying at [tier] tier. Starting recon."

### Step 2: Git Safety Net

Before touching anything, create a rollback checkpoint:

1. **Check for uncommitted work** -- Run `git status`. If there are uncommitted changes, warn the user and ask if they want to stash or commit first.
2. **Create a checkpoint branch** -- Run `git checkout -b agent-army/checkpoint-{timestamp}` from the current HEAD, then switch back to the working branch. This gives the user a clean rollback point if the army makes things worse.
3. **Record the checkpoint** -- Note the branch name so it can be referenced in the final report.

If the project is not a git repo, warn the user that there is no rollback safety net and ask for confirmation before proceeding.

### Step 3: Reconnaissance

Before spawning anything, gather the full scope of work:

1. **Scan** -- Use Grep, Glob, and Read to identify every file and location affected by the task.
2. **Quantify** -- Count the total units of work (files, components, endpoints, etc.).
3. **Weigh files** -- Check line counts (`wc -l`). Flag files over 500 lines as "heavy" (assign solo).
4. **Classify into domains** -- Group by directory, import graph, file type, or naming pattern.
5. **Identify shared dependencies** -- Files imported across multiple domains are **foundation files** (see Step 4).

Output a **Scope Report** to the user:

```
## Scope Report
- Total files affected: N
- Heavy files (500+ lines): [list with line counts]
- Total changes estimated: N
- Domains identified: [list]
- Shared dependencies: [list -- files imported across domains]
- Estimated token cost: ~N agents x avg context = rough estimate
```

### Step 4: Army Composition

Design the team structure based on the scope:

1. **Handle shared dependencies first** -- If there are foundation files (shared types, configs, utilities) that multiple domains depend on, assign them to a **Foundation Agent** that runs BEFORE the rest of the army. This agent completes its edits first, then the parallel wave launches. This prevents edit conflicts on shared files.
2. **Determine Layer 1 size** -- At least 3 team members (not counting the Foundation Agent if needed). One member per logical domain. If a domain is large, split it across multiple members.
3. **Determine Layer 2 size** -- At least 2 sub-agents per team member. Assign sub-agents based on **weighted file load**, not just file count:
   - Small files (< 200 lines): 2-3 per sub-agent
   - Medium files (200-500 lines): 1-2 per sub-agent
   - Heavy files (500+ lines): 1 per sub-agent, solo
4. **Name every agent** -- Give each team member and sub-agent a clear, descriptive name (e.g., `forms-agent`, `charts-agent`, `blog-migration-A`).
5. **Define ownership** -- Each file is owned by exactly one sub-agent. No overlaps. No gaps. Foundation files are owned by the Foundation Agent.

Output the **Army Plan** to the user and **pause for confirmation** (this is the dry run checkpoint):

```
## Army Plan

### Foundation Agent (runs first, if needed)
- Files: [shared dependencies]
- Completes before main wave launches

### Layer 1: Team Members (N total)
| # | Name | Domain | Files | Weight | Sub-agents |
|---|------|--------|-------|--------|------------|
| 1 | [name] | [domain] | N files | N lines | N sub-agents |
| 2 | ... | ... | ... | ... | ... |

### Layer 2: Sub-agent Assignments
**[Team Member Name]**
- Sub-agent [name]: file1.tsx (120 lines), file2.tsx (85 lines)
- Sub-agent [name]: file3.tsx (650 lines) -- solo, heavy file

(repeat for each team member)

### Cost Estimate
- Total agents: N (Layer 1) + N (Layer 2) = N
- Approximate context: N files across N agents
- Checkpoint branch: agent-army/checkpoint-{timestamp}

Proceed? (Y to deploy, N to adjust)
```

### Step 5: Briefing

Each agent must receive a **complete, self-contained brief**. Agents do not share context. Every brief must include:

1. **Objective** -- What to do, in one sentence.
2. **Approved patterns** -- Exact values/conventions to use, with concrete examples.
3. **Forbidden patterns** -- What to avoid or remove.
4. **File list** -- Absolute paths with line counts.
5. **Rules** -- Any constraints (preserve functionality, don't touch X, etc.).
6. **Idempotency guard** -- Check if the approved pattern already exists before replacing; skip and note "already correct."
7. **Cross-team flag protocol** -- Issues outside your files go to "Flags for Commander" -- do NOT fix them.
8. **Sub-agent instructions** (Layer 1 only) -- How many sub-agents, their names, their file assignments.
9. **Structured report format** (see below).

### Step 6: Deploy and Verify

1. **Foundation Agent first (if needed)** -- Launch the Foundation Agent and wait for it to complete before proceeding. This ensures shared dependencies are updated before dependent files are touched.
2. **Launch all Layer 1 agents in parallel** -- Use the Agent tool with `run_in_background: true`. Send ALL team member Agent calls in a single message to maximize parallelism.
3. **Each team member launches their Layer 2 sub-agents in parallel** -- The team member's brief instructs them to immediately spawn their sub-agents (also in parallel via a single message with multiple Agent calls).
4. **Sub-agents execute their file edits** -- Each sub-agent reads its assigned files, makes the changes, and reports completion in the structured format.
5. **Team members collect sub-agent results** -- Each team member verifies all sub-agents completed successfully and aggregates their reports.

After all agents complete, run verification and wave assessment:

#### Verification

1. **Pattern re-scan** -- Run the same Grep/Glob searches from Step 3 to check for remaining violations.
2. **Build check** -- Run the project's build command (`npm run build`, `tsc --noEmit`, etc.). If unclear, ask the user.
3. **Review cross-team flags** -- Resolve any "Flags for Commander" items from agent reports.
4. **Final report:**

```
## Army Report
- Agents deployed: N (Layer 1) + N (Layer 2) = N total
- Files modified: N / Files skipped (already correct): N
- Build status: PASS / FAIL
- Cross-team flags: [list or "None"]
- Remaining violations: [list or "None"]
- Rollback: git checkout agent-army/checkpoint-{timestamp}
```

#### Multi-Wave Protocol

After each wave: run build, re-scan for violations, check flags. If issues remain, deploy a fix wave. Max 3 waves total.

- **Wave 1 (Execute):** The core task. Always runs.
- **Wave 2 (Fix):** Triggered by build failures, remaining violations, or cross-team flags. Smaller army targeting what Wave 1 missed.
- **Wave 3 (Propagate):** Update tests, docs, configs, and downstream files affected by changes.

Each wave is a new, smaller army. The Commander pauses for user approval before launching. Each wave's report is the next wave's recon. If issues persist after 3 waves, report to user for manual resolution.

## Structured Report Format

Every agent (both Layer 1 and Layer 2) must return results in this format:

```
## Report: [Agent Name]

### Files Modified
- file1.tsx: N replacements
- file2.tsx: N replacements

### Files Skipped (already correct)
- file3.tsx: all patterns already applied

### Flags for Commander
- [file path]: [description of cross-team issue]
- (or "None")

### Issues Encountered
- [description, or "None"]

### Status: COMPLETE / PARTIAL / FAILED
```

## Prompt Template for Layer 1 Team Members

```
You are [AGENT_NAME], specialist on [DOMAIN].

## Objective
[One sentence]

## Approved Patterns
[Exact values -- hex codes, class names, etc.]

## Forbidden Patterns
[What to remove/avoid]

## Your Files
[Absolute paths with line counts]

## Rules
- [Constraints]. Skip files already using approved patterns. Flag issues outside your files in "Flags for Commander" -- do NOT fix them.

## Sub-agent Deployment
Spawn [N] sub-agents in parallel (single message, multiple Agent calls). Each gets:
- Sub-agent "[NAME]": [files with line counts]
Pass each sub-agent: objective, their files, approved/forbidden patterns, rules, and the report format below. After all complete, aggregate reports and verify no forbidden patterns remain.
```

## Prompt Template for Layer 2 Sub-agents

```
You are [SUB_AGENT_NAME], working under [TEAM_MEMBER_NAME].

## Objective
[One sentence]

## Files You Own
[Absolute paths with line counts -- only touch these]

## Approved Patterns / Forbidden Patterns
[Exact values to use and remove]

## Rules
[Constraints]. Skip files already correct. Flag issues outside your files -- do NOT fix them.

## Report Format
Return: Files Modified (file: N replacements), Files Skipped (already correct), Flags for Commander, Issues Encountered, Status (COMPLETE/PARTIAL/FAILED).
```

## Scaling Guidelines

| Task Size | Team Members | Sub-agents/Member | Total Agents |
|-----------|-------------|-------------------|--------------|
| 6-12 files | 3 | 2 | 9 |
| 12-25 files | 4-5 | 2-3 | 12-20 |
| 25-50 files | 5-8 | 3-4 | 20-40 |
| 50-100 files | 8-12 | 3-5 | 32-72 |
| 100+ files | 12+ | 4+ | 60+ |

These are guidelines, not hard rules. Scale to the actual work -- the only hard constraints are the minimums (3 team members, 2 sub-agents each). Weight assignment by file size, not just file count.

## Error Handling

- **Sub-agent fails**: Team member retries the sub-agent's files directly or spawns a replacement.
- **Team member fails**: Commander spawns a replacement with the same brief.
- **File conflict**: Prevented by the ownership model (no overlaps) and Foundation Agent (shared deps handled first). If a conflict somehow occurs, the commander resolves it manually after all agents complete.
- **Partial completion**: The verification step (Step 6) catches anything missed. The structured report format makes it clear which files were and weren't completed.
- **Build failure after completion**: Compare against the checkpoint branch to determine if the failure is new. If new, diagnose from the agent reports and fix directly.
- **Idempotency on re-run**: Agents check for already-applied patterns before making changes, so running the army twice won't double-apply.

