# Safe rollout: backup, sample merge, rollback

Most CRM merges can't be undone (see `vendor-notes.md`). The only real rollback is a
backup taken before the merge plus a record of what was merged into what. Go through these
phases in order and get the user's explicit go-ahead at each gate. A cleanup that saves an
hour and corrupts a pipeline costs a quarter.

## Phase 0: Freeze and back up

1. **Pause writers.** Turn off or pause the integrations, form-to-CRM syncs, enrichment
   tools, and workflows that create or update the records you're touching. Otherwise new
   duplicates land while you merge, and a workflow can fire on a survivor whose fields just
   changed.
2. **Full export of every object you'll touch**: contacts or leads, companies or accounts,
   and deals. Include **all properties**, not just the default view. Hidden and read-only
   fields are exactly what Salesforce drops silently from non-primary records.
3. **Export associations**: contact to company, contact to deal, company to deal. Many
   CRMs export these as separate files or ID columns. Without them you can't rebuild what a
   merge re-pointed.
4. **Export or snapshot activity counts** per record if the CRM allows it (emails, calls,
   meetings, notes). They let you prove after the merge that no history went missing.
5. Store the backup with a date in its name, somewhere outside the CRM, and read-only.
   Salesforce also offers a scheduled Data Export, and HubSpot and others allow full
   exports from settings. Use the native full export when there is one.

Gate: the user confirms the backup exists and says where it is stored.

## Phase 1: Dry run

```bash
python scripts/dedupe.py --contacts contacts.csv --companies companies.csv \
  --out plan/ --as-of YYYY-MM-DD
```

Review `summary.json` with the user: counts, warnings, `phone_engine`, and `column_map`.
A column mapped wrongly (for example `Stage` taken as lifecycle when it's really the deal
stage) makes every downstream number wrong, so confirm the map first.

## Phase 2: Human review

- Walk through `review_queue.csv` with the owner of the data, not only the admin. The
  owner knows that two records with the same name are a father and son. Fill in
  `decision` (`merge` or `keep`) and `decided_by`.
- Skim the auto clusters in `merge_plan.csv`. For each cluster, check the rows where
  `action` is `kept_survivor_conflict`: those are the values that disappear from the CRM.
  If a losing value is the better one (the newer title, the right owner), change the
  survivor rule or edit the survivor's value before merging.
- Pair merges that were approved in review become clusters for Phase 3. Re-running the
  script doesn't pick them up automatically; that is deliberate, so a human decision
  never gets lost in a re-run.

Gate: the user signs off on the auto list and on every review decision.

## Phase 3: Sample merge (5 to 10 clusters)

1. Pick 5 to 10 auto clusters that together cover the risky shapes: a 3-record cluster, a
   cluster with open deals, one with different owners, one with a secondary email, and a
   company cluster with contacts attached.
2. Merge them **in the CRM's native merge tool**, using the survivor from the plan as the
   primary. Don't merge by importing and then deleting: a native merge moves timeline
   activity, and delete-and-import throws it away.
3. Check each survivor:
   - the activity count equals the sum of the pre-merge counts
   - deals and tickets are still associated
   - the email and secondary emails are right, and so are the create date and lifecycle
     stage
   - the owner is the one the plan expected
   - no workflow fired unexpectedly (check the workflow history)
   - for Attio, the new record ID is recorded wherever the old IDs were stored
4. Write down anything that didn't match `vendor-notes.md` and update the plan.

Gate: the user reviews the sample results and approves the full run.

## Phase 4: Full merge in batches

- Merge in batches of 50 to 200 clusters. Record every executed merge (cluster ID,
  survivor ID, loser IDs, time, who ran it) in a `merge_log.csv`. The log plus the backup
  is the rollback.
- Tools that merge in bulk, such as vendor apps, the Salesforce API `merge()` call, or the
  HubSpot merge endpoint, are fine **only** if they take the survivor from this plan. This
  skill doesn't call them: run them yourself, with the user present.
- Stop at the first unexpected result and go back to Phase 3.

## Phase 5: Import the cleaned values

- Import `cleaned_contacts.csv` and `cleaned_companies.csv` **after** the merges, as an
  update keyed on the record ID (HubSpot Record ID, Salesforce 18-character ID, Pipedrive
  ID). Keying on email can create new records or fail when duplicates are still there.
- Leave out columns you don't mean to change, plus the helper columns `_cleanup_action`
  and `_flags`. Put `additional_emails` and `additional_phones` into the CRM's
  secondary-email and secondary-phone fields only if they exist.
- Check how the CRM treats blank cells on import before you include sparse columns.
  Behavior varies by vendor and setting. When unsure, drop the column.
- Associations: fix the rows in `associations.csv` by hand or with an association
  import. Orphaned company IDs mean the company was deleted or lives in a different export.

## Phase 6: Verify and resume

- Re-export and re-run the script. The auto count should now be close to zero. New auto
  clusters mean a writer kept running, or the import created records.
- Turn integrations and workflows back on one at a time.
- Keep the backup and `merge_log.csv` for at least one full sales cycle.

## Rollback by vendor

| Vendor | What rollback looks like |
|---|---|
| HubSpot | No unmerge. Recreate the record from the backup (the secondary email the merge kept helps you find it), then re-associate activities and deals by hand. Activity history can't be split back out. |
| Salesforce | Undelete the merged-away record from the Recycle Bin within 15 days (30 if extended). The docs don't say that re-parented related records move back, so re-point them from the backup's association export. |
| Pipedrive | No un-merge. Recreate from the backup. |
| Zoho CRM | Losers are deleted permanently. Recreate from the backup. |
| Close | Not documented. Ask Close support before the merge, and assume none. |
| Attio | Source records are marked as merged and a new ID is created. Recreate from the backup if needed, and update external systems with the new ID. |

Because every rollback is partial, precision beats recall. Leaving a duplicate unmerged
costs a second pass. Merging two different people costs their history, and possibly an
email sent to the wrong person.
