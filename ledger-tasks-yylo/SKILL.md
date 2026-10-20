---
name: ledger-tasks-yylo
description: Retrieve any YYLO Ledger Record by ID, discover PDRs and artifacts, and manage tasks and dependencies. Use for unknown record types, universal get/search, task operations, and source-of-truth boundaries.
argument-hint: "[command or workflow question]"
enable-shell-directives: true
---

## YYLO Ledger CLI Reference

Use `yy ledger` from the controller, or `yylo-ledger` standalone. Ledger exposes compatible flat task commands and native ID-first `record|task|wiki|pdr|workflow|artifact` groups, subject to installed help. `yy kanban` is a labelled compatibility alias for the same controller-routed runtime.

### Retrieve any Record first

Preflight `yy ledger get --help`. When it advertises universal retrieval, use
`yy ledger get RECORD_ID -f json` for tasks, documents, PDRs and artifacts without
knowing the type. If installed get is task-only, use
`yy ledger record get RECORD_ID -f json` after checking native help; if absent,
stop for an upgrade. Do not try each type until one works.

New generated IDs use `task_`, `doc_`, or `artifact_` for storage kind only;
existing IDs remain unchanged. New PDRs are artifact/report, while historical
document/pdr Records remain readable through the same command. Exact reads
include hot and archived Records in the selected project. When no ID is known,
start with `yy ledger record search --projection summary --limit 20 -f json`;
use explicit `--scope archive|all` for cold discovery.

Read [references/retrieval.md](references/retrieval.md) for bounded content,
`--content` byte retrieval, PDR examples, compatibility and refusal handling.
Small readable non-task payloads are included by default; Record metadata alone
is not proof that payload bytes were retrieved. Typed commands remain for
mutation and specialized rendering/validation.

### Supported task contract

- Preflight installed `yy ledger --version` and `yy ledger --help`; command help is authoritative for the selected runtime.
- Use universal get for reads, flat task commands for task bookkeeping, and the controller's `yy task` lifecycle for managed delivery. Use dedicated wiki, workflow, and artifact skills for typed mutations rather than guessing arguments.
- New operational PDRs, contracts, plans, reports, receipts, and evidence belong in typed Artifact Records, not product documentation, task bodies/responses, or new `.juno_task/specs` files.
- If a required native group is absent, fail closed and request a Ledger upgrade. Never invoke mutable source directly or write Ledger store files by hand.
- Read current task state before mutation, preserve mutation receipts where offered, and never bypass controller routing or lifecycle state with direct file edits.
- Normal discovery is hot-only unless an explicit cold-archive command is used.

### Opt-in cross-project routing

Cross-project access is disabled by default. The source `.juno_task/config.json` must set `kanbanRegistry.enabled: true` and explicitly list `allowedProjects`; environment overrides are `YYLO_LEDGER_REGISTRY_ENABLED` and `YYLO_LEDGER_REGISTRY_ALLOWED_PROJECTS`. Register with `yy ledger project add ALIAS --path /absolute/project`, then route any command with `--project ALIAS`. The destination wrapper/runtime remains authoritative, and routing failures never fall back to the source board.

### Legacy Task compatibility commands

**CREATE** — Add a new task
```bash
yy ledger create "Task description here" --status backlog --tags feature,backend
```
Options: `--status` (backlog|todo|in_progress|done), `--tags` (comma/space-separated), `--blocked-by` (task IDs), `--related-tasks` (task IDs)

**LIST** — Browse tasks with summary stats
```bash
yy ledger list --limit 5 --sort asc
yy ledger list --status todo --sort asc
yy ledger list --status todo,in_progress --limit 10
```

**SEARCH** — Find tasks by criteria
```bash
yy ledger search --status todo --tag backend --limit 10
yy ledger search --body "OAuth" --open
yy ledger search --commit abc123
```
Filters: `--status`, `--tag`, `--body`, `--response`, `--commit`, `--open` (no agent_response), `--recent`, `--exclude` (exclude tags)

