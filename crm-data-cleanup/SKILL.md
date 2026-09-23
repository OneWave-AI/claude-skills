---
name: crm-data-cleanup
description: Cleans up CRM data from HubSpot, Salesforce, Pipedrive, Zoho, Close, Attio, or any CRM CSV export. Finds duplicate contacts and companies with fuzzy matching (not just exact email), normalizes emails, phones to E.164, names, domains, states, and countries, flags stale, invalid, role, and test records, finds broken contact-company associations, and produces a reviewable merge plan plus import-ready files without touching the live CRM. Use this skill whenever the user wants to dedupe, find or merge duplicate contacts, merge companies or accounts, clean up a CRM, prep a CRM migration or re-import, or says the CRM export is a mess. Also use it when they mention only one symptom, like "the same person is in here three times", "half our leads are junk", or "our company records don't match".
---

# CRM Data Cleanup

This skill turns a messy CRM export into a merge plan a human can check, plus files that
are ready to import. It works the same way for any vendor, because every CRM exports CSV.

Duplicate cleanup usually fails in one of three ways. Exact-email matching misses most
duplicates. Merging on shared inboxes like `info@` fuses different people into one. And a
merge overwrites good values with blanks, losing history that can't be recovered. Most
CRM merges **can't be undone**, so this skill never merges anything itself. It plans, a
human approves, and the CRM's own merge tool does the merging.

## Files

- `scripts/dedupe.py`: the dry-run engine: normalize, block, score, cluster, pick a
  survivor, merge fields. Needs `pandas` and `rapidfuzz`. Uses `phonenumbers` if it's
  installed.
- `scripts/evaluate.py`: scores a run against a labeled truth file (pairwise precision
  and recall).
- `assets/fixture/`: 41 synthetic contacts and 14 companies with planted duplicates,
  plus `truth.csv`.
- `references/field-standards.md`: normalization rules, state and country codes,
  lifecycle stage mapping, and flag meanings.
- `references/vendor-notes.md`: what merge keeps and destroys in each CRM, import
  quirks, and links to the official docs.
- `references/safe-rollout.md`: backup, sample merge, batch execution, and rollback.

## Workflow

1. **Get the exports.** Ask for a full-property CSV of contacts (or leads/people) and,
   when companies are in scope, companies (accounts/organizations) with record IDs.
   Record IDs matter because the cleaned files update records by ID.
2. **Back up first.** Before any merge, confirm the user has a dated full export that
   includes associations (`safe-rollout.md`, Phase 0). A backup is the only real rollback.
3. **Run the dry run:**
   ```bash
   pip install pandas rapidfuzz phonenumbers   # phonenumbers is optional but preferred
   python scripts/dedupe.py --contacts contacts.csv --companies companies.csv \
     --out plan/ --as-of 2026-09-22 [--default-region GB] [--gmail-canonical]
   ```
   The script detects columns from common vendor headers. Fix a wrong guess with
   `--col email="E-mail 1"` (or `--company-col` for the companies file).
4. **Check `summary.json` before trusting any number.** Confirm `column_map` (a deal
   `Stage` column mapped as lifecycle skews everything), `phone_engine`, and `warnings`,
   such as a block that was skipped for being too large.
5. **Present the results by tier.** Auto clusters: the count and a few examples. Review
   queue: every pair, with its reasons. Flags: counts by type. Associations: orphaned
   and missing links. Lead with the review queue, because it's where the user's judgment
   is needed.
6. **Walk the review queue with the data owner.** Record `merge` or `keep` in the
   `decision` column. Then look at the `kept_survivor_conflict` rows in
   `merge_plan.csv`: those are the values that will disappear.
7. **Hand off the execution plan.** Merge a sample of 5 to 10 clusters in the native tool,
   verify, then do the rest in batches. After merging, import the cleaned files keyed on
   record ID. Follow `safe-rollout.md`, and check `vendor-notes.md` for the specific CRM.

## Merge-safety rules

- **Never auto-merge on a role or shared identifier.** `info@`, `sales@`, a household
  inbox, or an office main line shows that records belong to the same organization, not
  that they're the same person. A shared identifier goes to review at most.
- **Auto-merge needs a strong ID plus a compatible name.** A strong ID is an exact
  non-shared email, or an exact non-shared phone. A name match alone, even 100% with the
  same company, only goes to review, because two people named David Kim at one company is
  normal in large organizations.
- **Re-check every pair inside a cluster.** A=B by email and B=C by phone can chain two
  different people together. The script demotes any cluster with an incompatible pair,
  or with more than `--max-cluster` (5) members, to review.
- **Never overwrite a non-empty value with an empty one.** The survivor's value wins.
  Blanks are filled from the best-ranked loser. Create date takes the earliest, last
  activity the latest, and lifecycle stage the furthest along. Losing emails and phones
  go to `additional_emails` and `additional_phones`, so they aren't dropped.
