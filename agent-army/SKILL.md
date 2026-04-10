---
name: agent-army
description: Deploy a 2-layer parallel agent hierarchy to tackle large tasks at maximum speed. Layer 1 is a team of 3+ specialist agents, each with their own full context window. Layer 2 is 2+ sub-agents per team member that split that context. No upper limit on either layer. Includes git safety, dependency awareness, build verification, and structured reporting.
user_invocable: true
---

# Agent Army

A production-grade 2-layer parallel execution framework that decomposes large tasks into a coordinated hierarchy of agents working simultaneously. Each Layer 1 agent gets its own full context window (currently 1M tokens). Each spawns Layer 2 sub-agents that split up that window. The result is an army of independent brains -- not one brain divided.

## Architecture

```
You (Commander)
 |
 |-- Layer 1: Agent Team (minimum 3 members, no maximum)
 |    |  Each member = own full context window (1M tokens)
 |    |
 |    |-- Team Member A  (1M context)
 |    |    |-- Sub-agent A1  (splits A's context)
 |    |    |-- Sub-agent A2  (splits A's context)
 |    |    |-- ...           (no maximum)
 |    |
 |    |-- Team Member B  (1M context)
 |    |    |-- Sub-agent B1  (splits B's context)
 |    |    |-- Sub-agent B2  (splits B's context)
 |    |    |-- ...
 |    |
 |    |-- Team Member C  (1M context)
 |    |    |-- Sub-agent C1  (splits C's context)
 |    |    |-- Sub-agent C2  (splits C's context)
 |    |    |-- ...
 |    |
 |    |-- ... (no maximum team members)
```

**Key distinction:** Agent "swarms" are sub-agents splitting one context window -- one brain, divided. Agent Army uses agent teams where each member has its own independent context window. That's the difference between dividing one brain and deploying many.

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

## Execution Protocol

Follow these steps precisely when this skill is invoked.

### Step 0: Git Safety Net

Before touching anything, create a rollback checkpoint:

1. **Check for uncommitted work** -- Run `git status`. If there are uncommitted changes, warn the user and ask if they want to stash or commit first.
2. **Create a checkpoint branch** -- Run `git checkout -b agent-army/checkpoint-{timestamp}` from the current HEAD, then switch back to the working branch. This gives the user a clean rollback point if the army makes things worse.
3. **Record the checkpoint** -- Note the branch name so it can be referenced in the final report.

If the project is not a git repo, warn the user that there is no rollback safety net and ask for confirmation before proceeding.

### Step 1: Reconnaissance

Before spawning anything, gather the full scope of work:

1. **Scan** -- Use Grep, Glob, and Read to identify every file and location affected by the task.
2. **Quantify** -- Count the total units of work (files, components, endpoints, etc.).
3. **Weigh files** -- Check line counts for each affected file (`wc -l`). Flag any file over 500 lines as "heavy" -- these consume significant context and should be assigned solo or paired with small files only.
4. **Classify into domains** -- Group the work into logical domains using these heuristics:
   - **Directory structure**: files in the same directory or feature folder are likely related
   - **Import graph**: files that import from each other belong together (reduces cross-agent dependencies)
   - **File type/concern**: components vs. utilities vs. tests vs. styles vs. configs
   - **Naming patterns**: files sharing a prefix or suffix (e.g., `*-form.tsx`, `*-chart.tsx`)
5. **Identify shared dependencies** -- Find files that are imported by files across multiple domains. These are **foundation files** and must be handled specially (see Step 2).

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

### Step 2: Army Composition

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

### Step 3: Briefing

Each agent must receive a **complete, self-contained brief**. Agents do not share context. Every brief must include:

1. **Objective** -- What to do, in one sentence.
2. **Approved patterns** -- The exact values, palette, conventions, or patterns to use. Include concrete examples (e.g., `replace teal-400 with [#c2a87e]`).
3. **Forbidden patterns** -- What to avoid or remove.
4. **File list** -- The exact files this agent owns. Absolute paths. Include line counts so the agent knows what it's working with.
5. **Rules** -- Any constraints (e.g., "do not change error/validation colors", "preserve functionality", "do not modify imports").
6. **Idempotency guard** -- Tell agents: "Before making a replacement, check if the approved pattern is already present. If a file already uses the correct pattern, skip it and note it as 'already correct' in your report."
7. **Cross-team flag protocol** -- Tell agents: "If you discover an issue that affects files outside your ownership (e.g., a broken import, a missing type), do NOT fix it. Instead, include it in your report under 'Flags for Commander' with the file path and description."
8. **Sub-agent instructions** (Layer 1 only) -- Tell each team member exactly how many sub-agents to spawn, what to name them, and which files to assign to each.
9. **Structured report format** (see below) -- Every agent must return results in this format.

