#!/usr/bin/env python3
"""Pull cited financial statement numbers for a US public company from SEC EDGAR.

Uses only SEC's free, official JSON APIs on data.sec.gov (companyfacts,
companyconcept, frames, submissions) plus the ticker->CIK map at
https://www.sec.gov/files/company_tickers.json. Every output number carries the
accession number, form, fiscal period, filed date, XBRL tag and a link to the
filing index, so a human can open the filing and check it.

SEC requires a declared User-Agent with contact info. Set it first:

    export SEC_USER_AGENT="Your Company your.name@example.com"

Commands:
    sec_pull.py pull AAPL                     # last 3 FYs + latest quarter + TTM, curated metrics
    sec_pull.py pull MSFT --years 5 --quarters 4 --out ./out --format all
    sec_pull.py concept AAPL us-gaap:NetIncomeLoss   # every reported value of one tag
    sec_pull.py tags WMT --grep revenue       # which standard tags this company files
    sec_pull.py frame us-gaap:Revenues CY2025 # one value per company for a calendar period
    sec_pull.py resolve "BRK.B"               # ticker/CIK/name -> CIK

Requires Python 3.9+ and pandas. Not investment advice.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zlib
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Curated metric map. Order of `tags` = fallback priority. Strategy "max" picks,
# per period, the largest value among the candidate tags (total revenue is the
# largest of the revenue-like tags a company files); "priority" takes the first
# tag that has a value for the period. See references/xbrl-concepts.md.
# ---------------------------------------------------------------------------
METRICS: dict[str, dict] = {
    "revenue": {
        "label": "Revenue", "kind": "duration", "unit": "money", "additive": True, "strategy": "max",
        "tags": [
            "us-gaap:Revenues",
            "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax",
            "us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax",
            "us-gaap:SalesRevenueNet",
            "us-gaap:SalesRevenueGoodsNet",
            "us-gaap:SalesRevenueServicesNet",
            "us-gaap:RevenuesNetOfInterestExpense",
            "us-gaap:RegulatedAndUnregulatedOperatingRevenue",
            "ifrs-full:Revenue",
        ],
    },
    "gross_profit": {
        "label": "Gross profit", "kind": "duration", "unit": "money", "additive": True, "strategy": "priority",
        "tags": ["us-gaap:GrossProfit", "ifrs-full:GrossProfit"],
    },
    "operating_income": {
        "label": "Operating income", "kind": "duration", "unit": "money", "additive": True, "strategy": "priority",
        "tags": ["us-gaap:OperatingIncomeLoss", "ifrs-full:ProfitLossFromOperatingActivities"],
    },
    "net_income": {
        "label": "Net income (to parent)", "kind": "duration", "unit": "money", "additive": True, "strategy": "priority",
        "tags": [
            "us-gaap:NetIncomeLoss",
            "us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic",
            "us-gaap:ProfitLoss",
            "ifrs-full:ProfitLossAttributableToOwnersOfParent",
            "ifrs-full:ProfitLoss",
        ],
    },
    "eps_diluted": {
        "label": "EPS, diluted", "kind": "duration", "unit": "per_share", "additive": False, "strategy": "priority",
        "tags": [
            "us-gaap:EarningsPerShareDiluted",
            "us-gaap:EarningsPerShareBasicAndDiluted",
            "us-gaap:IncomeLossFromContinuingOperationsPerDilutedShare",
            "ifrs-full:DilutedEarningsLossPerShare",
        ],
    },
    "diluted_shares": {
        "label": "Weighted avg diluted shares", "kind": "duration", "unit": "shares", "additive": False,
        "strategy": "priority",
        "tags": ["us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding",
                 "ifrs-full:AdjustedWeightedAverageShares"],
    },
    "operating_cash_flow": {
        "label": "Operating cash flow", "kind": "duration", "unit": "money", "additive": True, "strategy": "priority",
        "tags": [
            "us-gaap:NetCashProvidedByUsedInOperatingActivities",
            "us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
            "ifrs-full:CashFlowsFromUsedInOperatingActivities",
        ],
    },
    "capex": {
        "label": "Capital expenditures", "kind": "duration", "unit": "money", "additive": True, "strategy": "priority",
        "tags": [
            "us-gaap:PaymentsToAcquirePropertyPlantAndEquipment",
            "us-gaap:PaymentsToAcquireProductiveAssets",
            "us-gaap:PaymentsForCapitalImprovements",
            "ifrs-full:PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities",
        ],
    },
    "total_assets": {
        "label": "Total assets", "kind": "instant", "unit": "money", "strategy": "priority",
        "tags": ["us-gaap:Assets", "ifrs-full:Assets"],
    },
    "cash": {
        "label": "Cash and equivalents", "kind": "instant", "unit": "money", "strategy": "priority",
        "tags": [
            "us-gaap:CashAndCashEquivalentsAtCarryingValue",
            "us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
            "us-gaap:Cash",
            "ifrs-full:CashAndCashEquivalents",
        ],
    },
    "lt_debt_noncurrent": {
        "label": "Long-term debt, noncurrent", "kind": "instant", "unit": "money", "strategy": "priority",
        "tags": [
            "us-gaap:LongTermDebtNoncurrent",
            "us-gaap:LongTermDebtAndCapitalLeaseObligations",
            "ifrs-full:NoncurrentPortionOfNoncurrentBorrowings",
        ],
    },
    "lt_debt_current": {
        "label": "Long-term debt, current portion", "kind": "instant", "unit": "money", "strategy": "priority",
        "tags": [
            "us-gaap:LongTermDebtCurrent",
            "us-gaap:LongTermDebtAndCapitalLeaseObligationsCurrent",
            "ifrs-full:CurrentPortionOfNoncurrentBorrowings",
        ],
    },
    "short_term_borrowings": {
        "label": "Short-term borrowings / CP", "kind": "instant", "unit": "money", "strategy": "priority",
        "tags": ["us-gaap:CommercialPaper", "us-gaap:ShortTermBorrowings", "us-gaap:OtherShortTermBorrowings",
                 "ifrs-full:ShorttermBorrowings"],
    },
    "shares_outstanding": {
        "label": "Common shares outstanding", "kind": "instant", "unit": "shares", "strategy": "priority",
        "tags": ["us-gaap:CommonStockSharesOutstanding", "dei:EntityCommonStockSharesOutstanding"],
    },
}
DEFAULT_METRICS = list(METRICS)

TAG_NOTES = {
    "us-gaap:ProfitLoss": "ProfitLoss includes noncontrolling interests; not the same as net income to parent.",
    "us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic": "Net income available to common (after preferred dividends).",
    "us-gaap:IncomeLossFromContinuingOperationsPerDilutedShare": "Continuing operations only; excludes discontinued ops.",
    "us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents": "Includes restricted cash (cash-flow statement total), not balance-sheet cash.",
    "us-gaap:LongTermDebtAndCapitalLeaseObligations": "Includes finance lease obligations.",
    "us-gaap:LongTermDebtAndCapitalLeaseObligationsCurrent": "Includes finance lease obligations.",
    "us-gaap:PaymentsToAcquireProductiveAssets": "Productive assets can include intangibles, not only PP&E.",
    "us-gaap:RevenuesNetOfInterestExpense": "Bank-style revenue net of interest expense.",
}

PERIODIC_FORMS = {"10-K", "10-K/A", "10-Q", "10-Q/A", "10-KT", "10-KT/A", "20-F", "20-F/A", "40-F", "40-F/A"}
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
DATA = "https://data.sec.gov"

# ---------------------------------------------------------------------------
# HTTP: declared User-Agent, <=10 req/s, retries, on-disk cache
# ---------------------------------------------------------------------------
_MIN_INTERVAL = 0.125  # 8 req/s, under SEC's 10 req/s fair-access ceiling
_last_request = [0.0]


class SecError(RuntimeError):
    pass


def user_agent() -> str:
    ua = os.environ.get("SEC_USER_AGENT", "").strip()
    if not ua or "@" not in ua:
        raise SecError(
            "SEC_USER_AGENT is not set (or has no email). SEC requires a declared User-Agent with contact info, "
            'e.g.  export SEC_USER_AGENT="Acme Research jane@acme.com"  -- requests without it get HTTP 403.'
        )
    return ua


def cache_dir() -> Path:
    d = Path(os.environ.get("SEC_CACHE_DIR", Path.home() / ".cache" / "sec-filing-puller"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def fetch_json(url: str, ttl_hours: float = 12.0, refresh: bool = False):
    key = hashlib.sha1(url.encode()).hexdigest()[:16] + "_" + re.sub(r"[^A-Za-z0-9]+", "_", url[-60:]) + ".json"
    path = cache_dir() / key
    if not refresh and path.exists() and (time.time() - path.stat().st_mtime) < ttl_hours * 3600:
        return json.loads(path.read_text())
    headers = {"User-Agent": user_agent(), "Accept-Encoding": "gzip, deflate"}
    delay = 1.0
    for attempt in range(5):
        wait = _MIN_INTERVAL - (time.time() - _last_request[0])
        if wait > 0:
            time.sleep(wait)
        _last_request[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
                raw = r.read()
                enc = r.headers.get("Content-Encoding", "")
            if enc == "gzip":
                raw = gzip.decompress(raw)
            elif enc == "deflate":
                raw = zlib.decompress(raw)
            data = json.loads(raw)
            path.write_text(json.dumps(data))
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise SecError(f"404 Not Found: {url} (no data for this CIK/tag/period)") from None
            if e.code == 403:
                raise SecError(
                    f"403 Forbidden from SEC for {url}. Usually an undeclared/generic User-Agent or the "
                    "10 req/s limit was exceeded; SEC may block the IP for ~10 minutes."
                ) from None
            if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(delay)
                delay *= 2
                continue
            raise SecError(f"HTTP {e.code} for {url}") from None
        except urllib.error.URLError as e:
            if attempt < 4:
                time.sleep(delay)
                delay *= 2
                continue
            raise SecError(f"Network error for {url}: {e.reason}") from None
    raise SecError(f"Gave up on {url}")


# ---------------------------------------------------------------------------
# Company resolution
# ---------------------------------------------------------------------------
def resolve(query: str) -> dict:
    """Ticker, CIK (digits) or company-name fragment -> {cik, ticker, title}."""
    q = query.strip()
    tickers = list(fetch_json(TICKERS_URL, ttl_hours=24 * 7).values())
    if q.isdigit():
        cik = int(q)
        hit = next((t for t in tickers if t["cik_str"] == cik), None)
        return {"cik": cik, "ticker": hit["ticker"] if hit else "", "title": hit["title"] if hit else ""}
    norm = q.upper().replace(".", "-").replace("/", "-")
    for t in tickers:
        if t["ticker"].upper() == norm:
            return {"cik": t["cik_str"], "ticker": t["ticker"], "title": t["title"]}
    matches = [t for t in tickers if q.lower() in t["title"].lower()]
    if len(matches) == 1:
        m = matches[0]
        return {"cik": m["cik_str"], "ticker": m["ticker"], "title": m["title"]}
    if matches:
        opts = ", ".join(f"{m['ticker']} ({m['title']}, CIK {m['cik_str']})" for m in matches[:10])
        raise SecError(f"'{query}' is ambiguous. Candidates: {opts}")
    raise SecError(f"No ticker/company matching '{query}' in company_tickers.json. Try the CIK "
                   "(https://www.sec.gov/search-filings/cik-lookup). Delisted/private companies are not listed.")


def cik10(cik) -> str:
    return f"{int(cik):010d}"


def get_companyfacts(cik, refresh=False) -> dict:
    return fetch_json(f"{DATA}/api/xbrl/companyfacts/CIK{cik10(cik)}.json", refresh=refresh)


def get_submissions(cik, refresh=False) -> dict:
    return fetch_json(f"{DATA}/submissions/CIK{cik10(cik)}.json", refresh=refresh)


def get_concept(cik, tag: str) -> dict:
    tax, name = tag.split(":", 1) if ":" in tag else ("us-gaap", tag)
    return fetch_json(f"{DATA}/api/xbrl/companyconcept/CIK{cik10(cik)}/{tax}/{name}.json")


def get_frame(tag: str, unit: str, period: str) -> dict:
    tax, name = tag.split(":", 1) if ":" in tag else ("us-gaap", tag)
    return fetch_json(f"{DATA}/api/xbrl/frames/{tax}/{name}/{unit}/{period}.json")


def filing_index_url(cik, accn: str) -> str:
    return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accn.replace('-', '')}/{accn}-index.htm"


def submissions_docs(sub: dict | None) -> dict:
    """accession -> {reportDate, primaryDocument, form, filingDate} from the 'recent' block."""
    out = {}
    if not sub:
        return out
    blocks = [sub.get("filings", {}).get("recent", {})] + sub.get("_older", [])
    for r in blocks:
        for i, a in enumerate(r.get("accessionNumber", [])):
            out[a] = {"reportDate": r["reportDate"][i], "primaryDocument": r["primaryDocument"][i],
                      "form": r["form"][i], "filingDate": r["filingDate"][i]}
    return out


def load_older_submissions(sub: dict) -> None:
    """Fetch the paged older-filings files listed in submissions['filings']['files'] (one request each)."""
    sub["_older"] = [fetch_json(f"{DATA}/submissions/{f['name']}") for f in sub.get("filings", {}).get("files", [])]


# ---------------------------------------------------------------------------
# Period logic (pure functions; unit-tested offline)
# ---------------------------------------------------------------------------
def d(s: str) -> date:
    return date.fromisoformat(s)


def days(start: str | None, end: str) -> int | None:
    return None if not start else (d(end) - d(start)).days + 1


def duration_class(start: str | None, end: str) -> str:
    n = days(start, end)
    if n is None:
        return "I"
    if 80 <= n <= 100:
        return "3M"
    if 170 <= n <= 200:
        return "6M"
    if 260 <= n <= 290:
        return "9M"
    if 350 <= n <= 380:
        return "FY"
    return f"{n}d"


def near(a: str, b: str, tol: int = 4) -> bool:
    return abs((d(a) - d(b)).days) <= tol


def fiscal_calendar(facts: dict, sub_docs: dict | None = None) -> list[dict]:
    """One row per periodic filing's own report period: {end, fy, fp, form, accn, filed}.

    fy/fp on a companyfacts fact describe the FILING (DocumentFiscalYearFocus/PeriodFocus),
    not the fact: a FY2025 10-K also carries FY2023 and FY2024 comparatives tagged fy=2025.
    So we label a fact's period by matching its END date to the report date of the filing
    that covered that period as its current period.
    """
    sub_docs = sub_docs or {}
    acc: dict[str, dict] = {}
    for tax in ("us-gaap", "ifrs-full"):
        for tag in facts.get("facts", {}).get(tax, {}).values():
            for unit_facts in tag.get("units", {}).values():
                for f in unit_facts:
                    if f.get("form") not in PERIODIC_FORMS or f.get("fy") is None:
                        continue
                    a = acc.setdefault(f["accn"], {"accn": f["accn"], "fy": f["fy"], "fp": f.get("fp"),
                                                   "form": f["form"], "filed": f["filed"], "max_end": f["end"]})
                    if f["end"] > a["max_end"]:
                        a["max_end"] = f["end"]
    cal: dict[str, dict] = {}
    for a in sorted(acc.values(), key=lambda x: x["filed"]):
        end = sub_docs.get(a["accn"], {}).get("reportDate") or a["max_end"]
        if not end:
            continue
        existing = next((k for k in cal if near(k, end)), None)
        if existing is None:  # keep the ORIGINAL filing for a period (earliest filed); amendments add nothing new
            cal[end] = {"end": end, "fy": a["fy"], "fp": a["fp"], "form": a["form"], "accn": a["accn"],
                        "filed": a["filed"]}
    return sorted(cal.values(), key=lambda x: x["end"])


def period_label(start: str | None, end: str, cal: list[dict]) -> tuple[str, int | None, str | None]:
    """-> (label, fiscal_year, fiscal_period) for a fact's period, using the fiscal calendar."""
    cls = duration_class(start, end)
    p = next((c for c in cal if near(c["end"], end)), None)
    if p is None:
        if cls == "I":  # e.g. cover-page share counts dated after period end: attach to the prior report period
            prior = [c for c in cal if c["end"] <= end and (d(end) - d(c["end"])).days <= 120]
            if prior:
                p = prior[-1]
                return f"FY{p['fy']} {p['fp']} (as of {end})".replace(" FY (", " ("), p["fy"], p["fp"]
        return f"{start or ''}..{end} ({cls})", None, None
    fy, fp = p["fy"], p["fp"]
    if cls == "I":
        return (f"FY{fy}" if fp == "FY" else f"FY{fy} {fp}") + " end", fy, fp
    if cls == "FY" and fp == "FY":
        return f"FY{fy}", fy, "FY"
    if cls == "3M":
        q = "Q4" if fp == "FY" else fp
        return f"FY{fy} {q}", fy, q
    if cls == "6M" and fp == "Q2":
        return f"FY{fy} H1 YTD", fy, "H1"
    if cls == "9M" and fp == "Q3":
        return f"FY{fy} 9M YTD", fy, "9M"
    return f"FY{fy} {fp} ({cls})", fy, fp


