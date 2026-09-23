#!/usr/bin/env python3
"""Prove an edit touched only the cells it was supposed to.

Compares a before and after copy of a CSV/XLSX table cell by cell (as text,
so "0012" vs "12" counts as a change) and lists every changed cell, added
row, removed row, and added/removed column. Exits 1 if anything changed
outside the allowed columns/rows, so an "update the invoice amount" edit
that also rewrote the bank account number fails loudly.

    python3 diff_edit.py before.csv after.csv --key invoice_id --allow amount
    python3 diff_edit.py before.xlsx after.xlsx --sheet Invoices --key line_id \
        --allow amount --rows INV-7,INV-9

Without --key, rows are matched by position (only safe when no rows were
inserted or deleted). Writes a markdown report to --report if given.
"""
import argparse
import os
import sys

import pandas as pd


def read(path, sheet=None):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm", ".xls"):
        df = pd.read_excel(path, sheet_name=sheet if sheet is not None else 0, dtype=str)
    else:
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
    return df.fillna("")


def diff(before, after, key=None, allow_cols=(), allow_rows=()):
    changes, violations = [], []
    cols_b, cols_a = list(before.columns), list(after.columns)
    for c in cols_b:
        if c not in cols_a:
            violations.append(f"column removed: {c}")
    for c in cols_a:
        if c not in cols_b:
            violations.append(f"column added: {c}")
    if key:
        for name, df in (("before", before), ("after", after)):
            if df[key].duplicated().any():
                raise SystemExit(f"--key {key} is not unique in the {name} file; pick a unique key")
        b, a = before.set_index(key), after.set_index(key)
    else:
        if len(before) != len(after):
            violations.append(f"row count changed {len(before)} -> {len(after)} and no --key given to match rows")
        b, a = before, after
    for k in b.index.difference(a.index):
        violations.append(f"row removed: {key or 'row'}={k}")
    for k in a.index.difference(b.index):
        violations.append(f"row added: {key or 'row'}={k}")
    shared_cols = [c for c in cols_b if c in cols_a and c != key]
    for k in b.index.intersection(a.index):
        for c in shared_cols:
            vb, va = b.at[k, c], a.at[k, c]
            if vb != va:
                ok = (c in allow_cols) and (not allow_rows or str(k) in allow_rows)
                changes.append({"row": k, "column": c, "before": vb, "after": va, "allowed": ok})
                if not ok:
                    violations.append(f"UNEXPECTED change {key or 'row'}={k} [{c}]: {vb!r} -> {va!r}")
    return changes, violations


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--key")
    ap.add_argument("--sheet")
    ap.add_argument("--allow", default="", help="comma-separated columns the edit may change")
    ap.add_argument("--rows", default="", help="comma-separated key values the edit may change (default: any row)")
    ap.add_argument("--report")
    a = ap.parse_args(argv)
    allow_cols = [x for x in a.allow.split(",") if x]
    allow_rows = [x for x in a.rows.split(",") if x]
    changes, violations = diff(read(a.before, a.sheet), read(a.after, a.sheet), a.key, allow_cols, allow_rows)
    L = [f"# Edit diff: {a.before} -> {a.after}", "",
         f"Allowed columns: {allow_cols or 'none'}; allowed rows: {allow_rows or 'any'}", "",
         f"{len(changes)} changed cells, {len(violations)} violations", "",
         "| row | column | before | after | allowed |", "|---|---|---|---|---|"]
    L += [f"| {c['row']} | {c['column']} | {c['before']} | {c['after']} | {'yes' if c['allowed'] else 'NO'} |" for c in changes]
    if violations:
        L += ["", "## Violations (revert these)", ""] + [f"- {v}" for v in violations]
    text = "\n".join(L) + "\n"
    if a.report:
        with open(a.report, "w") as f:
            f.write(text)
    print(text)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
