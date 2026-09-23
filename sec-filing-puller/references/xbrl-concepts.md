# Curated XBRL concepts and known pitfalls

This is the mapping `sec_pull.py` uses (the `METRICS` dict). Tags are listed in fallback order. The output always names the tag that produced each number, so check it against the definition below before you compare companies.

## Metric map

| Metric key | Tags, in fallback order | Kind | Strategy |
|---|---|---|---|
| `revenue` | us-gaap: Revenues, RevenueFromContractWithCustomerExcludingAssessedTax, RevenueFromContractWithCustomerIncludingAssessedTax, SalesRevenueNet, SalesRevenueGoodsNet, SalesRevenueServicesNet, RevenuesNetOfInterestExpense, RegulatedAndUnregulatedOperatingRevenue; ifrs-full: Revenue | duration, additive | **max** per period (ties go to the tag used most often) |
| `gross_profit` | GrossProfit | duration, additive | priority |
| `operating_income` | OperatingIncomeLoss; ifrs ProfitLossFromOperatingActivities | duration, additive | priority |
| `net_income` | NetIncomeLoss, NetIncomeLossAvailableToCommonStockholdersBasic, ProfitLoss; ifrs ProfitLossAttributableToOwnersOfParent, ProfitLoss | duration, additive | priority |
| `eps_diluted` | EarningsPerShareDiluted, EarningsPerShareBasicAndDiluted, IncomeLossFromContinuingOperationsPerDilutedShare; ifrs DilutedEarningsLossPerShare | duration, **not additive** | priority |
| `diluted_shares` | WeightedAverageNumberOfDilutedSharesOutstanding | duration, not additive | priority |
| `operating_cash_flow` | NetCashProvidedByUsedInOperatingActivities, ...ContinuingOperations; ifrs CashFlowsFromUsedInOperatingActivities | duration, additive | priority |
| `capex` | PaymentsToAcquirePropertyPlantAndEquipment, PaymentsToAcquireProductiveAssets, PaymentsForCapitalImprovements; ifrs PurchaseOfPropertyPlantAndEquipment... | duration, additive | priority |
| `total_assets` | Assets | instant | priority |
| `cash` | CashAndCashEquivalentsAtCarryingValue, CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents, Cash | instant | priority |
| `lt_debt_noncurrent` | LongTermDebtNoncurrent, LongTermDebtAndCapitalLeaseObligations | instant | priority |
| `lt_debt_current` | LongTermDebtCurrent, LongTermDebtAndCapitalLeaseObligationsCurrent | instant | priority |
| `short_term_borrowings` | CommercialPaper, ShortTermBorrowings, OtherShortTermBorrowings | instant | priority |
| `shares_outstanding` | CommonStockSharesOutstanding, then dei:EntityCommonStockSharesOutstanding | instant | priority |

To add a metric, add an entry to `METRICS` in `scripts/sec_pull.py`. Run `sec_pull.py tags TICKER --grep <word>` first to see which tags the company actually files, and over what dates.

## Pitfalls by metric

### Revenue
- **Companies switch tags over time.** SalesRevenueNet was deprecated in 2018 when ASC 606 arrived, and most filers moved to RevenueFromContractWithCustomerExcludingAssessedTax. Apple used SalesRevenueNet through FY2018, then switched. The script picks a tag per period and adds a "Tag differs across periods" note when the tag changes.
- **Total revenue vs net sales.** Walmart files both `Revenues` ($713,163M FY2026, total revenues including membership and other income) and `RevenueFromContract...` ($706,413M, net sales). The max rule picks the total, which matches the "Total revenues" line in the 10-K, and puts the other figure in the notes. When comparing companies, confirm that every company's number is the same concept.
- **Banks** file RevenuesNetOfInterestExpense (total net revenue), and some also file `Revenues` for the same number. Interest income alone is not revenue.
- **Excise and sales taxes**: "Including assessed tax" (tobacco, fuel) can be much larger than "excluding". Name which one you are showing.

### Net income
- NetIncomeLoss is the amount attributable to the parent. ProfitLoss includes noncontrolling interests: Walmart's consolidated $22,270M vs $21,893M attributable to Walmart. The script prefers NetIncomeLoss and lists ProfitLoss as an alternative.
- Net income available to common stockholders comes after preferred dividends. It is the numerator of EPS, not headline net income.

