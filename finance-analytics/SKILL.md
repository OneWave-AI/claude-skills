---
name: finance-analytics
description: Use this skill when the user wants to analyze financial performance, review P&L health, monitor
  MRR/ARR, investigate margin or cost trends, build a finance report, check cash flow or runway, or answer
  questions about their accounting/billing data. Triggers include 'how is revenue trending', 'gross margin',
  'MRR breakdown', 'churn impact on ARR', 'why did costs go up', 'operating expenses', 'cash runway',
  'P&L review', 'EBITDA', 'cost per acquisition trend', 'pull my QuickBooks numbers', 'finance report'.
  Reads live data from your Coupler.io workspace via the Coupler.io MCP connector.
---

# Finance Analytics

Analyze financial performance using data from Coupler.io dataflows (QuickBooks, Xero, Stripe, NetSuite, Sage, billing systems). This skill guides you through retrieving accounting and revenue data, computing P&L, margin, subscription, and cash metrics, detecting anomalies, and presenting actionable insights a finance lead can act on.

## Step 0: Context Check (Pre-requisite)

Before starting any analysis, the **Data Context Check** skill (`generate-data-set-context`) runs as a gate. It calls `get-schema` on each target dataset to determine whether meaningful context (chart of accounts mapping, entity/subsidiary structure, currency conventions, fiscal calendar, accrual vs. cash convention) is attached.

- If context exists → proceed to Step 1.
- If context is missing → the user is offered the option to generate it first.

Do not duplicate this check in Step 1d.

## Step 1: Discover and Select Data Sources

### 1a. Discover available data

Default to `search-datasets` with finance-flavored keywords — `quickbooks`, `xero`, `netsuite`, `stripe`, `sage`, `gl`, `invoice`, `revenue`, `mrr`, `arr`, `bank`, or whatever system the user named. Search keeps the response small and lands on the right dataflow when the domain is known.

Fall back to `list-datasets` only when the user is genuinely browsing or hasn't given any source/keyword to anchor on. Each dataflow represents a data pipeline (e.g. "QuickBooks GL", "Stripe Charges", "NetSuite Revenue", "Xero Invoices", "Bank Transactions").

### 1b. Select relevant datasets

**Unambiguous match (1 dataflow)** → use it; mention which one.

**Obvious candidates (2–3)** → state your selection with one-line reasoning, proceed but invite corrections.

**Ambiguous (5+, or unclear)** → present best candidates (up to 5–7) grouped by source/scope, with reasoning, and wait for confirmation:

```
I found 3 dataflows likely relevant to your MRR question:
  1. stripe_subscriptions — has plan, MRR amount, status
  2. quickbooks_gl — has revenue accounts, but at journal grain
  3. salesforce_opportunities — has booked ARR, less useful for recognized
Should I use Stripe alone, or combine Stripe and QuickBooks for cross-check?
```

**Hard gate only when ambiguous.** If you're confident and stated reasoning, proceed.

### 1c. Get dataflow details

Call `get-dataflow` for each candidate. Note `schedule` (data freshness), source health, and the close status of any GL data — finance refreshes are often slower than transactional sources.

### 1d. Understand the data structure

Call `get-schema` on each target dataset. If context was generated in Step 0, use the enriched schema directly.

For finance schemas, watch for these critical column families: account/account_code (chart of accounts), entity_id/subsidiary, currency, transaction_date/posting_date, amount (signed: positive = credit, varies by source), invoice_status (paid/open/voided), customer_id, plan_id, billing_period_start/end, refund flags.

### 1e. Sample the data

Sample each dataset to verify contents. Watch specifically for: signed-amount conventions (debit-positive vs. credit-positive), currency mixing, journal entry duplicates, voided/reversed entries that need exclusion. Flag anything off before proceeding.

## Step 2: Compute Metrics via SQL

Always compute via SQL in `get-data`. Floating-point aggregations over thousands of rows in-context are unreliable.

### Working with multiple datasets

**Date alignment:** Posting date vs. transaction date vs. service date can differ — confirm which the user wants. Use fiscal calendar if the company doesn't operate on calendar months.

**Currency normalization:** Multi-entity companies need consolidation; always state your conversion approach (period-end FX vs. average FX vs. native).

**Cash vs. accrual:** Critical distinction. Confirm which convention the user wants. Stripe data is mostly cash; QuickBooks/NetSuite GL can be either depending on configuration.

**Recognized vs. booked:** Booked = contract signed (Salesforce). Billed = invoice issued. Recognized = ASC 606 revenue recognition (subscription pro-ration). Don't conflate; ask if unclear.

**Voided/reversed entries:** GL data often includes voided journals — exclude them in the WHERE clause. Don't double-count refunds as new revenue.

## Step 3: Draft Findings and Get User Feedback

Before generating a full analysis, present a brief summary — the 3–5 most important numbers, anomalies, and direction. Wait for user response before continuing.

