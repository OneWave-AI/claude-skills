#!/usr/bin/env python3
"""Visual + structural QA for a deck built into a template.

Checks (per slide): estimated text overflow vs placeholder box (font-metric
approximation, flags reliance on shrink-on-overflow autofit), shapes outside
slide bounds, overlaps between text and other shapes, off-theme fonts and
colors, empty placeholders left behind, geometry drift from the layout,
action titles (length, full sentence), exhibits without a source line, missing
speaker notes, slide count vs storyboard. Renders via LibreOffice -> PDF ->
PNG and writes a contact sheet so the result gets LOOKED at.

Usage:
  python3 qa_deck.py deck.pptx [--storyboard sb.json] [--out-dir qa/] [--no-render] [--strict]
Exit code 1 when any ERROR is found (always with --strict on WARN too).
"""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pptx.enum.shapes import MSO_SHAPE_TYPE  # noqa: E402

from inspect_template import classify  # noqa: E402
from tdb_common import (CHROME_TYPES, EMU_PER_INCH, EMU_PER_PT, NS, PP_PLACEHOLDER, TITLE_TYPES,  # noqa: E402
                        open_presentation, ph_type, read_theme, rect)

# Helvetica/Arial advance widths (1/1000 em). Good enough to estimate wrapping.
_W = dict(zip(" !\"#$%&'()*+,-./0123456789:;<=>?@", [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584,
          278, 333, 278, 278] + [556] * 10 + [278, 278, 584, 584, 584, 556, 1015]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
          778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update(zip("abcdefghijklmnopqrstuvwxyz", [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556,
          556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update({"[": 278, "]": 278, "_": 556, "{": 334, "}": 334, "|": 260, "~": 584, "’": 222, "“": 333,
           "”": 333, "–": 556, "—": 1000, "•": 350, "€": 556, "£": 556})
# width relative to Arial, by family (lowercase substring match)
FAMILY_FACTOR = {"georgia": 1.02, "verdana": 1.18, "tahoma": 1.02, "trebuchet": 1.0, "calibri": 0.90,
                 "aptos": 0.97, "cambria": 1.0, "times": 0.88, "garamond": 0.88, "segoe": 1.0,
                 "helvetica": 1.0, "arial narrow": 0.82, "arial": 1.0, "roboto": 0.98, "open sans": 1.06,
                 "lato": 0.97, "montserrat": 1.12, "inter": 1.03, "century gothic": 1.12, "futura": 1.02}
DEFAULT_SIZE_PT = 18.0
VERBISH = set("""is are was were be been being am will would can could should must may might shall has have had do does
did grows grew rises rose falls fell drives drove cuts cut needs need makes made lets let gets got takes took gives
gave shows showed beats beat lags lagged leads led outperforms outpaces trails remains stays requires delivers
enables unlocks captures costs saves pays loses lost wins won doubles halves exceeds reaches hits misses creates
carry carries generate generates recover recovers price prices charge charges face faces""".split())
NOUN_SUFFIX = ("tion", "tions", "sion", "sions", "ment", "ments", "ness", "ities", "ics", "ship", "ships", "ence", "ance",
               "ss", "us", "is", "ous", "ess")


class Issue(dict):
    pass


def issue(sev, slide, check, msg, shape=None):
    return Issue(severity=sev, slide=slide, check=check, shape=shape, message=msg)


# ---------------------------------------------------------------- inheritance

def _lvl(lst, level):
    return None if lst is None else lst.find(f"a:lvl{level + 1}pPr", NS)


class TextContext:
    """Resolves effective paragraph/run properties through the inheritance chain:
    slide shape -> layout placeholder -> master placeholder -> master txStyles."""

    def __init__(self, prs, slide, shape, theme):
        self.shape, self.theme = shape, theme
        self.lsts, self.bodyprs = [], []
        tx = shape._element.find(".//p:txBody", NS)
        if tx is None:
            tx = shape._element.find(".//a:txBody", NS)
        self.lsts.append(tx.find("a:lstStyle", NS) if tx is not None else None)
        self.bodyprs.append(tx.find("a:bodyPr", NS) if tx is not None else None)
        self.is_title = False
        master = slide.slide_layout.slide_master
        txstyles = master._element.find(".//p:txStyles", NS)
        if shape.is_placeholder:
            t = ph_type(shape)
            idx = shape.placeholder_format.idx
            self.is_title = t in TITLE_TYPES
            lay_ph = next((p for p in slide.slide_layout.placeholders if p.placeholder_format.idx == idx), None)
            mst_ph = None
            want = "title" if self.is_title else {PP_PLACEHOLDER.DATE: "dt", PP_PLACEHOLDER.FOOTER: "ftr",
                                                  PP_PLACEHOLDER.SLIDE_NUMBER: "sldNum"}.get(t, "body")
            for p in master.placeholders:
                mt = ph_type(p)
                cat = "title" if mt in TITLE_TYPES else {PP_PLACEHOLDER.DATE: "dt", PP_PLACEHOLDER.FOOTER: "ftr",
                                                        PP_PLACEHOLDER.SLIDE_NUMBER: "sldNum"}.get(mt, "body")
                if cat == want:
                    mst_ph = p
                    break
            for p in (lay_ph, mst_ph):
                ptx = p._element.find(".//p:txBody", NS) if p is not None else None
                self.lsts.append(ptx.find("a:lstStyle", NS) if ptx is not None else None)
                self.bodyprs.append(ptx.find("a:bodyPr", NS) if ptx is not None else None)
            self.lsts.append(txstyles.find("p:titleStyle" if self.is_title else "p:bodyStyle", NS)
                             if txstyles is not None else None)
        else:
            dts = prs.part._element.find("p:defaultTextStyle", NS)
            self.lsts.append(dts)
            self.lsts.append(txstyles.find("p:otherStyle", NS) if txstyles is not None else None)

    def ppr(self, p_el, level):
        chain = [p_el.find("a:pPr", NS)] + [_lvl(l, level) for l in self.lsts]
        return [c for c in chain if c is not None]

    def run_attr(self, r_el, p_el, level, attr):
        rpr = r_el.find("a:rPr", NS) if r_el is not None else None
        if rpr is not None and rpr.get(attr) is not None:
            return rpr.get(attr)
        for ppr in self.ppr(p_el, level):
            d = ppr.find("a:defRPr", NS)
            if d is not None and d.get(attr) is not None:
                return d.get(attr)
        return None

    def typeface(self, r_el, p_el, level):
        rpr = r_el.find("a:rPr", NS) if r_el is not None else None
        el = rpr.find("a:latin", NS) if rpr is not None else None
        if el is not None:
            tf = el.get("typeface")
        else:
            tf = None
            for ppr in self.ppr(p_el, level):
                e = ppr.find("a:defRPr/a:latin", NS)
                if e is not None:
                    tf = e.get("typeface")
                    break
        if tf in (None, "+mn-lt"):
            return self.theme["fonts"]["major" if (tf is None and self.is_title) else "minor"] or "Arial"
        if tf == "+mj-lt":
            return self.theme["fonts"]["major"] or "Arial"
        return tf

    def spacing(self, p_el, level, tag, size_pt):
        for ppr in self.ppr(p_el, level):
            e = ppr.find(f"a:{tag}", NS)
            if e is not None:
                pts, pct = e.find("a:spcPts", NS), e.find("a:spcPct", NS)
                if pts is not None:
                    return ("pts", int(pts.get("val")) / 100.0)
                if pct is not None:
                    return ("pct", int(pct.get("val")) / 100000.0)
        return None

    def marl(self, p_el, level):
        for ppr in self.ppr(p_el, level):
            if ppr.get("marL") is not None:
                return int(ppr.get("marL"))
        return 0

    def body_attr(self, attr, default):
        for b in self.bodyprs:
            if b is not None and b.get(attr) is not None:
                return b.get(attr)
        return default

    def autofit(self):
        for b in self.bodyprs:
            if b is None:
                continue
            for tag in ("normAutofit", "spAutoFit", "noAutofit"):
                e = b.find(f"a:{tag}", NS)
                if e is not None:
                    return tag, e
        return None, None


# ---------------------------------------------------------------- text fit

SAFETY = 1.05  # renderer/kerning/substitution slack; calibrated against LibreOffice renders


def text_width_pt(text, size_pt, family, bold):
    f = 1.06  # unknown family: assume a bit wider than Arial
    fam = (family or "").lower()
    for k, v in FAMILY_FACTOR.items():
        if k in fam:
            f = v
            break
    w = sum(_W.get(ch, 556) for ch in text)
    return w / 1000.0 * size_pt * f * SAFETY * (1.06 if bold else 1.0)


def estimate_text(ctx, shape):
    """Return (needed_height_emu, available_height_emu, min_font_pt, fonts_used, autofit)."""
    tx = shape.text_frame._txBody
    r = rect(shape)
    lins = int(ctx.body_attr("lIns", 91440))
    rins = int(ctx.body_attr("rIns", 91440))
    tins = int(ctx.body_attr("tIns", 45720))
    bins = int(ctx.body_attr("bIns", 45720))
    wrap = ctx.body_attr("wrap", "square") != "none"
    fit_kind, fit_el = ctx.autofit()
    scale = 1.0
    ln_red = 0.0
    if fit_kind == "normAutofit" and fit_el is not None:
        scale = int(fit_el.get("fontScale", "100000")) / 100000.0
        ln_red = int(fit_el.get("lnSpcReduction", "0")) / 100000.0
    avail_w = (r[2] - lins - rins) / EMU_PER_PT
    total = 0.0
    sizes, fonts = [], set()
    max_line_w = 0.0
    for pi, p in enumerate(tx.findall("a:p", NS)):
        ppr = p.find("a:pPr", NS)
        level = int(ppr.get("lvl", "0")) if ppr is not None else 0
        runs = p.findall("a:r", NS) + p.findall("a:fld", NS)
        text = "".join((x.findtext("a:t", default="", namespaces=NS)) for x in runs)
        first = runs[0] if runs else None
        sz = ctx.run_attr(first, p, level, "sz")
        size = (int(sz) / 100.0 if sz else DEFAULT_SIZE_PT)
        size_nominal = size
        size *= scale
        bold = ctx.run_attr(first, p, level, "b") in ("1", "true")
        fam = ctx.typeface(first, p, level)
        fonts.add(fam)
        if text.strip():
            sizes.append(size_nominal)
        width = avail_w - ctx.marl(p, level) / EMU_PER_PT
        ls = ctx.spacing(p, level, "lnSpc", size)
        line_h = size * 1.2 * ((ls[1] if ls and ls[0] == "pct" else 1.0) - ln_red)
        if ls and ls[0] == "pts":
            line_h = ls[1]
        if not text:
            lines = 1
        elif not wrap:
            lines = 1
            max_line_w = max(max_line_w, text_width_pt(text, size, fam, bold))
        else:
            lines, cur = 1, 0.0
            space = text_width_pt(" ", size, fam, bold)
            for word in text.split(" "):
                ww = text_width_pt(word, size, fam, bold)
                if cur and cur + space + ww > width:
                    lines += 1
                    cur = ww
                    if ww > width:
                        lines += math.ceil(ww / width) - 1
                else:
                    cur = cur + (space if cur else 0) + ww
        before = ctx.spacing(p, level, "spcBef", size) if pi else None
        after = ctx.spacing(p, level, "spcAft", size)
        extra = 0.0
        for sp in (before, after):
            if sp:
                extra += sp[1] if sp[0] == "pts" else sp[1] * size * 1.2
        total += lines * line_h + extra
    needed = int(total * EMU_PER_PT) + tins + bins
    return {"needed": needed, "avail": r[3], "min_size": min(sizes) if sizes else None,
            "fonts": fonts, "autofit": fit_kind, "scale": scale,
            "nowrap_overflow": (not wrap and max_line_w * EMU_PER_PT > r[2] - lins - rins)}


# ---------------------------------------------------------------- title rules

def title_issues(n, text):
    out = []
    words = re.findall(r"[A-Za-z0-9%$'\-’.]+", text)
    wc = len(words)
    if wc > 15:
        out.append(issue("WARN", n, "action_title", f"title is {wc} words; keep action titles to ~15 words / two lines"))
    if 0 < wc < 5:
        out.append(issue("WARN", n, "action_title", f"'{text}' reads like a topic label; state the takeaway as a sentence"))
    low = [w.lower().strip(".,'’") for w in words]
    has_verb = any(w in VERBISH for w in low)
    if not has_verb:
        for i, w in enumerate(low[1:], 1):
            if len(w) > 3 and not w.endswith(NOUN_SUFFIX) and (w.endswith("ed") or (w.endswith("s") and not w.endswith("'s"))):
                has_verb = True
                break
    if wc >= 5 and not has_verb:
        out.append(issue("WARN", n, "action_title", "no verb found; an action title is a full sentence with a so-what (heuristic)"))
    if text.rstrip().endswith((":", "?")):
        out.append(issue("INFO", n, "action_title", "title ends with ':' or '?'; answer the question in the title instead"))
    return out


# ---------------------------------------------------------------- geometry

def inter(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[0] + a[2], b[0] + b[2]), min(a[1] + a[3], b[1] + b[3])
    return max(0, x2 - x1) * max(0, y2 - y1)


def has_text(s):
    return s.has_text_frame and s.text_frame.text.strip() != ""


def kind(s):
    if s.shape_type == MSO_SHAPE_TYPE.PLACEHOLDER or s.is_placeholder:
        if getattr(s, "has_chart", False) and s.has_chart:
            return "chart"
        if getattr(s, "has_table", False) and s.has_table:
            return "table"
        return "placeholder"
    if getattr(s, "has_chart", False) and s.has_chart:
        return "chart"
    if getattr(s, "has_table", False) and s.has_table:
        return "table"
    if s.shape_type == MSO_SHAPE_TYPE.PICTURE:
        return "picture"
    if s.shape_type == MSO_SHAPE_TYPE.TEXT_BOX:
        return "textbox"
    return "shape"


# ---------------------------------------------------------------- main checks

def check_deck(path, storyboard=None):
    prs = open_presentation(path)
    W, H = prs.slide_width, prs.slide_height
    issues, titles = [], []
    for si, slide in enumerate(prs.slides, 1):
        master = slide.slide_layout.slide_master
        theme = read_theme(master)
        theme_hex = set(theme["colors"].values())
        theme_fonts = {f for f in theme["fonts"].values() if f} | {"+mj-lt", "+mn-lt", "+mj-ea", "+mn-ea", "+mj-cs", "+mn-cs"}
        suits, _ = classify(slide.slide_layout, W, H)
        framing = bool({"title", "section", "quote"} & set(suits[:1])) or "blank" in suits[:1]
        shapes = list(slide.shapes)
        sb_type = None
        if storyboard and si <= len(storyboard.get("slides", [])):
            sb_type = storyboard["slides"][si - 1].get("type")
            if sb_type in ("title", "cover", "section", "divider", "quote", "closing"):
                framing = True
        slide_text = " ".join(s.text_frame.text for s in shapes if s.has_text_frame)
        has_exhibit = False
        title_text = None

        for s in shapes:
            r = rect(s)
            k = kind(s)
            if k in ("chart", "table", "picture"):
                has_exhibit = has_exhibit or k in ("chart", "table")
            if r is None:
                continue
            tol = int(0.01 * EMU_PER_INCH)
            if r[0] < -tol or r[1] < -tol or r[0] + r[2] > W + tol or r[1] + r[3] > H + tol:
                issues.append(issue("ERROR", si, "off_slide",
                                    f"'{s.name}' extends outside the slide ({r[0] / EMU_PER_INCH:.2f},{r[1] / EMU_PER_INCH:.2f}) "
                                    f"{r[2] / EMU_PER_INCH:.2f}x{r[3] / EMU_PER_INCH:.2f}in on {W / EMU_PER_INCH:.2f}x{H / EMU_PER_INCH:.2f}", s.name))
            if not s.is_placeholder and k in ("textbox", "shape") and has_text(s):
                sev = "INFO" if s.name == "tdb-source" else "WARN"
                issues.append(issue(sev, si, "free_text_box",
                                    f"'{s.name}' is a free-floating text box, not a template placeholder"
                                    + (" (source line fallback)" if sev == "INFO" else "; move the content into a layout placeholder"), s.name))
            if s.is_placeholder:
                t = ph_type(s)
                if t in TITLE_TYPES and has_text(s):
                    title_text = s.text_frame.text.strip()
                if s.has_text_frame and not has_text(s) and t not in CHROME_TYPES:
                    issues.append(issue("WARN", si, "empty_placeholder",
                                        f"empty placeholder '{s.name}' (idx {s.placeholder_format.idx}) left behind; fill it or remove it", s.name))
                if t in (PP_PLACEHOLDER.PICTURE,) and k == "placeholder":
                    issues.append(issue("WARN", si, "empty_placeholder", f"picture placeholder '{s.name}' has no picture", s.name))
                # geometry drift from the layout grid
                own = s._element.find("p:spPr/a:xfrm", NS)
                if own is not None:
                    lay = next((p for p in slide.slide_layout.placeholders
                                if p.placeholder_format.idx == s.placeholder_format.idx), None)
                    if lay is not None and rect(lay):
                        d = max(abs(a - b) for a, b in zip(rect(lay), r)) / EMU_PER_INCH
                        if d > 0.05:
                            issues.append(issue("INFO", si, "layout_drift",
                                                f"'{s.name}' moved/resized {d:.2f}in off the layout's position", s.name))
            # text fit
            if s.has_text_frame and has_text(s):
                ctx = TextContext(prs, slide, s, theme)
                est = estimate_text(ctx, s)
                ratio = est["needed"] / max(est["avail"], 1)
                where = f"'{s.name}': est. {est['needed'] / EMU_PER_INCH:.2f}in of text in a {est['avail'] / EMU_PER_INCH:.2f}in box ({ratio:.0%})"
                if est["autofit"] == "spAutoFit":
                    ratio = 0  # the box grows with its text: check where the grown box ends instead
                    if r[1] + est["needed"] > H + int(0.01 * EMU_PER_INCH):
                        issues.append(issue("ERROR", si, "off_slide",
                                            f"'{s.name}' resizes to fit its text and grows past the slide bottom", s.name))
                if est["autofit"] == "normAutofit" and est["scale"] < 1.0:
                    issues.append(issue("WARN", si, "autofit_reliance",
                                        f"'{s.name}' is shrunk to {est['scale']:.0%} by autofit; type sizes now differ from the template; cut text instead", s.name))
                if ratio > 1.05:
                    msg = where + "; overflows"
                    if est["autofit"] == "normAutofit":
                        msg += " (shrink-on-overflow is set, so PowerPoint will shrink it on edit and LibreOffice on render; do not rely on it)"
                    issues.append(issue("ERROR", si, "text_overflow", msg + "; cut or split the content", s.name))
                elif ratio > 0.92:
                    issues.append(issue("WARN", si, "text_tight", where + "; tight, may overflow with font substitution", s.name))
                if est["nowrap_overflow"]:
                    issues.append(issue("ERROR", si, "text_overflow", f"'{s.name}' has wrap off and a line wider than the box", s.name))
                if est["min_size"] and est["min_size"] < 10 and not s.name.startswith("tdb-source"):
                    issues.append(issue("WARN", si, "small_type", f"'{s.name}' has {est['min_size']:.0f}pt text; under 10pt is unreadable projected", s.name))
            if k == "table":
                issues.extend(check_table(si, s, H))

        # overlaps: any text-bearing shape against any other visible shape
        boxes = [(s, rect(s), kind(s)) for s in shapes if rect(s)]
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                (a, ra, ka), (b, rb, kb) = boxes[i], boxes[j]
                if not (has_text(a) or has_text(b)):
                    continue
                if ka == "placeholder" and not has_text(a) or kb == "placeholder" and not has_text(b):
                    continue
                area = inter(ra, rb)
                small = min(ra[2] * ra[3], rb[2] * rb[3]) or 1
                if area / small > 0.04:
                    if max(ra[2] * ra[3], rb[2] * rb[3]) > 0.9 * W * H:
                        continue  # full-bleed background shape
                    sev = "ERROR" if area / small > 0.15 else "WARN"
                    issues.append(issue(sev, si, "overlap",
                                        f"'{a.name}' and '{b.name}' overlap ({area / small:.0%} of the smaller); text over another shape", a.name))

        # theme fidelity in slide XML (+ chart parts)
        xml_roots = [slide._element]
        for s in shapes:
            if getattr(s, "has_chart", False) and s.has_chart:
                xml_roots.append(s.chart.part._element)
        bad_colors, bad_fonts = set(), set()
        for root in xml_roots:
            for el in root.iter(f"{{{NS['a']}}}srgbClr"):
                if el.get("val", "").upper() not in theme_hex:
                    # ignore colors inside pictures' effects
                    bad_colors.add(el.get("val").upper())
            for tag in ("latin", "ea", "cs"):
                for el in root.iter(f"{{{NS['a']}}}{tag}"):
                    tf = el.get("typeface")
                    if tf and tf not in theme_fonts and tag == "latin":
                        bad_fonts.add(tf)
        if bad_colors:
            issues.append(issue("WARN", si, "off_theme_color",
                                f"hard-coded colors not in the theme palette: {sorted(bad_colors)}; use theme colors (accent1..6, dk/lt)"))
        if bad_fonts:
            issues.append(issue("WARN", si, "off_theme_font",
                                f"fonts not in the theme ({theme['fonts']['major']}/{theme['fonts']['minor']}): {sorted(bad_fonts)}"))

        if title_text is not None:
            titles.append((si, title_text))
            if not framing:
                issues.extend(title_issues(si, title_text))
        elif not framing and suits[:1] != ["blank"]:
            issues.append(issue("WARN", si, "action_title", "content slide has no title; every content slide needs an action title"))
        elif suits[:1] == ["blank"] or not slide.placeholders:
            issues.append(issue("WARN", si, "template_bypass",
                                "slide uses a blank layout with hand-drawn shapes; rebuild it on a template layout"))
        if re.search(r"\[TBD\]|\bTBD\b|\bXX+\b|lorem ipsum|click to (add|edit)", slide_text, re.I):
            issues.append(issue("WARN", si, "placeholder_text", "unresolved placeholder text ([TBD], XX, lorem ipsum, 'Click to add')"))
        if has_exhibit and "source" not in slide_text.lower():
            issues.append(issue("WARN", si, "no_source", "chart/table without a source line"))
        notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        if not notes and not framing:
            issues.append(issue("INFO", si, "no_notes", "no speaker notes"))

    seen = {}
    for si, t in titles:
        if t.lower() in seen:
            issues.append(issue("WARN", si, "duplicate_title", f"same title as slide {seen[t.lower()]}"))
        seen[t.lower()] = si
    n = len(prs.slides)
    if storyboard is not None:
        exp = storyboard.get("expected_slide_count")
        if exp is None and not any("edit" in s for s in storyboard.get("slides", [])):
            exp = len(storyboard.get("slides", []))
        if exp is not None and exp != n:
            issues.append(issue("ERROR", 0, "slide_count", f"deck has {n} slides, storyboard expects {exp}"))
    return prs, issues, titles


def check_table(si, gf, H):
    out = []
    tbl = gf.table
    total = 0
    for ri, row in enumerate(tbl.rows):
        row_need = row.height
        for ci, cell in enumerate(row.cells):
            text = cell.text_frame.text
            if not text:
                continue
            sz = None
            for p in cell.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size:
                        sz = r.font.size.pt
            size = sz or DEFAULT_SIZE_PT
            width_pt = (tbl.columns[ci].width - 2 * 91440) / EMU_PER_PT
            lines = 0
            for para in text.split("\n"):
                lines += max(1, math.ceil(text_width_pt(para, size, "arial", False) * 1.05 / max(width_pt, 1)))
            need = int((lines * size * 1.2) * EMU_PER_PT) + 2 * 45720
            row_need = max(row_need, need)
        total += row_need
    if gf.top + total > H:
        out.append(issue("ERROR", si, "table_overflow",
                         f"table '{gf.name}' grows to ~{total / EMU_PER_INCH:.2f}in and runs off the slide; cut rows or split", gf.name))
    elif total > gf.height * 1.08:
        out.append(issue("WARN", si, "table_overflow",
                         f"table '{gf.name}' grows to ~{total / EMU_PER_INCH:.2f}in vs {gf.height / EMU_PER_INCH:.2f}in placeholder", gf.name))
    return out


# ---------------------------------------------------------------- render

def render(deck, out_dir, dpi):
    soffice = shutil.which("soffice") or shutil.which("libreoffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    pdftoppm = shutil.which("pdftoppm")
    if not Path(soffice).exists() and not shutil.which(soffice):
        return None, "LibreOffice (soffice) not found; skipped render"
    if not pdftoppm:
        return None, "pdftoppm (poppler) not found; skipped render"
    slides_dir = out_dir / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        profile = Path(tmp) / "lo_profile"  # isolated profile: parallel soffice runs do not collide
        cmd = [soffice, f"-env:UserInstallation=file://{profile}", "--headless", "--convert-to", "pdf",
               "--outdir", tmp, str(deck)]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        pdf = Path(tmp) / (Path(deck).stem + ".pdf")
        if not pdf.exists():
            return None, f"soffice failed: {res.stderr.strip()[:300]}"
        shutil.copy(pdf, out_dir / "deck.pdf")
        for old in slides_dir.glob("slide-*.png"):
            old.unlink()
        subprocess.run([pdftoppm, "-r", str(dpi), "-png", str(pdf), str(slides_dir / "slide")], check=True)
    pngs = sorted(slides_dir.glob("slide-*.png"), key=lambda p: int(re.findall(r"(\d+)", p.stem)[-1]))
    return pngs, None


def contact_sheet(pngs, issues, out_path, cols=3):
    from PIL import Image, ImageDraw, ImageFont
    thumbs = [Image.open(p).convert("RGB") for p in pngs]
    tw = 420
    th = int(thumbs[0].height * tw / thumbs[0].width)
    pad, label = 14, 26
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + label + pad) + pad), (236, 236, 236))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=15)
    except TypeError:
        font = ImageFont.load_default()
    for i, im in enumerate(thumbs):
        n = i + 1
        x = pad + (i % cols) * (tw + pad)
        y = pad + (i // cols) * (th + label + pad)
        sheet.paste(im.resize((tw, th)), (x, y + label))
        errs = sum(1 for s in issues if s["slide"] == n and s["severity"] == "ERROR")
        warns = sum(1 for s in issues if s["slide"] == n and s["severity"] == "WARN")
        color = (180, 30, 30) if errs else ((170, 110, 0) if warns else (40, 40, 40))
        draw.text((x, y + 4), f"Slide {n}   {errs} error / {warns} warn", fill=color, font=font)
        if errs:
            draw.rectangle([x - 3, y + label - 3, x + tw + 2, y + label + th + 2], outline=color, width=3)
    sheet.save(out_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck")
    ap.add_argument("--storyboard")
    ap.add_argument("--out-dir", default="qa")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--dpi", type=int, default=60)
    ap.add_argument("--strict", action="store_true", help="exit 1 on WARN as well as ERROR")
    a = ap.parse_args()
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    sb = json.loads(Path(a.storyboard).read_text()) if a.storyboard else None
    prs, issues, titles = check_deck(a.deck, sb)

    render_note, pngs = None, None
    if not a.no_render:
        pngs, render_note = render(a.deck, out, a.dpi)
        if pngs:
            if len(pngs) != len(prs.slides):
                issues.append(issue("ERROR", 0, "render", f"rendered {len(pngs)} pages for {len(prs.slides)} slides"))
            contact_sheet(pngs, issues, out / "contact_sheet.png")

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    issues.sort(key=lambda i: (i["slide"], order[i["severity"]]))
    counts = {k: sum(1 for i in issues if i["severity"] == k) for k in order}
    lines = [f"# QA report: {Path(a.deck).name}", "",
             f"Slides: {len(prs.slides)}   ERROR {counts['ERROR']}   WARN {counts['WARN']}   INFO {counts['INFO']}", ""]
    lines += ["## Storyline (titles only; should read as the argument)", ""]
    lines += [f"{n}. {t}" for n, t in titles] + [""]
    lines += ["## Issues", ""]
    lines += [f"- [{i['severity']}] slide {i['slide'] or '-'} {i['check']}: {i['message']}" for i in issues] or ["- none"]
    if render_note:
        lines += ["", f"Render: {render_note}"]
    elif pngs:
        lines += ["", f"Render: {len(pngs)} PNGs in {out / 'slides'}; contact sheet {out / 'contact_sheet.png'}",
                  "Open the contact sheet and look at every slide: the estimates above miss what only eyes catch."]
    report = "\n".join(lines)
    (out / "qa_report.md").write_text(report + "\n")
    (out / "qa_report.json").write_text(json.dumps({"counts": counts, "issues": issues,
                                                    "titles": titles}, indent=2))
    print(report)
    fail = counts["ERROR"] or (a.strict and counts["WARN"])
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
