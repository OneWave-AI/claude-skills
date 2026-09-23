# Tableau calculation patterns

Sources: help.tableau.com - Order of Operations, LOD expressions (overview, FIXED/INCLUDE/EXCLUDE, filters and LODs), Table Calculations, Table Calculation Functions, Show Totals.

Assumed data unless told otherwise: an Orders source, one row per order line, with `[Order Date]`, `[Customer ID]`, `[Order ID]`, `[Region]`, `[Product]`, `[Sales]`.

## Order of operations (decides most bugs)

1. Extract filters, data source filters
2. Context filters
3. **FIXED LOD** computed here
4. Dimension filters (including Top N)
5. **INCLUDE / EXCLUDE LOD** computed here, and ordinary aggregates
6. Measure filters (like SQL HAVING)
7. **Table calculations** computed on the aggregated marks in the view
8. Table calculation filters (hide marks, do not change calc inputs)

Consequences:
- FIXED ignores dimension filters and view dimensions. To make a filter affect a FIXED calc, right-click the filter > Add to Context. Context filters also change Top N and FIXED results everywhere on the sheet.
- INCLUDE/EXCLUDE respect dimension filters and are relative to the view level of detail.
- Table calcs see only what survived steps 1-6. Filtering out 2024 makes a 2025 YoY table calc BLANK. Hide rows with a table-calc filter instead, e.g. filter on `LOOKUP(MIN(YEAR([Order Date])), 0)`, which runs after the calculation.

## LOD vs table calc: choose

- **LOD**: needs a grain different from the view but computed in the data source (first purchase per customer, per-order totals). Results can be used as dimensions (FIXED only) and in further row-level logic. Syntax `{FIXED [Dim1], [Dim2] : AGG(expr)}`; `{SUM([Sales])}` with no keyword equals `{FIXED : SUM([Sales])}` (whole table).
- **Table calc**: needs relationships between marks (previous row, running sum, rank, percent of visible total). Configure Compute Using / Specific Dimensions: *addressing* fields are what the calc moves along, the remaining dimensions *partition* (restart) it. Always state the intended addressing, because the default (Table across) is often wrong once dimensions move.
- An LOD finer than the view is wrapped in an aggregation when placed on a shelf (often AVG; set it deliberately). EXCLUDE results replicate across marks and default to ATTR.

## Totals

Grand totals with "Automatic" are computed from the underlying disaggregated data at the total level (COUNTD over the whole set, not a sum of row counts). "Total Using: Sum/Average/..." aggregates the values visible in the view. Pick based on what the business wants the total to mean.

## YoY

Table calc (Year of Order Date on the view, compute along it):
```
// Sales YoY %
(ZN(SUM([Sales])) - LOOKUP(ZN(SUM([Sales])), -1)) / ABS(LOOKUP(ZN(SUM([Sales])), -1))
```
Gotcha: first year is null (nothing to look up), and filtering to one year kills it (see order of operations). Missing months shift LOOKUP by the wrong amount: turn on Show Missing Values for continuous dates or use the calc below.

Filter-proof row-level version with a parameter `[Selected Year]`:
```
// Sales CY (row level)
IF YEAR([Order Date]) = [Selected Year] THEN [Sales] END
// Sales PY (row level)
IF YEAR([Order Date]) = [Selected Year] - 1 THEN [Sales] END
// YoY % (aggregate)
(SUM([Sales CY]) - SUM([Sales PY])) / SUM([Sales PY])
```
Keep CY/PY row level and aggregate once in the ratio; wrapping them in SUM and then SUM again is an "aggregate of an aggregate" error.
Do not also put a Year dimension filter on the sheet that excludes the prior year.

## YTD and fiscal YTD

```
// Sales YTD (as of parameter [As Of Date])
SUM(IF [Order Date] >= DATETRUNC('year', [As Of Date]) AND [Order Date] <= [As Of Date] THEN [Sales] END)
```
Fiscal years starting in month M: compare on shifted dates, e.g. `DATETRUNC('year', DATEADD('month', -(M-1), [Order Date])) = DATETRUNC('year', DATEADD('month', -(M-1), [As Of Date]))` plus `[Order Date] <= [As Of Date]`. Test on a sample that crosses the fiscal boundary. Cumulative YTD by month: Quick Table Calc Running Total, compute along Month, partition by Year.

