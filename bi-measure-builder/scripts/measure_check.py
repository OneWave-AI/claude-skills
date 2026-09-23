#!/usr/bin/env python3
"""Compute the expected output of a BI measure from a small CSV sample.

The point is an independent oracle: build the number the DAX / Tableau / LookML
calculation *should* return for each visual row and for the grand total, then
compare against what the tool actually shows.

Semantics mirror how BI tools evaluate measures:
  * Every row AND the total are evaluated in their own context (the total is
    re-computed over the whole range, never summed from rows).
  * `range` is the report/slicer date filter. Time-intelligence calcs
    (prior_year, ytd, running_total, rolling, new/returning) read dates outside
    the range, exactly like SAMEPERIODLASTYEAR / DATESYTD / a FIXED LOD do.
  * `filters` are non-date filters (slicers on region, product...). They apply
    to everything, including history.
  * An empty result is BLANK (None), not 0.

Usage:
  python measure_check.py --data sales.csv --spec spec.json
  python measure_check.py --data sales.csv --spec spec.json --actual actual.csv
  python measure_check.py --data sales.csv --spec spec.json --json

--actual is a CSV with columns `label,value` (label = a row label as printed,
or `Total`). Exit code 1 if any value differs beyond --tol.
"""
import argparse
import json
import sys

import pandas as pd

TIME_CALCS = {"sum", "count_rows", "distinct_count", "ytd", "prior_year", "yoy_delta",
              "yoy_pct", "running_total", "rolling", "new_customers",
              "returning_customers", "last_balance"}
GROUP_CALCS = {"pct_of_total", "rank"}
FREQ = {"day": "D", "month": "M", "quarter": "Q", "year": "Y"}


def load(data_path, spec):
    df = pd.read_csv(data_path)
    for col, allowed in (spec.get("filters") or {}).items():
        df = df[df[col].astype(str).isin([str(v) for v in allowed])]
    if spec.get("date_column"):
        df = df.copy()
        df["_d"] = pd.to_datetime(df[spec["date_column"]]).dt.normalize()
    return df


def window(df, start, end):
    return df[(df["_d"] >= start) & (df["_d"] <= end)]


def blank_sum(s):
    return None if len(s) == 0 else float(s.sum())


def evaluate(calc, df, spec, start, end):
    """Evaluate a time calc for the context [start, end] (inclusive dates)."""
    p = spec.get("params", {})
    val, key = spec.get("value_column"), spec.get("key_column")
    cur = window(df, start, end)
    if calc == "sum":
        return blank_sum(cur[val])
    if calc == "count_rows":
        return None if cur.empty else float(len(cur))
    if calc == "distinct_count":
        n = cur[key].dropna().nunique()
        return None if n == 0 else float(n)
    if calc == "prior_year":
        off = pd.DateOffset(years=1)
        return blank_sum(window(df, start - off, end - off)[val])
    if calc in ("yoy_delta", "yoy_pct"):
        c = evaluate("sum", df, spec, start, end)
        py = evaluate("prior_year", df, spec, start, end)
        if c is None or py is None:
            return None
        if calc == "yoy_delta":
            return c - py
        return None if py == 0 else (c - py) / py
    if calc == "ytd":
        fy = int(p.get("fiscal_year_start_month", 1))
        ys = pd.Timestamp(end.year if end.month >= fy else end.year - 1, fy, 1)
        return blank_sum(window(df, ys, end)[val])
    if calc == "running_total":
        return blank_sum(df[df["_d"] <= end][val])
    if calc == "rolling":
        n = int(p["window"])
        last = end.to_period(FREQ[spec["grain"]])
        ws = (last - (n - 1)).start_time.normalize()
        return blank_sum(window(df, ws, end)[val])
    if calc in ("new_customers", "returning_customers"):
        first = df.groupby(key)["_d"].min()          # lifetime first purchase
        active = cur[key].dropna().unique()
        f = first.loc[active]
        n = int((f >= start).sum()) if calc == "new_customers" else int((f < start).sum())
        return None if n == 0 else float(n)
    if calc == "last_balance":
        if cur.empty:
            return None
        if p.get("mode", "per_entity") == "global_last_date":
            return float(cur[cur["_d"] == cur["_d"].max()][val].sum())
        idx = cur.groupby(key)["_d"].idxmax()        # each entity's last snapshot
        return float(cur.loc[idx, val].sum())
    raise ValueError(f"unknown calc {calc}")


