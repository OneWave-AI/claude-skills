# Phase Procedures

Detailed procedures for each of the five analytical phases. Execute phases sequentially. Each phase produces structured intermediate findings that feed the next.

---

## Phase 1: Document Inventory & Classification

### Objective
Catalog every document in the deal room directory. Classify each by type, assess completeness, and flag gaps.

### Procedure

1. Scan the directory using Glob to find all files recursively:
   - `**/*.pdf`, `**/*.docx`, `**/*.xlsx`, `**/*.csv`, `**/*.txt`, `**/*.md`, `**/*.png`, `**/*.jpg`, `**/*.jpeg`
   - Check for subdirectory structure that reveals organizational intent (folders named "Legal", "Financial", "HR").

2. Read each document using the Read tool. For PDFs, use the `pages` parameter to sample key pages (cover page, table of contents, signature pages). For spreadsheets, read headers and first rows to understand structure.

3. Classify each document using the category table in `references/classification.md`.

4. Assess completeness by checking for standard deal room requirements:
   - Is there a primary transaction agreement (SPA, APA, or Merger Agreement)?
   - Are audited financial statements present for at least 2-3 years?
   - Is there a cap table or equity summary?
   - Are material contracts identified and included?
   - Are employment agreements for key executives present?
   - Is there litigation disclosure?
   - Are IP schedules present?
   - Are tax returns or tax opinions included?

5. Produce a structured inventory table and a gap analysis identifying missing document categories. Use the format in `references/output-formats.md`.

---

## Phase 2: Contract & Legal Analysis

### Objective
Extract and analyze all legal terms, obligations, rights, and risk provisions from every contract and agreement in the deal room.

### Procedure

1. Prioritize documents for review:
   - Priority 1: Master transaction agreement (SPA, APA, Merger Agreement)
   - Priority 2: Ancillary agreements (non-competes, TSAs, IP assignments)
   - Priority 3: Material third-party contracts (customer agreements, vendor contracts, leases)
   - Priority 4: Employment agreements for C-suite and key personnel
   - Priority 5: All remaining legal documents

2. For each contract, extract the applicable terms listed in `references/term-extraction-checklist.md`.

3. Compare extracted terms to market standards using the benchmarks in `references/market-standards.md`.

4. Flag non-standard or concerning provisions:
   - Terms significantly outside market ranges
   - Ambiguous language that could be interpreted adversely
   - Missing standard protections
   - Asymmetric provisions favoring one party
   - Provisions that may be unenforceable in relevant jurisdictions
   - Unusual definitions or carve-outs

5. Produce the Phase 2 output using the format in `references/output-formats.md`.

---

## Phase 3: Financial Analysis

### Objective
Analyze all financial documents to assess the target's financial health, validate projections, and identify financial red flags.

### Procedure

1. Extract historical financial data from statements and spreadsheets using the line items in `references/financial-analysis.md`.

2. Analyze projections and forecasts (if provided):
   - Compare projected growth rates to historical performance
   - Assess reasonableness of margin expansion assumptions
   - Identify hockey-stick patterns and challenge underlying assumptions
   - Compare projections to industry benchmarks
   - Run sensitivity analysis: what happens at 75% and 50% of projected revenue?
   - Identify key assumptions driving the model (customer wins, pricing changes, cost reductions)
   - Build a bridge analysis from current state to projected state

3. Assess Quality of Earnings indicators:
   - Revenue recognition policies and changes
   - Non-recurring adjustments to EBITDA (sum total and trend)
   - Related-party transactions
   - Change in accounting policies or estimates
   - Audit qualifications or emphasis of matter paragraphs
   - Management override indicators

4. Run valuation sanity checks:
   - Implied multiples (EV/Revenue, EV/EBITDA, P/E) vs. comparable transactions
   - Implied growth rate embedded in purchase price
   - Breakeven analysis on investment return

5. Apply the financial red flags checklist in `references/financial-analysis.md`.

6. Produce the Phase 3 output using the format in `references/output-formats.md`.

---

## Phase 4: Risk Assessment & Scoring

### Objective
Synthesize findings from Phases 1-3 into a comprehensive risk matrix with severity ratings, likelihood assessments, and potential financial impact estimates.

### Procedure

1. Compile all findings from Phases 1, 2, and 3 into a unified risk register.

2. Rate each finding using the severity and likelihood scales in `references/risk-scoring.md`.

3. Categorize each risk into the domains listed in `references/risk-scoring.md`.

4. Calculate a composite Deal Risk Score using the formula and scoring bands in `references/risk-scoring.md`.

5. Map risks to mitigation strategies using the mitigation table in `references/risk-scoring.md`.

6. Produce the Phase 4 output using the format in `references/output-formats.md`.

---

## Phase 5: Synthesis & Report Generation

### Objective
Compile all phase outputs into a single, professional-grade due diligence report written to `deal-room-analysis.md` in the deal room directory.

### Procedure

1. Write the report using the Write tool at `[deal-room-directory]/deal-room-analysis.md`, following the exact structure in `references/report-template.md`.

2. Ensure the report meets professional standards:
   - Every factual claim references a specific document
   - Risk ratings are consistently applied
   - Market comparisons use the benchmarks from Phase 2
   - Negotiation recommendations are actionable and specific
   - The tone is measured, analytical, and objective
   - No speculative language without explicit qualification
   - All dollar amounts and percentages are clearly sourced

3. Print the completion summary to the user using the format in `references/output-formats.md`.