def pick_unit(units: dict, kind: str) -> str | None:
    keys = list(units)
    if kind == "money":
        # The reporting currency is the one with the most facts. A foreign filer that also tags a
        # USD "convenience translation" (one year-end rate, latest years only) must NOT be read as USD.
        cur = [k for k in keys if re.fullmatch(r"[A-Z]{3}", k)]
        return max(cur, key=lambda k: (len(units[k]), k == "USD")) if cur else None
    if kind == "per_share":
        if "USD/shares" in keys:
            return "USD/shares"
        ps = [k for k in keys if k.endswith("/shares")]
        return max(ps, key=lambda k: len(units[k])) if ps else None
    if kind == "shares":
        return "shares" if "shares" in keys else None
    return keys[0] if keys else None


def tag_facts(facts: dict, tag: str, unit_kind: str) -> tuple[str | None, list[dict]]:
    tax, name = tag.split(":", 1)
    node = facts.get("facts", {}).get(tax, {}).get(name)
    if not node:
        return None, []
    unit = pick_unit(node.get("units", {}), unit_kind)
    if not unit:
        return None, []
    rows = [f for f in node["units"][unit] if f.get("form") in PERIODIC_FORMS]
    return unit, rows


def select_values(rows: list[dict]) -> dict:
    """Group one tag's facts by period; keep latest-filed and originally-reported values.

    Returns {(start, end): {...}}. 'latest' = most recently FILED fact for that exact period
    (captures restatements/recasts in later 10-Ks and 10-K/As); 'original' = earliest filed.
    """
    groups: dict[tuple, list[dict]] = {}
    for f in rows:
        groups.setdefault((f.get("start"), f["end"]), []).append(f)
    out = {}
    for key, fs in groups.items():
        fs = sorted(fs, key=lambda f: (f["filed"], f["accn"]))
        orig = fs[0]
        # Latest-filed VALUE wins; cite the earliest filing that reported that value, so an
        # unrevised FY2023 number cites the FY2023 10-K, not a later 10-K's comparative column.
        latest = next(f for f in fs if f["val"] == fs[-1]["val"])
        distinct = sorted({f["val"] for f in fs})
        out[key] = {
            "start": key[0], "end": key[1], "value": latest["val"], "accn": latest["accn"], "form": latest["form"],
            "filed": latest["filed"], "fy": latest.get("fy"), "fp": latest.get("fp"),
            "original_value": orig["val"], "original_accn": orig["accn"], "original_form": orig["form"],
            "original_filed": orig["filed"], "revised": len(distinct) > 1, "n_filings": len({f["accn"] for f in fs}),
            "amended": latest["form"].endswith("/A"),
        }
    return out


