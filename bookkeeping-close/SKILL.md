---
name: bookkeeping-close
description: Runs small and midsize business bookkeeping operations - categorizes bank and card transactions to a chart of accounts, reconciles a bank or card statement against the ledger, works a month-end close checklist, and produces a close package for the accountant. Works from QuickBooks Online, Xero, bank CSV/OFX, or Mercury exports, and from the Xero, QuickBooks, or Mercury connectors when present. Use it whenever the user says "reconcile", "bank rec", "categorize transactions", "month end close", "close the books", "books don't match the bank", "reconciliation is off by", "uncategorized expenses", or shares a QuickBooks or Xero export or a bank statement CSV, even if they do not name the task. Never plugs a difference; every unreconciled dollar is explained or listed.
---

# Bookkeeping Close

A reconciliation proves that the books and the bank agree once timing is accounted for. Models get this wrong in predictable ways: they flip signs, treat an uncleared check as an error, count a transfer between the business's own accounts as income, miss a transaction imported twice, and force the rec to zero with an adjustment. This skill exists to prevent each of those. The deterministic matching lives in `scripts/reconcile.py`; the judgment lives here.

Scope: bookkeeping, not tax. When an item has a tax consequence (capitalize vs expense, owner draws vs wages, sales tax, 1099 status, meals deductibility), record the bookkeeping fact and put it on the accountant list. Do not give tax advice.

## Inputs to collect

For each account being reconciled (checking, savings, each credit card, loan, payment processor clearing):

1. Statement for the period: ending date, beginning balance, ending balance. Take the balances from the statement itself, not from the feed, because feeds can be incomplete.
2. Statement lines: bank CSV/OFX, Mercury export or `listTransactions`, or the platform's statement lines.
3. Ledger for the same account: QBO register or Transaction Detail by Account, Xero Account Transactions. Export from the date of the oldest uncleared item, not the period start, so prior-period outstanding checks can clear.
4. Book balance at period start or end for that account.
5. Chart of accounts, and any existing bank rules.

See `references/platform-notes.md` for export paths, column formats, and connector limits. Neither the QuickBooks Online API nor the Xero Accounting API can mark items reconciled; reconciliation is always finished inside the product.

## Workflow

### 1. Normalize

Convert every file to one convention: amount is the signed change to the balance the statement reports. For a bank account, deposits positive. For a card, charges positive. Watch the word "debit": on a bank statement it means money out, in a general ledger it means money into a cash account. `reconcile.py` handles both and prints which reading it used. Confirm dates are parsed in the right day/month order before trusting anything.

### 2. Prove the statement first

Beginning balance plus statement lines must equal ending balance. If it does not, the export is incomplete, overlaps another period, or contains a duplicated download. Stop and fix the input. Matching against a broken statement produces a rec that balances to the wrong number.

### 3. Match and classify

Run:

```
python scripts/reconcile.py --bank bank.csv --ledger ledger.csv \
  --period-start YYYY-MM-DD --period-end YYYY-MM-DD \
  --statement-begin N --statement-end N --book-begin N --out recon/
```

It matches in tiers (exact, check number, same amount within a date window, near amount with similar description, one-to-many for batched deposits) and classifies everything left over. Read its notes: it reports when it inverted a file's signs. Exit 0 = balanced, 2 = unexplained variance, 3 = statement does not roll forward.

Interpret the results with these rules:

- **Outstanding payments and deposits in transit** are timing, not errors. They adjust the bank side. Confirm they clear on next month's statement; anything older than 90 days is stale and goes to the accountant list (void, reissue, or unclaimed property).
- **Duplicates** adjust the book side. The common cause is the same transaction arriving through the bank feed and a CSV upload or manual entry. Delete one only after confirming against the statement; two identical real purchases on one day do happen.
- **Transfers between own accounts** and **credit card payments** belong on the balance sheet. If either leg is categorized to income or expense, revenue or expense is double counted. Record the transfer once; in Xero, creating it in one account creates the other leg.
- **Batched deposits**: one bank deposit often equals several customer payments. Group them (QBO: Undeposited Funds / bank deposit; Xero: match multiple).
- **Near-amount matches** are errors on one side, usually the book. A difference divisible by 9 suggests transposed digits. Correct the entry to the source document.
- **Statement lines not in the books** (fees, interest, unrecorded charges) need entries. Find the source document when one should exist.

### 4. Never plug

If the adjusted bank and adjusted book balances still differ, report the variance with what was ruled out. Do not create a "reconciliation discrepancy" or suspense entry to force zero. QuickBooks describes its adjusting entry as a last resort for small amounts only, and it hides the underlying error. If the user insists on an adjustment, list it as a proposed entry for accountant approval, with the amount and the investigation done.

Common causes to check, in order: wrong beginning balance (a previously reconciled item was edited or deleted), wrong statement balance typed in, a line outside the date range, a sign flip on a single line, a duplicate, a transfer recorded twice, a split transaction entered as the gross amount.

### 5. Categorize

Apply `references/categorization-rules.md`: existing bank rules first, then vendor patterns, then history. Every categorization carries a confidence: `high` (rule or consistent history), `medium` (pattern match only), `low` (guess). Only `high` is posted without review. Items in Uncategorized, Ask My Accountant, or suspense are never left there at close.

### 6. Work the close checklist

Follow `references/close-checklist.md`. Short version: all accounts reconciled including cards, loans, and processor clearing; AR and AP aging tie to the balance sheet; payroll liabilities tie; undeposited funds cleared; accruals and prepaids posted; fixed asset additions flagged; balance sheet reviewed line by line; P&L compared to prior month and prior year; period locked only after the accountant signs off.

## Output: the close package

Produce one document per period, in this order:

1. **Reconciliation summary** per account: the two-sided proof from `reconciliation.md`, balanced or not, with unexplained variance stated in dollars.
2. **Reconciling items**: outstanding payments, deposits in transit, stale items, with dates and ages.
3. **Review queue**: uncategorized and low/medium confidence items with the proposed account and the reason. Include amounts so the owner can prioritize.
4. **Proposed adjusting entries**, each marked `FOR ACCOUNTANT REVIEW` and never posted by this skill: date, debit account, credit account, amount, memo, evidence. Examples: record bank fee, remove duplicate, reclass transfer out of income, accrue unbilled expense.
5. **Accountant questions**: tax-sensitive items, stale checks, owner transactions, anything needing judgment.
6. **Checklist status**: each close step done, not done, or not applicable.

State plainly what was not verified (for example, "loan statement not provided, loan balance not reconciled").

See `examples/worked-example.md` for a full run on the bundled fixtures.
