---
name: trade-quote-builder
description: Builds estimates, quotes, and bids for trades and field-service businesses (HVAC, plumbing, electrical, roofing, landscaping, painting, cleaning, remodeling, general contracting, IT/AV installs). Turns a scope into line items with waste factors, burdened labor, materials, equipment, subs, permits, mobilization, contingency, overhead, profit, and tax, then writes a client-ready xlsx (live formulas) and PDF plus an internal cost sheet, with good/better/best options, add-ons, a payment schedule, exclusions, and assumptions. Use whenever someone asks for a quote, estimate, bid, proposal price, or job price, asks "how much should I charge for this job", wants to check a price or margin on a job, or is confused about markup vs margin. Computes deterministically with a script instead of mental math, because models routinely treat a 30% markup as a 30% margin and drop labor burden, waste, and mobilization.
---

# Trade Quote Builder

A quote is a promise priced in advance. The expensive mistakes are not in the unit costs; they are the items nobody priced (permits, disposal, mobilization, burden) and the arithmetic done in someone's head (a 30% markup is only a 23% margin). This skill fixes both: a checklist pass for missing scope, then `scripts/build_quote.py` for every number.

Never do the pricing arithmetic in prose. Write the spec, run the script, and quote its output. The script uses Decimal math and the same rounding as the Excel formulas it writes, so the PDF, the client xlsx, and the internal sheet always agree to the penny.

## Workflow

1. **Gather the scope and the business's numbers.** Ask for: the job (measurements, counts, site conditions, photos or drawings), the trade, and the business's own costs: base wages per role, labor burden %, overhead recovery, target margin or markup, supplier prices, tax rules for their jurisdiction. If they have no numbers, start from `references/unit-cost-starter.md` and label every figure in the output as a placeholder to replace. Never present an invented rate as a market price.
2. **Walk the checklist.** Open `references/scope-checklists.md` for the trade and ask about each commonly forgotten item. Every item ends up either priced as a line or written into `exclusions`. The script also scans the spec and flags common items it cannot find, so an unaddressed permit shows up as a `[CHECK]` line instead of a surprise.
3. **Write the spec** (YAML or JSON, schema below). Model each client-facing line as an assembly of components: materials with waste and pack sizes, labor hours by role, equipment, subs, fees. Put shared scope in `base_items`, tier-specific scope in `tiers`, and optional extras in `add_ons`.
4. **Run it.**
   ```bash
   python scripts/build_quote.py spec.yaml --check          # validate + totals, writes nothing
   python scripts/build_quote.py spec.yaml --out ./quotes   # xlsx + pdf + internal + summary.json
   python scripts/build_quote.py spec.yaml --explain LINE   # show every step for one line
   ```
   Needs `openpyxl`; `pyyaml` for YAML specs; `reportlab` for the PDF (skipped cleanly if missing).
5. **Sanity-check before sending.** Read the totals table and every `[WARN]`:
   - **Net margin vs target.** At-cost pass-throughs and lower sub markups pull the blended margin below target. Decide whether that is intended.
   - **Effective hourly** = (price minus non-labor direct cost) / labor hours. This is what each crew hour brings in to cover wages, burden, overhead, and profit. Compare it to `min_effective_hourly`; if it is low, the hours are too high or the price is too low.
   - **Option ladder.** Good < Better < Best, and the gaps should be explainable to a homeowner in one sentence each.
   - **Hand-check one line** with `--explain` and show the math to the user so they can trust the rest.
6. **Deliver.** Send the client xlsx and/or PDF. Keep `-internal.xlsx` for the business only, since it shows costs and profit. List the assumptions and exclusions in your reply, plus every placeholder the user still has to replace.

## Markup vs margin

State which one you are using every time. The script refuses a spec that sets both.

- Margin = profit / price. Price = cost / (1 - margin).
- Markup = profit / cost. Price = cost x (1 + markup).
- markup = margin / (1 - margin); margin = markup / (1 + markup).
- 20% margin = 25% markup; 25% = 33.3%; 30% = 42.9%; 40% = 66.7%; 50% = 100%.
- Quick answer: `python scripts/build_quote.py --margin-to-markup 0.30`.

In this script the target applies to **loaded cost** (direct + contingency + overhead), so it is a net profit margin. If the business sets `overhead` to 0, the target must be large enough to cover overhead too (a gross margin), and the script warns about it.

## Spec essentials

