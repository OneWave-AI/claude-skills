#!/usr/bin/env python3
"""Dry-run CRM duplicate detection, merge planning, and field normalization.

Reads CRM CSV exports (contacts, optionally companies) from any vendor, and
writes plans to an output directory. It NEVER calls a CRM API and never edits
the input files: a human reviews the plan and executes merges in the CRM's own
merge tool, which is what preserves activity history.

Outputs (in --out):
  merge_plan.csv            one row per (cluster, field): winning value + source record
  review_queue.csv          candidate pairs a human must decide on
  cleaned_contacts.csv      import-ready rows: survivors with merged values + untouched records
  record_flags.csv          per-record hygiene issues (invalid, stale, role, junk, typo)
  companies_merge_plan.csv  \
  companies_review_queue.csv > only when --companies is given
  cleaned_companies.csv     /
  associations.csv          contact->company fixes (orphans, remaps, suggestions)
  summary.json              counts, settings, and which phone engine ran

Usage:
  python dedupe.py --contacts contacts.csv --out plan/
  python dedupe.py --contacts c.csv --companies co.csv --out plan/ \
      --default-region US --survivor-rules most_recent_activity,most_complete,oldest_created
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz

try:  # optional, preferred
    import phonenumbers
    HAVE_PHONENUMBERS = True
except ImportError:  # documented fallback below
    HAVE_PHONENUMBERS = False

# ---------------------------------------------------------------- column map
ALIASES = {
    "id": ["recordid", "id", "contactid", "hsobjectid", "personid", "leadid", "vid"],
    "first_name": ["firstname", "first", "givenname"],
    "last_name": ["lastname", "surname", "familyname", "last"],
    "full_name": ["name", "fullname", "contactname", "personname"],
    "email": ["email", "emailaddress", "email1", "primaryemail", "workemail", "emails"],
    "phone": ["phone", "phonenumber", "mobile", "mobilephone", "mobilephonenumber",
              "workphone", "phone1", "phones", "businessphone"],
    "company": ["company", "companyname", "accountname", "organization", "organisation",
                "orgname", "organizationname", "associatedcompany"],
    "company_id": ["companyid", "accountid", "organizationid", "orgid",
                   "associatedcompanyid", "primarycompanyid"],
    "website": ["website", "websiteurl", "companydomainname", "domain", "url", "domains"],
    "title": ["jobtitle", "title"],
    "lifecycle": ["lifecyclestage", "lifecycle", "leadstatus", "stage"],
    "state": ["state", "stateregion", "province", "region", "mailingstate",
              "billingstate", "stateprovince"],
    "country": ["country", "countryregion", "mailingcountry", "billingcountry"],
    "created": ["createdate", "createddate", "createdat", "datecreated", "addtime",
                "created", "creationdate"],
    "last_activity": ["lastactivitydate", "lastactivity", "lastactivityat",
                      "lastcontacted", "lastmodifieddate", "updatedat", "lastinteraction"],
    "owner": ["owner", "contactowner", "recordowner", "leadowner", "accountowner",
              "companyowner"],
}


def header_key(h: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(h).lower())


def detect_columns(df: pd.DataFrame, overrides: dict[str, str]) -> dict[str, str]:
    by_key = {header_key(c): c for c in df.columns}
    mapping = {}
    for field, keys in ALIASES.items():
        if field in overrides:
            if overrides[field] not in df.columns:
                sys.exit(f"--col {field}={overrides[field]}: column not in file")
            mapping[field] = overrides[field]
            continue
        for k in keys:
            if k in by_key and by_key[k] not in mapping.values():
                mapping[field] = by_key[k]
                break
    return mapping


# ------------------------------------------------------------- reference data
FREE_MAIL = set("""gmail.com googlemail.com yahoo.com yahoo.co.uk ymail.com rocketmail.com
hotmail.com hotmail.co.uk outlook.com live.com msn.com aol.com icloud.com me.com mac.com
proton.me protonmail.com pm.me gmx.com gmx.de gmx.net mail.com zoho.com yandex.com yandex.ru
qq.com 163.com 126.com comcast.net verizon.net att.net sbcglobal.net web.de fastmail.com
hey.com cox.net charter.net""".split())

DOMAIN_TYPOS = {
    "gmial.com": "gmail.com", "gmai.com": "gmail.com", "gamil.com": "gmail.com",
    "gmail.co": "gmail.com", "gnail.com": "gmail.com", "gmaill.com": "gmail.com",
    "hotmial.com": "hotmail.com", "hotmal.com": "hotmail.com", "hotmai.com": "hotmail.com",
    "yaho.com": "yahoo.com", "yahooo.com": "yahoo.com", "yhoo.com": "yahoo.com",
    "outlok.com": "outlook.com", "outloo.com": "outlook.com", "iclod.com": "icloud.com",
    "icoud.com": "icloud.com",
}

ROLE_LOCALS = set("""info sales support admin administrator hello hi contact contactus office
team billing accounts accounting ar ap finance marketing hr jobs careers recruiting noreply
no-reply donotreply do-not-reply enquiries inquiries enquiry inquiry help service
customerservice webmaster postmaster mail general reception frontdesk orders ops
operations legal press media partners privacy security abuse""".split())

JUNK_NAMES = {"test", "testing", "asdf", "qwerty", "na", "n/a", "none", "null", "unknown",
              "xxx", "fake", "sample", "demo", "noname", "no name", "tbd"}

NICKNAMES = {
    "bob": "robert", "rob": "robert", "robbie": "robert", "bobby": "robert",
    "bill": "william", "will": "william", "billy": "william", "liam": "william",
    "jim": "james", "jimmy": "james", "jamie": "james", "mike": "michael", "mick": "michael",
    "liz": "elizabeth", "beth": "elizabeth", "betty": "elizabeth", "eliza": "elizabeth",
    "kate": "katherine", "katie": "katherine", "kathy": "katherine", "cathy": "katherine",
    "tom": "thomas", "tommy": "thomas", "dave": "david", "chris": "christopher",
    "jen": "jennifer", "jenny": "jennifer", "alex": "alexander", "dan": "daniel",
    "danny": "daniel", "matt": "matthew", "nick": "nicholas", "steve": "steven",
    "stephen": "steven", "tony": "anthony", "sam": "samuel", "joe": "joseph",
    "ben": "benjamin", "andy": "andrew", "drew": "andrew", "rick": "richard",
    "dick": "richard", "rich": "richard", "ed": "edward", "ted": "edward",
    "greg": "gregory", "jeff": "jeffrey", "jon": "jonathan", "johnny": "john",
    "pat": "patrick", "patty": "patricia", "peggy": "margaret", "maggie": "margaret",
    "meg": "margaret", "sue": "susan", "suzy": "susan", "vicky": "victoria",
    "abby": "abigail", "tim": "timothy", "ken": "kenneth", "larry": "lawrence",
    "ron": "ronald", "don": "donald", "charlie": "charles", "chuck": "charles",
    "fred": "frederick", "frank": "francis", "hank": "henry", "harry": "henry",
    "jack": "john", "nate": "nathan", "pete": "peter", "phil": "philip", "ray": "raymond",
    "russ": "russell", "zach": "zachary", "josh": "joshua", "becky": "rebecca",
    "debbie": "deborah", "deb": "deborah", "mandy": "amanda", "manny": "manuel",
}

LEGAL_SUFFIXES = set("""inc incorporated llc llp lp ltd limited corp corporation co company
plc gmbh ag sa sas sarl srl spa bv nv pty pvt oy ab as kk kg ohg pllc pc""".split())

US_STATES = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "district of columbia": "DC",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID", "illinois": "IL",
    "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA",
    "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI",
    "minnesota": "MN", "mississippi": "MS", "missouri": "MO", "montana": "MT",
    "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
    "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND",
    "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
    "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN",
    "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY", "puerto rico": "PR",
    "washington dc": "DC", "washington d.c.": "DC",
}
CA_PROVINCES = {
    "alberta": "AB", "british columbia": "BC", "manitoba": "MB", "new brunswick": "NB",
    "newfoundland and labrador": "NL", "newfoundland": "NL", "nova scotia": "NS",
    "ontario": "ON", "prince edward island": "PE", "quebec": "QC", "québec": "QC",
    "saskatchewan": "SK", "northwest territories": "NT", "nunavut": "NU", "yukon": "YT",
}
COUNTRIES = {
    "united states": "US", "united states of america": "US", "usa": "US", "us": "US",
    "u.s.": "US", "u.s.a.": "US", "america": "US", "canada": "CA", "ca": "CA",
    "united kingdom": "GB", "uk": "GB", "u.k.": "GB", "great britain": "GB", "england": "GB",
    "scotland": "GB", "wales": "GB", "gb": "GB", "ireland": "IE", "germany": "DE",
    "deutschland": "DE", "france": "FR", "spain": "ES", "españa": "ES", "italy": "IT",
    "netherlands": "NL", "the netherlands": "NL", "holland": "NL", "belgium": "BE",
    "switzerland": "CH", "austria": "AT", "sweden": "SE", "norway": "NO", "denmark": "DK",
    "finland": "FI", "poland": "PL", "portugal": "PT", "australia": "AU",
    "new zealand": "NZ", "india": "IN", "japan": "JP", "china": "CN", "singapore": "SG",
    "mexico": "MX", "méxico": "MX", "brazil": "BR", "brasil": "BR", "argentina": "AR",
    "south africa": "ZA", "israel": "IL", "united arab emirates": "AE", "uae": "AE",
    "south korea": "KR", "korea, republic of": "KR", "philippines": "PH",
}
# Canonical funnel ladder; later index = further down the funnel.
LIFECYCLE_LADDER = ["subscriber", "lead", "mql", "sql", "opportunity", "customer", "evangelist"]
LIFECYCLE_MAP = {
    "subscriber": "subscriber", "lead": "lead", "new": "lead", "open": "lead",
    "marketingqualifiedlead": "mql", "mql": "mql", "marketing qualified lead": "mql",
    "salesqualifiedlead": "sql", "sql": "sql", "sales qualified lead": "sql",
    "working": "sql", "working - contacted": "sql", "qualified": "sql",
    "opportunity": "opportunity", "customer": "customer", "closed won": "customer",
    "evangelist": "evangelist", "advocate": "evangelist",
}

# -------------------------------------------------------------- normalizers
EMAIL_RE = re.compile(r"^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
                      r"(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+$")


def s(v) -> str:
    return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v).strip()


def strip_accents(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))


def norm_email(raw: str) -> str:
    e = s(raw).lower()
    e = re.sub(r"^mailto:", "", e).strip("<>\"' ;,")
    return e.split(";")[0].split(",")[0].strip()  # first address if several


def email_match_key(e: str, gmail_canonical: bool, strip_plus_all: bool) -> str:
    """Key used for matching only; the stored email is never rewritten this way."""
    if "@" not in e:
        return e
    local, dom = e.rsplit("@", 1)
    if dom in ("gmail.com", "googlemail.com") and gmail_canonical:
        local = local.split("+", 1)[0].replace(".", "")
        dom = "gmail.com"
    elif strip_plus_all:
        local = local.split("+", 1)[0]
    return f"{local}@{dom}"


def norm_domain(raw: str) -> str:
    d = s(raw).lower()
    if not d:
        return ""
    d = re.sub(r"^[a-z]+://", "", d)
    d = d.split("/")[0].split("?")[0].split("#")[0].split(":")[0]
    d = re.sub(r"^www\d?\.", "", d).strip(".")
    return d if "." in d else ""


def split_ext(raw: str) -> tuple[str, str]:
    m = re.search(r"(?i)\s*(?:ext\.?|extension|x|#)\s*(\d{1,6})\s*$", raw)
    return (raw[: m.start()], m.group(1)) if m else (raw, "")


NANP = {"US", "CA", "PR"}


def norm_phone(raw: str, region: str) -> tuple[str, str]:
    """Return (E.164 or '', extension). '' means could not normalize safely."""
    txt = s(raw)
    if not txt:
        return "", ""
    txt, ext = split_ext(txt)
    if HAVE_PHONENUMBERS:
        try:
            num = phonenumbers.parse(txt, region)
            reason = phonenumbers.is_possible_number_with_reason(num)
            # IS_POSSIBLE_LOCAL_ONLY (7-digit US numbers with no area code) is rejected:
            # it cannot be written as a dialable E.164 number.
            if reason == phonenumbers.ValidationResult.IS_POSSIBLE:
                return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164), ext
        except phonenumbers.NumberParseException:
            pass
        return "", ext
    # Fallback (no phonenumbers): digits only; trust an explicit + or 00 prefix;
    # otherwise add +1 only for NANP regions with 10/11-digit numbers. Anything else
    # is left unnormalized and flagged, because guessing a country code corrupts data.
    intl = txt.startswith("+") or txt.startswith("00")
    digits = re.sub(r"\D", "", txt)
    if txt.startswith("00"):
        digits = digits[2:]
    if intl:
        return ("+" + digits, ext) if 8 <= len(digits) <= 15 else ("", ext)
    if region in NANP:
        if len(digits) == 10 and digits[0] not in "01":
            return "+1" + digits, ext
        if len(digits) == 11 and digits[0] == "1":
            return "+" + digits, ext
    return "", ext


def smart_case(name: str) -> str:
    """Fix ALL CAPS / all lower only; leave mixed case alone (McDonald, van der Berg)."""
    n = re.sub(r"\s+", " ", s(name))
    if not n or not (n.isupper() or n.islower()):
        return n

    def cap(w: str) -> str:
        w = w.capitalize()
        w = re.sub(r"^(Mc)([a-z])", lambda m: m.group(1) + m.group(2).upper(), w)
        w = re.sub(r"^(O')([a-z])", lambda m: m.group(1) + m.group(2).upper(), w)
        return w
    return " ".join("-".join(cap(p) for p in w.split("-")) for w in n.split(" "))


def name_key(n: str) -> str:
    n = strip_accents(s(n).lower())
    n = re.sub(r"[^a-z\s-]", "", n).replace("-", " ")
    return re.sub(r"\s+", " ", n).strip()


def canon_first(fk: str) -> str:
    first = fk.split(" ")[0] if fk else ""
    return NICKNAMES.get(first, first)


def company_key(n: str) -> str:
    k = strip_accents(s(n).lower()).replace("&", " and ")
    k = re.sub(r"[^a-z0-9\s]", " ", k)
    toks = k.split()
    if toks and toks[0] == "the":
        toks = toks[1:]
    while toks and toks[-1] in LEGAL_SUFFIXES:
        toks = toks[:-1]
    return " ".join(toks)


def norm_state(v: str, country: str) -> str:
    t = s(v)
    low = t.lower().strip(". ")
    if not t:
        return ""
    if country in ("US", "") and low in US_STATES:
        return US_STATES[low]
    if country in ("CA", "") and low in CA_PROVINCES:
        return CA_PROVINCES[low]
    if len(t) == 2 and t.isalpha():
        return t.upper()
    return t


def norm_country(v: str) -> str:
    t = s(v)
    low = t.lower().strip()
    if low in COUNTRIES:
        return COUNTRIES[low]
    if len(t) == 2 and t.isalpha():
        return t.upper()
    return t


def parse_date(v: str):
    t = s(v)
    if not t:
        return pd.NaT
    d = pd.to_datetime(t, errors="coerce", utc=True)
    if pd.isna(d) and re.fullmatch(r"\d{12,13}", t):  # epoch millis (HubSpot API style)
        d = pd.to_datetime(int(t), unit="ms", utc=True)
    return d


# ------------------------------------------------------------------ records
def prepare_contacts(df: pd.DataFrame, cmap: dict, args) -> pd.DataFrame:
    g = lambda row, f: s(row[cmap[f]]) if f in cmap else ""  # noqa: E731
    out = []
    as_of = pd.Timestamp(args.as_of, tz="UTC") if args.as_of else pd.Timestamp.now(tz="UTC")
    for i, row in df.iterrows():
        r = {"_row": i, "id": g(row, "id") or f"row{i + 2}"}
        first, last = smart_case(g(row, "first_name")), smart_case(g(row, "last_name"))
        if not first and not last and g(row, "full_name"):
            parts = smart_case(g(row, "full_name")).split(" ")
            first, last = parts[0], " ".join(parts[1:])
        r["first_name"], r["last_name"] = first, last
        r["fk"], r["lk"] = name_key(first), name_key(last)
        r["first_canon"] = canon_first(r["fk"])
        r["email"] = norm_email(g(row, "email"))
        r["email_valid"] = bool(EMAIL_RE.match(r["email"])) if r["email"] else False
        local, dom = (r["email"].rsplit("@", 1) + [""])[:2] if "@" in r["email"] else ("", "")
        r["email_local"], r["email_domain"] = local, dom
        r["email_key"] = email_match_key(r["email"], args.gmail_canonical, args.strip_plus) \
            if r["email_valid"] else ""
        r["role_email"] = local.split("+")[0] in ROLE_LOCALS
        r["free_mail"] = dom in FREE_MAIL
        r["phone_raw"] = g(row, "phone")
        r["phone"], r["phone_ext"] = norm_phone(r["phone_raw"], args.default_region)
        r["company"] = re.sub(r"\s+", " ", g(row, "company"))
        r["ck"] = company_key(r["company"])
        r["company_id"] = g(row, "company_id")
        site = norm_domain(g(row, "website"))
        r["domain"] = site or (dom if r["email_valid"] and not r["free_mail"] else "")
        r["country"] = norm_country(g(row, "country"))
        r["state"] = norm_state(g(row, "state"), r["country"])
        raw_stage = g(row, "lifecycle")
        r["lifecycle_raw"] = raw_stage
        r["lifecycle"] = LIFECYCLE_MAP.get(raw_stage.lower(), raw_stage.lower()) if raw_stage else ""
        r["created"] = parse_date(g(row, "created"))
        r["last_activity"] = parse_date(g(row, "last_activity"))
        r["completeness"] = sum(1 for c in df.columns if s(row[c]))
        flags, notes = [], []
        if r["email"] and not r["email_valid"]:
            flags.append("invalid_email")
        if dom in DOMAIN_TYPOS:
            flags.append("email_domain_typo")
            notes.append(f"did you mean {local}@{DOMAIN_TYPOS[dom]}")
        if r["role_email"]:
            flags.append("role_email")
        if not r["email_valid"] and not r["phone"]:
            flags.append("no_contact_method")
        if r["phone_raw"] and not r["phone"]:
            flags.append("phone_unparsed")
        full = f"{r['fk']} {r['lk']}".strip()
        if full in JUNK_NAMES or r["fk"] in JUNK_NAMES or r["lk"] in JUNK_NAMES \
                or local in {"test", "asdf", "fake"}:
            flags.append("junk_or_test")
        if not r["fk"] and not r["lk"]:
            flags.append("missing_name")
        act = r["last_activity"] if not pd.isna(r["last_activity"]) else r["created"]
        if not pd.isna(act) and (as_of - act).days > args.stale_days:
            flags.append("stale")
            notes.append(f"no activity for {(as_of - act).days} days")
        r["flags"], r["notes"] = flags, notes
        out.append(r)
    return pd.DataFrame(out)


def first_sim(a: dict, b: dict) -> float:
    fa, fb = a["first_canon"], b["first_canon"]
    if not fa or not fb:
        return -1
    if fa == fb:
        return 100
    if (len(fa) == 1 and fb.startswith(fa)) or (len(fb) == 1 and fa.startswith(fb)):
        return 90
    return fuzz.ratio(fa, fb)


def last_sim(a: dict, b: dict) -> float:
    la, lb = a["lk"], b["lk"]
    if not la or not lb:
        return -1
    if la == lb:
        return 100
    ta, tb = set(la.split()), set(lb.split())
    if ta & tb:  # "carter" vs "carter hayes": hyphenated / married names
        return 90
    return fuzz.ratio(la.replace(" ", ""), lb.replace(" ", ""))


def name_sim(a: dict, b: dict):
    """None when either side has no name at all (unknown, not a conflict)."""
    if not (a["fk"] or a["lk"]) or not (b["fk"] or b["lk"]):
        return None
    f, l_ = first_sim(a, b), last_sim(a, b)
    if f >= 0 and l_ >= 0:
        return round(0.4 * f + 0.6 * l_, 1)
    fa = f"{a['first_canon']} {a['lk']}".strip()
    fb = f"{b['first_canon']} {b['lk']}".strip()
    return float(fuzz.token_sort_ratio(fa, fb))


# ------------------------------------------------------------ pair scoring
def score_contact_pair(a: dict, b: dict, shared_phones: set, shared_emails: set, args):
    reasons = []
    ns = name_sim(a, b)
    email_exact = bool(a["email_key"]) and a["email_key"] == b["email_key"]
    email_shared = email_exact and (a["role_email"] or a["email_key"] in shared_emails)
    phone_match = bool(a["phone"]) and a["phone"] == b["phone"]
    phone_shared = phone_match and a["phone"] in shared_phones
    dom_match = bool(a["domain"]) and a["domain"] == b["domain"]
    comp = fuzz.ratio(a["ck"], b["ck"]) if a["ck"] and b["ck"] else None
    same_company = dom_match or (comp is not None and comp >= 90)
    company_conflict = (bool(a["domain"]) and bool(b["domain"]) and not dom_match
                        and (comp is None or comp < 60))
    loc_a = re.sub(r"[^a-z]", "", a["email_local"].split("+")[0])
    loc_b = re.sub(r"[^a-z]", "", b["email_local"].split("+")[0])
    local_sim = fuzz.ratio(loc_a, loc_b) if loc_a and loc_b and not email_exact else 0

    if email_exact:
        reasons.append("shared/role email" if email_shared else "email exact")
    if phone_match:
        reasons.append("shared phone line" if phone_shared else "phone exact")
    if ns is not None:
        reasons.append(f"name sim {ns:.0f}")
    if dom_match:
        reasons.append("same company domain")
    elif comp is not None and comp >= 90:
        reasons.append("same company name")
    if company_conflict:
        reasons.append("different company domains")
    if local_sim >= 85:
        reasons.append(f"email local-part sim {local_sim:.0f}")

    score = 0.0
    score += 50 if (email_exact and not email_shared) else (10 if email_exact else 0)
    score += 25 if (phone_match and not phone_shared) else (5 if phone_match else 0)
    score += (ns or 0) * 0.3 if ns is not None else 10
    score += 10 if same_company else 0
    score += 5 if local_sim >= 85 else 0
    if ns is not None and ns < args.conflict_name_sim:
        score -= 30
    if company_conflict:
        score -= 20
    score = max(0, min(100, round(score)))

    name_ok = ns is None or ns >= args.auto_name_sim
    name_conflict = ns is not None and ns < args.conflict_name_sim
    strong_email = email_exact and not email_shared
    strong_phone = phone_match and not phone_shared

    if strong_email and name_ok and not company_conflict:
        tier = "auto"
    elif strong_phone and ns is not None and ns >= args.auto_name_sim and not company_conflict:
        tier = "auto"
    elif (strong_email or strong_phone) and not name_conflict:
        tier = "review"
    elif strong_email and name_conflict:
        tier = "review"
        reasons.append("same email, different names (shared inbox, assistant, or typo)")
    elif email_shared and (ns is None or ns >= args.review_name_sim):
        tier = "review"
    elif ns is not None and ns >= args.review_name_sim and (
            same_company or local_sim >= 85 or phone_match):
        tier = "review"
    else:
        tier = "keep"
    return tier, score, reasons, {
        "name_conflict": name_conflict, "company_conflict": company_conflict,
        "name_incompatible": ns is not None and ns < args.auto_name_sim}


# ----------------------------------------------------------------- blocking
def candidate_pairs(recs: list[dict], key_fns, max_block: int, warnings: list):
    blocks = defaultdict(list)
    for idx, r in enumerate(recs):
        for kf in key_fns:
            k = kf(r)
            if k:
                blocks[k].append(idx)
    pairs = set()
    for k, members in blocks.items():
        if len(members) > max_block:
            warnings.append(f"block '{k}' has {len(members)} records; skipped (raise --max-block)")
            continue
        for i, j in combinations(sorted(set(members)), 2):
            pairs.add((i, j))
    return pairs


class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


def build_clusters(n, scored, pair_fn, max_cluster):
    """Union auto edges, then re-check every pair inside each cluster: transitive
    chains (A=B by email, B=C by phone) can join two people who never match directly."""
    dsu = DSU(n)
    for (i, j), v in scored.items():
        if v["tier"] == "auto":
            dsu.union(i, j)
    groups = defaultdict(list)
    for i in range(n):
        groups[dsu.find(i)].append(i)
    clusters, demoted = [], []
    for members in groups.values():
        if len(members) < 2:
            continue
        bad = len(members) > max_cluster
        if not bad:
            for i, j in combinations(members, 2):
                v = scored.get((min(i, j), max(i, j))) or pair_fn(i, j)
                c = v["conflicts"]
                if c["name_incompatible"] or c["company_conflict"]:
                    bad = True
                    break
        (demoted if bad else clusters).append(sorted(members))
    return clusters, demoted


# ------------------------------------------------------------ survivor/merge
def rank_key(r: dict, rules: list[str]):
    key = []
    for rule in rules:
        if rule == "most_recent_activity":
            t = r["last_activity"]
            key.append(-(t.value if not pd.isna(t) else -2**62))
        elif rule == "most_complete":
            key.append(-r["completeness"])
        elif rule == "oldest_created":
            t = r["created"]
            key.append(t.value if not pd.isna(t) else 2**62)
        elif rule == "business_email":  # prefer a work address as the primary email
            key.append(0 if r.get("email_valid") and not r.get("free_mail") else 1)
        elif rule == "newest_created":
            t = r["created"]
            key.append(-(t.value if not pd.isna(t) else -2**62))
        else:
            sys.exit(f"unknown survivor rule: {rule}")
    key.append(str(r["id"]))
    return tuple(key)


def plan_cluster(cid, members, recs, raw_df, cmap, rules, plan_rows, entity):
    ordered = sorted((recs[m] for m in members), key=lambda r: rank_key(r, rules))
    surv, losers = ordered[0], ordered[1:]
    loser_ids = ";".join(str(r["id"]) for r in losers)
    inv = {v: k for k, v in cmap.items()}
    merged = {}

    def emit(field, value, source, action, others):
        plan_rows.append({"cluster_id": cid, "entity": entity, "survivor_id": surv["id"],
                          "loser_ids": loser_ids, "survivor_rule": ",".join(rules),
                          "field": field, "winning_value": value, "source_id": source,
                          "action": action, "other_values": others})

    for col in raw_df.columns:
        canon = inv.get(col)
        vals = [(r["id"], normalized_value(r, canon, raw_df.at[r["_row"], col])) for r in ordered]
        nonempty = [(i, v) for i, v in vals if v != ""]
        if not nonempty:
            continue
        distinct_other = lambda win: "; ".join(  # noqa: E731
            sorted({f"{v} ({i})" for i, v in nonempty if v != win}))
        if canon == "id":
            merged[col] = surv["id"]
            continue
        if canon == "created":
            dated = [(r["created"], r["id"], raw_df.at[r["_row"], col]) for r in ordered
                     if not pd.isna(r["created"])]
            if dated:
                d, i, raw = min(dated, key=lambda x: x[0])
                merged[col] = s(raw)
                emit(col, s(raw), i, "earliest", distinct_other(s(raw)))
                continue
        if canon == "last_activity":
            dated = [(r["last_activity"], r["id"], raw_df.at[r["_row"], col]) for r in ordered
                     if not pd.isna(r["last_activity"])]
            if dated:
                d, i, raw = max(dated, key=lambda x: x[0])
                merged[col] = s(raw)
                emit(col, s(raw), i, "latest", distinct_other(s(raw)))
                continue
        if canon == "lifecycle":
            staged = [(LIFECYCLE_LADDER.index(r["lifecycle"]), r["id"],
                       s(raw_df.at[r["_row"], col])) for r in ordered
                      if r["lifecycle"] in LIFECYCLE_LADDER]
            if staged:
                _, i, raw = max(staged, key=lambda x: x[0])
                merged[col] = raw
                emit(col, raw, i, "furthest_stage", distinct_other(raw))
                continue
        sv = vals[0][1]
        if sv != "":
            win, src, action = sv, surv["id"], "kept_survivor"
        else:  # never overwrite non-empty with empty: fill from best-ranked loser
            src, win = nonempty[0]
            action = "filled_from_loser"
        merged[col] = win
        others = distinct_other(win)
        if others and action == "kept_survivor":
            action = "kept_survivor_conflict"
        emit(col, win, src, action, others)
        if canon in ("email", "phone") and others:
            extra = sorted({v for _, v in nonempty if v != win})
            key = "additional_emails" if canon == "email" else "additional_phones"
            merged[key] = ";".join(extra)
            emit(key, merged[key], ";".join(i for i, v in nonempty if v != win),
                 "preserved_secondary", "")
    return surv, losers, merged


def normalized_value(r: dict, canon, raw) -> str:
    """Normalized form for canonical fields; untouched (trimmed) text otherwise."""
    if canon is None:
        return s(raw)
    if r is None or "email_key" not in r:  # company records: only the domain is rewritten
        return (norm_domain(raw) or s(raw)) if canon == "website" else s(raw)
    if canon == "email":
        return r["email"]
    if canon == "phone":
        return (r["phone"] + (f" ext {r['phone_ext']}" if r["phone_ext"] else "")) \
            if r["phone"] else s(raw)
    if canon == "first_name":
        return r["first_name"]
    if canon == "last_name":
        return r["last_name"]
    if canon == "state":
        return r["state"]
    if canon == "country":
        return r["country"]
    if canon == "website":
        return norm_domain(raw) or s(raw)
    return s(raw)


# ----------------------------------------------------------------- companies
def prepare_companies(df, cmap, args):
    g = lambda row, f: s(row[cmap[f]]) if f in cmap else ""  # noqa: E731
    name_col = cmap.get("company") or cmap.get("full_name")
    recs = []
    for i, row in df.iterrows():
        name = s(row[name_col]) if name_col else ""
        r = {"_row": i, "id": g(row, "id") or f"row{i + 2}", "name": name,
             "ck": company_key(name), "domain": norm_domain(g(row, "website")),
             "created": parse_date(g(row, "created")),
             "last_activity": parse_date(g(row, "last_activity")),
             "completeness": sum(1 for c in df.columns if s(row[c])), "lifecycle": "",
             "flags": [], "notes": []}
        if not r["domain"]:
            r["flags"].append("missing_domain")
        recs.append(r)
    return recs


def score_company_pair(a, b, args):
    reasons = []
    ns = fuzz.token_sort_ratio(a["ck"], b["ck"]) if a["ck"] and b["ck"] else None
    dom_match = bool(a["domain"]) and a["domain"] == b["domain"]
    dom_conflict = bool(a["domain"]) and bool(b["domain"]) and not dom_match
    if dom_match:
        reasons.append("domain exact")
    if ns is not None:
        reasons.append(f"name sim {ns:.0f}")
    if dom_conflict:
        reasons.append("different domains")
    name_conflict = ns is not None and ns < 50
    if dom_match and not name_conflict:
        tier = "auto"
    elif dom_match:
        tier = "review"
        reasons.append("same domain, different names (parent/subsidiary or shared site)")
    elif ns is not None and ns >= 92:
        tier = "review"
        if dom_conflict:
            reasons.append("same name, different domains: could be distinct entities")
    else:
        tier = "keep"
    score = (60 if dom_match else 0) + (ns or 0) * 0.4 - (30 if dom_conflict else 0)
    return tier, max(0, min(100, round(score))), reasons, {
        "name_conflict": name_conflict, "company_conflict": dom_conflict and not dom_match,
        "name_incompatible": name_conflict}


# --------------------------------------------------------------------- run
def run_entity(recs, pairs, pair_fn, args, entity, raw_df, cmap, out, warnings):
    scored = {}
    for i, j in pairs:
        tier, score, reasons, conflicts = pair_fn(i, j)
        scored[(i, j)] = {"tier": tier, "score": score, "reasons": reasons,
                          "conflicts": conflicts}

    def lazy(i, j):
        t, sc, rs, cf = pair_fn(i, j)
        return {"tier": t, "score": sc, "reasons": rs, "conflicts": cf}

    clusters, demoted = build_clusters(len(recs), scored, lazy, args.max_cluster)
    rules = [r.strip() for r in args.survivor_rules.split(",") if r.strip()]
    plan_rows, merged_by_surv, loser_set, cluster_of = [], {}, set(), {}
    for n, members in enumerate(clusters, 1):
        cid = f"{'MC' if entity == 'contact' else 'MA'}{n:04d}"
        surv, losers, merged = plan_cluster(cid, members, recs, raw_df, cmap, rules,
                                            plan_rows, entity)
        merged_by_surv[surv["_row"]] = (cid, merged, [l_["id"] for l_ in losers])
        for m in members:
            cluster_of[m] = cid
        loser_set.update(l_["_row"] for l_ in losers)

    review_rows = []
    demoted_members = {m: k for k, grp in enumerate(demoted) for m in grp}
    for (i, j), v in sorted(scored.items(), key=lambda kv: -kv[1]["score"]):
        same_cluster = i in cluster_of and cluster_of.get(i) == cluster_of.get(j)
        in_demoted = i in demoted_members and demoted_members.get(j) == demoted_members[i]
        if same_cluster:
            continue
        if v["tier"] == "review" or (v["tier"] == "auto" and (in_demoted or not same_cluster)):
            a, b = recs[i], recs[j]
            reason = "; ".join(v["reasons"])
            if v["tier"] == "auto":
                reason += "; demoted: cluster chain contains a conflicting pair or is too large"
            suggested = sorted([a, b], key=lambda r: rank_key(r, rules))[0]["id"]
            row = {"pair_id": f"R{len(review_rows) + 1:04d}", "entity": entity,
                   "record_a": a["id"], "record_b": b["id"], "confidence": v["score"],
                   "reasons": reason, "suggested_survivor": suggested,
                   "decision": "", "decided_by": ""}
            for side, r in (("a", a), ("b", b)):
                if entity == "contact":
                    row[f"name_{side}"] = f"{r['first_name']} {r['last_name']}".strip()
                    row[f"email_{side}"] = r["email"]
                    row[f"phone_{side}"] = r["phone"] or r["phone_raw"]
                    row[f"company_{side}"] = r["company"]
                else:
                    row[f"name_{side}"] = r["name"]
                    row[f"domain_{side}"] = r["domain"]
            review_rows.append(row)

    pd.DataFrame(plan_rows, columns=["cluster_id", "entity", "survivor_id", "loser_ids",
                                     "survivor_rule", "field", "winning_value", "source_id",
                                     "action", "other_values"]).to_csv(
        out / ("merge_plan.csv" if entity == "contact" else "companies_merge_plan.csv"),
        index=False)
    pd.DataFrame(review_rows).to_csv(
        out / ("review_queue.csv" if entity == "contact" else "companies_review_queue.csv"),
        index=False)

    inv = {v: k for k, v in cmap.items()}
    review_ids = {r["record_a"] for r in review_rows} | {r["record_b"] for r in review_rows}
    cleaned = []
    for r in recs:
        if r["_row"] in loser_set:
            continue
        row = {c: normalized_value(r if entity == "contact" else None, inv.get(c),
                                   raw_df.at[r["_row"], c]) for c in raw_df.columns}
        if entity == "company" and "website" in cmap:
            row[cmap["website"]] = r["domain"] or row[cmap["website"]]
        row["additional_emails"] = row.get("additional_emails", "")
        row["additional_phones"] = row.get("additional_phones", "")
        action = "unchanged"
        if r["_row"] in merged_by_surv:
            cid, merged, lids = merged_by_surv[r["_row"]]
            row.update(merged)
            action = f"survivor of {cid} (absorbs {';'.join(lids)})"
        elif r["id"] in review_ids:
            action = "needs_review"
        row["_cleanup_action"] = action
        row["_row"] = r["_row"]
        row["_flags"] = ";".join(r["flags"])
        cleaned.append(row)
    return cleaned, clusters, demoted, review_rows, loser_set, cluster_of


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--contacts", required=True, help="contacts/leads/people CSV export")
    ap.add_argument("--companies", help="optional companies/accounts/organizations CSV")
    ap.add_argument("--out", required=True, help="output directory (created)")
    ap.add_argument("--col", action="append", default=[],
                    help="contacts column override, e.g. --col email='E-mail 1'")
    ap.add_argument("--company-col", action="append", default=[],
                    help="companies column override, e.g. --company-col company='Account Name'")
    ap.add_argument("--default-region", default="US",
                    help="ISO region for phones without a country code (default US)")
    ap.add_argument("--gmail-canonical", action="store_true",
                    help="OPT-IN: match gmail.com addresses ignoring dots and +tags")
    ap.add_argument("--strip-plus", action="store_true",
                    help="OPT-IN: ignore +tags on all domains when matching")
    ap.add_argument("--survivor-rules", default="most_recent_activity,most_complete,oldest_created",
                    help="ordered list of: most_recent_activity, most_complete, "
                         "oldest_created, newest_created, business_email")
    ap.add_argument("--auto-name-sim", type=float, default=85)
    ap.add_argument("--review-name-sim", type=float, default=88)
    ap.add_argument("--conflict-name-sim", type=float, default=60)
    ap.add_argument("--max-cluster", type=int, default=5,
                    help="clusters larger than this go to review, never auto")
    ap.add_argument("--max-block", type=int, default=500)
    ap.add_argument("--stale-days", type=int, default=365)
    ap.add_argument("--as-of", help="reference date for staleness (YYYY-MM-DD); default today")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    warnings = []
    if not HAVE_PHONENUMBERS:
        warnings.append("phonenumbers not installed: NANP-only fallback used for phones "
                        "without +country code (pip install phonenumbers)")
    parse_ov = lambda items: dict(x.split("=", 1) for x in items)  # noqa: E731

    raw = pd.read_csv(args.contacts, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    cmap = detect_columns(raw, parse_ov(args.col))
    if "email" not in cmap and "phone" not in cmap:
        sys.exit("no email or phone column detected; pass --col email=<header>")
    cdf = prepare_contacts(raw, cmap, args)
    recs = cdf.to_dict("records")

    # Shared identifiers: an office main line or household inbox used by several people
    # is evidence of the same ORGANIZATION, not the same PERSON.
    by_phone, by_email = defaultdict(set), defaultdict(set)
    for r in recs:
        if r["phone"]:
            by_phone[r["phone"]].add(r["lk"] or r["fk"])
        if r["email_key"]:
            by_email[r["email_key"]].add(r["first_canon"] or r["lk"])
    shared_phones = {p for p, names in by_phone.items() if len(names) >= 2}
    shared_emails = {e for e, names in by_email.items() if len(names) >= 3}
    for r in recs:
        if r["phone"] in shared_phones:
            r["flags"].append("shared_phone")

    key_fns = [
        lambda r: "e:" + r["email_key"] if r["email_key"] else "",
        lambda r: "p:" + r["phone"] if r["phone"] else "",
        lambda r: f"n1:{r['lk'][:3]}|{r['first_canon'][:1]}" if r["lk"] else "",
        lambda r: f"n2:{r['first_canon']}|{r['lk'][:1]}" if r["first_canon"] else "",
        lambda r: "d:" + r["domain"] if r["domain"] else "",
        lambda r: "c:" + r["ck"] if r["ck"] else "",
    ]
    pairs = candidate_pairs(recs, key_fns, args.max_block, warnings)
    pair_fn = lambda i, j: score_contact_pair(recs[i], recs[j], shared_phones,  # noqa: E731
                                              shared_emails, args)
    cleaned, clusters, demoted, review, losers, _ = run_entity(
        recs, pairs, pair_fn, args, "contact", raw, cmap, out, warnings)

    summary = {"input_contacts": len(recs), "candidate_pairs": len(pairs),
               "auto_clusters": len(clusters),
               "records_merged_away": len(losers),
               "demoted_clusters": len(demoted), "review_pairs": len(review),
               "contacts_after_merge": len(cleaned)}

    # Companies + associations
    assoc_rows = []
    if args.companies:
        craw = pd.read_csv(args.companies, dtype=str, keep_default_na=False,
                           encoding="utf-8-sig")
        comap = detect_columns(craw, parse_ov(args.company_col))
        if "company" not in comap and "full_name" in comap:
            comap["company"] = comap.pop("full_name")
        crecs = prepare_companies(craw, comap, args)
        ckeys = [lambda r: "d:" + r["domain"] if r["domain"] else "",
                 lambda r: "c:" + r["ck"] if r["ck"] else "",
                 lambda r: "c3:" + r["ck"][:3] if r["ck"] else ""]
        cpairs = candidate_pairs(crecs, ckeys, args.max_block, warnings)
        cfn = lambda i, j: score_company_pair(crecs[i], crecs[j], args)  # noqa: E731
        ccleaned, cclusters, cdemoted, creview, closers, ccluster_of = run_entity(
            crecs, cpairs, cfn, args, "company", craw, comap, out, warnings)
        pd.DataFrame(ccleaned).drop(columns=["_row"]).to_csv(out / "cleaned_companies.csv",
                                                             index=False)
        summary.update({"input_companies": len(crecs), "company_auto_clusters": len(cclusters),
                        "companies_merged_away": len(closers),
                        "company_review_pairs": len(creview)})
        # survivor map for loser company ids
        plan = pd.read_csv(out / "companies_merge_plan.csv", dtype=str, keep_default_na=False)
        remap = {}
        for _, pr in plan.drop_duplicates("cluster_id").iterrows():
            for lid in pr["loser_ids"].split(";"):
                remap[lid] = pr["survivor_id"]
        company_ids = {c["id"] for c in crecs}
        by_domain = defaultdict(list)
        for c in crecs:
            if c["domain"] and c["_row"] not in closers:
                by_domain[c["domain"]].append(c["id"])
        id_col = cmap.get("company_id")
        for row in cleaned:
            cid_val = row.get(id_col, "") if id_col else ""
            r = recs[row["_row"]]
            if cid_val and cid_val in remap:
                assoc_rows.append({"contact_id": r["id"], "issue": "company_merged",
                                   "current_company_id": cid_val,
                                   "suggested_company_id": remap[cid_val],
                                   "detail": "associated company is merged away; the CRM "
                                             "re-points this on merge, verify after"})
                row[id_col] = remap[cid_val]
            elif cid_val and cid_val not in company_ids:
                assoc_rows.append({"contact_id": r["id"], "issue": "orphan_company_id",
                                   "current_company_id": cid_val,
                                   "suggested_company_id": ";".join(by_domain.get(r["domain"], [])),
                                   "detail": "company id not found in companies export"})
            elif not cid_val and r["domain"] and by_domain.get(r["domain"]):
                assoc_rows.append({"contact_id": r["id"], "issue": "missing_association",
                                   "current_company_id": "",
                                   "suggested_company_id": ";".join(by_domain[r["domain"]]),
                                   "detail": f"email/website domain {r['domain']} matches"})
        pd.DataFrame(assoc_rows, columns=["contact_id", "issue", "current_company_id",
                                          "suggested_company_id", "detail"]).to_csv(
            out / "associations.csv", index=False)
        summary["association_issues"] = len(assoc_rows)

    pd.DataFrame(cleaned).drop(columns=["_row"]).to_csv(out / "cleaned_contacts.csv",
                                                        index=False)
    flag_rows = [{"id": r["id"], "flags": ";".join(r["flags"]), "notes": "; ".join(r["notes"]),
                  "email": r["email"], "phone_e164": r["phone"], "phone_raw": r["phone_raw"]}
                 for r in recs if r["flags"]]
    pd.DataFrame(flag_rows, columns=["id", "flags", "notes", "email", "phone_e164",
                                     "phone_raw"]).to_csv(out / "record_flags.csv", index=False)
    counts = defaultdict(int)
    for r in recs:
        for f in r["flags"]:
            counts[f] += 1
    summary.update({"flag_counts": dict(counts), "column_map": cmap,
                    "phone_engine": "phonenumbers" if HAVE_PHONENUMBERS else "fallback",
                    "settings": {k: v for k, v in vars(args).items()
                                 if k not in ("contacts", "companies", "out")},
                    "warnings": warnings,
                    "generated_at": datetime.now().isoformat(timespec="seconds"),
                    "note": "dry run: no CRM was contacted and no input file was modified"})
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("settings", "column_map")}, indent=2, default=str))


if __name__ == "__main__":
    main()
