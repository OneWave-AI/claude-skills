# Phase Output Formats

Console output templates for each phase and the final completion summary.

## Phase 1 Output

```
PHASE 1 COMPLETE: Document Inventory & Classification
======================================================

Documents Found: [count]
Categories Represented: [count]/16
Estimated Completeness: [percentage]

INVENTORY:
| # | File | Category | Pages/Rows | Key Dates | Status |
|---|------|----------|------------|-----------|--------|
| 1 | ... | ... | ... | ... | Reviewed |

GAP ANALYSIS:
- MISSING: [category] -- [impact of absence]
- MISSING: [category] -- [impact of absence]
- INCOMPLETE: [category] -- [what is missing]
```

## Phase 2 Output

```
PHASE 2 COMPLETE: Contract & Legal Analysis
=============================================

Contracts Analyzed: [count]
Key Terms Extracted: [count]
Non-Standard Provisions Flagged: [count]

PRIMARY TRANSACTION TERMS:
- Transaction Type: [type]
- Consideration: [amount/structure]
- Closing Conditions: [summary]

TERM EXTRACTION TABLE:
| Term | Value Found | Market Standard | Deviation | Risk |
|------|-------------|-----------------|-----------|------|
| ... | ... | ... | ... | ... |

NON-STANDARD PROVISIONS:
1. [Document] -- [Provision] -- [Concern] -- [Recommendation]
2. ...

MISSING PROTECTIONS:
1. [Protection] -- [Standard expectation] -- [Impact of absence]
2. ...
```

## Phase 3 Output

```
PHASE 3 COMPLETE: Financial Analysis
======================================

Financial Documents Analyzed: [count]
Years of Historical Data: [count]
Projection Period: [years]

KEY FINANCIAL METRICS:
| Metric | Year -3 | Year -2 | Year -1 | Current | Projected |
|--------|---------|---------|---------|---------|-----------|
| Revenue | | | | | |
| Growth Rate | | | | | |
| Gross Margin | | | | | |
| EBITDA | | | | | |
| EBITDA Margin | | | | | |
| Free Cash Flow | | | | | |
| Net Debt | | | | | |

EBITDA ADJUSTMENTS ANALYSIS:
| Adjustment | Amount | Reasonable? | Rationale |
|------------|--------|-------------|-----------|
| ... | ... | ... | ... |

PROJECTION ASSESSMENT:
- Realism Score: [1-10]
- Key Risk: [description]
- Downside Scenario Impact: [description]

RED FLAGS IDENTIFIED:
1. [Flag] -- [Severity] -- [Evidence] -- [Implication]
2. ...

FINANCIAL STRENGTHS:
1. [Strength] -- [Evidence]
2. ...
```

## Phase 4 Output

```
PHASE 4 COMPLETE: Risk Assessment & Scoring
=============================================

Total Findings: [count]
Critical: [count] | High: [count] | Medium: [count] | Low: [count]

COMPOSITE DEAL RISK SCORE: [score] -- [band label]

RISK HEAT MAP:
                    | Remote | Unlikely | Possible | Likely | Almost Certain |
| CRITICAL          |        |          |          |        |                |
| HIGH              |        |          |          |        |                |
| MEDIUM            |        |          |          |        |                |
| LOW               |        |          |          |        |                |

(Populate cells with finding reference numbers)

CRITICAL FINDINGS (require immediate attention):
1. [Finding ID] -- [Description] -- [Source Document] -- [Recommended Action]
2. ...

HIGH FINDINGS:
1. ...

MEDIUM FINDINGS:
1. ...

LOW FINDINGS:
1. ...

RISK-TO-MITIGATION MAP:
| Finding | Severity | Recommended Mitigation | Estimated Impact |
|---------|----------|----------------------|------------------|
| ... | ... | ... | ... |
```

## Progress Reporting

At the start of each phase, print:

```
[PHASE N/5] Starting: [Phase Name]
```

At the end of each phase, print the phase output summary above.

## Final Completion Summary

```
ANALYSIS COMPLETE
==================
Report written to: [path]/deal-room-analysis.md

Documents analyzed: [count]
Phases completed: 5/5
Deal Risk Score: [score] -- [band]
Critical findings: [count]
High findings: [count]
Negotiation items: [count]

Top 3 findings requiring immediate attention:
1. [finding]
2. [finding]
3. [finding]
```
