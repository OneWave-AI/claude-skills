# Vendor notes: how merge works, what it destroys, import quirks

Checked against each vendor's official help center in September 2026. Vendors change
merge behavior without notice, so re-open the linked page before a large merge and trust
it over this file wherever they disagree. Anything the docs do not state is marked
**not documented**; treat it as a risk, not a guarantee.

## Contents
- Cross-vendor summary
- HubSpot
- Salesforce
- Pipedrive
- Zoho CRM
- Close
- Attio
- Any other CRM

## Cross-vendor summary

| | Undo a merge? | Records per merge | Conflicting field values |
|---|---|---|---|
| HubSpot | No | 2 | Primary record wins, with exceptions (below) |
| Salesforce | Loser goes to Recycle Bin | Up to 3 | You pick per field in the merge screen |
| Pipedrive | No | 2 | Primary wins; you can preview first |
| Zoho CRM | No, losers deleted permanently | Up to 3 | You pick per field; exact matches auto-merge |
| Close | Not documented | Support-run bulk merge | Pick a winner rule: first created, latest status change, highest-priority status |
| Attio | Not documented | 2 (one pair at a time) | The right-hand record wins |

Across all six, merging is effectively permanent. So the dry-run plan, backup export, and
sample merge in `safe-rollout.md` are required, not optional extras.

## HubSpot

