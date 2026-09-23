---
name: bi-measure-builder
description: Writes, explains, debugs, and optimizes BI calculations - Power BI / Fabric DAX measures and calculated columns, Tableau calculated fields (FIXED/INCLUDE/EXCLUDE LOD expressions, table calculations), and Looker LookML measures, dimensions, and derived tables. Use it whenever the request involves DAX, CALCULATE, a Power BI measure, a Tableau calc or LOD, LookML, or a business metric such as YoY, YTD, rolling 12 months, running total, percent of total, distinct customers, ranking, new vs returning customers, closing balances, or basket analysis. Use it especially when someone says a measure "shows the wrong total", "is blank", "ignores my slicer/filter", "repeats the same value on every row", or "is slow" - those are filter context, context transition, LOD order-of-operations, or fanout bugs this skill is built to diagnose. Produces the formula, the context it evaluates in, and a hand-checkable test with expected numbers.
---

# BI Measure Builder

Most wrong BI numbers are not syntax errors. They are the right formula evaluated in the wrong context. Work context-first, and prove every measure against numbers computed independently.

## Workflow

1. **Pin down the model before writing anything.** Get (or state as an explicit assumption): the fact table and its grain (one row per order line? per snapshot?), dimension tables, relationship keys and direction, and the date table. Ask only for what changes the formula; otherwise state the assumption and proceed. Why: the same YoY formula is right on a star schema and wrong on a flat table with a text date.
2. **Name the platform and version features.** DAX: classic vs calendar-based time intelligence (preview), marked date table or not. Tableau: live vs extract, context filters in use. Looker: dialect (window-function support, `period_over_period` support).
3. **State the evaluation context in one or two sentences** for a typical visual cell *and* for the grand total. Example: "Row = Month; filters = Region slicer; total = all months in the slicer range, recomputed, not summed." Why: this is where most bugs live, and saying it forces the check.
4. **Write the calculation** from the matching pattern in the reference file. Use variables (DAX `VAR`) for readability and to evaluate each sub-expression once.
5. **Explain it** line by line in terms of context: what each filter argument adds, removes, or overrides; where context transition happens; which Tableau pipeline step each part runs in; which part Looker runs in SQL vs after the query.
6. **Give a hand-computable test**: a 5-10 row sample, the visual layout, and the expected value for each row and the total. Generate or confirm the numbers with `scripts/measure_check.py` (below) rather than mental arithmetic.
7. **Performance notes** only where they matter: iterator size, context transition inside large iterators, table filters vs column filters, bidirectional relationships, LOD on high-cardinality dimensions, PDT persistence.

## References (load only the one needed)

- `references/dax.md` - DAX semantics recap plus patterns: YoY, YTD/fiscal YTD, rolling N, running total, % of total/parent, distinct count, ranking, new vs returning, semi-additive balances, basket.
- `references/tableau.md` - order of operations, LOD vs table calc choice, the same pattern set.
- `references/looker.md` - measure types, symmetric aggregates and fanout, post-SQL measure limits, `period_over_period`, derived tables, the same pattern set.
- `examples/worked-example.md` - a full run: "YoY % total is wrong" diagnosed, fixed in all three tools, verified with the script.

## Top traps and the fix for each

