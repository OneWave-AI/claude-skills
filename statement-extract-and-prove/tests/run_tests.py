#!/usr/bin/env python3
"""End-to-end test: generate fixtures, extract, prove, compare to truth, then corrupt and
confirm prove.py pinpoints each fault. Requires pdfplumber + reportlab (+ openpyxl for --xlsx).

Usage: python tests/run_tests.py WORKDIR
"""
import csv
import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
PY = sys.executable
work = Path(sys.argv[1] if len(sys.argv) > 1 else "stmt-test")
fx, out = work / "fixtures", work / "out"
out.mkdir(parents=True, exist_ok=True)
failures = []


def run(args, expect=None):
    p = subprocess.run([PY, *map(str, args)], capture_output=True, text=True)
    text = (p.stdout + p.stderr).strip()
    print(text)
    if expect is not None and p.returncode != expect:
        failures.append(f"{' '.join(map(str, args[:2]))}: exit {p.returncode}, expected {expect}")
    return p.returncode, text


def rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write(path, rs):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rs[0].keys()))
        w.writeheader()
        w.writerows(rs)


def banner(s):
    print(f"\n{'=' * 8} {s} {'=' * (70 - len(s))}")


banner("generate fixtures")
run([HERE / "make_fixtures.py", fx], expect=0)

for name in ("us_checking", "eu_giro", "uk_current"):
    banner(f"{name}: extract")
    run([SCRIPTS / "extract_statement.py", fx / f"{name}.pdf", "--out", out / name, "--xlsx"], expect=0)
    banner(f"{name}: prove")
    run([SCRIPTS / "prove.py", out / f"{name}.csv"], expect=0)
    got, truth = rows(out / f"{name}.csv"), rows(fx / f"{name}.truth.csv")
    mism = [(i, g, t) for i, (g, t) in enumerate(zip(got, truth))
            if (g["date"], g["description"], Decimal(g["amount"])) != (t["date"], t["description"], Decimal(t["amount"]))]
    print(f"truth comparison: {len(got)} extracted vs {len(truth)} printed, {len(mism)} field mismatches")
    for i, g, t in mism[:5]:
        print(f"  row {i + 1}: got {g['date']} {g['description']!r} {g['amount']} | truth {t['date']} {t['description']!r} {t['amount']}")
    if len(got) != len(truth) or mism:
        failures.append(f"{name}: truth mismatch")

# ---------------------------------------------------------------- corruptions
base = rows(out / "us_checking.csv")
meta = out / "us_checking.meta.json"


def corrupt(label, rs, must_contain):
    banner(f"corrupted: {label}")
    p = out / f"us_bad_{label}.csv"
    write(p, rs)
    code, text = run([SCRIPTS / "prove.py", p, "--meta", meta], expect=1)
    for s in must_contain:
        if s not in text:
            failures.append(f"{label}: expected '{s}' in prove output")


dropped = base[:22] + base[23:]
print(f"\n(dropping row 23: page {base[22]['page']} y={base[22]['y']} {base[22]['date']} "
      f"{base[22]['description']!r} amount {base[22]['amount']})")
corrupt("dropped_row", dropped, ["NOT PROVEN", "MISSING", f"delta {Decimal(base[22]['amount']):.2f}"])

flipped = [dict(r) for r in base]
flipped[9]["amount"] = str(-Decimal(flipped[9]["amount"]))
corrupt("flipped_sign", flipped, ["WRONG SIGN", "row 10 "])

decimal_bad = [dict(r) for r in base]
decimal_bad[30]["amount"] = str(Decimal(decimal_bad[30]["amount"]) * 100)
corrupt("decimal_misread", decimal_bad, ["power of ten", "row 31 "])

p1_last = max(i for i, r in enumerate(base) if r["page"] == "1")
dup = base[:p1_last + 1] + [dict(base[p1_last], page="2", y="60.0")] + base[p1_last + 1:]
corrupt("page_break_duplicate", dup, ["repeats", "EXTRA", "row 17 "])

# ---------------------------------------------------------------- misaligned page -> localize -> re-extract
banner("shifted page 2 amounts: extract with auto bands")
run([SCRIPTS / "extract_statement.py", fx / "us_checking_shifted.pdf", "--out", out / "shifted"], expect=0)
code, text = run([SCRIPTS / "prove.py", out / "shifted.csv"], expect=1)
if "NO AMOUNT" not in text or "page 2" not in text:
    failures.append("shifted: prove did not localize the no-amount rows on page 2")
banner("shifted: dump page 2 word positions to choose bands")
_, dump = run([SCRIPTS / "extract_statement.py", fx / "us_checking_shifted.pdf", "--out", out / "x", "--dump-words", "2"])
m = json.loads((out / "shifted.meta.json").read_text())
print("page 2 bands used:", m["bands"]["2"])
banner("shifted: re-extract page 2 only with adjusted bands")
bands = "date=40-95,description=95-285,amount=285-480,balance=480-570"
run([SCRIPTS / "extract_statement.py", fx / "us_checking_shifted.pdf", "--out", out / "shifted_fixed",
     "--bands", bands, "--band-pages", "2"], expect=0)
run([SCRIPTS / "prove.py", out / "shifted_fixed.csv"], expect=0)

# ---------------------------------------------------------------- wrong locale ties out at x100
banner("eu_giro forced to --decimal dot (every amount x100)")
run([SCRIPTS / "extract_statement.py", fx / "eu_giro.pdf", "--out", out / "eu_wrong_decimal", "--decimal", "dot"], expect=0)
code, text = run([SCRIPTS / "prove.py", out / "eu_wrong_decimal.csv"], expect=1)
if "[PASS] tie-out" not in text or "[FAIL] number format" not in text:
    failures.append("wrong decimal: expected tie-out PASS (scale-invariant) and number format FAIL")

# ---------------------------------------------------------------- no text layer
banner("scanned (image-only) PDF")
run([SCRIPTS / "extract_statement.py", fx / "scanned.pdf", "--out", out / "scanned"], expect=3)

banner("RESULT")
print("ALL TESTS PASSED" if not failures else "FAILURES:\n  " + "\n  ".join(failures))
sys.exit(1 if failures else 0)
