---
name: statement-extract-and-prove
description: Converts bank, credit card and brokerage statement PDFs, invoices and vendor price lists into clean CSV or Excel, then proves the extraction is complete and correct - opening balance plus transactions equals closing balance, every running balance chains, page totals, row counts and summary totals all tie, signs and decimal separators are consistent. Handles digital PDFs with word-position column bands and detects scanned PDFs that need OCR first. Use it whenever the user wants to convert a bank statement PDF to Excel or CSV, extract transactions from a statement, turn a PDF table into a spreadsheet, import statements into QuickBooks or Xero, or says the converted statement does not balance, rows are missing, or signs look wrong, even if they do not ask for a proof. Never reads amounts off the page image when a text layer exists, and never fixes a failed tie-out by guessing.
---

# Statement Extract and Prove

A model reading a statement PDF by eye drops rows on long tables, flips signs, reads `1.234,56` as 1.234, and invents numbers where a scan is faint. Roughly one statement in seven fails to tie on the first pass. The fix is deterministic extraction from the PDF text layer plus arithmetic that the statement itself supplies: the bank already printed the opening balance, the closing balance, often a running balance on every row, and a summary box. If the extracted rows reproduce all of those, the extraction is proven. If not, the arithmetic points at the exact row.

Scope: this skill gets statement and table rows out of PDFs and proves them. For categorizing and reconciling against the books, hand the CSV to `bookkeeping-close` (its `scripts/reconcile.py` reads this CSV directly). For pulling header fields out of receipts and invoices (vendor, total, due date), use `financial-parser`; that skill does field extraction, while this one handles row tables that must tie out.

## Setup

```
pip install pdfplumber openpyxl        # required; openpyxl only for --xlsx
# optional, scanned PDFs only: ocrmypdf + tesseract (see references/ocr.md)
```

## Workflow

### 1. Check for a text layer

Run the extractor. It checks the text layer first and exits with code 3 and `NO TEXT LAYER` when the PDF is an image. In that case, OCR it as described in `references/ocr.md` and continue with the OCR'd file. Do not start reading the page images yourself: OCR plus the proof below catches misreads, and eyeballing catches none.

### 2. Extract

```
python scripts/extract_statement.py statement.pdf --out out/stmt --xlsx \
    [--account-type bank|card] [--decimal auto|dot|comma] [--date-order auto|mdy|dmy]
```

- `--account-type card` for credit cards: charges raise the balance owed, so they come out positive and payments negative. For bank accounts, deposits are positive. This matches what `bookkeeping-close` expects.
- `--decimal` defaults to auto: it counts `.dd` against `,dd` endings in the amount columns and stops with exit 2 if the evidence is mixed. Pass the flag explicitly whenever you know the locale, because an explicit flag cannot be fooled by a statement with few amounts.
- Dates printed without a year get it from the statement period; those rows are flagged `year_inferred`.
- Read the summary line it prints: row count, layout, decimal, date order, period, low-confidence rows, unassigned lines. Any WARNING needs a look before you go on.

Outputs: `stmt.csv` (one row per transaction, with `page` and `y` for traceability, raw printed text, and flags), `stmt.meta.json` (summary box values, forward/closing markers, the column bands used on each page, and every table line that did not become a row), and optionally `stmt.xlsx`.

### 3. Prove

```
python scripts/prove.py out/stmt.csv [--opening X --closing Y --stated-count N]
```

Hard checks: opening + sum = closing; every printed running balance equals the previous one plus the amounts in between; page continuity (brought forward = carried forward, start + page rows = page end); credits and debits against the summary box and totals rows; row counts against any count the statement prints; duplicates across page breaks; and a number-format check. The number-format check is needed because the other invariants do not depend on scale: a statement where every amount was read 100x too large still ties out perfectly. Exit 0 prints `PROVEN`; anything else is `NOT PROVEN`, with `proof_report.md`, `proof.json` and `low_confidence.csv` written.

