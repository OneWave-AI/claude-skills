# Merge Strategies

Reference for the `csv-excel-merger` skill. Covers column matching, conflict resolution, and deduplication.

## Column matching

Map columns from different files onto a single unified schema, in order of confidence:

- **Exact** — `email` = `email`
- **Case-insensitive** — `Email` = `email`
- **Fuzzy** — `E-mail` ≈ `email`

Common groupings seen in real data:

| Unified      | Variants                                  |
|--------------|-------------------------------------------|
| `first_name` | `firstname`, `First Name`, `fname`        |
| `last_name`  | `lastname`, `Last Name`, `lname`          |
| `email`      | `e-mail`, `email_address`, `Email`        |
| `phone`      | `phone_number`, `mobile`, `tel`           |
| `company`    | `organization`, `org`                     |
| `title`      | `job_title`, `position`                   |

Always emit the original → unified mapping in the report so the matching is auditable, and let the user override it.

## Conflict resolution

When the same record appears in multiple files with differing values:

- **Keep first** — value from the first file
- **Keep last** — value from the last (most recent) file
- **Keep longest** — the most complete value
- **Merge** — combine non-conflicting fields across sources
- **Manual review** — flag the conflict for the user to resolve

## Deduplication

Identify duplicates by primary key, then choose:

- **keep first** / **keep last** / **keep all**
- **merge values** — fold complementary fields into one row

Track the source file for every surviving row so data lineage is preserved.
