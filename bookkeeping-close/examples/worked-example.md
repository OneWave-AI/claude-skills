# Worked Example: August Close, Business Checking

Synthetic data in `fixtures/`. The business keeps its books in QuickBooks Online on the accrual basis. Inputs:

- `bank_statement.csv`: checking statement export, Aug 1 to Aug 31, 2026. It also contains one July 31 line from an overlapping download (the script drops it as out of period).
- `ledger.csv`: Transaction Detail by Account for checking, exported from Jul 28 (the oldest uncleared item) to Sep 2.
- Statement: beginning 25,000.00, ending 19,586.22.
- Book beginning balance 23,800.00: last month's rec left check 1038 (1,200.00) outstanding, so books were 1,200.00 below the bank.

Planted problems: an outstanding check, a deposit in transit, a payout imported twice, a savings transfer booked to Sales Income, a bank fee and interest missing from the books, a transposed amount, a batched deposit, an uncategorized expense, and a prior-month check clearing.

## 1. Run

```
python scripts/reconcile.py --bank examples/fixtures/bank_statement.csv \
  --ledger examples/fixtures/ledger.csv --period-start 2026-08-01 --period-end 2026-08-31 \
  --statement-begin 25000 --statement-end 19586.22 --book-begin 23800 --out recon/
```

Exit 0. Output (`recon/reconciliation.md`):

```
Statement beginning balance           25,000.00
  + statement lines (net)              -5,413.78
Statement ending balance              19,586.22   rolls forward: yes
  + deposits in transit                 3,400.00
  + outstanding payments (neg)         -1,650.00
Adjusted bank balance                 21,336.22

Book ending balance                   27,480.36
  + items not yet in books                -23.16
  - duplicate book entries             -6,120.80
  + amount corrections                     -0.18
Adjusted book balance                 21,336.22

UNEXPLAINED VARIANCE                       0.00   BALANCED
```

Matched: 9 exact, 2 by check number (1038 from July, 1041), 1 fuzzy (fuel, 0.18 off), 1 grouped (a 3,775.50 bank deposit = two customer checks).

Exceptions raised: the Stripe payout pairing was ambiguous because the ledger held it twice; the savings transfer in is categorized to Sales Income; Google Workspace sits in Uncategorized Expense.

## 2. Interpret

- **Balanced does not mean correct.** The rec balances only after the book-side corrections below are made. Until they are posted, the QBO reconcile screen will not reach 0.00, and it should not.
- **Duplicate payout (6,120.80)** overstates cash, and leaves Undeposited Funds negative (or revenue overstated, depending on the original split). The feed match and a CSV upload both added it. Remove the one not linked to the feed match.
- **Transfer from savings (2,000.00) in Sales Income** overstates revenue by 2,000.00. It matches the bank, so a pure rec would never catch it; the category check did.
- **Fuel 87.46 vs 87.64**: difference 0.18 is divisible by 9, a transposition. Correct the entry to the receipt.
- **Check 1044 and the Birchwood deposit** are timing. Carry them to September and confirm they clear.
- **Card payment (2,340.12)** is correctly posted to the card liability; no action.
- **Stripe payouts** are net of processing fees. Confirm the processor clearing account records gross sales and fees (checklist section 2).

## 3. Close package (excerpt)

**Reconciliation summary: Checking, Aug 31 2026.** Balanced after proposed corrections 1, 3, 4 and 5 (entry 2 is a reclass that does not touch cash). Unexplained variance 0.00. Savings, the card, and the processor clearing account are reconciled separately; the card statement was not provided and is marked not verified.

**Reconciling items carried forward**

| Date | Item | Amount | Age | Status |
|---|---|---:|---:|---|
| 2026-08-29 | Check 1044 Ortiz Electrical | -1,650.00 | 2 days | Outstanding, confirm in September |
| 2026-08-31 | Deposit, Birchwood | 3,400.00 | 0 days | In transit, confirm in September |

**Review queue**

| Date | Description | Amount | Current | Proposed | Confidence | Reason |
|---|---|---:|---|---|---|---|
| 2026-08-29 | Google Workspace | -72.00 | Uncategorized Expense | Software and Subscriptions | medium | pattern: SaaS vendor; no history |

**Proposed adjusting entries: FOR ACCOUNTANT REVIEW, not posted**

| # | Date | Debit | Credit | Amount | Memo | Evidence |
|---|---|---|---|---:|---|---|
| 1 | 08-18 | Undeposited Funds (original split) | Checking | 6,120.80 | Remove duplicate Stripe payout L0011 | One bank line B0010, two ledger lines |
| 2 | 08-22 | Sales Income | Savings 4821 | 2,000.00 | Reclass transfer from savings out of revenue | Bank: ONLINE TRANSFER FROM SAVINGS |
| 3 | 08-31 | Bank Service Charges | Checking | 25.00 | August monthly service fee | Statement line B0015 |
| 4 | 08-31 | Checking | Interest Income | 1.84 | August interest | Statement line B0016 |
| 5 | 08-14 | Vehicle: Fuel | Checking | 0.18 | Correct fuel entry 87.46 to 87.64 | Statement 87.64; transposition |

Entry 1 is best done by deleting the duplicate transaction rather than posting an offset, so the audit trail shows one payout. Entry 5 is an edit to the original transaction, shown as an entry for the reviewer.

**Accountant questions**
- None tax-sensitive this month. Check 1044 to an individual contractor: confirm year-end information reporting status is tracked.

**Checklist status**: cash (checking) done; card not done (statement missing); AR/AP tie-out done; payroll clearing done; accruals not applicable (none identified); lock period pending sign-off.

## 4. Failure modes the fixtures test

`bash examples/run_fixtures.sh` runs the base case plus three variants:

| Variant | Result |
|---|---|
| Ledger exported with every sign inverted | Detected (12 vs 0 amount hits), flipped, balanced, noted in output |
| Book beginning balance typed 50.00 high | Exit 2, `UNEXPLAINED VARIANCE -50.00 NOT BALANCED - do not plug, investigate` |
| Statement export missing one line | Exit 3 before matching: lines roll to 19,658.22, statement says 19,586.22, gap -72.00 |
