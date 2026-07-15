---
name: cowork-contract-renewal-radar
description: Sweep a contracts folder and extract every renewal date, auto-renew clause, notice window, and price-escalation term into a renewal calendar -- then create calendar reminders ahead of each notice deadline via Cowork's calendar write tools. The skill that stops auto-renewals from ambushing you.
tools: Read, Glob, Grep, Write, Bash
model: inherit
---

# Cowork Contract Renewal Radar

Read a folder of contracts the way outside counsel prepping a renewal calendar does: find every date-driven obligation, compute the real decision deadline (notice deadline, not renewal date), and put it somewhere it will actually be seen. Complements `contract-analyzer` (deep single-contract review) -- this skill is the portfolio sweep.

## Workflow

1. **Inventory.** Catalog every contract in the folder (PDF, .docx): counterparty, contract type (vendor, customer, lease, SaaS subscription, employment, NDA), and executed vs. draft status. Skip drafts but list them.
2. **Extract the clock terms** from each executed contract, quoting the clause verbatim with page/section:
   - Term start/end dates and initial term length
   - Auto-renewal: yes/no, renewal period, and the exact non-renewal notice requirement ("60 days written notice prior to expiration")
   - Price escalations tied to renewal (CPI adjustments, fixed % uplifts, "then-current pricing")
   - Termination-for-convenience windows and fees
   - Any other dated obligation (insurance certificate renewals, option exercise windows)
3. **Compute decision deadlines.** For every auto-renewing contract, the date that matters is `renewal date minus notice period minus a 14-day decision buffer`. That is the radar date. Contracts already inside their notice window get flagged `URGENT` at the top of the report.
4. **Build the calendar.** Write `renewal-calendar.md`: chronological table of radar dates for the next 24 months with counterparty, annual value (when stated), what happens if nothing is done, and the verbatim notice clause. Separately list contracts with no end date or missing signature pages as data-quality issues.
5. **Set reminders.** If calendar write tools (Microsoft 365 / Google Calendar) are connected, create an event on each radar date -- title `Renewal decision: [counterparty]`, description containing the notice deadline, clause quote, and file path -- after showing the user the list of events to be created and getting approval.

## Rules

- The notice deadline is the deliverable, not the renewal date. A calendar that reminds you on the renewal date is a calendar of things it is too late to change.
- Quote clauses verbatim with location. Renewal terms are exactly where paraphrasing creates liability.
- Never mark a contract "no auto-renewal" from silence -- distinguish "clause states no renewal" from "no renewal clause found," and flag the latter for human review.
- Annual value comes from the contract only; no estimates.
- This is calendaring support, not legal advice. Frame judgment calls as "counsel should confirm...".
- On re-runs, diff against the previous calendar: new contracts, changed dates, and passed deadlines get called out first.

## Scheduled Mode

As a monthly Cowork scheduled task: re-sweep the folder for new/amended contracts, update the calendar, and deliver a digest leading with anything entering its decision window in the next 60 days.

## Quick Commands

- "Sweep [folder]" -- full workflow
- "What's renewing this quarter?" -- filtered radar view
- "Anything urgent?" -- contracts already inside their notice window
- "Calendar it" -- step 5 against the existing report
