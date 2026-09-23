# Worked example: "My YoY % is right per month but the total is wrong"

## The request

> Our monthly sales report shows YoY % by month for Q1 2025. The months look right, but the Total row says 83.3%, and finance says Q1 growth was about 49%. Measure:
> ```dax
> YoY % = AVERAGEX ( VALUES ( 'Date'[Year Month] ), DIVIDE ( [Sales Amount] - [Sales PY], [Sales PY] ) )
> ```

## 1. Assumptions

- `Sales` fact, one row per order, `Sales[OrderDate]`, `Sales[Amount]`.
- `'Date'` table, one row per day 2024-01-01..2025-12-31, marked as date table, 1:* single direction to `Sales[OrderDate]`.
- `Sales PY := CALCULATE ( [Sales Amount], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )`.
- Visual: rows = `'Date'[Year Month]`, slicer = Q1 2025.

## 2. Evaluation context

- Month row: filter context is one month; `SAMEPERIODLASTYEAR` shifts the visible dates back a year, reading outside the slicer (intended).
- Total row: filter context is all of Q1 2025. `AVERAGEX` iterates the three months and averages their ratios: (120% - 10% + 140%) / 3 = 83.3%. That answers "average monthly growth rate", not "Q1 growth".

**Root cause:** an iterator was used to force a total; a ratio must be computed from totals, not averaged from rows.

## 3. The code

```dax
YoY % :=
VAR Cur = [Sales Amount]
VAR PY  = [Sales PY]
RETURN IF ( NOT ISBLANK ( Cur ) && NOT ISBLANK ( PY ), DIVIDE ( Cur - PY, PY ) )
```

Tableau (rows = discrete MONTH(Order Date) without year; filter Quarter = Q1, no Year filter; parameter `[Selected Year]` = 2025; Grand Total "Automatic"):
```
// Sales CY (row level)
IF YEAR([Order Date]) = [Selected Year] THEN [Sales] END
// Sales PY (row level)
IF YEAR([Order Date]) = [Selected Year] - 1 THEN [Sales] END
// YoY % (aggregate)
(SUM([Sales CY]) - SUM([Sales PY])) / SUM([Sales PY])
```
Both years must survive the filters, which is why the year lives in a parameter, not a dimension filter. "Automatic" grand totals recompute the ratio from underlying data (48.57%); "Total Using: Average" would reproduce the 83.3% bug.

LookML:
```lookml
measure: total_sales_yoy_pct {
  type: period_over_period
  based_on: total_sales
  based_on_time: created_month
  period: year
  kind: relative_change
  value_format_name: percent_1
}
```
PoP measures do not support row totals/subtotals; show the Q1 figure from a query at quarter grain (`based_on_time: created_quarter`), not from an Explore total.

## 4. How it works

`Cur` and `PY` are evaluated once in whatever context the cell has. In a month cell they are that month and the same month last year; in the total they are all of Q1 2025 and all of Q1 2024. The ratio is then taken once, so the total is the true Q1 growth. The ISBLANK guard returns BLANK for months with no prior-year sales instead of a misleading value, and DIVIDE returns BLANK when PY is 0.

## 5. Test

Sample (`tests/fixtures/sales.csv`):

| order_date | customer | region | amount |
|---|---|---|---|
| 2024-01-15 | A | East | 100 |
| 2024-02-10 | B | West | 200 |
| 2024-03-05 | A | East | 50 |
| 2024-12-20 | C | West | 80 |
| 2025-01-08 | A | East | 150 |
| 2025-01-22 | C | West | 70 |
| 2025-02-14 | B | West | 120 |
| 2025-02-28 | D | East | 60 |
| 2025-03-30 | A | East | 90 |
| 2025-03-31 | B | West | 30 |

By hand: 2025 months = 220, 180, 120 (Q1 520); 2024 months = 100, 200, 50 (Q1 350).

```bash
python scripts/measure_check.py --data tests/fixtures/sales.csv --spec examples/yoy_spec.json \
  --actual examples/actual_yoy_from_tool.csv --tol 0.0001
```

Output:

```
| row | expected |
|---|---|
| 2025-01 | 120.0000% |
| 2025-02 | -10.0000% |
| 2025-03 | 140.0000% |
| **Total** | **48.5714%** |

Note: sum of visible rows = 250.0000% but the correct total is 48.5714%. This measure is non-additive; ...
MISMATCH Total: tool shows 0.8333333333, expected 0.4857142857142857

1 mismatch(es).
```

The old measure matches on every month and fails only on the total (83.33% vs 48.57%), which confirms the diagnosis. After the fix, the report total is (520 - 350) / 350 = 48.57%, and rerunning against `examples/actual_yoy_fixed.csv` (the corrected report values) prints "All actual values match."

## 6. Gotchas for this model

- If the current quarter is still open, the Q row compares a partial quarter with a full one; add the `DateWithSales` restriction from `references/dax.md`.
- If the date table does not cover 2024, `SAMEPERIODLASTYEAR` returns no dates and PY is BLANK.
- Do not coalesce PY to 0: the ratio would still be BLANK (DIVIDE by 0), but a YoY delta measure would report a month with no history as 100% new growth, and the visual turns dense.
