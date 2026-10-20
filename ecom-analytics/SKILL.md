---
name: ecom-analytics
description: Use this skill when the user wants to analyze e-commerce performance, review funnel conversion,
  investigate AOV or repeat-purchase trends, build an ecom report, check sales velocity, understand customer
  cohorts and retention, or answer questions about their store's sales data. Triggers include 'how is
  my store performing', 'what's my conversion rate', 'cart abandonment', 'AOV trend', 'repeat purchase
  rate', 'why did revenue drop', 'cohort retention', 'top products', 'new vs returning customer revenue',
  'lifetime value', 'pull my Shopify numbers', 'ecom report'. Reads live data from your Coupler.io workspace
  via the Coupler.io MCP connector.
---

# Ecom Analytics

Analyze e-commerce performance using data from Coupler.io dataflows (Shopify, WooCommerce, BigCommerce, Magento, GA4, Stripe, Klaviyo, etc.). This skill guides you through retrieving order/session data, computing funnel and revenue metrics, detecting anomalies, and presenting actionable insights an ecom operator can act on.

## Step 0: Context Check (Pre-requisite)

Before starting any analysis, the **Data Context Check** skill (`generate-data-set-context`) runs as a gate. It calls `get-schema` on each target dataset to determine whether meaningful context (column descriptions, business rules, metric definitions, e.g. how returns are flagged, currency conventions, what counts as a 'completed' order) is attached.

- If context exists → proceed to Step 1.
- If context is missing → the user is offered the option to generate it first.

Do not duplicate this check in Step 1d. If the context check skill has already run and context is present, Step 1d should use the enriched schema directly.

## Step 1: Discover and Select Data Sources

Every analysis starts by connecting to the user's data through Coupler.io MCP tools.

### 1a. Discover available data

Default to `search-datasets` with ecom-flavored keywords — `shopify`, `woocommerce`, `bigcommerce`, `magento`, `orders`, `gmv`, `ecom`, `klaviyo`, `ga4`, `stripe`, or whatever store/source the user named. Search keeps the response small and lands on the right dataflow when the domain is known (which it is, by definition, when this skill is loaded).

Fall back to `list-datasets` only when the user is genuinely browsing or hasn't given any source/keyword to anchor on. Each dataflow represents a data pipeline (e.g. "Shopify Orders", "GA4 Ecommerce Events", "Klaviyo Email Engagement", "Stripe Charges", "WooCommerce Sales").

### 1b. Select relevant datasets

How you handle selection depends on the match clarity, not just the count:

**Unambiguous match (1 dataflow, clearly matches the request)** → use it. Mention which one you're using in your output. No confirmation needed.

**Obvious candidates (2–3 dataflows clearly relevant)** → state your selection with one-line reasoning. Proceed but invite corrections.

**Ambiguous (5+ dataflows, or unclear which subset matters)** → present your best candidates (up to 5–7) grouped by source/scope, with reasoning, and wait for confirmation:

```
I found 3 dataflows likely relevant to your repeat-purchase question:
  1. shopify_orders — has customer_id, order date, line items
  2. klaviyo_engagement — email touchpoints around purchases
  3. ga4_ecommerce — session-level conversion data
Should I use all three, or focus on one?
```

**Hard gate only when ambiguous:** wait for user confirmation when the right datasets aren't obvious. If you're confident and stated your reasoning, proceed — the user can redirect you.

### 1c. Get dataflow details

For each selected dataset, call `get-dataflow` to read its current state — sources, destinations, last run, schedule. Note data freshness (when the dataflow last ran) so you can mention it in the output.

### 1d. Understand the data structure

Call `get-schema` on each target dataset. If context was generated in Step 0, use the enriched schema directly. Otherwise build a mental mapping between `columnName` (used in SQL) and `label` (used when communicating).

For ecom-specific schemas, watch for these critical column families: `order_id`, `customer_id`/`email`, `created_at`/`processed_at`, `total`/`subtotal`/`tax`/`shipping`, `currency`, `financial_status` (paid/refunded/partially-refunded), `fulfillment_status`, `line_items` (often nested), `discount_codes`, `customer_segment` (new/returning).

### 1e. Sample the data

Sample each dataset to verify contents. For wide tables (>15 columns), sample only the columns relevant to the analysis. Flag anything off (empty columns, unexpected formats, null-heavy fields, refund flags missing, etc.) before proceeding.

## Step 2: Compute Metrics via SQL

Always compute metrics via SQL in `get-data`. Floating-point aggregations over thousands of rows in-context are unreliable; the Coupler.io SQL engine handles this correctly.

### Working with multiple datasets

**Date alignment:** Different sources use different date formats and grains (Shopify: ISO timestamp; GA4: date string; Stripe: Unix). Aggregate to a common grain before comparing.

**Currency normalization:** Multi-currency stores need explicit normalization (always confirm the conversion source/rate with the user before reporting).

**Refund handling — critical:** Decide upfront whether you're reporting `gross revenue` (includes refunded orders), `net revenue` (excludes refunds), or `paid revenue` (excludes pending). The user often doesn't realize these differ. State your choice in the output and check the assumption.

**New vs. returning customers:** If joining order data with customer history, define 'new' explicitly (first-ever order in the data window vs. first order in the analysis window). Flag the choice.

**Joining sessions and orders:** Web session data (GA4) and order data (Shopify) often don't share a join key. Be explicit about whether you're presenting them side-by-side (no join) or attempting an attribution join (typically requires `client_id` or UTM consistency).

