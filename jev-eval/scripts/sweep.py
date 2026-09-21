#!/usr/bin/env python3
"""Sweep criteria wordings and thresholds for a System One config.

  python sweep.py labelled.json configs.json --backend jev
  python sweep.py labelled.json configs.json --backend von --question lead_type

labelled.json  [{"id":"...", "state":"...", "truth":"label_or_bool"}, ...]
configs.json   {"<config name>": {"instructions":"...",
                                  "criteria":{"opt":"desc"} | ["level","level"] | null}, ...}
                criteria dict -> choice, list -> score, null/absent -> noul

Outputs: accuracy per config, the spread, a threshold sweep for nouls,
and confidence-gate economics (errors caught vs volume escalated).
"""
import argparse, json, subprocess, sys, time, urllib.request
from collections import Counter

API = "https://api.typesafe.ai/v1/systemone"

def keychain(service="typesafe-api-key"):
    r = subprocess.run(["security", "find-generic-password", "-s", service, "-w"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"no key in keychain service '{service}'. Store it with:\n"
                 f"  security add-generic-password -a \"$USER\" -s {service} -w '<key>' -U")
    return r.stdout.strip()

def qspec(cfg):
    crit = cfg.get("criteria")
    if isinstance(crit, dict):  return {"type": "choice", "instructions": cfg["instructions"], "criteria": crit}
    if isinstance(crit, list):  return {"type": "score",  "instructions": cfg["instructions"], "criteria": crit}
    return {"type": "noul", "instructions": cfg["instructions"]}

def ask_jev(state, qname, spec, key):
    body = json.dumps({"model": "jev-latest", "state": state,
                       "questions": {qname: spec}}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as f:
        return json.loads(f.read())["answers"][qname]

def ask_von(state, qname, spec):
    import von
    t = spec["type"]
    q = (von.Choice(instructions=spec["instructions"], criteria=spec["criteria"]) if t == "choice"
         else von.Score(instructions=spec["instructions"], criteria=spec["criteria"]) if t == "score"
         else von.Noul(instructions=spec["instructions"]))
    a = von.system_one(state=state, questions={qname: q}).answers[qname]
    return {"type": t, "choice": getattr(a, "choice", None), "score": getattr(a, "score", None),
            "noul": getattr(a, "noul", None), "confidence": getattr(a, "confidence", None),
            "probabilities": getattr(a, "probabilities", None)}

def value(ans):
    return ans.get("choice") if ans["type"] == "choice" else \
           ans.get("score")  if ans["type"] == "score"  else ans.get("noul")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("labelled"); p.add_argument("configs")
    p.add_argument("--backend", choices=["jev", "von"], default="jev")
    p.add_argument("--question", default="answer")
    p.add_argument("--keychain-service", default="typesafe-api-key")
    a = p.parse_args()

    rows = json.load(open(a.labelled))
    configs = json.load(open(a.configs))
    key = keychain(a.keychain_service) if a.backend == "jev" else None
    if a.backend == "von":
        import von; von.system_one(state="warm", questions={"w": von.Noul(instructions="t?")})

    results, lat = {}, {}
    for name, cfg in configs.items():
        spec = qspec(cfg); preds, confs, t0 = [], [], time.time()
        for r in rows:
            ans = (ask_jev(r["state"], a.question, spec, key) if a.backend == "jev"
                   else ask_von(r["state"], a.question, spec))
            preds.append(value(ans)); confs.append(ans.get("confidence"))
        lat[name] = (time.time() - t0) * 1000 / len(rows)
        results[name] = {"preds": preds, "confs": confs}

    is_noul = qspec(next(iter(configs.values())))["type"] == "noul"
    truth = [r["truth"] for r in rows]

    print(f"\n{'config':<28} {'accuracy':>10} {'ms/rec':>8}   misclassified as")
    print("-" * 82)
    accs = {}
    for name, res in results.items():
        if is_noul:
            hits = sum((p >= 0.5) == bool(t) for p, t in zip(res["preds"], truth))
        else:
            hits = sum(p == t for p, t in zip(res["preds"], truth))
        accs[name] = hits
        wrong = Counter(p for p, t in zip(res["preds"], truth)
                        if (p != t if not is_noul else (p >= 0.5) != bool(t)))
        print(f"{name:<28} {hits:>6}/{len(rows):<3} {lat[name]:>8.0f}   "
              f"{dict(list(wrong.items())[:3]) if wrong else '-'}")
    lo, hi = min(accs.values()), max(accs.values())
    print("-" * 82)
    print(f"spread across wordings: {lo}/{len(rows)} to {hi}/{len(rows)}"
          f"   ({'ROBUST - wording is not load-bearing' if hi - lo <= 1 else 'FRAGILE - criteria are load-bearing, every edit is a regression risk'})")

    if is_noul:
        best = max(accs, key=accs.get)
        print(f"\nthreshold sweep  [config: {best}]")
        print(f"{'t':>6} {'precision':>10} {'recall':>8} {'accuracy':>9}")
        for t in (0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95):
            z = list(zip(results[best]["preds"], truth))
            tp = sum(p >= t and bool(y) for p, y in z); fp = sum(p >= t and not bool(y) for p, y in z)
            fn = sum(p <  t and bool(y) for p, y in z); tn = sum(p <  t and not bool(y) for p, y in z)
            print(f"{t:>6} {tp/max(tp+fp,1):>10.2f} {tp/max(tp+fn,1):>8.2f} {(tp+tn)/len(z):>9.2f}")
    else:
        best = max(accs, key=accs.get)
        confs = results[best]["confs"]
        if any(c is not None for c in confs):
            print(f"\nconfidence gate  [config: {best}]")
            errs = [c for c, p, t in zip(confs, results[best]["preds"], truth) if p != t]
            print(f"{'gate':>6} {'errors caught':>15} {'volume escalated':>18}   verdict")
            for g in (0.5, 0.7, 0.9, 0.95):
                caught = sum(c < g for c in errs if c is not None)
                esc = sum(c < g for c in confs if c is not None)
                v = ("no gate needed" if not errs else
                     "saves nothing" if esc / len(rows) > 0.5 else
                     "workable" if errs and caught / len(errs) > 0.7 else "weak")
                print(f"{g:>6} {caught:>8}/{len(errs):<6} {esc/len(rows):>17.0%}   {v}")
    print()

if __name__ == "__main__":
    main()