| Trap | Symptom | Fix |
|---|---|---|
| CALCULATE boolean filter *replaces* the existing filter on that column | "Blue sales" shows the same number on every color row | Wrap in `KEEPFILTERS(...)` to intersect instead of overwrite, when the intent is "within the current selection" |
| Filtering a whole table in CALCULATE (`FILTER(Sales, ...)`) | Wrong numbers via expanded-table intersection; very slow | Filter columns: `KEEPFILTERS(Sales[Qty] * Sales[Price] >= 500)` |
| Context transition surprise | Measure referenced inside `SUMX`/`FILTER`/calculated column gives per-row results or double counts duplicate rows | Know that a measure reference is an implicit CALCULATE; iterate a unique key (`VALUES(Table[Key])`), not a table with duplicate rows |
| Aggregator where an iterator is needed | `SUM(Sales[Qty]) * SUM(Sales[Price])` is wrong | `SUMX(Sales, Sales[Qty] * Sales[Price])` |
| Non-additive total "fixed" by summing | Distinct count or % total "doesn't add up" | Usually correct as-is. Only if the business wants a visual total: `SUMX(VALUES(dim[key]), [Measure])` |
| Time intelligence without a proper date table | Blank or wrong YoY/YTD, errors on gaps | Classic DAX: contiguous date table marked as date table, relationship from it to the fact. Calendar-based: define a calendar. Never use the fact's own date column |
| BLANK vs 0 | Visual explodes to every customer; `= 0` tests misfire | Return BLANK when there is nothing meaningful (`DIVIDE` without the 3rd arg); test with `ISBLANK` or `==`, since `BLANK() = 0` is TRUE |
| Bidirectional relationships as a shortcut | Ambiguity, slow, confusing slicers | Single-direction model; enable `CROSSFILTER(..., BOTH)` inside the one measure that needs it |
| Tableau FIXED ignores the dimension filter | LOD total unchanged when user filters | FIXED runs before dimension filters: add the filter to context, or use INCLUDE/EXCLUDE (run after dimension filters) |
| Tableau table calc sees only what is in the view | YoY blank for first year, rolling window truncated after filtering | Filter with a table-calc filter (runs after the calc) instead of a dimension filter; densify missing dates |
| Tableau total vs COUNTD / averages | Grand total differs from the row sum | "Automatic" totals re-aggregate underlying data (usually right); "Total Using: Sum" sums what is visible |
| Looker fanout on one-to-many joins | Sums inflated after adding a joined view | Set `primary_key: yes` on every view and a correct `relationship:`; Looker then applies symmetric aggregates. For denormalized tables use `sum_distinct` + `sql_distinct_key` |
| Looker post-SQL measures | `running_total` / `percent_of_total` wrong, null, or unfilterable | They compute after the query on returned rows only: row limits break them, they cannot be filtered or referenced by other measures. Move logic to SQL (derived table + window function) when it must be exact |
| Looker `filters:` on `type: number` | Filter silently not applied | Put `filters:` on the component `sum`/`count` measures, then combine them in the `type: number` measure |

## Verification script

`scripts/measure_check.py` is an independent oracle (pandas). Give it the user's sample CSV and a JSON spec; it prints the expected value for every visual row and for the total, evaluated the way BI tools do (total recomputed in its own context, time calcs reading outside the slicer range, empty = BLANK). With `--actual` it diffs against what the tool shows and exits 1 on mismatch.

```bash
python scripts/measure_check.py --data sample.csv --spec spec.json [--actual tool_output.csv] [--json]
```

Spec fields: `calc` (`sum`, `count_rows`, `distinct_count`, `prior_year`, `yoy_delta`, `yoy_pct`, `ytd`, `running_total`, `rolling`, `new_customers`, `returning_customers`, `last_balance`, `pct_of_total`, `rank`), `date_column`, `value_column`, `key_column` (customer/entity/distinct key), `group_column` (for pct/rank), `grain` (`day|month|quarter|year`), `range` (`{start, end}` = report date filter), `filters` (`{column: [values]}`), `params` (`window`, `fiscal_year_start_month`, `ties: skip|dense`, `order`, `mode: per_entity|global_last_date`). Examples of every calc: `tests/specs/`. Self-test: `python tests/test_measure_check.py`.

When the user has no sample, build a 5-10 row one that exercises the edge that matters (a missing month, a customer with no prior purchase, an entity without an end-of-month snapshot) and show it.

## Output format

Return, in this order:
1. **Assumptions** - model, grain, relationships, date table (bullets, only what matters).
2. **Evaluation context** - one sentence for a row, one for the total.
3. **The code** - one fenced block per tool requested, named measures, formatted.
4. **How it works** - short, context-focused explanation.
5. **Test** - sample table, expected results table (rows + total), and the spec used if the script was run.
6. **Gotchas / performance** - only the ones relevant to this model.

When debugging an existing measure, lead with the one-line root cause, then the corrected code, then the test that shows old vs new values.
