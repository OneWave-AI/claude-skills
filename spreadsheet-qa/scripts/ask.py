#!/usr/bin/env python3
"""Answer one business question over CSV/XLSX files with SQL, auditably.

The question is a JSON spec of ordered SQL steps. Each step becomes a view
built on earlier ones, so the script can count rows at every stage and prove
nothing was silently dropped or multiplied:

  kind "clean"     parse/cast raw text columns; reports rows in vs out
  kind "filter"    WHERE clauses; reports rows before (from `from`) and after
  kind "join"      reports rows before (from `base`) and after; FAILS the run
                   if rows increased (join fan-out) unless "allow_fanout": true,
                   and warns if rows decreased (inner join dropped rows)
  kind "dedupe"    one row per key; reports rows removed
  kind "aggregate" the final answer (last step)

Outputs to --out: answer.md (number, definition, full query, step-by-step row
counts, reconciliation, sample rows, caveats), query.sql (one runnable WITH
query), steps.json, and rows_used.csv (every row feeding the answer).

    python3 ask.py spec.json --out sqa_out/q1
    python3 ask.py --table orders=orders.csv --sql "SELECT count(*) AS n FROM orders" --out sqa_out/adhoc

Engine: DuckDB when installed (pip install duckdb), else SQLite. Every input
column is loaded as TEXT on purpose: cast explicitly in a "clean" step so a
"$1,200.00" or an Excel serial never gets silently mis-typed. Helpers
available in SQL on both engines:
  to_num(x)      "$1,200.50" -> 1200.5, "(35.00)" -> -35, "12%" -> 12, junk -> NULL
  excel_date(x)  46204 -> '2026-07-01' (Excel 1900 date system)
DuckDB also has timezone conversion, e.g.
  CAST(created_at AS TIMESTAMPTZ) AT TIME ZONE 'America/New_York'
"""
import argparse
import json
import math
import os
import re
import sys
from datetime import date, timedelta

import pandas as pd

MACROS = """-- to_num / excel_date are registered by ask.py. To rerun this file in plain DuckDB, first run:
-- CREATE MACRO to_num(x) AS (CASE WHEN trim(x) LIKE '(%)' THEN -1 ELSE 1 END)
--   * TRY_CAST(regexp_replace(x, '[^0-9.\\-]', '', 'g') AS DOUBLE);
-- CREATE MACRO excel_date(x) AS DATE '1899-12-30' + CAST(TRY_CAST(x AS DOUBLE) AS INTEGER);
-- and load each source table as all-VARCHAR, e.g.
-- CREATE TABLE orders AS SELECT * FROM read_csv('orders.csv', all_varchar = true);
"""
KINDS = {"clean", "filter", "join", "dedupe", "aggregate", "derive"}


