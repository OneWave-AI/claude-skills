# Worked example: a 12-month operating forecast

The user shares `broken_model.xlsx` (build it with `python3 tests/build_fixtures.py`) and asks: "Can you check this forecast before I send it to the board? The opex total looks low."

It has five tabs: Inputs, Forecast (12 months plus a Total column), Commissions (one row per rep), Metrics, and a hidden Scratch tab.

## 1. Run the script

```bash
python3 scripts/audit_xlsx.py broken_model.xlsx --json audit.json --md audit.md
```

The first run says `cached values: NO`. The file was written by a script and never calculated, so the value checks were skipped. Re-run it with recalculation:

```bash
python3 scripts/audit_xlsx.py broken_model.xlsx --recalc --json audit.json --md audit.md
```

```
summary: critical 2, high 21, medium 10, low 3, info 6
```

Excerpt of `audit.md`:

```
## Critical
### circular reference (1)
- F001 `Metrics!B7` Circular loop of 2 cell(s): Metrics!B7, Metrics!B8.  `=B8*0.02`
### error value (1)
- F002 `Metrics!B4` #REF! (root cause; 0 direct dependents also in error).  `=#REF!*2`

## High
### double count (1)
- F003 `Metrics!B5` Range Commissions!D:D includes subtotal D8 (=SUM(D2:D7)) and the rows it sums.
### error value (2)
- F004 `Metrics!B2` #DIV/0! (root cause ...)  `=Forecast!N4/B3`
- F005 `Metrics!B10` #N/A (root cause ...)  `=[1]Inputs!B2`
### inconsistent formula (3)
- F007 `Forecast!F5` Breaks the row pattern (middle of a 12-cell run; 11 cells follow B5: =B4*Inputs!$B$5).  `=F4*0.35`
- F008 `Forecast!J9` Breaks the row pattern (... 11 cells follow B9: =B4*Inputs!$B$6).  `=J4*Inputs!$B$7`
- F009 `Forecast!E12` Breaks the row pattern (... 11 cells follow B12: =B6-B11).  `=E6-E11+E16`
### pasted over formula (1)
- F010 `Forecast!H4` Typed value 52000 between formulas that match (G4: =G2*G3).
### sum range omission (12)
- F011 `Forecast!B11` SUM skips adjacent data cell(s): B10.  `=SUM(B7:B9)`
  ... (C11 through M11, the same)
### total does not foot (1)
- `Commissions!B8` Typed total 250000 but the 6 cells above sum to 253000 (off by -3000).

## Medium
- `Inputs!B3` Percent-formatted input holds 3 (displays as 300%).
- `Forecast` hidden row 16 holds 2 cells (0 formulas, 1 feeding visible formulas).
- `Scratch` sheet is hidden with 2 populated cells (1 formula).
- `Metrics!B2` references empty cell(s): B3.   `Metrics!B11` uses INDIRECT.
- hardcoded 0.35 in Forecast!F5, 0.02 in Metrics!B7, 0.1 in Scratch!B1
## Low
- `Forecast!G14` Input 2 is ~0.001x the row median 2000.
- `Forecast row 15` 'Refunds' mixes positive (2) and negative (10) inputs.
- `Metrics!B12` uses TODAY.
```

## 2. Triage

Checking the flagged cells against the rest of the workbook:

- **F011-F022 are one problem.** Software (row 10) was added under the opex block, and `Total opex` still sums rows 7-9 in every month. Opex is understated by 1,200 a month (the Inputs software cost), 14,400 for the year. That explains why "the opex total looks low".
- **Inputs!B3 is the biggest problem in the file.** Monthly growth is typed as `3` in a percent cell, so units grow 300% a month. December units come out at 4.2 billion. No formula is wrong; one input is.
- **F008 (J9)** multiplies September revenue by rent (4,000) instead of the 8% commission rate. That single cell makes Total opex worthless.
- **F007 (F5)** hardcodes 35% COGS in May. It matches the input today, so the damage is latent, but the next COGS change will skip May.
- **F010 (H4)** July revenue was pasted as 52,000. It will not move with price or volume.
- **F009 + hidden row 16** are the same issue: a hidden "Manual adj" of 7,500 is added into April operating income. Ask the owner about it; do not delete it silently.
- **Commissions!B8** is a typed total of 250,000 against 253,000 of rep bookings. The commission column itself is calculated, so payouts are right, but the bookings number that would go in the deck is 3,000 short.
- **Metrics tab**: the circular fee (B7/B8), the `#REF!` in B4, the `#DIV/0!` from a blank customer count, the whole-column SUM that double counts commissions, and the broken link to `Budget FY25.xlsx` are all real. None of them feed the Forecast, so they are fix-before-sharing items rather than forecast errors.
- The unit outlier in G14 (marketing 2 vs 2,000) and the mixed-sign Refunds row are real smells. Mention them as low severity and ask about them.

