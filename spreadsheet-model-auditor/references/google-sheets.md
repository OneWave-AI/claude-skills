# Auditing Google Sheets models

The script reads .xlsx. Export first; everything structural survives the export.

## Export

- In the browser: File > Download > Microsoft Excel (.xlsx). The download includes stored values for every formula, so cached-value checks run without `--recalc`.
- From Drive, for automation: the Drive API export endpoint with MIME type `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, or `https://docs.google.com/spreadsheets/d/<ID>/export?format=xlsx` for a file the user can open.
- Do not use CSV export. It flattens one tab to values and discards every formula.

Hidden sheets, hidden rows/columns, and named ranges export intact, so those checks work as normal.

## Sheets-only functions and what happens to them

Excel has no equivalent for several Sheets functions. On export they are kept as formula text with the value Sheets last computed, so the script still sees them as formulas; LibreOffice `--recalc` may turn them into `#NAME?`. Do not use `--recalc` on a Sheets export unless you need to -- the cached values are already there and are Sheets' own results.

| Function | Audit concern |
|---|---|
| `IMPORTRANGE` | Cross-file link, like an Excel external link. The script flags it as `external_link` (high), including when the export wraps it in `__xludf.DUMMYFUNCTION`: the source file can change or lose sharing. |
| `IMPORTDATA`, `IMPORTHTML`, `IMPORTXML`, `IMPORTFEED` | Live pulls from the web (flagged as `external_link`). Values change without anyone editing the model. Note the source and as-of date. |
| `GOOGLEFINANCE` | Live market data (flagged as `external_link`); volatile. Numbers differ by the hour. |
| `QUERY` | A SQL-like string -- column letters inside the string are invisible to dependency tracing, like INDIRECT. Read each QUERY string by hand. |
| `ARRAYFORMULA`, `FILTER`, `SORT`, `UNIQUE` | One formula fills a range. Only the top-left cell holds the formula; the rest are values in the export, which can look like typed numbers. If a `pasted_over_formula` finding sits inside an array's spill area, it is a false positive. |
| `SPARKLINE`, `IMAGE` | Presentation only; ignore. |
| `NOW`, `TODAY`, `RAND` | Same volatility concerns as Excel; Sheets can also be set to recalculate them every minute or hour (File > Settings > Calculation). |

## Sheets-specific things to check by hand

- **Iterative calculation** (File > Settings > Calculation). If on, circular references calculate silently. The script still finds them; tell the user the setting is masking them.
- **Named functions and Apps Script custom functions** (`=MYFUNC(...)`) export as unknown functions. Their logic lives outside the sheet; ask for the script or treat outputs as unverified inputs.
- **Connected Sheets / BigQuery data** and pivot tables export as values. Audit the source query separately.
- **Edit history.** Sheets keeps version history; when a total changed unexpectedly, File > Version history shows who changed which cell and when. Recommend it when a `pasted_over_formula` or `hardcoded_total` needs an owner.
- **Protected ranges** do not export; ask whether inputs are protected, since unprotected formula rows are how pasted-over values happen.
