# DAX patterns (Power BI, Fabric, Analysis Services)

Sources: learn.microsoft.com/dax (CALCULATE, DATESINPERIOD, DIVIDE, RANKX, RANK, time intelligence), learn.microsoft.com/power-bi (date tables, calendar-based time intelligence, bidirectional guidance), sqlbi.com / daxpatterns.com (context transition, filter columns not tables, running totals, semi-additive, accurate totals, new/returning customers).

Assumed model unless told otherwise: `Sales` fact (one row per order line) with `Sales[OrderDate]`, `Sales[CustomerKey]`, `Sales[Amount]`; `'Date'` dimension, one row per day, related 1:* single-direction to `Sales[OrderDate]`; `Customer`, `Product` dimensions. Base measure: `Sales Amount := SUM ( Sales[Amount] )`. Build every pattern on base measures, not on raw columns.

## Semantics that decide correctness

- **CALCULATE filter arguments**: for each filter not wrapped in KEEPFILTERS, if the column is already filtered the new filter *overwrites* it; otherwise it is added. `KEEPFILTERS` intersects instead.
- **Boolean filter rules**: may reference columns of a single table only; no measures; no nested CALCULATE. Compute measure values into a `VAR` first, then compare.
- **Context transition**: CALCULATE turns every active row context into an equivalent filter context. A measure reference is an implicit CALCULATE, so a measure inside `SUMX`/`FILTER`/`ADDCOLUMNS` or a calculated column is evaluated per row. It filters by *all columns* of the row, so duplicate rows are matched together (double counting). Iterate unique keys.
- **Filter columns, not tables**: `CALCULATE(..., FILTER(Sales, ...))` filters the expanded table (Sales plus every related dimension) - wrong intersections and much slower. Use column predicates, with KEEPFILTERS when the current selection must survive.
- **Iterators vs aggregators**: `SUM(col)` aggregates one column; row-by-row math needs `SUMX(table, expr)`.
- **Totals are re-evaluated**, not summed. A non-additive measure's total is correct in its own context. For a visual total use `SUMX(VALUES(dim[key]), [Measure])`.
- **BLANK**: `BLANK()+5 = 5`, `BLANK()*5 = BLANK`, `5/BLANK() = Infinity` (use DIVIDE), `BLANK() = 0` is TRUE, `BLANK() == 0` is FALSE. DIVIDE's alternate result must be a constant and defaults to BLANK. Converting BLANK to 0 turns sparse visuals dense (every customer row appears) and slows reports - avoid unless required.
- **Time intelligence**: classic functions need a date table marked as date table with unique, non-null, contiguous dates (missing dates raise an error). Calendar-based time intelligence (preview; defined under Calendar options/TMDL) takes a calendar name instead: `TOTALYTD([Sales Amount], 'Fiscal Calendar')`; supports week-based and non-Gregorian calendars, sparse dates, but cannot be used with live-connected or composite models and calendar functions cannot be nested.
- **Relationships**: keep single direction. Enable both directions only inside a measure: `CALCULATE(DISTINCTCOUNT(Customer[Country]), CROSSFILTER(Customer[CustomerKey], Sales[CustomerKey], BOTH))`. Activate an inactive role-playing relationship (ship date) with `USERELATIONSHIP`.

## YoY

```dax
Sales PY := CALCULATE ( [Sales Amount], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
Sales YoY % :=
VAR Cur = [Sales Amount]
VAR PY  = [Sales PY]
RETURN IF ( NOT ISBLANK ( Cur ) && NOT ISBLANK ( PY ), DIVIDE ( Cur - PY, PY ) )
```
Gotcha: the current year is partial but the prior-year period is full (a year row compares Jan-Jun to all of last year). Restrict with a calculated column on the date table, `DateWithSales = 'Date'[Date] <= MAX ( Sales[OrderDate] )` (no row-to-filter transition in that MAX, so it is the global last sale date), and use `CALCULATE ( [Sales Amount], CALCULATETABLE ( SAMEPERIODLASTYEAR ( 'Date'[Date] ), 'Date'[DateWithSales] = TRUE ) )` for PY. Also: the total YoY is `(total cur - total PY) / total PY`, never the sum or average of row percentages.

## YTD and fiscal YTD

```dax
Sales YTD := CALCULATE ( [Sales Amount], DATESYTD ( 'Date'[Date] ) )
Sales FYTD := CALCULATE ( [Sales Amount], DATESYTD ( 'Date'[Date], "6-30" ) )  -- year ends Jun 30
```
Gotcha: at a year-level row or a total, YTD evaluates as of the last date in context - including future dates in the date table (flat line to Dec 31). Blank out future periods: `IF ( MIN ( 'Date'[Date] ) <= CALCULATE ( MAX ( Sales[OrderDate] ), REMOVEFILTERS ( 'Date' ) ), [Sales YTD] )`.

## Rolling N months

```dax
Sales R12M :=
VAR Anchor = MIN ( MAX ( 'Date'[Date] ), CALCULATE ( MAX ( Sales[OrderDate] ), REMOVEFILTERS ( 'Date' ) ) )
RETURN CALCULATE ( [Sales Amount], DATESINPERIOD ( 'Date'[Date], Anchor, -12, MONTH ) )
```
DATESINPERIOD with a negative count goes back from the start date and only returns dates that exist in the date column. Gotcha: anchoring on `MAX('Date'[Date])` alone makes the total and future months roll over empty dates; anchoring on the last fact date fixes it. Show "incomplete window" as BLANK if required: compare `MIN('Date'[Date])` of the window with the first fact date.

## Running total