def metric_periods(facts: dict, metric: str, as_reported: bool = False) -> dict:
    """{(start,end): selection} for one curated metric, with tag fallback per period."""
    spec = METRICS[metric]
    per_tag = {}
    for tag in spec["tags"]:
        unit, rows = tag_facts(facts, tag, spec["unit"])
        if rows:
            per_tag[tag] = (unit, select_values(rows))
    result = {}
    keys = {k for _, sel in per_tag.values() for k in sel}
    for k in keys:
        cands = [(tag, unit, sel[k]) for tag, (unit, sel) in per_tag.items() if k in sel]
        if spec["strategy"] == "max":  # ties go to the tag the company uses for the most periods
            tag, unit, rec = max(cands, key=lambda c: (c[2]["value"], len(per_tag[c[0]][1])))
        else:
            tag, unit, rec = cands[0]  # dict preserves priority order
        rec = dict(rec, tag=tag, unit=unit)
        if as_reported:
            rec.update(value=rec["original_value"], accn=rec["original_accn"], form=rec["original_form"],
                       filed=rec["original_filed"])
        alts = [f"{t} = {r['value']:,}" for t, u, r in cands if t != tag and r["value"] != rec["value"]]
        rec["alt_tags"] = alts
        result[k] = rec
    return result


def find(periods: dict, end: str, cls: str, start: str | None = None):
    for (s, e), rec in periods.items():
        if near(e, end) and duration_class(s, e) == cls and (start is None or (s and near(s, start))):
            return rec
    return None