```yaml
trade: hvac                      # selects the missing-item scan
pricing:
  target_margin: 0.25            # OR target_markup, never both
  by_component: {subs: {markup: 0.15}, fees: {at_cost: true}}
labor:
  burden_pct: 0.32               # payroll tax, workers comp, insurance, benefits
  roles: {lead_tech: {wage: 34.00}, helper: {wage: 19.00, burden_pct: 0.30}}
overhead: {pct_of_cost: 0.15, per_labor_hour: 0}
contingency_pct: 0.03
tax: {mode: charge_on_sell, rate: 0.07, taxable: [materials]}   # or contractor_pays_on_cost, or none
min_effective_hourly: 120
base_items:
  - id: LINE
    section: Installation
    description: Replace refrigerant line set, braze, pressure test, evacuate
    qty: 25
    unit: ft
    materials:
      - {item: Line set 25 ft, qty: 1, unit_cost: 165, waste_pct: 0}
      - {item: Insulation tape, qty: 1.6, unit: roll, unit_cost: 9, waste_pct: 0.10, pack_size: 1}  # buys 2 rolls
      - {item: Fittings, qty_per_unit: 1.4, unit_cost: 1, waste_pct: 0.10}   # scales with line qty
    labor: [{role: installer, hours: 2.5}]          # or hours_per_unit
    subs: [{item: Electrical sub, qty: 1, unit_cost: 425}]
tiers: [{name: Good, description: ..., items: [...]}]   # omit tiers for a single scope
add_ons: [{name: UV light, items: [...]}]
payment_terms: {schedule: [{milestone: Deposit, pct: 0.30}, {milestone: Completion, pct: 0.70}]}
exclusions: [...]
assumptions: [...]
```

Shorthand for simple lines: `unit_cost` (+ `cost_type`, `waste_pct`) and `hours` or `hours_per_unit` (+ `role`) directly on the line. Line flags: `at_cost: true` (pass-through), `lump_sum: true` (hide the unit price). `client.view: lump_sum` hides unit prices on every line.

Tax modes differ by jurisdiction and by job type, so ask rather than assume. `charge_on_sell` charges the client tax on the taxable share of each line. `contractor_pays_on_cost` adds tax to material cost, marks it up with the material, and notes "prices include sales tax on materials". Tell the user to confirm the treatment with their accountant.

## Output

- `<number>-client.xlsx`: Summary (options and add-ons with totals referencing each sheet), one sheet per option, Add-ons, Terms (payment schedule by option, exclusions, assumptions, signature block). Amounts, subtotals, tax, totals, and schedule are live formulas; the last milestone takes the remainder so the schedule sums to the penny.
- `<number>-client.pdf`: the same content as a sendable document.
- `<number>-internal.xlsx`: every component with base qty, waste, order qty, burdened rate, contingency, overhead, loaded cost, pricing rule, sell; per-line profit and margin; per-option summary with gross margin, net margin, markup achieved, labor hours, effective hourly, and all checks.
- `<number>-summary.json`: the same totals and warnings in machine-readable form.

## Worked example

`examples/interior-painting.json` (markup 50%, 6.25% tax paid on materials) produces a $6,180.95 base scope, 33.4% net margin, 68.68 labor hours, $74.26 effective hourly. Hand-check of the walls line (`--explain WALLS`):

```
Paint: 10.57 gal x 1.10 waste = 11.63 -> 12 gal (full cans) x $42 = $504.00, + 6.25% tax = $535.50
  contingency 5% = $26.78; overhead 10% of $562.28 = $56.23; loaded $618.50; x 1.50 = $927.75
Patch kit: $18.00 + $1.13 tax -> loaded $22.10 -> sell $33.14
Labor: 1,850 sf x 0.0125 hr = 23.125 hr x $24.00 x 1.28 burden = $710.40
  contingency $35.52; overhead 10% of $745.92 + 23.125 hr x $6.00 = $213.34; loaded $959.26; x 1.50 = $1,438.89
Line sell $2,399.79 / 1,850 sf = $1.2972 -> $1.30/sf x 1,850 = $2,405.00 (cent rounding added $5.21)
```

`examples/hvac-system-replacement.yaml` shows good/better/best tiers ($11,221.86 / $14,280.56 / $16,999.65 with 7% tax on materials), a sub at 15% markup, and a permit passed through at cost, which is why the blended margin lands near 24% against a 25% target.

## Rules

- Price from the business's own costs. Placeholder rates must be labeled as placeholders in every output until replaced.
- Burden every labor hour. Base wage alone understates labor cost by roughly a quarter to a half.
- Price or exclude every checklist item. Silence becomes a dispute on the job.
- Write exclusions and assumptions in plain language the client can check against the site.
- Payment terms, deposits, cancellation rights, and lien notices are regulated differently by state and country. Point to `references/terms-and-exclusions.md` and tell the user to have their terms reviewed by their own attorney. Do not give legal advice.
- No client names in examples or shared templates; use placeholders.

## References

- `references/scope-checklists.md`: commonly forgotten items per trade.
- `references/unit-cost-starter.md`: EXAMPLE placeholder rates and how to build real ones.
- `references/terms-and-exclusions.md`: plain-language terms, change orders, deposits, exclusion wording.