def run(df, spec):
    calc = spec["calc"]
    rows = []
    if calc in TIME_CALCS:
        rs, re_ = pd.Timestamp(spec["range"]["start"]), pd.Timestamp(spec["range"]["end"])
        for per in pd.period_range(rs, re_, freq=FREQ[spec["grain"]]):
            s = max(per.start_time.normalize(), rs)
            e = min(per.end_time.normalize(), re_)
            rows.append((str(per), evaluate(calc, df, spec, s, e)))
        total = evaluate(calc, df, spec, rs, re_)
    elif calc in GROUP_CALCS:
        g, val = spec["group_column"], spec["value_column"]
        d = df
        if spec.get("range"):
            d = window(df, pd.Timestamp(spec["range"]["start"]), pd.Timestamp(spec["range"]["end"]))
        sums = d.groupby(g)[val].sum().astype(float)
        if calc == "pct_of_total":
            grand = sums.sum()
            rows = [(str(k), None if grand == 0 else v / grand) for k, v in sums.items()]
            total = 1.0 if grand else None
        else:
            p = spec.get("params", {})
            method = "dense" if p.get("ties", "skip") == "dense" else "min"
            ranks = sums.rank(method=method, ascending=p.get("order", "desc") == "asc")
            rows = sorted(((str(k), float(v)) for k, v in ranks.items()), key=lambda r: r[1])
            total = None  # a rank has no meaningful grand total; guard it with ISINSCOPE
    else:
        raise ValueError(f"unknown calc {calc}")
    return rows, total


def fmt(v, pct):
    if v is None:
        return "BLANK"
    return f"{v:.4%}" if pct else (f"{v:,.0f}" if float(v).is_integer() else f"{v:,.4f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--actual", help="CSV label,value of what the BI tool shows")
    ap.add_argument("--tol", type=float, default=1e-6)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    rows, total = run(load(a.data, spec), spec)
    if a.json:
        print(json.dumps({"rows": dict(rows), "Total": total}, indent=2))
        return 0
    pct = spec["calc"] in ("yoy_pct", "pct_of_total")
    print(f"calc: {spec['calc']}  grain: {spec.get('grain', spec.get('group_column'))}  "
          f"range: {spec.get('range')}  filters: {spec.get('filters') or {}}\n")
    print("| row | expected |\n|---|---|")
    for label, v in rows:
        print(f"| {label} | {fmt(v, pct)} |")
    print(f"| **Total** | **{fmt(total, pct)}** |")
    visible = [v for _, v in rows if v is not None]
    if visible and total is not None and spec["calc"] not in ("rank",):
        s = sum(visible)
        if abs(s - total) > a.tol:
            print(f"\nNote: sum of visible rows = {fmt(s, pct)} but the correct total is "
                  f"{fmt(total, pct)}. This measure is non-additive; a BI total that equals the "
                  f"row sum is the bug, not the other way round (unless the business asked for "
                  f"a visual total, which needs SUMX / WINDOW_SUM / a derived table).")
    if a.actual:
        exp = dict(rows)
        exp["Total"] = total
        bad = 0
        for _, r in pd.read_csv(a.actual).iterrows():
            lab = str(r["label"])
            got = None if pd.isna(r["value"]) else float(r["value"])
            want = exp.get(lab, "missing")
            ok = (want is None and got is None) or (
                want not in (None, "missing") and got is not None and abs(want - got) <= a.tol)
            if not ok:
                bad += 1
                print(f"MISMATCH {lab}: tool shows {got}, expected {want}")
        print("\nAll actual values match." if not bad else f"\n{bad} mismatch(es).")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