def _derived(value, label_formula, parts, unit, tag):
    latest = max(parts, key=lambda p: p["filed"])
    return {"value": value, "derived": True, "formula": label_formula, "components": parts, "unit": unit,
            "tag": tag, "accn": "; ".join(dict.fromkeys(p["accn"] for p in parts)), "form": latest["form"],
            "filed": latest["filed"], "revised": any(p.get("revised") for p in parts), "alt_tags": []}


def build_quarters(periods: dict, cal: list[dict], additive: bool) -> list[dict]:
    """Reported or derived 3-month values for every fiscal quarter the calendar knows about.

    Derivations (additive flows only): Q2 = H1 YTD - Q1, Q3 = 9M YTD - H1 YTD, Q4 = FY - 9M YTD
    (fallback Q4 = FY - Q1 - Q2 - Q3). Cash-flow statements are YTD-only in 10-Qs, so Q2/Q3
    cash flows are almost always derived. Per-share and weighted-share values are never derived.
    """
    out = []
    years = sorted({c["fy"] for c in cal})
    for fy in years:
        ends = {c["fp"]: c["end"] for c in cal if c["fy"] == fy}
        fy_rec = find(periods, ends["FY"], "FY") if "FY" in ends else None
        fy_start = fy_rec["start"] if fy_rec else None
        q1 = find(periods, ends["Q1"], "3M") if "Q1" in ends else None
        if fy_start is None and q1:
            fy_start = q1["start"]
        prev_end, qs, ytd = None, {}, {}
        for qi, fp in enumerate(["Q1", "Q2", "Q3", "FY"], start=1):
            if fp not in ends:
                prev_end = None
                continue
            end = ends[fp]
            qname = "Q4" if fp == "FY" else fp
            rec = find(periods, end, "3M")
            ycls = {"Q1": "3M", "Q2": "6M", "Q3": "9M", "FY": "FY"}[fp]
            ytd[fp] = find(periods, end, ycls, fy_start) if fy_start else find(periods, end, ycls)
            if rec is None and additive:
                prior_fp = {"Q2": "Q1", "Q3": "Q2", "FY": "Q3"}.get(fp)
                cur, prv = ytd.get(fp), ytd.get(prior_fp)
                if cur and prv:
                    names = {"Q2": ("H1 YTD", "Q1"), "Q3": ("9M YTD", "H1 YTD"), "FY": ("FY", "9M YTD")}[fp]
                    rec = _derived(cur["value"] - prv["value"], f"{names[0]} - {names[1]} = "
                                   f"{cur['value']:,} - {prv['value']:,}", [cur, prv], cur["unit"], cur["tag"])
                    rec.update(start=(d(prv["end"]) + timedelta(days=1)).isoformat(), end=cur["end"])
                elif fp == "FY" and ytd.get("FY") and all(qs.get(q) for q in ("Q1", "Q2", "Q3")):
                    f = ytd["FY"]
                    parts = [f] + [qs[q] for q in ("Q1", "Q2", "Q3")]
                    v = f["value"] - sum(qs[q]["value"] for q in ("Q1", "Q2", "Q3"))
                    rec = _derived(v, f"FY - Q1 - Q2 - Q3 = {f['value']:,} - "
                                   + " - ".join(f"{qs[q]['value']:,}" for q in ("Q1", "Q2", "Q3")),
                                   parts, f["unit"], f["tag"])
                    rec.update(start=(d(qs["Q3"]["end"]) + timedelta(days=1)).isoformat(), end=f["end"])
            if rec is not None:
                rec = dict(rec, fiscal_year=fy, fiscal_period=qname, label=f"FY{fy} {qname}")
                rec.setdefault("derived", False)
                qs[qname] = rec
                out.append(rec)
    return sorted(out, key=lambda r: r["end"])