```dax
Sales RT :=
VAR MaxDate = MAX ( 'Date'[Date] )
RETURN CALCULATE ( [Sales Amount], 'Date'[Date] <= MaxDate, REMOVEFILTERS ( 'Date' ) )
```
The variable captures the current last date before CALCULATE overwrites the date filter. Gotcha: `REMOVEFILTERS('Date')` also removes date slicers, so it accumulates from the first date ever (all-time). To start the accumulation at the first date the user selected, use `ALLSELECTED ( 'Date' )` instead. REMOVEFILTERS is needed because the visual filters other date columns (Year, Month) that the `'Date'[Date]` predicate would not override.

## Percent of total / parent

```dax
Pct of All Products  := DIVIDE ( [Sales Amount], CALCULATE ( [Sales Amount], REMOVEFILTERS ( Product ) ) )
Pct of Selection     := DIVIDE ( [Sales Amount], CALCULATE ( [Sales Amount], ALLSELECTED ( Product ) ) )
Pct of Parent Category :=
DIVIDE ( [Sales Amount], CALCULATE ( [Sales Amount], REMOVEFILTERS ( Product[Subcategory] ) ) )
```
Gotcha: decide whether the denominator honors the user's slicer (ALLSELECTED) or not (REMOVEFILTERS). For a hierarchy, pick the level with `ISINSCOPE ( Product[Subcategory] )` first, then category.

## Distinct count

```dax
Customers := DISTINCTCOUNT ( Sales[CustomerKey] )
```
Count the key in the fact (customers who bought), not `COUNTROWS(Customer)` (all customers, unaffected by fact filters in a single-direction model). DISTINCTCOUNT counts BLANK as a value; `DISTINCTCOUNTNOBLANK` does not. Totals are non-additive by design.

## Ranking

```dax
Product Rank :=
IF (
    ISINSCOPE ( Product[Product Name] ) && NOT ISBLANK ( [Sales Amount] ),
    RANKX ( ALLSELECTED ( Product[Product Name] ), [Sales Amount], , DESC, Dense )
)
```
RANKX evaluates the expression for each row of the table (context transition via the measure) and treats BLANK as 0, so products with no sales are ranked unless guarded. Default ties = Skip, default order = DESC. Rank decimals can mis-tie from float precision: ROUND the expression. The newer window function `RANK` (ties, relation, ORDERBY, PARTITIONBY) returns BLANK on total rows by design and is the cleaner choice in visual calculations: `RANK(DENSE, ORDERBY([Sales Amount], DESC))`.

## New vs returning customers (lifetime first purchase)

```dax
New Customers :=
VAR PeriodStart = MIN ( 'Date'[Date] )
VAR CustFirst =
    ADDCOLUMNS (
        VALUES ( Sales[CustomerKey] ),                       -- customers active in the period
        "@First", CALCULATE ( MIN ( Sales[OrderDate] ), REMOVEFILTERS ( 'Date' ) )
    )
RETURN COUNTROWS ( FILTER ( CustFirst, [@First] >= PeriodStart ) )

Returning Customers :=
VAR PeriodStart = MIN ( 'Date'[Date] )
VAR CustFirst =
    ADDCOLUMNS ( VALUES ( Sales[CustomerKey] ),
        "@First", CALCULATE ( MIN ( Sales[OrderDate] ), REMOVEFILTERS ( 'Date' ) ) )
RETURN COUNTROWS ( FILTER ( CustFirst, [@First] < PeriodStart ) )
```
Context transition in ADDCOLUMNS filters one customer; REMOVEFILTERS('Date') looks at full history. Gotcha: other slicers (region, product) stay, so "new" means "new within that slice" - remove them too (`REMOVEFILTERS(Product)`) if new means new to the business. New + Returning = Customers for every period. daxpatterns.com has a faster version using TREATAS for large models.

## Semi-additive balances (inventory, account balance, headcount)

```dax
Balance :=                                     -- each account's last snapshot in the period, summed
SUMX (
    VALUES ( Balances[Account] ),
    VAR LastDate = CALCULATE ( MAX ( Balances[Date] ) )
    RETURN CALCULATE ( SUM ( Balances[Balance] ), 'Date'[Date] = LastDate )
)
```
Gotcha: `LASTDATE('Date'[Date])` returns the calendar's last day (Dec 31) and yields BLANK when no snapshot exists that day. `MAX(Balances[Date])` without the per-account iteration drops accounts whose last snapshot is earlier than the global last date. Pick deliberately: per-account (above) or global last date. SQLBI shows a TREATAS version that avoids the iteration on large models.

## Basket: orders containing the selected product and product B

```dax
Orders With B :=
VAR OrdersB =
    CALCULATETABLE ( VALUES ( Sales[OrderID] ), REMOVEFILTERS ( Product ), Product[Product Name] = "B" )
RETURN CALCULATE ( DISTINCTCOUNT ( Sales[OrderID] ), KEEPFILTERS ( OrdersB ) )
```
With Product in rows: orders that include the row's product and also B. `REMOVEFILTERS(Product)` is required or category slicers would hide B. For "any product vs any product", use a disconnected copy of Product and TREATAS.

## Calculated column vs measure

Calculated columns are computed at refresh, stored, row context only (use them for static attributes such as `'Date'[DateWithSales]`, customer segment by lifetime value). Anything that must respond to slicers is a measure. Aggregating inside a calculated column requires CALCULATE for context transition.

## Performance checklist

Iterate the smallest unique table (`VALUES(dim[key])`, not the fact). Avoid measures inside FILTER over the fact (context transition per row). Use VAR to avoid recomputing. Prefer column predicates over FILTER(table). Avoid bidirectional relationships and IFERROR. Check with Performance Analyzer / DAX Studio server timings.