## Step 4: Build the Analysis

### P&L Review

Standard structure: Revenue → COGS → Gross Profit → Operating Expenses → Operating Income → Other → Net Income.

- **Gross margin %** = (Revenue − COGS) / Revenue. Track period-over-period; a 2-point compression is meaningful.
- **Operating margin %** = Operating Income / Revenue.
- **Expense breakdown by category** (Sales & Marketing, R&D, G&A) — flag categories growing faster than revenue.
- Period-over-period and year-over-year comparisons. State the comparison basis explicitly.

Flag concentration: if one customer/product is >20% of revenue, call it out as a concentration risk.

### MRR / ARR & Subscription Health

For SaaS or subscription businesses:

- **MRR** = sum of monthly recurring revenue across active subscriptions. ARR = MRR × 12.
- **MRR movement bridge**: Starting MRR + New + Expansion + Reactivation − Contraction − Churn = Ending MRR. Always reconcile the bridge — gaps reveal data issues or missing categories.
- **Net Revenue Retention (NRR)** = (Starting MRR of cohort + Expansion − Contraction − Churn) / Starting MRR. Healthy SaaS: >100%.
- **Gross Revenue Retention (GRR)** = (Starting MRR − Contraction − Churn) / Starting MRR. Excludes expansion.
- **Logo churn vs. revenue churn** — present both; high logo churn with stable revenue churn signals SMB churn masked by enterprise stability.

### Cash & Runway

- **Cash burn (monthly)** = avg monthly net cash outflow over trailing 3 months.
- **Runway** = current cash balance / monthly burn. State both calendar months and 'months at current burn'.
- **Operating cash flow vs. net income** — divergences signal AR/AP timing issues.

If bank/cash data isn't in scope, say so. Don't extrapolate runway from P&L data without cash data.

### Cost-Center Investigation

When the user asks 'why did costs go up' or 'where is spend growing fastest':

1. Break down the cost category by sub-account or vendor.
2. Compare to prior period at the sub-account level.
3. Identify the top 3 sub-accounts driving the change.
4. Check for one-time items (annual renewals, project spikes) vs. structural increases.
5. Present: "Of the $X increase, $Y is from <vendor/account> renewing on annual cycle, $Z is structural increase in <category>, balance is distributed."

### Anomaly Detection and Metric Investigations

Any time the analysis involves investigating a change, drop, or spike — apply this framework:

**Severity classification:**
- **Informational** — within 1 SD of trailing 4-month average, or <5% change. Note it.
- **Warning** — 1–2 SD, or 5–15% change. Investigate, present hypotheses.
- **Critical** — >2 SD, >15% change, or any metric crossing a covenant/threshold. Lead with this finding.

Finance has tighter sensitivity than marketing/ecom — a 10% gross margin drop is a 'critical' event, not 'warning'.

**Baseline comparison:** Same period prior year (annual seasonality matters in finance), trailing 3-month average, budget if available.

**Root cause investigation steps:**
1. **Isolate the scope** — which entity, which account, which customer/vendor.
2. **Check posting period** — late-arriving journals, period-end accruals, reversal entries.
3. **Check upstream changes** — pricing changes, contract renewals, vendor changes, new accounting policy.
4. **Check for data issues** — duplicate journals, currency conversion errors, voided entries not excluded.
5. **Present hypotheses ranked by likelihood** — "Most likely: annual security audit fee posted to G&A in this month vs. amortized last year. Less likely: structural growth in headcount cost."

## Step 5: Present Results

Lead with the headline, use plain language, ensure every finding has a 'So what?' and 'Now what?', structure for scannability.

**Abbreviation expansion:** First use of MRR, ARR, NRR, GRR, EBITDA, COGS, GAAP, ASC 606, AR, AP, FX — expand it.

**Currency:** Always state on first use. If multi-currency, state your normalization approach (period-end vs. average FX, source of rates).

**Materiality:** Note material vs. immaterial movements. A $5 swing in a $50M revenue line is noise.

## Rules & Edge Cases

- Always state data freshness and the close status (preliminary, soft-closed, hard-closed) before presenting numbers. Pre-close numbers can shift materially.
- State revenue convention (cash, accrual, recognized) on first use; never silently switch.
- Voided/reversed journals must be excluded from totals. If you can't tell which entries are voided, say so.
- Multi-entity / multi-currency: never sum across entities without consolidation. State your consolidation approach.
- Prior-period adjustments and reclassifications: if a prior month was restated, mention it — comparing current period to a restated prior gives different results than to the original.
- Round to materiality: don't report margins to 4 decimals when 1 decimal is enough. Don't report dollar amounts to the cent on totals over $10K.
- Tax: distinguish pre-tax and post-tax metrics explicitly when both exist.
- If a dataflow's last execution failed or is stale (>2 days for a daily GL refresh), warn the user — and consider that GL data is often refreshed less frequently than transactional sources, so 'stale' definitions differ.
