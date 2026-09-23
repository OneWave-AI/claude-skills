"""Run every spec in tests/specs against its fixture and compare with hand-computed
`expected` values. Plain python, no pytest needed:  python tests/test_measure_check.py"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from measure_check import load, run  # noqa: E402


def close(a, b):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) < 1e-9


def main():
    failures = 0
    for path in sorted((HERE / "specs").glob("*.json")):
        spec = json.loads(path.read_text())
        data = HERE / "fixtures" / spec.get("data", "sales.csv")
        rows, total = run(load(data, spec), spec)
        got = dict(rows)
        got["Total"] = total
        bad = [f"{k}: got {got.get(k)} want {v}" for k, v in spec["expected"].items()
               if not close(got.get(k), v)]
        print(f"{'FAIL' if bad else 'ok  '} {path.stem}" + ("".join(f"\n     {b}" for b in bad)))
        failures += bool(bad)
    print(f"\n{failures} failed" if failures else "\nall specs passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
