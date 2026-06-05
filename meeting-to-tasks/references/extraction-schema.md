# Extraction Schema

Structured fields to capture during each extraction phase. Always preserve the exact source quote that produced each item.

## Phase 1: Meeting Metadata

```yaml
meeting:
  title: ""                # Inferred from content or asked
  date: ""                 # Extracted or today's date
  duration: ""             # If available
  type: ""                 # standup, planning, review, brainstorm, 1:1, all-hands, client, etc.
  participants:
    - name: ""
      role: ""             # Inferred from context (facilitator, presenter, decision-maker, etc.)
  agenda_items: []         # If an agenda was referenced
  context: ""              # Brief description of what the meeting was about
```

## Phase 2: Decisions

```yaml
decisions:
  - id: "D-001"
    decision: ""           # Clear statement of what was decided
    context: ""            # What led to this decision
    made_by: ""            # Who made or confirmed the decision
    participants: []       # Who was present for the decision
    confidence: ""         # high, medium, low (how clearly was this a decision?)
    conditions: ""         # Any conditions or caveats
    reversibility: ""      # easy, moderate, hard (can this be undone?)
    source_quote: ""       # Exact quote from transcript
```

## Phase 3: Action Items

```yaml
action_items:
  - id: "A-001"
    title: ""              # Clear, concise action statement (imperative mood)
    description: ""        # Detailed description with context
    owner: ""              # Person responsible
    collaborators: []      # Others involved
    deadline: ""           # Explicit deadline, inferred deadline, or "TBD"
    priority: ""           # high, medium, low (inferred from urgency signals)
    status: "open"         # open, in-progress, blocked, done
    type: ""               # task, research, decision-needed, follow-up, communication
    dependencies: []       # Other action items this depends on
    related_decisions: []  # Decision IDs this action relates to
    commitment_type: ""    # explicit, implicit, inferred
    source_quote: ""       # Exact quote from transcript
    confidence: ""         # high, medium, low (how certain is it this is an action item?)
    project: ""            # Which project or workstream this belongs to
    tags: []               # Categorization tags
```

## Phase 4: Open Questions

```yaml
open_questions:
  - id: "Q-001"
    question: ""           # The question as stated
    raised_by: ""          # Who asked
    context: ""            # Why it matters
    assigned_to: ""        # Who should answer (if identified)
    deadline: ""           # When an answer is needed
    related_items: []      # Related decisions or action items
    source_quote: ""
```

## Phase 5: Parking Lot

```yaml
parking_lot:
  - id: "P-001"
    topic: ""
    raised_by: ""
    reason_deferred: ""    # Why it was not addressed
    follow_up_meeting: ""  # When it should be revisited
```

## Phase 6: Key Discussion Points

```yaml
discussion_points:
  - topic: ""
    summary: ""            # 2-3 sentence summary
    participants: []       # Who contributed
    outcome: ""            # decision, action, deferred, informational
    time_spent: ""         # estimated, if timestamps available
```
