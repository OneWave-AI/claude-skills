# Error catalog

Every check `scripts/audit_xlsx.py` runs, in the order it is ranked. Each entry: what it detects, an example, why it matters, the fix, and when it may be a false positive. The `check` name matches the JSON field.

Severity scale: **critical** (the model's output is wrong or incomputable now), **high** (very likely wrong number in a visible output), **medium** (a fragility that will produce a wrong number when something changes), **low** (a smell worth a look), **info** (context, no action needed).

## Contents

1. circular_reference
2. error_value
3. pasted_over_formula
4. inconsistent_formula
5. sum_range_omission
6. total_does_not_foot / hardcoded_total
7. double_count
8. stale_cached_value
9. external_link
10. hardcoded_in_formula
11. ref_to_empty
12. whole_column_range
13. volatile_function
14. hidden_content
15. percent_as_whole_number
16. unit_outlier
17. mixed_sign_convention
18. cross_sheet_link, no_cached_values (info)

---

## 1. circular_reference -- critical

**Detects:** cells that depend on themselves through any chain of references, found by building the full dependency graph (ranges expanded, named ranges resolved) and finding strongly connected components.

**Example:** `B7 Processing fee =B8*0.02` and `B8 Amount incl fee =B6+B7`.

**Why it matters:** Excel either warns and shows 0, or with iterative calculation enabled converges to a value that depends on the iteration settings. Iterative calc is a workbook setting, so the same file gives different answers on different machines.

**Fix:** Solve it algebraically (fee = base * r / (1 - r)), use the prior period's balance (interest on opening balance, not average), or add an explicit on/off switch cell with a note.

**False positives:** none structurally; a deliberate, documented circularity (interest on average debt in a financing model) is still reported -- note it as intentional.

## 2. error_value -- critical (#REF!) / high (others)

**Detects:** cached values of `#REF!`, `#DIV/0!`, `#N/A`, `#VALUE!`, `#NAME?`, `#NUM!`, `#NULL!`, `#SPILL!`, `#CALC!`, and any formula whose text contains `#REF!` (detected even without cached values). Only root causes are listed; the count of cells that merely inherit an error is reported once as info.

**Example:** `=Forecast!N4/B3` where B3 is blank gives `#DIV/0!`; `=#REF!*2` after a referenced row was deleted.

**Why it matters:** Errors propagate into every dependent cell and are often masked by `IFERROR(...,0)` further down, turning a broken input into a silent zero.

**Fix:** Fix the root. `#REF!` must be rebuilt by hand (the original reference is gone). For `#DIV/0!`, guard the denominator explicitly (`=IF(B3=0,"n/a",N4/B3)`) rather than wrapping in IFERROR. For `#N/A` from lookups, check the key exists; for external links, see section 9.

**False positives:** `#N/A` used deliberately to blank chart points.

## 3. pasted_over_formula -- high / medium

**Detects:** a typed number in a row between two cells with the same relative (R1C1) formula, at the end of a row of matching formulas, or inside a column of matching formulas.

**Example:** Revenue row `=B2*B3 ... =G2*G3, 52000, =I2*I3 ...` -- July was pasted as a value.

**Why it matters:** The cell looks like part of the calculation but never updates. Change price or volume and every month moves except July.

**Fix:** Copy the neighboring formula back in. If an override is intended, put it in a separate, labeled override row and add it in the formula (`=H2*H3+H20`), so the override is visible and reversible.

**False positives:** a model that intentionally switches from actuals (typed) to forecast (formulas) -- the actuals are usually on the left and contiguous, and are not flagged unless a formula sits on both sides.

## 4. inconsistent_formula -- high (middle) / medium (last) / low (first)

**Detects:** within a contiguous run of formulas along a row or column (4+ cells), cells whose R1C1 form differs from a dominant pattern shared by at least 70% of the run. Runs are split where line formulas meet totals, a total that sums its own run is ignored, and a first cell that seeds a recursive pattern (`=B2*(1+g)` style) is expected and ignored.

**Example:** COGS row `=B4*Inputs!$B$5` everywhere except `F5 =F4*0.35`; commission row pointing at `Inputs!$B$7` (rent) in one month.

**Why it matters:** The classic copy-paste slip. One period is calculated differently from the others, and nothing looks broken.

**Fix:** Re-fill the row from a correct cell. If the difference is deliberate (a one-time event in one month), move the event into its own row so the formula stays uniform.

**False positives:** heterogeneous columns (a P&L column where each row is a different line item) are not flagged because no pattern reaches 70%. Genuine one-off formulas in a uniform row will be flagged; that is usually the right call anyway.

## 5. sum_range_omission -- high

**Detects:** a SUM of a single row or column range where numeric cells sit (a) between the range and the SUM cell, (b) in a hole inside a split range (`=SUM(B2:B5,B7:B9)` skipping B6), or (c) directly beyond the far edge of the range, when they look like the summed items (same formula pattern, or typed values like the summed values).

**Example:** Opex rows 7-10 (Rent, Payroll, Commission, Software); `Total opex =SUM(B7:B9)`. Software was inserted at the bottom and the range did not extend.

**Why it matters:** The total is understated and nothing errors. Inserting a row at the edge of a range is the most common way this happens.

**Fix:** Extend the range. Leave a blank spacer row inside the range above the total so future inserts land inside it.

**False positives:** a line deliberately excluded (a memo row). Label it "memo" or move it away from the block.

## 6. total_does_not_foot -- high / hardcoded_total -- medium

**Detects:** a typed number in a row labeled Total/Subtotal (or a column headed Total) compared with the contiguous numbers above it (or to its left). Mismatch is `total_does_not_foot`; a match is still `hardcoded_total`, because it will not update.

**Example:** Commissions `Total bookings 250000` over reps that sum to 253,000.

**Why it matters:** Readers take the total, not the detail. A typed total is the number that ends up in the deck.

**Fix:** Replace with `=SUM(...)`. If the total came from a source system, keep it in a separate "per system" row and add a check row (`=total - SUM(detail)`) that should be zero.

**False positives:** totals that intentionally include items not shown above (label them).

## 7. double_count -- high

**Detects:** a SUM whose range contains a SUM/SUBTOTAL cell that itself sums cells inside the same range.

**Example:** `=SUM(Commissions!D:D)` picks up every rep's commission and the Total row beneath them.

**Why it matters:** The result is exactly double the intended subtotal (or inflated by every nested subtotal), and it looks plausible.

**Fix:** Bound the range to the detail rows, sum only the subtotals (`=B5+B9`), or use `SUBTOTAL(9, ...)`, which ignores other SUBTOTALs in its range.

## 8. stale_cached_value -- high

**Detects:** a simple `=SUM(...)` whose stored value differs from the sum of its stored inputs. Requires cached values.

**Why it matters:** The file was saved in manual calculation mode, or edited by a tool that writes values without recalculating. What people see on screen is not what the formulas say.

**Fix:** Recalculate (F9, or Formulas > Calculation Options > Automatic) and save. Then re-run the audit, because other values moved too.

## 9. external_link -- high

**Detects:** formulas referencing another workbook (`'[Budget FY25.xlsx]Inputs'!B2` or openpyxl's `[1]Inputs!B2` form), and stored external-link definitions no formula uses.

**Why it matters:** The linked file may be moved, renamed, updated, or never sent. Recipients see stale values or a prompt they click past.

**Fix:** Bring the inputs in as values on an Inputs sheet with a source and as-of date, or document the link owner and refresh process. Remove unused links via Data > Edit Links > Break Link.

## 10. hardcoded_in_formula -- medium / low

**Detects:** numeric literals inside formulas, other than 0 and 1 and structural arguments (ROUND digits, VLOOKUP/INDEX column numbers, DATE parts, and similar). Unit conversions (12, 52, 100, 365, 1000...) are low; everything else medium. Formulas that are pure arithmetic on typed numbers (`=1200+350`) are medium.

**Example:** `=F4*0.35`, `=B8*0.02`, `=C10*1.07`.

**Why it matters:** The assumption is invisible, cannot be changed in one place, and cannot be sensitivity-tested. When the rate changes, some copies get updated and some do not -- which then shows up as an inconsistent formula.

**Fix:** Move the number to a labeled input cell or named range and reference it.

**False positives:** true constants (days in a week). Low severity covers the common ones.

## 11. ref_to_empty -- medium

**Detects:** single-cell references to cells that are completely empty, excluding references inside blank-aware functions (IF, ISBLANK, IFERROR, COUNTA, N...).

**Example:** `=Forecast!N4/B3` where the customer count in B3 was never entered.

**Why it matters:** A blank is treated as zero. Usually a reference that slipped when rows were inserted or an input nobody filled in.

**Fix:** Point at the intended input, or fill the input and add a check that it is not blank.

## 12. whole_column_range -- medium / high

**Detects:** `A:A` or `1:1` style ranges. High when the range includes the formula's own column or row on the same sheet.

**Why it matters:** Anything later typed in the column -- a total, a check, a note with a number -- is silently included. It also makes recalculation slow.

**Fix:** Use a bounded range, or convert the data to an Excel Table and use structured references (`=SUM(Sales[Amount])`), which grow with the data without catching totals.

## 13. volatile_function -- medium / low

**Detects:** INDIRECT, OFFSET, RAND, RANDBETWEEN, RANDARRAY (medium); NOW, TODAY, INFO, CELL (low).

**Why it matters:** INDIRECT and OFFSET hide their precedents from every auditing tool, including this one -- anything they point at is outside the dependency graph. RAND makes reported numbers change on every open. TODAY makes the model give different answers on different days.

**Fix:** Replace INDIRECT/OFFSET with INDEX or direct references. Put TODAY() in one labeled as-of cell and reference it. Remove RAND from anything reported, or freeze scenario draws as values.

## 14. hidden_content -- high (veryHidden sheet) / medium / low

**Detects:** hidden or very-hidden sheets, and hidden rows/columns that contain cells, with counts of formulas and of cells feeding visible formulas.

**Example:** hidden row 16 "Manual adj" with 7,500 in April, added into operating income.

**Why it matters:** Plugs and stale overrides live here. Very-hidden sheets can only be unhidden through the VBA editor, so most reviewers never see them.

**Fix:** Unhide, review, delete what is dead, move live inputs into a visible inputs area. If a hidden plug is legitimate, make it a visible, labeled adjustment row.

## 15. percent_as_whole_number -- medium

**Detects:** a typed input in a percent-formatted cell with a value between 1 and 100.

**Example:** Monthly growth `3` formatted as 0.0% displays 300.0% -- someone meant 3%.

**Why it matters:** The model compounds 300% a month. In a busy grid the displayed "300.0%" is easy to miss, and the downstream numbers are just "big".

**Fix:** Enter 0.03. If the model deliberately stores whole-number percentages, format the cell as a number and divide by 100 in formulas, consistently.

## 16. unit_outlier -- low

**Detects:** a typed input in a row of 4+ inputs that is about 90x or more larger or smaller than the row median.

**Example:** Marketing spend 2000 every month except one month entered as 2 (thousands).

**Fix:** Confirm the unit and put the unit in the row label ("Marketing spend ($)").

**False positives:** genuinely lumpy items (an annual insurance payment in one month). Keep it low severity and use judgment.

## 17. mixed_sign_convention -- low

**Detects:** a cost/expense/refund/discount/payroll/rent row whose typed inputs mix positive and negative values, and sheets where some expense rows are all positive and others all negative.

**Why it matters:** Totals that add the lines partially net instead of summing.

**Fix:** Pick one convention for the whole model and state it in a note on the inputs sheet.

## 18. Info-level context

- **cross_sheet_link** -- count of references from each sheet into each other sheet. Use it to see the model's shape and spot a sheet that should not be referenced (a scratch tab feeding the P&L).
- **no_cached_values** -- the file has formulas but no stored results. Value-dependent checks (errors from cache, stale cache, footing of formula-fed totals) were skipped. Re-run with `--recalc` or save in Excel first.

## Manual recalculation with LibreOffice

```bash
soffice --headless --calc --convert-to xlsx --outdir recalculated/ model.xlsx
python3 scripts/audit_xlsx.py recalculated/model.xlsx
```

`--recalc` does the same on a temp copy. LibreOffice calculates missing results on load; results match Excel for standard functions but may differ for the newest Excel-only functions.
