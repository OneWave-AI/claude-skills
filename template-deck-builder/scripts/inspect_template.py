#!/usr/bin/env python3
"""Map a company .pptx/.potx template so slides get built INTO it.

Writes layout_map.json with: slide size, theme colors + fonts, every master's
layouts with their placeholders (idx, type, name, geometry in EMU and inches),
which slide types each layout suits, a recommended layout per slide type, and
(for an existing deck) the slides already present.

Usage:
  python3 inspect_template.py TEMPLATE.pptx [-o layout_map.json] [--quiet]
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tdb_common import (CHROME_TYPES, CONTENT_TYPES, PP_PLACEHOLDER, TITLE_TYPES,  # noqa: E402
                        emu_to_in, is_source_ph, open_presentation, ph_type, read_theme, rect)

SLIDE_TYPES = ["title", "section", "agenda", "one_message_chart", "two_column", "table", "quote", "title_only", "blank"]

NAME_HINTS = {
    "title": r"\b(title slide|cover|opening)\b",
    "section": r"section|divider|chapter|break",
    "agenda": r"agenda|contents|overview",
    "two_column": r"two|2[- ]?col|comparison|compare|split|side",
    "quote": r"quote|testimonial|statement|big number|callout",
    "table": r"table",
    "one_message_chart": r"chart|content|exhibit|graph|body",
    "title_only": r"title only",
    "blank": r"blank",
}


def describe_placeholder(ph, slide_h):
    r = rect(ph)
    t = ph_type(ph)
    d = {
        "idx": ph.placeholder_format.idx,
        "type": t.name if t is not None else None,
        "name": ph.name,
        "role": role_of(ph, slide_h),
    }
    if r:
        d["emu"] = {"left": r[0], "top": r[1], "width": r[2], "height": r[3]}
        d["inches"] = {"left": emu_to_in(r[0]), "top": emu_to_in(r[1]),
                       "width": emu_to_in(r[2]), "height": emu_to_in(r[3])}
    return d


def role_of(ph, slide_h):
    t = ph_type(ph)
    if t in TITLE_TYPES:
        return "title"
    if t == PP_PLACEHOLDER.SUBTITLE:
        return "subtitle"
    if t in CHROME_TYPES:
        return "chrome (date/footer/number: NOT copied to new slides by python-pptx)"
    if is_source_ph(ph, slide_h):
        return "source line"
    if t == PP_PLACEHOLDER.CHART:
        return "content (chart)"
    if t == PP_PLACEHOLDER.TABLE:
        return "content (table)"
    if t in (PP_PLACEHOLDER.PICTURE, PP_PLACEHOLDER.BITMAP):
        return "content (picture)"
    if t == PP_PLACEHOLDER.OBJECT:
        return "content (text, chart or table)"
    if t == PP_PLACEHOLDER.BODY:
        return "content (text only)"
    return "other"


def classify(layout, slide_w, slide_h):
    """Return (suits, scores): structural fit first, name hints as tie-breakers."""
    phs = list(layout.placeholders)
    types = [ph_type(p) for p in phs]
    has_ctr = PP_PLACEHOLDER.CENTER_TITLE in types
    has_title = any(t in TITLE_TYPES for t in types)
    has_sub = PP_PLACEHOLDER.SUBTITLE in types
    content = [p for p in phs if ph_type(p) in CONTENT_TYPES and not is_source_ph(p, slide_h)]
    area = slide_w * slide_h
    big = [p for p in content if rect(p) and rect(p)[2] * rect(p)[3] > area * 0.25]
    mid = [p for p in content if rect(p) and area * 0.08 < rect(p)[2] * rect(p)[3] <= area * 0.25]
    name = layout.name.lower()
    scores = {k: 0 for k in SLIDE_TYPES}

    if has_ctr or (has_title and has_sub and not big):
        scores["title"] += 6
    if has_title and not content and not has_sub and not has_ctr:
        scores["title_only"] += 5
    if not phs or all(t in CHROME_TYPES for t in types):
        scores["blank"] += 6
    if has_title and not has_ctr and len(content) <= 1 and not big:
        scores["section"] += 3
    if has_title and len(big) == 1 and not mid:
        t = ph_type(big[0])
        # a typed chart/table/picture placeholder accepts only that content
        fits = {PP_PLACEHOLDER.CHART: ("one_message_chart",), PP_PLACEHOLDER.TABLE: ("table",),
                PP_PLACEHOLDER.PICTURE: (), PP_PLACEHOLDER.BITMAP: ()}.get(
                    t, ("one_message_chart", "agenda", "table"))
        for k in fits:
            scores[k] += 5
        if t == PP_PLACEHOLDER.CHART:
            scores["one_message_chart"] += 3
        if t == PP_PLACEHOLDER.TABLE:
            scores["table"] += 3
        if t == PP_PLACEHOLDER.BODY:  # text-only body: fine for agenda, chart goes in geometry
            scores["agenda"] += 1
    side = [p for p in content if rect(p) and rect(p)[3] > slide_h * 0.3]
    if has_title and len(side) >= 2:
        lefts = sorted({round(rect(p)[0] / (slide_w / 20)) for p in side})
        if len(lefts) >= 2:
            scores["two_column"] += 7
    if (not has_title or not big) and content and any(rect(p) and rect(p)[2] > slide_w * 0.5 for p in content):
        scores["quote"] += 2
    for k, pat in NAME_HINTS.items():
        if re.search(pat, name):
            scores[k] += 3
    suits = [k for k, v in sorted(scores.items(), key=lambda kv: -kv[1]) if v >= 5]
    return suits, scores


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("template")
    ap.add_argument("-o", "--out", default="layout_map.json")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    prs = open_presentation(a.template)
    W, H = prs.slide_width, prs.slide_height
    out = {
        "source_file": str(a.template),
        "slide_size": {"emu": [W, H], "inches": [emu_to_in(W), emu_to_in(H)],
                       "aspect": "16:9" if abs(W / H - 16 / 9) < 0.02 else ("4:3" if abs(W / H - 4 / 3) < 0.02 else f"{W / H:.3f}")},
        "masters": [],
        "recommended": {},
        "existing_slides": [],
    }
    best = {k: (0, None) for k in SLIDE_TYPES}
    for mi, master in enumerate(prs.slide_masters):
        m = {"index": mi, "theme": read_theme(master),
             "master_placeholders": [describe_placeholder(p, H) for p in master.placeholders],
             "layouts": []}
        for li, layout in enumerate(master.slide_layouts):
            suits, scores = classify(layout, W, H)
            m["layouts"].append({
                "index": li, "name": layout.name, "suits": suits,
                "used_by_slides": len(layout.used_by_slides),
                "placeholders": [describe_placeholder(p, H) for p in layout.placeholders],
                "non_placeholder_shapes": [s.name for s in layout.shapes if not s.is_placeholder],
            })
            for k, v in scores.items():
                if v >= 5 and v > best[k][0]:
                    best[k] = (v, layout.name)
        out["masters"].append(m)
    out["recommended"] = {k: v[1] for k, v in best.items()}

    for si, slide in enumerate(prs.slides, 1):
        shapes = []
        for s in slide.shapes:
            d = {"name": s.name, "placeholder_idx": s.placeholder_format.idx if s.is_placeholder else None,
                 "kind": str(s.shape_type).split(".")[-1].split(" ")[0] if s.shape_type else "UNKNOWN"}
            if s.has_text_frame and s.text_frame.text.strip():
                d["text"] = s.text_frame.text.strip()[:120]
            shapes.append(d)
        out["existing_slides"].append({"slide": si, "layout": slide.slide_layout.name, "shapes": shapes})

    Path(a.out).write_text(json.dumps(out, indent=2))
    if not a.quiet:
        th = out["masters"][0]["theme"]
        print(f"Template: {a.template}  size {out['slide_size']['inches']} in ({out['slide_size']['aspect']})")
        print(f"Theme fonts: heading={th['fonts']['major']} body={th['fonts']['minor']}")
        print("Theme colors: " + ", ".join(f"{k}={v}" for k, v in th["colors"].items()))
        for m in out["masters"]:
            for l in m["layouts"]:
                phs = ", ".join(f"{p['idx']}:{p['type']}" for p in l["placeholders"] if not p["role"].startswith("chrome"))
                print(f"  [{m['index']}.{l['index']}] {l['name']!r:34} suits={l['suits'] or '-'}  ph=[{phs}]")
        print("Recommended: " + json.dumps(out["recommended"]))
        print(f"Existing slides: {len(out['existing_slides'])}")
        print(f"Wrote {a.out}")


if __name__ == "__main__":
    main()
