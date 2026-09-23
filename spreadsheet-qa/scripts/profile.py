#!/usr/bin/env python3
"""Profile CSV/TSV/XLSX exports before answering any question about them.

For every file (and every sheet of a workbook) it reports: header row, row
count, grain (candidate primary keys and duplicate keys), per-column type with
parse rate, null %, distinct count, min/max, top values, suspected currency /
unit / timezone, date ranges, embedded total or footer rows, and, for .xlsx,
hidden rows/columns/sheets, autofilters, and merged cells. Across files it
flags shared key columns whose join would fan out.

Writes profile.json, profile.md, and a draft data_dictionary.md with open
questions to --out (default ./sqa_out).

    python3 profile.py orders.csv customers.csv refunds.csv --out sqa_out
    python3 profile.py export.xlsx --out sqa_out

Requires pandas (and openpyxl for .xlsx). Read-only: never modifies inputs.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

import pandas as pd

TOTAL_RE = re.compile(r"^\s*(grand\s+total|sub\s*-?total|totals?|sum|overall|all\s+(rows|customers|orders))\b[:\s]*$", re.I)
FOOTER_RE = re.compile(r"^\s*(filter(ed)?\s*(by|:)|applied filters|generated (on|at|by)|report (run|generated)|page \d+|confidential|source:|notes?:)", re.I)
CURRENCY_SYMBOLS = {"$": "USD or other dollar", "\u20ac": "EUR", "\u00a3": "GBP", "\u00a5": "JPY/CNY", "\u20b9": "INR", "R$": "BRL", "C$": "CAD", "A$": "AUD"}
ISO_CCY = {"USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CNY", "INR", "BRL", "MXN", "CHF", "SEK", "NOK", "DKK", "NZD", "SGD", "HKD", "ZAR", "PLN"}
NUM_CLEAN_RE = re.compile(r"[\s,$\u20ac\u00a3\u00a5\u20b9%]|[A-Z]{3}$|^[A-Z]{3}\s?|^[RCA]\$")
ID_NAME_RE = re.compile(r"(^id$|_id$|^id_|\bid\b|number$|_no$|^sku$|^email$|key$|code$|uuid)", re.I)
DATE_NAME_RE = re.compile(r"(date|_at$|time|created|updated|closed|day|month|period)", re.I)
MONEY_NAME_RE = re.compile(r"(amount|revenue|price|total|cost|fee|mrr|arr|value|spend|paid|net|gross|balance|refund|tax|discount)", re.I)
TZ_SUFFIX_RE = re.compile(r"(Z|[+-]\d{2}:?\d{2}|\bUTC\b|\bGMT\b|\b[A-Z]{3,4}T\b)\s*$")


# ---------------------------------------------------------------- loading
def detect_header_row(raw: pd.DataFrame, max_scan: int = 15) -> int:
    """Pick the first row that looks like a header: mostly non-empty, mostly
    non-numeric text, and followed by a row with at least as many filled cells."""
    ncols = raw.shape[1]
    if ncols == 0:
        return 0
    best = 0
    for i in range(min(max_scan, len(raw))):
        row = raw.iloc[i]
        filled = row.notna() & (row.astype(str).str.strip() != "")
        nfill = int(filled.sum())
        if nfill < max(2, int(0.6 * ncols)):
            continue
        vals = row[filled].astype(str)
        texty = sum(1 for v in vals if not _is_number(v) and not _looks_date(v))
        if texty / max(nfill, 1) < 0.8:
            continue
        if i + 1 < len(raw):
            nxt = raw.iloc[i + 1]
            if int((nxt.notna() & (nxt.astype(str).str.strip() != "")).sum()) < 0.5 * nfill:
                continue
        best = i
        break
    return best


def load_tables(path):
    """Yield (table_name, dataframe_of_strings, header_row, xlsx_meta)."""
    base = os.path.splitext(os.path.basename(path))[0]
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm", ".xls"):
        sheets = pd.read_excel(path, sheet_name=None, header=None, dtype=object)
        meta_all = xlsx_meta(path) if ext != ".xls" else {}
        for sheet, raw in sheets.items():
            raw = raw.dropna(how="all", axis=1)
            if raw.dropna(how="all").empty:
                continue
            h = detect_header_row(raw)
            df = _frame_from_raw(raw, h)
            name = f"{base}__{_slug(sheet)}" if len(sheets) > 1 else base
            yield name, df, h, meta_all.get(sheet, {}), sheet
    else:
        sep = "\t" if ext in (".tsv", ".tab") else None
        raw = pd.read_csv(path, header=None, dtype=str, sep=sep, engine="python",
                          keep_default_na=True, skip_blank_lines=False, encoding_errors="replace")
        h = detect_header_row(raw)
        yield base, _frame_from_raw(raw, h), h, {}, None


def _frame_from_raw(raw, h):
    header = [str(c).strip() if pd.notna(c) and str(c).strip() else f"unnamed_{j}" for j, c in enumerate(raw.iloc[h])]
    seen = Counter()
    cols = []
    for c in header:
        seen[c] += 1
        cols.append(c if seen[c] == 1 else f"{c}__{seen[c]}")
    df = raw.iloc[h + 1:].copy()
    df.columns = cols
    df = df.map(lambda v: None if (v is None or (isinstance(v, float) and pd.isna(v)) or str(v).strip() == "") else v)
    df.index = range(h + 2, h + 2 + len(df))  # 1-based source line/row numbers
    return df


def xlsx_meta(path):
    try:
        from openpyxl import load_workbook
    except ImportError:
        return {}
    out = {}
    wb = load_workbook(path, read_only=False, data_only=True)
    for ws in wb.worksheets:
        hidden_rows = [r for r, d in ws.row_dimensions.items() if d.hidden]
        hidden_cols = [c for c, d in ws.column_dimensions.items() if d.hidden]
        out[ws.title] = {
            "sheet_state": ws.sheet_state,
            "hidden_rows": sorted(hidden_rows),
            "hidden_columns": sorted(hidden_cols),
            "autofilter": ws.auto_filter.ref if ws.auto_filter and ws.auto_filter.ref else None,
            "merged_ranges": [str(m) for m in ws.merged_cells.ranges][:20],
        }
    return out


# ---------------------------------------------------------------- parsing
def _is_number(s):
    return _to_num(s) is not None


def _to_num(s):
    if s is None:
        return None
    if isinstance(s, (int, float)) and not isinstance(s, bool):
        return None if pd.isna(s) else float(s)
    t = str(s).strip()
    if not t:
        return None
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    t = NUM_CLEAN_RE.sub("", t)
    if t.endswith("-"):
        neg, t = True, t[:-1]
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def _looks_date(s):
    t = str(s).strip()
    return bool(re.match(r"^\d{4}-\d{1,2}-\d{1,2}", t) or re.match(r"^\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}", t)
                or re.match(r"^[A-Za-z]{3,9} \d{1,2},? \d{4}", t))


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_") or "sheet"


def profile_column(name, s: pd.Series):
    n = len(s)
    nn = s.dropna()
    raw_strs = nn.map(lambda v: str(v).strip())
    info = {"column": name, "null_pct": round(100 * (1 - len(nn) / n), 1) if n else 0.0,
            "distinct": int(raw_strs.nunique()), "non_null": int(len(nn))}
    flags = []
    if len(nn) == 0:
        info.update(type="empty", parse_rate=0.0)
        return info, ["column is entirely empty"]

    native_dt = nn.map(lambda v: hasattr(v, "year") and hasattr(v, "month")).mean()
    nums = nn.map(_to_num)
    num_rate = nums.notna().mean()
    plain_num_rate = raw_strs.map(lambda t: bool(re.fullmatch(r"-?\d+(\.\d+)?", t))).mean()
    date_like = raw_strs.map(_looks_date).mean()
    dts = pd.to_datetime(raw_strs, errors="coerce", utc=False, format="mixed") if date_like > 0 or native_dt > 0 else pd.Series([pd.NaT] * len(nn))
    dt_rate = max(float(dts.notna().mean()) if len(dts) else 0.0, float(native_dt))

    if dt_rate >= 0.8 and dt_rate >= num_rate:
        typ, rate = "datetime", dt_rate
        good = pd.to_datetime(dts.dropna().astype(str).str.replace(r"(Z|[+-]\d{2}:?\d{2})$", "", regex=True), errors="coerce")
        if good.notna().any():
            info["min"], info["max"] = str(good.min()), str(good.max())
            info["date_range_days"] = int((good.max() - good.min()).days)
        has_time = raw_strs.str.contains(r"\d{1,2}:\d{2}").mean()
        tz_hits = raw_strs.map(lambda t: (m := TZ_SUFFIX_RE.search(t)) and m.group(1)).dropna()
        if has_time > 0.5:
            if len(tz_hits) == 0:
                info["timezone"] = "none stated (naive timestamps)"
                flags.append("timestamps carry no timezone; confirm the export's timezone before bucketing by day")
            else:
                zones = sorted(set(tz_hits))
                info["timezone"] = ", ".join("UTC (Z suffix)" if z == "Z" else z for z in zones)
                if zones in (["Z"], ["+00:00"], ["UTC"]):
                    flags.append("timestamps are UTC; a 'day' or 'month' in the business's local time differs near midnight")
                elif len(zones) > 1:
                    flags.append(f"mixed timezone offsets: {zones}")
        if raw_strs.str.match(r"^\d{1,2}/\d{1,2}/\d{2,4}").mean() > 0.5:
            amb = raw_strs[raw_strs.str.match(r"^\d{1,2}/\d{1,2}/")].map(lambda t: [int(x) for x in t.split("/")[:2]])
            if not any(a > 12 or b > 12 for a, b in amb):
                flags.append("slash dates where both parts are <= 12: day-first vs month-first is ambiguous")
    elif num_rate >= 0.8:
        typ, rate = "number", float(num_rate)
        v = nums.dropna()
        info["min"], info["max"] = float(v.min()), float(v.max())
        info["sum"] = round(float(v.sum()), 4)
        if plain_num_rate < num_rate - 0.001:
            ex = raw_strs[~raw_strs.str.fullmatch(r"-?\d+(\.\d+)?")].head(3).tolist()
            flags.append(f"numbers stored as text with symbols/commas (e.g. {ex}); parse explicitly, do not trust auto-typing")
        syms = sorted({k for t in raw_strs for k in CURRENCY_SYMBOLS if k in t})
        codes = sorted({m for t in raw_strs for m in re.findall(r"\b[A-Z]{3}\b", t) if m in ISO_CCY})
        if syms or codes:
            info["currency_in_values"] = syms + codes
            if len(syms) + len(codes) > 1:
                flags.append(f"mixed currency markers inside values: {syms + codes}")
        if DATE_NAME_RE.search(name) and v.between(20000, 60000).mean() > 0.8 and (v == v.round()).mean() > 0.8:
            flags.append("integers 20000-60000 in a date-named column: likely Excel date serials (day 0 = 1899-12-30)")
            info["excel_serial_range"] = [str(pd.Timestamp("1899-12-30") + pd.Timedelta(days=float(v.min()))),
                                          str(pd.Timestamp("1899-12-30") + pd.Timedelta(days=float(v.max())))]
        if raw_strs.str.endswith("%").mean() > 0.5:
            info["unit"] = "percent"
        if raw_strs.str.match(r"^0\d+$").mean() > 0.2:
            flags.append("values with leading zeros: treat as text codes (ZIP, SKU), not numbers")
        if (v < 0).any() and MONEY_NAME_RE.search(name):
            flags.append(f"{int((v < 0).sum())} negative values: refunds/credits may already be netted in this column")
    else:
        lower = raw_strs.str.lower()
        if set(lower.unique()) <= {"true", "false", "yes", "no", "y", "n", "1", "0", "t", "f"}:
            typ, rate = "boolean", 1.0
        else:
            typ, rate = "text", 1.0
            if 0.2 < num_rate < 0.8:
                flags.append(f"mixed column: {round(100 * num_rate)}% parse as numbers, rest do not")
        vals = set(raw_strs.str.upper().unique())
        if vals and vals <= ISO_CCY:
            info["currency_codes"] = sorted(vals)
            if len(vals) > 1:
                flags.append(f"currency column holds {len(vals)} currencies {sorted(vals)}: never sum amounts across them without conversion")
        cased = raw_strs.groupby(lower).nunique()
        if (cased > 1).any():
            flags.append(f"same value in different case/spacing, e.g. {cased[cased > 1].index[:3].tolist()}")
        if (raw_strs != nn.map(str)).any():
            flags.append("leading/trailing whitespace in values")
    info["type"], info["parse_rate"] = typ, round(float(rate), 3)
    info["top_values"] = [[str(k), int(c)] for k, c in raw_strs.value_counts().head(5).items()]
    if MONEY_NAME_RE.search(name) and typ == "number":
        info["suspected_unit"] = "money"
    return info, flags


def find_total_rows(df):
    """Rows labelled as totals/footers, plus rows whose numeric value equals the
    sum of all other rows in that column (an unlabelled grand total)."""
    hits = {}
    for idx, row in df.iterrows():
        for col, v in row.items():
            if v is None:
                continue
            t = str(v)
            if TOTAL_RE.match(t):
                hits.setdefault(idx, []).append(f"'{t.strip()}' in {col}")
            elif FOOTER_RE.match(t):
                hits.setdefault(idx, []).append(f"footer text '{t.strip()[:40]}' in {col}")
    for col in df.columns:
        nums = df[col].map(_to_num)
        if nums.notna().mean() < 0.8 or nums.notna().sum() < 4:
            continue
        total = nums.sum()
        for idx, v in nums.dropna().items():
            rest = total - v
            if v != 0 and abs(rest - v) <= max(0.01, 1e-6 * abs(v)):
                hits.setdefault(idx, []).append(f"{col}={v:g} equals the sum of all other rows")
    fill = df.notna().mean(axis=1)
    for idx in fill[fill <= 0.34].index:
        if idx not in hits and len(df.columns) >= 4:
            hits.setdefault(idx, []).append(f"sparse row ({int(fill[idx] * len(df.columns))}/{len(df.columns)} cells filled): footer, note, or section break?")
    return [{"row": int(k), "why": v, "values": {c: df.at[k, c] for c in df.columns if df.at[k, c] is not None}} for k, v in sorted(hits.items())]


def grain(df, total_rows):
    body = df.drop(index=[t["row"] for t in total_rows if t["row"] in df.index], errors="ignore")
    n = len(body)
    cands, dups = [], []
    for c in body.columns:
        s = body[c]
        if s.isna().any() or n == 0:
            if ID_NAME_RE.search(c) and s.notna().sum() > 0:
                vc = s.dropna().astype(str).value_counts()
                if (vc > 1).any():
                    dups.append({"column": c, "duplicated_values": int((vc > 1).sum()),
                                 "extra_rows": int((vc[vc > 1] - 1).sum()), "examples": vc[vc > 1].head(5).to_dict()})
            continue
        vc = s.astype(str).value_counts()
        if len(vc) == n:
            cands.append([c])
        elif ID_NAME_RE.search(c) and len(vc) >= 0.5 * n:
            d = vc[vc > 1]
            dups.append({"column": c, "duplicated_values": int(len(d)), "extra_rows": int((d - 1).sum()),
                         "examples": d.head(5).to_dict()})
    if not cands and n:
        cols = [c for c in body.columns if body[c].notna().all()][:12]
        for i, a in enumerate(cols):
            for b in cols[i + 1:]:
                if not body.duplicated([a, b]).any():
                    cands.append([a, b])
            if len(cands) >= 5:
                break
    ranked = sorted(cands, key=lambda k: (len(k), 0 if ID_NAME_RE.search(k[0]) else 1))
    exact_dup_rows = int(body.duplicated().sum())
    return {"rows_excluding_flagged": n, "candidate_keys": ranked[:5], "duplicate_keys": dups,
            "exact_duplicate_rows": exact_dup_rows}


# ---------------------------------------------------------------- cross-file
def join_risks(tables):
    """For every column name shared by two tables, report whether a join on it
    would fan out (key not unique on either side)."""
    risks = []
    names = list(tables)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared = [c for c in tables[a]["df"].columns if c in tables[b]["df"].columns and ID_NAME_RE.search(c)]
            for c in shared:
                ka = tables[a]["df"][c].dropna().astype(str)
                kb = tables[b]["df"][c].dropna().astype(str)
                ua, ub = ka.is_unique, kb.is_unique
                ca, cb = ka.value_counts(), kb.value_counts()
                inner = int(sum(ca.get(k, 0) * cb.get(k, 0) for k in set(ca.index) & set(cb.index)))
                entry = {"left": a, "right": b, "column": c, "left_unique": bool(ua), "right_unique": bool(ub),
                         "left_rows": int(len(ka)), "right_rows": int(len(kb)), "inner_join_rows": inner,
                         "left_keys_missing_in_right": int((~ka.isin(set(kb))).sum()),
                         "right_keys_missing_in_left": int((~kb.isin(set(ka))).sum())}
                # The "lookup" side is the one closer to one-row-per-key (customers vs orders).
                ra, rb = ka.nunique() / max(len(ka), 1), kb.nunique() / max(len(kb), 1)
                dim, fact = (a, b) if ra >= rb else (b, a)
                cdim, cfact = (ca, cb) if dim == a else (cb, ca)
                if ua and ub:
                    entry["verdict"] = "one-to-one"
                elif cdim.max() == 1:
                    entry["verdict"] = f"one-to-many ({dim} unique per {c}); safe, aggregate on the {fact} side"
                else:
                    dupkeys = cdim[cdim > 1]
                    fan = int(sum(cfact.get(k, 0) * (n - 1) for k, n in dupkeys.items()))
                    entry["fanout_rows"] = fan
                    entry["verdict"] = (f"FAN-OUT: {dim}.{c} should be one row per key but {len(dupkeys)} keys repeat "
                                        f"(e.g. {list(dupkeys.index[:3])}); joining {fact} to {dim} adds {fan} rows "
                                        f"and double counts their amounts. Dedupe {dim} first (pick one row per key).")
                risks.append(entry)
    return risks


# ---------------------------------------------------------------- output
def build(paths, out):
    os.makedirs(out, exist_ok=True)
    tables = {}
    for p in paths:
        for name, df, h, meta, sheet in load_tables(p):
            cols, flags = [], {}
            totals = find_total_rows(df)
            body = df.drop(index=[t["row"] for t in totals])  # column stats exclude flagged rows
            for c in df.columns:
                info, f = profile_column(c, body[c])
                if info.get("currency_codes") and body[c].dropna().is_unique:
                    f = [x for x in f if "currencies" not in x]  # a lookup table (e.g. FX rates), not mixed amounts
                cols.append(info)
                if f:
                    flags[c] = f
            g = grain(df, totals)
            table_flags = []
            if h:
                table_flags.append(f"header is on row {h + 1}, not row 1: {h} title/preamble rows above it")
            if totals:
                table_flags.append(f"{len(totals)} total/footer/sparse rows embedded in the data; exclude them or every SUM double counts")
            for d in g["duplicate_keys"]:
                table_flags.append(f"duplicate key values in {d['column']}: {d['duplicated_values']} keys repeat, {d['extra_rows']} extra rows")
            if g["exact_duplicate_rows"]:
                table_flags.append(f"{g['exact_duplicate_rows']} exact duplicate rows")
            if meta:
                if meta.get("sheet_state") != "visible":
                    table_flags.append(f"sheet is {meta['sheet_state']}")
                if meta.get("hidden_rows"):
                    table_flags.append(f"hidden rows {meta['hidden_rows'][:10]}: pandas reads them; decide whether they belong")
                if meta.get("hidden_columns"):
                    table_flags.append(f"hidden columns {meta['hidden_columns']}")
                if meta.get("autofilter"):
                    table_flags.append(f"autofilter on {meta['autofilter']}: the user may have been looking at a filtered view, totals they quote may be filtered")
                if meta.get("merged_ranges"):
                    table_flags.append(f"merged cells {meta['merged_ranges'][:5]}: values sit only in the top-left cell")
            ccy_cols = [c["column"] for c in cols if len(c.get("currency_codes", [])) > 1 or len(c.get("currency_in_values", [])) > 1]
            tables[name] = {"source": p, "sheet": sheet, "header_row": h + 1, "rows": len(df), "columns": cols,
                            "column_flags": flags, "total_rows": totals, "grain": g, "table_flags": table_flags,
                            "xlsx": meta, "mixed_currency_columns": ccy_cols, "df": df}
    risks = join_risks(tables)
    report = {"tables": {k: {kk: vv for kk, vv in v.items() if kk != "df"} for k, v in tables.items()}, "join_risks": risks}
    with open(os.path.join(out, "profile.json"), "w") as f:
        json.dump(report, f, indent=2, default=str)
    with open(os.path.join(out, "profile.md"), "w") as f:
        f.write(render_md(report))
    with open(os.path.join(out, "data_dictionary.md"), "w") as f:
        f.write(render_dictionary(report))
    return report


def _cell(v):
    return str(v).replace("|", "\\|").replace("\n", " ")[:60]


def render_md(r):
    L = ["# Data profile", ""]
    for name, t in r["tables"].items():
        L += [f"## {name}", f"Source: `{t['source']}`" + (f" sheet `{t['sheet']}`" if t["sheet"] else ""),
              f"Header row: {t['header_row']}  |  Data rows: {t['rows']}  |  Rows after excluding flagged: {t['grain']['rows_excluding_flagged']}", ""]
        keys = t["grain"]["candidate_keys"]
        L.append(f"Grain: candidate key(s) {', '.join('+'.join(k) for k in keys) if keys else 'NONE FOUND (no unique column or pair)'}")
        dk = [d["column"] for d in t["grain"]["duplicate_keys"]]
        if dk:
            L.append(f"Key-like columns that are NOT unique: {', '.join(dk)} (if one of these is the intended key, the table has duplicates)")
        if t["total_rows"]:
            L.append("Column stats below exclude the flagged total/footer rows.")
        L.append("")
        if t["table_flags"]:
            L.append("Warnings:")
            L += [f"- {x}" for x in t["table_flags"]]
            L.append("")
        if t["total_rows"]:
            L.append("Embedded total/footer rows (row numbers are source lines):")
            L += [f"- row {x['row']}: {'; '.join(x['why'])}" for x in t["total_rows"]]
            L.append("")
        L += ["| column | type | parse % | null % | distinct | min | max | top values | notes |", "|---|---|---|---|---|---|---|---|---|"]
        for c in t["columns"]:
            notes = []
            for k in ("timezone", "currency_codes", "currency_in_values", "suspected_unit", "unit", "excel_serial_range"):
                if k in c:
                    notes.append(f"{k}: {c[k]}")
            notes += t["column_flags"].get(c["column"], [])
            top = ", ".join(f"{_cell(v)} ({n})" for v, n in c.get("top_values", [])[:3])
            L.append(f"| {c['column']} | {c['type']} | {round(100 * c.get('parse_rate', 0))} | {c['null_pct']} | {c['distinct']} | "
                     f"{_cell(c.get('min', ''))} | {_cell(c.get('max', ''))} | {top} | {_cell('; '.join(notes)) if len(notes) < 2 else '<br>'.join(_cell(n) for n in notes)} |")
        L.append("")
    if r["join_risks"]:
        L += ["## Join risks", ""]
        for j in r["join_risks"]:
            L.append(f"- `{j['left']}.{j['column']}` to `{j['right']}.{j['column']}`: {j['verdict']} "
                     f"(inner join rows {j['inner_join_rows']}; left keys missing on right {j['left_keys_missing_in_right']}, "
                     f"right keys missing on left {j['right_keys_missing_in_left']})")
        L.append("")
    return "\n".join(L)


def render_dictionary(r):
    L = ["# Data dictionary (DRAFT: confirm the open questions before quoting numbers)", ""]
    qs = []
    for name, t in r["tables"].items():
        keys = t["grain"]["candidate_keys"]
        L += [f"## {name}", f"One row = _TODO: describe the grain_ (candidate key: {'+'.join(keys[0]) if keys else 'none'})", "",
              "| column | type | meaning | example | notes |", "|---|---|---|---|---|"]
        for c in t["columns"]:
            ex = c.get("top_values", [[""]])[0][0] if c.get("top_values") else ""
            notes = "; ".join(t["column_flags"].get(c["column"], []))
            L.append(f"| {c['column']} | {c['type']} | _TODO_ | {_cell(ex)} | {_cell(notes)} |")
        L.append("")
        if t["total_rows"]:
            qs.append(f"{name}: rows {[x['row'] for x in t['total_rows']]} look like totals/footers. Exclude them? (default: yes)")
        for d in t["grain"]["duplicate_keys"]:
            qs.append(f"{name}.{d['column']} repeats for {d['duplicated_values']} keys (e.g. {list(d['examples'])[:3]}). Which row wins? (default: most recently updated)")
        if not keys:
            qs.append(f"{name}: no unique key found. What is one row?")
        for c in t["columns"]:
            if len(c.get("currency_codes", [])) > 1:
                qs.append(f"{name}.{c['column']} has {c['currency_codes']}. Report in which currency, at which FX rates and dates?")
            if c.get("timezone", "").startswith("none"):
                qs.append(f"{name}.{c['column']} has no timezone. What zone is it in, and which zone defines a business day?")
            elif c.get("timezone") and c["type"] == "datetime":
                qs.append(f"{name}.{c['column']} is {c['timezone']}. Bucket days/months in that zone or the business's local zone? (default: UTC, stated)")
            if c.get("suspected_unit") == "money":
                qs.append(f"{name}.{c['column']}: gross or net of discounts/tax/refunds/fees?")
            if "excel_serial_range" in c:
                qs.append(f"{name}.{c['column']} looks like Excel serial dates {c['excel_serial_range']}. Convert? (default: yes)")
        if t.get("xlsx", {}).get("hidden_rows"):
            qs.append(f"{name}: hidden rows {t['xlsx']['hidden_rows'][:10]}. Include or exclude? (default: include, and say so)")
        if t.get("xlsx", {}).get("autofilter"):
            qs.append(f"{name}: an autofilter exists. Is the number you want from the full sheet or a filtered view?")
    for j in r["join_risks"]:
        if "fanout_rows" in j or j["verdict"].startswith("MANY"):
            qs.append(f"Join {j['left']}/{j['right']} on {j['column']}: {j['verdict']}")
    L += ["## Open questions", ""] + [f"{i}. {q}" for i, q in enumerate(qs, 1)]
    L += ["", "## Metric definitions in use", "", "_Fill in: metric, exact definition, filters, source columns. See references/metric-definitions.md._", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", default="sqa_out")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    r = build(a.paths, a.out)
    if not a.quiet:
        for name, t in r["tables"].items():
            print(f"{name}: {t['rows']} rows, header row {t['header_row']}, keys {t['grain']['candidate_keys'][:2]}")
            for f in t["table_flags"]:
                print(f"  ! {f}")
            for col, fl in t["column_flags"].items():
                for f in fl:
                    print(f"  - {col}: {f}")
        for j in r["join_risks"]:
            print(f"join {j['left']}.{j['column']} ~ {j['right']}.{j['column']}: {j['verdict']}")
        print(f"\nWrote {a.out}/profile.md, profile.json, data_dictionary.md")
    return r


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