### Step 4: Deploy

1. **Foundation Agent first (if needed)** -- Launch the Foundation Agent and wait for it to complete before proceeding. This ensures shared dependencies are updated before dependent files are touched.
2. **Launch all Layer 1 agents in parallel** -- Use the Agent tool with `run_in_background: true`. Send ALL team member Agent calls in a single message to maximize parallelism.
3. **Each team member launches their Layer 2 sub-agents in parallel** -- The team member's brief instructs them to immediately spawn their sub-agents (also in parallel via a single message with multiple Agent calls).
4. **Sub-agents execute their file edits** -- Each sub-agent reads its assigned files, makes the changes, and reports completion in the structured format.
5. **Team members collect sub-agent results** -- Each team member verifies all sub-agents completed successfully and aggregates their reports.

### Step 5: Verification

After all agents complete:

1. **Pattern re-scan** -- Run the same Grep/Glob searches from Step 1 to check for any remaining violations.
2. **Build check** -- Run the project's build/compile command (e.g., `npm run build`, `tsc --noEmit`, `cargo check`) to verify the project still compiles. If no build command is obvious, ask the user.
3. **Review cross-team flags** -- Check all "Flags for Commander" items from agent reports. Resolve any cross-team issues manually.
4. **Final report** -- Show the user:

```
## Army Report

### Summary
- Agents deployed: N (Layer 1) + N (Layer 2) = N total
- Files modified: N
- Files skipped (already correct): N
- Replacements made: N
- Build status: PASS / FAIL

### Cross-team Flags
- [any issues agents flagged for commander]

### Remaining Violations
- [any patterns still found by re-scan, or "None"]

### Rollback
- Checkpoint branch: agent-army/checkpoint-{timestamp}
- To undo all changes: `git checkout agent-army/checkpoint-{timestamp}`
```

5. **Wave assessment** -- Determine if follow-up waves are needed (see Multi-Wave Protocol below).

### Step 6: Multi-Wave Protocol

After Wave 1 (Execute) completes, the Commander assesses the report and determines if additional waves are needed. Each wave is adaptive -- its composition is shaped by the previous wave's output. Maximum 4 waves total. The Commander presents each wave assessment to the user and waits for approval before launching.

#### Wave Types

| Wave | Name | Triggered When | Purpose |
|------|------|---------------|---------|
| 1 | **Execute** | Always | The core task -- make the changes |
| 2 | **Audit** | Build fails, remaining violations, 20+ files changed, or cross-team flags | Fresh agents review Wave 1's work for consistency, edge cases, and correctness |
| 3 | **Propagate** | Changes touch APIs, types, or interfaces; tests or docs exist that reference old patterns | Update tests, docs, configs, changelogs, and downstream files |
| 4 | **Notify** | User opts in | Draft PR description, Slack summary, changelog entry, documentation updates |

#### Wave Assessment Protocol

After each wave completes, run this assessment:

1. **Re-scan** -- Check for remaining violations from the original task.
2. **Build check** -- Run the project's build command. Record PASS/FAIL.
3. **Review flags** -- Collect all "Flags for Commander" from agent reports.
4. **Score the wave** -- Based on the data:
   - **Remaining violations > 0** → Audit wave needed (target: fix what was missed)
   - **Build fails** → Audit wave needed (target: fix build errors)
   - **Cross-team flags > 0** → Audit wave needed (target: resolve flagged issues)
   - **20+ files modified AND no audit yet** → Audit wave recommended (fresh eyes catch what original agents miss)
   - **Changed files are imported by tests/docs** → Propagate wave needed
   - **User has specified notification channels** → Notify wave available

5. **Present the assessment**:

```
## Wave Assessment

Wave 1 (Execute) complete.
- Files modified: N
- Build: PASS / FAIL
- Remaining violations: N
- Cross-team flags: N

### Recommendation
- Wave 2 (Audit): [NEEDED / RECOMMENDED / NOT NEEDED] -- [reason]
- Wave 3 (Propagate): [NEEDED / NOT NEEDED] -- [reason]
- Wave 4 (Notify): [AVAILABLE if requested]

Launch Wave 2? (Y / skip to Wave 3 / done)
```

6. **Compose the next wave's army** -- Each follow-up wave gets its own army composition, typically smaller and differently specialized than Wave 1:
   - **Audit wave**: 3+ agents reviewing changed files with fresh context. Assign files that Wave 1 agents flagged or that the re-scan caught. Include a build-fix agent if the build failed.
   - **Propagate wave**: Agents assigned to test files, doc files, config files, and any downstream code that imports from modified files.
   - **Notify wave**: One agent per channel (PR drafter, Slack summarizer, changelog writer).

