---
name: csv-excel-merger
description: Merge multiple CSV/Excel files with intelligent column matching, data deduplication, and conflict resolution. Handles different schemas, formats, and combines data sources. Use when users need to merge spreadsheets, combine data exports, or consolidate multiple files into one.
---

# CSV/Excel Merger

Merge multiple CSV or Excel files with automatic column matching, deduplication, and conflict resolution.

## Contents

- [Workflow](#workflow) — the step-by-step merge process
- [Verification](#verification) — confirm the merge before handing it back
- [Special cases](#special-cases) — encoding, compound keys, large files
- [Guidelines](#guidelines) — quality and transparency standards
- [Example triggers](#example-triggers)
- `references/merge_strategies.md` — column matching, conflict resolution, and dedup options
- `references/output_template.md` — the merge-report format

## Workflow

1. **Inspect the inputs.** Determine file count, format (CSV / Excel / TSV), and whether the files are attached or read from disk. Read each header; identify column names, data types, and encoding (UTF-8, Latin-1). Note the candidate primary key.

2. **Plan the merge.** Match columns across files to one unified schema, choose a conflict-resolution rule, and pick a deduplication strategy. See `references/merge_strategies.md` for the matching heuristics and the full set of options.

3. **Execute the merge** with pandas:

   ```python
   import pandas as pd

   df1 = pd.read_csv("file1.csv")
   df2 = pd.read_csv("file2.csv")

   # Normalize, then map column names onto the unified schema
   for df in (df1, df2):
       df.columns = df.columns.str.lower().str.strip()
   df2 = df2.rename(columns={"firstname": "first_name", "e_mail": "email"})

   merged = pd.concat([df1, df2], ignore_index=True)
   merged = merged.drop_duplicates(subset=["email"], keep="last")
   merged.to_csv("merged_output.csv", index=False)
   ```

4. **Verify the result** before reporting — see [Verification](#verification).

5. **Report** using the layout in `references/output_template.md`, then offer export options: CSV (UTF-8), Excel (.xlsx), JSON, SQL INSERT statements, or Parquet for large datasets.

## Verification

Never hand back a merge without checking it. After merging, assert the row math holds and the key is actually unique:

```python
total_in = len(df1) + len(df2)
assert len(merged) > 0, "merge produced an empty frame"
assert len(merged) <= total_in, "more rows than inputs — check the concat/join"
assert merged["email"].is_unique, "duplicate keys remain after dedup"

print(f"in: {total_in} rows | out: {len(merged)} rows | removed: {total_in - len(merged)}")
print(f"null keys: {merged['email'].isna().sum()} | columns: {list(merged.columns)}")
```

Report rows in vs. out, duplicates removed, and per-column completeness so the user can sanity-check the numbers against their own expectations.

## Special cases

- **Compound keys** — when no single column is unique, key on a tuple: `subset=["email", "company"]`.
- **Mixed data types** — standardize dates, phone numbers, and country codes; strip whitespace and normalize casing *before* deduping, or near-duplicates slip through.
- **Missing columns** — fill absent columns with empty values and flag them in the report; never silently drop data.
- **Large files (>100MB)** — read in chunks (`pd.read_csv(path, chunksize=...)`), report progress, and estimate memory before loading everything at once.

## Guidelines

- **Column matching** — prefer exact, then case-insensitive, then fuzzy. Always emit the original → unified mapping so every match is auditable, and allow manual override.
- **Data quality** — trim whitespace, standardize formats, flag invalid values, preserve types.
- **Transparency** — track the source file for every surviving row, log each merge decision, and report all conflicts with their resolutions.
- **Performance** — chunk large files, process in batches, and show progress on long-running merges.

## Example triggers

- "Merge these three CSV files"
- "Combine multiple Excel sheets into one file"
- "Deduplicate and merge customer data"
- "Join spreadsheets with different column names"
- "Consolidate contact lists from different sources"
