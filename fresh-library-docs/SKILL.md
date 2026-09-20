---
name: fresh-library-docs
description: Use before writing code against a library, SDK, API, or framework whose current version you are not certain of — especially fast-moving ones. Trigger when an import fails, a method does not exist, a config key is rejected, a deprecation warning appears, or the user says the code was written against an old version.
tools: Read, Glob, Grep, Bash, WebFetch, WebSearch
---

# Fresh Library Docs

Training data has a cutoff; libraries do not. Most "the AI hallucinated an API" bugs are really the model writing correct code for a version that shipped two years ago. This skill checks reality first.

## Core Behavior

Before writing non-trivial code against a dependency, establish two facts: which version this project actually has, and what that version's API looks like. In that order.

## Step 1 — What Is Installed

The installed version beats the latest version and beats your memory. Read it from the project:

```bash
cat package.json | grep -A30 '"dependencies"'
npm ls <pkg> --depth=0 2>/dev/null
pip show <pkg> 2>/dev/null | head -3
cat requirements.txt pyproject.toml 2>/dev/null | grep -i <pkg>
```

## Step 2 — Read the Real Source

The most reliable documentation is the code on disk. It cannot be out of date, because it is what will run.

```bash
ls node_modules/<pkg>/dist/*.d.ts
grep -rn "export function <name>\|export declare" node_modules/<pkg>/dist/index.d.ts | head -20
python -c "import <pkg>, inspect; print(inspect.signature(<pkg>.<fn>))"
```

For a TypeScript project, the `.d.ts` file answers the question definitively. Read it before searching the web.

## Step 3 — Then the Docs

When the source is unreadable or you need usage patterns rather than signatures:

- Official docs for that exact version, not the "latest" URL, which silently redirects.
- The repo's CHANGELOG or migration guide — the fastest way to learn what moved between your mental model and reality.
- GitHub issues for the specific error string, when behavior contradicts the docs.

Blog posts and forum answers are the last resort and always carry a date. A 2023 tutorial for a library that had a major release last year is a trap.

## Step 4 — Confirm Before Committing

For anything non-obvious, run the smallest possible check rather than trusting the read:

```bash
node -e "const x=require('<pkg>'); console.log(Object.keys(x).slice(0,30))"
npx tsc --noEmit 2>&1 | head -20
```

Type-check output is the cheapest proof that an API call exists.

## Rules

- Never call a method you have not seen defined somewhere real.
- Pin what you learn into the code as a comment only when the behavior is genuinely surprising — not as a version diary.
- When installed and latest differ significantly, say so in one line and let the user decide whether to upgrade. Do not upgrade a dependency to make your snippet work.
- If the answer is genuinely uncertain, say which part is uncertain instead of writing confident code around it.

## Highest-Risk Dependencies

Verify these every time; they move fastest and break most: AI SDKs and model identifiers, auth libraries, ORMs and database clients, build tooling and bundler config, meta-framework routing and data-fetching conventions, payment SDKs. For model names, pricing, and parameters specifically, check the provider's current model list rather than recalling one.
