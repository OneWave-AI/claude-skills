#!/usr/bin/env python3
"""Rebuild fixtures, profile them, answer 4 questions, and check every number
against values computed by hand. Also checks the naive join is caught and that
diff_edit.py catches an edit that touched a column it should not have.

    python3 tests/run_tests.py [--out DIR]

Needs pandas + openpyxl. The ask.py questions need duckdb (pip install duckdb);
without it they are reported as SKIPPED, not passed.
"""
import argparse
import csv
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

import build_fixtures  # noqa: E402
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("sqa_profile", os.path.join(SCRIPTS, "profile.py"))
prof = importlib.util.module_from_spec(_spec)  # loaded by path: "profile" is also a stdlib module name
_spec.loader.exec_module(prof)
import ask  # noqa: E402
import diff_edit  # noqa: E402

# Hand-computed from the fixture rows in build_fixtures.py (FX: EUR 1.10, GBP 1.25).
# Paid Q3 (UTC) orders in USD: 1200 + 300 + 1100 + 500 + 2000 + 150 + 550 + 350 + 800 + 250 + 770 + 450 + 600 = 9020
# Refunds on those orders: R01 200 + R02 100 EUR = 110 + R03 450 (issued Oct 2) = 760
EXPECTED = {
    "q1_net_revenue": 8260.00,                      # 9020 - 760
    "q2_august_ny": 1950.00,                        # NY-August paid: O1008 550 + O1009 350 + O1011 800 + O1012 250
    "q3_segment_revenue": {"Enterprise": 5820.00,   # C003 1100+550+770 + C005 2000+800+600
                           "SMB": 3200.00},         # C001 1200+350+450 + C002 300+150+250 + C004 500
    "q4_top_customers": [("C005", 3400.00), ("C003", 2310.00), ("C001", 1350.00)],  # C003 2420-110, C001 2000-650
}
WRONG = {  # what the traps produce if not handled
    "sum of amount column incl. Grand Total row, currencies mixed": 19400.00,
    "Q3 by UTC-day in August instead of New York": 1850.00,
    "segment totals after the fan-out join": 11440.00,
}

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))


def test_profile(fx_dir, out):
    paths = [os.path.join(fx_dir, f) for f in ("orders.csv", "customers.csv", "refunds.csv", "fx_rates.csv", "pipeline.xlsx")]
    r = prof.build(paths, os.path.join(out, "profile"))
    t = r["tables"]
    o = t["orders"]
    check("profile: Grand Total row found in orders (source line 18)", [x["row"] for x in o["total_rows"]] == [18],
          "; ".join(o["total_rows"][0]["why"]) if o["total_rows"] else "none")
    check("profile: amount stats exclude the total row (max 2000, not 9700)",
          next(c for c in o["columns"] if c["column"] == "amount")["max"] == 2000.0)
    check("profile: text-stored numbers flagged on orders.amount",
          any("stored as text" in f for f in o["column_flags"].get("amount", [])))
    check("profile: 3 currencies flagged on orders.currency",
          any("3 currencies" in f for f in o["column_flags"].get("currency", [])))
    check("profile: UTC timestamps flagged on orders.created_at",
          any("UTC" in f for f in o["column_flags"].get("created_at", [])))
    check("profile: order_id is the orders grain", ["order_id"] in o["grain"]["candidate_keys"][:1])
    dk = t["customers"]["grain"]["duplicate_keys"]
    check("profile: duplicate customer_id C003 found", dk and dk[0]["column"] == "customer_id" and "C003" in dk[0]["examples"])
    jr = [j for j in r["join_risks"] if j["column"] == "customer_id"]
    check("profile: orders->customers join fan-out predicted as +3 rows", jr and jr[0].get("fanout_rows") == 3,
          jr[0]["verdict"][:90] if jr else "")
    check("profile: fx_rates lookup table not flagged as mixed currency",
          not any("currencies" in f for f in t["fx_rates"]["column_flags"].get("currency", [])))
    p = t["pipeline"]
    check("profile: xlsx header row detected on row 3", p["header_row"] == 3)
    check("profile: xlsx Total row found (row 9)", [x["row"] for x in p["total_rows"]] == [9])
    check("profile: xlsx hidden row 6 and autofilter reported", p["xlsx"]["hidden_rows"] == [6] and p["xlsx"]["autofilter"])
    check("profile: Excel serial dates detected in close_date",
          any("serial" in f for f in p["column_flags"].get("close_date", [])))
    dd = open(os.path.join(out, "profile", "data_dictionary.md")).read()
    check("profile: data_dictionary.md has open questions for totals, dup keys, currency, timezone",
          all(s in dd for s in ("look like totals", "Which row wins", "which FX rates", "business's local zone")))


