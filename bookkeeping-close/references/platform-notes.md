# Platform Notes: QuickBooks Online, Xero, Bank Files, Mercury

## Contents
1. What any connector can and cannot do
2. QuickBooks Online
3. Xero
4. Bank CSV and OFX
5. Mercury
6. Sign convention cheat sheet

## 1. What any connector can and cannot do

Neither accounting API can complete a reconciliation. The QuickBooks Online API has no endpoint to reconcile or mark transactions cleared, and it cannot read or post to the bank-feed For Review list. Xero states that it does not support reconciling bank statement lines through the Accounting API, and unreconciled statement lines are not exposed through public APIs. So: pull data through connectors, do the analysis here, and have the user click through the final reconciliation in the product using the match list from `reconcile.py`.

Connector write actions (creating transactions, journal entries, rules) change the books. Propose them in the close package and create them only after the user explicitly approves each one. Never post adjusting entries on your own.

When a connector is attached, list its tools first and use the read tools that return transactions for one account and date range. If the connector cannot return what is needed, ask for an export instead of approximating.

## 2. QuickBooks Online

**Exports to request**
- Ledger for one account: Reports > Transaction Detail by Account (filter to the account, date range from oldest uncleared item to period end), or the account register export. Columns typically: Date, Transaction Type, Num, Name, Memo/Description, Split, Amount, Balance. `Split` is the offsetting account and is what to check for miscategorized transfers.
- Prior reconciliations: Reconcile > History by account. Use the last reconciled ending balance as this period's beginning balance.
- Chart of accounts: Chart of accounts > Run report, export.
- Bank rules: Transactions > Rules (export available).

**Upload format** (for statement lines QBO has not received through the feed): CSV in a 3-column layout (Date, Description, Amount) or a 4-column layout (Date, Description, Credit, Debit). Money out negative, money in positive in the 3-column form. Use one date format throughout. Limits: up to 1,000 lines and 350 KB per file. Card exports from some issuers come with the opposite sign, which uploads charges as payments; check a known charge before uploading. Uploading a file that overlaps the feed creates duplicates.

**Reconcile behavior**
- The reconcile screen needs the statement ending date and ending balance, and the goal is a Difference of 0.00.
- "Beginning balance is off" means a previously reconciled transaction was edited, deleted, voided, moved, or unreconciled, or a feed match was undone. Use the discrepancy report ("We can help you fix it"), which shows what changed, when, and by whom. Fix that before reconciling the new period; do not carry the error forward.
- Non-zero ending difference: QBO lists incorrect ending balance entered, transactions entered that have not cleared, missing or duplicate transactions, bank-combined payments that need grouping, and small amount differences such as bank fees.
- QBO offers an adjusting entry at finish to force a match, posted to a Reconciliation Discrepancies account. Intuit calls it a last resort for small amounts and warns it can cause accounting issues. This skill does not propose it; it lists the variance instead.
- Undeposited Funds: customer payments sit here until grouped into a bank deposit that matches the bank line. A batched deposit that was never grouped shows as separate unmatched receipts.
- Close the books: Settings > Account and settings > Advanced > Accounting > Close the books, with a closing date and optional password.
- Bank rules: up to 5 conditions per rule on description, bank text, or amount; applied in priority order; auto-add confirms matching transactions without review, so reserve it for unambiguous vendors.

## 3. Xero

**Exports to request**
- Ledger for one account: Accounting > Reports > Account Transactions (select the bank account), export to CSV/Excel.
- Statement lines: Bank account > Bank Statements (shows imported lines, including deleted ones).
- Bank Reconciliation Summary for the period end date: shows Balance in Xero and Statement balance (calculated); enter the actual statement ending balance and it shows the amount the calculated balance is out by. Bank Reconciliation Detail lists outstanding items.

**CSV statement import**: Date and Amount are the only required fields. Amounts in one column, income positive, expenses negative (minus sign or brackets). Optional Payee, Description, Reference help matching; Payee should match the contact name exactly to avoid new duplicate contacts. A precoded CSV can also carry account code and tax rate.