**GET** — Universal Record read; task details retain dependency and related-task compatibility
```bash
yy ledger get TASK_ID
```

**MARK** — Update status with required response message
```bash
yy ledger mark in_progress --id TASK_ID --response "Starting work on this"
yy ledger mark done --id TASK_ID --response "Completed: implemented X, tested Y" --commit abc123def
yy ledger mark todo --id TASK_ID --response "Reopening: found regression"
```
Required: `--id` and `--response`. Optional: `--commit` (recommended for done).

**UPDATE** — Modify task fields
```bash
yy ledger update TASK_ID --status todo --tags backend,urgent
yy ledger update TASK_ID --commit abc123def
yy ledger update TASK_ID --response "Additional context"
```

**ARCHIVE** — Soft delete (preserves data, sets status to archive)
```bash
yy ledger archive TASK_ID
```

### Immutable cold archive packs

Normal `list`, `search`, `ready`, and `order` are deliberately hot-only. Exact `get TASK_ID` transparently resolves a hot task or a read-only archived task; use `history TASK_ID` explicitly for its ledger. Discover cold tasks only with bounded, projected `archive-search` output:

```bash
yy ledger archive-search --tag backend --before 2026-01-01 --limit 20 --projection metadata
```

Before archive maintenance, preflight the installed version/help and obtain explicit owner authorization. The repository and index must be clean, and reports must be durable new paths outside the repository:

```bash
yy ledger --version
yy ledger archive-pack plan --status done,archive --older-than 90d --max-tasks 1000 --target-bytes 26214400 --hard-max-bytes 47185920 --report /external/receipts/archive-plan.json
# Independently inspect selected IDs, revisions, source HEAD, policy, and plan hash.
yy ledger archive-pack create --plan /external/receipts/archive-plan.json --report /external/receipts/archive-create.json
yy ledger archive-pack doctor
yy ledger doctor
```

A stale plan or selected-task/worktree conflict must fail closed: discard the plan, resolve the conflict, and plan again. Never automate archival, edit/append packs or manifests, restore/reopen an archived ID, use force/lossy controls, or enumerate archive files directly. Create follow-up work as a new hot task related to the archived ID. Production archival, push/deploy, and post-deploy E2E each require separate authorization; agents must not infer it from implementation approval.

### Dependency Management

**DEPS** — View, add, or remove task dependencies
```bash
# View dependency info (blockers, dependents, priority score)
yy ledger deps TASK_ID

# Add blockers (TASK_ID cannot start until BLOCKER1 and BLOCKER2 are done)
yy ledger deps add --id TASK_ID --blocked-by BLOCKER1 BLOCKER2

# Remove a blocker
yy ledger deps remove --id TASK_ID --blocked-by BLOCKER1
```
Cycle detection prevents circular dependencies automatically.

**READY** — Tasks with all blockers satisfied (safe to work on)
```bash
yy ledger ready
yy ledger ready --tag backend --limit 5
```
Returns tasks where status is backlog/todo/in_progress AND all `blocked_by` tasks are done/archive.

**ORDER** — Topological sort of open tasks respecting dependencies
```bash
yy ledger order
yy ledger order --scores
```
Use for determining safe parallel execution order.

### Body Markup for Inline Dependencies

Declare dependencies and relations directly in task body text:

```
[blocked_by]TASK_ID[/blocked_by]          — This task is blocked by TASK_ID
[blocked_by]ID1, ID2[/blocked_by]         — Blocked by multiple tasks
[task_id]RELATED_ID[/task_id]             — Reference a related task
[task_id]ID1 ID2[/task_id]                — Multiple related tasks
```

These are parsed automatically when the task is created/updated.

### Merge (Multi-Directory Consolidation)

When tasks get scattered across subdirectories:
```bash
# First produce and review a deterministic plan
yy ledger merge ./sub1/.juno_task ./sub2/.juno_task --into ./.juno_task \
  --dry-run --plan-file /external/ledger-merge-plan.json

# Apply only that reviewed plan and retain its receipt
yy ledger merge ./sub1/.juno_task ./sub2/.juno_task --into ./.juno_task \
  --apply-plan /external/ledger-merge-plan.json \
  --receipt-file /external/ledger-merge-receipt.json
```