def test_questions(out):
    try:
        import duckdb  # noqa: F401
    except ImportError:
        print("SKIP  ask.py questions: duckdb not installed (pip install duckdb)")
        results.append(("ask.py questions", None, "skipped"))
        return
    qdir = os.path.join(HERE, "questions")

    def run(name):
        with open(os.path.join(qdir, name + ".json")) as f:
            spec = json.load(f)
        return ask.run(spec, os.path.join(out, name), qdir)

    s = run("q1_net_revenue")
    got = s["result"][0]["net_revenue_usd"]
    check("Q1 net revenue Q3 = 8,260.00", abs(got - EXPECTED["q1_net_revenue"]) < 0.005 and not s["problems"], f"got {got:,.2f}")
    check("Q1 reconciles to the export's own Grand Total (9,700 native)", all(r["ok"] for r in s["reconcile"]))
    check("Q1 step table shows the Grand Total row removed (17 -> 16)",
          s["steps"][0]["rows_before"] == 17 and s["steps"][0]["rows_after"] == 16)

    s = run("q2_august_ny")
    got = s["result"][0]["gross_usd"]
    check("Q2 August (New York) gross = 1,950.00", abs(got - EXPECTED["q2_august_ny"]) < 0.005, f"got {got:,.2f}; UTC-day answer would be 1,850.00")

    s = run("q3_segment_revenue")
    got = {r["segment"]: r["gross_usd"] for r in s["result"]}
    check("Q3 segment revenue = Enterprise 5,820 / SMB 3,200", got == EXPECTED["q3_segment_revenue"] and not s["problems"], str(got))

    s = run("q3_naive_fanout")
    fan = [st for st in s["steps"] if st["kind"] == "join" and "FAN-OUT" in st.get("check", "")]
    tot = sum(r["gross_usd"] for r in s["result"])
    check("Q3 naive join: fan-out detected (13 -> 16 rows) and run marked failed",
          fan and fan[0]["rows_before"] == 13 and fan[0]["rows_after"] == 16 and s["problems"], f"inflated total {tot:,.2f}")
    check("Q3 naive join: reconciliation catches 11,440 vs 9,020",
          any(not r["ok"] and abs(r["got"] - WRONG["segment totals after the fan-out join"]) < 0.005 for r in s["reconcile"]))
    md = open(os.path.join(out, "q3_naive_fanout", "answer.md")).read()
    check("Q3 naive answer.md opens with DO NOT QUOTE", "DO NOT QUOTE" in md.split("\n", 3)[2])

    s = run("q4_top_customers")
    got = [(r["customer_id"], r["net_usd"]) for r in s["result"]]
    check("Q4 top 3 customers by net = C005 3,400 / C003 2,310 / C001 1,350", got == EXPECTED["q4_top_customers"], str(got))
    check("Q4 uses the current name for the duplicated customer", s["result"][1]["name"] == "Cobalt Logistics GmbH")
    for f in ("answer.md", "query.sql", "steps.json", "rows_used.csv"):
        check(f"Q4 wrote {f}", os.path.exists(os.path.join(out, "q4_top_customers", f)))


def test_sqlite_fallback(fx_dir, out):
    spec = {"question": "paid orders, all time, excluding the total row", "engine": "sqlite",
            "tables": {"orders": os.path.join(fx_dir, "orders.csv")},
            "steps": [{"name": "answer", "kind": "aggregate",
                       "sql": "SELECT count(*) AS n, round(sum(to_num(amount)), 2) AS native_sum FROM orders "
                              "WHERE order_id IS NOT NULL AND status = 'paid'"}]}
    s = ask.run(spec, os.path.join(out, "sqlite"), HERE)
    r = s["result"][0]
    check("sqlite fallback + to_num(): 15 paid orders, native sum 9,500", s["engine"] == "sqlite" and r["n"] == 15 and r["native_sum"] == 9500.0, str(r))
    check("excel_date(46204) = 2026-07-01 and to_num('(35.00)') = -35",
          ask.excel_date("46204") == "2026-07-01" and ask.to_num("(35.00)") == -35.0)


def test_edit_safety(out):
    d = os.path.join(out, "edit")
    os.makedirs(d, exist_ok=True)
    rows = [("line_id", "description", "amount", "bank_account"),
            ("L1", "Consulting", "1200.00", "021000021-000123456789"),
            ("L2", "Travel", "340.00", "021000021-000123456789")]
    good = [list(r) for r in rows]
    good[2][2] = "360.00"
    bad = [list(r) for r in good]
    bad[1][3] = "021000021-000123456780"  # the HN failure mode: an edit to one line changed the account number
    for name, data in (("before", rows), ("good", good), ("bad", bad)):
        with open(os.path.join(d, f"{name}.csv"), "w", newline="") as f:
            csv.writer(f).writerows(data)
    rc_good = diff_edit.main([os.path.join(d, "before.csv"), os.path.join(d, "good.csv"), "--key", "line_id",
                              "--allow", "amount", "--rows", "L2", "--report", os.path.join(d, "good.md")])
    rc_bad = diff_edit.main([os.path.join(d, "before.csv"), os.path.join(d, "bad.csv"), "--key", "line_id",
                             "--allow", "amount", "--rows", "L2", "--report", os.path.join(d, "bad.md")])
    check("diff_edit: targeted amount edit on L2 passes", rc_good == 0)
    check("diff_edit: collateral bank_account change on L1 fails", rc_bad == 1 and "bank_account" in open(os.path.join(d, "bad.md")).read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or tempfile.mkdtemp(prefix="sqa-tests-")
    fx_dir = build_fixtures.build(os.path.join(HERE, "fixtures"))
    print(f"fixtures: {fx_dir}\noutputs:  {out}\n")
    test_profile(fx_dir, out)
    test_questions(out)
    test_sqlite_fallback(fx_dir, out)
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        test_edit_safety(out)
    for n, ok, d in results[-2:]:
        print(f"{'PASS' if ok else 'FAIL'}  {n}")
    print("\nWrong answers the traps would have produced:")
    for k, v in WRONG.items():
        print(f"  {v:>10,.2f}  {k}")
    failed = [r for r in results if r[1] is False]
    skipped = [r for r in results if r[1] is None]
    print(f"\n{len(results) - len(failed) - len(skipped)} passed, {len(failed)} failed, {len(skipped)} skipped")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
