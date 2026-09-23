#!/usr/bin/env python3
"""Deterministic bank-statement vs ledger reconciliation.

Normalizes two exports (bank statement lines, and the ledger/register for the
same account), matches them in tiers, classifies every unmatched line, and
produces a two-sided reconciliation proof:

    adjusted bank = statement ending balance + deposits in transit - outstanding payments
    adjusted book = book ending balance + items on the statement not yet in the books
                    - duplicate book entries + amount corrections
    unexplained variance = adjusted bank - adjusted book   (must be 0.00)

The script never plugs a difference. A non-zero variance is reported and the
process exits with code 2.

Sign convention after normalization: amount = change to the balance the
statement reports. Bank account: deposit +, withdrawal -. Credit card: use
--account-type card; the statement proof fixes the orientation of the bank
file and the ledger is aligned to it.

Usage:
  python reconcile.py --bank bank.csv --ledger ledger.csv \
      --period-start 2026-08-01 --period-end 2026-08-31 \
      --statement-begin 25000.00 --statement-end 21000.00 \
      --book-begin 23800.00 [--book-end ...] --out out/

Exit codes: 0 balanced, 2 unexplained variance, 3 statement lines do not
roll from beginning to ending balance (incomplete export or bad balances),
4 input error.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

CENT = 0.005  # tolerance for float equality on money

DATE_COLS = ["date", "transaction date", "posted date", "posting date", "trans date",
             "txn date", "value date", "booking date"]
DESC_COLS = ["description", "memo", "memo/description", "payee", "name", "details",
             "transaction description", "narrative", "reference", "counterpartyname"]
AMOUNT_COLS = ["amount", "amt", "net amount", "transaction amount"]
IN_COLS = ["credit", "credits", "deposit", "deposits", "money in", "received", "inflow",
           "receive", "paid in"]
OUT_COLS = ["debit", "debits", "withdrawal", "withdrawals", "money out", "spent", "outflow",
            "payment", "payments", "spend", "paid out"]
CATEGORY_COLS = ["category", "split", "account code", "gl account", "account", "class"]
NUM_COLS = ["num", "no.", "check no", "check number", "check #", "ref no", "doc number"]

FEE_RE = re.compile(r"\b(FEE|SERVICE CHARGE|MAINT(ENANCE)?|OVERDRAFT|NSF|ANALYSIS CHARGE)\b")
INTEREST_RE = re.compile(r"\bINTEREST\b")
TRANSFER_RE = re.compile(r"\b(TRANSFER|XFER|TRNSFR|TO SAVINGS|FROM SAVINGS|TO CHECKING|"
                         r"FROM CHECKING|EPAYMENT|AUTOPAY|CARD PAYMENT|PAYMENT THANK YOU|"
                         r"SWEEP)\b")
CHECK_RE = re.compile(r"\b(?:CHECK|CHK|CK)\s*#?\s*(\d{3,})\b")
NOISE_RE = re.compile(r"\b(POS|ACH|DEBIT|CREDIT|PURCHASE|CARD|WEB|PPD|CCD|ONLINE|ID|"
                      r"X{2,}\d*|\d{5,})\b")
PL_CATEGORY_RE = re.compile(r"(INCOME|SALES|REVENUE|EXPENSE|COST|UNCATEGORI[SZ]ED|"
                            r"ASK MY ACCOUNTANT|SUSPENSE)", re.I)
REVIEW_CATEGORY_RE = re.compile(r"(UNCATEGORI[SZ]ED|ASK MY ACCOUNTANT|SUSPENSE)", re.I)


# ---------------------------------------------------------------- parsing

def parse_money(v) -> float | None:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    s = str(v).strip()
    if s == "" or s.lower() in {"nan", "none"}:
        return None
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg, s = True, s[1:-1]
    if s.endswith("-"):
        neg, s = True, s[:-1]
    up = s.upper()
    if up.endswith(" CR"):
        s = s[:-3]
    elif up.endswith(" DR"):
        neg, s = True, s[:-3]
    s = re.sub(r"[^\d.\-]", "", s)
    if s in {"", "-", "."}:
        return None
    x = float(s)
    return -abs(x) if neg else x


def find_col(cols: dict[str, str], names: list[str]) -> str | None:
    for n in names:
        if n in cols:
            return cols[n]
    return None


def load(path: str, role: str, account_type: str, date_format: str | None) -> tuple[pd.DataFrame, str]:
    """Return (normalized frame, description of how signs were read)."""
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    cols = {c.strip().lower(): c for c in raw.columns}
    dcol = find_col(cols, DATE_COLS)
    if not dcol:
        raise ValueError(f"{path}: no date column (looked for {DATE_COLS})")
    desc = find_col(cols, DESC_COLS)
    cat = find_col(cols, CATEGORY_COLS) if role == "ledger" else None
    num = find_col(cols, NUM_COLS)
    amt = find_col(cols, AMOUNT_COLS)
    incol, outcol = find_col(cols, IN_COLS), find_col(cols, OUT_COLS)

    if amt:
        amounts = raw[amt].map(parse_money)
        how = f"single signed column '{amt}'"
    elif incol and outcol:
        a_in = raw[incol].map(parse_money).fillna(0).abs()
        a_out = raw[outcol].map(parse_money).fillna(0).abs()
        gl_style = incol.strip().lower().startswith("credit") and outcol.strip().lower().startswith("debit")
        if role == "ledger" and gl_style:
            # General-ledger detail: for an asset (bank) account a DEBIT increases the
            # balance; for a liability (card) a CREDIT increases the balance owed.
            if account_type == "bank":
                amounts, how = a_out - a_in, "GL columns: debit = money in (asset account)"
            else:
                amounts, how = a_in - a_out, "GL columns: credit = charge (liability account)"
        else:
            # Statement / register view: 'debit'/'withdrawal' means money leaving the account.
            if account_type == "bank":
                amounts, how = a_in - a_out, f"'{incol}' = in, '{outcol}' = out"
            else:
                amounts, how = a_out - a_in, f"'{outcol}' = charge, '{incol}' = payment/credit"
    else:
        raise ValueError(f"{path}: need an Amount column or a pair of in/out columns")

    df = pd.DataFrame({
        "src_row": range(2, len(raw) + 2),  # spreadsheet row number incl. header
        "date": pd.to_datetime(raw[dcol], format=date_format, errors="coerce"),
        "description": raw[desc].fillna("") if desc else "",
        "amount": amounts.round(2),
    })
    df["category"] = raw[cat] if cat else ""
    df["num"] = raw[num] if num else ""
    bad = df["date"].isna() | df["amount"].isna()
    if bad.any():
        print(f"WARNING {path}: dropped {int(bad.sum())} rows with unreadable date/amount "
              f"(rows {df.loc[bad, 'src_row'].tolist()[:10]})", file=sys.stderr)
    df = df[~bad].copy()
    df["norm"] = df["description"].map(norm_desc)
    df["check_no"] = [extract_check(d, n) for d, n in zip(df["description"], df["num"])]
    df["side"] = role
    df["id"] = [f"{role[0].upper()}{i:04d}" for i in range(1, len(df) + 1)]
    return df.reset_index(drop=True), how


def norm_desc(s: str) -> str:
    s = re.sub(r"[^A-Z0-9 ]", " ", str(s).upper())
    s = NOISE_RE.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def extract_check(desc: str, num: str) -> str:
    m = CHECK_RE.search(str(desc).upper())
    if m:
        return m.group(1).lstrip("0")
    n = str(num).strip()
    return n.lstrip("0") if n.isdigit() and len(n) >= 3 else ""


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    ta, tb = set(a.split()), set(b.split())
    jac = len(ta & tb) / len(ta | tb) if ta | tb else 0.0
    return round(max(SequenceMatcher(None, a, b).ratio(), jac), 3)


# ---------------------------------------------------------------- matching

class Matcher:
    def __init__(self, bank: pd.DataFrame, ledger: pd.DataFrame, window: int, lead: int,
                 tol: float, min_sim: float):
        self.b, self.l = bank, ledger
        self.window, self.lead, self.tol, self.min_sim = window, lead, tol, min_sim
        self.bank_free = set(bank.index)
        self.led_free = set(ledger.index)
        self.matches: list[dict] = []
        self.period_start = None

    def in_window(self, bdate, ldate) -> bool:
        # Bank clears on or after the book date (checks lag); allow a small lead for
        # items booked late (e.g. card charges entered after posting).
        delta = (bdate - ldate).days
        return -self.lead <= delta <= self.window

    def record(self, bidx: list[int], lidx: list[int], tier: str, note: str = ""):
        if self.period_start is not None and (self.l.loc[lidx, "date"] < self.period_start).any():
            note = (note + "; " if note else "") + "prior-period outstanding item, cleared this period"
        bsum = round(self.b.loc[bidx, "amount"].sum(), 2)
        lsum = round(self.l.loc[lidx, "amount"].sum(), 2)
        sim = similarity(" ".join(self.b.loc[bidx, "norm"]), " ".join(self.l.loc[lidx, "norm"]))
        self.matches.append({
            "tier": tier,
            "bank_ids": ",".join(self.b.loc[bidx, "id"]),
            "ledger_ids": ",".join(self.l.loc[lidx, "id"]),
            "bank_date": self.b.loc[bidx[0], "date"].date().isoformat(),
            "ledger_date": self.l.loc[lidx[0], "date"].date().isoformat(),
            "bank_description": " + ".join(self.b.loc[bidx, "description"]),
            "ledger_description": " + ".join(self.l.loc[lidx, "description"]),
            "bank_amount": bsum, "ledger_amount": lsum,
            "variance": round(bsum - lsum, 2), "similarity": sim,
            "ledger_category": " + ".join(self.l.loc[lidx, "category"].astype(str)),
            "note": note,
        })
        self.bank_free -= set(bidx)
        self.led_free -= set(lidx)

    def one_to_one(self, tier: str, cond, need_sim: bool, allow_variance: bool):
        for bi in sorted(self.bank_free, key=lambda i: (self.b.at[i, "date"], i)):
            if bi not in self.bank_free:
                continue
            brow = self.b.loc[bi]
            cands = []
            for li in self.led_free:
                lrow = self.l.loc[li]
                if not cond(brow, lrow):
                    continue
                sim = similarity(brow["norm"], lrow["norm"])
                if need_sim and sim < self.min_sim:
                    continue
                cands.append((abs((brow["date"] - lrow["date"]).days), -sim, li))
            if not cands:
                continue
            cands.sort()
            li = cands[0][2]
            note = ""
            if len(cands) > 1 and cands[0][:2] == cands[1][:2]:
                note = f"ambiguous: {len(cands)} equal candidates, confirm pairing"
            diff = round(brow["amount"] - self.l.at[li, "amount"], 2)
            if abs(diff) > CENT and allow_variance:
                note = (note + "; " if note else "") + f"amount differs by {diff:+.2f}"
                if round(abs(diff) * 100) % 9 == 0:
                    note += " (divisible by 9: likely transposed digits)"
            self.record([bi], [li], tier, note)

    def many_to_one(self, max_parts: int = 4, pool_cap: int = 18):
        """One line on one side equals the sum of 2..max_parts lines on the other
        (batched deposits, split payments). Exact cents only."""
        for one_side, many_side in (("bank", "ledger"), ("ledger", "bank")):
            one_df = self.b if one_side == "bank" else self.l
            many_df = self.l if one_side == "bank" else self.b
            for oi in sorted(self.bank_free if one_side == "bank" else self.led_free):
                free_many = self.led_free if one_side == "bank" else self.bank_free
                if oi not in (self.bank_free if one_side == "bank" else self.led_free):
                    continue
                o = one_df.loc[oi]
                pool = []
                for mi in free_many:
                    m = many_df.loc[mi]
                    if (m["amount"] > 0) != (o["amount"] > 0):
                        continue
                    bdate, ldate = (o["date"], m["date"]) if one_side == "bank" else (m["date"], o["date"])
                    if self.in_window(bdate, ldate):
                        pool.append(mi)
                pool = sorted(pool)[:pool_cap]
                found = None
                for k in range(2, max_parts + 1):
                    for combo in itertools.combinations(pool, k):
                        if abs(many_df.loc[list(combo), "amount"].sum() - o["amount"]) < CENT:
                            found = list(combo)
                            break
                    if found:
                        break
                if found:
                    if one_side == "bank":
                        self.record([oi], found, "grouped", f"1 bank line = {len(found)} ledger lines (batched deposit/split)")
                    else:
                        self.record(found, [oi], "grouped", f"{len(found)} bank lines = 1 ledger line")

    def run(self):
        same_amt = lambda b, l: abs(b["amount"] - l["amount"]) < CENT
        self.one_to_one("exact", lambda b, l: same_amt(b, l) and b["date"] == l["date"], False, False)
        self.one_to_one("check_no", lambda b, l: b["check_no"] != "" and b["check_no"] == l["check_no"], False, True)
        self.one_to_one("amount_date_window", lambda b, l: same_amt(b, l) and self.in_window(b["date"], l["date"]), False, False)
        self.one_to_one("fuzzy", lambda b, l: abs(b["amount"] - l["amount"]) <= self.tol + CENT
                        and (b["amount"] > 0) == (l["amount"] > 0)
                        and self.in_window(b["date"], l["date"]), True, True)
        self.many_to_one()
        return pd.DataFrame(self.matches)


# ---------------------------------------------------------------- classification

def classify_ledger(led: pd.DataFrame, free: set, matched_ids: set, period_start, period_end,
                    stale_days: int) -> pd.DataFrame:
    rows = []
    matched = led[led["id"].isin(matched_ids)]
    for li in sorted(free):
        r = led.loc[li]
        dup_of = ""
        for _, m in matched.iterrows():
            if abs(m["amount"] - r["amount"]) < CENT and abs((m["date"] - r["date"]).days) <= 3 \
                    and similarity(m["norm"], r["norm"]) >= 0.8:
                dup_of = m["id"]
                break
        if dup_of:
            cls, side = "BOOK_DUPLICATE", "book"
            action = f"Likely double entry of {dup_of} (feed + manual/CSV import). Delete or void one after confirming."
        elif r["amount"] > 0:
            cls, side = "DEPOSIT_IN_TRANSIT", "bank"
            action = "Confirm it clears in the first days of next statement; if not, investigate."
        else:
            cls, side = "OUTSTANDING_PAYMENT", "bank"
            action = "Outstanding check/payment. Confirm it clears next period."
        age = (period_end - r["date"]).days
        if side == "bank" and age > stale_days:
            cls += "_STALE"
            action = f"{age} days old. Contact payee/payer; possible void, reissue, or unclaimed property. Accountant review."
        rows.append({**base_row(r), "class": cls, "adjusts": side, "action": action})
    return pd.DataFrame(rows)


def classify_bank(bank: pd.DataFrame, free: set) -> pd.DataFrame:
    rows = []
    for bi in sorted(free):
        r = bank.loc[bi]
        up = str(r["description"]).upper()
        if FEE_RE.search(up):
            cls, action = "BANK_FEE_NOT_IN_BOOKS", "Record as bank service charges (expense)."
        elif INTEREST_RE.search(up) and r["amount"] > 0:
            cls, action = "INTEREST_NOT_IN_BOOKS", "Record as interest income."
        elif TRANSFER_RE.search(up):
            cls, action = "TRANSFER_NOT_IN_BOOKS", ("Record as a transfer to/from the other own account "
                                                   "(balance sheet), never income/expense. Check the other "
                                                   "account's books for the matching leg.")
        else:
            cls, action = "NOT_IN_BOOKS", "Find source document; record it or dispute with the bank."
        rows.append({**base_row(r), "class": cls, "adjusts": "book", "action": action})
    return pd.DataFrame(rows)


def base_row(r) -> dict:
    return {"id": r["id"], "src_row": int(r["src_row"]), "date": r["date"].date().isoformat(),
            "description": r["description"], "amount": float(r["amount"]),
            "category": r.get("category", "")}


def exceptions(bank, led, matches) -> list[dict]:
    out = []
    # Identical statement lines: could be a real repeat purchase or an overlapping re-download.
    key = bank[["date", "amount", "norm"]].astype(str).agg("|".join, axis=1)
    for k, g in bank.groupby(key):
        if len(g) > 1:
            out.append({"type": "IDENTICAL_STATEMENT_LINES", "ids": ",".join(g["id"]),
                        "detail": f"{len(g)} identical lines {k}. Confirm against the PDF statement; "
                                  "delete only proven import duplicates."})
    # Transfers booked to P&L accounts double count income/expense.
    if not matches.empty:
        for _, m in matches.iterrows():
            if TRANSFER_RE.search(str(m["bank_description"]).upper()) and \
                    PL_CATEGORY_RE.search(str(m["ledger_category"])):
                out.append({"type": "TRANSFER_BOOKED_TO_PL", "ids": f"{m['bank_ids']}/{m['ledger_ids']}",
                            "detail": f"'{m['bank_description']}' categorized to '{m['ledger_category']}'. "
                                      "Own-account transfers and card payments belong on the balance sheet."})
            if m["note"].startswith("ambiguous"):
                out.append({"type": "AMBIGUOUS_MATCH", "ids": f"{m['bank_ids']}/{m['ledger_ids']}",
                            "detail": m["note"]})
    for _, r in led.iterrows():
        if REVIEW_CATEGORY_RE.search(str(r["category"])):
            out.append({"type": "NEEDS_CATEGORY", "ids": r["id"],
                        "detail": f"'{r['description']}' {r['amount']:.2f} sits in '{r['category']}'."})
    return out


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bank", required=True, help="statement lines CSV (bank/card export, Mercury, OFX->CSV)")
    ap.add_argument("--ledger", required=True, help="ledger/register CSV for the same account, "
                    "including uncleared items from prior periods")
    ap.add_argument("--period-start", required=True)
    ap.add_argument("--period-end", required=True)
    ap.add_argument("--statement-begin", type=float, required=True)
    ap.add_argument("--statement-end", type=float, required=True)
    ap.add_argument("--book-begin", type=float, help="book balance at period start")
    ap.add_argument("--book-end", type=float, help="book balance at period end (overrides --book-begin)")
    ap.add_argument("--account-type", choices=["bank", "card"], default="bank")
    ap.add_argument("--window", type=int, default=10, help="days a bank line may trail the book date")
    ap.add_argument("--lead", type=int, default=3, help="days a bank line may precede the book date")
    ap.add_argument("--tolerance", type=float, default=1.00, help="max amount gap for fuzzy matches")
    ap.add_argument("--min-sim", type=float, default=0.5, help="description similarity for fuzzy matches")
    ap.add_argument("--stale-days", type=int, default=90)
    ap.add_argument("--date-format", default=None, help="strftime format if dates are ambiguous, e.g. %%d/%%m/%%Y")
    ap.add_argument("--no-auto-flip", action="store_true", help="never invert ledger signs automatically")
    ap.add_argument("--out", default="recon_out")
    a = ap.parse_args(argv)

    try:
        bank, bank_how = load(a.bank, "bank", a.account_type, a.date_format)
        led, led_how = load(a.ledger, "ledger", a.account_type, a.date_format)
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 4
    ps, pe = pd.Timestamp(a.period_start), pd.Timestamp(a.period_end)
    notes = [f"bank signs: {bank_how}", f"ledger signs: {led_how}"]

    out_of_period_bank = bank[(bank["date"] < ps) | (bank["date"] > pe)]
    bank = bank[(bank["date"] >= ps) & (bank["date"] <= pe)]
    future_led = led[led["date"] > pe]
    led = led[led["date"] <= pe]
    if len(out_of_period_bank):
        notes.append(f"excluded {len(out_of_period_bank)} statement lines outside the period")
    if len(future_led):
        notes.append(f"excluded {len(future_led)} ledger lines dated after period end")

    # 1. Statement continuity: beginning + lines must equal ending. If only the inverted
    #    sign works, the export uses the opposite convention; flip it and say so.
    roll = round(a.statement_begin + bank["amount"].sum(), 2)
    if abs(roll - a.statement_end) > CENT:
        if abs(round(a.statement_begin - bank["amount"].sum(), 2) - a.statement_end) < CENT:
            bank["amount"] = -bank["amount"]
            roll = a.statement_end
            notes.append("bank file signs were inverted relative to the statement balances; flipped")
        else:
            print(f"STOP: statement lines do not roll forward. {a.statement_begin:,.2f} + lines "
                  f"{bank['amount'].sum():,.2f} = {roll:,.2f}, statement says {a.statement_end:,.2f} "
                  f"(gap {a.statement_end - roll:+,.2f}). The export is incomplete, overlaps another "
                  "period, contains duplicates, or the balances are wrong. Fix inputs before matching.",
                  file=sys.stderr)
            return 3

    # 2. Ledger orientation: if flipping the ledger sign produces far more exact matches,
    #    the ledger was exported from the opposite perspective.
    bank_amts = set(bank["amount"].round(2))
    as_is = led["amount"].round(2).isin(bank_amts).sum()
    flipped = (-led["amount"]).round(2).isin(bank_amts).sum()
    if flipped >= 3 and flipped > 2 * as_is:
        if a.no_auto_flip:
            notes.append(f"WARNING ledger signs look inverted ({flipped} vs {as_is} amount hits); not flipped")
        else:
            led["amount"] = -led["amount"]
            if a.book_begin is not None:
                a.book_begin = -a.book_begin
            if a.book_end is not None:
                a.book_end = -a.book_end
            notes.append(f"ledger signs inverted ({flipped} vs {as_is} amount hits); flipped ledger "
                         "and book balances. Confirm the account type is right.")

    led = led.reset_index(drop=True)
    bank = bank.reset_index(drop=True)
    m = Matcher(bank, led, a.window, a.lead, a.tolerance, a.min_sim)
    m.period_start = ps
    matches = m.run()
    matched_led_ids = set(",".join(matches["ledger_ids"]).split(",")) if not matches.empty else set()

    ul = classify_ledger(led, m.led_free, matched_led_ids, ps, pe, a.stale_days)
    ub = classify_bank(bank, m.bank_free)

    # 3. Book balance at period end.
    in_period_led = led[led["date"] >= ps]["amount"].sum()
    if a.book_end is not None:
        book_end = a.book_end
    elif a.book_begin is not None:
        book_end = round(a.book_begin + in_period_led, 2)
    else:
        book_end = round(a.statement_begin + in_period_led, 2)
        notes.append("WARNING no book balance given; assumed book beginning = statement beginning "
                     "(true only if there were no prior-period outstanding items)")

    def s(df, mask):
        return round(float(df.loc[mask, "amount"].sum()), 2) if len(df) else 0.0

    dit = s(ul, ul["class"].str.startswith("DEPOSIT_IN_TRANSIT")) if len(ul) else 0.0
    osp = s(ul, ul["class"].str.startswith("OUTSTANDING_PAYMENT")) if len(ul) else 0.0
    dups = s(ul, ul["class"] == "BOOK_DUPLICATE") if len(ul) else 0.0
    not_in_books = round(float(ub["amount"].sum()), 2) if len(ub) else 0.0
    amt_corr = round(float(matches["variance"].sum()), 2) if not matches.empty else 0.0

    adj_bank = round(a.statement_end + dit + osp, 2)
    adj_book = round(book_end + not_in_books - dups + amt_corr, 2)
    variance = round(adj_bank - adj_book, 2)

    exc = exceptions(bank, led, matches)
    summary = {
        "period": f"{a.period_start} to {a.period_end}",
        "account_type": a.account_type,
        "counts": {"statement_lines": len(bank), "ledger_lines": len(led),
                   "matched_groups": len(matches),
                   "matched_by_tier": matches["tier"].value_counts().to_dict() if not matches.empty else {},
                   "unmatched_bank": len(ub), "unmatched_ledger": len(ul)},
        "bank_side": {"statement_beginning": a.statement_begin, "statement_lines_total": round(float(bank["amount"].sum()), 2),
                      "statement_ending": a.statement_end, "rolls_forward": True,
                      "plus_deposits_in_transit": dit, "less_outstanding_payments": osp,
                      "adjusted_bank_balance": adj_bank},
        "book_side": {"book_ending": book_end, "plus_items_not_in_books": not_in_books,
                      "less_duplicate_book_entries": round(-dups, 2),
                      "plus_amount_corrections": amt_corr, "adjusted_book_balance": adj_book},
        "unexplained_variance": variance,
        "balanced": abs(variance) < CENT,
        "notes": notes,
        "exceptions": exc,
    }

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    matches.to_csv(out / "matched.csv", index=False)
    ub.to_csv(out / "unmatched_bank.csv", index=False)
    ul.to_csv(out / "unmatched_ledger.csv", index=False)
    pd.DataFrame(exc).to_csv(out / "exceptions.csv", index=False)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    report = render(summary, ub, ul, matches)
    (out / "reconciliation.md").write_text(report)
    print(report)
    return 0 if summary["balanced"] else 2


def render(sm, ub, ul, matches) -> str:
    b, k = sm["bank_side"], sm["book_side"]
    f = lambda x: f"{x:>14,.2f}"
    lines = [f"# Bank reconciliation {sm['period']}", "",
             "## Proof", "```",
             f"Statement beginning balance      {f(b['statement_beginning'])}",
             f"  + statement lines (net)         {f(b['statement_lines_total'])}",
             f"Statement ending balance         {f(b['statement_ending'])}   rolls forward: yes",
             f"  + deposits in transit           {f(b['plus_deposits_in_transit'])}",
             f"  + outstanding payments (neg)    {f(b['less_outstanding_payments'])}",
             f"Adjusted bank balance            {f(b['adjusted_bank_balance'])}",
             "",
             f"Book ending balance              {f(k['book_ending'])}",
             f"  + items not yet in books        {f(k['plus_items_not_in_books'])}",
             f"  - duplicate book entries        {f(k['less_duplicate_book_entries'])}",
             f"  + amount corrections            {f(k['plus_amount_corrections'])}",
             f"Adjusted book balance            {f(k['adjusted_book_balance'])}",
             "",
             f"UNEXPLAINED VARIANCE             {f(sm['unexplained_variance'])}   "
             + ("BALANCED" if sm["balanced"] else "NOT BALANCED - do not plug, investigate"),
             "```", "",
             f"Matched groups by tier: {sm['counts']['matched_by_tier']}", ""]
    if len(ul):
        lines += ["## Unmatched ledger lines (reconciling items)", "",
                  "| id | date | description | amount | class | action |", "|---|---|---|---:|---|---|"]
        lines += [f"| {r.id} | {r.date} | {r.description} | {r.amount:,.2f} | {r['class']} | {r.action} |"
                  for _, r in ul.iterrows()]
        lines.append("")
    if len(ub):
        lines += ["## Statement lines not in the books", "",
                  "| id | date | description | amount | class | action |", "|---|---|---|---:|---|---|"]
        lines += [f"| {r.id} | {r.date} | {r.description} | {r.amount:,.2f} | {r['class']} | {r.action} |"
                  for _, r in ub.iterrows()]
        lines.append("")
    if not matches.empty:
        var = matches[(matches["variance"].abs() > CENT) | (matches["tier"] == "grouped")]
        if len(var):
            lines += ["## Matches needing a look", "",
                      "| tier | bank | ledger | bank amt | ledger amt | variance | note |",
                      "|---|---|---|---:|---:|---:|---|"]
            lines += [f"| {r.tier} | {r.bank_description} | {r.ledger_description} | {r.bank_amount:,.2f} | "
                      f"{r.ledger_amount:,.2f} | {r.variance:+.2f} | {r.note} |" for _, r in var.iterrows()]
            lines.append("")
    if sm["exceptions"]:
        lines += ["## Exceptions", ""] + [f"- {e['type']} ({e['ids']}): {e['detail']}" for e in sm["exceptions"]] + [""]
    lines += ["## Notes", ""] + [f"- {n}" for n in sm["notes"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