7. **Repeat** -- After each wave, run the assessment again. Stop when all checks pass or max waves (4) reached.

#### Wave Rules

- Waves are **adaptive, not predefined** -- skip any wave that isn't needed.
- Each wave is a **new, smaller army** -- different agents, different files, different purpose.
- The Commander **always pauses for user approval** before launching a new wave.
- **Max 4 waves** to prevent infinite loops. If issues persist after 4 waves, report them to the user for manual resolution.
- Wave 1's report is Wave 2's reconnaissance. Wave 2's report is Wave 3's recon. Each wave feeds the next.

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
[List absolute file paths with line counts]

## Rules
- [Any constraints]
- Before replacing, check if the approved pattern is already present. Skip files that are already correct.
- If you discover an issue affecting files outside your ownership, do NOT fix it. Add it to "Flags for Commander" in your report.

## Sub-agent Deployment

You MUST spawn [N] sub-agents in parallel (in a single message with multiple Agent tool calls). Each sub-agent gets its own files and the same approved/forbidden patterns.

Assign files as follows:
- Sub-agent "[SUB_NAME_1]": [file1 (N lines), file2 (N lines)]
- Sub-agent "[SUB_NAME_2]": [file3 (N lines)]
[...]

For each sub-agent, pass this brief:
"You are [SUB_NAME]. Read each file, apply the approved patterns, remove the forbidden patterns, and verify your changes. Files: [list]. Approved: [list]. Forbidden: [list]. Rules: [list]. Before replacing, check if the pattern is already correct -- skip if so. If you find issues outside your files, flag them but do NOT fix them. Return your results in this format: [structured report format]."

After all sub-agents complete, aggregate their reports into a single team report and verify no forbidden patterns remain in your files. Return the aggregated report.
```

## Prompt Template for Layer 2 Sub-agents

```
You are [SUB_AGENT_NAME], working under [TEAM_MEMBER_NAME].

## Objective
[One sentence]

## Files You Own
[Absolute paths with line counts -- only touch these]

## Approved Patterns
[Exact values to use]

## Forbidden Patterns
[Exact values to remove/replace]

## Rules
- [Constraints]
- Before replacing, check if the approved pattern is already present. Skip if already correct.
- If you find issues affecting files outside your ownership, add to "Flags for Commander" -- do NOT fix them.

## Process
1. Read each file completely before making changes.
2. Check if any approved patterns are already in place (idempotency).
3. Apply all approved patterns, replacing all forbidden patterns.
4. Do NOT touch code outside your forbidden/approved scope.
5. After editing, re-read each file to verify no forbidden patterns remain.
6. Return your report in this exact format:

## Report: [Your Name]
### Files Modified
- [file]: N replacements
### Files Skipped (already correct)
- [file]: reason
### Flags for Commander
- [issue, or "None"]
### Issues Encountered
- [issue, or "None"]
### Status: COMPLETE / PARTIAL / FAILED
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
- **Partial completion**: The verification step (Step 5) catches anything missed. The structured report format makes it clear which files were and weren't completed.
- **Build failure after completion**: Compare against the checkpoint branch to determine if the failure is new. If new, diagnose from the agent reports and fix directly.
- **Idempotency on re-run**: Agents check for already-applied patterns before making changes, so running the army twice won't double-apply.

## Example Invocation

User: "Replace all neon Tailwind colors with our sand palette across the site"

**Wave 1 (Execute):** Commander creates a git checkpoint, runs recon, finds 45 files across 5 domains plus 2 shared dependencies. Composes an army: 1 Foundation Agent (runs first on shared files), then 5 team members with 2-4 sub-agents each (22 agents total). All deploy in parallel. Structured reports come back: 43 files modified, 2 skipped (already correct), 3 cross-team flags.

**Wave Assessment:** Build passes, but 3 cross-team flags exist and 2 remaining violations found in files that were edge cases. Commander recommends Audit wave.

**Wave 2 (Audit):** Smaller army -- 3 agents targeting the flagged files and violations. Fresh context, fresh eyes. Fixes the remaining issues. Build passes clean.

**Wave Assessment:** Zero violations, zero flags, build passes. Propagate wave recommended because 4 test files import from modified components.

**Wave 3 (Propagate):** 3 agents update test files and one doc file that referenced old color tokens. Build still passes.

**Final Report:** 3 waves, 28 total agents across all waves, 48 files touched, zero violations remaining, clean build. Rollback branch available if needed.