Source: [Merge records](https://knowledge.hubspot.com/records/merge-records),
[Deduplication of records](https://knowledge.hubspot.com/records/deduplication-of-records),
[Import records for a single object](https://knowledge.hubspot.com/import-and-export/import-records-for-a-single-object).

Merge behavior:
- The primary record's property values win. The exceptions: email (both are kept, and the
  secondary's becomes an additional email), lifecycle stage (the one furthest down the
  funnel is kept), form submissions (combined), analytics properties (totaled).
- Create date is taken from the oldest record, whichever one is primary.
- Timeline activities and associated records from both records end up on the merged record.
- Companies: the primary's domain stays primary and the other becomes a secondary domain.
  You can't merge a company that is a parent or child in a parent/child relationship.
- **Records can't be unmerged.** To recover, recreate the record from your backup, using
  the secondary email or domain that was kept.
- You can't merge a record that has already been part of 250 or more combined merges.

What gets lost: the secondary record's conflicting property values. The primary wins even
when the secondary's value is newer or better. Pick the primary deliberately, or copy the
values you want onto it before merging. `merge_plan.csv` lists every such value in
`other_values`.

Import and dedupe quirks:
- Contacts are deduplicated by email and companies by domain, both on import and on form
  submission. If the portal already has several records with the same email or domain,
  importing that value **fails with an error** rather than guessing.
- If you map Record ID in an import, it overrides every other unique identifier. A row
  with no Record ID creates a new record. So when you import `cleaned_contacts.csv`, map
  Record ID so rows update records and don't create new ones.
- Companies created through the API or a third-party sync app are **not** deduplicated by
  domain. Integrations are a common source of duplicate companies.

## Salesforce

Source: [Considerations for Merging Duplicate Contacts](https://help.salesforce.com/s/articleView?id=sales.contacts_considerations_for_merging_duplicates.htm&language=en_US&type=5),
[Merge Duplicate Accounts in Salesforce Classic](https://help.salesforce.com/apex/HTViewHelpDoc?id=sf.account_merge_classic.htm&language=en_us),
[Merge Duplicate Accounts in Lightning Experience](https://help.salesforce.com/s/articleView?language=en_US&id=sales.account_merge_lex.htm&type=5),
[Recycle Bin](https://help.salesforce.com/s/articleView?id=xcloud.recycle_bin.htm&language=en_US&type=5).

Merge behavior:
- Up to three records per merge. You pick one principal (master) record, then choose which
  record's value to keep for each field. Fields with conflicting values are highlighted.
- The merged record keeps Created By and Created Date from the **oldest** record,
  whichever one is primary.
- Hidden and read-only fields don't appear in the merge screen, and their values are kept
  **from the primary record only**. That is a silent loss. Export those fields first.
- Related items are re-parented to the merged record, with exceptions: Chatter feeds are
  kept from the primary only, and contact roles on the non-master contacts lose their
  primary status.
- Portal users: if a non-master contact has a portal user, that user is deactivated.
- Account merge requires Delete permission on accounts. You also have to be an admin, the
  account owner, or above the owner in the role hierarchy.
- Non-master records go to the Recycle Bin. Deleted items stay there for 15 days (30 if
  Salesforce Support enables extended retention).

Rollback caveat: undeleting a merged-away record from the Recycle Bin brings the record
back. Nothing documented says the related records re-parented during the merge move back.
Plan to re-point them yourself using the backup export.

Import quirks: the Data Import Wizard can match contacts and leads by Salesforce ID, name,
or email (external ID for custom objects). Record IDs are case-sensitive, so a spreadsheet
tool that changes their case breaks matching. Use the 18-character IDs from a report or
Data Loader export.

## Pipedrive

Source: [Merge duplicates](https://support.pipedrive.com/en/article/merge-duplicates),
[How does the Merge Duplicates feature identify duplicates](https://support.pipedrive.com/en/article/how-does-the-merge-duplicates-feature-identify-duplicates-in-pipedrive),
[How to avoid duplicates during an import](https://support.pipedrive.com/en/article/how-to-avoid-duplicates-during-an-import).

Merge behavior:
- You choose a primary item. Where values conflict, the primary's data is kept. There is a
  preview step where you can swap which record is primary.
- **Merged items can't be un-merged.**
- Only admins, or regular users with the right permission, can merge. Regular users only
  see the duplicates they have visibility to, so a non-admin sees a partial duplicate list.
- The built-in duplicate finder matches people on the same name **plus** one of: same
  phone, same email, or same organization. It matches organizations on the same name, or
  on the same address.
- What happens to deals, activities, emails, and notes is **not documented** in the merge
  article. Check a sample merge before you do the rest.

Import quirks:
- During import, Pipedrive can merge a person into an existing one when Person
  Organization, Phone, **or** Email matches. That is looser than you might expect: two
  colleagues sharing an organization can merge. Turn off the import-time merge option and
  use this skill's plan instead.
- Organizations are matched on address only at import. Two organizations with the same
  name but no address import as separate records.
- Deals have no duplicate identifier and always import as new records.

## Zoho CRM

Source: [Merging Duplicate Records](https://help.zoho.com/portal/en/kb/crm/manage-crm-data/duplication-management/articles/merge-duplicate-record),
[De-duplicate records](https://help.zoho.com/portal/en/kb/crm/manage-crm-data/duplication-management/articles/auto-merge-duplicates).

- Up to three records per merge. You pick a master record and choose the final value
  field by field.
- Attachments, notes, and activities move to the master record.
- **Merged records are deleted permanently and the action can't be reverted.**
- Needs the "Find and Merge" module permission. Available for Leads, Accounts, Contacts,
  Deals, Vendors, and custom modules.
- The De-duplicate tool merges records **automatically** when every field value matches,
  and asks you to resolve conflicts otherwise. Automatic merging only on exact matches is
  safe, but still take the backup first.

## Close

Source: [Finding and Merging Duplicates](https://help.close.com/getting-started/import-data-into-close/finding-and-merging-duplicates),
[Avoiding Lead Duplicates](https://help.close.com/getting-started/import-data-into-close/avoiding-lead-duplicates).

- There is no duplicate detection in the UI. A support tool run with your API key finds
  duplicate leads by lead name, phone, or email, and duplicate contacts within the same
  lead. You review the CSV it produces, pick a winner rule, and Close support carries out
  the merge.
- Winner rules: the lead created first, the lead with the most recent status change, or
  the lead with the highest-priority status.
- The docs don't say what data transfers or whether a merge can be undone. Assume it
  can't.
- Close is lead-centric: one lead (company) holds several contacts. Dedupe leads first,
  then contacts within each lead.

## Attio

Source: [Merge and delete records](https://attio.com/help/reference/managing-your-data/records/merge-and-delete-records).

- Only People and Companies records can be merged. Deals, Workspaces, Users, and custom
  objects can't.
- Records merge one pair at a time, and there is no bulk merge. The right-hand record's
  values win conflicts, and you can swap the two records' positions before merging.
- Both source records are marked as merged, and a **new record with a new ID** is created.
  Any external system that stored the old IDs has to be updated. Note this in the rollout
  plan.

## Any other CRM

Before you merge anything, find out five things from the vendor's docs, or by test-merging
two throwaway records:
1. Can a merge be undone? If so, for how long?
2. Which record's values win a conflict, and can you choose per field?
3. Do activities, notes, emails, deals, and files move to the survivor?
4. Does the survivor keep its ID, or does a new ID replace both?
5. What does import match on (ID, email, domain, name)? Does a blank cell overwrite a
   value that's already there?

Put the answers in the rollout plan. If you can't find the answers, do the sample merge
from `safe-rollout.md` before anything else.
