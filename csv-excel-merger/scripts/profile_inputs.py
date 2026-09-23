#!/usr/bin/env python3
"""Profile CSV/TSV/Excel files before a merge.

Prints, per file (and per sheet for Excel): encoding, delimiter, row and
column counts, headers, and columns that look like unique keys. Then prints
the header overlap across all inputs so the column mapping can be planned.

Usage:
    python scripts/profile_inputs.py file1.csv file2.xlsx data/*.tsv

Requires: pandas (>=2.2; tested on 3.0), openpyxl for .xlsx.
Reads everything as text so IDs, ZIP codes, and phone numbers keep their
leading zeros; nothing is modified on disk.
"""
import csv
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

# Encodings tried in order. utf-8-sig strips the BOM Excel adds to CSV exports;
# cp1252 covers most legacy Windows exports; latin-1 never fails, so it is last.
ENCODINGS = ("utf-8-sig", "cp1252", "latin-1")
SAMPLE_BYTES = 64 * 1024  # enough to sniff a delimiter without reading big files


def detect_encoding(path: Path) -> str:
    raw = path.read_bytes()[:SAMPLE_BYTES]
    for enc in ENCODINGS:
        try:
            raw.decode(enc)
            return enc
        except UnicodeDecodeError:
            continue
    return "latin-1"


def detect_delimiter(path: Path, encoding: str) -> str:
    sample = path.read_bytes()[:SAMPLE_BYTES].decode(encoding, errors="replace")
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        return "\t" if path.suffix.lower() == ".tsv" else ","


def load(path: Path) -> dict[str, tuple[pd.DataFrame, str]]:
    """Return {label: (frame, note)}; one entry per sheet for Excel files."""
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xlsm", ".xls"):
        sheets = pd.read_excel(path, sheet_name=None, dtype=str)
        return {f"{path.name}[{name}]": (df, "excel") for name, df in sheets.items()}
    enc = detect_encoding(path)
    sep = detect_delimiter(path, enc)
    df = pd.read_csv(path, dtype=str, encoding=enc, sep=sep, keep_default_na=False)
    return {path.name: (df, f"encoding={enc} delimiter={sep!r}")}


def candidate_keys(df: pd.DataFrame) -> list[str]:
    keys = []
    for col in df.columns:
        values = df[col].astype(str).str.strip().str.lower()
        values = values[values != ""]
        if len(values) and values.is_unique and len(values) >= 0.95 * len(df):
            keys.append(col)
    return keys


def main(paths: list[str]) -> int:
    if not paths:
        print(__doc__)
        return 1
    header_counts: Counter[str] = Counter()
    total_inputs = 0
    for p in map(Path, paths):
        if not p.exists():
            print(f"!! {p}: not found")
            continue
        try:
            frames = load(p)
        except Exception as exc:  # report and continue with the other files
            print(f"!! {p}: could not read ({exc})")
            continue
        for label, (df, note) in frames.items():
            total_inputs += 1
            normalized = [str(c).strip().lower() for c in df.columns]
            header_counts.update(set(normalized))
            dup_headers = [c for c, n in Counter(normalized).items() if n > 1]
            print(f"\n== {label}  ({note})")
            print(f"   rows={len(df):,} cols={len(df.columns)}")
            print(f"   headers: {list(df.columns)}")
            if dup_headers:
                print(f"   WARNING duplicate headers after normalizing: {dup_headers}")
            print(f"   candidate keys: {candidate_keys(df) or 'none (consider a compound key)'}")
            empty = [c for c in df.columns if (df[c].astype(str).str.strip() == "").all()]
            if empty:
                print(f"   empty columns: {empty}")
    if total_inputs > 1:
        print("\n== header overlap (normalized name: inputs containing it)")
        for name, n in sorted(header_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"   {name}: {n}/{total_inputs}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