- **Pick the survivor on purpose.** The default order is `most_recent_activity`, then
  `most_complete`, then `oldest_created`. Add `business_email` first when the work
  address should be the primary email. In HubSpot and Pipedrive the primary's values win
  every conflict, so the survivor choice decides what's kept.
- **Gmail dot and plus folding is opt-in only** (`--gmail-canonical`). Google says dots
  don't matter for personal Gmail, but they do matter for Workspace domains. Applied by
  default, it would merge real, distinct mailboxes.
- **Stay a dry run.** Never call a CRM API, and never write to the input files. A merge
  runs in the CRM's native tool, which moves activity history. Delete-and-reimport
  doesn't.
- **Flag, don't delete.** Stale, test, and invalid records go in `record_flags.csv`. The
  data owner decides whether to archive or delete them.

## Output format

| File | Contents |
|---|---|
| `merge_plan.csv` | One row per cluster per field: `cluster_id, survivor_id, loser_ids, survivor_rule, field, winning_value, source_id, action, other_values`. The `action` is `kept_survivor`, `kept_survivor_conflict`, `filled_from_loser`, `earliest`, `latest`, `furthest_stage`, or `preserved_secondary` |
| `review_queue.csv` | Pairs needing a human: both records side by side, `confidence`, `reasons`, `suggested_survivor`, and blank `decision` and `decided_by` columns |
| `cleaned_contacts.csv` | The original columns with normalized values. Survivors carry merged values, and losers are removed. Also `additional_emails`, `additional_phones`, `_cleanup_action`, and `_flags` |
| `record_flags.csv` | `invalid_email`, `email_domain_typo`, `role_email`, `shared_phone`, `no_contact_method`, `phone_unparsed`, `junk_or_test`, `missing_name`, `stale` |
| `companies_*.csv`, `cleaned_companies.csv` | The same outputs for companies (domain-first matching) |
| `associations.csv` | `company_merged` (the ID was re-pointed to the survivor), `orphan_company_id`, `missing_association` (the email domain matches a company) |
| `summary.json` | Counts, flag totals, column map, settings, warnings |

When reporting to the user, give: records in and out, auto clusters, review pairs, flag
counts, the three riskiest review pairs, and the next gate from `safe-rollout.md`.

## Worked example (bundled fixture)

```bash
python scripts/dedupe.py --contacts assets/fixture/contacts.csv \
  --companies assets/fixture/companies.csv --out plan/ --as-of 2026-09-22
python scripts/evaluate.py --plan-dir plan/ --truth assets/fixture/truth.csv
```

The fixture is 41 contacts holding 14 true duplicate pairs. It includes case and
whitespace email variants, a name typo, a nickname with a reformatted phone, the same
person with a work and a Gmail address, `Inc` versus no `Inc`, a hyphenated married name,
a 3-record cluster, and a Gmail dot/plus variant. It also plants traps that must not
merge: three people sharing `info@stark.com`, a couple sharing a household inbox, three
colleagues on one office line, and two different people named David Kim.

| Run | Auto pairs | Wrong auto | Auto precision | Auto recall | Recall incl. review |
|---|---|---|---|---|---|
| Naive: exact lowercase email only | 11 | 4 (the `info@` trio and the household) | 63.6% | 50.0% | n/a |
| Default | 11 | 0 | 100% | 78.6% | 100% |
| `--gmail-canonical` | 12 | 0 | 100% | 85.7% | 100% |

In the default run, 7 contact clusters absorb 9 records, and 6 pairs go to review: 3 true
duplicates plus the household and `info@` traps. For companies, `Acme Inc`/`ACME` and
`Tyrell Corp`/`The Tyrell Corporation` auto-merge by domain. `Globex LLC`/`Globex
Corporation` (no domain) and `Umbrella Ltd`/`Umbrella Corporation` (different domains) go
to review. Three association issues surface, including an orphaned `CO99` reference.

Cluster `MC0001` (Jane Doe x3) shows the field rules at work. Create date `2022-03-14`
comes from the oldest record. Lifecycle stage `customer` is the furthest along. The blank
state on the survivor is filled from C001, and the work email is kept in
`additional_emails`.

## Tuning

- `--auto-name-sim 85`, `--review-name-sim 88`, `--conflict-name-sim 60`: raise the auto
  threshold for large, name-dense databases.
- `--stale-days 365`, `--as-of`: set the staleness window. Always pass `--as-of` so reruns
  are reproducible.
- `--max-block 500`: blocks bigger than this are skipped with a warning. Keeping blocks
  small keeps pair scoring fast on 100k-row exports.
- Extend `NICKNAMES`, `ROLE_LOCALS`, `LIFECYCLE_MAP`, or `LEGAL_SUFFIXES` in the script
  for a specific region or portal. Custom HubSpot lifecycle stages have numeric internal
  IDs.
