---
name: grill-the-brief
description: Use before building anything from a vague request — a feature, an app, an agent, an automation, a page. Trigger when the user says "build me X" without specifics, when a brief could be read two ways, or when the user asks to be challenged, interrogated, or pushed on requirements before code gets written.
---

# Grill the Brief

Most rework comes from building the wrong thing confidently. This skill spends five minutes interrogating the request so the build hits the first time.

## Core Behavior

Ask questions before writing code — but only the questions whose answers change what gets built. A question whose every answer leads to the same implementation is a waste of the user's time; make that call yourself and say what you assumed.

Ask in one batch, not one at a time. Three to six questions, numbered, each with a default you will use if the user shrugs.

## What to Interrogate

Work down this list and pull only what is genuinely unresolved:

**The actual job.** What does the user do today that this replaces? If they cannot describe the current manual version, the spec is a wish, not a requirement.

**Who touches it.** One person, a team, or customers? That single answer decides auth, permissions, and polish level.

**Done looks like.** The observable condition that ends the work. If nobody can name it, the project has no end.

**Scale and shape of the data.** Ten rows or ten million. One file or a live feed. This decides architecture more than any preference does.

**What it must not do.** The constraints that are invisible until violated: cannot break the existing API, cannot add a dependency, cannot cost money per call, has to work offline.

**The deadline and the stakes.** A demo tomorrow and a production system get different code. Ask which one this is.

**What exists already.** Existing repo, existing schema, existing design system. Building beside something is different from building fresh.

## Questioning Rules

- Never ask what you can read. Check the repo, the files, the git history first — asking the user something the code answers is a tell that you did not look.
- Attach a default to every question: "Which auth? (default: Google SSO, since the repo already has it)". The user can answer with silence and still get moving.
- Push back once, concretely, when the brief has a real problem — then build what they asked if they confirm. One flag, not a debate.
- Stop at six questions. Beyond that you are stalling.
- No question that only serves your comfort. "What framework do you prefer?" is a decision you can make.

## Output Format

```
Before I build — <n> things that change the shape of this:

1. <question> (default: <what I'll assume>)
2. <question> (default: <what I'll assume>)
3. <question> (default: <what I'll assume>)

Say "go" and I'll build with the defaults.
```

Then, once answered, restate the brief in one paragraph — scope, constraints, done-condition — and start.

## Red Flags to Name Out Loud

Call these out when you see them, in a sentence each:

- The request names a solution but never the problem.
- "Just like <big product>" with no cut-down of scope.
- Success measured by something nobody tracks today.
- Two incompatible goals in one brief (fast and configurable, simple and enterprise-ready).
- A build where an existing tool already does the job — say so once, then build it anyway if they still want it.

## When to Skip This

Clear, small, or reversible work. A bug fix, a copy change, a one-file tweak. Grilling a two-minute request wastes the time it is supposed to save.
