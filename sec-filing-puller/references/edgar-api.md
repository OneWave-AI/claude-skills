# SEC EDGAR APIs: endpoints, headers, limits

Checked 2026-09-22 against SEC's own pages:
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data (the old `/os/accessing-edgar-data` URL redirects here)

## Access rules

| Rule | What SEC says | What the scripts do |
|---|---|---|
| Authentication | None. "These APIs do not require any authentication or API keys." | Nothing to configure except the User-Agent |
| User-Agent | "Please declare your user agent in request headers", sample `User-Agent: Sample Company Name AdminContact@<sample company domain>.com`, plus `Accept-Encoding: gzip, deflate` | Reads `SEC_USER_AGENT` and refuses to run without an `@` in it; sends gzip/deflate and decompresses |
| Rate | "Current max request rate: 10 requests/second." SEC may limit requests further to keep access fair | 8 req/s minimum spacing, exponential backoff on 429/5xx |
| Blocking | Requests SEC flags as an undeclared bot or over the limit are "managed", in practice HTTP 403 | Reports 403 with the likely cause. Wait about 10 minutes before retrying |
| CORS | data.sec.gov does not support CORS | Call from a server or script, never from browser JavaScript |
| Freshness | Submissions update in under a second and XBRL APIs in under a minute (longer at peak filing times). Bulk ZIPs are rebuilt nightly around 3:00 a.m. ET | 12 h cache for companyfacts/submissions, 7 days for the ticker map. Use `--refresh` on filing day |

Use a real contact string such as `"Acme Research jane@acme.com"`. A missing or generic value (python-urllib, curl) gets 403s.

## Endpoints

CIKs are 10 digits, zero-padded, in data.sec.gov paths (`CIK0000320193`). Archive paths use the CIK without padding.

| Purpose | URL | Notes |
|---|---|---|
| Ticker to CIK | `https://www.sec.gov/files/company_tickers.json` | `{"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}, ...}`. SEC says it does not guarantee its accuracy or scope. Share classes use a dash: `BRK-B`. Delisted companies drop out, so look them up by CIK |
| Ticker + exchange | `https://www.sec.gov/files/company_tickers_exchange.json` | Same data plus the exchange |
| Filing history | `https://data.sec.gov/submissions/CIK##########.json` | Name, tickers, `fiscalYearEnd` (MMDD), SIC. `filings.recent` holds columnar arrays (`accessionNumber`, `form`, `filingDate`, `reportDate`, `primaryDocument`, ...) covering at least one year or 1,000 filings. Older pages are listed in `filings.files` |
| All XBRL facts for a company | `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` | `facts.{us-gaap,ifrs-full,dei,srt}.{Tag}.units.{unit}[]`. This is the main input |
| One tag for a company | `https://data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/AccountsPayableCurrent.json` | Same fact rows for one tag, with separate arrays per unit |
| One tag, every company, one period | `https://data.sec.gov/api/xbrl/frames/us-gaap/AccountsPayableCurrent/USD/CY2019Q1I.json` | See Frames below |
| Filing index page | `https://www.sec.gov/Archives/edgar/data/{cik}/{accn-no-dashes}/{accn}-index.htm` | Use this as the citation link. Verified to return 200 for `0000320193-25-000079` |
| Primary document | `https://www.sec.gov/Archives/edgar/data/{cik}/{accn-no-dashes}/{primaryDocument}` | `primaryDocument` comes from submissions. This is the 10-K/10-Q HTML to spot-check against |
| Bulk | `https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip`, `.../bulkdata/submissions.zip` | Use these for thousands of companies instead of calling the API once per company |

## Fact row fields (companyfacts / companyconcept)

```json
{"start": "2024-09-29", "end": "2025-09-27", "val": 416161000000,
 "accn": "0000320193-25-000079", "fy": 2025, "fp": "FY", "form": "10-K",
 "filed": "2025-10-31", "frame": "CY2025"}
```

- `val` is in raw units (dollars, shares, dollars per share). A filing that says "in millions" still stores full dollars in XBRL, so never multiply again.
- `start` appears only on duration facts (income and cash-flow statements). Instant facts (balance sheet, share counts) have only `end`.
- `fy`/`fp` belong to the filing, not to the fact. They are the filing's DocumentFiscalYearFocus and DocumentFiscalPeriodFocus. The FY2025 10-K's FY2023 comparative column is also tagged `fy=2025, fp=FY`. Identify a fact's period by `start`/`end` and label it from the filing whose own report period ends on that date. `sec_pull.fiscal_calendar` does this.
- `form` is the form of the filing that carried the fact: 10-K, 10-Q, 10-K/A, 20-F, 40-F, 8-K, and some registration statements. The scripts keep only periodic reports (10-K, 10-Q, 10-KT, 20-F, 40-F and their /A amendments).
- The same period shows up in several filings: the original, later comparatives, and amendments. Where they disagree, the period was restated or recast.
- `frame` is set on at most one fact per company per calendar frame: the last-filed fact that best fits it. It is missing on YTD facts and on most comparatives. Do not use it to find fiscal periods.
- Only non-dimensional facts from standard taxonomies are included. Segment and geographic breakdowns (facts that carry axes/members) and company-extension tags (`aapl:...`) are missing. Get those from the filing document.

## Frames

`/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json`

- `CY2025`: annual data (duration 365 days +/- 30)
- `CY2025Q2`: one quarter (duration 91 days +/- 30)
- `CY2025Q2I`: an instant (balance sheet at about the calendar quarter end)
- Units with a denominator use `-per-`, for example `USD-per-shares`. The XBRL default unit is `pure`.
- SEC's docs: a frame "aggregates one fact for each reporting entity that is last filed that most closely fits the calendrical period requested". A company with a January fiscal year end lands in CY2025 with its Feb 2025 to Jan 2026 year. Walmart's FY2026 appears in `us-gaap:Revenues/USD/CY2025`. Always print `start`/`end` next to frame values.
- Frames are good for screens ("every filer's revenue for CY2025") and bad for exact comps. Each company files under one tag, so a frame on `Revenues` misses companies that file `RevenueFromContractWithCustomerExcludingAssessedTax`.

## Examples

```bash
export SEC_USER_AGENT="Acme Research jane@acme.com"
curl -s --compressed -H "User-Agent: $SEC_USER_AGENT" https://www.sec.gov/files/company_tickers.json | head -c 300
curl -s --compressed -H "User-Agent: $SEC_USER_AGENT" https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/NetIncomeLoss.json | head -c 600
python3 scripts/sec_pull.py concept AAPL us-gaap:NetIncomeLoss     # same data as a table, with index links
python3 scripts/sec_pull.py frame us-gaap:Revenues CY2025 --top 10
```

## Errors seen in practice

| Symptom | Cause | Fix |
|---|---|---|
| 403 on every call | Missing or generic User-Agent, or over the rate limit | Set `SEC_USER_AGENT` to a name and email. Slow down. Wait 10 minutes |
| 404 on companyconcept | The company never filed that tag | `sec_pull.py tags TICKER --grep word` lists the tags it does file |
| 404 on companyfacts | Entity has no XBRL financial data (funds, some trusts, pre-2009 filers) | Read the filings, or use the full-text search at efts.sec.gov |
| Latest 10-K/20-F missing from facts | Filing too new, or tagged with a taxonomy version companyfacts has not ingested. Seen with TSMC's 20-F filed 2026-04-16: only dei/srt facts, no ifrs-full | `sec_pull.py` warns when submissions lists a newer periodic filing than the XBRL data. Take the numbers from that document |