**Quirks**
- Duplicates: Xero has a duplicate statement lines report and a Statement Exceptions report in the bank reconciliation report pack. Deleting a statement line never removes it permanently; it stays on the statement and can be restored. Deleting requires an admin or standard + bank accounts role. If a whole statement was imported twice, delete the statement.
- Transfers between own accounts: create the transfer in one account only; Xero creates the other side, and you reconcile each side with OK. Creating it in both accounts duplicates it.
- Bank rules are checked in the order listed; put the most restrictive first. Rules suggest; automatic bank reconciliation (a per-account setting) reconciles only lines meeting high-confidence criteria. Review what it did before closing.
- Reconcile a period and close it, and set lock dates (an adviser role) after sign-off so reconciled transactions cannot be changed.
- API fields when reading through a connector: BankTransactions carry `IsReconciled`; BankTransfers carry `FromIsReconciled` and `ToIsReconciled`. These say what is reconciled; they cannot change it.

## 4. Bank CSV and OFX

- Bank CSVs vary: one signed Amount column, or Debit/Credit (or Withdrawal/Deposit) pairs. On a statement, Debit means money out. `reconcile.py` detects both.
- Some card exports show charges positive, others negative. The statement roll-forward check in `reconcile.py` detects and fixes an inverted file.
- Running-balance columns are useful: the last row's balance should equal the statement ending balance.
- Downloads covering overlapping date ranges, once combined, create duplicates. Deduplicate before reconciling.
- OFX/QFX: each `<STMTTRN>` has `DTPOSTED`, a signed `TRNAMT` (from the account holder's view), `FITID` (unique per transaction within the account), and `NAME`/`MEMO`. `LEDGERBAL` gives the closing balance. Deduplicate on FITID. To convert for the script:

```python
import re, csv
txt = open("statement.ofx", encoding="latin-1").read()
rows = []
for t in re.findall(r"<STMTTRN>(.*?)</STMTTRN>", txt, re.S):
    g = lambda k: (re.search(rf"<{k}>([^<\r\n]*)", t) or [None, ""])[1].strip()
    rows.append({"Date": g("DTPOSTED")[:8], "Description": g("NAME") or g("MEMO"),
                 "Amount": g("TRNAMT"), "FITID": g("FITID")})
rows = list({r["FITID"]: r for r in rows}.values())  # drop repeated FITIDs
with open("statement.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
```
Run the script with `--date-format %Y%m%d` for this output.

## 5. Mercury

- Transactions (connector `listTransactions` or API `/transactions`): `amount` is negative for debits and positive for credits, which is the normalized convention already.
- `status` is one of pending, sent, cancelled, failed, reversed, blocked. Reconcile only posted money movement: use `sent` lines with a `postedAt` inside the period. Exclude pending (not on the statement yet), and cancelled/failed/blocked (never moved). A reversed item may appear with its reversal; keep both if both posted.
- Use `postedAt` for statement matching, not `createdAt`; they can differ by days.
- `kind` identifies `internalTransfer` (between Mercury accounts: balance-sheet transfer), card transactions, wires, fees, and interest.
- Statement balances: `getAccountStatements` for the period. Account-level balance endpoints give the current balance, not the balance at period end.
- `counterpartyName` is the cleanest description field for matching and categorization. Mercury's own categories (`categoryData`) are a hint, not the business's chart of accounts.

## 6. Sign convention cheat sheet

| Source | Money into a bank account appears as |
|---|---|
| Bank statement Amount column | positive |
| Bank statement Debit/Credit columns | Credit |
| QBO register / Transaction Detail by Account (bank) | positive Amount, or Deposit column |
| General ledger Debit/Credit columns (bank = asset) | Debit |
| Xero statement CSV | positive |
| Mercury API | positive |
| OFX TRNAMT | positive |

For a credit card (a liability), a charge increases the balance owed: positive on most card statements, Credit in a general ledger. Pass `--account-type card` to `reconcile.py`.
