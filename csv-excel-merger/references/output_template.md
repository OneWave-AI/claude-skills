# Merge Report Template

Reference for the `csv-excel-merger` skill. Use this layout when reporting a completed merge.

```
CSV/EXCEL MERGER REPORT

INPUT FILES
  File 1: contacts_jan.csv    — 1,245 rows, 8 cols (name, email, phone, company, ...)
  File 2: contacts_feb.csv    —   987 rows, 9 cols (firstname, lastname, email, mobile, ...)
  File 3: leads_export.xlsx   — 2,103 rows, 12 cols (full_name, email_address, phone, ...)

COLUMN MAPPING (unified schema)
  first_name  <- firstname, first name, fname
  last_name   <- lastname, last name, lname
  email       <- email, e-mail, email_address
  phone       <- phone, mobile, phone_number, tel
  company     <- company, organization, org
  title       <- title, job_title, position
  source      <- file-origin tracking

MERGE ANALYSIS
  Rows before merge:   4,335
  Duplicates found:      892
  Conflicts detected:     47
  Primary key:         email
  Dedup strategy:      keep most recent (by source file date)

CONFLICTS (top 10)
  john.doe@example.com
    File 1 phone: (555) 123-4567
    File 2 phone: (555) 987-6543
    -> kept most recent (File 2)

RESULTS
  Output:      merged_contacts.csv
  Total rows:  3,443
  Columns:     7
  Removed:     892 duplicates

  By source:
    contacts_jan.csv    1,245 rows (398 unique)
    contacts_feb.csv      987 rows (521 unique)
    leads_export.xlsx   2,103 rows (2,524 unique)

  Completeness:
    email   98.2%
    phone   87.5%
    company 91.3%

RECOMMENDATIONS
  - Review 47 conflict records manually
  - Standardize phone number format
  - Fill missing company names (8.7% incomplete)
  - Export conflicts to conflicts_review.csv
```
