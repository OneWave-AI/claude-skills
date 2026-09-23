#!/usr/bin/env python3
"""Prove a statement extraction with arithmetic invariants. Reports, never repairs.

Checks (hard = must pass for PROVEN):
  1. tie-out (hard)          opening balance + sum(amounts) == closing balance, to the cent
  2. running balance (hard)  every printed balance == previous balance + amounts since; the
                             first broken row is pinpointed by page and y, with a diagnosis
  3. page continuity (hard)  brought-forward on page N+1 == carried-forward / last balance on N
  4. summary totals (hard)   credits and debits vs the statement's summary box and totals rows
  5. counts (hard)           row counts vs any count the statement states
  6. duplicates (hard)       rows repeated across a page break (same date, text, amount, balance)
  7. number format (hard)    no amount contradicts the decimal setting (a consistent x100 error ties out!)
  8. period (warn)           dates outside the statement period, order not monotonic
  9. leftovers (warn)        unassigned lines with an amount (possible dropped rows), fallback parses

Usage:
  python prove.py out/stmt.csv [--meta out/stmt.meta.json] [--opening 4210.33] [--closing 7790.57]
                  [--stated-count 32] [--report-dir out/proof]
Writes proof_report.md, proof.json and low_confidence.csv. Exit 0 = PROVEN, 1 = NOT PROVEN.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_statement import is_money, parse_amount  # noqa: E402

D0 = Decimal("0")


def dec(s):
    return Decimal(s) if s not in (None, "", "None") else None


def load(csv_path):
    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    for i, r in enumerate(rows):
        r["_i"] = i
        r["_amt"] = dec(r.get("amount"))
        r["_bal"] = dec(r.get("balance"))
    return rows


def where(r):
    return f"row {r['_i'] + 1} (page {r['page']}, y={r['y']}, {r['date'] or r.get('date_raw', '')}, " \
           f"\"{r['description'][:48]}\", amount {r['amount'] or '?'}, balance {r['balance'] or '-'})"


def pick(summary, markers, key, kind, first=True):
    if key in summary:
        return dec(summary[key]["value"]), f"summary box, page {summary[key]['page']}: \"{summary[key]['text']}\""
    ms = [m for m in markers if m["kind"] == kind]
    if ms:
        m = ms[0] if first else ms[-1]
        return dec(m["value"]), f"{kind} line, page {m['page']} y={m['y']}"
    return None, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--meta")
    ap.add_argument("--opening", help="opening balance read from the statement (overrides detection)")
    ap.add_argument("--closing", help="closing balance read from the statement (overrides detection)")
    ap.add_argument("--stated-count", type=int, help="transaction count printed on the statement")
    ap.add_argument("--report-dir")
    a = ap.parse_args()

    csv_path = Path(a.csv)
    meta_path = Path(a.meta) if a.meta else csv_path.with_suffix("").with_suffix(".meta.json")
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    summary, markers = meta.get("summary", {}), meta.get("markers", [])
    acct = meta.get("account_type", "bank")
    decimal = (meta.get("decimal") or {}).get("used", "dot")
    rows = load(csv_path)
    report_dir = Path(a.report_dir) if a.report_dir else csv_path.parent / (csv_path.stem + "_proof")
    report_dir.mkdir(parents=True, exist_ok=True)

    checks, low = [], {}

    def check(name, ok, detail, hard=True):
        checks.append({"check": name, "status": "PASS" if ok else ("FAIL" if hard else "WARN"),
                       "hard": hard, "detail": detail})

    def flag(r, reason):
        low.setdefault(r["_i"], set()).add(reason)

    for r in rows:
        if "source=visual" in r.get("flags", ""):
            flag(r, "value read from the page image, not the text layer")
        if r.get("low_confidence"):
            flag(r, "parsed with fallback: " + r["flags"])
        if r["_amt"] is None:
            flag(r, "no amount")

    # newest-first statements: walk the chain in date order
    dated = [r["date"] for r in rows if r["date"]]
    descending = len(dated) > 2 and sum(b < a_ for a_, b in zip(dated, dated[1:])) > len(dated) / 2
    chain = list(reversed(rows)) if descending else rows

    # ---- opening / closing
    opening, o_src = (dec(a.opening), "--opening") if a.opening else pick(summary, markers, "opening_balance", "brought_forward")
    closing, c_src = (dec(a.closing), "--closing") if a.closing else pick(summary, markers, "closing_balance", "closing", first=False)
    derived = []
    if closing is None:
        last_bal = next((r for r in reversed(chain) if r["_bal"] is not None), None)
        if last_bal:
            closing, c_src = last_bal["_bal"], f"last printed running balance ({where(last_bal)})"
    if opening is None:
        first = next((r for r in chain if r["_bal"] is not None and r["_amt"] is not None), None)
        if first and first is chain[0]:
            opening, o_src = first["_bal"] - first["_amt"], "DERIVED from first row (balance - amount); not independent"
            derived.append("opening")

    total = sum((r["_amt"] for r in rows if r["_amt"] is not None), D0)
    inc = sum((r["_amt"] for r in rows if r["_amt"] is not None and r["_amt"] > 0), D0)
    out = -sum((r["_amt"] for r in rows if r["_amt"] is not None and r["_amt"] < 0), D0)

    if not rows:
        check("rows extracted", False, "0 rows extracted: header not found or bands wrong; see meta warnings")
    if opening is None or closing is None:
        check("tie-out", False, f"cannot prove: opening={opening} closing={closing}. Read them off the statement "
                                f"and pass --opening/--closing.")
        tie_diff = None
    else:
        tie_diff = opening + total - closing
        check("tie-out", tie_diff == 0,
              f"opening {opening} + sum {total} = {opening + total}; closing {closing}; difference {tie_diff}. "
              f"[opening from {o_src}; closing from {c_src}]")

    # ---- running balance chain
    breaks = []
    has_bal = any(r["_bal"] is not None for r in rows)
    if has_bal and opening is not None:
        prev, pending, prev_row, segment = opening, D0, None, []
        for r in chain:
            pending += r["_amt"] or D0
            segment.append(r)
            if r["_bal"] is None:
                continue
            expected = prev + pending
            if r["_bal"] != expected:
                breaks.append({"row": r, "prev_row": prev_row, "expected": expected, "printed": r["_bal"],
                               "delta": r["_bal"] - expected, "segment": segment})
            prev, pending, prev_row, segment = r["_bal"], D0, r, []
        diagnose(breaks, meta, decimal, acct)
        for b in breaks:
            flag(b.get("culprit") or b["row"], "running balance break: " + b["hint"])
        if breaks:
            b = breaks[0]
            detail = (f"{len(breaks)} break(s). FIRST BROKEN BALANCE: {where(b['row'])}. Expected balance {b['expected']} "
                      f"(previous {b['prev_row']['balance'] if b['prev_row'] else 'opening ' + str(opening)} + amounts), "
                      f"printed {b['printed']}, delta {b['delta']}. Diagnosis: {b['hint']}")
        else:
            detail = f"all {sum(1 for r in rows if r['_bal'] is not None)} printed balances chain from opening {opening}"
        check("running balance", not breaks, detail)
    elif not has_bal:
        check("running balance", True, "no running-balance column on this statement; tie-out and totals carry the proof",
              hard=False)

    # ---- page continuity and per-page sums
    pages = sorted({int(r["page"]) for r in rows})
    last_bal_by_page = {}
    for r in chain:
        if r["_bal"] is not None:
            last_bal_by_page[int(r["page"])] = r["_bal"]
    page_notes, page_ok = [], True
    for m in markers:
        p = m["page"]
        if m["kind"] == "brought_forward" and p > min(pages or [p]):
            prior_cf = next((x for x in markers if x["kind"] == "carried_forward" and x["page"] == p - 1), None)
            ref = dec(prior_cf["value"]) if prior_cf else last_bal_by_page.get(p - 1)
            if ref is not None:
                ok = dec(m["value"]) == ref
                page_ok &= ok
                page_notes.append(f"page {p} brought forward {m['value']} vs page {p - 1} end {ref}: {'ok' if ok else 'MISMATCH'}")
        if m["kind"] == "carried_forward" and p in last_bal_by_page:
            ok = dec(m["value"]) == last_bal_by_page[p]
            page_ok &= ok
            page_notes.append(f"page {p} carried forward {m['value']} vs last balance {last_bal_by_page[p]}: {'ok' if ok else 'MISMATCH'}")
    per_page = []
    bf = {m["page"]: dec(m["value"]) for m in markers if m["kind"] == "brought_forward"}
    ends = {m["page"]: dec(m["value"]) for m in markers if m["kind"] in ("carried_forward", "closing")}
    for p in pages:
        s = sum((r["_amt"] for r in rows if int(r["page"]) == p and r["_amt"] is not None), D0)
        n = sum(1 for r in rows if int(r["page"]) == p)
        start = bf.get(p, opening if p == pages[0] else None)
        end = ends.get(p, last_bal_by_page.get(p))
        diff = (start + s - end) if (start is not None and end is not None) else None
        per_page.append({"page": p, "rows": n, "sum": str(s), "start": str(start), "end": str(end),
                         "difference": str(diff) if diff is not None else "n/a"})
        if diff not in (None, D0):
            page_ok = False
            page_notes.append(f"page {p}: start {start} + rows {s} = {start + s} but page ends at {end} "
                              f"(off by {-diff}) - the fault is on this page")
    if page_notes or len(pages) > 1:
        check("page continuity", page_ok, "; ".join(page_notes) or "per-page start + sum = end on every page")

    # ---- summary totals
    lbl_in, lbl_out = ("total_credits", "total_debits") if acct == "bank" else ("total_debits", "total_credits")
    tot_detail, tot_ok, any_tot = [], True, False
    for key, got in ((lbl_in, inc), (lbl_out, out)):
        if key in summary:
            any_tot = True
            want = abs(dec(summary[key]["value"]))
            ok = want == got
            tot_ok &= ok
            tot_detail.append(f"{key} stated {want} vs extracted {got}: {'ok' if ok else 'MISMATCH by ' + str(got - want)}")
    for t in meta.get("totals_rows", []):
        for role in ("debit", "credit"):
            if role in t["values"] and t["values"][role] not in (None, "None"):
                any_tot = True
                col = sum((abs(dec(r[role])) for r in rows if r.get(role) and int(r["page"]) <= t["page"]), D0)
                want = abs(dec(t["values"][role]))
                ok = col == want
                tot_ok &= ok
                tot_detail.append(f"{role} column total row (page {t['page']}) {want} vs extracted {col}: "
                                  f"{'ok' if ok else 'MISMATCH by ' + str(col - want)}")
    if any_tot:
        check("summary totals", tot_ok, "; ".join(tot_detail))

    # ---- counts
    cnt_detail, cnt_ok, any_cnt = [], True, False
    stated = a.stated_count or (summary.get("transaction_count") or {}).get("value")
    if stated:
        any_cnt = True
        ok = int(stated) == len(rows)
        cnt_ok &= ok
        cnt_detail.append(f"stated {stated} transactions vs {len(rows)} rows")
    for key, n in ((lbl_in, sum(1 for r in rows if r["_amt"] and r["_amt"] > 0)),
                   (lbl_out, sum(1 for r in rows if r["_amt"] and r["_amt"] < 0))):
        if key in summary and "count" in summary[key]:
            any_cnt = True
            ok = summary[key]["count"] == n
            cnt_ok &= ok
            cnt_detail.append(f"{key} count stated {summary[key]['count']} vs {n} rows: {'ok' if ok else 'MISMATCH'}")
    if any_cnt:
        check("counts", cnt_ok, "; ".join(cnt_detail))

    # ---- duplicates
    dups = []
    seen = {}
    for r in rows:
        key = (r["date"], r["description"], r["amount"], r["balance"])
        if r["balance"] and key in seen:
            dups.append((seen[key], r))
        seen.setdefault(key, r)
    for p in pages[:-1]:
        last = [r for r in rows if int(r["page"]) == p][-1:]
        first = [r for r in rows if int(r["page"]) == p + 1][:1]
        if last and first and (last[0]["date"], last[0]["description"], last[0]["amount"]) == \
                (first[0]["date"], first[0]["description"], first[0]["amount"]) and (last[0], first[0]) not in dups:
            dups.append((last[0], first[0]))
    for x, y in dups:
        flag(y, f"possible duplicate of row {x['_i'] + 1}")
    check("duplicates", not dups, "; ".join(f"{where(y)} repeats {where(x)}" for x, y in dups) or "none found")

    # ---- period and order (warn)
    per = meta.get("period")
    warn = []
    if per:
        outside = [r for r in rows if r["date"] and not (per[0] <= r["date"] <= per[1])]
        for r in outside:
            flag(r, f"date outside statement period {per[0]}..{per[1]}")
        if outside:
            warn.append(f"{len(outside)} row(s) dated outside {per[0]}..{per[1]}")
    unsorted = sum(1 for x, y in zip(chain, chain[1:]) if x["date"] and y["date"] and y["date"] < x["date"])
    if unsorted:
        warn.append(f"{unsorted} place(s) where dates go backwards in {'reversed ' if descending else ''}order")
    ok_msg = f"all dates inside {per[0]}..{per[1]}, in order" if per else "no statement period found; order checked only"
    check("period and order", not warn, "; ".join(warn) or ok_msg, hard=False)

    # ---- number format. Invariants are scale-invariant: a document-wide separator mistake
    # (every amount x100) still ties out, so format conflicts are a hard failure of their own.
    fmt_bad = [r for r in rows if any(f in r.get("flags", "") for f in ("locale_conflict", "bad_grouping"))]
    check("number format", not fmt_bad,
          f"{len(fmt_bad)} row(s) contradict the decimal setting '{decimal}' (first: {where(fmt_bad[0])}, printed "
          f"{fmt_bad[0]['raw_amount']!r}). A consistent separator error ties out at the wrong scale; re-extract with "
          f"the other --decimal" if fmt_bad else f"every amount parses cleanly as decimal '{decimal}'")
    other_low = [r for r in rows if r.get("low_confidence") and r not in fmt_bad]
    check("fallback parses", not other_low,
          f"{len(other_low)} row(s) parsed with a fallback; they tie out but read each one against the page"
          if other_low else "none", hard=False)

    # ---- leftovers
    money_lines = [u for u in meta.get("unassigned_lines", []) if any(is_money(t) for t in u["text"].split())]
    check("unassigned lines", not money_lines,
          "; ".join(f"page {u['page']} y={u['y']}: \"{u['text'][:70]}\" ({u['why']})" for u in money_lines)
          or f"{len(meta.get('unassigned_lines', []))} unassigned line(s), none containing an amount", hard=False)

    # ---- verdict
    hard_fail = [c for c in checks if c["hard"] and c["status"] == "FAIL"]
    proven = not hard_fail and not derived
    verdict = "PROVEN" if proven else "NOT PROVEN"
    if not hard_fail and derived:
        verdict += " (opening balance not printed on the statement; derived value only - confirm it)"
    if tie_diff not in (None, D0) and breaks and len(breaks) == 1 and breaks[0]["delta"] == -tie_diff:
        b0 = breaks[0]
        localized = (f"LOCALIZED: the whole tie-out gap ({-tie_diff}) is explained by one break, "
                     + (f"culprit {where(b0['culprit'])}." if b0.get("culprit")
                        else f"just before {where(b0['row'])}."))
    else:
        localized = ""

    # ---- write
    with open(report_dir / "low_confidence.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["row", "page", "y", "date", "description", "amount", "balance", "reasons"])
        for i in sorted(low):
            r = rows[i]
            w.writerow([i + 1, r["page"], r["y"], r["date"], r["description"], r["amount"], r["balance"],
                        " | ".join(sorted(low[i]))])
    result = {"verdict": verdict, "rows": len(rows), "sum": str(total), "credits": str(inc), "debits": str(out),
              "opening": str(opening), "closing": str(closing), "checks": checks, "per_page": per_page,
              "breaks": [{"row": b["row"]["_i"] + 1, "page": b["row"]["page"], "y": b["row"]["y"],
                          "expected": str(b["expected"]), "printed": str(b["printed"]), "delta": str(b["delta"]),
                          "culprit_row": b["culprit"]["_i"] + 1 if b.get("culprit") else None,
                          "hint": b["hint"]} for b in breaks],
              "low_confidence_rows": len(low), "localized": localized}
    (report_dir / "proof.json").write_text(json.dumps(result, indent=2))
    md = [f"# Statement proof: {verdict}", "", f"Source: `{meta.get('file', csv_path)}`  ",
          f"Rows: {len(rows)} | layout: {meta.get('layout')} | decimal: {decimal} | account type: {acct}  ",
          f"Opening {opening} + credits {inc} - debits {out} = {opening + total if opening is not None else 'n/a'}; "
          f"closing {closing}", ""]
    if localized:
        md += [f"**{localized}**", ""]
    md += ["| Check | Status | Detail |", "|---|---|---|"]
    md += [f"| {c['check']} | {c['status']} | {c['detail'].replace('|', '/')} |" for c in checks]
    md += ["", "## Per page", "", "| Page | Rows | Start | Sum | End | Difference |", "|---|---|---|---|---|---|"]
    md += [f"| {p['page']} | {p['rows']} | {p['start']} | {p['sum']} | {p['end']} | {p['difference']} |" for p in per_page]
    if breaks:
        md += ["", "## Running-balance breaks", ""]
        md += [f"- {where(b['row'])}: expected {b['expected']}, printed {b['printed']}, delta {b['delta']}. {b['hint']}"
               for b in breaks]
    md += ["", f"## Low-confidence queue: {len(low)} row(s) in `low_confidence.csv`", "",
           "Nothing here was corrected. Re-extract the page (adjusted --bands) or read the page image, "
           "then re-run prove.py. Do not edit amounts to force a tie."]
    (report_dir / "proof_report.md").write_text("\n".join(md) + "\n")

    print(f"{verdict}: {len(rows)} rows, opening {opening} + sum {total} vs closing {closing}")
    for c in checks:
        print(f"  [{c['status']}] {c['check']}: {c['detail']}")
    if localized:
        print("  " + localized)
    print(f"  low-confidence queue: {len(low)} row(s) -> {report_dir / 'low_confidence.csv'}")
    print(f"  report: {report_dir / 'proof_report.md'}")
    sys.exit(0 if proven else 1)


def diagnose(breaks, meta, decimal, acct):
    """Attach a plain-language hint (and a culprit row when one is identifiable) to each break.
    Hints describe; they never change data."""
    unassigned = []
    for u in meta.get("unassigned_lines", []):
        for t in u["text"].split():
            if is_money(t):
                v, _ = parse_amount(t, decimal, acct)
                if v is not None:
                    unassigned.append((abs(v), u))
    powers = (Decimal(100), Decimal("0.01"), Decimal(1000), Decimal("0.001"), Decimal(10), Decimal("0.1"))
    for i, b in enumerate(breaks):
        d, seg = b["delta"], b["segment"]
        nxt = breaks[i + 1] if i + 1 < len(breaks) else None
        prv = breaks[i - 1] if i > 0 else None
        span = (f"between {where(b['prev_row'])} and {where(b['row'])}" if b["prev_row"]
                else f"between the opening balance and {where(b['row'])}")
        no_amt = [r for r in seg if r["_amt"] is None]
        flip = [r for r in seg if r["_amt"] and d == -2 * r["_amt"]]
        p10 = [r for r in seg if r["_amt"] and any(r["_amt"] + d == r["_amt"] * k for k in powers)]
        extra = [r for r in seg if r["_amt"] and d == -r["_amt"]]
        hit = next((u for v, u in unassigned if v == abs(d)), None)
        if nxt and nxt["delta"] == -d and nxt["prev_row"] is b["row"]:
            b["hint"] = (f"the printed BALANCE on this row looks misread by {d} (the next balance breaks by the "
                         f"opposite amount); amounts are consistent")
        elif prv and prv["delta"] == -d and prv["row"] is b["prev_row"]:
            b["hint"] = "follows from the misread balance on the previous row"
        elif no_amt:
            r = b["culprit"] = no_amt[0]
            b["hint"] = (f"{where(r)} has NO AMOUNT; its text is \"{r['description'][-40:]}\". If a number sits in the "
                         f"description, the column bands are wrong on page {r['page']}: re-extract that page with --bands")
        elif len(flip) == 1:
            r = b["culprit"] = flip[0]
            b["hint"] = f"{where(r)} has the WRONG SIGN (printed {r['raw_amount']!r}, parsed {r['amount']})"
        elif len(p10) == 1:
            r = b["culprit"] = p10[0]
            b["hint"] = (f"{where(r)} is off by a power of ten (printed {r['raw_amount']!r}, parsed {r['amount']}): "
                         f"decimal or thousands separator misread")
        elif len(extra) == 1:
            r = b["culprit"] = extra[0]
            b["hint"] = (f"{where(r)} looks EXTRA: removing it closes the gap exactly (a duplicate, or a "
                         f"subtotal/forward line read as a transaction)")
        elif hit:
            b["hint"] = (f"a row of {d} is MISSING {span}; the unassigned line at page {hit['page']} "
                         f"y={hit['y']} (\"{hit['text'][:60]}\") carries that amount - it is the dropped row")
        else:
            cands = ", ".join(f"row {r['_i'] + 1}" for r in flip + p10 + extra) or "none"
            b["hint"] = (f"the balance moved by {d} more than the extracted amounts explain: a row of {d} is "
                         f"probably MISSING {span} (look at the PDF between those y-positions), or an amount "
                         f"in that span is misread by {d}. Single-row explanations checked: {cands}")


if __name__ == "__main__":
    main()