## 3. Judgment pass (after structural fixes)

With growth set to 0.03, the SUM extended, and J9/F5/H4 restored, the model gives FY revenue of 695,409, gross profit of 452,016, opex of 478,033, and an **operating loss of 26,017**.

The assumption review turns up two points:

- Growth of 3% a month is 43% a year. Is that consistent with the last 12 months of actuals? The model has no actuals tab, so ask.
- COGS at 35% and commission at 8% are flat all year, with no volume discount and no commission accelerators. Is that intended?

Sensitivity on the top three drivers (FY operating income):

| Driver | -10% | Base | +10% |
|---|---|---|---|
| Price per unit (49) | -65,655 | -26,017 | +13,621 |
| Starting units (1,000) | -65,655 | -26,017 | +13,621 |
| Payroll (30,000/mo) | +9,983 | -26,017 | -62,017 |

A 10% move in price, volume, or payroll changes the answer from a loss to a profit. That belongs in the verdict.

## 4. Final report to the user

```
## Verdict
Do not send yet. One typed input (monthly growth entered as 3 instead of 3%) makes
every revenue number wrong by orders of magnitude, and the opex total leaves out
Software in all 12 months (-14,400/yr). Once the fixes below are made, the model
shows a 26k operating loss that flips to a profit with a 10% move in price, volume,
or payroll.

## Must fix
1. Inputs!B3 -- growth typed as 3 (300%/month) -- all revenue, COGS, commission
   wrong -- enter 0.03.
2. Forecast!B11:M11 -- Total opex =SUM(B7:B9) omits Software (row 10) -- opex
   understated 1,200/month -- change to =SUM(B7:B10) across.
3. Forecast!J9 -- September commission multiplies by rent (Inputs!B7) instead of
   the commission rate (Inputs!B6) -- copy I9 across.
4. Forecast!H4 -- July revenue typed as 52,000 -- restore =H2*H3.
5. Forecast!E12 + hidden row 16 -- hidden 7,500 "Manual adj" added to April
   operating income -- confirm with owner; if real, unhide and label it.
6. Commissions!B8 -- typed total 250,000 vs 253,000 of detail -- =SUM(B2:B7).
7. Metrics tab -- circular fee (B7/B8), #REF! (B4), #DIV/0! (B2, blank customer
   count in B3), SUM(Commissions!D:D) double counts the total row, broken link to
   Budget FY25.xlsx (B10).

## Should fix
- Forecast!F5 hardcodes 35% COGS -- reference Inputs!B5 like the other months.
- Metrics!B11 INDIRECT -- replace with a direct reference.
- Hidden Scratch tab with a 10% plug on operating income -- delete if dead.

## Worth knowing
- Forecast!G14 marketing = 2 where every other month is 2,000 (units?).
- Refunds row mixes signs (two months positive).
- 83 references from Forecast into Inputs; inputs are centralized, which is good.

## Assumption review (judgment)
| Input | Value | Concern |
| Monthly growth | 3% | 43%/yr compounding; no actuals to support it |
| COGS % | 35% | flat all year; any volume discount? |
| Commission | 8% | no accelerators or clawbacks modeled |

## Sensitivity
(table above)

## Not checked
INDIRECT target in Metrics!B11; the linked Budget FY25.xlsx; no cash-flow tab
exists, so timing of collections is not modeled.
```
