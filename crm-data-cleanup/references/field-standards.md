# Field standards

These are the normalization rules `scripts/dedupe.py` applies, and the reasons for them.
One principle runs through all of it: a **match key** is used only for comparing records,
while the **stored value** is what gets written back to the CRM. The script builds
aggressive match keys, but changes stored values only in ways that are always safe.

## Contents
- Email
- Phone
- Person names
- Company names and domains
- State, province, country
- Lifecycle stage mapping
- Dates
- Record flags

## Email

Stored value: lowercased, trimmed, with `mailto:`, angle brackets, and quotes removed.
When a cell holds several addresses separated by `;` or `,`, the first one is kept. The
domain part of an address is case-insensitive in practice. The local part technically
isn't, but no mainstream mailbox provider treats it that way, so lowercasing is safe.

Match key options, **both off by default**:
- `--gmail-canonical` drops the dots and the `+tag` for `gmail.com` and `googlemail.com`
  only. Google [documents](https://support.google.com/mail/answer/7436150) that dots don't
  matter for personal Gmail, and that they **do** matter for Workspace (company domain)
  mailboxes. So never apply dot-stripping to other domains. It stays opt-in because
  `a.smith@gmail.com` and `asmith@gmail.com` are sometimes two different people's
  addresses entered by a sloppy rep. The dotted variant has to be real before it counts
  as a match.
- `--strip-plus` ignores the `+tag` on every domain. Many providers support plus
  addressing, but some companies use `+` in real mailbox names.

Classification:
- **Role address**: the local part is `info`, `sales`, `support`, `admin`, `hello`,
  `office`, `billing`, `hr`, `noreply`, and similar (see `ROLE_LOCALS` in the script). A
  role address is evidence of an organization, never of a person, so it can't trigger an
  auto-merge.
- **Free mail**: gmail, yahoo, outlook/hotmail/live, icloud, aol, proton, gmx, and ISP
  domains. A free-mail domain is never used as a company domain.
- **Domain typo**: `gmial.com`, `hotmial.com`, `yaho.com`, and the like are flagged with a
  suggested fix. They are **not** corrected automatically, because the address might
  really be on that domain and the fix belongs to the record owner.
- **Invalid**: fails a practical RFC 5322 subset: no `@`, an empty domain, or no dot in
  the domain.

## Phone

Target format: [E.164](https://www.itu.int/rec/T-REC-E.164), which is `+` followed by the
country code and national number, with no spaces and at most 15 digits. For example,
`+14155550101`. An extension goes after the number as ` ext 204`, so it is kept and still
kept out of the match key.

Engines:
1. **`phonenumbers`** (the Python port of Google's libphonenumber). The script uses it
   when it's installed. It parses using `--default-region` (default `US`) and accepts only
   `IS_POSSIBLE` numbers. `IS_POSSIBLE_LOCAL_ONLY` numbers (for example a 7-digit US
   number with no area code) are rejected, because they can't be dialed as E.164.
2. **Fallback**, used when `phonenumbers` isn't installed. It keeps only the digits, then:
   - With an explicit `+` or `00` prefix, it keeps the number as international if it has
     8 to 15 digits.
   - With a NANP region (US, CA, PR), it turns 10 digits (first digit not 0 or 1) into
     `+1XXXXXXXXXX`, and 11 digits starting with `1` into `+1...`.
   - Anything else is left as-is and flagged `phone_unparsed`. The fallback never guesses a
     country code: a guessed code turns a real number into someone else's number.

Install the real engine with `pip install phonenumbers` for any non-US data.

Shared lines: when one number appears on records with two or more different last names,
it is flagged `shared_phone` and scores as weak evidence. It is almost always an office
main line or a household line.

## Person names

- Case is fixed only when the name is ALL CAPS or all lower case. `McDonald`, `van der
  Berg`, and `DeShawn` stay as they are. Casing rules for `Mc` and `O'` apply only when
  the case is being fixed anyway.
- A "Full Name" column is split on the first space when there's no first/last column. The
  split is a guess, so check it before importing split names back.
- Match key: accents are stripped and letters lowercased. Punctuation is dropped, and
  hyphens become spaces, so `O'Brien` matches `OBrien` and `Carter-Hayes` shares a token
  with `Carter`.
- Nicknames: a small canonical map (`bob` to `robert`, `liz` to `elizabeth`, and so on)
  used for matching only. The stored first name is never rewritten to the formal version.
- An initial is compatible with any first name that starts with the same letter
  (`L.` and `Luis`), at reduced confidence.

Name similarity is 0.4 times the first-name score plus 0.6 times the last-name score, each
scored with rapidfuzz `ratio`. Last names get more weight because typos in them are rarer
and they separate people better.

## Company names and domains

Company match key: lowercase, accents stripped, `&` turned into `and`, punctuation
removed, a leading `The` dropped, and trailing legal suffixes removed over and over:
`inc incorporated llc llp lp ltd limited corp corporation co company plc gmbh ag sa sas
sarl srl spa bv nv pty pvt oy ab as kk kg ohg pllc pc`. After that, `The Tyrell
Corporation` and `Tyrell Corp` both reduce to `tyrell`. Words like `Holdings`, `Group`,
and `International` are **not** removed, because they often mark a separate legal entity.

Domain: the scheme (`http://`), the `www.` prefix, the path, the port, and the query
string are removed. The domain comes from the website column first. If that's empty, it
comes from the email domain, as long as the email isn't free mail. Subdomains are kept,
because `eu.example.com` can be a separate business unit. Merge those by hand.

Why a matching name isn't enough for companies: `Umbrella Ltd (umbrella.co.uk)` and
`Umbrella Corporation (umbrellacorp.com)` share a match key and can still be unrelated.
When names match but domains differ, the pair always goes to review.

## State, province, country

- Country goes to [ISO 3166-1 alpha-2](https://www.iso.org/iso-3166-country-codes.html)
  (`United States of America` becomes `US`, `UK` becomes `GB`, `Deutschland` becomes
  `DE`). Note that the correct ISO code for the United Kingdom is `GB`, not `UK`.
- US states go to [USPS two-letter codes](https://pe.usps.com/text/pub28/28apb.htm).
  Canadian provinces go to their two-letter postal codes (`Ontario` becomes `ON`). A state
  name is mapped only when the country is empty or matches, so that `Georgia` in a record
  whose country is `GE` isn't turned into a US state.
- Values the script can't recognize are left as-is. Check with the user before changing
  address data, because many CRMs sync these fields to billing systems.
- If the CRM uses picklists (Salesforce State and Country Picklists, HubSpot dropdowns),
  the import value has to match the picklist value or code exactly. Check which of the two
  the org expects.

## Lifecycle stage mapping

A canonical ladder is used to settle merge conflicts ("keep the furthest stage"):
`subscriber < lead < mql < sql < opportunity < customer < evangelist`.

| Canonical | HubSpot internal value | Salesforce (typical Lead Status or Opportunity) | Pipedrive / others |
|---|---|---|---|
| subscriber | `subscriber` | n/a (use a campaign member) | label or custom field |
| lead | `lead` | Open, New | label |
| mql | `marketingqualifiedlead` | custom status | label |
| sql | `salesqualifiedlead` | Working, Qualified | label |
| opportunity | `opportunity` | converted, with an open Opportunity | open deal |
| customer | `customer` | Closed Won Opportunity | won deal |
| evangelist | `evangelist` | custom | label |

HubSpot's default stages have fixed text internal names, while **custom stages have
numeric internal IDs**
([create and customize lifecycle stages](https://knowledge.hubspot.com/object-settings/create-and-customize-lifecycle-stages)).
Always map on the internal value, never the label, and extend `LIFECYCLE_MAP` in the
script to cover a portal's custom stages. The script writes the original raw value back,
never the canonical label, so the import still matches the CRM's picklist.

Salesforce lead statuses are defined per org, so read the org's picklist before mapping.
HubSpot tools (import, forms, API, workflows) only move the default lifecycle stage
forward. To set an earlier stage, you have to clear the value first
([use lifecycle stages](https://knowledge.hubspot.com/records/use-lifecycle-stages)). So
importing an "earlier" stage fails silently, which is one more reason to keep the furthest
stage.

## Dates

Dates are parsed with pandas and treated as UTC. 12- or 13-digit integers are read as
epoch milliseconds, which is the HubSpot API export style. In cleaned files the original
string is kept as-is; parsed dates are used only to pick the earliest create date, the
latest activity, and staleness. Staleness defaults to no activity (or no create date, when
there's no activity) in `--stale-days 365` days before `--as-of`.

## Record flags

| Flag | Meaning | Default action |
|---|---|---|
| `invalid_email` | the address doesn't parse | fix or clear; never delete the record for this alone |
| `email_domain_typo` | common misspelled provider domain | confirm with the owner, then fix |
| `role_email` | shared role inbox | keep; never auto-merge on it |
| `shared_phone` | line used by several people | keep; weak match evidence |
| `no_contact_method` | no valid email and no parsed phone | candidate for archive |
| `phone_unparsed` | the number can't be normalized safely | fix by hand |
| `junk_or_test` | test, asdf, fake, and similar | candidate for delete after review |
| `missing_name` | no first or last name | enrich or accept |
| `stale` | no activity within the stale window | archive or re-engage; don't delete |

Flags are computed per source record, before merging. A stale loser merged into an
active survivor stops mattering, so read `_flags` on `cleaned_contacts.csv` for what
survives.
