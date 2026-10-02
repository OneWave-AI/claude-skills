# Agent Army

Deploy a 2-layer army of Claude agents on large, parallelizable work: big refactors, multi-file migrations, codebase-wide audits, and bulk generation.

The session model acts as Commander. It scouts the codebase, plans the army, briefs each Layer 1 agent, and verifies the result. Every Layer 1 agent gets its own full context window and spawns at least two Layer 2 sub-agents. Many independent agents run at once, instead of one context window split between them.

```
Commander (the session model)
 |-- Layer 1: 3 to 50+ specialist agents, each with its own context
 |    |-- Agent A -- sub-agents A1, A2, ...
 |    |-- Agent B -- sub-agents B1, B2, ...
```

## What it does

- **You pick the size.** Conservative (3 agents), up to 50+ for codebase-wide jobs, with a token estimate for each tier before anything runs.
- **You pick the power level.** Max Power, Heavy, Balanced or Economy set the Opus, Sonnet and Haiku mix per layer. Every agent call names its model explicitly, so you are never billed for a tier you did not choose.
- **Git safety.** A checkpoint before deploying, and a pre-deploy gate that shows the full plan.
- **Proof, not claims.** After each wave it runs the build and a phantom-completion check, because an agent reporting "done" is a claim until the diff says so.
- **Multi-wave follow-up.** Gaps found in verification become the next wave.

## When to use it

Use it for any task with six or more independent units of work: a color or API migration across dozens of files, a security or accessibility audit of a whole codebase, or bulk content generation.

Skip it for fewer than six units, for tightly sequential work, or for a single file. The skill says so itself and offers to do the work inline.

## Install

In Claude Code:

```
/plugin marketplace add OneWave-AI/claude-skills
/plugin install agent-army@onewave-skills
```

Then ask for it by name: "use agent army to migrate every component to the new tokens."

## Privacy and data

Agent Army is instructions only. It ships no code, makes no network requests of its own, and stores nothing. The agents it deploys run with the permissions of your Claude Code session and use your plan's usage. Larger armies use proportionally more tokens. The size table shows an estimate before you confirm.

## Support

- Questions or problems: [onewave-ai.com/contact](https://www.onewave-ai.com/contact)
- Bugs: [GitHub issues](https://github.com/OneWave-AI/claude-skills/issues)

Built by [OneWave AI](https://www.onewave-ai.com), an Anthropic Partner Network firm. MIT licensed.
