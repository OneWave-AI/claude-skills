---
name: spreadsheet-model-auditor
description: Audits business spreadsheet models (.xlsx, .xlsm, or Google Sheets exported to .xlsx) for structural integrity errors and explains each fix -- budgets, forecasts, pricing models, commission calculators, FP&A packs, ops trackers, not only banking models. A bundled openpyxl script finds hardcoded numbers inside formulas, typed values pasted over formulas, inconsistent formulas across a row or column, #REF!/#DIV/0!/#N/A errors, circular references, SUM ranges that skip adjacent rows, totals that do not foot, whole-column ranges that double count, external links, volatile functions, and hidden sheets/rows, each with a cell address and severity. Use this whenever the user says "check my spreadsheet", "audit this model", "review this workbook", "why doesn't this total match", "is this forecast right", "sanity check my budget", "find errors in this Excel", or shares an xlsx/Sheets file and asks whether the numbers can be trusted, even if they never say "audit".
---

# Spreadsheet Model Auditor

Models look right when you read them cell by cell. Structural errors -- a SUM that stopped one row short, a formula overwritten with a typed number in month 7, a rate hardcoded in one copy of a formula -- are invisible to eyeballing and are exactly what gets people fired over a board number. Do not audit by reading the grid. Run the script, which reads every formula, then spend human judgment on what a script cannot know: whether the assumptions are sane.

## Workflow

### 1. Get an .xlsx

- Excel file: use it directly (.xlsx or .xlsm). Legacy .xls: convert first with `soffice --headless --convert-to xlsx file.xls`.
- Google Sheets: File > Download > Microsoft Excel (.xlsx). Read `references/google-sheets.md` for which Sheets functions survive export and what to check manually.
- CSV is not a model. It has no formulas; there is nothing structural to audit. Ask for the workbook.

### 2. Run the script

```bash
python3 scripts/audit_xlsx.py model.xlsx --json audit.json --md audit.md
```

Add `--recalc` when the report says `cached values: NO`. That happens when the file was written by a script, a BI export, or any tool that does not calculate: openpyxl can read formulas from any file, but stored results exist only if Excel (or LibreOffice) calculated and saved it. `--recalc` runs `soffice --headless --convert-to xlsx` on a copy so error, footing, and stale-value checks can run. Without LibreOffice the script still runs every formula-based check and says which value checks it skipped -- never report "no errors" for a check that was skipped.

Needs only `openpyxl` (`pip install openpyxl`). It handles 50k-formula workbooks in a few seconds.

### 3. Triage the findings

Read `audit.md`. Findings are ranked critical > high > medium > low > info, each with the cell, the formula, why it matters, and the fix. Before presenting:

- Open the cited cells yourself (the JSON has the formula). Confirm each critical and high finding is real in context; drop or downgrade what is clearly intentional (a labeled override row, a deliberate plug with a note).
- Collapse repeats. Twelve `sum_range_omission` findings across B11:M11 are one problem: "Total opex omits the Software row in every month."
- Trace the dollar impact of the top findings where you can: "Total opex is understated by 1,200/month, 14,400/year, so operating income is overstated by the same."
- `error_value` lists root causes only; propagated errors clear when the root is fixed.

The full list of checks, with examples and fixes, is in `references/error-catalog.md`. Read it when a finding type is unfamiliar or the user asks what a check means.

### 4. Review what the script cannot judge

Structural integrity is necessary, not sufficient. A perfectly built model with a 40% monthly growth rate is still wrong. Always do this pass and label it as judgment, not detection:

- **Assumptions.** List every input on the inputs sheet (or every typed number feeding formulas). For each: is it plausible for this business, sourced, and dated? Flag growth rates that compound to absurd annual numbers (3%/month is 43%/year), churn and conversion rates outside normal ranges, prices that disagree with the stated price list.
- **Units and periods.** Monthly vs annual rates mixed (an annual salary divided by 12 in one row and not another), thousands vs units, percentages typed as whole numbers, fiscal vs calendar periods, a 13th month or a missing one.
- **Sign conventions.** Costs positive-and-subtracted or negative-and-added, consistently. Check that every total's arithmetic matches the convention.
- **Timing.** Does cash follow the stated terms (net-30 revenue should not land the same month)? Do annual costs hit the right month?
- **Sensitivity of the top 3 drivers.** Identify the three inputs that move the headline output most (usually volume, price, and the largest cost). State the output at +/-10% on each, computed from the model's own structure. If the conclusion flips inside that range, say so -- that is the most useful sentence in the audit.
- **Does it answer the question?** A forecast with no cash line, a commission calc that ignores clawbacks, a pricing model with no volume discount: note what is missing.

### 5. Report

Use this shape. Lead with the verdict, not the method.

```
## Verdict
<Trustworthy / Usable after fixes / Do not use>, in one or two sentences with the
dollar impact of the worst problem.

## Must fix (critical + high)
1. <Sheet!Cell> -- <what is wrong in plain words> -- <impact> -- <exact fix>

## Should fix (medium)
## Worth knowing (low / info, grouped)

## Assumption review (judgment, not detected)
<table: input, value, concern, suggested range or question for the owner>

## Sensitivity
<top 3 drivers, output at -10% / base / +10%>

## Not checked
<anything skipped: no cached values, INDIRECT targets, macros, pivot tables>
```

Offer to fix the workbook when the user wants it: make the changes with openpyxl on a copy (never overwrite the original), re-run the audit on the copy, and show the before/after finding counts.

## What the script cannot catch

Say these limits out loud when relevant instead of implying a clean bill of health:

- Wrong logic that is internally consistent (the wrong formula copied correctly across all 12 months).
- Wrong assumptions, wrong units, wrong source data.
- Targets of INDIRECT and OFFSET (they are flagged, but their precedents are invisible), macros/VBA, Power Query, pivot table sources, data validation, conditional formatting logic.
- Values when the file has no cached results and LibreOffice is unavailable.
- LibreOffice recalculation is close to Excel but not identical for newer functions (LAMBDA, some dynamic arrays); treat value-based findings on those cells with care.

## Rules

- Cite every finding by `Sheet!Cell`. A finding without an address cannot be fixed.
- Never call a model "correct". The strongest claim is "no structural errors found by these checks", plus the assumption review.
- Separate detected (script) from judged (you). Readers weigh them differently.
- Business-neutral language: explain why it matters in terms of the decision the model drives (budget approval, price change, payout), not spreadsheet jargon.
- Do not modify the user's file unless asked, and then only a copy.

## Files

- `scripts/audit_xlsx.py` -- the auditor (JSON + markdown output).
- `references/error-catalog.md` -- every check: example, why it matters, fix, false-positive notes.
- `references/google-sheets.md` -- exporting from Sheets and Sheets-only functions.
- `examples/worked-example.md` -- a full run on a broken operating model, from script output to final report.
- `tests/build_fixtures.py`, `tests/run_tests.py` -- planted-error fixtures and the regression test.
