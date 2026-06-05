# Output Templates

Templates for every generated artifact and the directory layout that holds them.

## Output Directory Structure

```
meeting-outputs/
  {date}-{meeting-slug}/
    meeting-summary.md           # Complete meeting summary
    follow-up-email.md           # Ready-to-send follow-up
    action-items.yaml            # All action items in structured format
    tasks/
      linear/                    # Linear-compatible task files
        A-001.md
        A-002.md
      github/                    # GitHub Issues-compatible files
        A-001.md
        A-002.md
      generic/                   # Generic YAML task files
        A-001.yaml
        A-002.yaml
    raw/
      transcript.md              # Original transcript (preserved)
      extraction-log.md          # Log of extraction decisions and confidence scores
```

## Output 1: Meeting Summary (meeting-summary.md)

```markdown
# Meeting Summary: [Title]
**Date**: [Date]
**Duration**: [Duration]
**Participants**: [List]
**Type**: [Meeting type]

---

## Summary

[2-3 paragraph narrative summary of the meeting. What was discussed, what was decided,
and what needs to happen next. Written for someone who was not in the meeting.]

---

## Decisions Made

| # | Decision | Made By | Confidence |
|---|----------|---------|------------|
| D-001 | [Decision statement] | [Name] | [High/Medium/Low] |

---

## Action Items

| # | Action | Owner | Deadline | Priority | Type |
|---|--------|-------|----------|----------|------|
| A-001 | [Action statement] | [Name] | [Date] | [H/M/L] | [Type] |

### Implicit Commitments Detected

These items were not explicitly called out as action items but represent commitments made during the meeting:

| # | Commitment | Who Said It | Original Quote |
|---|-----------|-------------|----------------|
| A-XXX | [Interpreted action] | [Name] | "[exact quote]" |

---

## Open Questions

| # | Question | Raised By | Assigned To | Deadline |
|---|----------|-----------|-------------|----------|
| Q-001 | [Question] | [Name] | [Name] | [Date] |

---

## Parking Lot

| Topic | Raised By | Follow-Up |
|-------|-----------|-----------|
| [Topic] | [Name] | [When/Where] |

---

## Discussion Notes

### [Topic 1]
[Summary of discussion]

### [Topic 2]
[Summary of discussion]
```

## Output 2: Individual Task Files

Generate one task file per action item in a format compatible with the user's project management tool.

### Linear-Compatible Format (tasks/linear/)

```markdown
---
title: "[Action item title]"
assignee: "[Owner name]"
priority: "[urgent|high|medium|low]"
status: "Todo"
labels: ["meeting-action", "[project]"]
due_date: "[YYYY-MM-DD]"
---

## Description

[Detailed description of the task]

## Context

This action item came from the [Meeting Title] meeting on [Date].

**Original quote**: "[Source quote from transcript]"

**Related decisions**: [List any related decisions]

## Acceptance Criteria

- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]

## Dependencies

- [List dependencies]
```

### GitHub Issues Format (tasks/github/)

```markdown
---
title: "[Action item title]"
assignees: ["[github-username]"]
labels: ["meeting-action", "[priority]"]
milestone: "[if applicable]"
---

## Description

[Detailed description]

## Context

From: [Meeting Title] ([Date])
Owner: [Name]
Deadline: [Date]
Priority: [Priority]

## Tasks

- [ ] [Subtask 1]
- [ ] [Subtask 2]

## Related

- Decision: [Related decision]
- Meeting: [Link to meeting summary]
```

### Generic Task Format (tasks/generic/)

```yaml
task:
  id: "A-001"
  title: ""
  description: ""
  owner: ""
  deadline: ""
  priority: ""
  status: "open"
  tags: []
  subtasks: []
  notes: ""
  source: "Meeting: [Title] on [Date]"
```

## Output 3: Follow-Up Email Draft (follow-up-email.md)

```markdown
Subject: [Meeting Title] - Summary and Action Items ([Date])

Hi team,

Thank you for the productive meeting today. Here is a summary of what we covered,
the decisions we made, and the action items with owners and deadlines.

## Key Decisions
[Numbered list of decisions]

## Action Items
[Table of action items with owners and deadlines]

## Open Questions
[List of questions that still need answers]

## Next Meeting
[Date/time of next meeting, if known]

Please review the action items assigned to you and let me know if any deadlines
need to be adjusted.

Best,
[Name]
```