## Rolling N periods

```
// Rolling 3 months, compute along continuous Month of Order Date
WINDOW_SUM(SUM([Sales]), -2, 0)
```
Gotcha: the window is N *marks*, not N months - sparse months break it (Show Missing Values), and the first N-1 marks after a date filter are truncated. Filter with a table-calc filter or compute the window in a row-level calc against a parameter date. Use `IF FIRST() > -2 THEN NULL ELSE ... END`-style guards (FIRST() is 0 at the first row, negative after) to blank incomplete windows.

## Running total

`RUNNING_SUM(SUM([Sales]))` - restarts per partition. To run across years, address Year and Month; to restart per year, partition by Year.

## Percent of total / parent

```
// Of the visible total (table calc, respects filters)
SUM([Sales]) / TOTAL(SUM([Sales]))
// Of the parent Region, independent of view layout (respects dimension filters)
SUM([Sales]) / SUM({EXCLUDE [Product] : SUM([Sales])})
// Of the entire data, ignoring dimension filters (FIXED)
SUM([Sales]) / MIN({FIXED : SUM([Sales])})
```
Gotcha: these three give different answers once a filter is applied; state which denominator the business means.

## Distinct count

`COUNTD([Customer ID])`. Non-additive; with Automatic totals, the grand total is distinct over the whole set. COUNTD is one of the most expensive aggregates on large sources.

## Ranking

`RANK(SUM([Sales]))` (standard competition, default descending), `RANK_DENSE`, `RANK_UNIQUE`. It is a table calc: set addressing to the dimension being ranked; partition to rank within a group. Top N per group needs the rank as a table-calc filter, not a Top N dimension filter (that one runs before and ignores the partition).

## New vs returning customers

```
// First Purchase Date (lifetime, ignores dimension filters)
{FIXED [Customer ID] : MIN([Order Date])}
// New customers at month grain
COUNTD(IF DATETRUNC('month', [First Purchase Date]) = DATETRUNC('month', [Order Date]) THEN [Customer ID] END)
// Returning customers at month grain
COUNTD(IF [First Purchase Date] < DATETRUNC('month', [Order Date]) THEN [Customer ID] END)
```
Gotcha: FIXED is lifetime *unless* a context filter is present (then "first purchase within the context"). The 'month' literal ties the calc to the view grain; drive it from a parameter if the view grain changes. New + Returning = COUNTD(Customer ID) per period.

## Semi-additive balances

```
// Last snapshot date per account in the month
{FIXED [Account], DATETRUNC('month', [Snapshot Date]) : MAX([Snapshot Date])}
// Balance: each account's last snapshot in the period, summed
SUM(IF [Snapshot Date] = [Last Snapshot In Month] THEN [Balance] END)
```
Gotcha: a quarter view needs the quarter version of the FIXED; SUM of monthly balances across a quarter is wrong. Accounts with no snapshot in a month disappear from that month (decide whether to carry forward, which needs densified data).

## Basket: orders containing product A and B

```
// Order has B (row level, per order)
{FIXED [Order ID] : MAX(IF [Product] = 'B' THEN 1 ELSE 0 END)}
// Orders with the row's product and B
COUNTD(IF [Order Has B] = 1 THEN [Order ID] END)
```
Put `[Product]` on rows and exclude 'B' itself. Because FIXED runs before dimension filters, filtering Product to 'A' still sees B lines in the same order - that is the desired behavior here.

## Performance

Prefer row-level and aggregate calcs over LODs when the view grain already matches. FIXED on high-cardinality dimensions (Order ID, Customer ID) produces large subqueries/joins; materialize in the extract or source when slow. Context filters are costly on live connections. String comparisons and COUNTD are the slowest aggregates. Use the Performance Recorder.
