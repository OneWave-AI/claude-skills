---
name: runbook-generator
description: Generates comprehensive operational runbooks for any system or process. Reads codebase, infrastructure config, and deployment scripts to produce structured runbook.md files formatted for on-call engineers. Use when you need operations documentation, incident response guides, deployment procedures, or disaster recovery plans.
tools: Read, Glob, Grep, Bash, Write, Edit
model: inherit
---

# Runbook Generator

Generate a comprehensive operational `runbook.md` from a system's codebase, infrastructure config, and deployment scripts -- written for on-call engineers working incidents, deployments, and routine operations at 3am.

## Contents
- `references/discovery-patterns.md` -- Glob/Grep patterns and config files to inspect during discovery.
- `references/output-template.md` -- The full 9-section runbook.md structure to populate.
- `references/writing-style.md` -- Clarity, urgency, completeness, formatting, and accuracy rules plus output requirements.

## Workflow

1. Discover the system. Run the Glob patterns in `references/discovery-patterns.md` (Step 1) to identify the stack and infrastructure.
2. Read key configuration. Open and analyze the config files listed in `references/discovery-patterns.md` (Step 2): IaC, containers, CI/CD, app config, deploy scripts, monitoring, migrations, load balancers, docs.
3. Identify operational behavior. Run the Grep patterns in `references/discovery-patterns.md` (Step 3) to surface health checks, metrics, caching, jobs, migrations, rollback, scaling, backups, TLS, secrets, alerting, and more.
4. Generate the runbook. Produce `runbook.md` following the structure in `references/output-template.md`. Cover all 9 sections; adapt content to what discovery found; never include purely speculative sections.
5. Apply writing standards. Follow every rule in `references/writing-style.md` -- copy-pasteable commands, expected outputs, sequential steps, P1-first ordering, tables for structured data, and the accuracy rules.
6. Verify and flag gaps. Confirm referenced paths and scripts exist. Mark unverifiable details with `[VERIFY]` and missing sections with `[ACTION REQUIRED]: ...` so the runbook doubles as a gap analysis.

## Output

Write `runbook.md` to the project root (or a directory the user specifies). It must be 500+ lines, cover all 9 sections, contain real commands derived from the codebase, include at least one architecture diagram, carry a complete table of contents, and never fabricate infrastructure details. See `references/writing-style.md` for the full output checklist.
