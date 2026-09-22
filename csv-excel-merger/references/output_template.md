# Merge Report Template

Reference for the `csv-excel-merger` skill. Use this layout when reporting a completed merge. Every number must come from the verification step, and the per-source counts must add up to the output total.

```
MERGE REPORT

INPUTS
  contacts_jan.csv       1,245 rows   8 cols   utf-8
  contacts_feb.csv         987 rows   9 cols   cp1252
  leads_export.xlsx      2,103 rows  12 cols   sheet "Leads"
  Total in:              4,335 rows

OPERATION
  Append + dedupe on email (normalized: trimmed, lowercased)
  Conflict rule: most recent source wins (feb > jan; export last)

COLUMN MAPPING
  first_name  <- firstname, First Name, fname
  email       <- email, e-mail, email_address
  phone       <- phone, mobile, phone_number
  company     <- company, organization
  source_file <- added for lineage
  Fuzzy matches confirmed by user: fname -> first_name

RESULTS
  Output:              merged_contacts.csv (utf-8-sig)
  Rows out:            3,443
  Duplicates removed:    892
  Blank-key rows kept:    31 (not deduped; listed in no_key_rows.csv)
  Conflicts:              47 (written to conflicts_review.csv)

  Surviving rows by source (sums to 3,443):
    contacts_jan.csv       610
    contacts_feb.csv       842
    leads_export.xlsx    1,991

  Completeness:
    email    99.1%
    phone    87.5%
    company  91.3%

CHECKS
  rows out <= rows in           pass
  email unique (keyed rows)     pass
  3 removed duplicates spot-checked against sources   pass

NEEDS ATTENTION
  - 47 conflicting phone numbers: review conflicts_review.csv
  - 12 IDs in leads_export.xlsx were already in scientific notation in the source file
```