If the opening balance is not printed and the tool had to derive it from the first row, the verdict says so. Read the opening balance off the statement and pass `--opening`, because a derived opening proves nothing about the first row.

### 4. If the proof fails, localize before touching anything

The report tells you where the fault is. Work from it, in this order:

1. **Per-page table**: the page whose start + rows does not equal its end is the page with the fault.
2. **First broken running balance**: the diagnosis names a culprit row or a span between two y-positions. It identifies: wrong sign (the gap is twice one row's amount), power of ten (a decimal or thousands separator misread), extra row (removing it closes the gap, usually a duplicate or a subtotal read as a transaction), missing row (the gap equals a printed row that is not in the CSV; an unassigned line carrying that amount is named when one exists), no amount (usually wrong column bands), and misread balance (two consecutive breaks of opposite size).
3. **Tie-out explained**: when one break accounts for the whole gap, the report prints `LOCALIZED`. Fix that one thing, not the rest of the statement.

### 5. Re-extract the broken page with adjusted bands

Most failures are column bands: a page printed with a different template, a header the detector missed, or amounts drifting left of their header. Look at the real word positions:

```
python scripts/extract_statement.py statement.pdf --out /tmp/x --dump-words 2
```

Choose x-ranges that separate the columns, then re-run the whole document with overrides for that page only:

```
python scripts/extract_statement.py statement.pdf --out out/stmt \
    --bands "date=40-95,description=95-285,amount=285-480,balance=480-570" --band-pages 2
python scripts/prove.py out/stmt.csv
```

Other levers: `--decimal` when the number-format check fails, `--date-order` when dates land outside the period, `--account-type` when every sign is inverted, `--invert-amount` for a signed column printed from the other party's view, `--allow-integers` for price lists without cents. See `references/formats.md` for layouts and their traps.

### 6. Visual reading, last resort only

If a page still fails after band and flag adjustments (a damaged scan, handwriting, a stamp over a figure), render just that page (`pdftoppm -r 200 -f N -l N -png statement.pdf page`) and read only the rows in the localized span. Every value obtained this way goes into the deliverable marked `source=visual` in the flags column, the proof is re-run, and the handoff says which rows were read by eye. Never type in a number so that the statement ties; if the visual reading does not close the gap, report the gap.

### 7. Deliver

Hand over the CSV or XLSX, `proof_report.md`, and the low-confidence queue. State the verdict in one line: "PROVEN: 44 rows, opening 4,210.33 + 25,374.85 = closing 29,585.18, 20 running balances chained, totals and counts match." For NOT PROVEN, give the gap, the localized row or span, and what was tried. For bookkeeping, point to `bookkeeping-close` and pass the proven balances as `--statement-begin` / `--statement-end`.

## Rules

- Extract from the text layer. Only read the page image for a localized span after deterministic options are exhausted, and mark those rows.
- Report, do not repair. A plug, a dropped "extra" row, or a retyped amount must be confirmed against the page, never made up to close the gap.
- A tie-out with a derived opening balance, or with number-format conflicts, is not a proof.
- Keep `page` and `y` in every deliverable, so any figure can be traced back to its spot on the PDF.
- Multi-statement PDFs (a year of statements in one file): split by statement period and prove each statement on its own, because a combined tie-out hides offsetting errors.

## Files

- `scripts/extract_statement.py`: text-layer check, header and band detection, row assembly, number and date parsing, CSV/XLSX/meta output, `--dump-words`
- `scripts/prove.py`: invariants, diagnosis, report, low-confidence queue
- `references/formats.md`: statement layouts, sign conventions, locale number and date formats, invoice and price-list notes
- `references/ocr.md`: when to OCR, how, confidence, and re-checking OCR output
- `tests/make_fixtures.py`, `tests/run_tests.py`: synthetic statements (US 3-page running balance, German decimal comma, UK paid-out/paid-in with CR/DR, misaligned page, scanned) and corruption tests
