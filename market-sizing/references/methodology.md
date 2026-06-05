# Calculation Methodology

## Top-Down Approach

Start from the broadest defensible market number and narrow progressively.

```
TAM (Top-Down) = Total Industry Revenue in Category
SAM (Top-Down) = TAM x Geographic Filter x Segment Filter x Product-Fit Filter
SOM (Top-Down) = SAM x Realistic Capture Rate (based on competitive dynamics)
```

Steps:
1. Identify the broadest relevant market figure from research (cite source).
2. Apply geographic adjustment (what % of the global market is the target geography?).
3. Apply segment adjustment (what % of the geographic market is the target customer segment?).
4. Apply product-fit adjustment (what % of the segment actually needs this specific product/service?).
5. Apply realistic market share capture rate for SOM (typically 1-5% for early-stage, 5-15% for growth-stage, varies by market concentration).

## Bottom-Up Approach

Build from unit economics upward.

```
TAM (Bottom-Up) = Total Potential Customers x Average Annual Revenue per Customer
SAM (Bottom-Up) = Reachable Customers x Average Annual Revenue per Customer
SOM (Bottom-Up) = Target Customers in [timeframe] x Expected Revenue per Customer
```

Steps:
1. Count total potential customers (companies, users, or units depending on the model).
2. Determine average revenue per customer from pricing data and competitor benchmarks.
3. Multiply for TAM.
4. Narrow to reachable customers (those matching ICP, in target geography, using relevant technology, etc.).
5. Multiply for SAM.
6. Estimate realistic customer acquisition over a 3-5 year horizon for SOM.

## Triangulation

Compare top-down and bottom-up results:
- Within 2x of each other: good convergence, present the range.
- Diverge by more than 2x: investigate the gap, identify which assumptions drive the difference, and explain.
- Present a "best estimate" that weighs the more reliable methodology more heavily.
- Always present all three numbers (top-down, bottom-up, best estimate) for transparency.

## Sensitivity Analysis

For each of TAM, SAM, and SOM, produce three scenarios:

| Scenario | Description | Methodology |
|---|---|---|
| **Conservative** | Pessimistic but defensible | Lowest credible growth rate, smallest addressable segment, lowest ACV, highest competitive pressure |
| **Base Case** | Most likely outcome | Median estimates from research, moderate assumptions |
| **Aggressive** | Optimistic but not fantasy | Highest credible growth rate, broadest defensible segment, highest ACV, favorable competitive dynamics |

Identify the top 3-5 variables that most impact the sizing and show how each shifts the output. Present as a tornado chart description.

## Growth Projections

Project market size forward 5 years:
1. Apply researched CAGR to base case TAM/SAM.
2. Model SOM growth separately (company execution curve, not just market growth).
3. Account for market maturation (growth deceleration in later years if applicable).
4. Flag any structural breaks (regulation changes, technology shifts, platform transitions).

## Competitive Landscape Sizing

Estimate market share distribution:
1. List the top 5-10 competitors by estimated revenue.
2. Calculate their combined market share of SAM.
3. Identify the remaining white space or fragmented share.
4. Assess barriers to entry (high/medium/low).
5. Map competitive positioning (price vs. feature, enterprise vs. SMB, etc.).

## Common Pitfalls to Avoid

- **Double-counting**: Ensure TAM segments do not overlap. If sizing by vertical and by company size, pick one dimension.
- **Conflating TAM and SAM**: TAM is the theoretical max. SAM must reflect real constraints (geography, segment, product fit). Never present TAM as if it were SAM.
- **Stale data**: Prefer data from the last 12-24 months. Flag anything older with a note about potential staleness.
- **Single-source reliance**: Triangulate market size from at least 2-3 independent sources when possible.
- **Aspirational SOM**: Ground SOM in realistic competitive dynamics, go-to-market capacity, and sales cycle length. A 20% SOM in year 1 for a startup entering a crowded market is not credible.
- **Ignoring market concentration**: A $10B TAM with 3 dominant players at 80% share is very different from a $10B TAM that is highly fragmented.
- **Currency and year mismatches**: Always normalize to a single currency and base year.
- **Circular reasoning**: Do not use your own TAM estimate as a source for your SAM estimate methodology. Each must have independent grounding.
