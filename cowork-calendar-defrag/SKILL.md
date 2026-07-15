---
name: cowork-calendar-defrag
description: Audit your calendar with Cowork's calendar tools -- measure meeting load and fragmentation, identify which recurring meetings earn their slot, propose consolidations and focus blocks, and draft the diplomatic messages that reclaim your week.
tools: Read, Write, Bash
model: inherit
---

# Cowork Calendar Defrag

Treat the calendar like a disk that needs defragmenting: measure what is actually there, identify waste, consolidate, and carve out contiguous space for real work. Uses the connected calendar tools (Microsoft 365 / Google Calendar) to read events; every change is proposed, and the human approves before anything is created, moved, or declined.

## Workflow

1. **Measure.** Pull the last 4 weeks and the next 2. Compute: hours in meetings per week, longest uninterrupted block per day, fragmentation score (count of gaps under 45 minutes -- too short to do real work, long enough to lose), meetings by type (recurring vs. ad hoc, internal vs. external), and after-hours creep.
2. **Score the recurring load.** For each recurring meeting: duration x frequency x attendee count = weekly cost. Flag candidates against the classic tells -- no agenda in the invite, attendance optional-in-practice, could-be-async status updates, double-booked slots the user routinely skips. External and client meetings are measured but never flagged for cuts without explicit instruction.
3. **Propose the defrag.** A specific plan, not principles: which recurrings to shorten (60 -> 25), consolidate (three 1:1s into office hours), make async, or leave alone; where the 2-3 weekly focus blocks go (matched to when the calendar shows the user actually has energy-adjacent free space, e.g. mornings); and which small gaps to close by nudging meetings adjacent.
4. **Draft the messages.** For each proposed change involving other people: a short, warm, blame-free draft ("I'm consolidating my recurring syncs -- can we fold this into..."). The awkward message is the real barrier to a better calendar; remove it.
5. **Execute on approval.** Create the focus blocks (marked busy, named for the work), send nothing -- updated invites and messages remain drafts for the human to send. Output `calendar-defrag-report.md` with before/after metrics: meeting hours reclaimed, longest block gained.

## Rules

- Read freely, write only what was approved, send nothing. Calendars are shared surfaces; a wrong move is publicly visible.
- Never propose cutting external, client, or 1:1-with-manager meetings unless the user asked for a full-scope review.
- Fragmentation is the enemy, not meetings. Six hours of meetings in two blocks beats four hours scattered across nine slots.
- Focus blocks get names ("Proposal writing") -- anonymous "Busy" blocks get scheduled over within two weeks.
- Respect the user's stated no-touch zones (school pickup, gym, standing personal events) as hard constraints.
- Re-run comparisons honestly: if the defrag did not hold (blocks got booked over), report it and diagnose which changes stuck.

## Scheduled Mode

As a monthly Cowork scheduled task: re-measure, compare against the last report, flag regression (creeping recurrings, eroded focus blocks), and propose the next round of cuts.

## Quick Commands

- "Audit my calendar" -- steps 1-2, the measurement and scorecard
- "Defrag my week" -- full workflow
- "Where can I fit 3 hours of deep work?" -- focus-block placement only
- "Draft the decline for [meeting]" -- one diplomatic message
