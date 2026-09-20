---
name: context-budget
description: Use when a coding session is burning context fast, output is drowning in noise, the model keeps forgetting earlier decisions, or the user asks to reduce tokens, stop the verbose narration, work in a huge repo, or make a long session survive. Covers what to read, what to summarize, what to write to disk, and when to start fresh.
---

# Context Budget

Context is the scarcest resource in a long session. It gets spent on three things: files you read, output you generate, and narration nobody asked for. Only the first one is usually worth it.

## Core Behavior

Treat the context window like a budget with a balance. Before any expensive action — reading a big file, running a chatty command, dumping a directory tree — ask what the cheapest way to get the same answer is.

## Spend Rules

**Read narrowly.** `sed -n '120,190p' file.ts` beats reading a 2,000-line file to see one function. Grep for the symbol, then read the 40 lines around it. Read a whole file only when you are about to restructure it.

**Search before reading.** `grep -rn "symbolName" --include="*.ts"` costs a few hundred tokens and tells you which of forty files matters.

**Silence the noisy commands.** Pipe installs, builds, and test runs through a filter instead of dumping them whole:

```bash
npm test 2>&1 | tail -30
npm run build 2>&1 | grep -E "error|Error|warning" | head -20
npm install --silent 2>&1 | tail -5
git diff --stat            # not git diff, unless you need the hunks
```

A passing test suite needs one line of proof, not 400.

**Write instead of remembering.** Anything that must survive — a plan, a decision, a list of files to touch — goes in a file on disk. Files are re-readable at a cost you choose; context is not.

**Do not re-read what you just wrote.** If an edit succeeded, it succeeded. Re-reading to "verify" is pure spend.

**Cut the narration.** No preamble, no recap of what was just shown, no bulleted summary of a diff the user can see. Say what changed and what is next, in a line or two.

## Where the Budget Actually Goes

When a session bloats, it is almost always one of these:

| Leak | Fix |
|------|-----|
| Whole-file reads for one function | grep, then a line-ranged read |
| Full `npm install` / build logs | `\| tail -n` or grep for errors |
| Directory listings of `node_modules`, `dist`, `.next` | prune them in the find/ls |
| Re-reading files after editing | trust the edit result |
| Long explanations of finished work | one line |
| Pasting a file back to show a small change | show the diff hunk only |
| Repeating the plan every turn | plan lives in a file |

## Compaction Points

When roughly two-thirds of the window is gone, stop adding and start consolidating:

1. Write the current state to a plan or handoff file on disk.
2. State the single next action.
3. Tell the user a fresh session will be faster and more accurate than continuing.

A fresh session that reads a good plan file outperforms a stuffed session every time. Do not treat starting over as failure — it is the intended move.

## Large Repos

- Map before you dig: directory names and entry points first, implementation later.
- Follow imports from the entry point rather than crawling folders alphabetically.
- One subsystem at a time. Finish it, write down what you learned, move on.
- Generated code, lockfiles, and snapshots are never worth reading. Exclude them by default.

## What Not to Cut

Economy has a floor. Never skip:

- Reading the actual code before changing it.
- The error output when something failed — that is the one long dump worth having.
- The user's own requirements, quoted.

Being cheap about the wrong thing produces confident, wrong work. The goal is fewer tokens, not less evidence.
