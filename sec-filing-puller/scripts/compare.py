#!/usr/bin/env python3
"""Side-by-side comps from SEC EDGAR XBRL, with period-alignment warnings.

    export SEC_USER_AGENT="Your Company your.name@example.com"
    compare.py AAPL MSFT WMT
    compare.py AAPL MSFT WMT --basis ttm --metrics revenue,operating_income,net_income --out ./comps

Columns are each company's latest fiscal year and/or TTM. Fiscal years rarely line up
(AAPL ends late September, MSFT June 30, WMT January 31), so "FY2025" means a different
12 months for each company; the script prints the exact dates and warns when they drift.
TTM ending at each company's latest quarter is usually the fairer comparison.

Not investment advice.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec_pull as sp  # noqa: E402

DEFAULT = ["revenue", "gross_profit", "operating_income", "net_income", "eps_diluted",
           "operating_cash_flow", "capex", "cash", "total_assets", "lt_debt_noncurrent"]


def latest_rows(df: pd.DataFrame, basis: str) -> pd.DataFrame:
    """Pick, per metric, the latest FY row and/or the TTM row (instants: latest balance)."""
    out = []
    for metric, g in df.groupby("metric", sort=False):
        kind = sp.METRICS[metric]["kind"]
        if kind == "instant":
            g2 = g[g["value"].notna()]
            if not g2.empty:
                out.append(g2.sort_values("end").iloc[-1].to_dict() | {"col": "Latest balance"})
            continue
        if basis in ("fy", "both"):
            fy = g[(g["period_type"] == "FY")]
            if not fy.empty:
                out.append(fy.sort_values("fiscal_year").iloc[-1].to_dict() | {"col": "Latest FY"})
        if basis in ("ttm", "both"):
            t = g[g["period_type"] == "TTM"]
            if not t.empty:
                out.append(t.iloc[-1].to_dict() | {"col": "TTM"})
    return pd.DataFrame(out)


def margins(sel: pd.DataFrame) -> list[dict]:
    rows = []
    for col in sel["col"].unique():
        s = sel[sel["col"] == col].set_index("metric")
        rev = s["value"].get("revenue")
        if rev is None or pd.isna(rev) or rev == 0:
            continue
        for m, label in (("gross_profit", "Gross margin"), ("operating_income", "Operating margin"),
                         ("net_income", "Net margin")):
            v = s["value"].get(m)
            if v is not None and not pd.isna(v) and s.loc[m, "end"] == s.loc["revenue", "end"]:
                rows.append({"metric": m.replace("_income", "").replace("_profit", "") + "_margin",
                             "metric_label": label, "col": col, "value": v / rev,
                             "value_fmt": f"{100 * v / rev:.1f}%", "basis": "computed",
                             "period": s.loc["revenue", "period"], "end": s.loc["revenue", "end"],
                             "start": s.loc["revenue", "start"], "unit": "pure", "accn": "",
                             "notes": f"{m} / revenue, same period"})
    return rows


def alignment_warnings(info: list[dict], sel_all: pd.DataFrame) -> list[str]:
    w = []
    fy = {i["ticker"]: i for i in info if i.get("fy_end")}
    if len(fy) > 1:
        ends = {t: date.fromisoformat(i["fy_end"]) for t, i in fy.items()}
        spread = (max(ends.values()) - min(ends.values())).days
        if spread > 31:
            detail = "; ".join(f"{t} {i['fy_label']} = {i['fy_start']}..{i['fy_end']}" for t, i in fy.items())
            w.append(f"Fiscal years do not align (latest FY ends are {spread} days apart): {detail}. "
                     "Compare TTM, or calendarize, before ranking companies on annual figures.")
    q = {i["ticker"]: date.fromisoformat(i["q_end"]) for i in info if i.get("q_end")}
    if len(q) > 1:
        spread = (max(q.values()) - min(q.values())).days
        if spread > 45:
            w.append("Latest reported quarters end " + f"{spread} days apart ("
                     + ", ".join(f"{t} {d}" for t, d in q.items()) + "); TTM windows are offset by that much.")
    for i in info:
        if i.get("fy_days") and i["fy_days"] > 368:
            w.append(f"{i['ticker']} {i['fy_label']} is a 53-week year ({i['fy_days']} days); growth vs the prior "
                     "52-week year is overstated by roughly one week.")
        if i.get("q_end") and (date.today() - date.fromisoformat(i["q_end"])).days > 200:
            w.append(f"{i['ticker']} latest periodic filing covers a period ending {i['q_end']}: stale or delinquent; "
                     "check the submissions feed for NT 10-K/10-Q notices.")
    if not sel_all.empty:
        for metric, g in sel_all[sel_all["value"].notna() & sel_all["tag"].notna()].groupby("metric"):
            tags = g.groupby("ticker")["tag"].first()
            if tags.nunique() > 1:
                w.append(f"{metric}: companies use different XBRL tags (" + ", ".join(
                    f"{t}={tag.split(':')[-1]}" for t, tag in tags.items()) + "); definitions may differ"
                    + (" (e.g. total revenues incl. membership/other income vs net sales)." if metric == "revenue"
                       else "; check each company's notes column."))
        rev = sel_all[sel_all.get("revised", False) == True]  # noqa: E712
        for _, r in rev.iterrows():
            w.append(f"{r['ticker']} {r['metric']} {r['period']}: revised in a later filing "
                     f"(originally {r.get('original_value'):,.0f}). Latest-filed value shown.")
        units = sel_all[sel_all["unit"].notna() & ~sel_all["unit"].isin(["USD", "USD/shares", "shares", "pure"])]
        for _, r in units.iterrows():
            w.append(f"{r['ticker']} {r['metric']} is in {r['unit']}, not USD: convert before comparing.")
    return w


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("companies", nargs="+")
    ap.add_argument("--metrics", default=",".join(DEFAULT))
    ap.add_argument("--basis", choices=["fy", "ttm", "both"], default="both")
    ap.add_argument("--out", help="directory for comps.md / comps_long.csv")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args(argv)
    try:
        sp.user_agent()
    except sp.SecError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    metrics = [m.strip() for m in a.metrics.split(",") if m.strip()]
    bad = [m for m in metrics if m not in sp.METRICS]
    if bad:
        print(f"error: unknown metric(s) {bad}", file=sys.stderr)
        return 2

    info, sels, longs = [], [], []
    for q in a.companies:
        try:
            co, df = sp.pull(q, refresh=a.refresh, metrics=metrics, years=1, quarters=1)
        except sp.SecError as e:
            print(f"error: {q}: {e}", file=sys.stderr)
            return 2
        t = co["ticker"] or q.upper()
        longs.append(df)
        sel = latest_rows(df, a.basis)
        sel = pd.concat([sel, pd.DataFrame(margins(sel))], ignore_index=True) if not sel.empty else sel
        sel["ticker"] = t
        sels.append(sel)
        fyr = df[(df["period_type"] == "FY") & df["value"].notna()].sort_values("end")
        qr = df[(df["period_type"].isin(["Q", "instant"])) & df["value"].notna()].sort_values("end")
        i = {"ticker": t, "name": co["name"], "cik": co["cik"], "fye": co.get("fiscal_year_end")}
        if not fyr.empty:
            r = fyr.iloc[-1]
            i.update(fy_label=r["period"], fy_start=r["start"], fy_end=r["end"], fy_days=r["days"])
        if not qr.empty:
            qq = df[(df["period_type"] == "Q") & df["value"].notna()].sort_values("end")
            if not qq.empty:
                i.update(q_label=qq.iloc[-1]["period"], q_end=qq.iloc[-1]["end"])
        info.append(i)

    sel_all = pd.concat(sels, ignore_index=True)
    warns = [f"{t}: {w}" for t, df in zip([i["ticker"] for i in info], longs) for w in df.attrs.get("warnings", [])]
    warns += alignment_warnings(info, sel_all)

    lines = ["## Comps (SEC EDGAR XBRL, primary source)", "",
             "| Ticker | Company | FYE (MMDD) | Latest FY | Latest quarter |", "|---|---|---|---|---|"]
    for i in info:
        lines.append(f"| {i['ticker']} | {i['name']} | {i.get('fye') or ''} | {i.get('fy_label', '')} "
                     f"({i.get('fy_start', '')}..{i.get('fy_end', '')}) | "
                     + (f"{i['q_label']} ending {i['q_end']}" if i.get("q_end") else "none in XBRL (annual-only)") + " |")
    lines.append("")
    if warns:
        lines += ["**Period alignment and definition warnings**", ""] + [f"- {x}" for x in warns] + [""]

    cols = [c for c in ["Latest FY", "TTM"] if c in sel_all["col"].unique()]
    tickers = [i["ticker"] for i in info]
    header = ["Metric"] + [f"{t} {c}" for c in cols for t in tickers]
    lines += ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    order = metrics + [m for m in ["gross_margin", "operating_margin", "net_margin"]]
    labels = {m: sp.METRICS[m]["label"] for m in metrics}
    labels.update(gross_margin="Gross margin", operating_margin="Operating margin", net_margin="Net margin")
    for m in order:
        if m in sp.METRICS and sp.METRICS[m]["kind"] == "instant":
            continue
        cells = []
        for c in cols:
            for t in tickers:
                r = sel_all[(sel_all["ticker"] == t) & (sel_all["metric"] == m) & (sel_all["col"] == c)]
                v = r.iloc[0] if not r.empty else None
                cells.append("n/a" if v is None or pd.isna(v["value"]) else
                             v["value_fmt"] + (" (d)" if v["basis"] == "derived" and c != "TTM" else ""))
        if any(x != "n/a" for x in cells):
            lines.append(f"| {labels.get(m, m)} | " + " | ".join(cells) + " |")
    inst = [m for m in metrics if sp.METRICS[m]["kind"] == "instant"]
    if inst:
        lines += ["", "| Balance sheet (latest) | " + " | ".join(tickers) + " |", "|" + "---|" * (len(tickers) + 1)]
        for m in inst:
            cells = []
            for t in tickers:
                r = sel_all[(sel_all["ticker"] == t) & (sel_all["metric"] == m)]
                cells.append("n/a" if r.empty else f"{r.iloc[0]['value_fmt']} ({r.iloc[0]['end']})")
            lines.append(f"| {labels[m]} | " + " | ".join(cells) + " |")
    lines += ["", "TTM = sum of the latest four fiscal quarters (reported or derived). (d) = derived value. "
              "Per-row tags, formulas and accession numbers are in comps_long.csv.", "", "**Sources**", ""]
    for t, df in zip(tickers, longs):
        used = df[df["value"].notna() & df["accn"].notna()]
        accns = sorted({a.strip() for x in used["accn"] for a in str(x).split(";") if a.strip()})
        cik = int(df["cik"].iloc[0])
        lines.append(f"- {t}: " + ", ".join(f"[{x}]({sp.filing_index_url(cik, x)})" for x in accns))
    lines += ["", "Source: SEC EDGAR XBRL API (data.sec.gov). Not investment advice."]
    md = "\n".join(lines)
    print(md)
    if a.out:
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "comps.md").write_text(md + "\n")
        pd.concat(longs, ignore_index=True).to_csv(out / "comps_long.csv", index=False)
        sel_all.to_csv(out / "comps_selected.csv", index=False)
        print(f"\nwrote {out}/comps.md, comps_long.csv, comps_selected.csv", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