## Step 3: Draft Findings and Get User Feedback

Before generating a full analysis, present a brief summary — the 3–5 most important numbers, anomalies, and direction. Wait for the user's response before continuing.

## Step 4: Build the Analysis

Based on what the user asked for, follow the appropriate analysis path:

### Funnel Analysis

Quantify the path from visit → product view → add to cart → checkout → purchase. Key stages and standard metrics:

- **Conversion rate (overall)** — purchases / sessions for the period.
- **Add-to-cart rate** — add-to-cart events / product views.
- **Cart-to-checkout rate** — checkouts initiated / carts.
- **Checkout-to-purchase rate** — completed purchases / checkouts initiated. (Cart abandonment = 1 - this rate, by convention.)

Identify the biggest drop-off stage. A funnel with strong product-view → add-to-cart but weak checkout → purchase signals checkout friction (shipping cost surprise, payment issues, account-required friction). A weak product-view → add-to-cart suggests product/pricing/imagery issues.

Flag asymmetries: if mobile and desktop convert very differently, present them separately.

### Cohort & Retention Analysis

Group customers by acquisition month/week. Compute repeat-purchase rate at month 1, 2, 3, 6, 12. Healthy ecom businesses see clear retention plateaus; declining cohorts signal product/experience issues.

Report the curve, not just a single number. "Month-3 repeat rate has dropped from 22% (Q1) to 14% (Q3)" tells the operator more than "repeat rate is 14%".

### AOV / Revenue Mix

- **AOV (Average Order Value)** = total revenue / number of orders. Track period-over-period.
- **AOV by segment** — new vs. returning customers, channels, geographies, top SKUs. Returning customers should typically have higher AOV; if not, investigate.
- **Revenue mix** — share of revenue from new vs. returning customers, top 10 SKUs vs. long tail, full-price vs. discounted. Concentrations >40% in any single SKU/channel are risk concentrations to flag.
- **Discount load** — share of orders/revenue using a discount code. If creeping up over time, margin is at risk.

### Repeat Purchase / Lifetime Value

- **Repeat purchase rate** — share of customers with 2+ orders in the window.
- **Days between purchases (median)** — gives a sense of replenishment cadence.
- **Customer LTV proxy** — average revenue per customer cohort over a fixed window (e.g., 12-month LTV).

Distinguish between LTV (true lifetime, requires long history) and windowed LTV (proxy, comparable across cohorts). Always state the window.

### Anomaly Detection and Metric Investigations

Any time the analysis involves investigating a change, drop, or spike — whether the user explicitly asks 'why did revenue drop' or you notice unusual patterns during a routine report — apply this framework:

**Severity classification:**
- **Informational** — within 1 standard deviation of trailing 4-week average, or <10% change. Note it.
- **Warning** — 1–2 standard deviations, or 10–30% change. Investigate, present hypotheses.
- **Critical** — >2 standard deviations, >30% change, or any metric collapsing to zero. Lead with this finding.

**Baseline comparison:** Compare against same day-of-week last week, trailing 4-week average for the same day-of-week, and same period last year (seasonality matters a lot in ecom — Black Friday, holiday, Mother's Day, back-to-school).

**Root cause investigation steps:**
1. **Isolate the scope** — one channel, one product, one geo, or everything? Break down by available dimensions.
2. **Check data freshness** — did the dataflow actually run? Partial-day data masquerading as a 'drop' is the most common false alarm.
3. **Check upstream changes** — site speed, payment provider issues, inventory stockouts, paid traffic pauses, email send pauses, promo schedule changes.
4. **Check for data issues** — duplicate orders, refund spikes counted as new orders, currency conversion bugs.
5. **Present hypotheses ranked by likelihood** — "Most likely: SKU X stocked out on the 12th, accounts for 60% of the revenue drop. Less likely: paid social CPM spike (only 8% of acquisition)."

## Step 5: Present Results

Lead with the headline, use plain language, ensure every finding has a 'So what?' and 'Now what?', structure for scannability.

**Abbreviation expansion:** First time using AOV, LTV, CAC, ROAS, CR, etc. — expand it. After first use, the abbreviation alone is fine.

**Currency:** Always state the currency on first use. If multi-currency, normalize and state the conversion approach.

## Rules & Edge Cases

- Always mention data freshness (when the dataflow last ran) before presenting metrics. A report on 5-day-old ecom data needs that context.
- State revenue convention (gross/net/paid) on first use; never silently switch mid-analysis.
- Refunds and chargebacks: if not in scope of the data, say so explicitly. Don't pretend net revenue when you only have gross.
- Returning customer definitions: when in doubt, ask. 'New within window' vs. 'first ever' produce very different cohort numbers.
- Inventory/stockouts: a revenue drop with no traffic drop is almost always a stockout or pricing change — check inventory data if available.
- Partial-week comparisons: never compare a full week to a partial week without flagging it. Same for partial month, partial quarter.
- Promotion effects: Black Friday week, sale-week promotions, and first-purchase discounts skew AOV and CR. Call out the promo context when comparing periods that include/exclude them.
- Round numbers appropriately: AOV/revenue to whole currency units for large values; rates to 1 decimal percent.
- If a dataflow's last execution failed or is stale (>1 day for a daily-refresh ecom flow, >12h for hourly), warn the user before proceeding.
