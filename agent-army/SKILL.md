---
name: agent-army
description: 2-layer parallel agent hierarchy. Layer 1: 3-50+ agents, each with independent context. Layer 2: 2+ sub-agents per member, each with own context seeded by parent brief. No upper limit on either layer.
user_invocable: true
---

# Agent Army

## Architecture

```
Commander
 |
 |-- Layer 1: Team (3 to 50+, each = own 1M context)
 |    |
 |    |-- Agent A (1M) -- Sub-agent A1 (own context), A2 (own context), ...
 |    |-- Agent B (1M) -- Sub-agent B1 (own context), B2 (own context), ...
 |    |-- Agent C (1M) -- Sub-agent C1 (own context), C2 (own context), ...
 |    |-- ... (no cap)
```

## Layer 1 Prompt Template

This is what spawned agents actually see. It is the most important section in this skill.

```
You are [AGENT_NAME], specialist on [DOMAIN].

Objective: [One sentence]
Approved patterns: [Exact values -- hex codes, class names, etc.]
Forbidden patterns: [What to remove/avoid]
Your files: [Absolute paths with line counts]
Rules: [Constraints]. Skip files already using approved patterns. Flag issues outside your files in "Flags for Commander" -- do NOT fix them.

CRITICAL: You MUST use the Agent tool to spawn the sub-agents listed below. Do NOT do the work yourself. Do NOT skip spawning. Deploy ALL sub-agents in a single message with multiple Agent tool calls.

Sub-agents:
- "[NAME]": [files with line counts]
- "[NAME]": [files with line counts]

Pass each sub-agent: objective, their files, approved/forbidden patterns, rules, report format. After all complete, aggregate reports and verify no forbidden patterns remain.
```

## Layer 2 Prompt Template

```
You are [SUB_AGENT_NAME], working under [TEAM_MEMBER_NAME].

Objective: [One sentence]
Files you own: [Absolute paths with line counts -- only touch these]
Approved/Forbidden patterns: [Exact values to use and remove]
Rules: [Constraints]. Skip files already correct. Flag issues outside your files -- do NOT fix them.

Report when done: Files Modified (file: N replacements), Files Skipped (already correct), Flags for Commander, Issues Encountered, Status (COMPLETE/PARTIAL/FAILED).
```

<mandatory-rules>
## MANDATORY RULES

1. EVERY Layer 1 agent MUST spawn 2+ sub-agents. No exceptions. If deploying without sub-agents, STOP and restructure.
2. NEVER silently reduce army size. Match the user's chosen tier.
3. Report as agents complete: `[Agent N/M complete] name: X files modified, Y flags`
4. Show the army plan before deploying (Full Mode). Quick Mode: compose plan internally, skip confirmation.
5. Sub-agent deployment instructions go INSIDE the Layer 1 brief. If missing, sub-agents will not exist.
6. Build check after every wave. If it fails, trigger a fix wave.
7. "Keep going" / "don't stop" = continuous mode. Launch new agents as each completes. Do not wait. Do not ask.
</mandatory-rules>

## Army Size

Confirm tier before starting. Present this table:

```
| Tier | Agents | Total with Sub-agents | Est. Tokens |
|------|--------|----------------------|-------------|
| Conservative | 3 | ~9 | ~200-500K |
| Standard | 5-10 | ~15-30 | ~500K-1.5M |
| Aggressive | 10-20 | ~30-60 | ~1.5-4M |
| Maximum | 20-50+ | ~60-100+ | ~4M+ |
| Custom | You pick | You pick | Varies |

Token estimates vary by task complexity. Pick a tier or enter a custom number:
```

Default to Standard if user says "just do it." Tier question applies to BOTH Quick and Full modes.

After recon (Step 3), recommend a specific number based on what you found. Example: "Found 35 files across 6 domains. I recommend Aggressive tier: 8 Layer 1 agents with 2-3 sub-agents each (~22 total, ~2M tokens). Want to adjust?"

## Deployment Gate

Output this checklist in your response before deploying. Do NOT skip it. Do NOT just check it mentally.

```
DEPLOYMENT GATE:
[ ] Every L1 brief contains "You MUST spawn N sub-agents"
[ ] Every sub-agent named with specific files assigned
[ ] Every file owned by exactly one sub-agent
[ ] L1 briefs include full sub-agent deployment instructions
[ ] Tier matches user's selection
```

All must PASS. If any FAIL: fix the plan first.

## Protocol

**Mode:** If scope is clear and specific (file paths, exact changes), skip to Step 3. Otherwise start at Step 1.

### Step 1: Intake (Full Mode)

Confirm with user:
1. Goal (one sentence)
2. Scope (files, directories, or "everything")
3. Constraints (don't touch X, match Y style)
4. Tier (show table above)

If user already provided context, confirm in one line: "Goal: [X]. Scope: [Y]. Tier: [Z]. Starting."

### Step 2: Git Checkpoint

1. Run `git status`. Warn if uncommitted changes.
2. Create checkpoint: `git checkout -b agent-army/checkpoint-{timestamp}`, switch back.
3. No git repo? Warn user and get confirmation.

### Step 3: Recon

1. Scan -- Grep, Glob, Read to find all affected files
2. Count units of work
3. `wc -l` each file. Flag 500+ line files as heavy (assign solo)
4. Classify into domains (by directory, imports, file type, naming pattern)
5. Identify shared dependencies (foundation files -- handle first)
6. Identify build command (check package.json, Makefile, etc.)

Output scope report:
```
Files: N | Heavy: [list] | Domains: [list] | Shared deps: [list] | Build cmd: [cmd]
```

### Step 4: Compose

1. Foundation Agent for shared deps (runs first, before parallel wave)
2. Layer 1: 1 agent per domain. Split large domains across multiple agents.
3. Layer 2: 2+ sub-agents per L1 agent based on file weight
4. Name every agent. Assign every file to exactly one sub-agent.

Output army plan. Full Mode: pause for "Proceed?" Quick Mode: show one-line summary, deploy.

### Step 5: Deploy

1. Foundation Agent first (if needed). Wait for completion.
2. Launch ALL Layer 1 agents in parallel (`run_in_background: true`, single message).
3. L1 agents spawn L2 sub-agents in parallel (per their brief).
4. Report each completion: `[Agent N/M complete] name: results`

### Step 6: Verify

1. Re-scan for remaining violations (same searches as Step 3)
2. Run build command
3. Resolve cross-team flags
4. Output army report:
```
Agents: N total | Files modified: N | Skipped: N | Build: PASS/FAIL | Flags: [list] | Rollback: git checkout agent-army/checkpoint-{timestamp}
```

## Waves

After Wave 1: build + re-scan. If clean, done. If issues remain, deploy Wave 2 (fix wave). If still issues, Wave 3 (propagate to tests/docs). Max 3 waves. Pause for user approval before each.

### Shared Scratchpad (optional)

For complex multi-wave tasks, write `.army-state.md` after Wave 1: files modified, flags, issues, decisions. Wave 2 agents read it directly for full context. Skip for single-wave tasks.

## Report Format

Every agent returns:
```
## Report: [Name]
Files Modified: [file: N replacements]
Files Skipped: [file: reason]
Flags for Commander: [issue or "None"]
Issues: [issue or "None"]
Status: COMPLETE / PARTIAL / FAILED
```

## Error Handling

- Sub-agent fails: L1 agent retries or spawns replacement
- L1 agent fails: Commander spawns replacement with same brief
- Build failure: compare against checkpoint, diagnose, fix wave
