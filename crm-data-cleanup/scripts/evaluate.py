#!/usr/bin/env python3
"""Score a dedupe.py run against a labeled truth file (record_id,entity_id).

Pairwise metrics: a predicted pair is two records placed in the same auto-merge
cluster (or listed together in the review queue). Precision is what matters most:
a false auto-merge destroys data; a missed duplicate only costs a second pass.

  python evaluate.py --plan-dir plan/ --truth assets/fixture/truth.csv
"""
import argparse
from itertools import combinations
from pathlib import Path

import pandas as pd


def pairs_from_plan(path: Path) -> set:
    if not path.exists() or path.stat().st_size == 0:
        return set()
    plan = pd.read_csv(path, dtype=str, keep_default_na=False)
    out = set()
    for _, r in plan.drop_duplicates("cluster_id").iterrows():
        members = [r["survivor_id"]] + [x for x in r["loser_ids"].split(";") if x]
        out |= {tuple(sorted(p)) for p in combinations(members, 2)}
    return out


def pairs_from_review(path: Path) -> set:
    if not path.exists() or path.stat().st_size <= 1:
        return set()
    try:
        q = pd.read_csv(path, dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError:
        return set()
    return {tuple(sorted((a, b))) for a, b in zip(q["record_a"], q["record_b"])}


def report(label, auto, review, truth_pairs, ids):
    auto = {p for p in auto if p[0] in ids and p[1] in ids}
    review = {p for p in review if p[0] in ids and p[1] in ids}
    tp = auto & truth_pairs
    fp = auto - truth_pairs
    both = auto | review
    rtp = review & truth_pairs
    print(f"\n== {label}")
    print(f"true duplicate pairs: {len(truth_pairs)}")
    print(f"auto-merge pairs: {len(auto)}  correct: {len(tp)}  WRONG: {len(fp)}")
    print(f"auto precision: {len(tp) / len(auto):.2%}" if auto else "auto precision: n/a")
    print(f"auto recall:    {len(tp) / len(truth_pairs):.2%}" if truth_pairs else "")
    print(f"review pairs: {len(review)}  true dupes among them: {len(rtp)}")
    print(f"recall incl. review: {len(both & truth_pairs) / len(truth_pairs):.2%}"
          if truth_pairs else "")
    missed = truth_pairs - both
    if fp:
        print("WRONG auto-merges:", sorted(fp))
    if missed:
        print("missed entirely:", sorted(missed))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan-dir", required=True)
    ap.add_argument("--truth", required=True)
    a = ap.parse_args()
    d = Path(a.plan_dir)
    truth = pd.read_csv(a.truth, dtype=str)
    for label, plan, queue, prefix in (
            ("contacts", "merge_plan.csv", "review_queue.csv", "C0"),
            ("companies", "companies_merge_plan.csv", "companies_review_queue.csv", "CO")):
        t = truth[truth["record_id"].str.startswith(prefix)] if prefix == "CO" else \
            truth[~truth["record_id"].str.startswith("CO")]
        ids = set(t["record_id"])
        groups = t.groupby("entity_id")["record_id"].apply(list)
        truth_pairs = {tuple(sorted(p)) for g in groups for p in combinations(g, 2)}
        report(label, pairs_from_plan(d / plan), pairs_from_review(d / queue), truth_pairs, ids)


if __name__ == "__main__":
    main()
