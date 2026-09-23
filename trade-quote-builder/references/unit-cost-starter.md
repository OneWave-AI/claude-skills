# Unit Cost Starter

**EXAMPLE PLACEHOLDERS ONLY. These are not market rates.** They exist so a first draft can run end to end. Replace every number with the business's own payroll, supplier invoices, and job history before a quote goes to a client. Label any output that still uses these numbers as containing placeholders.

Why it matters: wages, burden, and material prices vary a lot by region, season, supplier, and crew. A quote built on someone else's averages is a guess dressed up as an estimate.

## How to build real numbers

1. **Base wage per role.** Take it from payroll, not from job ads.
2. **Labor burden %.** Add up a year of employer payroll taxes, workers comp premiums, general liability allocated to payroll, health and retirement contributions, paid time off, and training. Divide by total base wages. Include paid-but-not-billable time (shop time, drive time, callbacks) either here or in overhead, but not both.
3. **Overhead recovery.** Take annual overhead (office rent, office staff, trucks not charged to jobs, insurance not in burden, software, marketing, accounting) and divide it by annual direct job cost to get `pct_of_cost`, or by annual billable labor hours to get `per_labor_hour`. Labor-heavy trades usually recover overhead better per hour; material-heavy trades per cost.
4. **Production rates** (hours per unit). Pull from past jobs: actual hours divided by actual quantity. Adjust for access, height, occupied spaces, and crew experience.
5. **Material costs.** Use current supplier quotes. Keep the quote date on file, and keep the quote validity window short when prices are moving.
6. **Target margin.** Set it from what the business needs to earn after overhead, then check it against what jobs actually made (see a job profitability review).

## Public data you can look up (then adapt locally)

- US wages by occupation and metro area: Bureau of Labor Statistics, Occupational Employment and Wage Statistics, https://www.bls.gov/oes/
- US employer cost of benefits as a share of compensation: Bureau of Labor Statistics, Employer Costs for Employee Compensation, https://www.bls.gov/ecec/

These describe broad averages, not what a given shop pays or charges. Use them only to sanity-check the business's own numbers.

## Placeholder values used in the examples

| Input | Placeholder | Replace with |
|---|---|---|
| Lead technician wage | $34.00/hr | payroll |
| Installer / painter wage | $24.00 to $25.00/hr | payroll |
| Helper wage | $19.00/hr | payroll |
| Labor burden | 28% to 32% of wage | your burden calculation |
| Overhead | 10% to 15% of cost, optional $/labor hour | your overhead calculation |
| Contingency | 3% to 5% | job risk; 0 if hidden conditions are excluded |
| Target margin | 25% (or 50% markup, which is 33.3% margin) | your target |
| Paint spread rate | 350 sf per gallon per coat | product data sheet |
| Paint production | 0.0125 hr per sf of wall (both coats) | your job history |
| Material waste | 0% boxed equipment, 10% to 15% cut or bulk goods | your job history |

## Waste factor guidance (placeholders, confirm per material)

- Boxed equipment, fixtures, devices: 0%, but set it explicitly so the script knows it was considered.
- Sheet goods, flooring, tile, shingles, sheet metal: waste rises with cuts, angles, and pattern matching.
- Liquids (paint, sealant): coverage math first, then waste, then round up to the container size with `pack_size`.
- Pipe, wire, cable: add waste for offcuts and routing, then round to the reel or stick length.