### EPS
- **Never add or subtract EPS across periods.** The share count differs every quarter, so FY EPS does not equal the sum of the quarterly EPS figures. The script never derives Q4 EPS or TTM EPS. A missing Q4 EPS comes out as "not derivable". Take it from the earnings release (an 8-K exhibit), and from the 10-K's quarterly data note where one still exists.
- Some filers tag EPS with the unit `pure` by mistake (Walmart, 2009-2010). The script only reads `USD/shares`, or `<CUR>/shares` for foreign filers.
- Stock splits: past EPS and share counts are restated in later filings. The latest-filed value is split-adjusted and the original value is not. Look at `original_value` before charting a long history.

### Share counts
- `dei:EntityCommonStockSharesOutstanding` is the cover-page count, dated a few weeks after period end. Walmart has no balance-sheet share tag after 2012, so the script falls back to the cover count and labels its date.
- Multi-class issuers file class-level counts with dimensions, and those are not in companyfacts. The entity-level count may be missing or may cover only one class. Read the cover page.
- Use weighted average diluted shares for per-share maths over a period, and period-end outstanding shares for market cap.

### Cash, debt
- CashCashEquivalentsRestrictedCash... is the cash-flow statement total, which includes restricted cash. It is larger than balance-sheet cash (Apple FY2023: $30,737M vs $29,965M).
- Total debt is not one tag. Approximate it as `lt_debt_noncurrent + lt_debt_current + short_term_borrowings`, then check the debt footnote. Leases are excluded unless the tag says CapitalLeaseObligations. Tags vanish when a balance is zero: Microsoft stopped filing CommercialPaper after FY2025. So "not in XBRL" can mean zero or can mean the line was dropped. Read the balance sheet before you print $0.

### Cash flow and capex
- **10-Q cash-flow statements are year-to-date only.** Q2 and Q3 operating cash flow and capex are always derived (H1 minus Q1, 9M minus H1). The output marks them `derived` and shows the formula.
- Capex is reported as a positive outflow. PaymentsToAcquireProductiveAssets can include intangibles. Free cash flow (OCF minus capex) is non-GAAP. Compute it and label it computed.

### Gross profit
- Many retailers and service companies never tag GrossProfit (Walmart reports cost of sales but no gross profit line). The script says "not in XBRL" and does not compute revenue minus cost of revenue itself. If you compute it, label it computed and name the cost tag used.

## Period pitfalls (all metrics)

| Pitfall | How the script handles it |
|---|---|
| `fy`/`fp` on a fact describe the filing, not the fact's period | Labels come from matching `end` to the report date of the filing that covered that period as its own current period |
| 52/53-week fiscal years (Apple, Walmart and others): FY2023 at Apple ran 371 days | Duration classes accept 350-380 days for FY and 80-100 for a quarter. compare.py flags 53-week years |
| Fiscal year naming: a year ending Jan 31 2026 is Walmart's "FY2026". Some retailers call the year ending in early Feb 2026 "fiscal 2025" | The label is the filing's own DocumentFiscalYearFocus. Quote the start/end dates next to any FY label |
| Quarterly vs YTD vs TTM | 3-month, 6/9-month YTD and 12-month facts are kept apart by duration. TTM = the latest four contiguous quarters |
| Q4 is rarely tagged | Q4 = FY - 9M YTD (same fiscal-year start), with FY - Q1 - Q2 - Q3 as the fallback. Always marked `derived` and citing both filings. Apple FY2025 Q4 revenue: 416,161 - 313,695 = $102,466M |
| Restatements and recasts (accounting changes, discontinued operations, splits) | Latest-filed value by default, with the originally reported value, its accession and `revised=True`. `--as-reported` flips to original values. Live examples: Apple FY2009 revenue 36,537 to 42,905 ($M, 2010 revenue-recognition change). Microsoft FY2016-17 recast for ASC 606 |
| Amendments (10-K/A) | Included. A value taken from an /A filing is noted |
| Units and scale | Values are raw units. Display is in millions. Foreign filers use their reporting currency (the unit with the most facts), never the USD convenience translation (TSMC: TWD) |
| Company-extension tags (`aapl:...`), segments, non-GAAP | Not in companyfacts. Say so and point to the filing section |
