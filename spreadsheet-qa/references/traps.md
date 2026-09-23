# Data traps in business exports

Each trap: what it looks like, how profile.py flags it, and the fix. Every one of these produces a confident, wrong number with no error message.

## Join fan-out (double counting after a join)

- Looks like: revenue by segment adds up to more than total revenue. The lookup table (customers, products, reps) has two rows for one key, so every order for that key is duplicated.
- Caught by: profile.py "Join risks" (FAN-OUT verdict with the number of extra rows), and ask.py `kind: "join"` steps, which fail the run when the row count grows.
- Fix: dedupe the lookup side first (`row_number() OVER (PARTITION BY key ORDER BY updated_at DESC) = 1`), or aggregate the many side before joining (refunds per order, then join). Then reconcile: the grouped total must equal the ungrouped total.
- Related: a many-to-many join on a non-key (name, email, date) multiplies both sides. Join on IDs.
- The opposite failure: an inner join silently drops orders whose customer is missing from the customer export. ask.py warns when a join shrinks rows. Default to LEFT JOIN and count the NULLs.

## Embedded totals, subtotals, and footers

- Looks like: a "Grand Total", "Total", or "Subtotal" row at the bottom or after each group, or report footers ("Filtered by: Region = West", "Generated on ..."). SUM on the column exactly doubles the answer.
- Caught by: profile.py matches total/footer labels and also finds unlabelled rows whose value equals the sum of all other rows in that column.
- Fix: exclude the rows in a `clean` step and show the row count drop in the evidence. Then use the export's own total as a reconciliation target: your parsed sum must equal it.

## Header not on row 1

- Looks like: a title, date range, or logo row above the column names. Loaded naively, the header becomes the first data row and every column is text.
- Caught by: profile.py `header_row`.
- Fix: pass `"header_row": N` for that table in the ask.py spec.

## Excel dates as serial numbers

- Looks like: 45292 in a date column. Excel stores dates as days since 1899-12-30. CSVs exported from Excel often keep the serial.
- Caught by: profile.py flags integers from 20000 to 60000 in a date-named column and prints the converted range.
- Fix: `excel_date(col)` in ask.py (or `DATE '1899-12-30' + CAST(col AS INTEGER)`). Workbooks from old Macs may use the 1904 system (serials 1462 days smaller); if the converted dates land four years early, that is why.

## Numbers stored as text

- Looks like: "$1,200.00", "1 200,00", "(35.00)", "12%", "1.2K", or leading apostrophes. Auto-typing either makes the column text (so SUM skips it or errors) or parses some rows and nulls others.
- Caught by: profile.py "numbers stored as text" and "mixed column" flags, with examples.
- Fix: `to_num(col)` in a clean step, plus an `assert_zero` check that no non-empty value failed to parse. Parentheses mean negative in accounting exports. European formats ("1.234,56") need an explicit swap before to_num; check for a comma as the decimal separator when values have exactly two digits after a comma.
- Also: leading-zero codes (ZIP 02134, SKU 0012) must stay text. ask.py loads everything as text for this reason.

## Currency mixing

- Looks like: one `amount` column with a `currency` column next to it holding USD, EUR, GBP. Or symbols inside the values. Summing gives a number in no currency.
- Caught by: profile.py "currency column holds N currencies" and "mixed currency markers".
- Fix: convert with an explicit rate table in a join step and assert every row matched a rate. State the rate basis in the answer (fixed, month-average, or transaction-date). If no rates exist, report per currency and say you did not convert.
- Stripe amounts are in minor units (cents). Zero-decimal currencies (JPY, KRW) are not.

## Timezone day boundaries

- Looks like: timestamps ending in Z or +00:00 (Stripe, Shopify API, most ad platforms export UTC), while the business thinks in local days. An order at 02:30 UTC on Aug 1 is July 31 in New York. Month and quarter totals shift at the edges.
- Caught by: profile.py timezone note and the data dictionary open question.
- Fix: decide the reporting zone (default: UTC when the data is UTC and the user has not said otherwise, and state it). Convert with `CAST(ts AS TIMESTAMPTZ) AT TIME ZONE 'America/New_York'` before bucketing. Naive timestamps with no zone: ask what zone the export uses; Shopify admin exports use the store's zone, while many CRMs export the exporting user's zone.
- Daylight saving: never add a fixed offset by hand; use a named zone.

## Filtered views exported

- Looks like: the user's number came from a filtered on-screen view ("my dashboard says 412") and the export has everything, or the export itself was made from a filtered report (footer text "Filtered by", or suspiciously round ranges).
- Caught by: profile.py autofilter flag on xlsx and footer-text detection.
- Fix: ask which filters their reference number uses before calling a mismatch an error. Show the filters you applied, one per step, with row counts.

## Hidden rows, columns, and sheets

- Looks like: rows hidden in Excel (often excluded or "old" items) still read by pandas. Hidden sheets with lookup tables or stale copies.
- Caught by: profile.py `hidden_rows`, `hidden_columns`, `sheet_state`.
- Fix: default to include hidden rows and say so. Ask when hidden rows look like the difference between your number and theirs.

## Merged cells

- Looks like: a group label merged down several rows, so only the first row has a value and the rest are blank.
- Caught by: profile.py `merged_ranges`.
- Fix: forward-fill the label column in a clean step (`last_value(col IGNORE NULLS) OVER (ORDER BY row_number)`), after confirming the order is the sheet order.

## Duplicate records

- Looks like: the same order twice because two monthly exports overlapped, or the same customer under two IDs.
- Caught by: profile.py `exact_duplicate_rows` and duplicate-key reports.
- Fix: dedupe on the business key, not all columns, and report how many rows were removed. For combining several files first, use the `csv-excel-merger` skill.

## Snapshot vs event tables

- Looks like: a subscriptions export with one row per subscription per month, or a pipeline export with one row per stage change. Summing across rows counts the same thing many times.
- Caught by: the grain check. If the candidate key is (id, date) rather than id, the table is a snapshot or event log.
- Fix: take the latest row per id for point-in-time questions, and sum only for flows (payments, orders).

## Rates and averages

- Averaging per-row rates (CTR, margin %, conversion %) weights a 10-click row the same as a 10,000-click row. Recompute the rate from summed numerator and denominator.
- Averages of averages across groups of different sizes: same problem.

## Status and lifecycle fields

- Test orders, internal accounts, $0 orders, voided invoices, draft invoices, and deleted records often sit in the export with a status flag. List the distinct status values (profile.py top_values) and say which ones you included.
