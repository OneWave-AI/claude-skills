---
name: plan-in-files
description: Use for any task that spans more than a couple of steps, files, or sessions — refactors, migrations, multi-file features, anything that must survive a context reset or crash. Trigger when the user asks for a plan, says "keep track of this", "don't lose the thread", or when a task is large enough that forgetting step four is likely.
---

# Plan in Files

A plan that lives in the conversation dies with the conversation. A plan that lives in a file survives a crash, a `/clear`, a laptop reboot, and a different person picking the work up on Monday.

## Core Behavior

Before starting multi-step work, write the plan to disk. Update it as you go. The file is the source of truth about progress — not memory, not the chat.

Default location: `PLAN.md` at the repo root for one-off work, or `docs/plans/<yyyy-mm-dd>-<topic>.md` when the repo keeps plan history. Gitignore it or commit it — ask once, then follow the repo's convention.

## Plan Shape

```markdown
# <Task> — plan

**Goal:** <one sentence, in the user's words>
**Done when:** <the observable condition that ends this work>

## Constraints
- <the things that must stay true: no API break, no new deps, ships today>

## Steps
- [ ] 1. <action> — `path/to/file`
- [ ] 2. <action> — `path/to/file`
- [ ] 3. <action> — verify with `<command>`

## Notes
<discoveries, gotchas, things that turned out to be false>

## Log
- <date/time> — <what happened>
```

Each step is one action on a named file or a named command. "Refactor the auth layer" is not a step; "move `verifyToken` out of `api/auth.ts` into `lib/token.ts` and update the three imports" is.

## Working the Plan

1. Write it. Show it to the user before executing when the work is large or destructive.
2. Do one step.
3. Tick the box in the file, immediately. Not at the end — a crash between step three and the end loses everything.
4. When reality disagrees with the plan, edit the plan. A plan you silently abandoned is worse than no plan.
5. Append surprises to Notes as you hit them. That is where the next session's time savings live.

## Rules

- Never tick a box for work you have not verified. "Edited the file" is not "step done" if the step said the tests pass.
- Never fake progress to make the plan look finished. An honest half-done plan is useful; a dishonest complete one is a trap.
- Keep the plan under a page. A plan longer than the work is a symptom of avoiding the work.
- If a step turns out to be five steps, split it in the file before continuing.
- When work finishes, write one closing line in the Log and leave the file. It becomes the record of why the code looks the way it does.

## Resuming

When picking up an existing plan file:

1. Read it.
2. Verify the ticked steps against reality — `git log`, `git diff`, run the tests. Ticked does not always mean true.
3. Correct the file if it lied.
4. Start at the first genuinely unfinished step.

## When Not to Use This

A single-file edit, a one-line fix, a question. Writing a plan file for a two-minute change is ceremony, and ceremony is the thing this library is against. The test: if losing the session would cost more than five minutes of rework, write the file.
