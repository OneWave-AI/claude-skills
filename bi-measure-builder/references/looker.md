# LookML patterns (Looker)

Sources: cloud.google.com/looker/docs (now docs.cloud.google.com) - measure types, symmetric aggregates, `sql_distinct_key`, field `filters`, period-over-period measures, derived tables, table calculation functions.

Assumed model unless told otherwise: view `orders` (one row per order, `primary_key: yes` on `id`), view `order_items` joined `relationship: one_to_many`, `dimension_group: created { type: time }` on `orders`. SQL snippets are ANSI-ish; adjust to the connection's dialect.

## Semantics that decide correctness

- **Measures are SQL aggregates** generated per query. Dimensions in the query define the grain (GROUP BY); totals are a separate aggregate (not a sum of rows).
- **Fanout and symmetric aggregates**: joining a one-to-many view duplicates the "one" side rows. Looker corrects `sum`, `average`, `count` via symmetric aggregates only when every view has a unique `primary_key` and every join has the correct `relationship`. Wrong or missing primary key = inflated sums. Median/percentile types are not symmetric.
- **Denormalized tables** (no join to fix): `type: sum_distinct` / `average_distinct` with `sql_distinct_key`; every distinct key must map to exactly one `sql` value.
- **`type: number`** does arithmetic on other measures only; `filters:` does not work on it. Filter the component measures instead. Guard division with `NULLIF(..., 0)` and force decimals (`1.0 *`) to avoid integer division on some dialects.
- **Post-SQL measures** (`running_total`, `percent_of_total`, `percent_of_previous`) are calculated after the query returns: they depend on sort order, cannot be filtered on, should not be referenced by other measures, and `percent_of_total` shows nulls if the row limit is hit. Table calculations have the same "only the returned rows" limit.
- **`period_over_period`** (new LookML runtime, supported dialects): `based_on` must be an aggregate measure (count/sum/average/min/max/median/percentile or distinct variants), `based_on_time` a time dimension group timeframe, `kind: previous | difference | relative_change`, `period: year | fiscal_year | quarter | fiscal_quarter | month | week | date`. The query must include a time dimension at or below `period`. Cannot be filtered on; no subtotals, row totals, custom fields, or aggregate awareness.

## Base fields

```lookml
view: orders {
  sql_table_name: analytics.orders ;;
  dimension: id { primary_key: yes  type: number  sql: ${TABLE}.id ;; }
  dimension: customer_id { type: number  sql: ${TABLE}.customer_id ;; }
  dimension_group: created { type: time  timeframes: [raw, date, month, quarter, year]  sql: ${TABLE}.created_at ;; }
  dimension: amount { type: number  sql: ${TABLE}.amount ;; }
  measure: total_sales { type: sum  sql: ${amount} ;;  value_format_name: usd }
  measure: order_count { type: count }
}
```

## YoY

```lookml
measure: total_sales_py {
  type: period_over_period
  based_on: total_sales
  based_on_time: created_year
  period: year
  kind: previous
}
measure: total_sales_yoy_pct {
  type: period_over_period
  based_on: total_sales
  based_on_time: created_year
  period: year
  kind: relative_change
  value_format_name: percent_1
}
```
Gotcha: partial current period. A "year" row for the current year compares YTD with a full prior year; use a month timeframe or a YTD yesno filter. On dialects without PoP, use filtered measures against yesno dimensions (below).

## YTD (and like-for-like prior YTD)

```lookml
dimension: is_ytd {
  type: yesno
  sql: EXTRACT(DAYOFYEAR FROM ${created_raw}) <= EXTRACT(DAYOFYEAR FROM CURRENT_DATE) ;;
}
measure: sales_this_year_ytd { type: sum  sql: ${amount} ;;  filters: [is_ytd: "yes", created_year: "this year"] }
measure: sales_last_year_ytd { type: sum  sql: ${amount} ;;  filters: [is_ytd: "yes", created_year: "last year"] }
measure: ytd_growth { type: number  sql: 1.0 * (${sales_this_year_ytd} - ${sales_last_year_ytd}) / NULLIF(${sales_last_year_ytd}, 0) ;; }
```
Gotcha: day-of-year drifts by one day in leap years; compare month and day if exactness matters. Fiscal years: set `fiscal_month_offset` on the model and use `fiscal_year` timeframes.

## Rolling N periods

Quick, in the Explore (month rows sorted ascending): table calculation `sum(offset_list(${orders.total_sales}, -2, 3))`.
Gotcha: sees only returned rows - missing months shorten the window, row limits and date filters truncate it. Exact version: derived table on a date spine.
```lookml
view: sales_rolling_3m {
  derived_table: {
    sql:
      SELECT month, SUM(sales) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS sales_r3m
      FROM (SELECT m.month AS month, COALESCE(SUM(o.amount), 0) AS sales
            FROM analytics.month_spine m LEFT JOIN analytics.orders o
              ON DATE_TRUNC(o.created_at, MONTH) = m.month
            GROUP BY 1) t ;;
  }
  dimension: month { primary_key: yes  type: date  sql: ${TABLE}.month ;; }
  measure: sales_r3m { type: sum  sql: ${TABLE}.sales_r3m ;; }
}
```
Filters on the Explore do not reach inside this SQL; add templated filters (`{% condition %}`) or make it a native derived table with `bind_filters` if slicers must apply.