def ttm(quarters: list[dict]) -> dict | None:
    """Sum of the latest four contiguous quarters (reported or derived)."""
    if len(quarters) < 4:
        return None
    last4 = quarters[-4:]
    for a, b in zip(last4, last4[1:]):
        if not a.get("start") or not b.get("start") or abs((d(b["start"]) - d(a["end"])).days) > 5:
            return None
    v = sum(q["value"] for q in last4)
    parts = []
    for q in last4:
        parts.extend(q["components"] if q.get("derived") else [q])
    rec = _derived(v, "sum of " + " + ".join(q["label"] for q in last4), parts, last4[-1]["unit"],
                   last4[-1]["tag"])
    rec.update(start=last4[0]["start"], end=last4[-1]["end"], label=f"TTM to {last4[-1]['end']}",
               fiscal_year=None, fiscal_period="TTM",
               derived_quarters=[q["label"] for q in last4 if q.get("derived")])
    return rec


# ---------------------------------------------------------------------------
# Table assembly
# ---------------------------------------------------------------------------
def fmt_value(v, unit: str) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return ""
    if unit.endswith("/shares"):
        cur = unit.split("/")[0]
        return f"{'$' if cur == 'USD' else cur + ' '}{v:,.2f}"
    if unit == "shares":
        return f"{v / 1e6:,.1f}M sh"
    prefix = "$" if unit == "USD" else unit + " "
    return f"{'-' if v < 0 else ''}{prefix}{abs(v) / 1e6:,.0f}M"


