# Retrieve any Ledger Record

Use `yy ledger` from the canonical controller, or `yylo-ledger` standalone.
Preflight `yy ledger --version`, `yy ledger --help`, and `yy ledger get --help`.
Installed help is authoritative; source merge or skill installation does not
activate a new Ledger runtime. Universal flat get advertises all Record kinds
and `--content`. If installed get is task-only, use the existing native
`yy ledger record get RECORD_ID -f json` after checking its help. If neither
universal API is available, stop and request an upgrade. Never guess types by
repeatedly trying task/wiki/pdr/workflow/artifact get, or read store files directly.

## Known ID: one command

```bash
yy ledger get RECORD_ID -f json
```

`show` is an alias. This resolves exact hot and archived identities in the selected
project. Cross-project routing requires an explicitly allowed `--project ALIAS`;
never hunt across projects after a miss. Prefer immutable IDs for repeat reads;
slugs and retained aliases are discovery conveniences and may be ambiguous.

```text
Have an ID?
  |
  +-- yes --> get ID --> prefix-selected store OR legacy resolver
  |                              |
  |                       hot/archive exact lookup
  |                              |
  |                       record + bounded content
  |
  +-- no ---> bounded record search --> select actual returned ID --> get ID
```

New automatically generated IDs use storage-kind prefixes only:

| Prefix | Storage kind | Examples of purpose/profile |
| --- | --- | --- |
| `task_` | task | requested work, dependencies, status |
| `doc_` | document | wiki, workflow, historical document/pdr |
| `artifact_` | artifact | report, receipt, stdout, model-output |

The prefix is immutable storage kind, not mutable purpose. There is no `pdr_`,
`wiki_`, `workflow_`, or `benchmark_` identity category. Existing IDs remain
unchanged and readable; never prepend a prefix to a historical ID or derive an
ID from a title. Prefixes route exact reads to one store; they do not remove
archive integrity checks. Exact Document/Artifact reads need no global search
index rebuild; slug/alias discovery can be more expensive.

## Unknown ID: bounded discovery

```bash
yy ledger record search --text "requirements" --projection summary --limit 20 -f json
yy ledger record search --kind artifact --profile report --projection summary --limit 20 -f json
# Cold discovery is explicit; ordinary searches are hot-only.
yy ledger record search --scope archive --text "requirements" --projection metadata --limit 20 -f json
```

`record search` spans kinds; flat `search/list/ready/order` remain task surfaces.
Use `--scope all` only when both tiers are needed. Do not list every payload to
find one ID, rebuild a cache, or retry every kind after an exact lookup error.

## Record metadata is not necessarily payload bytes

Universal flat get returns non-task metadata with kind, profile, revision and a
`content` result. Readable UTF-8 local/inline content is included up to **64 KiB**
by default. Larger, binary, non-UTF-8, and external/link payloads have an explicit
omission reason; omission is not an empty document or missing Record. Existing
flat task output, related/dependency enrichment and `--compact` remain compatible;
use native `record get` when a full native task envelope is needed.

For one local/inline payload, request exact bytes deliberately with a bound:

```bash
# Choose a fresh external destination; check exit status before trusting output.
yy ledger get RECORD_ID --content --max-content-bytes 1048576 > /external/new-report.md
```

`--content` emits exact bytes (including binaries), not JSON. The default bound is
65536 bytes; the maximum accepted bound is **16 MiB** (16777216). A refused read
must not be mistaken for an empty successful capture. Artifact bytes are checked
against manifest digest/size; compare the readback with the intended evidence.
Ledger never downloads external/link payloads through get. A URI needs a separately
authorized client; links do not guarantee immutable bytes. Native/typed `get`
retains its existing metadata/source contract: do not infer a byte round-trip from
metadata/history alone. `--raw` is not a universal artifact-byte retrieval flag.

## PDRs and specialized operations

New operational PDRs remain **artifact/report** Records, normally local immutable
Markdown. Historical **document/pdr** Records remain readable. Given either ID,
use the same universal get; do not move or reclassify existing PDRs to simplify
retrieval. Reports and benchmark evidence likewise need no new identity prefix.

Typed commands remain appropriate for creation/mutation, history, revision-pinned
retrieval and specialized rendering: `wiki get ID --raw`,
`workflow get ID --validated`, and `artifact history ID`, subject to installed help.
Reading a workflow is not permission to execute it. A prefix is routing information,
not mutation, retention, publication or release authority.

## Refusals

Keep the original diagnostic. Invalid/unknown prefixes, missing Records,
ambiguous identities, mismatched kinds, unavailable payloads, byte-limit refusal,
and integrity failures are different outcomes. A missing ID means no match in the
selected project, not proof of global absence. Resolve ambiguity with a canonical
ID; choose an explicit adequate content bound for large local payloads; stop on
corruption. Do not silently substitute another revision, type or project.
