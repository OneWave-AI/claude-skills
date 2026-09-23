# Metric definitions that change the answer

Most "wrong numbers" are really the right arithmetic on the wrong definition. For every metric below: pick the stated default when the user has not said otherwise, name it in the answer, and give the one or two alternatives that would move the number by a meaningful amount. Ask first only when the alternatives differ by more than the user could plausibly tolerate (for example, a board number, or a gap over 10%).

Each entry lists: the competing definitions, the default to use, and what to confirm.

## Revenue

| Definition | What it includes | Typical source |
|---|---|---|
| Gross sales / bookings | Order value before discounts, refunds, tax | Shopify "Gross sales", CRM closed-won amount |
| Net sales | Gross minus discounts minus returns/refunds | Shopify "Net sales" |
| Net revenue (payments) | Charges minus refunds minus processor fees | Stripe balance / payouts |
| Recognized revenue | Earned in the period under accrual accounting (an annual prepay is spread over 12 months) | QuickBooks P&L, rev-rec schedules |
| Cash collected | Money received in the period, regardless of when earned | Bank, Stripe payouts |

Default: net sales (gross minus discounts and refunds), excluding tax, shipping, and cancelled or failed orders.

Confirm:
- Tax and shipping: in or out? Shopify "Total sales" includes both.
- Refund timing: charge against the original order's period (order cohort) or the period the refund was issued (cash view). The two views can move a quarter's number by the size of any late refund.
- Status values that count: `paid`, `fulfilled`, `partially_refunded`? And are `pending` and `authorized` in or out?
- Currency: report currency, and which FX rate (transaction-date rate, month-average, or the single fixed rate you have). Say which.
- Stripe amounts are integer minor units (cents): divide by 100, except for zero-decimal currencies (JPY, KRW).

## MRR and ARR

- MRR = sum of the normalized monthly value of active subscriptions on a date. Annual plans divided by 12, quarterly by 3.
- Choices that change it: whether discounts are netted (default: yes, use what the customer actually pays), whether trials and $0 plans count (default: no), whether past-due subscriptions count (default: yes until canceled, and state it), whether usage or overage fees count (default: no, they are not recurring), and whether one-time setup fees count (never).
- ARR = MRR x 12 for subscription businesses. Do not call annualized total revenue "ARR" when part of it is one-off.
- Measure at a point in time (end of month), not summed across a month.

## Churn

| Type | Formula |
|---|---|
| Logo (customer) churn | customers lost in period / customers at start of period |
| Gross revenue churn | MRR lost to cancellations + downgrades / MRR at start |
| Net revenue churn | (MRR lost - expansion MRR from existing customers) / MRR at start; can be negative |
| Net revenue retention (NRR) | (start MRR + expansion - contraction - churn) / start MRR, same cohort |

Default: logo churn, monthly. Confirm: monthly vs annual (monthly 3% is not annual 36%; annual = 1 - (1 - 0.03)^12, which is about 30.6%), whether customers who joined during the period are in the denominator (default: no), and whether a downgrade to a free plan counts as churn (default: yes).

## Active customers / active users

The single most invented definition. "Active" might mean any of:
- placed at least one order in the last 30 / 90 / 365 days
- has a live subscription on the date
- logged in or performed a key action in the window (DAU/WAU/MAU)
- has a status field equal to "Active" in the CRM, which is often stale

Default: had at least one paid transaction in the trailing 90 days ending on the export's latest date. Always state the window, the event, and the as-of date. Never mix a CRM status field with behavioral activity.

## Customer count

Confirm the entity: account, company, billing entity, email, or person. One company can have several customer IDs, and one email can have several accounts. Distinct `customer_id` is the default. Say how many duplicates you found by name or email.

## CAC (customer acquisition cost)

- Blended CAC = total sales + marketing spend / new customers in the period.
- Paid CAC = ad spend only / customers attributed to paid channels.
- Choices: whether salaries, tools, and agency fees are in spend (blended: yes, paid: no), attribution model (last click is the ad platforms' default, and each platform over-claims), and lag (spend this month converts next month).
- Default: blended, same-period, and state that ad platforms double count conversions across platforms.

## LTV (lifetime value)

- Simple: ARPA x gross margin % / monthly churn rate.
- Historical: actual cumulative gross margin per customer cohort to date.
- Choices: revenue vs gross margin (default: gross margin; revenue LTV overstates), churn source, and whether to cap the lifetime (default: cap at 36 months or say it is uncapped). A very low churn rate makes the simple formula explode; say so.

## AOV (average order value)

- AOV = net sales / number of orders, for the same order set.
- Choices: gross vs net numerator (default: net, pre-tax, pre-shipping), include $0 or fully refunded orders (default: exclude cancelled, include refunded with their net), and mean vs median (report the mean and give the median when a few large orders skew it).

## Conversion rate

- Rate = conversions / the denominator, and the denominator is the definition: sessions, users, visitors, leads, or trials.
- Choices: session vs user basis (GA4 reports both), which event counts as a conversion, and the attribution window.
- Default: orders / sessions for e-commerce, closed-won / opportunities created in the same cohort for sales pipelines. Never divide this month's wins by this month's new leads when the sales cycle is longer than a month; use a cohort.

## Pipeline and win rate

- Win rate by count vs by value can differ a lot. Default: by count, and give by value alongside.
- Exclude open deals from the denominator. Decide whether "closed lost - no decision" and disqualified leads count (default: yes for lost, no for disqualified before qualification).
- CRM exports often carry both `amount` and a weighted `expected_revenue`. Never sum the weighted column and call it pipeline.

## Headcount and HR metrics

- Headcount on a date vs average headcount over the period (turnover uses the average).
- Employees vs contractors vs interns: confirm which are included.
- Turnover = separations in period / average headcount. Say whether it is voluntary only or total.
- FTE vs people: two half-time people are 1 FTE and 2 headcount.

## Ad platform metrics

- Spend, clicks, and impressions sum cleanly. Rates (CTR, CPC, ROAS) do not: recompute them from summed parts, never average the per-row rates.
- Platform-reported conversions and conversion value use each platform's own attribution window, so two platforms' conversions do not add up to the store's orders.
