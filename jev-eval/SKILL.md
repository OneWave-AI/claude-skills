---
name: jev-eval
description: Build and run a labelled eval set for a System One model (Jev, Von, or any typed-decision config), then sweep criteria wordings and thresholds against it. Use when a Jev/Von classification is wrong or unreliable, when choosing between the hosted API and a local open model, when tuning noul thresholds, or before shipping any typed-decision feature. Produces an accuracy-by-wording matrix and a calibrated threshold.
---

# Evaluating a typed-decision config

**The eval set is the product.** A System One model's accuracy is dominated by how the
question was written, and the failure mode is silent — it returns a confident, type-valid,
wrong answer. Without labels you cannot tell a bad question from a bad model.

Measured: rewriting the criteria moved an open model from **4/15 to 14/15** on 15 records.
No model change. Then the same comparison at 150 records put that model at **61%** overall
against Jev's **97%** — the 15-record read was an artifact of a small, easy set. Both facts
are the point: wording swings results, and small sets lie about which way.

## Run it

```bash
python ~/.claude/skills/jev-eval/scripts/sweep.py labelled.json configs.json \
    --backend jev|von --question <name>
```

`labelled.json` is `[{"id","state","truth"}]`. `configs.json` maps a config name to
`{"instructions", "criteria"}` — a dict of options makes it a **choice**, a list of levels
makes it a **score**, omitting it makes it a **noul**. The script reads the Jev key from
Keychain (`typesafe-api-key`), prints accuracy per config, labels the spread
ROBUST or FRAGILE, sweeps thresholds for nouls, and scores the confidence gate.

Real output, 50 records of agent shell-command risk, only the backend changed:

```
config                         accuracy   ms/rec
A terse one-liners               45/50       410      <- Jev
B rich criteria                  49/50       415
C rich + exclusions              46/50       418
D deliberately lazy              44/50       411
spread: 44/50 to 49/50   (ROBUST - wording is not load-bearing)

A terse one-liners                9/50        66      <- Von, same configs
B rich criteria                  23/50       121
C rich + exclusions              15/50       129
D deliberately lazy              22/50        53
spread: 9/50 to 23/50    (FRAGILE - and the ceiling is still not usable)
```

Read the ceiling before the spread. A FRAGILE model whose best config is 23/50 is not a
wording problem you can write your way out of — it is the wrong model for that question.

## 1. Build the set

**50 records minimum, 200+ before shipping.** Pull from the real stream, not synthetic data.

- Include the **boring middle**, not just clean examples and dramatic edge cases
- Include records with **broken/missing metadata** — that is where classifiers fail
- Label by reading the record, **before** any model runs. Never label from model output
- Store as JSON with the raw record plus a `truth` field

```json
[{"id":"D-1994","state":"...full record text...","truth":"inbound_prospect"}]
```

If you cannot label a record confidently yourself, the model cannot either — either
drop it or fix the question so the answer is determinate.

## 2. Sweep wordings, not just models

The core move. Write 3–4 genuinely different criteria configs and run all of them:

- **A** — one terse line per option (what everyone writes first)
- **B** — 3–4 sentences per option with concrete examples
- **C** — B plus an explicit default and explicit exclusions ("ONLY when…")
- **D** — deliberately lazy, four or five words, as a floor test

Report accuracy per config per model:

```
config                    JEV       VON      LAYA     (lead triage, n=50)
A terse one-liners      47/50     34/50     21/50
B rich criteria         49/50     28/50     15/50
C rich + exclusions     48/50     24/50     19/50
D deliberately lazy     48/50     22/50     24/50
```

**Read the floor first, then the spread.** The floor is "can this model do the job at all
if I phrase it badly"; the spread is "how much will maintaining it cost me." Measured on the
command task, every hosted model floors at 82-92% (Haiku 46-48, GPT-4.1-mini 45-50, Jev
44-49, GPT-5-mini 41-49) while Von floors at 9/50 and Laya at 18/50. Note that **Jev is not
more wording-robust than a small LLM** — it swings the same ten points. What you buy is the
floor, not immunity.

Note what the leads column does NOT show: a clean "richer is better" gradient. Von's best
config here is the terse one. Whatever moves an open model's numbers is sensitivity to
surface form, not comprehension, so do not assume your next criteria rewrite improves it —
re-run the set.

## 3. Sweep thresholds for every noul

Never ship 0.5. Sweep and read the curve:

```python
for t in [0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.95]:
    tp = sum(p>=t and y     for p,y in z); fp = sum(p>=t and not y for p,y in z)
    fn = sum(p< t and y     for p,y in z); tn = sum(p< t and not y for p,y in z)
    print(f"{t}  P={tp/max(tp+fp,1):.2f}  R={tp/max(tp+fn,1):.2f}  acc={(tp+tn)/len(z):.2f}")
```

Different models have different **floors**. Jev's noul sat at 0.2–0.5 on records that were
plainly clean, where Claude went to 0.0 — so its real cut was ~0.85. A threshold tuned on
one model does not transfer to another. Re-sweep when you switch.

## 4. Score the confidence gate honestly

Two numbers, always together:

```python
errs   = [r for r in rows if r.pred != r.truth]
rights = [r for r in rows if r.pred == r.truth]
for g in [0.5,0.7,0.9]:
    caught    = sum(r.conf <  g for r in errs)      # errors the gate escalates
    escalated = sum(r.conf <  g for r in rows)      # total volume escalated
    print(f"gate {g}: catches {caught}/{len(errs)} errors, escalates {escalated/len(rows):.0%} of volume")
```

A gate catching 10/11 errors while escalating 93% of volume is **not a working gate** —
it is a slow path with extra steps. Good calibration without good accuracy buys nothing.

## 5. Report

- accuracy per config per model, with the spread called out
- chosen threshold per noul, with the sweep that justified it
- gate: errors caught **and** volume escalated
- projected latency and cost per 1k at production volume
- explicit statement of eval-set size and what it does **not** cover

Small sets lie. 15 records where two models both score 100% distinguishes nothing — say so
rather than implying the tie is meaningful.

## Related

`jev-integrate` is the wiring workflow this feeds. `jev-audit` finds candidates worth evaluating.