def build_table(facts: dict, sub: dict | None = None, metrics=None, years: int = 3, quarters: int = 1,
                include_ttm: bool = True, as_reported: bool = False, ticker: str = "",
                all_periods: bool = False) -> pd.DataFrame:
    metrics = metrics or DEFAULT_METRICS
    cik = facts.get("cik")
    company = facts.get("entityName", "")
    docs = submissions_docs(sub)
    cal = fiscal_calendar(facts, docs)
    if not cal:
        raise SecError(f"No 10-K/10-Q/20-F XBRL facts for {company or cik}. It may be a fund, a pre-2009 "
                       "filer, or file only non-periodic forms.")
    extra_warn = []
    if not any(c["fp"] in ("Q1", "Q2", "Q3") for c in cal):
        quarters, include_ttm = 0, False
        extra_warn.append("Annual-only filer (no 10-Q XBRL): foreign private issuers report interim results on 6-K, "
                          "which rarely carries tagged financial statements and is not used here. Take quarterly "
                          "and TTM figures from the 6-K itself and cite it.")
    fy_ends = [c for c in cal if c["fp"] == "FY"]
    q_ends = [c for c in cal if c["fp"] in ("Q1", "Q2", "Q3", "FY")]
    want_fy = fy_ends if all_periods else fy_ends[-years:]
    rows = []

    def cite(rec):
        accns = list(dict.fromkeys(a.strip() for a in str(rec.get("accn", "")).split(";") if a.strip()))
        return " ; ".join(filing_index_url(cik, a) for a in accns)

    def doc_url(accn):
        info = docs.get(accn)
        if info and info.get("primaryDocument"):
            return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accn.replace('-', '')}/{info['primaryDocument']}"
        return ""

    def emit(metric, rec, label, ptype, fy=None, fp=None, note=""):
        spec = METRICS[metric]
        notes = []
        if note:
            notes.append(note)
        if rec is None:
            rows.append({"ticker": ticker, "cik": cik, "company": company, "metric": metric,
                         "metric_label": spec["label"], "period": label, "period_type": ptype, "fiscal_year": fy,
                         "fiscal_period": fp, "value": None, "value_fmt": "", "basis": "not in XBRL",
                         "notes": " ".join(notes)})
            return
        tag = rec.get("tag", "")
        if tag in TAG_NOTES:
            notes.append(TAG_NOTES[tag])
        if rec.get("revised") and not rec.get("derived"):
            if as_reported:
                notes.append(f"Later filings revised this period; later-filed value {rec['value']:,} not used "
                             f"(--as-reported).")
            else:
                notes.append(f"Revised in a later filing: originally reported {rec['original_value']:,} "
                             f"in {rec['original_form']} {rec['original_accn']} filed {rec['original_filed']}.")
        elif rec.get("revised"):
            notes.append("A component was revised in a later filing; latest-filed values used.")
        if rec.get("amended"):
            notes.append("Value comes from an amended filing (/A).")
        if rec.get("alt_tags"):
            notes.append("Other tags for this period: " + "; ".join(rec["alt_tags"]) + ".")
        if rec.get("unit") and rec["unit"] not in ("USD", "USD/shares", "shares"):
            notes.append(f"Reported in {rec['unit']}, not USD (any USD figures in the filing are convenience "
                         "translations at a single rate).")
        if rec.get("derived_quarters"):
            notes.append("Includes derived quarters: " + ", ".join(rec["derived_quarters"]) + ".")
        first_accn = str(rec.get("accn", "")).split(";")[0].strip()
        rows.append({
            "ticker": ticker, "cik": cik, "company": company, "metric": metric, "metric_label": spec["label"],
            "period": label, "period_type": ptype, "fiscal_year": fy, "fiscal_period": fp,
            "start": rec.get("start"), "end": rec.get("end"), "days": days(rec.get("start"), rec["end"])
            if rec.get("start") else None,
            "value": rec["value"], "unit": rec.get("unit"), "value_fmt": fmt_value(rec["value"], rec.get("unit", "")),
            "basis": "derived" if rec.get("derived") else "reported", "formula": rec.get("formula", ""),
            "tag": tag, "form": rec.get("form"), "accn": rec.get("accn"), "filed": rec.get("filed"),
            "filing_index_url": cite(rec), "document_url": doc_url(first_accn) if not rec.get("derived") else "",
            "original_value": rec.get("original_value") if not rec.get("derived") else None,
            "original_accn": rec.get("original_accn") if not rec.get("derived") else None,
            "revised": bool(rec.get("revised")), "notes": " ".join(notes),
        })

    for metric in metrics:
        spec = METRICS[metric]
        periods = metric_periods(facts, metric, as_reported=as_reported)
        if spec["kind"] == "duration":
            for c in want_fy:
                rec = find(periods, c["end"], "FY")
                emit(metric, rec, f"FY{c['fy']}", "FY", c["fy"], "FY",
                     "" if rec else "No full-year value in XBRL for this metric/tag set.")
            qs = build_quarters(periods, cal, spec.get("additive", False))
            chosen_q = q_ends if all_periods else q_ends[-quarters:] if quarters else []
            for c in chosen_q:
                qname = "Q4" if c["fp"] == "FY" else c["fp"]
                rec = next((q for q in qs if near(q["end"], c["end"])), None)
                note = ""
                if rec is None:
                    note = ("Quarter not reported in XBRL and not derivable: per-share and weighted-share values "
                            "are not additive. Use the earnings release or the 10-K quarterly data note."
                            if not spec.get("additive") else
                            "Quarter not reported and YTD components missing; not derivable.")
                elif rec.get("derived"):
                    note = f"Derived: {rec['formula']}."
                emit(metric, rec, f"FY{c['fy']} {qname}", "Q", c["fy"], qname, note)
            if include_ttm and spec.get("additive"):
                t = ttm(qs)
                if t and (not q_ends or near(t["end"], q_ends[-1]["end"])):
                    emit(metric, t, "TTM", "TTM", None, "TTM", f"Computed: {t['formula']}.")
                else:
                    emit(metric, None, "TTM", "TTM", None, "TTM",
                         "TTM not computable: four contiguous quarters ending at the latest period are not available.")
        else:  # instant
            points = [(c, f"FY{c['fy']} end", "FY") for c in want_fy]
            latest = q_ends[-quarters:] if quarters else []
            if all_periods:
                latest = q_ends
            for c in latest:
                if not any(near(c["end"], p[0]["end"]) for p in points):
                    points.append((c, f"FY{c['fy']} {c['fp']} end", "Q"))
            for c, label, ptype in points:
                rec = next((r for (s, e), r in periods.items() if s is None and near(e, c["end"])), None)
                note = ""
                if rec is None and metric == "shares_outstanding":
                    # cover-page counts are dated weeks after period end
                    later = sorted((r for (s, e), r in periods.items() if s is None and e > c["end"]
                                    and (d(e) - d(c["end"])).days <= 120), key=lambda r: r["end"])
                    if later:
                        rec = later[0]
                        note = (f"Cover-page (dei) count as of {rec['end']}, not the balance-sheet date; "
                                "multi-class issuers may report only one class here.")
                emit(metric, rec, label, "instant", c["fy"], c["fp"],
                     note or ("" if rec else "No value at this balance-sheet date in XBRL."))

    df = pd.DataFrame(rows)
    df.attrs["warnings"] = coverage_warnings(cal, docs) + extra_warn
    # Flag tag switches across periods for the same metric (definition may have changed).
    if not df.empty and "tag" in df:
        for m, g in df[df["value"].notna()].groupby("metric"):
            tags = [t for t in g["tag"].dropna().unique() if t]
            if len(tags) > 1:
                df.loc[df["metric"] == m, "notes"] = df.loc[df["metric"] == m, "notes"].fillna("").astype(str) + \
                    f" Tag differs across periods ({', '.join(tags)}): confirm the definitions match."
    return df


