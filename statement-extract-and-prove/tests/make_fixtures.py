#!/usr/bin/env python3
"""Generate synthetic statement PDFs with known answers (reportlab).

  us_checking.pdf   3 pages, MM/DD dates with no year across a Dec->Jan period, parenthesis
                    negatives, running balance printed once per day, multi-line descriptions,
                    carried/brought-forward lines at page breaks, summary box with counts
  eu_giro.pdf       German layout, 1.234,56 decimal commas, trailing-minus debits, DD.MM. dates,
                    booking + value date columns, Uebertrag lines, Summe Soll/Haben
  uk_current.pdf    Paid out / Paid in / Balance columns, '05 Jan' dates printed once per day,
                    CR/DR balance suffixes with an overdraft, totals row
  us_checking_shifted.pdf  same data, page 2 amounts printed far left of the header
  scanned.pdf       image-only copy of us_checking page 1 (no text layer)

Every fixture also writes <name>.truth.csv (the rows as printed) for comparison.
All names are fictional.

Usage: python make_fixtures.py OUTDIR
"""
import csv
import random
import subprocess
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas

C = Decimal("0.01")
MERCHANTS = ["HARBOR GROCERY #214", "CITY WATER UTILITY", "ACH PAYROLL LUMEN DESIGN LLC", "SHELL OIL 57442",
             "ONLINE TRANSFER TO SAVINGS", "CHECK 1041", "AMZN MKTP US", "RIVERSIDE PHARMACY", "PAYPAL INST XFER",
             "ZELLE FROM J MORALES", "COSTCO WHSE #0112", "VERIZON WIRELESS", "MORTGAGE PMT HOMESTEAD LOANS",
             "ATM WITHDRAWAL 4411 MAIN ST", "DEPOSIT MOBILE", "PARKING METER CITY", "INTEREST PAYMENT"]
LONG_TAIL = [["REF 8841-22 ORIG CO NAME LUMEN DESIGN", "IND ID 000417 CCD"],
             ["CONF# 7G2K91 MEMO: JANUARY RENT SHARE"],
             ["CARD 4417 PURCHASE AUTHORIZED ON 12/28", "SEQ 552190 TERMINAL 03"]]


def money_us(v):
    s = f"{abs(v):,.2f}"
    return f"({s})" if v < 0 else s


def money_eu(v, trailing=True):
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s + ("-" if v < 0 else "") if trailing else ("-" if v < 0 else "") + s


def money_crdr(v):
    return f"{abs(v):,.2f} {'DR' if v < 0 else 'CR'}"


def gen_txns(rng, start, days, n, opening, credit_bias=0.3):
    rows, bal = [], opening
    ds = sorted(start + timedelta(days=rng.randrange(days)) for _ in range(n))
    for d in ds:
        if rng.random() < credit_bias:
            amt = Decimal(rng.randrange(5000, 480000)) / 100
            desc = rng.choice(["ACH PAYROLL LUMEN DESIGN LLC", "DEPOSIT MOBILE", "ZELLE FROM J MORALES",
                               "PAYPAL INST XFER", "INTEREST PAYMENT"])
        else:
            amt = -Decimal(rng.randrange(250, 260000)) / 100
            desc = rng.choice([m for m in MERCHANTS if m not in ("DEPOSIT MOBILE", "INTEREST PAYMENT")])
        extra = rng.choice(LONG_TAIL) if rng.random() < 0.25 else []
        bal += amt
        rows.append({"date": d, "desc": desc, "extra": extra, "amount": amt, "balance": bal})
    return rows


class Doc:
    def __init__(self, path, size=letter):
        self.c = canvas.Canvas(str(path), pagesize=size)
        self.w, self.h = size
        self.page = 1

    def text(self, x, y, s, size=8.5, bold=False, align="left"):
        self.c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        {"left": self.c.drawString, "right": self.c.drawRightString}[align](x, y, s)

    def new_page(self):
        self.c.showPage()
        self.page += 1

    def save(self):
        self.c.save()


# ------------------------------------------------------------------ US checking

