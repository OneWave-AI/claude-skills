---
name: sec-filing-puller
description: Pulls financial statement numbers for US public companies straight from SEC EDGAR's free official XBRL APIs (companyfacts, companyconcept, frames, submissions) into a cited table. Every value carries its accession number, form, fiscal period, filed date, XBRL tag and a link to the filing, and the tool handles fiscal-year ends, quarterly vs YTD vs TTM, derived Q4, restatements and units. Use this whenever the user wants 10-K numbers or 10-Q numbers, says "pull financials for", asks for public company revenue, net income, EPS, cash, debt or capex, wants comps or a competitor side-by-side, a credit check, prospect research, or model inputs, or mentions SEC filings or EDGAR, even if they never say XBRL. Free and primary-source, no paid data terminal needed. Do not use it for private companies, stock prices or valuation multiples.
---

# SEC Filing Puller

Analysts lose a day prompting for 10-K numbers and still distrust the result. Models get these numbers wrong in predictable ways: they mix fiscal years, blend restated and originally reported figures, confuse quarterly with YTD or TTM, and slip on units. Do not recall financials from memory and do not scrape them from websites. Run the scripts. They read SEC's structured data and attach a filing citation to every number. Spend your own effort on judgment: whether the periods line up, whether the definitions match, and what the XBRL cannot tell you.

## Setup (once)

SEC requires a declared User-Agent with contact info. Without one, requests get HTTP 403. Ask the user for their name/company and email if you don't have them, then run:

```bash
export SEC_USER_AGENT="Acme Research jane@acme.com"   # the user's own contact, never a made-up one
pip install pandas                                     # the only dependency; everything else is stdlib
```

The scripts stay under SEC's 10 requests/second limit and cache responses in `~/.cache/sec-filing-puller` (override with `SEC_CACHE_DIR`, bypass with `--refresh`). Endpoint details are in `references/edgar-api.md`.

## Workflow

### 1. Resolve the company

```bash
python3 scripts/sec_pull.py resolve "BRK.B"      # ticker, CIK or a name fragment
```

The command resolves the company to a CIK through SEC's `company_tickers.json`. If the name is ambiguous it lists the candidates, so ask the user which one they mean. Delisted companies are not in the ticker file, so use the CIK instead.

### 2. Pull

```bash
python3 scripts/sec_pull.py pull AAPL                          # last 3 FYs + latest quarter + TTM, all metrics
python3 scripts/sec_pull.py pull MSFT --metrics revenue,net_income --years 5 --quarters 4
python3 scripts/sec_pull.py pull WMT --all-periods --format all --out ./sec   # full history for a model
python3 scripts/compare.py AAPL MSFT WMT --out ./comps                        # side-by-side comps
```

Metrics: revenue, gross_profit, operating_income, net_income, eps_diluted, diluted_shares, operating_cash_flow, capex, total_assets, cash, lt_debt_noncurrent, lt_debt_current, short_term_borrowings, shares_outstanding.

Output is a markdown table on stdout. With `--out`, the tool also writes a tidy CSV/JSON with one row per metric and period. Each row has these columns: `value` (raw units), `unit`, `basis` (reported / derived / not in XBRL), `formula`, `tag`, `form`, `accn`, `filed`, `filing_index_url`, `document_url`, `original_value`, `original_accn`, `revised` and `notes`.

### 3. Check before presenting

Read the `> WARNING` lines and the notes column. They carry the parts that matter:

- **Fiscal alignment.** AAPL's year ends in late September, MSFT's on June 30 and WMT's on January 31. "FY2025" covers a different 12 months for each, and compare.py prints the exact dates. For comps, lead with TTM, or say plainly that the fiscal years are offset.
- **Derived values.** Q4 is almost never tagged, so it is computed as FY minus the 9M YTD figure. 10-Q cash flows are YTD-only, so Q2 and Q3 cash flow is derived. Present derived numbers as derived and show the formula. EPS and share counts are never derived because they are not additive.
- **Restatements.** By default the tool uses the latest-filed value. `revised=True` means a later filing changed the number, and the originally reported value and accession are kept next to it. Use `--as-reported` when the user wants what the company said at the time, for example to check an old model or a guidance comparison.
- **Tag and definition differences.** Walmart's revenue is `Revenues` (total, including membership income) while Apple and Microsoft use `RevenueFromContract...` (net sales). The note gives the alternative value. When a comp mixes definitions, say so. The pitfalls for each metric are in `references/xbrl-concepts.md`.
- **Coverage.** If the tool warns that a newer 10-K/10-Q/20-F exists without XBRL facts, the table is stale for that company. Read the newer filing and cite it. Do not present the older period as the latest.
- **Currency.** Foreign filers report in their own currency (TSMC in TWD). Never label those numbers USD, and convert before comparing, stating the rate and its source.

### 4. Present with citations

Keep the source on every number in the answer, not only in a footnote. Show the form, fiscal period, filed date and a linked accession, for example: Revenue FY2025 $416,161M (10-K, filed 2025-10-31, [0000320193-25-000079](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/0000320193-25-000079-index.htm), us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax). Give the period dates next to fiscal labels. Round consistently (millions by default) and state the unit once.

When the stakes are high (a credit memo, a board slide, a number someone will quote), spot-check one or two values against the filing text. Open `document_url` and find the line in the income statement. The scripts were validated this way: Apple's FY2025 $416,161M net sales and $112,010M net income, and Walmart's FY2026 $713,163M total revenues and $21,893M net income, all match the 10-K text.

### 5. When a number isn't in XBRL, say so

Companyfacts contains only non-dimensional facts from standard taxonomies. These are not in the data:

- Segment and geographic revenue, product lines, and backlog. Point to the segment note ("Segment Information" or "Revenue by geography") in the 10-K and quote it from the document.
- Non-GAAP figures (adjusted EBITDA, adjusted EPS, free cash flow as the company defines it). These appear only in earnings releases, which are 8-K Exhibit 99.1. Label them non-GAAP and cite the exhibit.
- KPIs such as subscribers, same-store sales and units shipped. They live in MD&A text.
- Company-extension tags (`aapl:...`). Use `sec_pull.py concept` only for standard tags. For extensions, read the filing.
- Quarterly data for foreign private issuers (20-F/40-F filers report interims on 6-K).

Write "not in XBRL; see 10-K Note X / MD&A / 8-K Ex. 99.1" rather than estimating. A guessed number next to cited ones spoils the whole table.

## Drill-down tools

```bash
python3 scripts/sec_pull.py tags WMT --grep revenue           # which standard tags a company files, date ranges
python3 scripts/sec_pull.py concept AAPL us-gaap:NetIncomeLoss # every filed value of one tag, with index links
python3 scripts/sec_pull.py frame us-gaap:Revenues CY2025      # one value per company for a calendar period (screens)
```

Use `tags` when a metric comes back "not in XBRL". The company may use a tag outside the curated list, and you can report that tag by name. Use `concept` to trace a surprising number back to every filing that reported it. Frames align facts to calendar periods, not fiscal ones, so print start/end with every frame value.

## Tests

```bash
python3 -m unittest discover -s tests -v    # offline, uses saved fixtures, no User-Agent needed
```

The fixtures cover Q4 derivation (FY minus 9M, plus the three-quarter fallback), YTD-only cash flow, restatement through a 10-K/A, `--as-reported`, the max-tag revenue rule, and a real Apple subset (FY2025 Q4 = $102,466M).

## Scope

This is data retrieval, not investment advice. Present figures as reported by the company to the SEC, with their limitations stated, and leave conclusions about buying, selling or lending to the user.