### Output Formats

Legacy task formats: `-f json`, `-f ndjson`, `-f xml`, `-f table`.
`list/search/ready/order -f json` emits one object containing `tasks` and
`summary`, including empty results. Use `--raw` for compact JSON or `-f json -p`
for indented JSON. Without a format, output defaults to pretty JSON; `--raw`
makes it compact, while `--pretty` selects human-readable task rendering.
NDJSON emits one task per line and no summary record (zero bytes when empty).
For non-empty list/search/ready, NDJSON/XML/table summaries go to stderr;
order retains no stderr summary. Empty XML emits an empty `<tasks>` document.
`--raw` accepts JSON/NDJSON only and cannot be combined with `--pretty`.
Unsupported combinations fail before task enumeration. Style flags may appear
before or after these collection commands; the canonical wrapper preserves
this contract and keeps runtime diagnostics on stderr.
These source contracts require a matching Ledger release; skill source delivery
alone does not install or activate that runtime.

### Best Practices

1. **Task sizing**: Create tasks small enough to complete in one iteration without filling the context window
2. **Status flow**: backlog → todo → in_progress → done (or archive for abandoned tasks)
3. **Always include `--response`** when using `mark` — document what you did and how you tested it
4. **Attach commits**: Use `--commit HASH` when marking done, then `update TASK_ID --commit HASH` to link the git history
5. **Use `ready`** before starting work to find unblocked tasks
6. **Use `order --scores`** to plan parallel execution pipelines
7. **Use `[blocked_by]` markup** in task body when creating tasks that depend on others
8. **Use `[task_id]` markup** in task body to cross-reference related tasks
9. **Use `get TASK_ID`** to see full task details including resolved dependency and related task info
10. **Concurrent features are supported** — start each selected task with `yy task start TASK_ID`; each gets a dedicated product worktree, while `yy merge` serializes only target updates

### Canonical Controller Routing

YYLO Ledger mutation resolves the controller in this order: explicit `JUNO_TASK_ROOT`, repository-local registration, then the current project root. Diagnose before orchestration with `.juno_task/scripts/controller_resolver.py --cwd "$PWD" --operation kanban`. The resolver may bootstrap or idempotently confirm a registration, but changing an existing controller requires `yy migrate registration plan` followed by a separately authorized apply. Explicit/registered path or branch errors fail closed—YYLO Ledger never switches Git branches or falls back silently.

Run YYLO Ledger and workflows from the controller. A task checkout may implement/test but routes task/session writes to that controller. An integration-owner checkout stays clean and refuses Kanban/orchestration/session writes in strict mode; launch from the controller and pass the product checkout separately as `TASK_ROOT`.

### Environment Variables

- `JUNO_TASK_ROOT` — Explicit canonical controller/task-storage root (not the product `TASK_ROOT`)
- `JUNO_CONTROLLER_BRANCH` — Expected controller branch for environment-based routing
- `JUNO_WORKSPACE_ROLE` — `controller`, `task`, or `integration-owner`
- `JUNO_WORKSPACE_ENFORCEMENT` — `off`, `warn`, or `strict`
- `JUNO_DEBUG=true` — Show diagnostic messages
- `JUNO_VERBOSE=true` — Show informational messages
- `JUNO_KANBAN_LIST_BODY_TRUNCATE_CHARS=N` — Override list body truncation (default: 1200)

## User-facing Record results

After creation, update, discovery, or handoff, report the Record kind/profile,
actual immutable Record ID, and actual Ledger slug from the returned Record or a
native get readback. Never invent a slug from the title or confuse it with the ID.
If the selected API omits a field, say it is unavailable rather than fabricate it.
IDs remain authoritative for relations and lifecycle operations; slugs aid discovery.

$ARGUMENTS