def us_checking(out, shifted=False):
    """shifted=True prints page 2 amounts 140pt left of their header (a template quirk)."""
    rng = random.Random(7)
    opening = Decimal("4210.33")
    start, end = date(2025, 12, 15), date(2026, 1, 14)
    txns = gen_txns(rng, start, 31, 44, opening, credit_bias=0.42)
    closing = txns[-1]["balance"]
    cr = [t for t in txns if t["amount"] > 0]
    dr = [t for t in txns if t["amount"] < 0]
    name = "us_checking_shifted" if shifted else "us_checking"
    doc = Doc(out / f"{name}.pdf")
    cols = {"date": 50, "desc": 100, "amount": 470, "balance": 560}

    def head(first):
        doc.text(50, 760, "NORTHBRIDGE COMMUNITY BANK", 12, True)
        doc.text(50, 746, "Everyday Checking  |  Account ending 4417")
        doc.text(560, 760, "Statement period: 12/15/2025 - 01/14/2026", align="right")
        y = 720
        if first:
            doc.text(50, 715, "Account summary", 10, True)
            lines = [("Beginning balance on 12/15/2025", "$" + money_us(opening)),
                     (f"Deposits and other credits ({len(cr)})", money_us(sum(t['amount'] for t in cr))),
                     (f"Withdrawals and other debits ({len(dr)})", "-" + money_us(-sum(t['amount'] for t in dr))),
                     ("Ending balance on 01/14/2026", "$" + money_us(closing)),
                     ("Number of transactions", str(len(txns)))]
            for i, (k, v) in enumerate(lines):
                doc.text(60, 700 - i * 12, k)
                doc.text(330, 700 - i * 12, v, align="right")
            y = 620
        doc.text(cols["date"], y, "Date", bold=True)
        doc.text(cols["desc"], y, "Description", bold=True)
        doc.text(cols["amount"], y, "Amount", bold=True, align="right")
        doc.text(cols["balance"], y, "Balance", bold=True, align="right")
        return y - 16

    def foot(total_pages=3):
        doc.text(50, 40, "Member FDIC. Questions? Call 1-800-555-0142.", 7)
        doc.text(560, 40, f"Page {doc.page} of {total_pages}", 7, align="right")

    y = head(True)
    doc.text(cols["desc"], y, "Balance brought forward")
    doc.text(cols["balance"], y, money_us(opening), align="right")
    y -= 13
    per_page = [16, 17, 99]
    idx, on_page = 0, 0
    for i, t in enumerate(txns):
        if on_page >= per_page[doc.page - 1]:
            doc.text(cols["desc"], y, "Balance carried forward")
            doc.text(cols["balance"], y, money_us(txns[i - 1]["balance"]), align="right")
            foot()
            doc.new_page()
            y = head(False)
            doc.text(cols["desc"], y, "Balance brought forward")
            doc.text(cols["balance"], y, money_us(txns[i - 1]["balance"]), align="right")
            y -= 13
            on_page = 0
        last_of_day = i == len(txns) - 1 or txns[i + 1]["date"] != t["date"] or on_page + 1 >= per_page[doc.page - 1]
        doc.text(cols["date"], y, t["date"].strftime("%m/%d"))
        doc.text(cols["desc"], y, t["desc"])
        ax = cols["amount"] - (140 if shifted and doc.page == 2 else 0)
        doc.text(ax, y, money_us(t["amount"]), align="right")
        if last_of_day:
            doc.text(cols["balance"], y, money_us(t["balance"]), align="right")
        y -= 11
        for e in t["extra"]:
            doc.text(cols["desc"] + 8, y, e, 7.5)
            y -= 10
        y -= 2
        on_page += 1
    doc.text(cols["desc"], y - 4, "Ending balance", bold=True)
    doc.text(cols["balance"], y - 4, money_us(closing), bold=True, align="right")
    foot()
    doc.save()
    write_truth(out / f"{name}.truth.csv", txns)
    return {"opening": opening, "closing": closing, "rows": len(txns)}


# ------------------------------------------------------------------ EU giro (German)

