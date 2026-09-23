---
name: spreadsheet-qa
description: Answers business questions about the user's own spreadsheet or data export (CSV, TSV, XLSX from a CRM, Shopify, Stripe, QuickBooks, ad platforms, HR or payroll systems) correctly and auditably. Profiles every file first (grain, duplicate keys, embedded Grand Total rows, text-stored numbers, mixed currencies, UTC timestamps, Excel serial dates, hidden rows), states the metric definition used, computes every number in SQL or pandas instead of mental math, checks joins for fan-out, reconciles to a known total, and returns the query, filters, row counts, and rows behind the answer. Use this whenever the user says "analyze this spreadsheet", "how many...", "what's the total in this export", "which customers...", "pivot this", "revenue by month", "top 10", "what's our churn/MRR/AOV", or asks any question about their data, CSV, or Excel file, even a quick one. Also use when they ask to change values in a data file.
---

# Spreadsheet QA

Business exports lie quietly. A "Grand Total" row doubles every SUM. A customer listed twice multiplies their orders through a join. EUR and USD sit in one amount column. A UTC timestamp at 02:30 on Aug 1 is a July order in New York. None of these raise an error, so an answer computed by eye or by one quick query looks right and is wrong. This skill makes every number reproducible: profile, define, compute in code, reconcile, show the evidence.

Scope: questions about the data in the file. To combine or dedupe several files into one first, use `csv-excel-merger`. To check whether a financial model's formulas are sound, use `spreadsheet-model-auditor`.

## Workflow

### 1. Profile before answering anything

```bash
python3 scripts/profile.py path/to/*.csv path/to/book.xlsx --out sqa_out
```

Read `sqa_out/profile.md`. It reports, per file and sheet: header row, row count, candidate keys, duplicate keys, each column's type and parse rate, null %, distinct count, min/max, top values, currency and timezone hints, date ranges, embedded total/footer rows, hidden rows/columns, autofilters, merged cells, and a join-risk section predicting fan-out between files. It also drafts `data_dictionary.md` with open questions.

Why first: the traps above are visible only in the profile. Once a query has run, nobody rereads the raw rows. Do this even for "just give me the total": the total is the question most exposed to embedded total rows.

State the grain in one line per table ("one row = one order; key order_id") before writing a query. If no key is unique, say what one row is before counting anything.

### 2. Pin the metric definition, then proceed

Look up the metric in `references/metric-definitions.md`. If different definitions give materially different answers, list the one to three that matter, pick a stated default, and continue. Do not stall waiting for an answer. Example:

> Using net revenue = paid orders minus refunds against them, in USD at the rates in fx_rates.csv, by UTC date. By refund date instead: 8,710. Gross: 9,020. Say if you want one of those.

Ask before computing only when the choice is unknowable and decisive: which of two amount columns is the real one, which currency to report in when no rates exist, or what "active" means when the file has no activity dates.

Never invent a definition silently. "Active customer", "revenue", "churn", and "conversion" each have several; the answer must name the one used.

### 3. Compute in code only

Write a question spec (JSON steps) and run it:

```bash
python3 scripts/ask.py spec.json --out sqa_out/q1
```

Each step is one SQL view built on the previous ones, with a `kind`: `clean` (cast text, drop total rows), `filter`, `join`, `dedupe`, `derive`, `aggregate` (last step is the answer). ask.py counts rows before and after every step, fails the run when a join grows rows (fan-out) and warns when one drops rows, runs `assert_zero` checks (e.g. "amounts that failed to parse"), and writes `answer.md`, `query.sql`, `steps.json`, and `rows_used.csv`. Worked specs covering all of this: `tests/questions/*.json`. Copy the closest one.

