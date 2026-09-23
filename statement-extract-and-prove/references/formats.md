# Statement formats, sign conventions and number formats

## Contents
- Layout families
- Sign conventions
- Number formats by locale
- Date formats
- Page furniture
- Brokerage statements
- Invoices and vendor price lists
- Known traps and which check catches them

## Layout families

| Layout | Columns | What the extractor does | Proof strength |
|---|---|---|---|
| Signed amount + running balance | Date, Description, Amount, Balance | sign as printed: `-`, `( )`, trailing `-`, CR/DR | strongest: every row is checked |
| Debit / credit + running balance | Date, Description, Withdrawals / Deposits (Paid out / Paid in, Money out / Money in, Soll / Haben), Balance | bank: credit - debit; card: debit - credit | strongest |
| Balance once per day | same, balance only on the last row of each date | rows without a balance accumulate until the next printed balance | strong: a break names the span, and the one-row tests name the row |
| No running balance | Date, Description, Amount | tie-out, summary totals and counts only | weaker: a missing row plus an extra row of the same size cancel out, so check counts |
| Card statement | Trans date, Post date, Description, Amount | two date columns: second becomes `post_date` | tie-out against Previous / New balance and the Payments / Purchases boxes |
| Newest first | any of the above, dates descending | prove.py detects descending dates and walks the chain in reverse | same as the layout |

Header detection wants a line with a date column, at least one amount-type column and three recognized headings. Headings are matched as whole phrases (English, German, French, Spanish vocabulary in `ROLE_PATTERNS`). When a bank uses a heading the vocabulary does not know, or prints the header only on page 1, bands carry over from the previous page. If there is no header anywhere, supply `--bands` yourself.

## Sign conventions

Output convention: `amount` is the signed change to the balance the statement reports.

- **Bank / deposit accounts**: deposits and credits positive, withdrawals and debits negative. A `CR` suffix means in credit (positive), `DR` means overdrawn or a debit (negative). German `H` (Haben) is credit, `S` (Soll) is debit.
- **Credit cards** (`--account-type card`): purchases, fees and interest positive (they raise the balance owed), payments and refunds negative. On a card statement `CR` marks a credit to the cardholder, so it comes out negative.
- **Parentheses** `(1,234.56)`, a leading `-`, a trailing `-` (`1.234,56-`), and the Unicode minus `−` are all negative.
- **Directional columns hold magnitudes**. A negative number inside a Withdrawals column is a reversal. The extractor keeps the arithmetic (`-(-x)` = money in) and flags `negative_in_directional_column`.
- **"Debit" is ambiguous across documents**. On a bank statement it means money out. In a general ledger it means money into a cash account. This skill only reads statements; `bookkeeping-close` handles the ledger side.
- **The whole statement's signs are inverted** when the tie-out gap is exactly `-2 x sum` or when every running balance breaks by twice its row's amount. Check `--account-type` first, then `--invert-amount`.

## Number formats by locale

| Style | Example | Where | Flag |
|---|---|---|---|
| Dot decimal, comma thousands | 1,234.56 | US, UK, AU, CA (en), (Indian lakh grouping 1,23,456.78 is not recognized as an amount: those rows come out with no amount and the proof fails) | `--decimal dot` |
| Comma decimal, dot thousands | 1.234,56 | DE, NL, ES, IT, BR, most of EU | `--decimal comma` |
| Comma decimal, space thousands | 1 234,56 (often a narrow no-break space) | FR, SE, NO, FI, PL, CZ | `--decimal comma` |
| Apostrophe thousands | 1'234.56 | CH | `--decimal dot` |
| No decimals | 1,234 | JPY, KRW, some price lists | `--allow-integers` |

Detection: auto mode counts amounts in the numeric columns ending `.dd` against `,dd`. Mixed evidence (over 10% minority) stops with exit 2 so that nobody guesses. Per token, a two-digit tail after the non-decimal separator is flagged `locale_conflict`, and thousands groups that are not 3 digits are flagged `bad_grouping`. Both make prove.py fail its number-format check, because a document-wide separator error multiplies every figure by the same factor and still ties out.