def eu_giro(out):
    rng = random.Random(11)
    opening = Decimal("12345.67")
    txns = gen_txns(rng, date(2026, 3, 1), 31, 30, opening, credit_bias=0.35)
    for t in txns:
        t["desc"] = rng.choice(["SEPA-Lastschrift Stadtwerke Aachen", "Kartenzahlung REWE Markt 0412",
                                "Dauerauftrag Miete", "Überweisung an L. Becker", "Bargeldauszahlung GAA 5521"]) \
            if t["amount"] < 0 else rng.choice(["Gehalt Firma Krause GmbH", "Gutschrift Rückerstattung"])
        t["extra"] = ["Mandatsref. KR-20260301-77 Gläubiger-ID DE98ZZZ09999999999"] if rng.random() < 0.3 else []
    closing = txns[-1]["balance"]
    doc = Doc(out / "eu_giro.pdf", A4)
    W, H = A4
    cols = {"bt": 40, "wert": 100, "desc": 155, "betrag": 470, "saldo": 555}
    soll = -sum(t["amount"] for t in txns if t["amount"] < 0)
    haben = sum(t["amount"] for t in txns if t["amount"] > 0)

    def head(first):
        doc.text(40, H - 50, "Stadtsparkasse Kleinheim", 12, True)
        doc.text(40, H - 64, "Girokonto  IBAN DE00 1234 5678 0000 1234 56")
        doc.text(555, H - 50, "Kontoauszug 3/2026", align="right")
        doc.text(555, H - 64, "Zeitraum: 01.03.2026 bis 31.03.2026", align="right")
        y = H - 100
        if first:
            doc.text(40, y, "Alter Saldo", bold=True)
            doc.text(300, y, money_eu(opening), bold=True, align="right")
            y -= 30
        for k, x, al in (("Buchungstag", "bt", "left"), ("Wert", "wert", "left"), ("Verwendungszweck", "desc", "left"),
                         ("Betrag", "betrag", "right"), ("Saldo", "saldo", "right")):
            doc.text(cols[x], y, k, bold=True, align=al)
        return y - 16

    y = head(True)
    for i, t in enumerate(txns):
        if i == 17:
            doc.text(cols["desc"], y, "Übertrag auf Blatt 2")
            doc.text(cols["saldo"], y, money_eu(txns[i - 1]["balance"]), align="right")
            doc.text(555, 30, "Seite 1 von 2", 7, align="right")
            doc.new_page()
            y = head(False)
            doc.text(cols["desc"], y, "Übertrag von Blatt 1")
            doc.text(cols["saldo"], y, money_eu(txns[i - 1]["balance"]), align="right")
            y -= 13
        doc.text(cols["bt"], y, t["date"].strftime("%d.%m."))
        doc.text(cols["wert"], y, t["date"].strftime("%d.%m.%Y"))
        doc.text(cols["desc"], y, t["desc"])
        doc.text(cols["betrag"], y, money_eu(t["amount"]), align="right")
        doc.text(cols["saldo"], y, money_eu(t["balance"]), align="right")
        y -= 11
        for e in t["extra"]:
            doc.text(cols["desc"], y, e, 7.5)
            y -= 10
        y -= 2
    y -= 6
    doc.text(cols["desc"], y, "Summe Soll")
    doc.text(cols["betrag"], y, money_eu(soll), align="right")
    doc.text(cols["desc"], y - 12, "Summe Haben")
    doc.text(cols["betrag"], y - 12, money_eu(haben), align="right")
    doc.text(cols["desc"], y - 26, "Neuer Saldo", bold=True)
    doc.text(cols["saldo"], y - 26, money_eu(closing), bold=True, align="right")
    doc.text(555, 30, "Seite 2 von 2", 7, align="right")
    doc.save()
    write_truth(out / "eu_giro.truth.csv", txns)
    return {"opening": opening, "closing": closing, "rows": len(txns)}


# ------------------------------------------------------------------ UK current (paid out / paid in)

