# Risk Scoring Framework

## Severity Scale

| Rating | Definition | Financial Impact Proxy |
|--------|------------|----------------------|
| CRITICAL | Deal-breaker or fundamental value impairment. Requires resolution before closing or significant price adjustment. | >15% of purchase price at risk |
| HIGH | Material risk requiring contractual protection, specific indemnity, or price adjustment. | 5-15% of purchase price at risk |
| MEDIUM | Notable concern requiring monitoring, disclosure, or minor contractual protection. | 1-5% of purchase price at risk |
| LOW | Minor issue requiring awareness but unlikely to impact deal value materially. | <1% of purchase price at risk |

## Likelihood Scale

| Rating | Definition |
|--------|------------|
| Almost Certain | >90% probability of materializing |
| Likely | 60-90% probability |
| Possible | 30-60% probability |
| Unlikely | 10-30% probability |
| Remote | <10% probability |

## Risk Domains

- Legal / Contractual Risk: Inadequate protections, unfavorable terms, enforceability concerns
- Financial Risk: Revenue quality, margin sustainability, projection credibility, debt
- Operational Risk: Key person dependency, customer concentration, supplier risk
- Regulatory Risk: Compliance gaps, pending regulatory changes, approval uncertainty
- IP / Technology Risk: IP ownership gaps, open source contamination, technology obsolescence
- Tax Risk: Uncertain tax positions, transfer pricing exposure, structural tax issues
- Integration Risk: Cultural mismatch, system compatibility, customer retention during transition
- Market Risk: Competitive threats, market decline, disruption risk
- Litigation Risk: Pending or threatened litigation, historical patterns
- Environmental / ESG Risk: Environmental liabilities, ESG compliance gaps

## Composite Deal Risk Score

```
Deal Risk Score = Sum of (Severity Weight x Likelihood Weight) for all findings

Severity Weights: CRITICAL=10, HIGH=5, MEDIUM=2, LOW=1
Likelihood Weights: Almost Certain=5, Likely=4, Possible=3, Unlikely=2, Remote=1

Scoring Bands:
0-25:   LOW RISK -- Standard deal protections sufficient
26-50:  MODERATE RISK -- Enhanced protections and specific indemnities recommended
51-100: HIGH RISK -- Significant price adjustment or structural changes needed
100+:   CRITICAL RISK -- Recommend reconsidering deal or fundamental restructuring
```

## Risk-to-Mitigation Map

| Mitigation Type | When to Apply |
|-----------------|---------------|
| Price Reduction | Quantifiable, certain financial impact |
| Specific Indemnity | Identified contingent liability with uncertain timing/amount |
| Escrow / Holdback | Post-closing adjustment risk, earnout uncertainty |
| R&W Insurance | Broad contractual risk transfer, supplement to indemnification |
| Closing Condition | Risk that must be resolved before transaction closes |
| Covenant / Restriction | Ongoing behavioral risk requiring contractual guardrails |
| Walk Away | Unmitigable risk exceeding deal value |
| Further Diligence | Insufficient information to assess risk |
