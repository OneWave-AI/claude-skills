# Detection Markers and Inference Rules

Lookup tables for identifying decisions, action items, and implicit commitments, plus the rules for inferring priority and deadlines.

## Decision Markers

Explicit decision markers:
- "We decided to..."
- "Let's go with..."
- "The decision is..."
- "We're going to..."
- "We agreed that..."
- "Final answer is..."
- "Approved."
- "Let's move forward with..."
- "That's the plan."

Implicit decision markers:
- Consensus after debate: multiple people agreeing on a direction after discussion
- Leader pronouncement: a senior person stating direction without objection
- Default by silence: proposal made with no objection raised
- Conditional decision: "If X, then we'll do Y"

## Action Item Markers

Explicit action item markers:
- "I will..."
- "Can you [do X]?"
- "Let's [do X] by [date]"
- "[Name] will..."
- "Action item: ..."
- "TODO: ..."
- "Next step is..."
- "We need to..."
- "Make sure to..."
- "Follow up on..."
- "Schedule a..."
- "Send [something] to [someone]"
- "Update [something]"
- "Review [something]"
- "Prepare [something]"
- "Set up [something]"

Implicit commitment markers (critical -- people often do not realize they committed):
- "I'll look into that" = ACTION: Research and report back
- "Let me check" = ACTION: Investigate and share findings
- "I can probably..." = ACTION: Attempt and confirm
- "We should..." (when said by someone with authority) = ACTION: Do it
- "That's a good point, let me think about it" = ACTION: Consider and respond
- "I'll circle back on that" = ACTION: Follow up
- "Let me talk to [person]" = ACTION: Have conversation and report back
- "I think we need to..." (with group agreement) = ACTION: Initiate
- "Yeah, I can do that" = ACTION: Explicit acceptance of task
- "I'll take care of it" = ACTION: Ownership accepted
- "We'll figure it out" = ACTION: Needs decomposition into specific tasks
- "I'll ping you" = ACTION: Send follow-up communication
- "Let me get you that" = ACTION: Provide deliverable

## Priority Inference Rules

- HIGH: Mentioned as urgent, blocking other work, has a tight deadline, or requested by a senior leader
- MEDIUM: Standard action item with a deadline, part of normal workflow
- LOW: Nice-to-have, exploratory, no deadline mentioned

## Deadline Inference Rules

- Explicit: "by Friday", "before the next meeting", "end of week"
- Inferred from context: "before the launch" (if launch date is known), "before the next sprint"
- Meeting cadence: If it is a weekly meeting, default deadline is "before next meeting" (1 week)
- If no deadline signal at all: Mark as "TBD" and flag for owner to set

## Confidence Scoring

- HIGH: Clear, explicit statement. Speaker named. Unambiguous meaning.
- MEDIUM: Reasonable inference from context. Speaker identifiable. Meaning is likely correct but could be interpreted differently.
- LOW: Implicit commitment or ambiguous statement. Speaker may be unclear. Flag for human review.

For LOW confidence items, always flag them for review:

```
[LOW CONFIDENCE] The following items were extracted but may not be accurate.
Please review and confirm or remove:

- A-XXX: [Action] - Assigned to [Name]
  Reason for low confidence: [Explanation]
  Original quote: "[Quote]"
```