def uk_current(out):
    rng = random.Random(5)
    opening = Decimal("1050.00")
    txns = gen_txns(rng, date(2026, 1, 1), 31, 34, opening, credit_bias=0.2)
    closing = txns[-1]["balance"]
    doc = Doc(out / "uk_current.pdf", A4)
    W, H = A4
    cols = {"date": 40, "desc": 95, "out": 400, "in": 475, "bal": 555}
    paid_out = -sum(t["amount"] for t in txns if t["amount"] < 0)
    paid_in = sum(t["amount"] for t in txns if t["amount"] > 0)

    def head(first):
        doc.text(40, H - 50, "Fenwick & Hale Bank plc", 12, True)
        doc.text(40, H - 64, "Current Account  Sort code 00-00-00  Account 01234567")
        doc.text(555, H - 50, "Period: 1 January 2026 to 31 January 2026", align="right")
        y = H - 95
        if first:
            for i, (k, v) in enumerate([("Opening balance", money_crdr(opening)), ("Total paid out", f"{paid_out:,.2f}"),
                                        ("Total paid in", f"{paid_in:,.2f}"), ("Closing balance", money_crdr(closing))]):
                doc.text(40, y - i * 12, k)
                doc.text(300, y - i * 12, v, align="right")
            y -= 70
        doc.text(cols["date"], y, "Date", bold=True)
        doc.text(cols["desc"], y, "Description", bold=True)
        doc.text(cols["out"], y, "Paid out", bold=True, align="right")
        doc.text(cols["in"], y, "Paid in", bold=True, align="right")
        doc.text(cols["bal"], y, "Balance", bold=True, align="right")
        return y - 16

    y = head(True)
    doc.text(cols["desc"], y, "Balance brought forward")
    doc.text(cols["bal"], y, money_crdr(opening), align="right")
    y -= 13
    prev_date = None
    for i, t in enumerate(txns):
        if i == 20:
            doc.text(cols["desc"], y, "Balance carried forward")
            doc.text(cols["bal"], y, money_crdr(txns[i - 1]["balance"]), align="right")
            doc.text(W / 2, 30, "Page 1 of 2", 7)
            doc.new_page()
            y = head(False)
            doc.text(cols["desc"], y, "Balance brought forward")
            doc.text(cols["bal"], y, money_crdr(txns[i - 1]["balance"]), align="right")
            y -= 13
            prev_date = None
        if t["date"] != prev_date:
            doc.text(cols["date"], y, t["date"].strftime("%d %b"))
        prev_date = t["date"]
        doc.text(cols["desc"], y, t["desc"])
        col = "out" if t["amount"] < 0 else "in"
        doc.text(cols[col], y, f"{abs(t['amount']):,.2f}", align="right")
        doc.text(cols["bal"], y, money_crdr(t["balance"]), align="right")
        y -= 11
        for e in t["extra"]:
            doc.text(cols["desc"], y, e, 7.5)
            y -= 10
        y -= 2
    doc.text(cols["desc"], y - 4, "Totals", bold=True)
    doc.text(cols["out"], y - 4, f"{paid_out:,.2f}", bold=True, align="right")
    doc.text(cols["in"], y - 4, f"{paid_in:,.2f}", bold=True, align="right")
    doc.text(W / 2, 30, "Page 2 of 2", 7)
    doc.save()
    write_truth(out / "uk_current.truth.csv", txns)
    return {"opening": opening, "closing": closing, "rows": len(txns)}


def scanned(out):
    """Rasterize page 1 of us_checking and wrap the image in a PDF: no text layer."""
    png = out / "scan_p1"
    subprocess.run(["pdftoppm", "-r", "110", "-f", "1", "-l", "1", "-png", "-singlefile",
                    str(out / "us_checking.pdf"), str(png)], check=True)
    c = canvas.Canvas(str(out / "scanned.pdf"), pagesize=letter)
    c.drawImage(str(png) + ".png", 0, 0, *letter)
    c.save()


def write_truth(path, txns):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "description", "amount", "balance"])
        for t in txns:
            w.writerow([t["date"].isoformat(), " ".join([t["desc"]] + t["extra"]), f"{t['amount']:.2f}",
                        f"{t['balance']:.2f}"])


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "fixtures")
    out.mkdir(parents=True, exist_ok=True)
    for fn in (us_checking, eu_giro, uk_current):
        info = fn(out)
        print(f"{fn.__name__}: {info['rows']} rows, opening {info['opening']}, closing {info['closing']}")
    us_checking(out, shifted=True)
    print("us_checking_shifted: same rows, page 2 amount column misaligned")
    scanned(out)
    print(f"scanned.pdf written (image only) -> {out}")