Rules:
- Every source column loads as text. Cast explicitly with `to_num()` (handles "$1,200.00", "(35.00)", "12%") and `excel_date()`, and assert that nothing failed to parse. Auto-typing is how "$1,200" becomes NULL without anyone noticing.
- Exclude embedded total, subtotal, and footer rows in the first clean step and let the row count show it.
- Dedupe lookup tables (customers, products) before joining, or aggregate the many side first (refunds per order). Use LEFT JOIN and count unmatched rows instead of letting an inner join drop them.
- Convert currencies through an explicit rate table and assert every row found a rate. If there are no rates, report per currency.
- Convert timestamps to the reporting timezone before bucketing by day, week, or month: `CAST(ts AS TIMESTAMPTZ) AT TIME ZONE 'America/New_York'`.
- Recompute rates (CTR, margin %, conversion) from summed parts. Never average row-level rates.
- No mental math, including "quick" sums in prose. If a number appears in the answer, it came from a query output. Differences, percentages, and "X more than last month" too: add them as a step.
- DuckDB is the engine (`pip install duckdb`). Without it, ask.py falls back to SQLite, which lacks timezone functions; or use pandas and print the same row counts yourself.

For a one-off exploratory look, `ask.py --table orders=orders.csv --sql "SELECT ..."` works, but the final answer comes from a spec with the full step accounting.

### 4. Reconcile

Before reporting, tie the number to something independent. Add a `reconcile` entry to the spec:
- the export's own total row (your parsed sum must equal it)
- a total the user quoted, or one from the source system's dashboard
- the ungrouped total (grouped rows must sum to it; this is what catches fan-out)
- a second route to the same number (net = gross - refunds computed separately)

If it does not reconcile, the answer is not ready. Find the gap (usually filters, a hidden row, a timezone edge, or a status value) and say what explains it. Filtered views are a common cause: ask which filters the user's reference number used. `references/traps.md` lists the usual culprits.

### 5. Answer with an evidence block

Lead with the number and the definition in one or two sentences, then the evidence:

```
Net revenue, Q3 2026: $8,260.00 (USD, paid orders minus refunds against them, UTC dates)

Evidence
- Source: orders.csv (17 rows), refunds.csv (3), fx_rates.csv (3)
- Filters: dropped 1 Grand Total row (17 -> 16); status = paid, created Jul 1-Sep 30 UTC (16 -> 13)
- Joins: FX rates (13 -> 13, all matched); refunds pre-summed per order (13 -> 13)
- Reconciled: parsed amounts = the export's own Grand Total (9,700); net = gross 9,020 - refunds 760
- Other definitions: by refund date 8,710; gross 9,020
- Caveats: one fixed FX rate per currency, not transaction-date rates
- Query and rows: sqa_out/q1/query.sql, sqa_out/q1/rows_used.csv
```

Show sample rows when the user asks "which" (which customers, which orders): list the rows themselves, not only a count. Keep the evidence block even when the user wants a quick answer. It is five lines and it is what lets them trust or challenge the number.

## Editing data safely

When asked to change values in a file (fix a price, update a status, correct an invoice line):

1. Copy the original first. Never edit the only copy.
2. Change only the targeted cells, addressed by a unique key and column name, never by row position or by rewriting the whole file from memory. Re-emitting a full table from context is how an edit to one invoice line also changes the bank account number on another.
3. Diff before and after for every other column:

```bash
python3 scripts/diff_edit.py original.csv edited.csv --key invoice_id --allow amount --rows INV-7
```

It lists every changed cell and exits 1 if anything outside the allowed columns and rows changed, or if rows or columns appeared or disappeared. Show the user the diff. For .xlsx, edit with openpyxl on the specific cells so formulas and formatting survive, then run the same diff on the sheet.

## Testing

`python3 tests/run_tests.py` rebuilds the fixtures (orders with a Grand Total row, text amounts, three currencies and UTC timestamps; customers with a duplicated key; refunds; an xlsx with a title row, serial dates, a hidden row, and a Total row), checks that the profile catches every trap, answers four questions against hand-computed values, confirms the naive join is caught, and checks the edit diff.
