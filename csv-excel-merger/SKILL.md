---
name: csv-excel-merger
description: Merges, appends, joins, and deduplicates multiple CSV, TSV, and Excel files (including multi-sheet workbooks) with pandas - mapping mismatched column names to one schema, normalizing keys, resolving conflicting values, tracking which file each row came from, and verifying the row math. Use when the user wants to combine spreadsheets or exports, stack monthly files, consolidate contact or lead lists, VLOOKUP-style join two sheets on an ID or email, or dedupe records across sources, even if they only say "put these together" or "clean up these lists into one".
---

# CSV/Excel Merger

Combine tabular files into one clean output without silently losing, duplicating, or corrupting rows.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Profile inputs
- [ ] 2. Choose append vs join
- [ ] 3. Map columns and normalize keys
- [ ] 4. Merge and resolve conflicts
- [ ] 5. Verify row math
- [ ] 6. Write output and report
```

1. **Profile inputs.** Run the bundled profiler first; it reports encoding, delimiter, rows, headers, candidate keys, and header overlap without changing anything:

   ```bash
   python scripts/profile_inputs.py file1.csv file2.xlsx
   ```

   Excel files are profiled per sheet. Confirm with the user which sheets count if a workbook has more than one.

2. **Choose the operation.** This is the decision that most often goes wrong:
   - **Append (stack)** - same kind of records from different sources or periods (Jan + Feb exports, three lead lists). Use `pd.concat`, then dedupe.
   - **Join (enrich)** - different facts about the same entities (contacts + their deal values). Use `pd.merge` on a key.
   - Unsure? If the files share most columns, append. If they share only an ID column, join.

3. **Map columns and normalize keys.** Build an explicit `{original: unified}` rename map per file (see [references/merge_strategies.md](references/merge_strategies.md) for common variants) and show it to the user when any match is fuzzy. Normalize key columns before dedupe or join: strip whitespace, lowercase emails, strip non-digits from phones, unify date formats. Without this, `A@x.com ` and `a@x.com` survive as two people.

4. **Merge.** Read every file with `dtype=str` so IDs, ZIP codes, and phone numbers keep leading zeros, then convert specific columns afterward.

   ```python
   import pandas as pd

   frames = []
   for path, rename in [("jan.csv", {"E-mail": "email"}), ("feb.xlsx", {"Email Address": "email"})]:
       df = (pd.read_excel(path, dtype=str) if path.endswith((".xlsx", ".xls"))
             else pd.read_csv(path, dtype=str, encoding="utf-8-sig",  # use the profiler's encoding
                           keep_default_na=False))
       df = df.rename(columns=rename)
       df["email"] = df["email"].str.strip().str.lower()
       df["source_file"] = path          # lineage for every row
       frames.append(df)

   combined = pd.concat(frames, ignore_index=True, sort=False)
   # Blank keys are not duplicates of each other: set them aside before deduping.
   has_key = combined["email"].fillna("") != ""
   # Later files win: list the most recent source last, then keep="last".
   deduped = combined[has_key].drop_duplicates(subset=["email"], keep="last")
   no_key = combined[~has_key]
   merged = pd.concat([deduped, no_key], ignore_index=True)
   ```

   For a join, make pandas enforce the relationship you expect so a duplicate key raises instead of multiplying rows:

   ```python
   out = pd.merge(contacts, deals, on="email", how="left",
                  validate="one_to_one", indicator=True)
   unmatched = out[out["_merge"] == "left_only"]
   ```

   Conflict strategies (keep first/last/most complete, combine fields, flag for review) are in [references/merge_strategies.md](references/merge_strategies.md).

5. **Verify before reporting.** Never hand back a merge without checking it:

   ```python
   rows_in = sum(len(f) for f in frames)
   assert len(merged) > 0, "merge produced an empty frame"
   assert len(merged) <= rows_in, "more rows out than in: check the join keys"
   assert deduped["email"].is_unique, "duplicate keys remain after dedupe"
   print(f"in={rows_in} out={len(merged)} removed={rows_in - len(merged)} blank_keys={len(no_key)}")
   print(merged["source_file"].value_counts())
   ```

   Spot-check three removed duplicates by hand against the source files; the asserts prove the math, not that the right row won.

6. **Write output and report.** Use the layout in [references/output_template.md](references/output_template.md).
   - CSV for Excel users: `to_csv(path, index=False, encoding="utf-8-sig")` (the BOM makes Excel read accents correctly).
   - Excel: `to_excel(path, index=False)` with openpyxl installed. A sheet holds at most 1,048,576 rows; split or use CSV/Parquet beyond that.
   - Also write `conflicts_review.csv` or `unmatched.csv` when those sets are non-empty.

## pandas version notes

Current pandas is 3.x (Python 3.11+). Differences that affect merges:
- Text columns default to the `str` dtype, not `object`. Check `pd.api.types.is_string_dtype(col)` instead of `dtype == object`.
- Copy-on-Write is always on. Chained assignment such as `df[col][mask] = x` never updates `df` (pandas only warns); use `df.loc[mask, col] = x`.
- Parsed datetimes default to microsecond resolution. Call `.dt.as_unit("ns")` before casting to integers if something downstream expects nanoseconds.
- `pd.read_excel(..., engine="calamine")` (needs `python-calamine`) reads large workbooks much faster than openpyxl.

The code in this skill also runs on pandas 2.2.

## Failure modes to check for

- **Row explosion on join** - duplicate keys on both sides multiply rows. `validate=` catches it.
- **Leading zeros lost** - reading without `dtype=str` turns `01234` into `1234`.
- **Excel-mangled values** - long IDs already shown as `1.23E+15` or dates already reformatted in the source file cannot be recovered by pandas; flag them.
- **Header rows not on line 1** - exports with a title block need `skiprows=` or `header=`.
- **Mixed encodings** - one file in cp1252 among UTF-8 files shows up as `Ã©` artifacts. The profiler reports the encoding per file.
- **Silent column drops** - a column present in only one file becomes mostly empty after append. Keep it and report its completeness; never drop data without saying so.
- **Large files** (over a few hundred MB) - read with `chunksize=` or use Polars/DuckDB, and dedupe with a key set instead of loading everything into memory.
