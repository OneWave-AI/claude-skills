#!/usr/bin/env bash
# Runs reconcile.py against the synthetic fixtures and three failure variants.
# Expected exits: 0 (balanced), 0 (inverted ledger signs auto-detected), 2 (unexplained variance), 3 (statement does not roll).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
R="python3 $HERE/../scripts/reconcile.py"
F="$HERE/fixtures"
T="$(mktemp -d)"
COMMON="--period-start 2026-08-01 --period-end 2026-08-31 --statement-begin 25000 --statement-end 19586.22"

echo "== 1. base case"; $R --bank "$F/bank_statement.csv" --ledger "$F/ledger.csv" $COMMON --book-begin 23800 --out "$T/1" >/dev/null; echo "exit=$? (want 0)"
grep -A3 "UNEXPLAINED" "$T/1/reconciliation.md" | head -1

echo "== 2. ledger exported with inverted signs"
python3 - "$F/ledger.csv" "$T/ledger_inv.csv" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1])))
for r in rows: r["Amount"] = f"{-float(r['Amount']):.2f}"
w = csv.DictWriter(open(sys.argv[2], "w", newline=""), fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
PY
$R --bank "$F/bank_statement.csv" --ledger "$T/ledger_inv.csv" $COMMON --book-begin -23800 --out "$T/2" >/dev/null; echo "exit=$? (want 0)"
grep -E "UNEXPLAINED|inverted" "$T/2/reconciliation.md"

echo "== 3. wrong book beginning balance (50.00 off)"
$R --bank "$F/bank_statement.csv" --ledger "$F/ledger.csv" $COMMON --book-begin 23850 --out "$T/3" >/dev/null; echo "exit=$? (want 2)"
grep "UNEXPLAINED" "$T/3/reconciliation.md"

echo "== 4. statement export missing a line"
grep -v "GOOGLE" "$F/bank_statement.csv" > "$T/bank_missing.csv"
$R --bank "$T/bank_missing.csv" --ledger "$F/ledger.csv" $COMMON --book-begin 23800 --out "$T/4"; echo "exit=$? (want 3)"
rm -rf "$T"