def coverage_warnings(cal: list[dict], docs: dict) -> list[str]:
    """Periodic filings in the submissions feed that companyfacts has no financial facts for."""
    known = {c["accn"] for c in cal}
    if not docs or not cal:
        return []
    latest_end = cal[-1]["end"]
    w = []
    for accn, info in docs.items():
        if info["form"] in PERIODIC_FORMS and not info["form"].endswith("/A") and accn not in known \
                and (info.get("reportDate") or "") > latest_end:
            w.append(f"{info['form']} {accn} filed {info['filingDate']} (period {info['reportDate']}) is newer than "
                     f"the latest XBRL financial data ({latest_end}) and has no us-gaap/ifrs facts in companyfacts. "
                     "Read that filing directly for the latest numbers; do not present the older period as current.")
    return sorted(w)


def to_markdown(df: pd.DataFrame, title: str = "") -> str:
    lines = []
    if title:
        lines += [f"### {title}", ""]
    for w in df.attrs.get("warnings", []):
        lines += [f"> WARNING: {w}", ""]
    lines += ["| Metric | Period | Dates | Value | Basis | XBRL tag | Source | Notes |",
              "|---|---|---|---|---|---|---|---|"]
    for _, r in df.iterrows():
        start, end = r.get("start"), r.get("end")
        start = start if isinstance(start, str) else ""
        end = end if isinstance(end, str) else ""
        dates = f"{start}..{end}" if start else end
        if pd.isna(r.get("value")):
            src, val = "", "n/a"
        else:
            urls = str(r.get("filing_index_url", "")).split(" ; ")
            accns = str(r.get("accn", "")).split("; ")
            src = ", ".join(f"[{a}]({u})" for a, u in zip(accns, urls))
            src = f"{r.get('form')} filed {r.get('filed')}: {src}" if r.get("basis") == "reported" else f"derived from {src}"
            val = r.get("value_fmt")
        notes = str(r.get("notes") or "").replace("|", "/").strip()
        tag = r.get("tag") if isinstance(r.get("tag"), str) else ""
        lines.append(f"| {r['metric_label']} | {r['period']} | {dates} | {val} | {r.get('basis')} | {tag} | {src} | {notes} |")
    return "\n".join(lines)


