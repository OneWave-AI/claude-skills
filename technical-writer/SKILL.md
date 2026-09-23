---
name: technical-writer
description: Writes and restructures technical documentation - READMEs, tutorials, how-to guides, user guides, architecture docs, onboarding guides, runbooks and SOPs, troubleshooting guides, release notes, and knowledge base articles - grounded in the actual code or product, with commands and examples verified where possible. Use when the user asks to document a project, feature, system, or process, write or fix a README, explain a codebase to new developers, turn notes into a guide, or make existing docs clearer. For endpoint-by-endpoint API reference or OpenAPI specs, use api-documentation-writer; for CLAUDE.md or AGENTS.md files, use claude-md-writer.
---

# Technical Writer

Write documentation that lets a specific reader finish a specific task without asking anyone.

## Workflow

1. **Name the reader and the job.** One sentence: "[Reader] needs to [do what] and already knows [what]." A new contributor setting up the repo, an admin configuring SSO, and an executive evaluating the architecture need different documents. If the request does not say, infer from context and state the assumption at the top of your draft.

2. **Pick the document type.** Each type answers one question; mixing them is the most common reason docs feel unclear.

   | Reader wants to... | Type | Shape |
   |---|---|---|
   | learn by doing, first time | Tutorial | One guaranteed-to-work path, start to finish |
   | complete a known task | How-to guide | Goal, prerequisites, numbered steps, verify |
   | look something up | Reference | Tables and lists, complete and consistent |
   | understand why | Explanation / architecture | Context, design, trade-offs |
   | fix something broken | Troubleshooting | Symptom, cause, fix |

   A README is a front door: what it is, quickstart, links to the rest. Templates for every type are in [references/templates.md](references/templates.md).

3. **Gather facts from the source, not from memory.** In a codebase, read the entry points, `package.json` / `pyproject.toml` / `Makefile` scripts, config files, env var usage (`grep -r "process.env\|os.environ"`), and existing docs. Every command, flag, file path, env var, and default value in the doc must come from something you read or ran. When a fact cannot be verified, mark it `[VERIFY: ...]` rather than guessing.

4. **Draft with the template**, then apply [references/style-guide.md](references/style-guide.md). Lead with the most common task. Put prerequisites before step 1, not in the middle.

5. **Test the doc.** If you can run commands, walk the steps in order in a clean state and fix anything that fails or needs an unstated step. Otherwise, reread as the reader: is every step possible with only what the doc and prerequisites provide?

6. **Deliver** as the actual file (for example `README.md` or `docs/setup.md`), not wrapped in commentary. After it, list any `[VERIFY]` markers, assumptions about the reader, and what should trigger an update (a config format change, a new required env var).

## Worked example

Request: "Write setup docs for this repo for new devs."

- Reader and job: a developer who knows TypeScript but not this repo needs a running local environment and a passing test suite.
- Type: how-to guide (a known task), plus a short README section that links to it.
- Facts gathered: `package.json` scripts `dev`, `test`, `db:migrate`; `.env.example` lists `DATABASE_URL` and `STRIPE_SECRET_KEY`; `docker-compose.yml` runs Postgres 17; `engines.node` is `>=22`.
- Draft: Prerequisites (Node 22+, Docker) -> clone and install -> copy `.env.example` to `.env.local` and what each variable is for -> `docker compose up -d` -> `npm run db:migrate` -> `npm run dev` with the expected URL -> `npm test` with the expected output -> Troubleshooting for port 5432 already in use and a missing `DATABASE_URL`.
- Test: running the steps revealed a seed step (`npm run db:seed`) that the app needs; it was added as step 6.

## Failure modes

- **Invented details.** A plausible flag or env var that does not exist costs the reader more than a missing one. Verify or mark it.
- **Wall of prose where steps belong.** If the reader does things in order, number them. One action per step.
- **Missing expected results.** After each command that produces output, show what success looks like so the reader knows they are on track.
- **Mixing types.** A tutorial that stops to explain every design decision loses the learner. Link to the explanation instead.
- **Stale screenshots and versions.** Prefer text over screenshots for UI that changes. Pin versions only where the version matters, and say where the version comes from.
- **Documenting the happy path only.** Add the two or three failures a new reader is most likely to hit.