Split numbers: PDF text often breaks `1 234,56` or `$ 12.00` or `12.00 CR` into separate words. The extractor rejoins tokens separated by less than about one character width.

## Date formats

- Numeric: `MM/DD/YYYY`, `MM/DD/YY`, `MM/DD`, `DD/MM/YYYY`, `DD.MM.YYYY`, `DD.MM.`, `YYYY-MM-DD`.
- Text: `05 Jan`, `05 Jan 26`, `Jan 5, 2026`, `5. März 2026`, `5 janv. 2026`.
- Day/month order: auto mode proves it from any value above 12. If none exists (all dates day 1-12), it assumes `dmy` for comma-decimal documents and `mdy` otherwise, and warns. A wrong guess shows up as dates outside the statement period. Pass `--date-order` when the statement shows no day above 12.
- Missing year: taken from the statement period, and a December date in a Dec-Jan statement gets the earlier year. Without a period line, pass `--year`.
- Dates printed once per day: rows without a date inherit the previous one (`date_inherited`, informational).

## Page furniture

Handled explicitly, never turned into transactions:
- Page headers above the column header, and repeated column headers on later pages.
- Footers: `Page n of m`, `Seite n von m`, `continued`, FDIC lines.
- Balance brought forward / carried forward / Übertrag / Saldo Vortrag / Solde reporté lines: recorded as markers and used for the page-continuity check. A bare "forward" line above the first row of a page counts as brought forward.
- Closing balance lines and Total / Summe rows: recorded, and they end the table on that page. Lines after that are logged as unassigned.
- Summary boxes (Beginning / Ending balance, Deposits and other credits (n), Withdrawals and other debits (n), Number of transactions, Summe Soll / Haben, Total paid in / out) are parsed into `meta.summary`, including counts in parentheses.

Anything inside the table region that did not become a row is written to `meta.unassigned_lines` along with the reason. Unassigned lines that contain an amount are flagged in the proof, since they are the usual place a dropped row turns up.

## Brokerage statements

Use the activity / transactions section, where cash balance works like a bank balance: opening cash + activity = closing cash. Holdings tables do not tie by rows. Instead, check quantity x price = market value per line (within rounding) and that the sum of market values equals the stated total. Do that with a short script on the extracted rows, using `--allow-integers` for share quantities. Trade confirms: gross + fees + commissions = net.

## Invoices and vendor price lists

- Invoice lines: quantity x unit price = line amount, sum of lines = subtotal, subtotal + tax + shipping - discount = total. These replace the running balance as the proof.
- Price lists: no totals, so the proof is the row count (compare to the item numbering or the last SKU), no unassigned lines containing prices, and every price parsing cleanly. Unit prices with three decimals (`0,125`, `1.125`) are exactly where auto detection is weakest, since `1.125` is 1125 in German and 1.125 in English. Always pass `--decimal` for price lists, and `--allow-integers` when prices have no cents.
- Header fields (vendor, invoice number, due date) belong to `financial-parser`.

## Known traps and which check catches them

| Failure | Caught by |
|---|---|
| Dropped row on a long table or at a page break | running-balance break with the gap equal to the missing amount; counts; per-page sum |
| Row duplicated across a page break | duplicates; "EXTRA" diagnosis |
| Sign flipped on one row | running-balance break equal to twice the amount, "WRONG SIGN" |
| All signs flipped | tie-out gap = -2 x sum; every balance breaks |
| Comma read as decimal on one row | power-of-ten diagnosis; `locale_conflict` |
| Comma read as decimal on every row | number-format check (tie-out still passes) |
| Invented number (visual reading) | any invariant; plus visual rows are marked |
| Subtotal read as a transaction | "EXTRA" diagnosis; summary totals |
| Amount column drifted on one page | "NO AMOUNT" rows on that page; fix with `--bands --band-pages` |
| Wrong day/month order | period check (warn); dates out of order |