def pull(query: str, refresh: bool = False, **kw) -> tuple[dict, pd.DataFrame]:
    co = resolve(query)
    facts = get_companyfacts(co["cik"], refresh=refresh)
    sub = get_submissions(co["cik"], refresh=refresh)
    df = build_table(facts, sub, ticker=co["ticker"] or query.upper(), **kw)
    co.update(name=sub.get("name") or facts.get("entityName"), fiscal_year_end=sub.get("fiscalYearEnd"),
              sic=sub.get("sicDescription"))
    return co, df


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("pull", help="curated, cited metrics for one company")
    p.add_argument("company")
    p.add_argument("--metrics", default=",".join(DEFAULT_METRICS), help=f"comma list from: {', '.join(METRICS)}")
    p.add_argument("--years", type=int, default=3)
    p.add_argument("--quarters", type=int, default=1, help="latest N fiscal quarters (0 = none)")
    p.add_argument("--no-ttm", action="store_true")
    p.add_argument("--all-periods", action="store_true", help="every FY and quarter on file (model inputs)")
    p.add_argument("--as-reported", action="store_true",
                   help="use originally reported values instead of latest-filed (restated) values")
    p.add_argument("--format", choices=["md", "csv", "json", "all"], default="md")
    p.add_argument("--out", help="directory for <TICKER>_sec.csv / .md / .json")
    p.add_argument("--refresh", action="store_true", help="ignore cache")
    c = sp.add_parser("concept", help="every reported value of one XBRL tag (companyconcept API)")
    c.add_argument("company")
    c.add_argument("tag", help="e.g. us-gaap:NetIncomeLoss")
    c.add_argument("--unit")
    t = sp.add_parser("tags", help="list standard-taxonomy tags this company files")
    t.add_argument("company")
    t.add_argument("--grep", default="")
    f = sp.add_parser("frame", help="one value per company for a calendar period (frames API)")
    f.add_argument("tag")
    f.add_argument("period", help="CY2025 (annual), CY2025Q2 (quarter), CY2025Q2I (instant)")
    f.add_argument("--unit", default="USD")
    f.add_argument("--top", type=int, default=25)
    r = sp.add_parser("resolve")
    r.add_argument("company")
    a = ap.parse_args(argv)

    try:
        user_agent()  # fail fast even when the cache could answer: every run must be attributable
        if a.cmd == "resolve":
            print(json.dumps(resolve(a.company), indent=2))
        elif a.cmd == "pull":
            metrics = [m.strip() for m in a.metrics.split(",") if m.strip()]
            bad = [m for m in metrics if m not in METRICS]
            if bad:
                raise SecError(f"Unknown metric(s) {bad}. Choose from {list(METRICS)}")
            co, df = pull(a.company, refresh=a.refresh, metrics=metrics, years=a.years, quarters=a.quarters,
                          include_ttm=not a.no_ttm, as_reported=a.as_reported, all_periods=a.all_periods)
            title = (f"{co['name']} ({co['ticker']}, CIK {co['cik']}) -- fiscal year ends "
                     f"{co.get('fiscal_year_end') or '?'} (MMDD). Source: SEC EDGAR XBRL companyfacts.")
            md = to_markdown(df, title)
            if a.out:
                out = Path(a.out)
                out.mkdir(parents=True, exist_ok=True)
                stem = out / f"{(co['ticker'] or a.company).upper()}_sec"
                if a.format in ("csv", "all"):
                    df.to_csv(f"{stem}.csv", index=False)
                if a.format in ("md", "all"):
                    Path(f"{stem}.md").write_text(md + "\n")
                if a.format in ("json", "all"):
                    df.to_json(f"{stem}.json", orient="records", indent=2)
                print(f"wrote {stem}.*", file=sys.stderr)
            if a.format == "csv" and not a.out:
                df.to_csv(sys.stdout, index=False)
            elif a.format == "json" and not a.out:
                print(df.to_json(orient="records", indent=2))
            else:
                print(md)
        elif a.cmd == "concept":
            co = resolve(a.company)
            data = get_concept(co["cik"], a.tag)
            unit = a.unit or next(iter(data["units"]))
            df = pd.DataFrame(data["units"][unit])
            df["period"] = [duration_class(s, e) for s, e in zip(df.get("start", [None] * len(df)), df["end"])]
            df["filing_index_url"] = [filing_index_url(co["cik"], x) for x in df["accn"]]
            print(f"# {data.get('entityName')} {a.tag} [{unit}] -- {data.get('label')}: {data.get('description')}\n")
            print(df.sort_values(["end", "filed"]).to_string(index=False))
        elif a.cmd == "tags":
            co = resolve(a.company)
            facts = get_companyfacts(co["cik"])
            out = []
            for tax, tags in facts["facts"].items():
                for name, node in tags.items():
                    label = node.get("label") or ""
                    if a.grep.lower() not in (name + " " + label).lower():
                        continue
                    for unit, fs in node["units"].items():
                        out.append({"tag": f"{tax}:{name}", "unit": unit, "n": len(fs),
                                    "first_end": min(x["end"] for x in fs), "last_end": max(x["end"] for x in fs),
                                    "label": label[:70]})
            print(pd.DataFrame(out).sort_values("last_end", ascending=False).to_string(index=False)
                  if out else "no matching tags")
        elif a.cmd == "frame":
            data = get_frame(a.tag, a.unit, a.period)
            df = pd.DataFrame(data["data"]).sort_values("val", ascending=False).head(a.top)
            print(f"# {a.tag} {a.unit} {a.period}: {data.get('pts')} companies. Each value is the last-filed fact "
                  "that best fits the CALENDAR period; fiscal periods differ by company (check start/end).\n")
            print(df.to_string(index=False))
    except SecError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
