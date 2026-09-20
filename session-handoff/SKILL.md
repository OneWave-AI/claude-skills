---
name: session-handoff
description: Use when a working session is ending, the context window is nearly full, work needs to pass to a teammate or a fresh session, or the user says "hand this off", "write this up before we lose it", "I'm starting a new session", or "summarize where we are". Produces a handoff document that lets the next session resume without re-reading the transcript.
---

# Session Handoff

A session ends three ways: the context fills up, the person leaves, or the work moves to someone else. All three lose the same thing — the reasoning that never made it into a file. This skill writes that reasoning down before it evaporates.

## Core Behavior

Write a handoff file, do not summarize in chat. Chat scrolls away; a file survives a `/clear`, a crash, and a different person opening the repo tomorrow.

Default path: `HANDOFF.md` at the repo root, or `docs/handoff/<yyyy-mm-dd>-<topic>.md` if the repo already has a docs convention. If a handoff file exists, append a new dated section rather than overwriting — the history of what was tried is half the value.

## What Goes In It

Write these sections in this order. Skip a section only when it is genuinely empty.

**Goal.** One sentence: what this work is supposed to achieve, in the user's terms, not the ticket's.

**State.** What is done, what is half-done, what has not been started. Be specific about half-done — "auth works, but the refresh-token path is stubbed and returns a fixed string" beats "auth in progress".

**Files touched.** Path plus one line on what changed and why. Include files you read and decided not to change when the decision was non-obvious.

**Decisions and why.** The choices a reasonable person would question. Each one: what was chosen, what was rejected, and the reason. This is the section that saves the next session an hour.

**Dead ends.** What was tried and did not work. Name the failure mode. Without this, the next session repeats it.

**Next step.** The single next action, concrete enough to start on immediately. Not "continue the refactor" — "extract `parseInvoice` from `billing.ts:210` into its own module, then point the three callers at it".

**Open questions.** Anything waiting on a human. Name who, and what the question is.

## How to Gather It

Prefer evidence over memory:

- `git status` and `git diff --stat` for what actually changed on disk.
- `git log --oneline -15` for what landed.
- Test/build output from the last run, if there was one.
- The user's own words for the goal — quote them rather than paraphrasing into corporate language.

If the transcript disagrees with the repo, the repo wins. Say so in the handoff.

## Rules

- No status-report padding. No "we made great progress". A handoff is field notes, not a stakeholder update.
- Include the commands to get back to a working state: the dev-server command, the test command, any env var that has to be set.
- Never claim something works that you did not see work. Write "untested" next to it.
- If work is on a branch, name the branch and the base it forked from.
- Uncommitted changes: say so explicitly at the top, and list them. That is the most common way work gets lost.

## Output Format

```markdown
# Handoff — <topic> — <date>

**Goal:** <one sentence>

**Branch:** <name> (base: <name>) · **Uncommitted:** <yes, list / no>

## State
- Done: ...
- In progress: ...
- Not started: ...

## Files
- `path/to/file.ts` — <what and why>

## Decisions
- <chose X over Y because Z>

## Dead ends
- <tried X, failed with Y — don't repeat>

## Next step
<one concrete action>

## Open questions
- <question> — needs <person>

## Getting back to work
```bash
<commands>
```
```

## When the Context Window Is the Reason

If the handoff is being written because context is nearly full, write the file first, before any other work. Then tell the user to start a fresh session and open the file. Do not try to squeeze in one more fix — a truncated handoff is worse than an early one.