# ---------------------------------------------------------------- helpers
def to_num(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return None if (isinstance(x, float) and math.isnan(x)) else float(x)
    t = str(x).strip()
    if not t:
        return None
    neg = t.startswith("(") and t.endswith(")")
    t = re.sub(r"[\s,$€£¥₹%()]|^[A-Z]{3}|[A-Z]{3}$", "", t)
    if t.endswith("-"):
        neg, t = True, t[:-1]
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def excel_date(x):
    v = to_num(x)
    if v is None:
        return None
    return (date(1899, 12, 30) + timedelta(days=int(v))).isoformat()


# ---------------------------------------------------------------- engine
class Engine:
    def __init__(self, force=None):
        self.kind = None
        if force != "sqlite":
            try:
                import duckdb
                self.con = duckdb.connect()
                self.kind = "duckdb"
                self.con.execute("SET TimeZone='UTC'")
                self.con.create_function("to_num", to_num, ["VARCHAR"], "DOUBLE", null_handling="special")
                self.con.create_function("excel_date", excel_date, ["VARCHAR"], "VARCHAR", null_handling="special")
            except ImportError:
                if force == "duckdb":
                    raise
        if self.kind is None:
            import sqlite3
            self.con = sqlite3.connect(":memory:")
            self.kind = "sqlite"
            self.con.create_function("to_num", 1, to_num, deterministic=True)
            self.con.create_function("excel_date", 1, excel_date, deterministic=True)

    def load(self, name, df):
        df = df.astype(object).where(df.notna(), None)
        if self.kind == "duckdb":
            self.con.register(f"_{name}_df", df.astype("string") if len(df.columns) else df)
            self.con.execute(f'CREATE OR REPLACE TABLE "{name}" AS SELECT * FROM "_{name}_df"')
            self.con.unregister(f"_{name}_df")
        else:
            df.to_sql(name, self.con, index=False, if_exists="replace", dtype={c: "TEXT" for c in df.columns})

    def view(self, name, sql):
        self.con.execute(f'DROP VIEW IF EXISTS "{name}"')
        self.con.execute(f'CREATE VIEW "{name}" AS {sql}')

    def df(self, sql):
        if self.kind == "duckdb":
            return self.con.execute(sql).df()
        return pd.read_sql_query(sql, self.con)

    def count(self, rel):
        return int(self.df(f'SELECT count(*) AS n FROM "{rel}"')["n"].iloc[0])


def read_table(path, sheet=None, header_row=1):
    ext = os.path.splitext(path)[1].lower()
    h = int(header_row) - 1
    if ext in (".xlsx", ".xlsm", ".xls"):
        df = pd.read_excel(path, sheet_name=sheet if sheet is not None else 0, header=h, dtype=str)
    else:
        df = pd.read_csv(path, header=h, dtype=str, sep="\t" if ext in (".tsv", ".tab") else ",",
                         keep_default_na=True, encoding_errors="replace")
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all")
    return df


# ---------------------------------------------------------------- run
def run(spec, out, base_dir=".", engine=None):
    os.makedirs(out, exist_ok=True)
    eng = Engine(engine or spec.get("engine"))
    loaded = {}
    for name, t in spec["tables"].items():
        t = {"path": t} if isinstance(t, str) else t
        p = t["path"] if os.path.isabs(t["path"]) else os.path.join(base_dir, t["path"])
        df = read_table(p, t.get("sheet"), t.get("header_row", 1))
        eng.load(name, df)
        loaded[name] = {"path": t["path"], "rows": len(df), "columns": list(df.columns)}

    steps_out, problems, warnings = [], [], []
    counts = {n: v["rows"] for n, v in loaded.items()}
    for i, st in enumerate(spec["steps"]):
        kind = st.get("kind", "derive")
        if kind not in KINDS:
            raise SystemExit(f"step {st['name']}: unknown kind {kind}")
        eng.view(st["name"], st["sql"])
        after = eng.count(st["name"])
        counts[st["name"]] = after
        ref = st.get("base") or st.get("from")
        before = counts.get(ref) if ref else None
        rec = {"step": st["name"], "kind": kind, "from": ref, "rows_before": before, "rows_after": after,
               "delta": None if before is None else after - before, "note": st.get("note", ""), "sql": st["sql"].strip()}
        if kind == "join" and before is not None:
            if after > before and not st.get("allow_fanout"):
                rec["check"] = f"FAN-OUT: {after - before} extra rows after join"
                problems.append(f"step `{st['name']}`: join grew rows {before} -> {after}. A key on the right side is not unique; "
                                f"amounts are now double counted. Dedupe or aggregate the right side first.")
            elif after < before:
                rec["check"] = f"DROPPED {before - after} rows (inner join or unmatched keys)"
                warnings.append(f"step `{st['name']}`: join dropped {before - after} rows; unmatched keys are excluded from the answer.")
            else:
                rec["check"] = "ok: row count preserved"
        if kind == "clean" and before is not None and after != before:
            rec["check"] = f"removed {before - after} rows"
        if st.get("expect_rows") is not None and after != st["expect_rows"]:
            problems.append(f"step `{st['name']}`: expected {st['expect_rows']} rows, got {after}")
        for chk in st.get("assert_zero", []):
            n = int(eng.df(chk["sql"]).iloc[0, 0])
            rec.setdefault("asserts", []).append({"label": chk["label"], "value": n})
            if n:
                problems.append(f"step `{st['name']}`: {chk['label']} = {n} (expected 0)")
        steps_out.append(rec)

    final = spec["steps"][-1]["name"]
    result = eng.df(f'SELECT * FROM "{final}"')
    sample_from = spec.get("sample_from") or (spec["steps"][-2]["name"] if len(spec["steps"]) > 1 else final)
    rows_used = eng.df(f'SELECT * FROM "{sample_from}"')
    rows_used.to_csv(os.path.join(out, "rows_used.csv"), index=False)

    recon = []
    for r in spec.get("reconcile", []):
        got = float(eng.df(r["sql"]).iloc[0, 0])
        exp = r.get("expected")
        if isinstance(exp, str):  # expected may be SQL for a second, independent route to the same number
            exp = float(eng.df(exp).iloc[0, 0])
        ok = exp is None or abs(got - float(exp)) <= float(r.get("tolerance", 0.005))
        recon.append({"label": r["label"], "got": got, "expected": exp, "ok": ok})
        if not ok:
            problems.append(f"reconciliation failed: {r['label']}: got {got:,.2f}, expected {float(exp):,.2f}")

    query_sql = assemble(spec["steps"])
    with open(os.path.join(out, "query.sql"), "w") as f:
        f.write(f"-- {spec.get('question', '')}\n-- engine: {eng.kind}; every source column loaded as TEXT\n{MACROS}{query_sql}\n")
    summary = {"question": spec.get("question"), "engine": eng.kind, "tables": loaded, "steps": steps_out,
               "result": json.loads(result.to_json(orient="records")), "reconcile": recon,
               "problems": problems, "warnings": warnings, "sample_from": sample_from, "rows_used": len(rows_used)}
    with open(os.path.join(out, "steps.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)
    with open(os.path.join(out, "answer.md"), "w") as f:
        f.write(render(spec, summary, result, rows_used, query_sql))
    return summary


def assemble(steps):
    parts = [f'"{s["name"]}" AS (\n  ' + s["sql"].strip().replace("\n", "\n  ") + "\n)" for s in steps]
    return "WITH " + ",\n".join(parts) + f'\nSELECT * FROM "{steps[-1]["name"]}";'


def md_table(df, limit=None):
    if limit:
        df = df.head(limit)
    if df.empty:
        return "_(no rows)_"
    cols = list(df.columns)
    L = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False):
        L.append("| " + " | ".join(_fmt(v) for v in r) + " |")
    return "\n".join(L)


def _fmt(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    if isinstance(v, float):
        return f"{v:,.2f}"
    return str(v).replace("|", "\\|")


def render(spec, s, result, rows_used, query_sql):
    L = [f"# {spec.get('question', 'Answer')}", ""]
    if s["problems"]:
        L += ["**DO NOT QUOTE THIS NUMBER YET. Checks failed:**", ""] + [f"- {p}" for p in s["problems"]] + [""]
    if result.shape == (1, 1):
        v = result.iloc[0, 0]
        L += [f"**{spec.get('answer_label', result.columns[0])}: {_fmt(v)}**", ""]
    else:
        L += ["**Answer:**", "", md_table(result), ""]
    L += ["## Definition used", "", spec.get("definition", "_state the definition_"), ""]
    if spec.get("alternatives"):
        L += ["Other definitions that would change the answer:", ""] + [f"- {a}" for a in spec["alternatives"]] + [""]
    L += ["## Row counts at each step", "", "| step | kind | from | rows before | rows after | check | note |", "|---|---|---|---|---|---|---|"]
    for n, t in s["tables"].items():
        L.append(f"| {n} | source | `{t['path']}` | | {t['rows']} | | loaded as text |")
    for st in s["steps"]:
        L.append(f"| {st['step']} | {st['kind']} | {st['from'] or ''} | {'' if st['rows_before'] is None else st['rows_before']} | "
                 f"{st['rows_after']} | {st.get('check', '')} | {st['note']} |")
    L.append("")
    for st in s["steps"]:
        for a in st.get("asserts", []):
            L.append(f"- check `{st['step']}`: {a['label']} = {a['value']}")
    if s["reconcile"]:
        L += ["", "## Reconciliation", ""]
        for r in s["reconcile"]:
            exp = "" if r["expected"] is None else f" vs expected {float(r['expected']):,.2f}"
            L.append(f"- {'OK' if r['ok'] else 'MISMATCH'}: {r['label']}: {r['got']:,.2f}{exp}")
    if s["warnings"] or spec.get("caveats"):
        L += ["", "## Caveats", ""] + [f"- {w}" for w in s["warnings"] + spec.get("caveats", [])]
    L += ["", f"## Rows used (`{s['sample_from']}`, {s['rows_used']} rows; first 10 shown, all in rows_used.csv)", "",
          md_table(rows_used, 10), "", "## Query", "", f"Engine: {s['engine']}. Rerun: `query.sql`.", "", "```sql", query_sql, "```", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?", help="question spec JSON")
    ap.add_argument("--table", action="append", default=[], help="name=path[:sheet] for ad hoc mode")
    ap.add_argument("--sql", help="ad hoc single query (no step accounting; prefer a spec)")
    ap.add_argument("--out", default="sqa_out/answer")
    ap.add_argument("--engine", choices=["duckdb", "sqlite"])
    a = ap.parse_args(argv)
    if a.spec:
        with open(a.spec) as f:
            spec = json.load(f)
        base = os.path.dirname(os.path.abspath(a.spec))
    elif a.sql and a.table:
        tables = {}
        for t in a.table:
            n, p = t.split("=", 1)
            sheet = None
            if re.search(r"\.xls[xm]?:", p):
                p, sheet = p.rsplit(":", 1)
            tables[n] = {"path": p, "sheet": sheet}
        spec = {"question": a.sql, "tables": tables, "steps": [{"name": "answer", "kind": "aggregate", "sql": a.sql}]}
        base = os.getcwd()
    else:
        ap.error("give a spec file, or --table and --sql")
    s = run(spec, a.out, base, a.engine)
    print(open(os.path.join(a.out, "answer.md")).read().split("## Rows used")[0])
    return 1 if s["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