## Running total

`measure: running_sales { type: running_total  sql: ${total_sales} ;; }` or table calc `running_total(${orders.total_sales})`. Both depend on sort order and only see returned rows; a window function in a derived table is exact.

## Percent of total

`measure: pct_of_sales { type: percent_of_total  sql: ${total_sales} ;; }` - column share of returned rows; nulls when the row limit is exceeded. Exact share of all data: derived table with `SUM(x) OVER ()` or a `type: number` over a filtered/unfiltered pair of measures.

## Distinct count and fanout

```lookml
measure: customer_count { type: count_distinct  sql: ${customer_id} ;; }
measure: total_shipping {            # shipping repeats on every order_items row
  type: sum_distinct
  sql_distinct_key: ${order_id} ;;
  sql: ${order_shipping} ;;
}
```
Gotcha: a `type: sum` on the "one" side of a one_to_many join is only safe with symmetric aggregates (primary keys plus relationships set). Totals of count_distinct are non-additive by design.

## Ranking

Table calc `rank(${orders.total_sales}, ${orders.total_sales})` on returned rows. For ranks that must be filterable or stable across queries, compute `RANK() OVER (PARTITION BY region ORDER BY sales DESC)` in a derived table and expose it as a dimension.

## New vs returning customers

```lookml
view: customer_facts {
  derived_table: {
    sql: SELECT customer_id, MIN(created_at) AS first_order_at FROM analytics.orders GROUP BY customer_id ;;
    datagroup_trigger: nightly
  }
  dimension: customer_id { primary_key: yes  type: number  sql: ${TABLE}.customer_id ;; }
  dimension_group: first_order { type: time  timeframes: [raw, month]  sql: ${TABLE}.first_order_at ;; }
}
# explore: orders { join: customer_facts { sql_on: ${orders.customer_id} = ${customer_facts.customer_id} ;; relationship: many_to_one } }
# in view orders:
dimension: is_first_order_month {
  type: yesno
  sql: DATE_TRUNC(${created_raw}, MONTH) = DATE_TRUNC(${customer_facts.first_order_raw}, MONTH) ;;
}
measure: new_customers       { type: count_distinct  sql: ${customer_id} ;;  filters: [is_first_order_month: "yes"] }
measure: returning_customers { type: count_distinct  sql: ${customer_id} ;;  filters: [is_first_order_month: "no"] }
```
Gotcha: the derived table is lifetime and ignores Explore filters (usually intended). The flag's grain must match the query grain: at month rows it is exact, but a quarter query would count a customer who first ordered in January and again in February as both new and returning. Add an `is_first_order_quarter` flag for quarter reporting. Persist the derived table (`datagroup_trigger` or `persist_for`) and alias every derived column with `AS`.

## Semi-additive balances

```lookml
view: balances {
  derived_table: {
    sql: SELECT *, ROW_NUMBER() OVER (PARTITION BY account_id, DATE_TRUNC(snapshot_date, MONTH)
                                      ORDER BY snapshot_date DESC) = 1 AS is_last_in_month
         FROM analytics.balance_snapshots ;;
  }
  dimension: pk { primary_key: yes  sql: CONCAT(${TABLE}.account_id, '-', CAST(${TABLE}.snapshot_date AS STRING)) ;; }
  dimension: is_last_in_month { type: yesno  sql: ${TABLE}.is_last_in_month ;; }
  measure: month_end_balance { type: sum  sql: ${TABLE}.balance ;;  filters: [is_last_in_month: "yes"] }
}
```
Gotcha: valid only for month rows; a quarter total needs an `is_last_in_quarter` flag. A plain `sum` of balances across months is the classic wrong answer.

## Basket: orders with product A and B

Derived table at order grain: `SELECT order_id, MAX(CASE WHEN product = 'A' THEN 1 ELSE 0 END) AS has_a, MAX(CASE WHEN product = 'B' THEN 1 ELSE 0 END) AS has_b FROM order_items GROUP BY order_id`, joined `many_to_one` from order_items; then `measure: orders_a_and_b { type: count_distinct  sql: ${order_id} ;;  filters: [order_basket.has_a: "1", order_basket.has_b: "1"] }` (expose `has_a`/`has_b` as yesno for cleaner filters).

## Performance

Persist expensive derived tables (PDTs with a datagroup). Avoid huge fanout joins in the default Explore; use `fields:` / separate Explores. Prefer SQL window functions in derived tables over post-SQL measures when correctness must survive row limits. Check the generated SQL in the Explore's SQL tab for every new measure.
